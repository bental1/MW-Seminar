import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
plt.rcParams["font.family"] = ["Carlito", "Calibri", "DejaVu Sans"]   # Carlito = metric-compatible Calibri

# Four stocks, sixteen days, eta = 0.4.  Costs are daily losses in [-1, 1].
# AutoCo starts crashing on day 5, RetailCo on day 9, EnergyCo drifts up.
# Left: what the market does.  Right: where MW puts its probability mass.

BLACK  = "#1a1a1a"
ORANGE = "#E08E45"
PURPLE = "#6C4AB6"
GREEN  = "#4A8C6F"
GREY   = "#777777"

names = ["TechCo", "AutoCo", "RetailCo", "EnergyCo"]
cols  = [BLACK, ORANGE, PURPLE, GREEN]
T, eta = 16, 0.4
rng = np.random.default_rng(3)

cost = np.zeros((4, T))
cost[0] = rng.normal(0.0, 0.18, T)                       # TechCo: noise around zero
cost[1] = np.where(np.arange(1, T + 1) >= 5, 0.55, 0.0) + rng.normal(0, 0.10, T)   # AutoCo crashes day 5
cost[2] = np.where(np.arange(1, T + 1) >= 9, 0.50, 0.0) + rng.normal(0, 0.10, T)   # RetailCo crashes day 9
cost[3] = -0.15 + rng.normal(0, 0.10, T)                 # EnergyCo: steady gain
cost = np.clip(cost, -1, 1)

w = np.ones(4); P = []
for t in range(T):
    p = w / w.sum(); P.append(p)
    w = w * (1 - eta * cost[:, t])
P = np.array(P)                                          # P[t] = distribution used on day t+1
days = np.arange(1, T + 1)
cum = np.cumsum(cost, axis=1)

fig = plt.figure(figsize=(11.2, 3.9), dpi=200)

# ---- left: cumulative cost
axL = fig.add_axes([0.06, 0.17, 0.40, 0.70])
for i in range(4):
    axL.plot(days, cum[i], color=cols[i], lw=2.0)
    axL.text(T + 0.35, cum[i, -1], names[i], color=cols[i], fontsize=12, va="center")
axL.axhline(0, color="#cccccc", lw=1)
for d, lab in [(5, "AutoCo\ncrashes"), (9, "RetailCo\ncrashes")]:
    axL.axvline(d, color="#bbbbbb", lw=1.2, ls="--")
    axL.text(d + 0.2, cum.max() * 0.98, lab, fontsize=10.5, color=GREY, va="top", linespacing=1.25)
axL.set_xlim(1, T + 3.2)
axL.set_xticks([1, 5, 9, 13, 16])
axL.set_xlabel("day  t", fontsize=12.5)
axL.set_ylabel("cumulative cost", fontsize=12.5)
axL.set_title("what the market does", fontsize=12, color=GREY, pad=8)
axL.tick_params(labelsize=11)
axL.spines["top"].set_visible(False); axL.spines["right"].set_visible(False)

# ---- right: stacked probability
axR = fig.add_axes([0.56, 0.17, 0.40, 0.70])
axR.stackplot(days, P.T, colors=cols, alpha=0.92, linewidth=0)
mid = np.cumsum(P, axis=1) - P / 2
for i in range(4):
    d = 3 if i < 3 else 10
    axR.text(d, mid[d - 1, i], names[i], color="white", fontsize=11.5,
             ha="center", va="center", fontweight="bold")
axR.set_xlim(1, T)
axR.set_ylim(0, 1)
axR.set_xticks([1, 5, 9, 13, 16])
axR.set_yticks([0, 0.25, 0.5, 0.75, 1.0]); axR.set_yticklabels(["0", "¼", "½", "¾", "1"])
axR.set_xlabel("day  t", fontsize=12.5)
axR.set_ylabel("probability  pᵢ", fontsize=12.5)
axR.set_title("where MW puts its money", fontsize=12, color=GREY, pad=8)
axR.tick_params(labelsize=11)
axR.spines["top"].set_visible(False); axR.spines["right"].set_visible(False)

fig.savefig(str(Path(__file__).with_suffix(".png")), dpi=200, facecolor="white",
            bbox_inches="tight", pad_inches=0.06)
print("final p:", np.round(P[-1], 3))

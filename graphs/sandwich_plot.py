import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
plt.rcParams["font.family"] = ["Carlito", "Calibri", "DejaVu Sans"]   # Carlito = metric-compatible Calibri

# The sandwich from Part 4, on a real run:  w_best <= Phi <= n * exp(-eta * sum m.p).
# n = 8 decisions, T = 250 rounds, costs uniform in [-1, 1], eta = 0.1.
# Costs can be negative, so Phi is allowed to rise; both bounds still hold.

BLACK  = "#1a1a1a"
ORANGE = "#E08E45"
PURPLE = "#6C4AB6"
GREY   = "#777777"

n, T, eta = 8, 250, 0.1
rng = np.random.default_rng(5)
m = rng.uniform(-1, 1, (n, T))
m[2] -= 0.15                                   # give one decision a mild edge, so "best" is meaningful
m = np.clip(m, -1, 1)

w = np.ones(n); Phi = [n]; paid = 0.0; upper = [n]; wbest = []
best = int(np.argmin(m.sum(axis=1)))
wbest.append(1.0)
for t in range(T):
    p = w / w.sum()
    paid += m[:, t] @ p
    w = w * (1 - eta * m[:, t])
    Phi.append(w.sum()); upper.append(n * np.exp(-eta * paid)); wbest.append(w[best])
tt = np.arange(T + 1)

fig = plt.figure(figsize=(10.4, 3.7), dpi=200)
ax = fig.add_axes([0.085, 0.18, 0.66, 0.70])
ax.fill_between(tt, wbest, upper, color="#ececec", zorder=0)
ax.plot(tt, upper, color=ORANGE, lw=1.8, ls=":", zorder=2)
ax.plot(tt, Phi, color=BLACK, lw=1.9, zorder=3)
ax.plot(tt, wbest, color=PURPLE, lw=1.8, ls="--", zorder=2)

# three labels, stacked so they never collide (Phi and w_best end close together)
ys = sorted([("u", upper[-1]), ("p", Phi[-1]), ("w", wbest[-1])], key=lambda z: z[1])
ymax = max(upper) * 1.22
gap = ymax * 0.145
pos = {}
cur = -1e9
for k, y in ys:
    y = max(y, cur + gap); pos[k] = y; cur = y
over = pos["u"] - (ymax - gap * 0.55)
if over > 0:
    for k in pos: pos[k] -= over
ax.text(T * 1.02, pos["u"], "upper bound\nn·exp(−η Σ m·p)", color=ORANGE, fontsize=11.5,
        va="center", linespacing=1.3)
ax.text(T * 1.02, pos["p"], "Φ⁽ᵗ⁾, the actual\ntotal weight", color=BLACK, fontsize=11.5,
        va="center", linespacing=1.3)
ax.text(T * 1.02, pos["w"], "lower bound: the best\ndecision's own weight", color=PURPLE,
        fontsize=11.5, va="center", linespacing=1.3)
for k, y in [("u", upper[-1]), ("p", Phi[-1]), ("w", wbest[-1])]:
    if abs(pos[k] - y) > 1e-9:
        ax.plot([T, T * 1.015], [y, pos[k]], color=GREY, lw=0.8, clip_on=False)
ax.set_ylim(0, ymax)

ax.set_xlim(0, T)
ax.set_xticks([0, 50, 100, 150, 200, 250])
ax.set_xlabel("round  t", fontsize=12.5)
ax.set_ylabel("Φ⁽ᵗ⁾", fontsize=12.5)
ax.set_title("n = 8,  costs uniform in [−1, 1],  η = 0.1  —  costs can be negative, so Φ may rise",
             fontsize=11, color=GREY, pad=8, loc="left")
ax.tick_params(labelsize=11)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

fig.savefig(str(Path(__file__).with_suffix(".png")), dpi=200, facecolor="white",
            bbox_inches="tight", pad_inches=0.06)
print("Phi end", round(Phi[-1], 2), "| upper", round(upper[-1], 2), "| wbest", round(wbest[-1], 2))

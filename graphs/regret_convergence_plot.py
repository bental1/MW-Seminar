import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
plt.rcParams["font.family"] = ["Carlito", "Calibri", "DejaVu Sans"]   # Carlito = metric-compatible Calibri

# Average regret  regret/T  of MW versus the horizon T, n = 8 decisions,
# eta = sqrt(ln n / T) chosen per horizon.  Costs uniform in [0, 1], one decision
# with a mild edge.  Averaged over many random runs.  It tracks 2*sqrt(ln n / T).

BLACK  = "#1a1a1a"
ORANGE = "#E08E45"

n = 8
Ts = np.array([25, 50, 100, 200, 400, 800, 1600, 3200, 6400])
rng = np.random.default_rng(11)
R = 200
meas = []
for T in Ts:
    eta = np.sqrt(np.log(n) / T)
    tot = 0.0
    for _ in range(R):
        m = rng.uniform(0, 1, (n, T)); m[0] -= 0.1; m = np.clip(m, 0, 1)
        w = np.ones(n); paid = 0.0
        for t in range(T):
            p = w / w.sum(); paid += m[:, t] @ p; w *= (1 - eta * m[:, t])
        tot += (paid - m.sum(axis=1).min()) / T
    meas.append(tot / R)
meas = np.array(meas)
bound = 2 * np.sqrt(np.log(n) / Ts)

fig = plt.figure(figsize=(10.0, 3.7), dpi=200)
ax = fig.add_axes([0.09, 0.19, 0.88, 0.76])
ax.axhline(0, color="#cccccc", lw=1)
ax.plot(Ts, bound, ":", color=ORANGE, lw=2.2)
ax.plot(Ts, meas, "o-", color=BLACK, lw=1.9, ms=6)
ax.text(Ts[3], bound[3] + 0.03, "the bound:  2√(ln n / T)", color=ORANGE, fontsize=12.5, ha="left", va="bottom")
ax.text(Ts[3] * 1.15, meas[3] - 0.03, "measured average regret", color=BLACK, fontsize=12.5, ha="left", va="top")
ax.set_xscale("log")
ax.set_ylim(-0.02, 0.62)
ax.set_xlabel("horizon  T  (log scale)", fontsize=12.5)
ax.set_ylabel("regret / T", fontsize=12.5)
ax.set_title("n = 8,  η = √(ln n / T)", fontsize=11, color="#777777", loc="left", pad=6)
ax.tick_params(labelsize=11)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.savefig(str(Path(__file__).with_suffix(".png")), dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.06)
print(np.round(meas, 3))

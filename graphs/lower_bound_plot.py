import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
plt.rcParams["font.family"] = ["Carlito", "Calibri", "DejaVu Sans"]   # Carlito = metric-compatible Calibri

# Lemma 4.2, one picture and nothing else: how far below T/2 the BEST of the n
# decisions lands, as n grows.  It tracks sqrt(ln n).  Direct labels, no legend box.

BLACK  = "#1a1a1a"
ORANGE = "#E08E45"

T = 500
HALF = T / 2

fig = plt.figure(figsize=(8.0, 3.4), dpi=200)
ax = fig.add_axes([0.115, 0.185, 0.855, 0.755])

ns = np.array([2, 4, 8, 16, 32, 64, 128, 256, 512, 1024])
rng = np.random.default_rng(7)
K = 3000
sim = np.array([(HALF - rng.binomial(T, 0.5, size=(K, nn - 1)).min(axis=1)).mean()
                for nn in ns])

ref = np.sqrt(np.log(np.maximum(ns - 1, 1.0001)))
c = (sim @ ref) / (ref @ ref)

ax.plot(ns, c * ref, "--", color=ORANGE, lw=2.2, zorder=2)
ax.plot(ns, sim, "o-", color=BLACK, lw=1.8, ms=6, zorder=3)

ax.text(ns[-1] * 0.92, sim[-1] + 2.6, "measured", color=BLACK,
        fontsize=12.5, ha="right", va="bottom", fontweight="bold")
ax.text(24, c * np.sqrt(np.log(23)) + 3.4, "√(ln n)", color=ORANGE,
        fontsize=12.5, ha="center", va="bottom", fontweight="bold")

ax.set_xscale("log")
ax.set_ylim(0, sim.max() * 1.22)
ax.set_xlabel("number of decisions  n", fontsize=13)
ax.set_ylabel("how far below T/2\nthe best decision lands", fontsize=13, linespacing=1.4)
ax.tick_params(labelsize=11.5)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.savefig(str(Path(__file__).with_suffix(".png")), dpi=200, facecolor="white",
            bbox_inches="tight", pad_inches=0.06)
print("sim =", np.round(sim, 1))

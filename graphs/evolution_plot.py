import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
plt.rcParams["font.family"] = ["Carlito", "Calibri", "DejaVu Sans"]   # Carlito = metric-compatible Calibri

# Four variants of one gene, weak selection.  Each generation every allele's
# frequency is multiplied by (1 + s * fitness) and the population renormalises --
# which is literally w_i <- w_i (1 - eta m_i) with m_i = -fitness_i and eta = s.
# Same shape as the stock chart in Part 3, on purpose.

BLACK  = "#1a1a1a"
ORANGE = "#E08E45"
PURPLE = "#6C4AB6"
GREY   = "#777777"
LGREY  = "#b5b5b5"

alleles = ["A", "B", "C", "D"]
fitness = np.array([0.00, 0.03, 0.06, 0.02])     # relative fitness advantages
s = 0.5                                           # selection strength = eta
G = 260
freq = np.full(4, 0.25)
hist = [freq.copy()]
for g in range(G):
    freq = freq * (1 + s * fitness)               # the multiplicative update
    freq /= freq.sum()                            # renormalise
    hist.append(freq.copy())
hist = np.array(hist)

cols = [LGREY, PURPLE, ORANGE, BLACK]
fig = plt.figure(figsize=(9.6, 3.4), dpi=200)
ax = fig.add_axes([0.09, 0.19, 0.70, 0.73])
for i in range(4):
    ax.plot(hist[:, i], color=cols[i], lw=2.2 if i == 2 else 1.7, zorder=3 if i == 2 else 2)
    if i == 2:
        ax.text(G * 1.02, hist[-1, i], "allele C", color=cols[i],
                fontsize=11.5, va="center", ha="left", fontweight="bold")

ax.annotate("fittest variant\ntakes over", xy=(150, hist[150, 2]), xytext=(60, 0.80),
            fontsize=11, color=ORANGE, va="center", linespacing=1.3,
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.0, shrinkA=3, shrinkB=4))

ax.text(G * 1.02, 0.045, "A, B, D\nfade out", color=GREY, fontsize=11,
        va="center", ha="left", linespacing=1.3)
ax.set_xlim(0, G)
ax.set_ylim(0, 1.0)
ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_yticklabels(["0", "¼", "½", "¾", "1"])
ax.set_xlabel("generation", fontsize=12)
ax.set_ylabel("share of the population", fontsize=12)
ax.tick_params(labelsize=11)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.savefig(str(Path(__file__).with_suffix(".png")), dpi=200, facecolor="white",
            bbox_inches="tight", pad_inches=0.06)
print("final shares:", np.round(hist[-1], 3))

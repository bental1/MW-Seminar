import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np
plt.rcParams["font.family"] = ["Carlito", "Calibri", "DejaVu Sans"]   # Carlito = metric-compatible Calibri

# The biological setting behind Part 6, in one picture: a population of organisms,
# one gene with four alleles, one generation of selection.  Each dot is one organism,
# coloured by the allele it carries.  Same colours as the evolution chart.

BLACK  = "#1a1a1a"
ORANGE = "#E08E45"
PURPLE = "#6C4AB6"
GREY   = "#777777"
LGREY  = "#b5b5b5"
ACC    = "#8A5A28"

alleles = ["A", "B", "C", "D"]
cols    = [LGREY, PURPLE, ORANGE, BLACK]
fitness = np.array([0.00, 0.03, 0.06, 0.02])
s = 5.0                                     # exaggerated for one visible step
share0 = np.full(4, 0.25)
share1 = share0 * (1 + s * fitness); share1 /= share1.sum()

W, H = 12.6, 4.4
fig = plt.figure(figsize=(W, H), dpi=200)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

def population(x0, y0, shares, title, sub, seed):
    # 10 x 10 dots, counts rounded to 100, shuffled so it looks like a population
    counts = np.round(shares * 100).astype(int); counts[-1] = 100 - counts[:-1].sum()
    dots = np.repeat(np.arange(4), counts)
    rng = np.random.default_rng(seed); rng.shuffle(dots)
    for k, a in enumerate(dots):
        r, c = divmod(k, 10)
        ax.add_patch(plt.Circle((x0 + 0.16 + c * 0.30, y0 + 2.86 - r * 0.30), 0.115, color=cols[a], zorder=3))
    ax.text(x0 + 1.5, y0 + 3.35, title, ha="center", va="center", fontsize=14, color=BLACK, fontweight="bold")
    ax.text(x0 + 1.5, y0 - 0.32, sub, ha="center", va="center", fontsize=11.5, color=GREY)

def strip(x0, y, shares, label):
    xx = x0
    for a in range(4):
        w = 2.96 * shares[a]
        ax.add_patch(FancyBboxPatch((xx, y), w - 0.02, 0.22, boxstyle="round,pad=0,rounding_size=0.03",
                                    facecolor=cols[a], edgecolor="none", zorder=3))
        ax.text(xx + w / 2, y + 0.11, f"{alleles[a]} {int(round(shares[a]*100))}%", ha="center", va="center",
                fontsize=10.5, color="white" if a != 0 else BLACK, zorder=4, fontweight="bold")
        xx += w
    ax.text(x0 + 1.48, y - 0.22, label, ha="center", va="center", fontsize=11.5, color=GREY)

X1, X2, Y = 0.35, 8.05, 0.75
population(X1, Y, share0, "generation  t", "100 organisms, one dot each", 1)
strip(X1 + 0.02, Y - 0.72, share0, "the shares  =  the weights")
population(X2, Y, share1, "generation  t + 1", "the offspring, renormalised to 100", 2)
strip(X2 + 0.02, Y - 0.72, share1, "C grew, A shrank  —  a little")

# ---- middle: what happens in between
mx = (X1 + 3.0 + X2) / 2
ax.add_patch(FancyArrowPatch((X1 + 3.25, 2.25), (X2 - 0.25, 2.25), arrowstyle="-|>", mutation_scale=18,
                             color=GREY, lw=1.8, zorder=2))
ax.text(mx, 3.85, "one generation of selection", ha="center", va="center", fontsize=13, color=BLACK, fontweight="bold")
ax.text(mx, 3.20, "every carrier of allele i leaves\n1 + s · fitnessᵢ  offspring on average",
        ha="center", va="center", fontsize=11.5, color=BLACK, linespacing=1.4)
for k, (a, col) in enumerate(zip(alleles, cols)):
    ax.add_patch(plt.Circle((mx - 1.05, 1.62 - k * 0.34), 0.11, color=col, zorder=3))
    ax.text(mx - 0.82, 1.62 - k * 0.34, f"allele {a}:  fitness {fitness[k]:+.2f}", ha="left", va="center",
            fontsize=11, color=BLACK)
ax.text(mx, 0.22, "s  =  how strongly fitness matters  (the learning rate)", ha="center", va="center",
        fontsize=12, color=ACC, style="italic")

fig.savefig(str(Path(__file__).with_suffix(".png")), dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.06)
print(np.round(share1, 3))

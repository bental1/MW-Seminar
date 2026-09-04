import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
from pathlib import Path
plt.rcParams["font.family"] = ["Carlito", "Calibri", "DejaVu Sans"]   # Carlito = metric-compatible Calibri

# Left  : the rediscoveries the talk covered -- separate fields, no cross-citation.
# Centre: the 2012 survey, the paper that noticed they were one algorithm.
# Right : real papers that cite it, pulled from its citation list, 2010-2025.

BLACK  = "#1a1a1a"
ORANGE = "#E08E45"
GREY   = "#777777"
LGREY  = "#cfcfcf"

before = [
    ("1988", "Winnow", "learning theory"),
    ("1991", "Plotkin, Shmoys, Tardos", "linear programs"),
    ("1997", "AdaBoost", "boosting"),
]
after = [
    ("evolution under natural selection", "Chastain et al.,  PNAS 2014"),
    ("differentially private data release", "Hardt & Rothblum,  FOCS 2010"),
    ("quantum SDP solvers", "van Apeldoorn et al.,  FOCS 2017"),
    ("mixing the training data for an LLM", "Chen et al.,  ICLR 2025"),
    ("densest subgraph", "Nguyen et al.,  ICML 2024"),
    ("correlation clustering LPs", "Cao et al.,  STOC 2025"),
    
]

fig = plt.figure(figsize=(13.6, 4.0), dpi=200)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 13.6)
ax.set_ylim(0, 4.0)
ax.axis("off")

CX, CY = 5.20, 2.00
LX, RX = 2.80, 8.00          # where the lines start / end

yb = np.linspace(3.05, 0.95, len(before))
for (yr, who, what), y in zip(before, yb):
    ax.plot([LX + 0.14, CX - 0.92], [y, CY], color=LGREY, lw=1.5, zorder=1,
            solid_capstyle="round")
    ax.text(LX, y + 0.11, f"{yr}   {who}", ha="right", va="center",
            fontsize=12.5, color=BLACK)
    ax.text(LX, y - 0.19, what, ha="right", va="center",
            fontsize=11, color=GREY)

ya = np.linspace(3.42, 0.62, len(after))
for (topic, cite), y in zip(after, ya):
    ax.plot([CX + 0.92, RX - 0.10], [CY, y], color=ORANGE, lw=1.4, alpha=0.5,
            zorder=1, solid_capstyle="round")
    ax.text(RX, y + 0.085, topic, ha="left", va="center",
            fontsize=12.5, color=BLACK, fontweight="bold")
    ax.text(RX, y - 0.125, cite, ha="left", va="center",
            fontsize=10.5, color=ORANGE)

box = FancyBboxPatch((CX - 0.90, CY - 0.52), 1.80, 1.04,
                     boxstyle="round,pad=0.02,rounding_size=0.10",
                     facecolor=ORANGE, edgecolor="none", zorder=3)
ax.add_patch(box)
ax.text(CX, CY + 0.21, "2012", ha="center", va="center",
        fontsize=17, color="white", fontweight="bold", zorder=4)
ax.text(CX, CY - 0.20, "Arora, Hazan\n& Kale", ha="center", va="center",
        fontsize=11, color="white", linespacing=1.35, zorder=4)

ax.text(LX, 3.82, "found in three separate fields",
        ha="right", va="center", fontsize=10.5, color=GREY, style="italic")
ax.text(RX, 3.82, "a few of the papers that cite it",
        ha="left", va="center", fontsize=10.5, color=ORANGE, style="italic")

fig.savefig(str(Path(__file__).with_suffix(".png")), dpi=200, facecolor="white",
            bbox_inches="tight", pad_inches=0.06)
print("ok")

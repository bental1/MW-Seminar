import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from pathlib import Path
plt.rcParams["font.family"] = ["Carlito", "Calibri", "DejaVu Sans"]   # Carlito = metric-compatible Calibri

# One single run, shown twice, with the arithmetic spelled out.
#   Left   : the first 16 rounds of the cost matrix.
#   Middle : what each decision actually paid over those 16 rounds, and its
#            gap = 16/2 - cost.  8 = 16/2 is the no-skill baseline: it is what a
#            fair coin pays on average, and exactly what decision 1 pays.
#   Right  : the same run carried to t = 500, plotting that same gap at every t.

BLACK  = "#1a1a1a"
ORANGE = "#E08E45"
GREY   = "#777777"
LGREY  = "#bcbcbc"

T, n_coins = 500, 5
SHOW = 16
rng = np.random.default_rng(531)

costs = rng.integers(0, 2, (n_coins, T)).astype(float)
cum   = np.cumsum(costs, axis=1)
t     = np.arange(1, T + 1)
gap   = t / 2 - cum

lucky   = int(np.argmax(gap[:, -1]))
gap_end = gap[lucky, -1]
gap_16  = gap[:, SHOW - 1]
cost_16 = cum[:, SHOW - 1]

fig = plt.figure(figsize=(11.6, 3.55), dpi=200)
B, H = 0.185, 0.660

# ---------------------------------------------------------------- left: cost matrix
axL = fig.add_axes([0.048, B, 0.300, H])
grid = np.vstack([np.full((1, SHOW), 0.5), costs[:, :SHOW]])

axL.imshow(np.where(grid == 0.5, np.nan, grid), cmap="gray_r", vmin=0, vmax=1,
           aspect="auto", extent=[0.5, SHOW + 0.5, n_coins + 1.5, 0.5],
           interpolation="nearest")
axL.add_patch(Rectangle((0.5, 0.5), SHOW, 1.0, facecolor="#9a9a9a", edgecolor="none"))
axL.text(SHOW / 2 + 0.5, 1.0, "½  every round", ha="center", va="center",
         color="white", fontsize=10.5, fontweight="bold", zorder=6,
         bbox=dict(boxstyle="square,pad=0.15", facecolor="#9a9a9a", edgecolor="none"))

for k in range(SHOW + 1):
    axL.axvline(0.5 + k, color="white", lw=0.9)
for k in range(n_coins + 2):
    axL.axhline(0.5 + k, color="white", lw=0.9)

axL.add_patch(Rectangle((0.5, lucky + 1.5), SHOW, 1.0, facecolor="none",
                        edgecolor=ORANGE, lw=2.2, zorder=5))

axL.set_xticks([1, 4, 8, 12, 16])
axL.set_yticks(range(1, n_coins + 2))
axL.set_yticklabels(range(1, n_coins + 2))
axL.tick_params(labelsize=10.5)
axL.set_xlabel("round  t   (16 rounds played)", fontsize=11.5)
axL.set_ylabel("decision  i", fontsize=11.5)
axL.set_title("cost each round:  black = 1,  white = 0",
              fontsize=10, color=GREY, pad=8)
for s in axL.spines.values():
    s.set_visible(False)
for i, lab in enumerate(axL.get_yticklabels()):
    if i == lucky + 1:
        lab.set_color(ORANGE)
        lab.set_fontweight("bold")

# ------------------------------------- middle: the arithmetic that defines the gap
def numcol(left, header, values, d1, hot_fmt="{:+.0f}", fmt="{:+.0f}", box=False):
    ax = fig.add_axes([left, B, 0.078, H])
    ax.set_xlim(0, 1); ax.set_ylim(n_coins + 1.5, 0.5); ax.axis("off")
    ax.text(0.5, 1.02, header, ha="center", va="bottom", fontsize=9.8,
            color=GREY, linespacing=1.3, transform=ax.transAxes)
    ax.text(0.5, 1.0, d1, ha="center", va="center", fontsize=12, color=BLACK)
    for i, v in enumerate(values):
        hot = (i == lucky)
        if hot and box:
            ax.add_patch(Rectangle((0.03, i + 1.58), 0.94, 0.84, facecolor="none",
                                   edgecolor=ORANGE, lw=2.0))
        lab = (hot_fmt if hot else fmt).format(v)
        if lab in ("+0", "-0"):
            lab = "0"
        ax.text(0.5, i + 2.0, lab, ha="center", va="center",
                fontsize=13 if hot else 12,
                color=ORANGE if hot else BLACK,
                fontweight="bold" if hot else "normal")
    return ax

numcol(0.352, "cost paid\nover 16 rounds", cost_16, "8", fmt="{:.0f}", hot_fmt="{:.0f}")
numcol(0.442, "gap\n=  8 − cost\n(8 = 16 × ½)", gap_16, "0", box=True)

fig.text(0.437, 0.055, "largest gap  =  best in hindsight",
         ha="center", va="bottom", fontsize=10.5, color=ORANGE, fontweight="bold")

# ------------------------------------------------------------- right: the same run
axR = fig.add_axes([0.590, B, 0.272, H])
for i in range(n_coins):
    if i == lucky:
        continue
    axR.plot(t, gap[i], color=LGREY, lw=1.0, zorder=1)
axR.plot(t, gap[lucky], color=ORANGE, lw=1.9, zorder=3)
axR.axhline(0, color=BLACK, lw=1.4, ls="--", zorder=2)

ymax = gap.max() * 1.18
axR.set_ylim(gap.min() * 1.16, ymax)

axR.axvline(SHOW, color=ORANGE, lw=1.0, ls=":", zorder=2)
axR.plot([SHOW], [gap_16[lucky]], "o", ms=6.5, color=ORANGE, zorder=4)
axR.annotate(f"t = 16:  gap {gap_16[lucky]:+.0f}\n(from the table)",
             xy=(SHOW, gap_16[lucky]), xytext=(40, ymax * 0.99),
             fontsize=10, color=ORANGE, va="top", ha="left", linespacing=1.25,
             arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.9,
                             shrinkA=3, shrinkB=6))

axR.annotate("", xy=(T * 0.985, 0), xytext=(T * 0.985, gap_end),
             arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=1.5))
axR.text(T * 1.05, gap_end * 0.55,
         f"t = 500:  gap {gap_end:+.0f}\nthis gap is the\nregret, on average",
         fontsize=11, color=ORANGE, va="center", linespacing=1.35)
axR.text(T * 1.05, 0, "decision 1:\ngap 0 at every t", va="center",
         fontsize=11, color=BLACK, linespacing=1.3)

axR.set_xlim(-8, T * 1.02)
axR.set_xticks([0, 200, 400])
axR.tick_params(labelsize=10.5)
axR.set_xlabel("round  t   (same run, carried to 500)", fontsize=11.5)
axR.set_ylabel("gap  =  t/2 − cost so far", fontsize=11.5)
axR.set_title("the same gap, at every t", fontsize=10, color=GREY, pad=8)
axR.spines["top"].set_visible(False)
axR.spines["right"].set_visible(False)

fig.savefig(str(Path(__file__).with_suffix(".png")), dpi=200, facecolor="white")
print("lucky =", lucky + 2, "| cost16 =", cost_16, "| gap16 =", gap_16, "| gapT =", gap[:, -1])

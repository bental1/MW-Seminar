import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import sys
from pathlib import Path
plt.rcParams["font.family"] = ["Carlito", "Calibri", "DejaVu Sans"]   # Carlito = metric-compatible Calibri

# The journey (slide 2) as a horizontal flow, drawn once per part with that part lit.
# Goes on the dark section-divider slides, so it is drawn on the same dark ground.

BG = "#1a1a1a"; ORANGE = "#E08E45"; WHITE = "#ffffff"; DONE = "#a8a8a8"; DONE_FC = "#3c3c3c"; FUT = "#6e6e6e"; LINE = "#4a4a4a"
PARTS = [("I", "History"), ("II", "The problem"), ("III", "The algorithm"), ("IV", "The proof"),
         ("V", "The limits"), ("VI", "Nature"), ("VII", "Summary")]

def draw(cur, out):
    W, H = 12.2, 1.25
    fig = plt.figure(figsize=(W, H), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    n = len(PARTS); xs = [0.9 + k * (W - 1.8) / (n - 1) for k in range(n)]; cy = 0.78; r = 0.26
    for k in range(n - 1):
        ax.add_patch(FancyArrowPatch((xs[k] + r + 0.06, cy), (xs[k + 1] - r - 0.06, cy), arrowstyle="-|>",
                                     mutation_scale=12, color=ORANGE if k < cur else LINE, lw=1.4, zorder=1))
    for k, (num, lab) in enumerate(PARTS):
        if k == cur:   fc, ec, tc, lc, bold = ORANGE, ORANGE, WHITE, WHITE, True
        elif k < cur:  fc, ec, tc, lc, bold = DONE_FC, DONE_FC, DONE, DONE, False
        else:          fc, ec, tc, lc, bold = BG, FUT, FUT, FUT, False
        ax.add_patch(plt.Circle((xs[k], cy), r * (1.18 if k == cur else 1.0), facecolor=fc, edgecolor=ec, lw=1.4, zorder=2))
        ax.text(xs[k], cy, num, ha="center", va="center", fontsize=11 if k == cur else 10, color=tc, fontweight="bold", zorder=3)
        ax.text(xs[k], cy - r - 0.24, lab, ha="center", va="center", fontsize=12.5 if k == cur else 11.5,
                color=lc, fontweight="bold" if bold else "normal", zorder=3)
    fig.savefig(out, dpi=200, facecolor=BG, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)

if __name__ == "__main__":
    for k in range(7):
        draw(k, str(Path(__file__).with_name(f"roadmap_{k+1}.png")))
    print("ok")

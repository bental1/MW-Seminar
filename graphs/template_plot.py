import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams["font.family"] = ["Carlito", "Calibri", "DejaVu Sans"]   # Carlito = metric-compatible Calibri

# Slide 4: a meta-algorithm is a template with slots.  Fill the slots, get an algorithm.

BLACK = "#1a1a1a"; ORANGE = "#E08E45"; PURPLE = "#6C4AB6"; GREY = "#777777"; LGREY = "#ececec"; ACC = "#8A5A28"; TINT = "#F7EFE6"
W, H = 12.6, 4.0
fig = plt.figure(figsize=(W, H), dpi=200)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
def card(x, y, w, h, fc, ec="none", r=0.14, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", facecolor=fc, edgecolor=ec, lw=1.5, zorder=z))

# template
tx, ty, tw, th = 0.4, 0.45, 4.3, 3.1
card(tx, ty, tw, th, TINT, r=0.18)
ax.text(tx + tw / 2, ty + th - 0.38, "the template", ha="center", va="center", fontsize=13.5, color=ACC, fontweight="bold")
ax.text(tx + tw / 2, ty + th - 0.86, "wᵢ ← wᵢ (1 − η mᵢ)", ha="center", va="center", fontsize=15, color=BLACK)
slots = [("a round is", "?"), ("a weight wᵢ sits on", "?"), ("a cost mᵢ is", "?"), ("the rate η is", "?")]
for k, (a, b) in enumerate(slots):
    y = ty + th - 1.40 - k * 0.5
    card(tx + 0.35, y - 0.19, tw - 0.7, 0.38, "white", ec="#e0d3c2", r=0.08, z=3)
    ax.text(tx + 0.55, y, a, ha="left", va="center", fontsize=11.5, color=BLACK, zorder=4)
    ax.text(tx + tw - 0.55, y, b, ha="right", va="center", fontsize=11.5, color=ORANGE, fontweight="bold", zorder=4)

# arrow
ax.add_patch(FancyArrowPatch((tx + tw + 0.15, 2.0), (tx + tw + 1.35, 2.0), arrowstyle="-|>", mutation_scale=18, color=GREY, lw=1.8))
ax.text(tx + tw + 0.75, 2.32, "fill the slots", ha="center", va="center", fontsize=11.5, color=GREY, style="italic")

# instances
inst = [("AdaBoost  (1997)", ["a weak learner runs", "training example i", "1 if right, 0 if wrong", "γ, the learner's edge"], BLACK),
        ("PST linear programs  (1991)", ["an oracle is called", "constraint i", "(Aᵢx − bᵢ) / ρ", "ε / 4ℓ, the accuracy"], PURPLE),
        ("evolution  (PNAS 2014)", ["one generation", "allele i", "minus its fitness", "s, selection strength"], ORANGE)]
ix, iw, ih = tx + tw + 1.55, 6.05, 0.92
for k, (name, vals, col) in enumerate(inst):
    y = 3.55 - 0.16 - k * (ih + 0.14) - ih
    card(ix, y, iw, ih, "white", ec=col, r=0.12)
    ax.text(ix + 0.22, y + ih - 0.26, name, ha="left", va="center", fontsize=12, color=col, fontweight="bold")
    ax.text(ix + 0.22, y + 0.26, "   ·   ".join(vals), ha="left", va="center", fontsize=9.8, color=BLACK)
ax.text(ix + iw / 2, 0.22, "two applications from the survey, and one from far outside it", ha="center", va="center",
        fontsize=10.5, color=GREY, style="italic")
fig.savefig(str(Path(__file__).with_suffix(".png")), dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.06)
print("ok")

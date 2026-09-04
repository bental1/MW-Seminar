import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import sys
from pathlib import Path
plt.rcParams["font.family"] = ["Carlito", "Calibri", "DejaVu Sans"]   # Carlito = metric-compatible Calibri

# The online-decision game in one picture, drawn several times with different parts
# lit up, so Part 2 can walk through it step by step and Parts 4-5 can point back at it.
#   python setting_plot.py <variant>     variants: story, symbols, adversary, regret, all, coins

BLACK  = "#1a1a1a"; ORANGE = "#E08E45"; PURPLE = "#6C4AB6"; GREY = "#777777"; LGREY = "#ececec"; ACC = "#8A5A28"

def draw(variant, out):
    symbols  = variant in ("symbols", "regret", "all", "coins", "adversary")
    lit = {"story":     {"decisions", "choose", "adversary", "pay", "loop"},
           "symbols":   {"decisions", "choose", "adversary", "pay", "loop"},
           "adversary": {"adversary"},
           "regret":    {"yard"},
           "all":       {"decisions", "choose", "adversary", "pay", "loop", "yard"},
           "coins":     {"adversary", "decisions"}}[variant]
    def a(part): return 1.0 if part in lit else 0.22

    W, H = 13.0, 4.3
    fig = plt.figure(figsize=(W, H), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

    def card(x, y, w, h, fc, ec="none", r=0.12, z=2, alpha=1.0):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                    facecolor=fc, edgecolor=ec, lw=1.4, zorder=z, alpha=alpha))
    def arrow(x0, y0, x1, y1, color=GREY, rad=0.0, lw=1.6, z=3, alpha=1.0):
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=16, color=color,
                                     lw=lw, connectionstyle=f"arc3,rad={rad}", zorder=z, alpha=alpha))

    # ---- left: the n decisions
    lx, top = 0.45, 3.55; al = a("decisions")
    ax.text(lx + 0.85, top + 0.42, "n decisions", ha="center", va="center", fontsize=13, color=BLACK, fontweight="bold", alpha=al)
    names = ["decision 1", "decision 2", "decision 3", "⋮", "decision n"] if variant != "coins" else \
            ["decision 1", "decision 2", "decision 3", "⋮", "decision n"]
    for i, lab in enumerate(names):
        y = top - 0.15 - i * 0.62
        if lab == "⋮":
            ax.text(lx + 0.85, y - 0.24, "⋮", ha="center", va="center", fontsize=15, color=GREY, alpha=al); continue
        fc = LGREY
        if variant == "coins":
            fc = "#f3e2cf" if i == 0 else LGREY
        card(lx, y - 0.48, 1.7, 0.48, fc, r=0.08, alpha=al)
        txt = lab
        if variant == "coins":
            txt = "decision 1:  pays ½" if i == 0 else lab + ":  a fair coin"
        ax.text(lx + 0.85, y - 0.24, txt, ha="center", va="center", fontsize=10.5 if variant == "coins" else 11.5,
                color=BLACK, zorder=3, alpha=al)
    sub = "could be stocks, experts,\nroutes, constraints …" if variant != "coins" else "cost 1 or 0, each with\nprobability ½, every round"
    ax.text(lx + 0.85, 0.28, sub, ha="center", va="center", fontsize=10, color=GREY, style="italic", linespacing=1.3, alpha=al)

    # ---- middle: one round, three steps
    cx = [3.00, 5.70, 8.40]; cw, ch, cy = 2.35, 1.55, 1.95
    if symbols:
        bodies = ["a distribution  p⁽ᵗ⁾\nover the n decisions",
                  "sees p⁽ᵗ⁾, then sets\ncosts  m⁽ᵗ⁾ ∈ [−1, 1]ⁿ",
                  "the expected cost\nm⁽ᵗ⁾ · p⁽ᵗ⁾"]
    else:
        bodies = ["how much to bet\non each decision", "only now reveals\nwhat each one costs", "the average cost\nunder our bets"]
    if variant == "coins":
        bodies[1] = "flips a coin for each\ndecision 2 … n"
    steps = [("we choose", bodies[0], BLACK, "choose"), ("the adversary", bodies[1], PURPLE, "adversary"),
             ("we pay", bodies[2], ORANGE, "pay")]
    for k, (x, (head, body, col, key)) in enumerate(zip(cx, steps)):
        al = a(key)
        card(x, cy, cw, ch, "white", ec=col, r=0.14, alpha=al)
        ax.add_patch(plt.Circle((x + 0.34, cy + ch - 0.34), 0.2, color=col, zorder=3, alpha=al))
        ax.text(x + 0.34, cy + ch - 0.34, str(k + 1), ha="center", va="center", fontsize=11, color="white", fontweight="bold", zorder=4, alpha=al)
        ax.text(x + 0.68, cy + ch - 0.34, head, ha="left", va="center", fontsize=13, color=col, fontweight="bold", zorder=3, alpha=al)
        ax.text(x + cw / 2, cy + 0.52, body, ha="center", va="center", fontsize=11.5, color=BLACK, linespacing=1.35, zorder=3, alpha=al)
    for k in range(2):
        arrow(cx[k] + cw + 0.05, cy + ch / 2, cx[k + 1] - 0.05, cy + ch / 2, alpha=max(a(steps[k][3]), a(steps[k+1][3])))
    al = a("loop")
    ax.text(cx[0] + (cx[2] + cw - cx[0]) / 2, cy + ch + 0.42, "one round  t", ha="center", va="center", fontsize=13,
            color=BLACK, fontweight="bold", alpha=max(a("choose"), a("loop")))
    arrow(cx[2] + cw / 2, cy - 0.05, cx[0] + cw / 2, cy - 0.05, color=GREY, rad=-0.30, lw=1.4, alpha=al)
    ax.text(cx[1] + cw / 2, cy - 1.32, "next round  t + 1   —   T rounds in all", ha="center", va="center", fontsize=11.5, color=GREY, alpha=al)
    arrow(lx + 1.7 + 0.08, 2.60, cx[0] - 0.05, cy + ch / 2, color=GREY, lw=1.2, alpha=max(a("decisions"), a("choose")))

    # ---- right: the yardstick
    al = a("yard"); R = 12.85
    ax.text(R, 3.62, "after T rounds", ha="right", va="center", fontsize=13, color=BLACK, fontweight="bold", alpha=al)
    paid = "what we paid\nΣₜ m⁽ᵗ⁾ · p⁽ᵗ⁾" if symbols else "what we paid\nin total"
    best = "the best single decision,\nseen in hindsight" if not symbols else "the best single decision,\nin hindsight:  minᵢ Σₜ mᵢ⁽ᵗ⁾"
    ax.text(R, 3.02, paid, ha="right", va="center", fontsize=11.5, color=ORANGE, linespacing=1.35, alpha=al)
    ax.text(R, 2.36, "versus", ha="right", va="center", fontsize=11, color=GREY, style="italic", alpha=al)
    ax.text(R, 1.72, best, ha="right", va="center", fontsize=11.5, color=BLACK, linespacing=1.35, alpha=al)
    ax.text(R, 0.95, "the difference is\nour regret", ha="right", va="center", fontsize=12, color=ACC, fontweight="bold", linespacing=1.35, alpha=al)
    if variant == "regret":
        card(10.88, 0.45, 2.12, 3.55, "none", ec=ACC, r=0.16, z=1)

    fig.savefig(out, dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)

if __name__ == "__main__":
    for v in (sys.argv[1:] or ["story", "symbols", "adversary", "regret", "all", "coins"]):
        draw(v, str(Path(__file__).with_name(f"setting_{v}.png"))); print("wrote", v)

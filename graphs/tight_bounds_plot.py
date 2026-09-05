import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
plt.rcParams["font.family"] = ["Carlito", "Calibri", "DejaVu Sans"]   # Carlito = metric-compatible Calibri

# Upper bound (Thm 2.1) 2 sqrt(T ln n) and lower bound (Thm 4.1) (1/80) sqrt(T ln(n-1)),
# both against T on log-log axes: parallel lines, so the gap is a constant factor.

BLACK  = "#1a1a1a"
ORANGE = "#E08E45"
GREY   = "#777777"
n = 8
T = np.logspace(1, 5, 200)
up = 2 * np.sqrt(T * np.log(n))
lo = np.sqrt(T * np.log(n - 1)) / 80

fig = plt.figure(figsize=(10.0, 3.7), dpi=200)
ax = fig.add_axes([0.09, 0.19, 0.88, 0.76])
ax.fill_between(T, lo, up, color="#ececec", zorder=0)
ax.plot(T, up, color=BLACK, lw=2.4)
ax.plot(T, lo, "--", color=ORANGE, lw=2.2)
ax.set_xscale("log"); ax.set_yscale("log")
def along(x0, y, txt, color, above, f):
    # label rotated to follow a log-log line of slope 1/2
    p1 = ax.transData.transform((1e2, f(1e2)))
    p2 = ax.transData.transform((1e4, f(1e4)))
    ang = np.degrees(np.arctan2(p2[1] - p1[1], p2[0] - p1[0]))
    ax.text(x0, y, txt, color=color, fontsize=12.5, ha="center", va="bottom" if above else "top",
            rotation=ang, rotation_mode="anchor", transform_rotates_text=False, fontweight="bold")
fig.canvas.draw()
along(1.5e3, 2 * np.sqrt(1.5e3 * np.log(n)) * 1.25, "upper bound:  2√(T ln n)", BLACK, True,
      lambda T: 2 * np.sqrt(T * np.log(n)))
along(1.5e3, np.sqrt(1.5e3 * np.log(n - 1)) / 80 / 1.25, "lower bound:  (1/80)√(T ln(n−1))", ORANGE, False,
      lambda T: np.sqrt(T * np.log(n - 1)) / 80)
ax.text(1.0e3, np.sqrt(2 * np.sqrt(1e3 * np.log(n)) * np.sqrt(1e3 * np.log(n - 1)) / 80),
        "same slope  —  the gap is only a constant factor", color=GREY, fontsize=12.5, ha="center", va="center")
ax.set_xlabel("horizon  T  (log scale)", fontsize=12.5)
ax.set_ylabel("regret  (log scale)", fontsize=12.5)
ax.set_title("n = 8", fontsize=11, color=GREY, loc="left", pad=6)
ax.tick_params(labelsize=11)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.savefig(str(Path(__file__).with_suffix(".png")), dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.06)
print("ok")

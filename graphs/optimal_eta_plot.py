import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
plt.rcParams["font.family"] = ["Carlito", "Calibri", "DejaVu Sans"]   # Carlito = metric-compatible Calibri

# The regret bound  eta*T + ln(n)/eta  as a function of eta, for n = 8, T = 256.
# Two terms pull in opposite directions; the minimum is at eta* = sqrt(ln n / T).

BLACK  = "#1a1a1a"
ORANGE = "#E08E45"
PURPLE = "#6C4AB6"
ACC    = "#8A5A28"

n, T = 8, 256
eta = np.linspace(0.01, 0.5, 400)
a = eta * T
b = np.log(n) / eta
eta_s = np.sqrt(np.log(n) / T)
best = 2 * np.sqrt(T * np.log(n))

fig = plt.figure(figsize=(10.0, 3.7), dpi=200)
ax = fig.add_axes([0.09, 0.19, 0.88, 0.76])
ax.plot(eta, a, "--", color=PURPLE, lw=1.8)
ax.plot(eta, b, ":", color=ORANGE, lw=1.8)
ax.plot(eta, a + b, color=BLACK, lw=2.6)
ax.plot([eta_s], [best], "o", color=ORANGE, ms=9, zorder=5)

ax.text(0.42, 0.42 * T - 22, "ηT  —  overreacting", color=PURPLE, fontsize=12, ha="center", va="top")
ax.text(0.035, 175, "ln(n)/η  —  learning too slowly", color=ORANGE, fontsize=12, ha="left", va="center")
ax.text(0.33, 0.33 * T + np.log(n) / 0.33 + 22, "ηT + ln(n)/η", color=BLACK, fontsize=12.5, ha="center", va="bottom", fontweight="bold")
ax.annotate("η* = √(ln n / T) ≈ %.2f\nbound ≈ %.0f = 2√(T ln n)" % (eta_s, best),
            xy=(eta_s, best), xytext=(0.17, 110), fontsize=12, color=ACC, linespacing=1.35,
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2, shrinkB=6))

ax.set_xlim(0, 0.5); ax.set_ylim(0, 230)
ax.set_xlabel("learning rate  η", fontsize=12.5)
ax.set_ylabel("regret bound", fontsize=12.5)
ax.set_title("n = 8,  T = 256", fontsize=11, color="#777777", loc="left", pad=6)
ax.tick_params(labelsize=11)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.savefig(str(Path(__file__).with_suffix(".png")), dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.06)
print("eta*", eta_s, "bound", best)

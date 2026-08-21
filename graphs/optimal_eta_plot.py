import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Visualizes the eta-optimization on the "Optimal eta" corollary slide: bound(eta) =
# eta*T + ln(n)/eta over eta in (0, 1/2], with the minimizer eta* = sqrt(ln(n)/T) marked.
# Same n, T as the rest of the deck's simulations (n=8, T=250) so the whole deck stays
# one consistent running example.

n, T = 8, 250
eta = np.linspace(0.01, 0.5, 500)
bound = eta * T + np.log(n) / eta

eta_star = np.sqrt(np.log(n) / T)
bound_star = eta_star * T + np.log(n) / eta_star

black = "#1a1a1a"
orange = "#E08E45"

fig, ax = plt.subplots(figsize=(9.6, 4.6), dpi=300)

ax.plot(eta, bound, color=black, lw=2.4, label="bound(η) = ηT + ln(n)/η")
ax.axvline(eta_star, color=orange, lw=1.6, ls=":")
ax.plot([eta_star], [bound_star], marker="o", ms=7, color=orange, zorder=5)
ax.annotate(
    f"η* = √(ln n / T) ≈ {eta_star:.3f}\nmin bound ≈ {bound_star:.1f}",
    xy=(eta_star, bound_star), xytext=(eta_star + 0.05, bound_star + 25),
    fontsize=11.5, color="#8a5a28",
    arrowprops=dict(arrowstyle="->", color=orange, lw=1.3),
)

ax.set_xlabel("η", fontsize=13)
ax.set_ylabel("bound(η)", fontsize=13)
ax.set_title(f"n = {n},  T = {T}", fontsize=11, color="#777777")
fig.suptitle("Choosing η to Minimize the Bound", fontsize=15, color=black, fontweight="bold", y=0.99)
ax.legend(loc="upper center", fontsize=10.5, frameon=True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=10)
ax.set_xlim(0, 0.5)
ax.set_ylim(bottom=0)

fig.tight_layout(rect=[0, 0.115, 1, 0.94])
fig.text(0.5, 0.015,
    "The bound ηT + ln(n)/η trades off two terms moving in opposite directions as η changes;\n"
    "the minimum sits at η* = √(ln(n)/T), giving the familiar O(√(T ln n)) rate.",
    ha="center", va="bottom", fontsize=11, color="#555555")
fig.savefig("/home/claude/mw_deck/optimal_eta_plot.png", dpi=300, facecolor="white")
print(f"eta*={eta_star:.4f}  min bound={bound_star:.2f}")
print("saved optimal_eta_plot.png")

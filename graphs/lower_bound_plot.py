import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Visualizes the matching-lower-bound argument: draw each decision's cost i.i.d. and
# UNBIASED (mean 0) every round, so no algorithm can do better than 0 in expectation --
# yet the single best-in-hindsight decision still beats 0 by pure luck, and that luck
# gap grows like sqrt(T ln n). This IS the T ln n) lower bound: any algorithm's regret
# against this adversary is at least this gap, in expectation.

rng = np.random.default_rng(11)
n = 8
T_list = [25, 50, 100, 200, 400, 800, 1600, 3200, 6400]
K = 800  # trials per T, for a stable expectation

gaps = []
for T in T_list:
    costs = rng.uniform(-1, 1, (K, n, T))          # i.i.d., mean 0, no algorithm can beat 0 in expectation
    cum = costs.sum(axis=2)                          # (K, n) cumulative cost per expert
    best_hindsight = cum.min(axis=1)                 # best FIXED decision, per trial
    gap = -best_hindsight.mean()                     # how much luck alone beats "expected 0"
    gaps.append(gap)

gaps = np.array(gaps)
T_arr = np.array(T_list)

# Least-squares fit of gap ~= c * sqrt(T ln n) to show the matching growth RATE
ref = np.sqrt(T_arr * np.log(n))
c = (gaps @ ref) / (ref @ ref)

T_fine = np.logspace(np.log10(T_arr.min()), np.log10(T_arr.max()), 200)
fit = c * np.sqrt(T_fine * np.log(n))

black = "#1a1a1a"
orange = "#E08E45"

fig, ax = plt.subplots(figsize=(9.6, 4.6), dpi=300)

ax.plot(T_arr, gaps, color=black, lw=0, marker="o", ms=6, label="best-in-hindsight advantage (simulated, unbiased costs)")
ax.plot(T_fine, fit, color=orange, lw=2.2, ls=":", label=f"fit:  {c:.2f}·√(T ln n)   (matching Ω(√(T ln n)) rate)")

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("time horizon  T  (log scale)", fontsize=13)
ax.set_ylabel("E[ best fixed decision's edge ]  (log scale)", fontsize=13)
ax.set_title(f"n = {n} decisions, i.i.d. unbiased costs, {K} trials per T", fontsize=11, color="#777777")
fig.suptitle("Why √(T ln n) Can't Be Beaten", fontsize=15, color=black, fontweight="bold", y=0.99)
ax.legend(loc="upper left", fontsize=10, frameon=True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=10)

fig.tight_layout(rect=[0, 0.13, 1, 0.94])
fig.text(0.5, 0.015,
    "Even with every cost i.i.d. and unbiased — so no algorithm beats 0 in expectation — the best\n"
    "decision in hindsight still beats 0 by luck, and that edge grows at exactly the Ω(√(T ln n)) rate.",
    ha="center", va="bottom", fontsize=11, color="#555555")
fig.savefig("/home/claude/mw_deck/lower_bound_plot.png", dpi=300, facecolor="white")
for T, g in zip(T_list, gaps):
    print(f"T={T:>5}  gap={g:.3f}")
print("saved lower_bound_plot.png")

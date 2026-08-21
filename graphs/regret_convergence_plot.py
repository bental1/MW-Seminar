import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Proves the o(T) / average-regret-to-zero claim properly: sweep the horizon T, tune eta
# optimally FOR EACH T (Slide 14's eta = sqrt(ln n / T) -- fixed eta does NOT go to zero,
# that's exactly the "T known in advance" caveat from Slide 2), average over many
# independent trials per T (not one noisy run), and compare against the actual
# Theorem 2.1 bound curve 2*sqrt(ln(n)/T).

rng = np.random.default_rng(42)
n = 8
T_list = [25, 50, 100, 200, 400, 800, 1600, 3200, 6400]
K = 200  # independent trials per T

means, stds = [], []
for T in T_list:
    eta = np.sqrt(np.log(n) / T)
    biases = rng.uniform(-0.03, 0.03, (K, n, 1))
    noise = rng.normal(0, 1, (K, n, T)) * 0.9
    costs = np.clip(biases + noise, -1, 1)          # (K, n, T)

    w = np.ones((K, n))
    alg_cum = np.zeros(K)
    expert_cum = np.zeros((K, n))
    for t in range(T):
        p = w / w.sum(axis=1, keepdims=True)
        m = costs[:, :, t]
        alg_cum += (p * m).sum(axis=1)
        expert_cum += m
        w = w * (1 - eta * m)

    oracle_cum = expert_cum.min(axis=1)               # best FIXED decision, per trial
    avg_regret = (alg_cum - oracle_cum) / T
    means.append(avg_regret.mean())
    stds.append(avg_regret.std())

means = np.array(means)
stds = np.array(stds)
T_arr = np.array(T_list)

T_fine = np.logspace(np.log10(T_arr.min()), np.log10(T_arr.max()), 200)
bound = 2 * np.sqrt(np.log(n) / T_fine)

black = "#1a1a1a"
orange = "#E08E45"

fig, ax = plt.subplots(figsize=(9.6, 4.8), dpi=300)

ax.plot(T_fine, bound, color=orange, lw=2, ls=":", label="Theorem 2.1 bound:  2√(ln(n)/T)")
ax.plot(T_arr, means, color=black, lw=2.2, marker="o", ms=5,
        label=f"empirical average regret  (mean over {K} runs)")
ax.fill_between(T_arr, means - stds, means + stds, color=black, alpha=0.10,
                 label="± 1 std across runs")
ax.axhline(0, color="#cccccc", lw=1, zorder=0)

ax.set_xscale("log")
ax.set_xlabel("time horizon  T  (log scale)", fontsize=13)
ax.set_ylabel("average regret  (regret / T)", fontsize=13)
ax.set_title(f"n = {n} experts,  η = √(ln n / T) tuned per T,  {K} independent runs per point",
             fontsize=11, color="#777777")
fig.suptitle("Average Regret Shrinks to Zero", fontsize=15, color=black, fontweight="bold", y=0.99)
ax.legend(loc="upper right", fontsize=10.5, frameon=True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=10)
ax.set_ylim(bottom=-0.05)

fig.tight_layout(rect=[0, 0.115, 1, 0.93])
fig.text(0.5, 0.015,
    "Dividing total regret by T, the empirical average (black) tracks the theoretical bound\n"
    "(orange) down toward zero as the horizon T grows, confirming sublinear regret empirically.",
    ha="center", va="bottom", fontsize=11, color="#555555")
fig.savefig("/home/claude/mw_deck/regret_convergence_plot.png", dpi=300, facecolor="white")

for T, m, s in zip(T_list, means, stds):
    print(f"T={T:>5}  avg regret = {m:.4f}  (std {s:.4f})   bound = {2*np.sqrt(np.log(n)/T):.4f}")
print("saved regret_convergence_plot.png")

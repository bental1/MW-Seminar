import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Same simulation family as the Sandwich / oracle charts (n=8, T=250, eta=0.12, seed=7) --
# makes the whole deck describe one consistent run. Purpose: make "o(T)" concrete on the
# Problem Definition slide itself, before any proof -- plot the running regret (the "diff"
# between the algorithm and the best fixed decision) against a plain reference line for T
# (the round count itself), on the SAME axis/units, so the gap in growth rates is visible.
rng = np.random.default_rng(7)
n, T, eta = 8, 250, 0.12
biases = rng.uniform(-0.03, 0.03, n)
costs = biases[:, None] + rng.normal(0, 1, (n, T)) * 0.9
costs = np.clip(costs, -1, 1)

w = np.ones(n)
alg_cum = [0.0]
expert_cum = np.zeros(n)
expert_cum_history = [expert_cum.copy()]

for t in range(T):
    p = w / w.sum()
    m = costs[:, t]
    alg_cum.append(alg_cum[-1] + (p * m).sum())
    expert_cum = expert_cum + m
    expert_cum_history.append(expert_cum.copy())
    w = w * (1 - eta * m)

expert_cum_history = np.array(expert_cum_history)
alg_cum = np.array(alg_cum)
best_i = expert_cum_history[-1].argmin()
oracle_cum = expert_cum_history[:, best_i]

rounds = np.arange(T + 1)
diff = alg_cum - oracle_cum          # the round-by-round "diff": regret so far

# The actual Theorem 2.1 bound for THIS run's eta, evaluated as a running horizon of length t:
# eta*t + ln(n)/eta. This IS the actual regret limit the algorithm is proven to respect --
# concrete, not just "eventually sublinear" -- so it's the headline comparison, not a generic
# reference line for t.
bound = eta * rounds + np.log(n) / eta

black = "#1a1a1a"
orange = "#E08E45"

fig, ax = plt.subplots(figsize=(9.6, 4.6), dpi=300)

ax.plot(rounds, bound, color=orange, lw=2.2, ls=":", label="regret limit:  η·t + ln(n)/η")
ax.plot(rounds, diff, color=black, lw=2.4, label="regret so far")
ax.fill_between(rounds, diff, bound, color=orange, alpha=0.07)

ax.annotate(f"{bound[-1]:.1f}", xy=(T, bound[-1]), xytext=(6, 0),
            textcoords="offset points", fontsize=12, color=orange, va="center")
ax.annotate(f"{diff[-1]:.1f}", xy=(T, diff[-1]), xytext=(6, 4),
            textcoords="offset points", fontsize=12, color=black, va="bottom")

ax.set_xlabel("round  t", fontsize=13)
ax.set_ylabel("cost units", fontsize=13)
ax.set_title("n = 8,  T = 250,  η = 0.12", fontsize=11, color="#777777")
fig.suptitle("Regret So Far vs. the Proven Limit", fontsize=15, color=black, fontweight="bold", y=0.99)
ax.legend(loc="upper left", fontsize=10.5, frameon=True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=10)
ax.set_xlim(0, T)
ax.set_ylim(bottom=-5)

fig.tight_layout(rect=[0, 0.115, 1, 0.94])
fig.text(0.5, 0.015,
    "The algorithm's actual regret (black) stays far below the worst-case limit ηT + ln(n)/η that\n"
    "Theorem 2.1 guarantees (orange) — the bound holds, with room to spare.",
    ha="center", va="bottom", fontsize=11, color="#555555")
fig.savefig("/home/claude/mw_deck/problem_oT_plot.png", dpi=300, facecolor="white")

print(f"final round T={T}: regret(diff)={diff[-1]:.2f}, actual regret limit={bound[-1]:.2f}")
print("saved problem_oT_plot.png")

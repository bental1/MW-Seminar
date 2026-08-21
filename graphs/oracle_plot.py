import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Same simulation family as the Sandwich chart (sandwich_plot.py): n=8, T=250, eta=0.12,
# per-expert bias + noise, clipped to [-1,1] -- so the two charts describe one consistent story.
rng = np.random.default_rng(7)
n, T, eta = 8, 250, 0.12
biases = rng.uniform(-0.03, 0.03, n)
costs = biases[:, None] + rng.normal(0, 1, (n, T)) * 0.9
costs = np.clip(costs, -1, 1)

w = np.ones(n)
alg_cum = [0.0]          # algorithm's cumulative cost, round by round
expert_cum = np.zeros(n)  # each fixed decision's own cumulative cost, round by round
expert_cum_history = [expert_cum.copy()]

for t in range(T):
    p = w / w.sum()
    m = costs[:, t]
    alg_cum.append(alg_cum[-1] + (p * m).sum())
    expert_cum = expert_cum + m
    expert_cum_history.append(expert_cum.copy())
    w = w * (1 - eta * m)

expert_cum_history = np.array(expert_cum_history)     # (T+1, n)
alg_cum = np.array(alg_cum)                            # (T+1,)

# The oracle: the ONE fixed decision that is best at t=T, tracked from round 0 --
# not "whichever expert happens to be lowest at each round" (that's a different, invalid quantity).
best_i = expert_cum_history[-1].argmin()
oracle_cum = expert_cum_history[:, best_i]

rounds = np.arange(T + 1)
regret = alg_cum - oracle_cum

black = "#1a1a1a"
purple = "#6C4AB6"

fig, ax = plt.subplots(figsize=(9.6, 4.8), dpi=300)

ax.plot(rounds, alg_cum, color=black, lw=2.2, label="algorithm's cumulative cost")
ax.plot(rounds, oracle_cum, color=purple, lw=2, ls="--",
         label="oracle: best fixed decision's cumulative cost")
ax.fill_between(rounds, alg_cum, oracle_cum, color=black, alpha=0.06)

# direct end-of-line labels instead of relying on the legend alone
ax.annotate("algorithm", xy=(T, alg_cum[-1]), xytext=(6, 4), textcoords="offset points",
            fontsize=11, color=black, va="bottom")
ax.annotate("oracle (best fixed decision)", xy=(T, oracle_cum[-1]), xytext=(6, -4),
            textcoords="offset points", fontsize=11, color=purple, va="top")

# mark the gap = regret at one round, with a small double-headed arrow only (no text attached,
# so it can't collide with either curve) -- the numbers go in a fixed, empty corner instead
mid_t = int(T * 0.55)
y_alg_mid = alg_cum[mid_t]
y_oracle_mid = oracle_cum[mid_t]
ax.annotate(
    "",
    xy=(mid_t, y_alg_mid), xytext=(mid_t, y_oracle_mid),
    arrowprops=dict(arrowstyle="<->", color="#888888", lw=1.2),
)

# empty lower-left region for both curves at this seed -- safe for a text block
ax.text(8, -23,
        f"gap between the curves = regret\n"
        f"regret at t={mid_t}: {alg_cum[mid_t]-oracle_cum[mid_t]:.2f}\n"
        f"final regret at t={T}: {regret[-1]:.2f}   (Theorem 2.1 bound: {2*np.sqrt(T*np.log(n)):.2f})",
        fontsize=10.5, color="#555555", va="top", ha="left")

ax.set_xlabel("round  t", fontsize=13)
ax.set_ylabel("cumulative cost", fontsize=13)
ax.set_title("n = 8 experts,  T = 250 rounds,  η = 0.12", fontsize=11, color="#777777")
fig.suptitle("Algorithm vs. the Best Fixed Decision", fontsize=15, color=black, fontweight="bold", y=0.99)
ax.legend(loc="upper right", fontsize=11, frameon=True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=10)
ax.axhline(0, color="#dddddd", lw=1, zorder=0)

fig.tight_layout(rect=[0, 0.12, 1, 0.94])
fig.text(0.5, 0.015,
    "The algorithm's cumulative cost tracks the single best-in-hindsight decision closely; the\n"
    "gap between the two curves at any round is exactly that round's regret.",
    ha="center", va="bottom", fontsize=11, color="#555555")
fig.savefig("/home/claude/mw_deck/oracle_plot.png", dpi=300, facecolor="white")
print(f"best fixed decision (oracle) index: {best_i}")
print(f"algorithm final cumulative cost: {alg_cum[-1]:.2f}")
print(f"oracle final cumulative cost:    {oracle_cum[-1]:.2f}")
print(f"final regret:                    {regret[-1]:.2f}")
print(f"Theorem 2.1 bound (2*sqrt(T ln n)): {2*np.sqrt(T*np.log(n)):.2f}")
print("saved oracle_plot.png")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Matching Pennies (zero-sum): both players run MW against each other, each round's
# cost computed against the OPPONENT'S CURRENT distribution (so the dynamics are smooth).
# Nash equilibrium is (0.5, 0.5) for both. Instantaneous play can drift/cycle, but the
# TIME-AVERAGE of each player's strategy converges to the equilibrium -- exactly the
# claim on the Nash Equilibria slide.

T = 400
eta = 0.35
p1_H = 0.92   # player 1 starts heavily biased toward Heads
p2_H = 0.50

p1_hist, p2_hist = [], []
w1 = np.array([p1_H, 1 - p1_H])
w2 = np.array([p2_H, 1 - p2_H])

avg1_H_running = []
avg2_H_running = []
cum1, cum2 = np.zeros(2), np.zeros(2)

for t in range(T):
    p1 = w1 / w1.sum()
    p2 = w2 / w2.sum()
    p1_hist.append(p1[0])
    p2_hist.append(p2[0])
    cum1 += p1
    cum2 += p2
    avg1_H_running.append((cum1[0]) / (t + 1))
    avg2_H_running.append((cum2[0]) / (t + 1))

    # cost to player 1's actions {H, T}, given player 2's current mixed strategy:
    # player 1 wins (cost -1) on a match, loses (cost +1) on a mismatch.
    cost1 = np.array([1 - 2 * p2[0], 2 * p2[0] - 1])  # cost(H), cost(T)
    # player 2 wins (cost -1) on a MISMATCH, loses (cost +1) on a match.
    cost2 = np.array([2 * p1[0] - 1, 1 - 2 * p1[0]])

    w1 = w1 * (1 - eta * cost1)
    w2 = w2 * (1 - eta * cost2)

black = "#1a1a1a"
orange = "#E08E45"
gray = "#999999"

fig, ax = plt.subplots(figsize=(9.6, 4.6), dpi=300)

rounds = np.arange(1, T + 1)
ax.plot(rounds, p1_hist, color=gray, lw=1, alpha=0.5, label="P1's instantaneous P(Heads)")
ax.plot(rounds, avg1_H_running, color=black, lw=2.4, label="P1's average P(Heads) over time")
ax.plot(rounds, avg2_H_running, color=orange, lw=2.4, ls="--", label="P2's average P(Heads) over time")
ax.axhline(0.5, color="#cccccc", lw=1.4, ls=":", label="Nash equilibrium: (0.5, 0.5)")

ax.set_xlabel("round  t", fontsize=13)
ax.set_ylabel("P(Heads)", fontsize=13)
ax.set_title("Matching Pennies — MW self-play, η = 0.35", fontsize=11, color="#777777")
fig.suptitle("MW Self-Play Converges to Nash Equilibrium", fontsize=15, color=black, fontweight="bold", y=0.99)
ax.legend(loc="upper right", fontsize=10, frameon=True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=10)
ax.set_ylim(-0.02, 1.02)

fig.tight_layout(rect=[0, 0.115, 1, 0.93])
fig.text(0.5, 0.015,
    "Both players run Multiplicative Weights against each other; instantaneous play cycles, but\n"
    "each player's running-average strategy settles onto the unique Nash equilibrium, 50/50.",
    ha="center", va="bottom", fontsize=11, color="#555555")
fig.savefig("/home/claude/mw_deck/nash_matching_pennies_plot.png", dpi=300, facecolor="white")
print(f"final avg P1(H)={avg1_H_running[-1]:.3f}  avg P2(H)={avg2_H_running[-1]:.3f}")
print("saved nash_matching_pennies_plot.png")

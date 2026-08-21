import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from itertools import permutations

# Vanilla CFR on Kuhn Poker (the standard 3-card toy game used to introduce CFR).
# Verifies the regret-minimization-in-games claim on this talk's own terms: track the
# expected value to Player 1 under CFR's AVERAGE strategy and show it converge to the
# known Nash equilibrium value of Kuhn Poker, -1/18 (Kuhn, 1950). Same "regret -> good
# outcome" story as the MW charts earlier in the deck, now for CFR specifically.

CARDS = [0, 1, 2]
ACTIONS = ['p', 'b']


class InfoSet:
    def __init__(self):
        self.regret_sum = np.zeros(2)
        self.strategy_sum = np.zeros(2)


infosets = {}


def get_infoset(key):
    if key not in infosets:
        infosets[key] = InfoSet()
    return infosets[key]


def is_terminal(h):
    return h in ("pp", "bp", "bb", "pbp", "pbb")


def kuhn_payoff(h, cards):
    p0, p1 = cards[0], cards[1]
    if h == "pp":
        return 1 if p0 > p1 else -1
    if h in ("bb", "pbb"):
        return 2 if p0 > p1 else -2
    if h == "bp":
        return 1
    if h == "pbp":
        return -1
    raise ValueError(h)


def get_strategy(infoset, reach):
    pos = np.maximum(infoset.regret_sum, 0)
    total = pos.sum()
    strat = pos / total if total > 0 else np.array([0.5, 0.5])
    infoset.strategy_sum += reach * strat
    return strat


def cfr(cards, history, p0, p1):
    plays = len(history)
    player = plays % 2
    if is_terminal(history):
        u0 = kuhn_payoff(history, cards)
        return u0 if player == 0 else -u0
    key = f"{cards[player]}{history}"
    infoset = get_infoset(key)
    strategy = get_strategy(infoset, p0 if player == 0 else p1)
    util = np.zeros(2)
    node_util = 0.0
    for a, ch in enumerate(ACTIONS):
        nh = history + ch
        if player == 0:
            util[a] = -cfr(cards, nh, p0 * strategy[a], p1)
        else:
            util[a] = -cfr(cards, nh, p0, p1 * strategy[a])
        node_util += strategy[a] * util[a]
    for a in range(2):
        regret = util[a] - node_util
        cf_reach = p1 if player == 0 else p0
        infoset.regret_sum[a] += cf_reach * regret
    return node_util


def walk_value(history, cards, avg_strategy):
    plays = len(history)
    player = plays % 2
    if is_terminal(history):
        return kuhn_payoff(history, cards)
    key = f"{cards[player]}{history}"
    strat = avg_strategy.get(key, np.array([0.5, 0.5]))
    val = 0.0
    for a, ch in enumerate(ACTIONS):
        val += strat[a] * walk_value(history + ch, cards, avg_strategy)
    return val


deals_all = list(permutations(CARDS, 2))


def game_value(avg_strategy):
    total = sum(walk_value("", cards, avg_strategy) for cards in deals_all)
    return total / len(deals_all)


N = 20000
checkpoints = sorted(set(np.unique(np.logspace(0, np.log10(N), 60).astype(int))))
iters, vals = [], []
for it in range(1, N + 1):
    for cards in deals_all:
        cfr(list(cards), "", 1, 1)
    if it in checkpoints:
        avg_strategy = {}
        for key, iset in infosets.items():
            s = iset.strategy_sum
            total = s.sum()
            avg_strategy[key] = s / total if total > 0 else np.array([0.5, 0.5])
        iters.append(it)
        vals.append(game_value(avg_strategy))

iters = np.array(iters)
vals = np.array(vals)
target = -1 / 18

black = "#1a1a1a"
orange = "#E08E45"

fig, ax = plt.subplots(figsize=(9.6, 4.6), dpi=300)

ax.plot(iters, vals, color=black, lw=2.2, label="value to P1 under CFR's average strategy")
ax.axhline(target, color=orange, lw=2.2, ls=":", label=f"Nash equilibrium value:  -1/18 ≈ {target:.4f}")

ax.set_xscale("log")
ax.set_xlabel("CFR iteration  (log scale)", fontsize=13)
ax.set_ylabel("expected value to Player 1", fontsize=13)
ax.set_title("Kuhn Poker — 12 information sets, vanilla CFR self-play", fontsize=11, color="#777777")
fig.suptitle("CFR Converges to the Known Nash Value", fontsize=15, color=black, fontweight="bold", y=0.99)
ax.legend(loc="lower right", fontsize=10.5, frameon=True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=10)

fig.tight_layout(rect=[0, 0.115, 1, 0.93])
fig.text(0.5, 0.015,
    "Vanilla CFR self-play on Kuhn Poker's 12 information sets; the value to Player 1 under CFR's\n"
    "average strategy converges to the game's known equilibrium value, −1/18 (Kuhn, 1950).",
    ha="center", va="bottom", fontsize=11, color="#555555")
fig.savefig("/home/claude/mw_deck/cfr_kuhn_plot.png", dpi=300, facecolor="white")

print(f"final value at iter {iters[-1]}: {vals[-1]:.5f}  (target {target:.5f})")
print("saved cfr_kuhn_plot.png")

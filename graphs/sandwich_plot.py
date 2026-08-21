import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(7)

n, T, eta = 8, 250, 0.12
biases = rng.uniform(-0.03, 0.03, n)
costs = biases[:, None] + rng.normal(0, 1, (n, T)) * 0.9
costs = np.clip(costs, -1, 1)

w = np.ones(n)
Phi = [n]
best_w = [1.0]
upper = [n]
cum_alg = 0.0
for t in range(T):
    p = w / w.sum()
    m = costs[:, t]
    alg_cost = (p * m).sum()
    cum_alg += alg_cost
    w = w * (1 - eta * m)
    Phi.append(w.sum())
    best_w.append(w.max())
    upper.append(n * np.exp(-eta * cum_alg))

rounds = np.arange(T + 1)

fig, ax = plt.subplots(figsize=(9.6, 4.6), dpi=300)
purple = "#6C4AB6"
orange = "#E08E45"
black = "#1a1a1a"

ax.plot(rounds, Phi, color=black, lw=2.2, label=r"$\Phi^{(t)}$   (actual potential)")
ax.plot(rounds, best_w, color=purple, lw=2, ls="--", label=r"best expert's weight  $w_i^{(t)}$   (lower bound)")
ax.plot(rounds, upper, color=orange, lw=2, ls=":", label=r"upper bound:  $n\cdot\exp(-\eta\sum m^{(s)}\!\cdot p^{(s)})$")
ax.fill_between(rounds, best_w, upper, color=black, alpha=0.06)

ax.set_xlabel("round  t", fontsize=13)
ax.set_ylabel(r"$\Phi^{(t)}$", fontsize=14)
ax.set_title("Simulation:  n = 8 experts,  T = 250 rounds,  η = 0.12", fontsize=13, color="#555555")
ax.legend(loc="upper left", fontsize=11, frameon=True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=10)

fig.tight_layout()
fig.savefig("assets/sandwich_plot.png", dpi=300, transparent=True)
print("saved sandwich_plot.png")

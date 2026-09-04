import numpy as np

# The Multiplicative Weights algorithm, exactly as on slide 16 of the seminar:
#   start with w_i = 1, each round play p = w / sum(w), observe costs m in [-1, 1],
#   update w_i <- w_i (1 - eta * m_i).

def multiplicative_weights(costs, eta):          # costs: T x n array, m^(t)_i in [-1, 1]
    T, n = costs.shape
    w = np.ones(n)
    alg_cost = 0.0
    for t in range(T):
        p = w / w.sum()                          # p^(t)_i = w_i^(t) / Phi^(t)
        alg_cost += costs[t] @ p                 # pay m^(t) . p^(t)
        w *= (1 - eta * costs[t])                # w_i^(t+1) = w_i^(t) (1 - eta m_i^(t))
    return alg_cost

if __name__ == "__main__":
    rng = np.random.default_rng(0)
    n, T = 5, 200
    eta = np.sqrt(np.log(n) / T)                 # the optimal eta from slide 30
    costs = rng.uniform(-1, 1, size=(T, n))
    alg_cost = multiplicative_weights(costs, eta)
    best_fixed = costs.sum(axis=0).min()         # best single decision in hindsight
    bound = 2 * np.sqrt(T * np.log(n))           # Theorem 2.1 with eta = eta*
    print(f"algorithm paid      {alg_cost:8.2f}")
    print(f"best fixed decision {best_fixed:8.2f}")
    print(f"regret              {alg_cost - best_fixed:8.2f}   (bound 2*sqrt(T ln n) = {bound:.2f})")

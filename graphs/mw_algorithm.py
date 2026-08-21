import numpy as np

def multiplicative_weights(costs, eta):          # costs: T x n array, m^(t)_i in [-1,1]
    T, n = costs.shape
    w = np.ones(n)
    alg_cost = 0.0
    for t in range(T):
        p = w / w.sum()                          # p^(t)_i = w_i^(t) / Phi^(t)
        alg_cost += costs[t] @ p                  # incur m^(t) . p^(t)
        w *= (1 - eta * costs[t])                 # w_i^(t+1) = w_i^(t)(1 - eta*m_i^(t))
    return alg_cost

if __name__ == "__main__":
    np.random.seed(0)
    n, T = 5, 200
    eta = np.sqrt(np.log(n) / T)                  # optimal eta from Slide 14
    costs = np.random.uniform(-1, 1, size=(T, n))
    alg_cost = multiplicative_weights(costs, eta)
    best_fixed = costs.sum(axis=0).min()
    bound = 2 * np.sqrt(T * np.log(n))
    print(f"n={n}, T={T}, eta={eta:.4f}")
    print(f"algorithm total cost:   {alg_cost:.2f}")
    print(f"best fixed decision:    {best_fixed:.2f}")
    print(f"excess (regret):        {alg_cost - best_fixed:.2f}")
    print(f"Theorem 2.1 bound O(.): {bound:.2f}")

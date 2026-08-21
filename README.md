# MW-Seminar

Code for Seminar 20954, "The Multiplicative Weights Update Method: A
Meta-Algorithm and Applications" (Tal Idelson, supervised by Prof. Zeev
Nutov), based on Arora, Hazan & Kale (2012), *Theory of Computing*, Vol. 8.

## graphs/

Python simulations of the Multiplicative Weights algorithm (and, for the
poker section, Counterfactual Regret Minimization). Each script generates
its own figure with a heading and a short explanation baked into the image,
so the output is readable on its own.

- `mw_algorithm.py` — the ~10-line MW implementation plus a small demo run.
- `oracle_plot.py` — algorithm vs. oracle (best fixed decision) cumulative
  cost over one run; the gap between the curves at any round is that
  round's regret.
- `problem_oT_plot.py` — regret so far vs. the actual Theorem 2.1 regret
  limit (η·t + ln(n)/η) for one run.
- `optimal_eta_plot.py` — the bound ηT + ln(n)/η plotted directly against
  η, with the minimizer η* = √(ln(n)/T) marked.
- `lower_bound_plot.py` — simulates the matching lower-bound argument:
  i.i.d. unbiased costs still let the best-in-hindsight decision beat 0 by
  luck, at a rate matching Ω(√(T ln n)).
- `regret_convergence_plot.py` — average regret vs. T, swept across
  horizons with η re-tuned per T and averaged over many independent
  trials, compared against the theoretical bound curve.
- `nash_matching_pennies_plot.py` — two MW instances self-playing Matching
  Pennies; instantaneous play cycles, but each player's running-average
  strategy converges to the Nash equilibrium (0.5, 0.5).
- `cfr_kuhn_plot.py` — a from-scratch vanilla CFR implementation on Kuhn
  Poker (12 information sets); verifies convergence to the game's known
  Nash value, −1/18 (Kuhn, 1950).
- `sandwich_plot.py` — an early draft of the "sandwich" simulation (Φ
  bounded between the best expert's weight and the exponential upper
  bound). Kept for reference; it does not reproduce the exact chart in the
  seminar report.

Run any script with:

```
pip install -r requirements.txt
python3 graphs/<script>.py
```

Each script saves its own PNG next to it (not committed here — regenerate
by running the script).

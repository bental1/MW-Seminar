# MW-Seminar

Code and generated figures for Seminar 20954, "The Multiplicative Weights Update
Method: A Meta-Algorithm and Applications" (Tal Idelson, supervised by Prof. Zeev
Nutov), based on Arora, Hazan & Kale (2012), *Theory of Computing*, Vol. 8.

## graphs/

Python simulations of the Multiplicative Weights algorithm (and, for the poker
section, Counterfactual Regret Minimization) and the figures built from them
(matplotlib, numpy). Every figure below has its own heading and a one- or
two-line explanation baked into the image itself, so each one is readable on
its own, without the slides.

- `mw_algorithm.py` — the ~10-line MW implementation plus a small demo run.
- `oracle_plot.py` / `oracle_plot.png` — algorithm vs. oracle (best fixed
  decision) cumulative cost over one run; the gap between the curves at any
  round is that round's regret.
- `problem_oT_plot.py` / `problem_oT_plot.png` — regret so far vs. the actual
  Theorem 2.1 regret limit (η·t + ln(n)/η) for one run.
- `optimal_eta_plot.py` / `optimal_eta_plot.png` — the bound ηT + ln(n)/η
  plotted directly against η, with the minimizer η* = √(ln(n)/T) marked.
- `lower_bound_plot.py` / `lower_bound_plot.png` — simulates the matching
  lower-bound argument: i.i.d. unbiased costs still let the best-in-hindsight
  decision beat 0 by luck, at a rate matching Ω(√(T ln n)).
- `regret_convergence_plot.py` / `regret_convergence_plot.png` — average regret
  vs. T, swept across horizons with η re-tuned per T and averaged over many
  independent trials, compared against the theoretical bound curve.
- `nash_matching_pennies_plot.py` / `nash_matching_pennies_plot.png` — two MW
  instances self-playing Matching Pennies; instantaneous play cycles, but each
  player's running-average strategy converges to the Nash equilibrium (0.5, 0.5).
- `cfr_kuhn_plot.py` / `cfr_kuhn_plot.png` — a from-scratch vanilla CFR
  implementation on Kuhn Poker (12 information sets); verifies convergence to
  the game's known Nash value, −1/18 (Kuhn, 1950), as a concrete, exactly
  checkable instance of the same regret-minimization claim, on a poker game
  small enough to solve without any sampling.
- `sandwich_plot.py` — an early draft of the "sandwich" simulation (Φ bounded
  between the best expert's weight and the exponential upper bound). Kept for
  reference; it does not reproduce the exact chart in the seminar report (that
  one composites a matplotlib chart with a separately rendered LaTeX equation
  and isn't fully scripted here yet).

Run any script with:

```
pip install -r requirements.txt
python3 graphs/<script>.py
```

## slides/

`build_deck.js` generates the seminar slide deck (a plain white/no-design
skeleton: headings, body text, equations, figures, speaker notes) as a `.pptx`
using [pptxgenjs](https://www.npmjs.com/package/pptxgenjs). It expects the
referenced images (algorithm box, sandwich chart, WM/PST screenshots, Libratus
figures, and the generated plots above) to be available at the paths set near
the top of the script — update those paths for your own environment before
running.

```
npm install pptxgenjs
node slides/build_deck.js
```

const pptxgen = require("pptxgenjs");
const path = require("path");

const A = (p) => path.join("/tmp", p);
const ASSETS = {
  algoBox: "claude-chrome-screenshots-SMq26O/screenshot-1785595425700-0.png",
  sandwich: "sandwich_final.png",
  wm: "claude-chrome-screenshots-hRyzuH/WM_screenshot_highlighted.png",
  pst: "claude-chrome-screenshots-yxv6ET/screenshot-1786815956075-3.png",
  fig1: "fig1_top_panel.png",
  fig2: "claude-chrome-screenshots-yxv6ET/screenshot-1786814497251-2.png",
  fig3: "claude-chrome-screenshots-yxv6ET/screenshot-1786814472024-0.png",
  oT: "problem_oT_plot.png",
  etaOpt: "optimal_eta_plot.png",
  lowerBound: "lower_bound_plot.png",
  regretConv: "regret_convergence_plot.png",
  nash: "nash_matching_pennies_plot.png",
  cfrKuhn: "cfr_kuhn_plot.png",
};
const ASPECT = {
  algoBox: 1150 / 408,
  sandwich: 1242 / 660,
  wm: 1166 / 362,
  pst: 1200 / 236,
  fig1: 924 / 195,
  fig2: 924 / 430,
  fig3: 1404 / 446,
  oT: 2880 / 1380,
  etaOpt: 2880 / 1380,
  lowerBound: 2880 / 1380,
  regretConv: 2880 / 1440,
  nash: 2880 / 1380,
  cfrKuhn: 2880 / 1380,
};

// v10: full revision per advisor comments. 30 slides. Order:
// Title, Program, Intuition, Problem, Notation(NEW), Algorithm, Example, Theorem,
// Theorem->Problem(NEW), ProofStrategy(redesigned), Potential Phi, Update, Telescoping,
// BoundingEachExpert, Sandwich, TakingLogs, CompletingProof, OptimalEta(+chart),
// MatchingLowerBound(+chart), RegretVanishes(+chart), BeyondMW, IndependentDiscovery(reframed,
// TwoInstantiations CUT), NashEquilibria(+chart), CFR:GameTrees, MonteCarloCFR(NEW,+chart),
// CFRvsMW(table), Libratus:Architecture, Libratus:Compute(NEW), Libratus:Results, Summary(NEW).
const NOTES = {
  1: "I'm going to talk about the Multiplicative Weights Update method — one algorithmic idea that turns out to solve problems in machine learning, optimization, game theory, and even poker. This is based on Arora, Hazan and Kale's 2012 survey, and on my own seminar report, supervised by Professor Nutov.",
  2: "Here's the shape of the talk: state the problem precisely, give the algorithm, prove its guarantee, draw out some corollaries, then show two real papers that turn out to be the same theorem in disguise, and finish with a poker application.",
  3: "Before any notation: every round you're choosing among n options, and only afterward does an adversary reveal how every option would have done. You have to commit before you know. The question this whole talk answers is whether you can adapt fast enough to end up almost as good as whichever option would have been best all along — without ever knowing in advance which one that is.",
  4: "Formally: n decisions, T rounds. Each round we pick a distribution over decisions, an adversary reveals a cost for every decision, and we pay the expected cost. The question is whether we can guarantee our total cost stays close to the best single decision in hindsight — and 'close' has to mean sublinear in T, because a gap that grows linearly with T is really just a constant penalty every round, forever. This chart makes that concrete: the algorithm's regret stays far below the actual proven limit, not just some vague eventual bound.",
  5: "Before the algorithm itself, here's every symbol I'll use from here on, in one place: n decisions, T rounds, the weight w, the distribution p, the potential Phi, the learning rate eta, and the update rule that ties them together. Everything for the rest of the talk is built from exactly these six pieces — so if a symbol comes back later, this is the slide it was defined on.",
  6: "With the notation in hand, here's the algorithm. Every decision starts at equal weight. Each round we pick a decision proportional to its current weight, and after costs are revealed, we shrink each decision's weight by (1 − eta times its cost). Decisions that just did badly shrink; decisions that did well barely move. Nothing is ever thrown away completely, but persistent losers fade out.",
  7: "Before proving anything: here's the whole algorithm in about ten lines, and a real run — five decisions, two hundred rounds of random costs. The algorithm's regret came out to 12.83, and Theorem 2.1 guarantees it can't exceed about 35.88 for this instance. It holds, with room to spare, as you'd expect from a worst-case bound running against a friendlier random adversary.",
  8: "This is the formal guarantee — Theorem 2.1. For any single fixed decision i, the algorithm's total cost is bounded by that decision's total cost, plus two extra terms: one that grows with eta, one that shrinks with eta. Everything from here on is building toward exactly this inequality.",
  9: "One thing worth making explicit: this theorem isn't a different claim from the Problem Definition a few slides back — it's the same one. The theorem holds for every fixed i separately; plug in i equal to the best decision in hindsight, use the fact that each cost is at most 1 in size so the middle term is at most eta times T, and it collapses into exactly the inequality on the Problem Definition slide. Nothing new is being claimed here, just proved.",
  10: "The whole proof is one sandwich, and it's worth seeing the shape before the details. On one side: any single expert's own weight can never exceed the total weight Phi — that's just non-negativity, bound 1. On the other: Phi itself can't shrink slower than the algorithm's own performance dictates — bound 2, which takes the next few slides to derive. Put those two together and you're comparing the algorithm directly to any fixed expert, through Phi in the middle. That's the entire strategy — and it's exactly the shape the Sandwich Bound chart in a few slides will show you numerically.",
  11: "Recall Phi from the notation slide: the sum of all the weights. It mirrors the algorithm exactly, since p_i = w_i / Phi — and non-negativity is exactly what gives us bound 1 from the Proof Strategy slide, since no single weight can exceed the sum of all of them.",
  12: "If you expand the definition of Phi and substitute the update rule, Phi next round equals Phi this round times (1 − eta times the algorithm's own expected cost). So Phi's shrinkage rate each round tracks how well the algorithm itself is doing.",
  13: "That relationship has a product of T terms, which is awkward. The standard trick — 1 minus x is at most e to the minus x — turns the product into a single exponential once you telescope across all T rounds, giving bound 2 from the Proof Strategy slide: a clean upper bound on Phi in terms of the algorithm's own cost.",
  14: "And here's bound 1, derived properly: any one decision's own weight can never exceed Phi — non-negativity again — and if you unroll that decision's update on its own, you get a product depending only on that decision's own costs. This holds for every decision simultaneously, without needing to know in advance which one is best.",
  15: "Put bound 1 and bound 2 together and Phi is sandwiched: any expert's own product on one side, the algorithm's exponential bound on the other — exactly as previewed. This chart is my own simulation — eight experts, two hundred fifty rounds — showing that sandwich holds round by round. The two labeled gaps are the slack from the two approximations we're about to use.",
  16: "Products are hard to compare directly. Taking logs turns the sandwich's products into sums and cancels the exponential on the upper side, so now it's one additive inequality.",
  17: "Two more standard inequalities, both valid whenever eta is at most one half, clean up the logs on each side. Substitute them in, simplify, and Theorem 2.1 falls out. That's the proof.",
  18: "Eta was a free parameter this whole time. This chart plots the bound as a function of eta directly — it's a simple U-shape, and minimizing it analytically gives eta-star equal to root of ln(n)/T, marked here. Plugging that back in gives the familiar order root T log n bound.",
  19: "Is that the best possible? This chart simulates the argument: draw every decision's cost i.i.d. and unbiased, so no algorithm can beat zero in expectation — but the single best decision in hindsight still beats zero by pure luck, and that luck gap grows at exactly the root(T log n) rate, confirmed by the fit. So Theorem 2.1 isn't loose; no algorithm can do meaningfully better against this adversary.",
  20: "Divide the whole bound by T and you get average regret per round. This chart shows it empirically shrinking to zero as T grows, tracking the theoretical curve — and n only ever shows up as its logarithm, so a million decisions barely moves the bound.",
  21: "Nothing in this proof assumed anything about how the adversary picks costs. And the proof skeleton — define a potential function, bound it two ways, compare via logs — is reusable; swap in relative entropy and you get Hedge's guarantee the same way.",
  22: "So why does this matter? Two reasons. First, the bound needed no assumptions at all about how costs are generated — it holds even against a fully adversarial opponent, which is exactly why it transfers across completely different fields. Second, it unites separate research directions under one theorem: these two papers — 1994 in machine learning, 1991 in optimization — independently invented essentially the same update rule, with no shared citation. One multiplies a wrong trader's weight by beta; the other multiplies a violated constraint's weight by e to the alpha times the violation. Different fields, same theorem underneath.",
  23: "A Nash equilibrium is just a pair of strategies where neither player can do better by unilaterally switching. In a two-player zero-sum game, if decisions are one player's strategies and cost is the other player's best response, running MW on both sides and averaging play over time converges to exactly that. This chart is real self-play on Matching Pennies: each player's instantaneous play cycles, but the running average of both settles onto the equilibrium, fifty-fifty, right where the dotted line is.",
  24: "Poker has an enormous game tree of decision points, not one. CFR decomposes the tree into information sets and runs a separate regret minimizer at each one. If every local minimizer has sublinear regret — cited, not derived here — so does the strategy for the whole game.",
  25: "Vanilla CFR needs to traverse the entire game tree every iteration — fine for Kuhn Poker's twelve information sets, hopeless for real poker's roughly ten to the hundred sixty-one decision points. Monte Carlo CFR instead samples trajectories through the tree each iteration — outcome sampling follows one path, external sampling samples the acting player's actions — and still gets unbiased regret estimates, just noisier per iteration and far cheaper. This chart is real vanilla CFR, run to convergence on Kuhn Poker: the value to Player 1 under CFR's own average strategy converges to the known Nash value, minus one eighteenth. Same convergence claim as every MW chart in this talk — proven exactly, on a game small enough to solve without sampling at all. Libratus needs the Monte Carlo version because its real game is many orders of magnitude bigger.",
  26: "So how does CFR relate to this whole talk? Its actual update isn't this talk's exponential rule — it's regret matching, playing each action proportional to its own positive cumulative regret, proven through a different tool, Blackwell's approachability theorem. But the shape is identical: minimize regret locally, get convergence to equilibrium globally. Brown and Sandholm show Hedge — this talk's exact update — can substitute into that same role, and then Theorem 2.1 applies directly.",
  27: "This machinery is the engine inside Libratus. Three pieces: a blueprint strategy, computed offline over an abstraction of the game; nested subgame solving, which re-solves the current subgame in real time at a much finer resolution once play reaches it; and a self-improvement process that watches for gaps the opponents are exploiting and patches them overnight. The blueprint itself comes from an improved Monte Carlo CFR — regret-based pruning skips actions with very negative regret, for a three-times speedup.",
  28: "None of this is free. Libratus ran on Bridges, the Pittsburgh Supercomputing Center's supercomputer — about twenty-five million core-hours total, split across computing the blueprint equilibrium, real-time subgame solving, self-improvement, and evaluation. The real game of no-limit hold'em has on the order of ten to the hundred sixty-one decision points; the abstraction Libratus actually solves brings that down to about ten to the twelve. Compare that to our n equals eight toy examples all talk — same algorithdm family, twelve orders of magnitude more decisions.",
  29: "In January 2017, Libratus played a hundred twenty thousand hands over twenty days against four top professionals — Dong Kim, Jason Les, Jimmy Chou, and Daniel McCauley — for a two-hundred-thousand-dollar prize pool, in a match called Brains vs. AI: Upping the Ante. It won by 147 milli-big-blinds per game at 99.98 percent significance, and beat every pro individually. The core idea is the one we started with — track something regret-like per decision, bias future play, prove sublinear regret — scaled to roughly ten to the twelve information sets. That's the talk.",
  30: "To close: multiplicative weights minimizes regret against an arbitrary adversary using one potential-function argument; the same argument reappears, independently discovered, in trading and in optimization; and the same core idea, swapped for regret matching and scaled by orders of magnitude, is what actually beats professional poker players. A few open threads for anyone interested: the algorithm needs T in advance to set eta optimally — the doubling trick removes that assumption at a small constant cost; the cost model here is linear, and extending the same argument to more general convex losses is its own line of work; and there are parameter-free, adaptive variants — like optimistic and AdaHedge-style methods — that tune eta on the fly and can do better than the worst case when the adversary isn't actually adversarial.",
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.3 x 7.5
const PAGE_W = 13.3, PAGE_H = 7.5, MARGIN = 0.6;
const BLACK = "1A1A1A", GRAY = "666666";
const HEAD_Y = 0.45, HEAD_H = 0.75;
const BODY_Y0 = 1.55;

function newSlide() {
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  return s;
}

function addKicker(s, text) {
  s.addText(text, {
    x: MARGIN, y: 0.18, w: PAGE_W - 2 * MARGIN, h: 0.3,
    fontFace: "Arial", fontSize: 13, color: GRAY, align: "left", margin: 0,
  });
}

function addHeadline(s, text) {
  s.addText(text, {
    x: MARGIN, y: HEAD_Y, w: PAGE_W - 2 * MARGIN, h: HEAD_H,
    fontFace: "Arial", fontSize: 28, bold: true, color: BLACK, align: "left",
    valign: "top", margin: 0,
  });
}

function addBody(s, text, opts = {}) {
  const y = opts.y || BODY_Y0;
  s.addText(text, {
    x: MARGIN, y, w: PAGE_W - 2 * MARGIN, h: opts.h || 1.2,
    fontFace: "Arial", fontSize: opts.fontSize || 20, color: BLACK,
    align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.3,
  });
}

function addCaption(s, text, y, opts = {}) {
  s.addText(text, {
    x: MARGIN, y, w: PAGE_W - 2 * MARGIN, h: opts.h || 0.35,
    fontFace: "Arial", fontSize: opts.fontSize || 14, color: GRAY,
    align: "left", valign: "top", margin: 0, italic: opts.italic || false,
  });
}

function addEq(s, text, y, opts = {}) {
  s.addText(text, {
    x: MARGIN, y, w: PAGE_W - 2 * MARGIN, h: opts.h || 0.8,
    fontFace: "Cambria", fontSize: opts.fontSize || 24, color: opts.color || BLACK,
    align: "left", margin: 0,
  });
}

function addImageFit(s, key, box) {
  const aspect = ASPECT[key];
  let w = box.maxW, h = w / aspect;
  if (h > box.maxH) { h = box.maxH; w = h * aspect; }
  const x = box.x !== undefined ? box.x : (PAGE_W - w) / 2;
  const y = box.y + (box.maxH - h) / 2;
  s.addImage({ path: A(ASSETS[key]), x, y, w, h });
  return { x, y, w, h };
}

function footer(s, n) {
  s.addText(String(n), {
    x: PAGE_W - 0.9, y: PAGE_H - 0.55, w: 0.5, h: 0.35,
    fontFace: "Arial", fontSize: 11, color: GRAY, align: "right", margin: 0,
  });
}

// ---------- Slide 1: Title ----------
{
  const s = newSlide();
  s.addText("The Multiplicative Weights Update Method", {
    x: 1, y: 2.6, w: PAGE_W - 2, h: 1.1,
    fontFace: "Arial", fontSize: 36, bold: true, color: BLACK, align: "center", margin: 0,
  });
  s.addText("A Meta-Algorithm and Applications", {
    x: 1, y: 3.55, w: PAGE_W - 2, h: 0.6,
    fontFace: "Arial", fontSize: 20, color: GRAY, align: "center", margin: 0,
  });
  s.addText(
    "Seminar 20954  ·  Tal Idelson  ·  Supervised by Prof. Zeev Nutov\nBased on: Arora, Hazan & Kale (2012), Theory of Computing, Vol. 8",
    {
      x: 1, y: 4.3, w: PAGE_W - 2, h: 0.9,
      fontFace: "Arial", fontSize: 14, color: GRAY, align: "center", margin: 0, lineSpacingMultiple: 1.4,
    }
  );
  s.addNotes(NOTES[1]);
  footer(s, 1);
}

// ---------- Slide 2: Program ----------
{
  const s = newSlide();
  addHeadline(s, "Program");
  const items =
`1.  The Problem
2.  The Algorithm
3.  The Guarantee  —  Theorem 2.1
4.  The Proof
5.  Corollaries
6.  Payoff  —  Two Real Papers, One Theorem
7.  Application  —  Poker`;
  s.addText(items, {
    x: MARGIN, y: 1.8, w: PAGE_W - 2 * MARGIN, h: 4.5,
    fontFace: "Arial", fontSize: 22, color: BLACK, align: "left", valign: "top",
    margin: 0, lineSpacingMultiple: 1.9,
  });
  s.addNotes(NOTES[2]);
  footer(s, 2);
}

// ---------- Slide 3: Intuition ----------
{
  const s = newSlide();
  addKicker(s, "Part 1 — The Problem");
  addHeadline(s, "Intuition");
  addBody(
    s,
    "Each round you pick among n options; only afterward does an adversary reveal how every option would have done. Can you do almost as well as the single best option in hindsight — without ever knowing in advance which one that is?",
    { y: BODY_Y0, h: 1.3, fontSize: 20 }
  );
  s.addNotes(NOTES[3]);
  footer(s, 3);
}

// ---------- Slide 4: Problem Definition ----------
{
  const s = newSlide();
  addKicker(s, "Part 1 — The Problem");
  addHeadline(s, "Problem Definition");
  addBody(
    s,
    "Each round: pick p⁽ᵗ⁾, an adversary reveals m⁽ᵗ⁾ ∈ [−1,1]ⁿ, you incur cost m⁽ᵗ⁾·p⁽ᵗ⁾ — over n decisions, T rounds. The goal: bound the excess cost over the single best fixed decision by an explicit, provable limit.",
    { y: BODY_Y0, h: 1.0, fontSize: 18 }
  );
  addEq(s, "Σₜ m⁽ᵗ⁾·p⁽ᵗ⁾ − minᵢ Σₜ mᵢ⁽ᵗ⁾ ≤ ηT + ln(n)/η", 2.65, { h: 0.5, fontSize: 22 });
  addImageFit(s, "oT", { x: (PAGE_W - 7.6) / 2, y: 3.35, maxW: 7.6, maxH: 3.45 });
  s.addNotes(NOTES[4]);
  footer(s, 4);
}

// ---------- Slide 5: Notation (NEW) ----------
{
  const s = newSlide();
  addKicker(s, "Part 1 — The Problem");
  addHeadline(s, "Notation");
  addBody(
    s,
    "Every symbol used for the rest of the talk, in one place:",
    { y: BODY_Y0, h: 0.5, fontSize: 20 }
  );
  s.addTable(
    [
      [
        { text: "symbol", options: { bold: true, fill: { color: "F5F5F5" } } },
        { text: "meaning", options: { bold: true, fill: { color: "F5F5F5" } } },
      ],
      ["n", "number of decisions"],
      ["T", "number of rounds"],
      ["wᵢ⁽ᵗ⁾", "weight of decision i at round t  (starts at 1)"],
      ["p⁽ᵗ⁾", "pᵢ⁽ᵗ⁾ = wᵢ⁽ᵗ⁾ / Φ⁽ᵗ⁾  —  the distribution played at round t"],
      ["Φ⁽ᵗ⁾", "Σᵢ wᵢ⁽ᵗ⁾  —  the total weight (\"potential\")"],
      ["η", "learning rate, fixed with η ≤ 1/2"],
      ["update", "wᵢ⁽ᵗ⁺¹⁾ = wᵢ⁽ᵗ⁾(1 − η·mᵢ⁽ᵗ⁾)"],
    ],
    {
      x: MARGIN, y: 2.15, w: PAGE_W - 2 * MARGIN, h: 4.6,
      colW: [2.0, PAGE_W - 2 * MARGIN - 2.0],
      fontFace: "Arial", fontSize: 17, color: BLACK, border: { type: "solid", color: "CCCCCC", pt: 0.75 },
      autoPage: false, valign: "middle",
    }
  );
  s.addNotes(NOTES[5]);
  footer(s, 5);
}

// ---------- Slide 6: The MW Algorithm ----------
{
  const s = newSlide();
  addKicker(s, "Part 2 — The Algorithm");
  addHeadline(s, "The MW Algorithm");
  addBody(
    s,
    "Init η≤1/2, wᵢ⁽¹⁾=1; each round pᵢ⁽ᵗ⁾=wᵢ⁽ᵗ⁾/Φ⁽ᵗ⁾, observe m⁽ᵗ⁾, then wᵢ⁽ᵗ⁺¹⁾=wᵢ⁽ᵗ⁾(1−η·mᵢ⁽ᵗ⁾). Probability mass shifts toward whichever decisions have cost the least so far.",
    { y: BODY_Y0, h: 0.9, fontSize: 18 }
  );
  addImageFit(s, "algoBox", { x: (PAGE_W - 8.6) / 2, y: 2.55, maxW: 8.6, maxH: 3.9 });
  s.addNotes(NOTES[6]);
  footer(s, 6);
}

// ---------- Slide 7: Example Run ----------
{
  const s = newSlide();
  addKicker(s, "Part 2 — The Algorithm");
  addHeadline(s, "Example Run");
  addBody(
    s,
    "On a random 200-round instance (n=5), MW's regret (12.83) lands well inside Theorem 2.1's bound (35.88).",
    { y: 1.3, h: 0.5, fontSize: 18 }
  );
  const code =
`def multiplicative_weights(costs, eta):          # costs: T x n array, m^(t)_i in [-1,1]
    T, n = costs.shape
    w = np.ones(n)
    alg_cost = 0.0
    for t in range(T):
        p = w / w.sum()                          # p^(t)_i = w_i^(t) / Phi^(t)
        alg_cost += costs[t] @ p                  # incur m^(t) . p^(t)
        w *= (1 - eta * costs[t])                 # w_i^(t+1) = w_i^(t)(1 - eta*m_i^(t))
    return alg_cost`;
  s.addText(code, {
    x: MARGIN, y: 1.9, w: PAGE_W - 2 * MARGIN, h: 2.75,
    fontFace: "Courier New", fontSize: 13, color: BLACK, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.2,
  });
  s.addText("Output (n=5, T=200, random costs):", {
    x: MARGIN, y: 4.8, w: PAGE_W - 2 * MARGIN, h: 0.35,
    fontFace: "Arial", fontSize: 13, color: GRAY, align: "left", margin: 0,
  });
  const output =
`n=5, T=200, eta=0.0897
algorithm total cost:   -3.77
best fixed decision:    -16.61
excess (regret):        12.83
Theorem 2.1 bound O(.): 35.88`;
  s.addText(output, {
    x: MARGIN, y: 5.15, w: 7.5, h: 1.6,
    fontFace: "Courier New", fontSize: 14, color: BLACK, align: "left", valign: "top", margin: 0,
    fill: { color: "F5F5F5" },
  });
  s.addNotes(NOTES[7]);
  footer(s, 7);
}

// ---------- Slide 8: Main Theorem ----------
{
  const s = newSlide();
  addKicker(s, "Part 3 — The Guarantee");
  addHeadline(s, "Main Theorem");
  addBody(
    s,
    "For any fixed decision i and η≤1/2, the algorithm's total cost trails i's total cost by at most two correction terms:",
    { y: BODY_Y0, h: 0.6, fontSize: 19 }
  );
  addEq(s, "Σₜ m⁽ᵗ⁾·p⁽ᵗ⁾ ≤ Σₜ mᵢ⁽ᵗ⁾ + η·Σₜ|mᵢ⁽ᵗ⁾| + ln(n)/η", 2.5);
  s.addNotes(NOTES[8]);
  footer(s, 8);
}

// ---------- Slide 9: From Theorem to Problem (NEW) ----------
{
  const s = newSlide();
  addKicker(s, "Part 3 — The Guarantee");
  addHeadline(s, "From Theorem to Problem");
  addBody(
    s,
    "The theorem holds for every fixed i. Choose i = the best decision in hindsight, and use |mᵢ⁽ᵗ⁾|≤1 to bound the middle term by ηT:",
    { y: BODY_Y0, h: 0.75, fontSize: 18 }
  );
  addEq(s, "Σₜ m⁽ᵗ⁾·p⁽ᵗ⁾  ≤  minᵢΣₜ mᵢ⁽ᵗ⁾  +  ηT  +  ln(n)/η", 2.5, { fontSize: 22 });
  addBody(
    s,
    "Rearrange, and it's exactly the Problem Definition's bound — the same inequality, not a new one:",
    { y: 3.5, h: 0.55, fontSize: 18 }
  );
  addEq(s, "Σₜ m⁽ᵗ⁾·p⁽ᵗ⁾ − minᵢ Σₜ mᵢ⁽ᵗ⁾  ≤  ηT + ln(n)/η        (Slide 4)", 4.25, { fontSize: 22, color: "8a5a28" });
  s.addNotes(NOTES[9]);
  footer(s, 9);
}

// ---------- Slide 10: Proof Strategy (redesigned as explicit sandwich) ----------
{
  const s = newSlide();
  addKicker(s, "Part 4 — The Proof");
  addHeadline(s, "Proof Strategy");
  addBody(
    s,
    "Everything below is one sandwich: bound Φ from both sides, then compare the two sides directly.",
    { y: BODY_Y0, h: 0.55, fontSize: 19 }
  );
  addEq(s, "wᵢ⁽ᵀ⁺¹⁾   ≤   Φ⁽ᵀ⁺¹⁾", 2.35, { fontSize: 23 });
  addCaption(s, "bound 1 — any expert's own weight can't exceed the total (non-negativity)", 2.9, { fontSize: 15 });
  addEq(s, "Φ⁽ᵀ⁺¹⁾   ≤   n · exp(−η·Σₜ m⁽ᵗ⁾·p⁽ᵗ⁾)", 3.5, { fontSize: 23 });
  addCaption(s, "bound 2 — the total can't shrink slower than the algorithm's own rate (next 3 slides)", 4.05, { fontSize: 15 });
  addEq(s, "wᵢ⁽ᵀ⁺¹⁾   ≤   n · exp(−η·Σₜ m⁽ᵗ⁾·p⁽ᵗ⁾)   for every i", 4.75, { fontSize: 23, color: "8a5a28" });
  addCaption(s, "combined — that's the whole proof. The Sandwich Bound slide shows this numerically.", 5.3, { fontSize: 15, italic: true });
  s.addNotes(NOTES[10]);
  footer(s, 10);
}

// ---------- Slides 11-14: proof derivation steps ----------
const proofSlides = [
  {
    headline: "The Potential Φ",
    body: "Recall Φ⁽ᵗ⁾=Σᵢwᵢ⁽ᵗ⁾ from the notation. It mirrors the algorithm exactly, since pᵢ=wᵢ/Φ — and non-negativity is exactly bound 1 from the Proof Strategy slide.",
  },
  {
    headline: "Φ's Per-Round Update",
    body: "Expanding the definition and substituting the update rule gives Φ's exact shrinkage each round:",
    eq: "Φ⁽ᵗ⁺¹⁾ = Σᵢwᵢ⁽ᵗ⁾(1−ηmᵢ⁽ᵗ⁾) = Φ⁽ᵗ⁾(1−η·m⁽ᵗ⁾·p⁽ᵗ⁾)",
  },
  {
    headline: "Telescoping the Bound",
    body: "Since 1−x ≤ e⁻ˣ, telescoping from Φ⁽¹⁾=n bounds Φ after T rounds — this is bound 2 from the Proof Strategy slide:",
    eq: "Φ⁽ᵀ⁺¹⁾ ≤ n·exp(−η·Σₜm⁽ᵗ⁾·p⁽ᵗ⁾)",
  },
  {
    headline: "Bounding Each Expert",
    body: "And bound 1, derived properly: every expert's final weight is bounded above by Φ, and depends only on that expert's own costs:",
    eq: "wᵢ⁽ᵀ⁺¹⁾ ≤ Φ⁽ᵀ⁺¹⁾ = Πₜ(1−ηmᵢ⁽ᵗ⁾)  — holds for every i simultaneously",
  },
];
proofSlides.forEach((p, i) => {
  const s = newSlide();
  addKicker(s, "Part 4 — The Proof");
  addHeadline(s, p.headline);
  let y = BODY_Y0;
  const h = p.eq ? 0.7 : 0.9;
  addBody(s, p.body, { y, h, fontSize: 18 });
  y += h;
  if (p.eq) addEq(s, p.eq, y + 0.15, { fontSize: 22 });
  s.addNotes(NOTES[11 + i]);
  footer(s, 11 + i);
});

// ---------- Slide 15: The Sandwich Bound ----------
{
  const s = newSlide();
  addKicker(s, "Part 4 — The Proof");
  addHeadline(s, "The Sandwich Bound");
  addBody(
    s,
    "Bound 1 and bound 2 together, exactly as previewed. This simulation (n=8, T=250, η=0.12) shows the sandwich holds every round; the labeled gaps are the slack from the two approximations we're about to use.",
    { y: BODY_Y0, h: 0.95, fontSize: 17 }
  );
  addImageFit(s, "sandwich", { x: (PAGE_W - 8.2) / 2, y: 2.5, maxW: 8.2, maxH: 4.35 });
  s.addNotes(NOTES[15]);
  footer(s, 15);
}

// ---------- Slides 16-17: Taking Logs, Completing the Proof ----------
const logSlides = [
  {
    headline: "Taking Logs",
    body: "Taking logs turns the sandwich's products into sums, and cancels the exponential on the upper-bound side — now it's one additive inequality.",
  },
  {
    headline: "Completing the Proof",
    body: "Two more standard approximations, both valid for η≤1/2, turn the logged sandwich directly into Theorem 2.1:",
    eq: "(1−η)ˣ ≤ 1−ηx  and  ln(1/(1−η)) ≤ η+η² ,  for η≤1/2.   ∎",
  },
];
logSlides.forEach((p, i) => {
  const s = newSlide();
  addKicker(s, "Part 4 — The Proof");
  addHeadline(s, p.headline);
  let y = BODY_Y0;
  const h = p.eq ? 0.7 : 0.9;
  addBody(s, p.body, { y, h, fontSize: 19 });
  y += h;
  if (p.eq) addEq(s, p.eq, y + 0.15, { fontSize: 21 });
  s.addNotes(NOTES[16 + i]);
  footer(s, 16 + i);
});

// ---------- Slide 18: Optimal eta (+ chart) ----------
{
  const s = newSlide();
  addKicker(s, "Part 5 — Corollaries");
  addHeadline(s, "Optimal η");
  addBody(
    s,
    "Minimizing the bound ηT + ln(n)/η over η gives η* = √(ln(n)/T):",
    { y: BODY_Y0, h: 0.5, fontSize: 19 }
  );
  addImageFit(s, "etaOpt", { x: (PAGE_W - 8.4) / 2, y: 2.15, maxW: 8.4, maxH: 3.9 });
  s.addNotes(NOTES[18]);
  footer(s, 18);
}

// ---------- Slide 19: Matching Lower Bound (+ chart) ----------
{
  const s = newSlide();
  addKicker(s, "Part 5 — Corollaries");
  addHeadline(s, "Matching Lower Bound");
  addBody(
    s,
    "Draw every decision's cost i.i.d. and unbiased: no algorithm beats 0 in expectation, yet the best decision in hindsight still beats 0 by luck — and that luck gap grows at exactly the Ω(√(T ln n)) rate.",
    { y: BODY_Y0, h: 0.85, fontSize: 17 }
  );
  addImageFit(s, "lowerBound", { x: (PAGE_W - 8.4) / 2, y: 2.5, maxW: 8.4, maxH: 3.6 });
  s.addNotes(NOTES[19]);
  footer(s, 19);
}

// ---------- Slide 20: Regret Vanishes (+ chart) ----------
{
  const s = newSlide();
  addKicker(s, "Part 5 — Corollaries");
  addHeadline(s, "Regret Vanishes");
  addBody(
    s,
    "Dividing the bound by T, average regret per round shrinks to zero as T grows — and n enters only logarithmically:",
    { y: BODY_Y0, h: 0.9, fontSize: 19 }
  );
  addImageFit(s, "regretConv", { x: (PAGE_W - 8.4) / 2, y: 2.55, maxW: 8.4, maxH: 3.5 });
  s.addNotes(NOTES[20]);
  footer(s, 20);
}

// ---------- Slide 21: Beyond MW ----------
{
  const s = newSlide();
  addKicker(s, "Part 5 — Corollaries");
  addHeadline(s, "Beyond MW");
  addBody(
    s,
    "The proof never assumed anything about how costs are generated — even adversarial, even weight-aware ones. The same four-step skeleton (define Φ, bound it two ways, compare via logs) proves guarantees for Hedge and other cost models.",
    { y: BODY_Y0, h: 0.9, fontSize: 19 }
  );
  s.addNotes(NOTES[21]);
  footer(s, 21);
}

// ---------- Slide 22: Independent Discovery (reframed; Two Instantiations cut) ----------
{
  const s = newSlide();
  addKicker(s, "Part 6 — Payoff");
  addHeadline(s, "Independent Discovery");
  addBody(
    s,
    "Why this matters: the bound needs no assumptions about how costs are generated — it holds against a worst-case adversary — and it unites separate research directions under one theorem, as these two papers show independently.",
    { y: BODY_Y0, h: 0.95, fontSize: 17 }
  );
  addImageFit(s, "wm", { x: MARGIN, y: 2.65, maxW: 5.85, maxH: 3.0 });
  addImageFit(s, "pst", { x: PAGE_W / 2 + 0.1, y: 2.65, maxW: 5.85, maxH: 3.0 });
  s.addText("wrong trader → weight × β", {
    x: MARGIN, y: 5.75, w: 5.85, h: 0.4, fontFace: "Arial", fontSize: 14, color: GRAY, align: "center", margin: 0,
  });
  s.addText("violated constraint → weight × e^(α·violation)", {
    x: PAGE_W / 2 + 0.1, y: 5.75, w: 5.85, h: 0.4, fontFace: "Arial", fontSize: 14, color: GRAY, align: "center", margin: 0,
  });
  s.addNotes(NOTES[22]);
  footer(s, 22);
}

// ---------- Slide 23: Nash Equilibria (+ chart + explanation) ----------
{
  const s = newSlide();
  addKicker(s, "Part 7 — Application: Poker");
  addHeadline(s, "Nash Equilibria");
  addBody(
    s,
    "A Nash equilibrium: neither player can improve by unilaterally switching. Decisions as strategies, cost as the opponent's best response — MW self-play's average converges there, no caveat needed:",
    { y: BODY_Y0, h: 0.95, fontSize: 17 }
  );
  addImageFit(s, "nash", { x: (PAGE_W - 8.2) / 2, y: 2.55, maxW: 8.2, maxH: 3.55 });
  s.addNotes(NOTES[23]);
  footer(s, 23);
}

// ---------- Slide 24: CFR: Game Trees ----------
{
  const s = newSlide();
  addKicker(s, "Part 7 — Application: Poker");
  addHeadline(s, "CFR: Game Trees");
  addBody(
    s,
    "Poker's enormous game tree is decomposed into information sets, each running its own regret minimizer. Cited fact, not derived here: sublinear local regret everywhere ⟹ sublinear regret for the whole game (Zinkevich et al. 2007).",
    { y: BODY_Y0, h: 1.0, fontSize: 17 }
  );
  addImageFit(s, "fig1", { x: (PAGE_W - 6.5) / 2, y: 2.75, maxW: 6.5, maxH: 2.6 });
  s.addNotes(NOTES[24]);
  footer(s, 24);
}

// ---------- Slide 25: Monte Carlo CFR (NEW, + chart) ----------
{
  const s = newSlide();
  addKicker(s, "Part 7 — Application: Poker");
  addHeadline(s, "Monte Carlo CFR");
  addBody(
    s,
    "Vanilla CFR traverses the whole tree every iteration — fine for Kuhn Poker's 12 infosets, hopeless for real poker's ~10¹⁶¹. MCCFR samples trajectories instead (outcome / external sampling): unbiased regret estimates, far cheaper per iteration.",
    { y: BODY_Y0, h: 0.95, fontSize: 16 }
  );
  addImageFit(s, "cfrKuhn", { x: (PAGE_W - 8.4) / 2, y: 2.6, maxW: 8.4, maxH: 3.5 });
  s.addNotes(NOTES[25]);
  footer(s, 25);
}

// ---------- Slide 26: CFR vs. MW (table) ----------
{
  const s = newSlide();
  addKicker(s, "Part 7 — Application: Poker");
  addHeadline(s, "CFR vs. MW");
  addBody(
    s,
    "Same shape, different update — and Hedge can substitute directly into CFR's role:",
    { y: BODY_Y0, h: 0.5, fontSize: 19 }
  );
  s.addTable(
    [
      [
        { text: "", options: { fill: { color: "FFFFFF" } } },
        { text: "MW (this talk)", options: { bold: true, fill: { color: "F5F5F5" } } },
        { text: "CFR", options: { bold: true, fill: { color: "F5F5F5" } } },
      ],
      ["update rule", "wᵢ *= (1−η·mᵢ)  — exponential", "play ∝ max(regretᵢ, 0)  — regret matching, linear"],
      ["minimizes", "one global regret", "regret at every information set, separately"],
      ["proof technique", "potential function Φ  (Theorem 2.1)", "Blackwell's approachability theorem"],
      ["guarantee", "sublinear regret ⟹ time-avg → equilibrium", "same — and Hedge can play CFR's role directly"],
    ],
    {
      x: MARGIN, y: 2.15, w: PAGE_W - 2 * MARGIN, h: 3.6,
      colW: [1.7, 5.0, PAGE_W - 2 * MARGIN - 1.7 - 5.0],
      fontFace: "Arial", fontSize: 14, color: BLACK, border: { type: "solid", color: "CCCCCC", pt: 0.75 },
      autoPage: false, valign: "middle",
    }
  );
  s.addNotes(NOTES[26]);
  footer(s, 26);
}

// ---------- Slide 27: Libratus: Architecture (expanded) ----------
{
  const s = newSlide();
  addKicker(s, "Part 7 — Application: Poker");
  addHeadline(s, "Libratus: Architecture");
  addBody(
    s,
    "Three pieces: a blueprint (MCCFR over an abstraction), nested subgame solving (real-time, finer-grained), and self-improvement (patches gaps opponents find, overnight). Regret-based pruning gives the blueprint's MCCFR a 3× speedup.",
    { y: BODY_Y0, h: 0.95, fontSize: 16 }
  );
  addImageFit(s, "fig2", { x: (PAGE_W - 6.2) / 2, y: 2.7, maxW: 6.2, maxH: 3.1 });
  s.addNotes(NOTES[27]);
  footer(s, 27);
}

// ---------- Slide 28: Libratus: Compute (NEW) ----------
{
  const s = newSlide();
  addKicker(s, "Part 7 — Application: Poker");
  addHeadline(s, "Libratus: Compute");
  addBody(
    s,
    "None of this is free. Scale, in one place:",
    { y: BODY_Y0, h: 0.5, fontSize: 19 }
  );
  s.addTable(
    [
      [
        { text: "metric", options: { bold: true, fill: { color: "F5F5F5" } } },
        { text: "value", options: { bold: true, fill: { color: "F5F5F5" } } },
      ],
      ["hardware", "Bridges (Pittsburgh Supercomputing Center)"],
      ["total compute", "≈25 million core-hours"],
      ["  split", "6M equilibrium · 3M subgame solving · 3M self-improvement · 13M evaluation"],
      ["nodes", "196 × 28 cores × 128GB (blueprint/self-improve); 50 nodes/game (real-time)"],
      ["game size", "~10¹⁶¹ decision points, abstracted down to ~10¹²"],
    ],
    {
      x: MARGIN, y: 2.15, w: PAGE_W - 2 * MARGIN, h: 3.3,
      colW: [2.2, PAGE_W - 2 * MARGIN - 2.2],
      fontFace: "Arial", fontSize: 15, color: BLACK, border: { type: "solid", color: "CCCCCC", pt: 0.75 },
      autoPage: false, valign: "middle",
    }
  );
  addCaption(s, "Compare: our simulations all talk use n=8 toy decisions — twelve orders of magnitude smaller.", 5.7, { fontSize: 14, italic: true });
  s.addNotes(NOTES[28]);
  footer(s, 28);
}

// ---------- Slide 29: Libratus: Results (expanded) ----------
{
  const s = newSlide();
  addKicker(s, "Part 7 — Application: Poker");
  addHeadline(s, "Libratus: Results");
  addBody(
    s,
    "Brains vs. AI: Upping the Ante — Rivers Casino, January 2017. 120,000 hands over 20 days against four top professionals, $200,000 prize pool.",
    { y: BODY_Y0, h: 0.7, fontSize: 17 }
  );
  const output =
`margin:          147 mbb/game
significance:    99.98%  (p = 0.0002)
result:          beat all four pros individually`;
  s.addText(output, {
    x: MARGIN, y: 2.35, w: 7.3, h: 1.15,
    fontFace: "Courier New", fontSize: 14, color: BLACK, align: "left", valign: "top", margin: 0,
    fill: { color: "F5F5F5" },
  });
  addImageFit(s, "fig3", { x: (PAGE_W - 8.2) / 2, y: 3.75, maxW: 8.2, maxH: 2.35 });
  s.addNotes(NOTES[29]);
  footer(s, 29);
}

// ---------- Slide 30: Summary & Open Problems (NEW) ----------
{
  const s = newSlide();
  addKicker(s, "Summary");
  addHeadline(s, "Summary & Open Problems");
  const items =
`MW minimizes regret against ANY adversary, via one potential-function argument
The same argument was independently rediscovered in trading and in optimization
The same core idea — regret matching, at scale — beats professional poker players

Open problems:
  •  η needs T in advance — the doubling trick removes that assumption
  •  this talk's cost model is linear — general convex losses are their own line of work
  •  adaptive, parameter-free variants (optimistic MW, AdaHedge) can beat the worst case`;
  s.addText(items, {
    x: MARGIN, y: 1.75, w: PAGE_W - 2 * MARGIN, h: 4.8,
    fontFace: "Arial", fontSize: 17, color: BLACK, align: "left", valign: "top",
    margin: 0, lineSpacingMultiple: 1.5,
  });
  s.addNotes(NOTES[30]);
  footer(s, 30);
}

pres.writeFile({ fileName: "/home/claude/mw_deck/MW_Seminar_Skeleton_v6_FullRevision.pptx" }).then(() => {
  console.log("saved");
});

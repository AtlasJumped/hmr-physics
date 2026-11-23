# Rules with memory, and the balance test in four dimensions

Council computation, 2026-11-22/23. Model output, not Leo's words. Not on the site. No web: nothing here cites a source that was opened. Labels: [EST] established elsewhere (taken from the council files, unverified here), [MEAS] measured here, [CONJ] conjecture, [ANALOGY].

(Saved by HMR Opus V1 from the helper's returned text; the helper could not write files itself.)

## Summary for Leo (120 words)

Any rule that lets a new thought see shape gives some memory. The smallest change we found is tiny in effect. The strongest simple one, "build on thoughts that nothing has built on yet", remembers well but forgets within about a thousand births. One rule keeps a memory that does not fade, but it works like a fuse that can never be reset, and it runs away. No rule produced a pattern that persists like a particle, two stable states, or a stable dimension. Every one breaks two of V1's four conditions, not one. The attention rules copied from AI gave almost no memory. In four dimensions, the "same share at every scale" liking fails more clearly than in two.

## 1. Method

All rules: the new thought picks a focus set S and is born after S and all S rests on. Only the draw of S differs. K = 2 draws unless stated.

| Rule | How S is drawn | What it sees |
|---|---|---|
| K2, K5, P | V1 family: uniform draws; P is the simplest rule | sizes only |
| L | uniform among the last 50 births | birth labels only |
| H | each draw is the higher (longer chain below) of two uniform draws | shape of the candidate's own past |
| M | each draw: chance 1/2 uniform among thoughts with nothing after them, else uniform | whether a candidate has a future |
| N (q) | a uniform; with chance q, b is a sibling of a (shares a direct parent) | local links: "closure by nearness" |
| U (q) | a uniform, plus every sibling of a, each with chance q | same, focus unbounded |
| C | a uniform; b is, of 8 uniform candidates, the one whose local shape (direct parents, direct children, height) is most like a's | content-addressed attention |
| T | as C, but the key is the shape attended to by the previous birth | attention keyed on recent context |

Memory measure: statistics internal to a block of consecutive births (related pairs R, links, longest chain, diamonds, first thoughts), correlated between an early and a later block over many independent runs. Noise: the same with runs shuffled. Dimension: Myrheim-Meyer from the related share, whole pattern and inside intervals by size, and height against size; n = 500, 2,000, 8,000, 32,000, 5 seeds each. The estimator was checked on true 4D scatters: share 0.100 in every interval bin (section 7).

## 2. Which conditions each rule breaks [MEAS, exact]

Exact rational arithmetic on every pattern up to 5 thoughts (conditions_out.txt). Conditions 1 and 4 hold for all by construction.

| Rule | Condition 2 (birth order irrelevant) | Condition 3 (odds depend only on the two pasts) |
|---|---|---|
| K2 | holds, 0 of 23 patterns | holds, 0 of 56 tests |
| L (window 2) | broken, first at 5 thoughts | 0 of 1 (too few cases to say) |
| H | broken, 9 of 23, first at 4 | broken, 32 of 56 |
| M | broken, 9 of 23 | broken, 49 of 56 |
| N | broken, 9 of 23 | broken, 44 of 56 |
| C | broken, 9 of 23 | broken, 52 of 56 |
| U | broken, 8 of 23 | broken, 23 of 56 |

T uses "the previous birth", so it breaks condition 2 by definition (not enumerated). Cost: every hand-built shape rule breaks both 2 and 3. V1 proposes to give up only 3.

The one candidate that keeps 1, 2, and 4 is V1's own form: a reference rule reweighted by a liking of the final pattern. Tested by reweighting 200,000 K2 runs of 24 thoughts (doob_out.txt): liking exp(0.5 x diamonds) gives early/late correlation +0.014 +- 0.005; exp(-0.05 x related pairs) gives +0.008 +- 0.003. About 3 and 2.5 standard errors. Stronger likings left too few effective runs. Verdict: a hint, not a result. At 200 thoughts: nothing detectable.

## 3. Memory [MEAS]

Correlation of related pairs, first block against later blocks (mem_out.txt). "Max" = largest of 25 statistic pairs against the 99th percentile of the shuffled maximum.

| Rule | n=24, 200k runs (noise 0.002) | max / shuffle 99% | n=200, 100k runs, block 1 vs blocks 2, 3, 4 (noise 0.003) | n=2,000, 20k runs, vs blocks 2, 3, 4 (noise 0.007) |
|---|---|---|---|---|
| K2 | +0.002 | 0.004 / 0.008 | +0.004, 0.000, 0.000 | +0.003, -0.003, +0.010 |
| P | 0.000 | 0.003 / 0.008 | 0.000, +0.002, +0.003 | -0.004, +0.010, -0.005 |
| L | +0.001 | 0.005 / 0.008 | 0.000, +0.007, +0.004 | -0.003, -0.004, -0.008 |
| H | -0.015 | 0.034 / 0.007 | -0.014, -0.001, -0.005 | -0.014, -0.001, -0.001 |
| M | +0.159 | 0.195 / 0.008 | +0.154, +0.027, +0.010 | +0.146, +0.027, +0.013 |
| N 0.5 | +0.022 | 0.073 / 0.007 | +0.009, +0.009, +0.004 | +0.008, +0.007, +0.002 |
| N 0.9 | +0.050 | 0.137 / 0.007 | +0.023, +0.014, +0.007 | +0.002, +0.007, +0.007 |
| C | +0.014 | 0.043 / 0.008 | +0.020, +0.013, +0.009 | +0.039, +0.031, +0.007 |
| T | +0.011 | 0.020 / 0.008 | +0.018, +0.018, +0.010 | +0.031, +0.032, +0.024 |
| U 0.1 | -0.004 | 0.028 / 0.007 | -0.007, 0.000, -0.009 | +0.142, +0.115, +0.091 |
| U 0.2 | -0.017 (40k runs) | 0.109 / 0.017 | +0.222, +0.223, +0.233 (20k runs) | not run (too slow) |

Mutual information R-early; R-late at n=24: M 0.017 bits, N 0.9 0.002 bits, all others below 0.001 (shuffle sd 0.00003).

Findings:
1. V1 family and the label-only rule: zero, as the no-memory proof says. Seeing birth labels is not enough. [MEAS, agrees with R2_phys]
2. The smallest change that gives memory is H (a candidate's own past shape). Real (7 standard errors at n=24) and tiny: 0.015.
3. The smallest change that gives strong memory is M (seeing whether a thought has a future).
4. Nearness (N) and attention (C, T): weak, 0.01 to 0.05.
5. U has two regimes, section 5.

## 4. Retention [MEAS]

n = 1,600, blocks of 100, 40,000 runs, blocks 5 onward (retention_out.txt). Correlation of links in a block with a block `lag` births later. Noise 0.0015 at lag 100, 0.005 at lag 1,100.

| Rule | 100 | 200 | 300 | 400 | 600 | 800 | 1,100 |
|---|---|---|---|---|---|---|---|
| K2 | +0.002 | -0.001 | +0.001 | -0.001 | +0.004 | +0.001 | +0.004 |
| M | +0.687 | +0.501 | +0.369 | +0.274 | +0.149 | +0.074 | +0.018 |
| N 0.9 | +0.005 | +0.004 | +0.004 | +0.004 | +0.003 | +0.001 | +0.005 |
| C | -0.003 | -0.001 | -0.001 | -0.002 | 0.000 | -0.001 | -0.002 |
| T | -0.005 | 0.000 | -0.001 | +0.002 | -0.002 | 0.000 | +0.006 |
| U 0.10 | +0.006 | +0.005 | +0.002 | +0.001 | +0.002 | +0.007 | +0.004 |
| U 0.14 | +0.164 | +0.163 | +0.161 | +0.162 | +0.161 | +0.164 | +0.171 |

- M forgets on one time scale: about 27% lost per 100 births (time constant about 320 births), gone by 1,100. The related-pairs statistic shows a slightly faster first step (0.505, 0.291, 0.190, 0.128, 0.065, 0.032); that is not enough to claim a second scale.
- U 0.14 does not decay at all over 1,100 births.
- C and T: no retention in the steady regime. Their small numbers in section 3 come from the start of the run.
- No rule shows a hierarchy of a fast and a slow store. Across rules there is one fading memory (M) and one permanent one (U).

## 5. Multistability, write cost, motifs

Multistable states [MEAS]: not found. U has a threshold between q = 0.12 and 0.16 (multi_out.txt, 30 seeds each, 8,000 births). Below it, direct parents per birth stay near 1.5. Above it they grow without limit (median 74, maximum 343 at q = 0.18 and still rising). At q = 0.12, 1 of 30 runs crossed briefly and returned; at 0.14, 12 crossed and none came back; at 0.16, 27 crossed and 3 dipped back. So this is one metastable state and a runaway, not two stable states with a barrier. It is a fuse, not a bit: written once, never erased, and the "written" state has no fixed form. U's durable memory in sections 3 and 4 is the record of when the fuse blew. M has one stable state.

Write cost [MEAS, and a negative]: bits of free choice per birth given up relative to K2 (entropy_out.txt, births 4,001 to 8,000, 5 seeds): H 0.56, N 0.5 3.5, U 0.14 5.2 (seeds differ, sd 4.2), M 5.6, N 0.9 7.3, U 0.1 10.3, L 13.8. Memory does not track this cost: L pays most and remembers nothing. For M the information carried to the next 100 births is at least 0.46 bits (from the correlation 0.687, one statistic, a lower bound), against about 555 bits of choice given up over those births. So there is a cost in "fewer histories", but no fixed price per stored bit. A Landauer match cannot be tested: the model has no temperature and no erasure step. Not computed for C and T.

Recurring motifs [MEAS]: the diamond (one thought, two built on it, one built on both), dim_out.txt and motif_out.txt.

| Rule | diamonds per 100 births at n = 500 -> 32,000 | diamonds stacked on diamonds, against chance (n=32,000) |
|---|---|---|
| K2 | 1.4 -> 0.04 (dies out) | too few to judge |
| C, T, H, M | die out the same way | too few to judge |
| L | 3.8 -> 4.7 | 0.9 x chance |
| N 0.5 / 0.9 | 46 -> 46 / 94 -> 89 (constant) | 1.03 / 1.02 x chance |
| U 0.1 | 45 -> 107 (growing, bursty) | 1.45 x chance |

N makes the same motif at a constant rate forever, because the rule draws it. The motif does not persist: stacks of diamonds occur at chance level, longest 9 at 32,000. No rule produced a pattern that carries itself forward. Nothing here is a candidate particle.

## 6. Dimension [MEAS]

Whole pattern, mean of 5 seeds (sd 0.02 to 0.20 unless noted), dim_out.txt:

| Rule | d at 500 | 2,000 | 8,000 | 32,000 | inside intervals at 32,000, sizes 16 -> largest bin | verdict |
|---|---|---|---|---|---|---|
| K2 | 3.82 | 4.60 | 5.37 | 6.15 | 1.90 -> 3.53 | drifts |
| K5 | 2.15 | 2.51 | 2.87 | 3.22 | 2.06 -> 4.74 -> 3.82 | drifts |
| L | 1.81 | 1.45 | 1.37 | 1.35 | 1.97 -> 1.08 | a line (height grows as n) |
| H | 2.85 | 3.39 | 3.93 | 4.46 | 1.72 -> 3.90 -> 3.30 | drifts |
| M | 1.69 | 1.72 | 1.76 | 1.79 | 1.01 -> 2.72 | whole value nearly steady, intervals drift |
| N 0.5 | 4.08 | 4.99 | 5.87 | 6.76 | 1.79 -> 3.17 | drifts |
| N 0.9 | 4.38 | 5.46 | 6.52 | 7.59 | 1.56 -> 2.59 | drifts |
| C | 3.89 | 4.72 | 5.55 | 6.39 | 2.25 -> 3.80 | drifts |
| T | 3.84 | 4.66 | 5.48 | 6.29 | 2.02 -> 3.44 | drifts |
| U 0.1 | 5.38 | 6.64 | 7.88 | 9.05 | too few intervals | drifts |
| U 0.2 | 4.63 | 4.52 | 3.50 | timed out | 3.5 -> 3.9 -> 2.7 (n=8,000) | drifts, seeds disagree (sd 0.6) |

No rule stabilizes a dimension. M comes closest (whole-pattern 1.7 to 1.8, chain-growth 1.6 to 1.8), but its intervals read 1.0 at small sizes and 2.7 at large ones, which a space would not do. Memory and dimension did not arrive together anywhere. This agrees with R2_math's bounded-parents argument for the K = 2 rules, and the unbounded rule U did not escape it.

## 7. Task 2: balance test in four dimensions [MEAS]

Done in 4D at 1,000 and 2,000 thoughts (balance.c, bal_out.txt). Differences from R2_phys: moves add or remove one link, so every interval's size and related count update incrementally (checked against a full rebuild: difference below 1e-9); at zero liking the sampler is uniform over labeled orders; five bins (5-9 to 80-159); beta = 100 N squared. Runs: 4e8 steps (N=1,000), 6e8 (N=2,000); two starts (true scatter, simplest-rule pattern), two seeds each for the liking, one each for the null.

N = 2,000, last quarter of each run:

| | longest chain | links | pairs with 1, 2, 3 between | first thoughts | intervals of 20-39 |
|---|---|---|---|---|---|
| True 4D scatter (100) | 12.2 +- 0.7 | 55,100 +- 1,300 | 20,700, 13,100, 9,600 | 212 +- 26 | 19,400 |
| Null, two starts | 3, 2 | 204,600, 206,600 | 0, 0, 0 | 974, 964 | 462, 0 |
| Multi-scale, random start, seeds 1, 2 | 8, 7 | 190,200, 191,800 | 1,900, 1,800, 1,500; 1,500, 1,600, 1,500 | 973, 984 | 1,975, 188 |
| Multi-scale, scatter start, seeds 1, 2 | 12, 12 | 171,100, 173,100 | 2,800, 1,700, 1,900; 2,400, 1,400, 1,500 | 884, 568 | 4,650, 4,260 |

N = 1,000 gives the same picture (links: truth 17,700; multi-scale 43,900 to 48,800; null 51,100 to 51,600).

- The null collapses to two or three layers, the known typical order [EST].
- The liking holds the share at 0.100 in every bin, and the pattern is still far from a scatter: links 3.1 to 3.5 times too many, small intervals 7 to 14 times too few, first thoughts 2.7 to 4.6 times too many. It closes about 10% (random start) to 23% (scatter start) of the null-to-truth gap in links. In 2D at 60 thoughts R2_phys found about two thirds.
- Started from a true scatter, it leaves the scatter.
- A loophole: the liking is met by a small core of intervals sitting inside a mostly two-layer bulk. A mean over intervals does not say how many intervals there must be.
- Convergence: not reached across starts. Each chain is steady between its third and fourth quarter (links within 0.8%), but the two starts disagree (chain 7-8 against 12). At ten times higher beta the scatter start moves away more slowly (links 35,700 and rising at N=1,000). The chains are glassy. The statement that survives: from neither start does the liking reach or hold a scatter. The longest chain of 12 from the scatter start is left over from the start, not evidence.

Verdict: in 4D, "same share at every scale" is a real constraint and clearly not sufficient. Weaker than the 2D toy suggested. The 2D result was not re-run with this sampler.

## 8. Computing and AI analogies [ANALOGY throughout]

| Method | Growth-rule analog tried | Result |
|---|---|---|
| Attention / modern Hopfield (content-addressed) | C: build on the candidate most similar in local shape | memory 0.01 to 0.04 near the start, none in steady state; no dimension |
| Attention over recent context | T | same; also breaks condition 2 by definition |
| Location-addressed memory, fixed context window | L: last 50 births | zero memory; becomes a line |
| Recurrent state with a forget gate | M: the frontier acts as a small running state | strong memory, lost in about 1,000 births |
| Vanishing gradient / catastrophic forgetting | retention curve of M | present: geometric fade, one time scale |
| Local association (triadic closure) | N | motif recurs, memory weak, no persistence |
| Redundant records (error-correcting codes, quantum Darwinism) | U: build on all near thoughts at once | durable, but as a runaway, not a code; redundancy of a specific record not measured |
| Multistable cell with a barrier (magnet, flash) | U near threshold | not found: one-way fuse |
| Refresh (DRAM) | none tried | M's fade is what a refresh would have to fight; no rule refreshes |
| Landauer's limit | choice entropy given up per birth | a cost exists; no fixed price per bit; no temperature, so no match is testable |
| Fast-fragile and slow-durable stores | retention curves | no hierarchy within one rule |
| Bekenstein bound, quantum error correction | none | not testable at these sizes with classical rules |

## 9. Verdicts

1. [MEAS] Shape memory needs a rule that sees order relations, not labels. Every such rule tested has some. Minimal: H (0.015). Minimal and strong: M.
2. [MEAS] No tested rule gives durable, erasable, multistable memory, a persisting motif, or a converging dimension.
3. [MEAS] All hand-built shape rules break conditions 2 and 3 together. The condition-2-keeping form showed only a 3-sigma hint at 24 thoughts.
4. [MEAS] The balance liking fails in 4D at 1,000 and 2,000 thoughts, with chains not converged across starts.
5. [CONJ, a suggestion for Leo, not a result] What is missing is copying: a rule in which an existing shape raises the chance of the same shape nearby later. M and U store a number (how wide, how dense), not a shape. A copy rule was not tried.

Limits: one statistic family for memory (counts in blocks); motif test covers diamonds only; K = 2 for most rules; one parameter value for most; U 0.2 could not be run at 32,000 or in the 2,000-thought memory test; the condition-3 check for L had one test case; no 2D re-run of the balance test; the sandbox clock looked unreliable, so run times are not reported.

# Copy rules: memory, a bit, a lineage, a dimension

Council computation, 2026-11-23. Model output, not Leo's words. Not on the site. No web: no source was opened. Labels: [MEAS] measured here, [EST] from council files, unverified here, [CONJ] conjecture, [ANALOGY].

## Summary for Leo (100 words)

Copying gives memory. Every copy rule remembers strongly, and none forgets on a fixed clock. But copying a local shape only freezes: the mix of shapes set early stays, and a later write leaves a small lasting trace. That is not a bit. A real bit appeared only when the rule favors the shape most common among the latest births: two stable states, a write that sticks past a threshold and otherwise resets, switchable both ways. That bit lives in ongoing activity, one for the whole pattern, not in a place. Shapes do carry themselves forward. No dimension became stable. All rules break two conditions.

## 1. Rules

Base: V1's K = 2 rule. A thought's shape is its direct parents, one step deep: C (one parent), V (two parents, no shared parent), D (two parents sharing a parent, a diamond top). "Make X on a": C builds on a alone; D on a and a sibling; V on a and an unrelated non-sibling. Parents never exceed two.

| Rule | Change to V1 |
|---|---|
| K0, K | pure K2; K2 plus spontaneous C and D (5% each), the control |
| A (q) | twin templating: with chance q, take the parents of a uniform earlier thought |
| F (q) | forward templating: with chance q, pick a uniform thought and make its shape on it |
| B (W) | motif liking, global, saturating: chance of X rises with the square of X's count over about the last W births, floor eps |
| G | same liking, counted over the anchor's parents, siblings, and children |
| T | lineage threshold: copy the anchor's shape with chance 0.9 (T1: 1.0) if its same-shape chain is 3 or longer, else 0.1 |
| D | threshold and overnight reset: days of 200 births; a fast trace wiped nightly; a durable shape s that changes only if a shape took 60% of a day |
| F9f | F 0.9, template from the frontier half the time |

Sizes: dimension to 128,000 thoughts (5 seeds, 3 at the largest); memory 20,000 runs of 2,000; free runs 128,000 births, 6 seeds; write tests 20 seeds. Each run took seconds.

## 2. Conditions [MEAS, exact, up to 5 thoughts]

K0 keeps both. Every other rule, the control K included, breaks condition 2 (8 or 9 of 23 patterns, first at 4 thoughts) and condition 3 (42 to 52 of 56 tests, first at 3). K breaks them because making a diamond looks at siblings. A copy rule in V1's own form (a liking of the finished pattern) was not tried.

## 3. Memory [MEAS]

First block against last of four, 2,000 thoughts, shuffle sd 0.007. Shape counts are not block-internal, so K0 is their baseline.

| Rule | internal related pairs | count of C | count of D | bits, C early to late |
|---|---|---|---|---|
| K0 / K | +0.004 / -0.005 | +0.076 / +0.049 | +0.027 / -0.003 | 0.004 / 0.001 |
| A 0.5 / 0.9 | +0.004 / -0.008 | +0.551 / +0.948 | +0.656 / +0.911 | 0.21 / 1.14 |
| F 0.5 / 0.9 | +0.022 / +0.333 | +0.415 / +0.908 | +0.528 / +0.949 | 0.12 / 0.91 |
| G | +0.532 | +0.966 | +0.965 | 1.24 |
| T / T1 | +0.669 / +0.838 | +0.982 / +0.994 | +0.878 / +0.938 | 1.64 / 1.96 |
| B (W 100) | +0.097 | +0.789 | +0.894 | 0.000 |
| D | +0.005 | -0.007 | -0.015 | 0.000 |

Every copy rule remembers shape, far above the earlier search (best there 0.15). B's correlation comes from a few runs in the other state. D's free runs never leave the starting state; its memory is in section 5.

## 4. Retention [MEAS]

Correlation of the C count between blocks of 100, by lag (noise 0.007):

| Rule | 100 | 300 | 1,100 |
|---|---|---|---|
| K | +0.019 | +0.016 | +0.011 |
| A 0.5 / 0.9 | +0.200 / +0.788 | +0.198 / +0.788 | +0.188 / +0.792 |
| F 0.5 / 0.9 | +0.142 / +0.677 | +0.138 / +0.676 | +0.151 / +0.685 |
| G / T | +0.857 / +0.919 | +0.857 / +0.919 | +0.858 / +0.920 |
| D | +0.096 | +0.001 | +0.003 |

- Templating has no time scale. Memory depends on the ratio of birth times, not the lag. F 0.5, D count, between 1.4 and 6.2 times a block's age: 0.37 to 0.20; in runs 16 times longer, 0.49 to 0.21. Expected fading goes as (age ratio)^-(1-q) [CONJ]; observed factors 0.43 to 0.55 against 0.48. At q = 0.9 almost nothing fades.
- A write agrees: forcing D for 800 births leaves an excess D share of +0.036 falling to +0.028 over 12,000 births (F 0.5), +0.058 flat (F 0.9). The excess is proportional to write length. No threshold.
- D has a fast store gone within a day and a durable one (section 5): the first rule with two stores, by construction.

## 5. Multistability and writes [MEAS]

Local rules (A, F, G, T): no bit. Each run freezes at its own mix: across seeds the C share has sd 0.03 to 0.29, within a run 0.01 to 0.02. T1 seeds ended between 22% and 99% C. Writes barely move it (G: +0.04 after 800 forced births). A graded fuse set by early history.

B: two stable states (C-majority, V-majority) with a barrier. A D state is brief (2% of time). With a linear liking there is one state, so the nonlinearity makes the barrier.

| B, eps 0.10 | W = 10 | 15 | 20 | 25 | 30 |
|---|---|---|---|---|---|
| mean dwell in C / in V (births) | 919 / 1,771 | 1,399 / 2,624 | 2,837 / 5,852 | 3,986 / 10,313 | 18,892 / 20,900 |
| switches, 6 seeds | 562 | 384 | 177 | 107 | 36 |

Switches go both ways (W = 25: 33 and 38). W of 35 to 50 gave 10 or fewer. At W = 100 or more, none in 768,000 births.

Write tests: force one shape for P births, then another 12,000 births later; seeds of 20 holding each written state 8,000 or more births on.

| P | 25 | 50 | 100 | 150 to 800 |
|---|---|---|---|---|
| B, W 100: V, then C | 0, 20 | 2, 19 | 20, 20 | 20, 20 |
| D: D, then C | 0, 0 | 1, 2 | 20, 20 | 20, 20 |

Both are bits, not fuses: below threshold the write relaxes back, above it sticks, and it can be rewritten. B's threshold sits near W ln 2 = 69 [CONJ, mean-field]. D never changed s on its own in 3,840 days; with the fast trace weighted 0.8 it changed 19 to 34 times per run.

Limits: the state is a variable of the rule read from birth labels (last W births, or the day clock). It is one bit for the whole pattern, held by refresh; births older than a few W carry none of it.

## 6. Lineage [MEAS]

Same-shape chains along links at 32,000 thoughts, against the same pattern with shapes shuffled (in brackets).

| Rule | C in a chain of 10 or more | D in a chain of 10 or more | longest D chain, 500 to 128,000 thoughts | bits, thought to parent shape |
|---|---|---|---|---|
| K | 0.000 (0.000) | 0.000 (0.000) | 3 to 5 (2 to 4) | 0.0003 |
| A 0.9 | 0.000 (0.000) | 0.000 (0.000) | 1 to 3 (2 to 5) | 0.18 |
| F 0.5 | 0.028 (0.000) | 0.005 (0.000) | 6 to 13 (2 to 4) | 0.11 |
| F 0.9 | 0.561 (0.018) | 0.020 (0.000) | 3 to 16 (1 to 3) | 0.43 |
| F9f | 0.735 (0.004) | 0.128 (0.000) | 5 to 20 (2 to 4) | 0.40 |
| G | 0.186 (0.024) | 0.010 (0.000) | 4 to 15 (2 to 7) | 0.15 |
| T | 0.634 (0.005) | 0.002 (0.000) | 3 to 11 (2 to 2) | 0.31 |

B and D are at chance. Forward copying makes shapes carry themselves forward, and the longest lineage grows with the pattern, to a third of its height or more. This is the first persisting motif in either search. Limits: in F a lineage continues with chance q at every step whatever its age, so nothing protects it. T protects long ones and the result is a takeover, not an object. A makes families (up to 12,155 thoughts on one parent pair), not lineages. Whether a lineage stays narrow was not measured. Nothing here is yet a particle.

## 7. Write cost [MEAS, lower bounds]

Bits of free choice given up per birth against K2: K 0.9, F 0.5 0.5, D 1.0, T 4.0, F 0.9 7.1, G 9.1, T1 10.0, A 0.9 14.5, B 14.8 in C and 4.3 to 5.1 mostly in V. No fixed price per bit: cost follows which shape is held (one parent costs a whole draw), not how much is remembered. A write costs about 0.7 W forced births while retention grows about tenfold per 15 to 19 of W: the trade seen in real memories [ANALOGY].

## 8. Dimension [MEAS]

| Rule | d at 2,000 | 32,000 | 128,000 | rise per doubling |
|---|---|---|---|---|
| K0 | 4.58 | 6.16 | 6.96 | 0.40 |
| A 0.5 / 0.9 | 6.07 / 8.28 | 8.15 / 10.97 | 9.15 / 12.32 | 0.50 / 0.67 |
| F 0.5 / 0.9 / F9f | 5.07 / 6.27 / 5.32 | 6.59 / 8.27 / 6.79 | 7.35 / 9.06 / 7.27 | 0.38 / 0.39 / 0.24 |
| B | 6.78 | 9.40 | 10.70 | 0.65 |
| G | 6.38 | 8.44 | 9.01 | 0.28 (seed sd 0.8) |
| T / T1 | 5.68 / 6.10 | 7.47 / 8.46 | 8.64 / 10.41 | 0.58 / 0.97 |
| D | 4.74 | 6.35 | 7.17 | 0.41 |

Every rule drifts. Inside intervals all read about 1.8 at 16 thoughts and 3.5 to 4.1 at 512 or more, as K0 does. Height grows as the logarithm of size. This agrees with the bounded-parents argument [EST]. Frontier-only anchors collapse G and T to a line; frontier-only F reads 2.5 to 3.5 and still rises (3 seeds).

## 9. Verdicts

1. [MEAS] Conjecture 5 holds in part: copying gives strong shape memory and the first self-carrying lineage, but no bit and no dimension.
2. [MEAS] Local copying freezes or dilutes. [CONJ] Reason: under uniform draws a thought is built on only about ln(n/i) times ever, so no local store is refreshed.
3. [MEAS] A bit needed a liking nonlinear in the count plus refresh at a constant rate. B and D have both. Cost: the store is global and reads birth labels.
4. [MEAS] All copy rules break conditions 2 and 3.
5. [CONJ, a suggestion for Leo, not a result] Missing next: a local store that is refreshed, meaning growth that returns to the same neighborhood at a steady rate. Uniform draws cannot, and the pure frontier collapses to a line.

Clues [ANALOGY]: "sticks only past a threshold, otherwise resets overnight" matches D and B (D by construction). "Thoughts that generate more thoughts stay selected" matches B: the bit exists only while births remake it. "Returning to a stored shape" matches D's failed writes. "Repeating the first act" matches F: lineages, but no next level measured. "Boundary and binding sites": not tested.

Limits: three shapes, one step deep; K = 2; one or two parameter values per rule; dwell above W = 30 rests on few events; switch counts in ts_out.txt mean something only for B and D; write cost is the entropy of the drawing procedure.

Files: README_files.txt lists code, commands, outputs, and raw data. No binaries kept.

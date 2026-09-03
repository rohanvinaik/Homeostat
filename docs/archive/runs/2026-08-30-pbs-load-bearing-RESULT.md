# Run record — making PBS load-bearing: it works, and it breaks the gates (2026-08-30)

**Restricting the candidate set to §7's top-K PBS ranking DOES make the population
signal load-bearing (cross-cohort seed Jaccard 0.318 vs 0.997 for all-genes). But
the consequence is decisive and negative: once the PBS signal actually drives the
candidate set, the gates that passed on the all-genes graph do NOT robustly hold or
replicate. Gate-pass and PBS-load-bearing are ANTI-CORRELATED. The clean all-genes
results were an artifact of the population signal being inert.**

## The design
Two constructions of §7's bounded-d candidate set, swept over K ∈ {500,1000,2000,
5000}, run on both cohorts (Pan-UKBB, gnomAD SAS):
- **hard**: candidate genes = top-K by gene PBS only.
- **seeded**: seeds = top-K by PBS ∪ their one-hop STRING neighbors (so a low-PBS
  connector can still enter — faithful to §5.8).
Then the LRRK2 gate + §3.2 pleiotropy test on each restricted graph.

## PBS is now load-bearing (the fix worked)
- **Mean top-K PBS seed Jaccard across cohorts = 0.318** (was 0.997 all-genes). The
  two SA cohorts' most-differentiated genes are mostly different, so the candidate
  set is genuinely cohort/population-dependent. The LRRK2 verdict and §3.2 result
  now DIVERGE across cohorts (e.g. hard-5000 LRRK2 PASS/FAIL; seeded-500 FAIL/PASS;
  seeded-2000 PASS/FAIL) — exactly the divergence that was absent before.

## But the gates do not survive it — 0/8 configs pass both gates in both cohorts
| mode | K | seedJ | LRRK2 pk/gn | §3.2 pk/gn | §3.2 obs−null |
|---|---|---|---|---|---|
| hard | 500 | 0.27 | FAIL/FAIL | n/n | 21.5 / 2.0 |
| hard | 1000 | 0.27 | FAIL/FAIL | **Y**/n | 129 / 58 (pk only) |
| hard | 2000 | 0.31 | FAIL/FAIL | n/n | 56 / 27 |
| hard | 5000 | 0.42 | PASS/FAIL | n/**Y** | 42 / 67 (gn only) |
| seeded | 500 | 0.27 | FAIL/PASS | n/n | 31 / 23 |
| seeded | 1000 | 0.27 | **PASS/PASS** | n/n | 17.6 / 19.9 |
| seeded | 2000 | 0.31 | PASS/FAIL | n/n | 18 / 25 |
| seeded | 5000 | 0.42 | PASS/PASS | n/n | 18 / 19 |

- **No configuration has LRRK2 PASS/PASS *and* §3.2 pass/pass** (0/8).
- The two LRRK2 PASS/PASS configs (seeded 1000, 5000) have **§3.2 failing in both**,
  with **observed BELOW null** (obs 17–18 vs null 24–25): under population
  restriction the high-participation "bridges" are LESS pleiotropic than matched
  background — the enrichment inverts.
- The two §3.2 passes (hard-1000 pk; hard-5000 gn) are **cohort-idiosyncratic** —
  each passes in one cohort and fails in the other (129 vs 58; 42 vs 67). Not
  replication; noise.

## The anti-correlation — the crux
Gate-pass concentrates at **large K / seeded** (13,826 nodes ≈ the full graph,
seedJ drifting back up to 0.42) — i.e. where the restriction is weakest and the
analysis approaches the all-genes case (PBS least load-bearing). Genuine
restriction (**small K / hard**, seedJ 0.27, most load-bearing) → LRRK2 FAILs and
§3.2 collapses. **You can have the population signal load-bearing, or the gates
passing — not both.**

## The session-level synthesis (all three probes agree)
1. §8.4 selection-enrichment — the gate that used PBS *values* — **failed** LD
   correction.
2. §3.2 + LRRK2 on the all-genes graph — which do NOT use PBS values — **passed,
   but topologically** (the gnomAD replication proved it: 98.7% identical
   participation despite PBS differing).
3. §3.2 + LRRK2 on the PBS-restricted graph — where PBS IS load-bearing — **do not
   robustly hold or replicate** (this run).

**In no configuration is the population-differential PBS signal doing the work AND
the gates holding.** The current operationalization — E/I/R PBS pile → gene-
participation bridges → pleiotropy / LRRK2 validators — does not cohere as a test
of the population thesis: the population object and the participation metric are
orthogonal.

## What this is and is NOT
- It is **NOT a refutation of the thesis.** It is a demonstration that the current
  *gene-participation gates on static allele-frequency data* cannot validate the
  E/I/R population signal. This is exactly §12.4 (missing dynamics = the binding
  constraint) and §15's NAMED RISK ("the method may be sound while data quality,
  not method, remains the limiting factor"), now shown empirically rather than
  asserted.
- It **IS** the honest fruit of doing what the theory said: §7 demands the candidate
  set be PBS-restricted; doing so revealed the gates were passing only because that
  restriction was absent.

## The fork (do NOT tune K further — that is approach-cycling)
The empirical work has located the problem precisely. The next move is a design
decision, not another parameter sweep:
- (a) The gene-participation gates are the wrong downstream consumer of the PBS
  object. The intended consumer is the §III intelligence layer (κ-descent, with
  selection as the §10.3 weighting) — build THAT to consume PBS, not participation.
- (b) The binding constraint is §12.4: static frequency data cannot carry the
  population-signal validation, and the honest Phase-1 conclusion is
  hypothesis-generation only (§12.7), not mechanism.
- (c) Re-examine whether E/I/R PBS + gene-coupling can be coupled at all, or whether
  the thesis needs a different operationalization on this data.

## Outputs
`pbs_restricted_sweep.json`, `pbs_restricted_sweep_gnomad.json`,
`pbs_restricted_comparison.json`.

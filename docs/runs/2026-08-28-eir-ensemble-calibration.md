# Run record — §13.4 oracle-ensemble calibration (structure-derived slice), 2026-08-28

**Headline: the structure-derived slice does NOT produce a degree-independent
bridge signal. The naive positive result was a hub confound; under a
degree-matched null it is not significant (0/6 resolutions). Reported as a
calibration finding, not massaged.**

## Setup
- Known partition: GWAS Catalog (bulk FTP release — the query endpoint was
  server-side-500ing, see below) MAPPED_TRAIT-exact gene sets for leprosy (99
  genes), Crohn disease (852), IBD (812). Bridge set = genes in >=2 of the
  three single-trait sets: 442 total, **264 present in the STRING physical
  subgraph** (751-gene induced universe).
- Oracle ensemble (structure-derived slice): greedy-modularity carvings at
  gamma in {0.5, 0.75, 1.0, 1.25, 1.5, 2.0}. Signal = mean participation
  coefficient of bridge genes minus the rest, per carving.
- Sourcing note: `/gwas/api/search/downloads` threw a Tomcat **Exception
  report** (server-side, reproduced with a browser UA — not bot-rejection, not
  my request); homepage 200, FTP 200. Switched to the bulk associations file
  (same primary source, working code path). `make gwas-extract` is the
  reproducible step; policy is exact single-trait MAPPED_TRAIT match, so a
  bridge = independently associated in separate focused studies.

## Result — the two nulls disagree, and that IS the finding

| gamma | separation | naive-null p | **degree-matched p** |
|---|---|---|---|
| 0.5  | +0.022 | 0.016  | 0.31 |
| 0.75 | +0.034 | 0.0025 | 0.40 |
| 1.0  | +0.034 | 0.009  | 0.51 |
| 1.25 | +0.048 | 0.0005 | 0.38 |
| 1.5  | +0.051 | 0.0005 | 0.26 |
| 2.0  | +0.066 | 0.0005 | 0.051 |

- **Naive null** (random gene sets, degree-blind): bridge participation
  significant at all 6 resolutions — looks like a clean §6.3 result.
- **Degree-matched null** (fake bridge set drawn to match the real set's
  per-decile degree profile): **not significant anywhere** (min p 0.051).

The gap between the columns is the whole story: bridge genes have elevated
cross-community participation, but *only as much as any equally-connected gene*.
Participation coefficient over PPI physical topology, at this scale, cannot
separate "bridges bridge" from "bridges are hubs."

## Interpretation (honest, and note the genuine tension)

- Pleiotropic bridges ARE high-degree — that is part of the biology (§9). So
  degree-matching is arguably conservative: it removes signal that is partly
  real. The defensible statement is therefore about the **instrument**, not the
  biology: *this metric on this data adds no information beyond node degree.*
- This is precisely what §13.4 is for: "calibrates whether ensemble variance
  behaves as §6.3 predicts **before** it is used on unknown structure." The
  answer for the structure-derived slice: not on its own. A degree-blind
  read-out would have manufactured a significant result — the calibration
  caught it.
- §6.3's actual claim is survival across a DIVERSE oracle ensemble (independent
  traditions + structure), not a resolution sweep of one method. That full test
  needs the traditional-tradition carvings, which need the §6 carving compiler
  (THEORY Part II.6, deferred). This run establishes the structure-derived
  baseline and the degree confound the compiler's members must be scored
  against.
- Consistent with §13.3's FAIL and §13.2's null: at Phase-1 data scale (PPI
  topology + n=1-derived priors, no cohort, no dynamics), the known bridges are
  not cleanly recoverable. The three results agree, for one structural reason.

## Process note (fix, not p-hack)
The first run used a label-shuffle null and reported the §6.3 prediction as
holding at a glance. That null was **wrong** — shuffling community labels
inflates participation for hubs, so it measured the degree confound rather than
controlling for it. Replaced with the degree-matched permutation, which flips
the verdict to negative. A null was changed because the first was demonstrably
confounded, in the stricter direction; both are shown above.

## Outputs
- `data/e_i_r/ensemble_calibration.json` — per-gamma separations, degree-matched
  p, dials, the 264 in-graph bridge genes.
- `data/network/gwas_{leprosy,crohns_disease,inflammatory_bowel_disease}.tsv` —
  reproducible via `make gwas-extract`.

# Run record — §13.2 selection-signature enrichment, first run (2026-08-28)

**Headline: no evidence of iHS enrichment in the top E/I/R pile under the v1
dials. This is a null result and is reported as one.**

## Setup
- Pile: 594,846 candidates → 3,877 LD-collapsed loci with priority > 0
  (positional clumping, 500kb window) → top 1,000 loci; 288 abstained (no iHS
  window data — abstention, never zero), 712 used.
- Validator: PopHuman iHS (1000G phase 3, GRCh37, 10kb windows), mean across
  the 5 SAS populations (≥3 with data required); CEU+GBR as the EUR comparison.
  Independent of the derivation channel: iHS is within-population haplotype
  structure; the pile was built from between-population AF divergence (§10.1).
- Controls: SAS-AF-bin-matched sites from the remaining pool (255,869 usable;
  108,100 abstained; ~231k excluded within 500kb of pile loci), 2,000 seeded
  permutation sets. All dials in `data/e_i_r/enrichment.json`.

## Result
| | pile mean iHS | control mean (sd) | one-sided p |
|---|---|---|---|
| SAS (validator) | 0.7418 | 0.7322 (0.0120) | **0.208** |
| EUR (comparison) | 0.7274 | 0.7358 | 0.740 |

The direction is thesis-consistent (pile sits above controls in SAS, below in
EUR) but the SAS excess is ~0.8 control-sd — not evidence. Recorded as: **the
v1 pile is not detectably enriched for recent positive selection.**

## Interpretation discipline
- Drift passes neither validator (§10.2); a pile dominated by drift + founder
  structure would look exactly like this. That reading is currently live.
- The validator as built is conservative by construction: 10kb window means
  attenuate sharp sweep signals, and averaging across 5 SAS populations
  attenuates population-specific sweeps. This is a sensitivity note, NOT a
  license to iterate dials until significance appears. Any dial exploration
  from here is exploratory, labeled as such, and never promoted post hoc.
- **§13.3 (LRRK2 blind bridge recovery) now does double duty:** positive
  control for the pipeline AND calibration of this validator's sensitivity —
  if a known, population-structured selection story isn't visible through
  these dials, weak sensitivity (not absence of signal) remains a candidate
  explanation for this null.

## Outputs
- `data/e_i_r/loci.tsv.gz` — 3,877 collapsed loci (chrom, pos, priority, n_absorbed).
- `data/e_i_r/enrichment.json` — full result with dials, abstention counts, seeds.

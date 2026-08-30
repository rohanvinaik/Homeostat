# Run record — §8.4 LD-block re-test: INCONCLUSIVE (test miscalibrated)

**Verdict: the preregistered block test (e1b02a2) is MISCALIBRATED on this pile's
structure, and its p is not interpretable as a clean result. Recorded honestly as
inconclusive — NOT reported as a pass, NOT reported as a fail. The LD caveat on
§8.4 remains OPEN; a well-posed replacement is preregistered next.**

## What it returned
- observed block-mean iHS = 0.745 over 1,356 pile blocks
- block-matched permutation p = **0.977** (i.e. control blocks scored HIGHER)
- control blocks with iHS = **1,199**

## Why this is miscalibrated (visible in the run's own diagnostics)
The test defines a "pile block" as any 1Mb window containing ≥1 top-50k-PBS
variant, and removes those whole windows from the control pool. But the top-PBS
variants are **dispersed across 1,579 of the genome's ~2,900 1Mb windows — more
than half.** (This dispersion is the same fact the §8.4 adversarial check reported
as a strength: the pile is genome-wide, not one locus.) The consequence for THIS
test is fatal:
- **control pool (1,199 blocks) is SMALLER than the pile (1,356 blocks)** — the
  non-pile genome is too small to match against;
- **13 of 20 MAF bins are underfilled** (`control_bins_underfilled`): most bins
  cannot supply as many control blocks as the pile needs, so the null is drawn
  from a depleted, MAF-mismatched remnant.

A MAF-matched permutation whose control arm is smaller than its test arm and
underfilled in 65% of bins does not yield an interpretable p. The p = 0.977 is an
artifact of control depletion, not evidence that high-PBS windows lack selection
signal.

## The methodological lesson
Block-COLLAPSING is the wrong LD unit for a genome-wide-dispersed pile: removing
whole windows starves the control set. The pile's dispersion (good for the
not-one-locus claim) is exactly what breaks block-collapsing. The correct LD-aware
correction is to **THIN** the pile to ~one (seeded-random) variant per 1Mb window —
approximately independent representatives — and run the original per-variant
MAF-matched permutation against the FULL, undepleted reservoir. Effective n drops
to ~1,579 (the independence unit) without depleting controls. Random (not
max-PBS) representative → no "lead SNP" selection, so this is decorrelation for an
honest variance, not the forbidden clumping-to-lead-SNP-as-object (Law 2).

## Discipline note (why this is not massaging)
This is not re-tuning to rescue a passed result. The block test's OWN output
(control 1,199 < pile 1,356; 13/20 bins underfilled) shows it is broken
independent of which way the p fell. The replacement is preregistered BEFORE it
runs (next file), and its result — pass or fail — will be recorded as it lands.
The honest current state: §8.4's per-variant p = 0.0005 has NOT been confirmed
LD-robust, and NOT been refuted. The question is open.

## Output
`data/e_i_r/eir_selection_enrichment_ldblock.json` (kept, marked inconclusive).

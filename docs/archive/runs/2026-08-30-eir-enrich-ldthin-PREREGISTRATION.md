# PREREGISTRATION — §8.4 LD-thinned re-test (replaces the miscalibrated block test)

**Committed before the harness exists. Date: 2026-08-30.** Replaces the block-
collapsing test (e1b02a2), which its own diagnostics showed was miscalibrated by
control depletion (pile spans >half the genome's 1Mb windows → control pool
starved, 13/20 MAF bins underfilled; see the block RESULT record). This is the
well-posed LD-aware version of the same question, NOT a re-tune to pass: the
result — pass or fail — is recorded as it lands.

## The question (unchanged)
Is the top of the E/I/R PBS pile enriched for PopHuman SAS iHS beyond a MAF-matched
background, ONCE pseudoreplication from LD is removed? The per-variant §8.4
(p = 0.0005) did not correct for the 50k pile variants' non-independence.

## The correction: THIN, don't collapse (FROZEN)
- **Thin the pile to one variant per 1Mb window.** Group the top-50k PBS pile by
  `(chrom, pos // 1_000_000)`; from each window pick **one variant at random**
  (seeded, `random.Random(20260830)`) — NOT the max-PBS one, so no "lead SNP"
  selection enters. ~1,579 approximately-independent representatives (LD for common
  variants rarely exceeds ~1Mb).
- **Observed** = mean iHS over the thinned representatives that carry iHS data.
- **Controls: the FULL reservoir (undepleted).** MAF-matched per-variant exactly
  as the original §8.4 — same fixed 0.025 MAF bins, controls drawn from the whole
  reservoir minus the pile, with the same per-MAF-bin counts as the THINNED pile.
  The control pool is the whole genome's variants, so it is NOT depleted (the block
  test's fatal flaw is removed because we thin the PILE, we do not remove whole
  windows from the controls).
- **Null:** N_PERM = 2,000; null statistic = mean iHS of the MAF-matched control
  draw; `p = (1 + #{null ≥ observed}) / (1 + n_used)` (add-one). Seed 20260830.
- **Decision:** p < 0.05 → §8.4 survives LD correction (selection enrichment is not
  an LD/pseudoreplication artifact). p ≥ 0.05 → the per-variant enrichment does NOT
  survive honest LD thinning; §8.4 is downgraded to inconclusive/negative and that
  is recorded plainly. Either way, §3.2 (the primary falsifier) and §13.3 (LRRK2)
  are untouched — they are independent validators.

## Why thinning is Law-2-clean
Law 2 forbids LD-clumping to lead SNPs **as the analytic object / significance
definition**. Here the candidate object remains the full PBS pile; thinning is used
ONLY to compute an honest permutation p that does not overcount correlated variants,
and the representative is random, not the lead. This is variance calibration, not
significance-by-clumping.

## Named residual (declared)
1Mb fixed windows approximate LD blocks; they are not recombination-map haplotype
blocks (a future refinement if a recombination map is added). One representative
per window slightly under-uses within-window data, which is the intended
decorrelation, not a defect.

## Output
`data/e_i_r/eir_selection_enrichment_ldthin.json`; a dated RESULT record.

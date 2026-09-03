# PREREGISTRATION — §8.4 selection enrichment, LD-block-corrected re-test

**Committed before the harness exists. Date: 2026-08-30.** A robustness
refinement of the PASSED §8.4 validator (`65e069b`, p = 0.0005), NOT a re-tuning
of it. The original result stands; this asks whether it survives when LD is
handled honestly.

## Why
The §8.4 record named one load-bearing caveat: the 50,000 top-PBS pile variants
are **not independent** — variants within a ~1Mb window are in LD, so the
effective independent n is far below 50,000, and the per-variant permutation
p = 0.0005 overstates confidence. The record named the honest fix: **an LD-block
permutation (block bootstrap)**, explicitly NOT clumping to lead SNPs (that is the
forbidden single-variant move, Law 2). This preregisters exactly that.

## The refinement (FROZEN)
Make the **1,000,000 bp genomic window the exchangeable unit**, not the variant.

- **Blocks:** fixed 1Mb windows, `block = (chrom, pos // 1_000_000)`. (The §8.4
  adversarial check already used 1Mb windows; the pile spans 1,579 of them.)
- **Block iHS:** the mean PopHuman SAS iHS over the block's variants that carry
  iHS data (MIN_POPS = 3, unchanged). A block with zero iHS-covered variants is
  dropped from both arms and the count reported.
- **Observed statistic:** the mean over **pile blocks** of block-mean-iHS — each
  ~LD block contributes once, so a single densely-differentiated window cannot
  inflate the statistic through its variant count.
- **MAF match at block level:** a block's MAF bin = `maf_bin(mean MAF of its
  variants)`, same fixed-width bins (0.025) as §8.4. The null draws control
  **blocks** with the same per-MAF-bin block counts as the pile, from reservoir
  blocks not overlapping pile blocks.
- **Null:** N_PERM = 2,000 block-level MAF-matched draws; null statistic = mean
  of drawn block-mean-iHS. `p = (1 + #{null ≥ observed} + ... )/(1 + n_used)`
  (add-one). Seed 20260830.
- **Decision:** p < 0.05 → **§8.4 survives LD-block correction** (the selection
  enrichment is not an LD artifact). p ≥ 0.05 → the per-variant result was
  LD-inflated; record honestly and down-weight §8.4 accordingly (do NOT re-tune).

## Expectation and honest reading
Collapsing to ~1,579 blocks reduces the effective n by ~30×, so the LD-block p
**will be less extreme than 0.0005** by construction — that is the point, not a
failure. The question is whether it stays below 0.05 on the block units. The
1Mb-window spread already reported (densest window 1.1% of the pile) predicts it
should. A survive-at-block-level result is the robust one worth carrying.

## Named residual (declared, not eliminated)
Pile blocks use ALL their pile variants; control blocks use the per-MAF-bin
reservoir sample of that window's variants (the reservoir bounds cost — computing
iHS for all ~10M variants is the perf trap `eir_enrich` already avoids). So a
control block's mean-iHS is a sampled estimate; a pile block's is complete. This
is a minor asymmetry in a control arm, noted so the p is read with it in view.
1Mb fixed windows approximate LD blocks; they are not recombination-defined
haplotype blocks (a future refinement if a recombination map is added).

## Output
`data/e_i_r/eir_selection_enrichment_ldblock.json`; a dated RESULT record. The
original `eir_selection_enrichment.json` is untouched.

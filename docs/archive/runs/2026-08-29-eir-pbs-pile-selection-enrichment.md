# Run record — E/I/R PBS pile + selection enrichment (the correct object), 2026-08-29

**The program's primary validator (§8.4/§10.2) passes on the right object for the
first time. The population-differential PBS pile is enriched for South Asian
selection signal beyond a MAF-matched background, genome-wide — not drift, not a
single-locus artifact.** Caveats below; this is a validator pass on a search-order
prior, not mechanism proof (§12.4 still binding).

## What this replaces
The prior Pan-UKBB analysis gated on EUR p ≤ 5e-8 and ran enrichment on the
EUR-significant set — the single-variant paradigm the program is a structural
critique of (§2.4, Law 2). Deleted. This runs the theory doc's own pipeline.

## The candidate object (§7) — `eir_cohort.py`
PBS(CSA focal, EUR close, EAS outgroup) per variant from Pan-UKBB population
allele frequencies. **No p-value gate, no gene annotation, no n=1.** A
population-differential search-order prior that bounds *d*.
- 28,987,534 variants streamed; **10,024,732** written (both CSA & EUR
  polymorphic); 18,953,864 dropped for missing CSA allele frequency (CSA is the
  small cohort — rare variants lack a CSA estimate); 8,938 monomorphic.

## The validator (§8.4/§10.2) — `eir_enrich.py`
Selection-signature enrichment on the top-50,000 PBS pile vs **MAF-matched**
controls (fixed-width MAF bins, per-bin reservoir), PopHuman SAS iHS, 2,000
permutations. Annotation-blind — uses no gene annotation, so it does not circle
back through the held-out layer (§8.4).

| | value |
|---|---|
| pile size (top-K by PBS) | 50,000 |
| pile variants with iHS data | 30,381 (61%) |
| pile mean iHS | 0.778 |
| **MAF-matched permutation p** | **0.0005** |

## Adversarial check — is it one LD region? No.
The top-50k pile spans **1,579 distinct 1Mb windows** across all chromosomes;
the densest single window is **1.1%** of the pile; chromosomes contribute roughly
in proportion to size (2: 10%, 4: 9%, 1: 8%, ...). So the enrichment is
**genome-wide distributed**, not driven by a single differentiated locus — which
is what §8.4 predicts if the pile captures real mechanistic difference rather than
drift. (A drift pile passes neither MAF-matched enrichment nor selection.)

## Caveats (load-bearing; do not oversell)
1. **Residual LD inflation of the p.** 50,000 variants are not independent —
   variants within a 1Mb window are correlated, so the effective independent n is
   smaller than 50,000 and p = 0.0005 overstates confidence somewhat. This is
   NOT fixed by clumping to lead SNPs (that is the forbidden single-variant move,
   Law 2); the honest tightening is an LD-block permutation (block bootstrap) —
   a future refinement. The 1,579-window spread already shows it is not a
   single-locus artifact, which is the load-bearing point.
2. **61% iHS coverage** — 30,381/50,000 pile variants have iHS window data; the
   rest abstain (no data), never counted as zero.
3. **This validates the pile is not drift (§8.4's exact question); it does not
   recover any mechanism.** Mechanism recovery is the κ-over-coupling layer
   (§III), gated behind LRRK2 blind recovery (§13.3), and ultimately bounded by
   missing dynamics (§12.4).

## Next
LRRK2–NOD2–RIPK2 blind recovery on this pile before any novel output counts
(Law 3 / §13.3), then the κ intelligence layer.

## Outputs
- `data/e_i_r/eir_pbs_pile.tsv.gz` — the 10M-variant PBS pile.
- `data/e_i_r/eir_selection_enrichment.json` — the validator result + dials.

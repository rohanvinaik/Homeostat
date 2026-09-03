# Run record — Pan-UKBB eosinophil count, EUR vs CSA (2026-08-29)

**The first cohort-scale signal in the project — not resting on n=1 — and it is
thesis-consistent. Two controls are needed before the numbers are claims; both
are named below and NOT yet run.**

Free data: `s3://pan-ukb-us-east-1` (AWS Registry of Open Data, anonymous
access, no affiliation, no fee). Phenotype: continuous-30150 eosinophil count
(irnt), 8,502 CSA individuals, QC-PASS. 28,987,534 variants streamed (GRCh37);
13,335,283 EUR-confident with a CSA effect estimate; 114,339 EUR genome-wide-
significant (p ≤ 5e-8) with both populations confident.

## Result 1 — effect-size transferability (§8.1), measured directly
| metric | value |
|---|---|
| sign concordance beta_EUR vs beta_CSA (at EUR-sig variants) | **0.742** |
| Pearson r beta_EUR vs beta_CSA (at EUR-sig) | **0.467** |
| genome-wide beta Pearson (all 13.3M) | 0.003 (≈0, expected — mostly null×null) |
| EUR-sig variants replicating direction at CSA p<0.05 | 14,557 / 114,339 |

**Read:** European-discovered eosinophil effects transfer to South Asians
**partially** — clearly above chance (0.5 concordance / 0 correlation) but far
from perfect. ~1 in 4 EUR-significant variants flips direction. This is §8.1's
"reduced portability," now a measured number rather than an n=1 assertion.

**Caveats (load-bearing — the value is directional, the precise number is not
yet publishable):**
- **Not LD-independent.** 114,339 variants clump into far fewer independent
  loci; the per-variant statistics overstate n and narrow the apparent CI. LD
  clumping is required for a locus-level estimate.
- **CSA is underpowered** (8,502): beta_CSA is noisy, which ATTENUATES r by
  measurement error — true transferability is ≥ 0.467, not ≤.
- **Winner's-curse on the EUR side** inflates apparent non-transfer.
- The 14,557 "replicated" is a floor set by CSA power, not a transfer rate.

## Result 2 — population divergence at trait loci (§7)
| metric | value |
|---|---|
| mean F_ST(CSA,EUR) at EUR-sig loci | 0.0294 |
| mean F_ST(CSA,EUR) genome-wide background | 0.0172 |
| **enrichment ratio** | **1.71×** |
| mean PBS (CSA focal, EUR close, EAS out) at sig loci | −0.003 |

**Read:** eosinophil-associated variants are ~1.7× more differentiated between
South Asians and Europeans than the genome-wide average — trait architecture is
population-structured. BUT PBS ≈ 0 means this is **general EUR–CSA
differentiation, not CSA-specific selection** at these loci; do not overclaim a
sweep.

**CRITICAL caveat — the §13.4 lesson applies verbatim.** This enrichment is NOT
MAF-matched. Genome-wide-significant variants skew common (power), and common
variants have a systematically different F_ST distribution than rare ones. The
1.71× could be partly or wholly a MAF confound. **A MAF-matched background is
required before this is a claim** — exactly the degree-matching discipline that
overturned the §13.4 naive result. Until then: suggestive, not established.

## What is solid regardless of the caveats
- **The n=1 dependency is broken.** Every prior phase (§13.2/13.3/13.4, Phase-2)
  rested on one genome or a European-calibrated array; this rests on 8,502 South
  Asian individuals' allele frequencies and effect sizes. The machinery runs end
  to end on real cohort data, free.
- Both signals point the thesis's way (partial transfer + trait-locus
  differentiation), which is more than any prior phase produced.

## Next (decisions, not yet run)
1. **LD-clump** the EUR-sig set to independent loci → clean transferability CI.
2. **MAF-matched F_ST background** → turn the 1.71× into a claim or retire it.
3. **More phenotypes:** the other well-powered CSA traits (eosinophil %, asthma
   J45, rheumatoid arthritis phecode 714) — is partial-transfer + differentiation
   consistent across the inflammatory panel, or eosinophil-specific?
4. Heritability note already in hand: h2 is higher in CSA (0.26) than EUR (0.20)
   for this trait — cross-check with the transfer/divergence picture (different
   estimators per ancestry; treat as a lead).

## Output
`data/e_i_r/panukbb_eos_eur_vs_csa.json` — full result, dials, counts.

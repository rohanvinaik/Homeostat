# Run record — §8.4 LD-thinned re-test: NEGATIVE (§8.4 does not survive LD correction)

**Verdict under the preregistration (8a72ade): the §8.4 selection-signature
enrichment does NOT survive honest LD correction. This is a real, clean negative —
recorded as such, not rescued. The per-variant p = 0.0005 was substantially LD
pseudoreplication.**

## Result (well-posed: controls undepleted, all bins full)
| | value |
|---|---|
| thinned pile (1 random variant / 1Mb window) | 1,579 |
| thinned variants with iHS data | 991 |
| observed mean iHS | 0.735 |
| **LD-thinned permutation p** | **0.985** (control draws scored HIGHER) |
| control bins underfilled | **none** (all 2,000 perms valid) |

Unlike the block-collapse test (which was miscalibrated by control depletion),
this one is well-posed: thinning the PILE to independent representatives leaves the
full-genome reservoir intact, so MAF-matched controls are abundant and no bin
underfills. The negative is therefore interpretable, and it is unambiguous:
p = 0.985 is nowhere near the 0.05 threshold, so the seeded choice of
representative is immaterial (a different pick cannot move it to significance).

## What flipped, and the honest reading
Per-variant §8.4: pile mean iHS 0.778, p = 0.0005 (pile ABOVE MAF-matched controls).
LD-thinned: pile mean iHS 0.735, p = 0.985 (pile BELOW controls). The observed
barely moved (0.778 → 0.735); the enrichment vanished because the per-variant test
counted many LD-correlated variants in a few high-iHS windows as independent
evidence. At one ~independent variant per window, that pseudoreplication is gone,
and the high-PBS pile is not iHS-enriched — if anything mildly the reverse.

**Biological reading (offered as interpretation, not established):** PBS measures
BETWEEN-population differentiation (CSA vs EUR/EAS); iHS measures WITHIN-population
recent positive selection (long haplotypes). They are different signatures. A pile
selected for between-population differentiation need not be under ongoing
within-SAS selection — drift and population-specific history also drive PBS. So
§8.4's premise ("a real mechanistic pile should be iHS-enriched") is simply not
borne out by iHS. This does not show the pile is drift; it shows *this particular
selection validator does not corroborate it.*

## What this does and does NOT change
- **§8.4 (selection-signature enrichment, §10.2 validator #1): DOWNGRADED from
  "PASS p=0.0005" to NEGATIVE / not LD-robust.** Do not cite the per-variant p as
  evidence going forward.
- **§3.2 annotation-recovery (the program's PRIMARY falsifier, §3.2/§10.2):
  UNTOUCHED. Still PASS, p < 1e-4, dose-responsive, robust to LRRK2 removal.** It is
  independent of the selection channel and independent of annotation.
- **§13.3 LRRK2 bridge recovery: UNTOUCHED. Still PASS, p = 0.023.**

§10.2 states the two primary validators "fail differently, which is why both are
needed." That is now literally instantiated: one (annotation-recovery) passes
robustly; the other (selection-enrichment) does not survive LD correction. The
program's evidentiary weight now rests on annotation-recovery + the LRRK2 control,
NOT on selection enrichment. That is a real reduction in support, reported plainly.

## Discipline note
Two independent LD corrections (block-collapse, thin) both failed to reproduce the
enrichment; the well-posed one is decisive. No further variant was run to rescue it
— that would be the method-cycling trap. The honest state: §8.4 is retired as a
passing validator; the finding is that its per-variant significance was an LD
artifact. A forensic follow-up (why the MAF-bin composition flips the control mean)
is available if wanted, but it cannot make a p=0.985 into a pass.

## Output
`data/e_i_r/eir_selection_enrichment_ldthin.json`.

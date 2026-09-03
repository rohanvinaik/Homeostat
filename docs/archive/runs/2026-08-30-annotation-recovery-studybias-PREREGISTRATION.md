# PREREGISTRATION — §3.2 study-bias-controlled re-test

**Committed before the harness exists. Date: 2026-08-30.** Closes the named
residual confound of the passed §3.2 test (`a239d01`): well-studied genes accrue
both more STRING edges and more GWAS traits, so pleiotropy enrichment could be a
study-bias artifact. This adds an INDEPENDENT study-intensity control and asks
whether the enrichment survives. Not a re-tune: result — survive or collapse —
recorded as it lands.

## The confound is real (pre-run design calibration, not the outcome)
Per-gene PubMed count (NCBI gene2pubmed, distinct PMIDs per human gene):
- **candidate bridges mean 381 citations vs background mean 191** (median 96.5 vs
  76) — candidates are ~2× more studied. The confound the §3.2 record named is
  present and material.
- Candidate study-tertile distribution skews high: {low 177, mid 186, high 265}.
This is *why* the control is needed; the pleiotropy enrichment must be shown to
exceed what study intensity alone would produce.

## The control: add study-intensity to the matched null (FROZEN)
Re-run the §3.2 primary test with a THIRD matching stratum:
- **Match = degree ±20% AND pbs_weight ±0.02 AND same PubMed tertile.** Tertiles
  are the `n//3` and `2n//3` order statistics of PubMed count over ALL scorable
  genes (deterministic; genes absent from gene2pubmed → count 0 → low tertile).
- Everything else identical to the passed §3.2 (frozen, `16ddddf`): candidate set
  = the 628 (p<0.05); statistic = mean-pleiotropy difference, one-sided; N_PERM =
  10,000; seed 20260830; add-one p; without-replacement within a draw.
- **Feasibility (pre-run):** 3-way matching drops only **6/628** candidates —
  pools stay populated. Dropped candidates reported.
- **Decision:** p < 0.05 → the §3.2 pleiotropy enrichment SURVIVES study-bias
  control (it is not merely that candidates are better-studied). p ≥ 0.05 → study
  intensity explains the enrichment; §3.2 is downgraded and recorded plainly.

## Sensitivities (declared; same as §3.2)
Same 3-way matching applied to: top-100 and top-300 by p; leave-LRRK2-out. Robust
if the survival is monotone and not carried by the one famous gene.

## Interpretation guard
Even a survival here is degree+PBS+study-intensity-conditioned, not causal:
PubMed count is a proxy for study intensity, tertiles are coarse, and pleiotropy
itself partly drives citations (a gene studied because it is pleiotropic). The
honest claim on survival is "pleiotropy enrichment beyond what degree, PBS, AND
coarse study-intensity strata jointly explain" — a strong control, not a proof of
mechanism. Still §12.4-bounded.

## Output
`data/e_i_r/annotation_recovery_studybias.json`; a dated RESULT record. The passed
§3.2 result is untouched.

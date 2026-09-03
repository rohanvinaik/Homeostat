# PREREGISTRATION — §III intelligence layer: selection-weighted κ (PBS as the §10.3 prior)

**Committed before the harness exists. Date: 2026-08-30.** The PBS-restriction
result showed a hard node-set restriction makes PBS load-bearing but breaks the
gates. This builds the INTENDED consumer instead (THEORY_OF_THE_CASE Part III): the
κ-descent over the coupling graph, with PBS entering SOFTLY as the §10.3 prior
weighting on the coherence math — not as a node filter.

## The theory this realizes
- §5.5: κ = marginal coverage = hub-score = PageRank over the structure graph.
- §10.3: "Steps under strong differential selection get higher PRIOR PARTICIPATION
  in the coherence math. The selection scan is both validator and prior."
- The existing sigsearch null (`sigsearch_baseline.json`, committed): unweighted κ
  over STRING∪GTEx surfaces GENERIC inflammation hubs (RELA/STAT3/...); the known
  population-structured bridges LRRK2/NOD2/RIPK2 sit MID-PACK. Its own recorded
  conclusion: "structure + unweighted κ alone does NOT isolate the bridges... the
  next build (selection-weighted κ) is what must lift the specific bridges above
  generic hubs." THIS is that build.

## The construction (FROZEN)
- **Coupling graph**: STRING physical ∪ GTEx co-expression over the pile-weighted
  genes (the same `build_coupling_graph` the gates use) — the whole graph, no PBS
  node restriction.
- **κ_unweighted** = PageRank with uniform teleportation (the sigsearch null).
- **κ_PBS** = PERSONALIZED PageRank with teleportation vector ∝ gene PBS weight
  (normalized over nodes). This is §10.3: differential-selection genes get higher
  prior participation, and the prior DIFFUSES through the structure (a gene coupled
  to high-PBS genes is lifted too — the coherence math, not a per-node multiply).
- Controls (LRRK2/NOD2/RIPK2) are LABELLED in output, never used in ranking (§5.9).

## Preregistered tests and decisions
1. **Positive control — does selection-weighting LIFT the bridges? (the §13.3 analog)**
   Criterion: the mean rank of {LRRK2, NOD2, RIPK2} under κ_PBS is BETTER (smaller)
   than under κ_unweighted, in BOTH cohorts. Report each control's rank + percentile
   under both. A lift that replicates is the pass. (Directional, one-sided:
   selection-weighting should help, not hurt.)
2. **Not-trivial guard — beats raw PBS alone.** Also rank genes by raw PBS weight
   alone. κ_PBS must surface the controls BETTER than raw-PBS-alone (else the graph
   adds nothing and it is just PBS) AND better than κ_unweighted (else selection adds
   nothing). The claim is the graph-diffused selection prior beats either component
   alone.
3. **Pleiotropy of the top (§3.2 on the new ranking).** Are the top-N by κ_PBS
   enriched for GWAS pleiotropy vs a degree+PBS-matched background — and does THIS
   replicate across cohorts (unlike the PBS-restricted gates, which did not)?
4. **Load-bearing + replication.** κ_PBS ranks must DIVERGE across cohorts more than
   κ_unweighted (which is cohort-independent, ~topological) — proving PBS is
   load-bearing here — while the control-lift REPLICATES. Divergent-yet-replicating
   is the coherent outcome the restriction approach failed to achieve.

## What each outcome means
- **Lift replicates + top pleiotropy-enriched in both cohorts** → the §III layer is
  the coherent PBS consumer: selection-weighted κ isolates the population-structured
  bridges the gates could not. The thesis is operationalized.
- **Lift does not replicate, or κ_PBS ≈ κ_unweighted** → soft PBS-weighting also
  fails to make the population signal do coherent work on static data; that
  strengthens the §12.4 (missing-dynamics) conclusion. Recorded honestly.
- No K to tune here; the only dial is PageRank damping (fixed 0.85, the standard).

## Output
`sig_descent.json` (+ `_gnomad`); a dated RESULT record; cross-cohort comparison.

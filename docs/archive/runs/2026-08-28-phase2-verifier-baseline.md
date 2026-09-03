# Run record — Phase-2 verifier baseline (deterministic, no LLM), 2026-08-28

**The null for the significance-search layer. Two findings, both shaping the LLM
proposer build.**

## Setup
- Grounded base graph = STRING physical UNION GTEx co-expression (cross-tissue
  Pearson >= 0.70 on the v8 gene-median-TPM matrix), induced on the GWAS
  universe (1,299 leprosy/Crohn/IBD genes).
- κ = PageRank hub-score (the §5 form; the reachable-set form degenerates on an
  undirected substrate — see `kappa.py` transport note).
- Controls LRRK2/NOD2/RIPK2 labelled, never used in ranking (§5.9 firewall).

## Finding 1 — the "two clusters" premise does not hold at this granularity
Under STRING+co-expression the universe is **one module**: 938 of 1,299 genes in
the giant weak component, the other 352 components all size <=3. There are no
two structurally-separated immunity/IBD clusters to bridge at the gene-universe
level — they are one interwoven inflammation module. So literal component-joining
(is_bridge) is trivial here, and the operative κ is within-module hub-score.

## Finding 2 — raw κ surfaces GENERIC hubs; the known bridges sit mid-pack
Top κ hubs: RELA, THADA, STAT3, SMARCE1, MED30, SNX13, BRD2, CDKAL1, ... — the
canonical inflammation hubs, exactly what unweighted centrality should surface.

| control | κ rank / 1299 | percentile |
|---|---|---|
| RIPK2 | 236 | top 18% |
| LRRK2 | 622 | top 48% |
| NOD2  | 716 | top 55% |

The known population-structured bridges are unremarkable under structure +
unweighted κ. This is consistent with §13.2/13.3/13.4: raw structure at this
scale does not isolate the bridges from generic connectivity.

## What this null establishes for the LLM-proposer build
1. **The LLM must bring OUT-OF-UNIVERSE candidates.** The controls are already
   in the GWAS sets and are mid-pack hubs; the value the proposer adds is
   surfacing bridge genes/mechanisms the GWAS sets do NOT contain, which
   structure then grounds and κ then ranks. (This is also where LRRK2 could be
   recovered despite failing §13.3 — it need not clear the European-calibrated
   array; but see the proposal-contamination caveat in PHASE2_SIGNIFICANCE_SEARCH.md.)
2. **κ must be selection-weighted (§10.3).** Unweighted κ = generic hubs. The
   iHS selection prior is the orthogonal signal that should lift
   population-differential bridges above generic inflammation hubs. Weighting κ
   by selection is the first refinement, and it uses no gene annotation (§10.2
   legitimacy).
3. **The bar for the proposer:** beat this null — surface, above the generic
   hubs, bridges that are (a) grounded in structure the LLM never saw and (b)
   enriched for the selection signal. Preregister the criterion before the run.

## Discipline
Thresholds were NOT tuned to manufacture clusters after seeing the blob. The
one-module finding is reported as-is; it corrects the design (κ = hub-score, not
component-join, on this substrate) rather than being optimised away.

## Outputs
- `data/e_i_r/sigsearch_baseline.json` — module stats, top-30 κ hubs, control ranks.
- New reusable spine: `kappa.py` (κ math, Regenesis-faithful), `coexpr.py`
  (GTEx grounding channel).

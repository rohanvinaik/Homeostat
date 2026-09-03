# Run record — gnomAD SAS replication: gates replicate, but the replication reveals the PBS is not load-bearing (2026-08-30)

**The pile + both live gates replicate almost exactly on an independent South
Asian cohort (gnomAD v2.1.1 SAS exomes). But the near-identity is itself the
finding: it proves the passing gates are driven by the STRING∪GTEx graph topology,
NOT by the population-differential PBS signal. This empirically confirms the LRRK2
gate RESULT's caveat #4 ("the recovery is topological").**

## The replication (gnomAD v2.1.1 SAS exomes vs Pan-UKBB CSA)
Independent SA reference: different cohort, different platform (exome sequencing vs
array/imputation), different individuals, GRCh37 (no liftover). 1,360,052 coding
variants (from 17.2M streamed) vs Pan-UKBB's 10M genome-wide.

| gate | Pan-UKBB | gnomAD SAS | replicates? |
|---|---|---|---|
| §13.3 LRRK2 gate | PASS, part 0.041, p=0.023 | **PASS**, part 0.0412, p=0.026 | ✅ ~identical |
| §3.3 bridge discovery | 628 candidates, LRRK2 rank 300 | 627 candidates, **rank 301** | ✅ ~identical |
| §3.2 annotation-recovery | obs 34.7 / null 23.9, p<1e-4 | obs **34.80** / null 24.12, **p<1e-4** | ✅ ~identical |
| §3.2 top-100 | 53.5 | **53.52** | ✅ identical |
| §3.2 leave-LRRK2-out | 34.7 | **34.77** | ✅ ~identical |

## Why it is near-identical — the load-bearing diagnostic
Directly comparing the two piles' full per-gene score tables:
- **99.7% gene-set overlap** (13,789 common of 13,816∪13,800).
- **98.7% of common genes have IDENTICAL participation**; 89% identical degree.
- **But the PBS weights differ substantially**: mean 0.070 (Pan-UKBB) vs 0.045
  (gnomAD), mean |diff| 0.036, max 2.28.

So the population-differential signal (PBS) is genuinely different between the two
cohorts, yet the participation metric — which drives §3.2 and the LRRK2 gate — is
98.7% unchanged. **The gates are a function of the coupling-graph topology, not of
the PBS.** By construction: `degree_matched_p` (bridge_discovery) is computed from
`participation` and `degree`, both pure graph properties; PBS enters ONLY through
which genes are nodes (`candidates = genes-with-any-pile-variant ∩ STRING`), and
because nearly every gene has some coding variant, that node set is ~99.7% the same
for any pile. **PBS gates near-universal node membership and nothing else the metric
consumes.**

## The honest synthesis (with the §8.4 hardening result)
- The ONE gate that actually used PBS *values* — §8.4 selection-enrichment (ranks
  the top-50k by PBS) — did NOT survive LD correction (retired).
- The gates that PASS — §3.2, §13.3 — do NOT use PBS values, only near-universal
  node membership, so they are graph-topology results. The gnomAD replication proves
  this: swap the entire SA reference and the numbers barely move because the PBS was
  never load-bearing.
- Net: the population-differential PBS signal — Law 2's candidate object — is
  currently either not load-bearing where the gates pass, or not surviving where it
  is tested. This is not a contradiction of a prior claim; it is empirical
  confirmation of the LRRK2 RESULT's own caveat #4, now demonstrated by an
  independent-cohort swap.

## What replicated is still real (do not over-deflate)
- The §3.2 pleiotropy enrichment is a robust, cohort-independent fact: community-
  bridging genes in STRING∪GTEx are markedly more pleiotropic than degree+PBS-matched
  genes (and survives study-bias control). That is a genuine result about the
  coupling graph — it just is not evidence about the SAS population signal.
- The LRRK2 bridge is recovered function-blind — but topologically (from STRING∪GTEx
  structure), not from SAS population differentiation.

## The constructive implication (for later, not done here)
To make the population thesis load-bearing, the gates must CONSUME the PBS values,
not just gene-has-a-variant membership: e.g. a PBS threshold that makes the
candidate set genuinely restrictive (bounding d as §7 intends, rather than admitting
~all genes), or PBS-weighted participation, or a bridge test conditioned on PBS.
As implemented, the pile is computed but its values scarcely enter the passing
gates. This is the honest next design question, surfaced by the replication.

## Outputs (side-by-side, TAG=_gnomad — Pan-UKBB results untouched)
`eir_pbs_pile_gnomad.tsv.gz`, `lrrk2_gate_gnomad.json`,
`bridge_discovery_gnomad.json`, `bridge_scores_full_gnomad.tsv.gz`,
`annotation_recovery_gnomad.json`.

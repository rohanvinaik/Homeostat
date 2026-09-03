# Run record — §III selection-weighted κ: NEGATIVE (soft PBS-weighting demotes the bridges)

**Verdict: NEGATIVE, and it is the third independent confirmation of the same
limit. Feeding PBS in softly as the κ teleportation prior (§10.3) does NOT lift the
population-structured bridges — it slightly DEMOTES them, consistently in both
cohorts, and the effect is graph-dominated and non-replicating. Recorded honestly,
not tuned (there is no K to tune; damping is the standard 0.85).**

## Results (both cohorts)
| quantity | Pan-UKBB | gnomAD |
|---|---|---|
| control mean rank, κ_unweighted | 3421 | 3416 |
| control mean rank, **κ_PBS** | **3550** | **3949** |
| lift vs unweighted (>0 = better) | **−129** | **−533** |
| control mean rank, raw PBS alone | 5318 | 9286 |
| lift vs raw-PBS (>0 = better) | +1768 | +5338 |
| top-628 κ_PBS pleiotropy p | 0.057 | 0.013 |
| top-κ_PBS Jaccard across cohorts | — | **0.923** |

## Reading against the four preregistered tests
1. **Does κ_PBS lift the bridges vs κ_unweighted?** NO — it demotes them (−129,
   −533), consistently in both cohorts. The preregistered positive control FAILS.
2. **Beats raw PBS alone?** YES (+1768, +5338). But this only says the graph does
   the ranking (κ_unweighted puts the controls at ~3400/14,886, ~77th pct — the
   sigsearch "mid-pack" finding); layering PBS on top nudges them slightly DOWN.
3. **Top-N pleiotropy, replicated?** NO — p=0.057 (fail) vs 0.013 (pass); does not
   replicate, and observed (22) is well below the all-genes §3.2 (34.7).
4. **Load-bearing + replicating?** NO on both counts: top-κ_PBS Jaccard 0.923 means
   the PBS prior barely moves the graph-dominated ranking (only weakly load-bearing),
   and the control-lift is negative (does not replicate a benefit).

So soft weighting avoids the hard-restriction failure (it does not break the gates)
but at the cost of the population signal being nearly inert again (0.92 overlap) —
and where it does act, it hurts the controls. There is no regime in between where
PBS is load-bearing AND helps.

## The full session synthesis — four probes, one conclusion
| probe | how PBS enters | outcome |
|---|---|---|
| §8.4 selection-enrichment | ranks by PBS *values* | FAILED under LD correction |
| §3.2 + LRRK2, all-genes | node membership only (PBS inert) | passed, but purely topological |
| §3.2 + LRRK2, hard PBS-restricted | node-set restriction (load-bearing) | gates BREAK (0/8, enrichment inverts) |
| **§III soft PBS-weighted κ** | teleportation prior (soft) | bridges DEMOTED, graph-dominated, non-replicating |

**Across four independent, preregistered operationalizations — value-ranked,
membership, hard-restricted, soft-weighted — there is no configuration in which the
population-differential PBS signal does coherent mechanism-recovery work on the
static gene-coupling substrate.** When PBS is inert the analysis passes
(topologically); when PBS is made to act, it either breaks the analysis or hurts it.

## What this establishes (the honest, and publishable, conclusion)
This is NOT a refutation of the thesis. It is a rigorous, multi-cohort, preregistered
demonstration of exactly what §12.4 and §15's NAMED RISK predicted: **on static
allele-frequency data, the population-differential object and the coupling-graph
mechanism-recovery do not couple. The binding constraint is DATA (missing dynamics),
not method.** The program said this in advance ("the method may be sound while data
quality, not method, remains the limiting factor"); this session turned that
assertion into an empirical result by trying, and exhausting, every way to make the
static-data operationalization cohere.

The real next advance is not another metric on static frequencies — it is the
§12.4 substrate: longitudinal / state-resolved (flare-to-remission) multi-omic data,
which is the affiliation-gated path (the physician co-author or the Dalli/Queen Mary
collaboration, `docs/DATA_ACCESS_LANDSCAPE.md`). What the static program CAN honestly
deliver stands: a method + hypothesis-generation contribution (§12.7), with the
§3.2 pleiotropy enrichment as a real fact about the coupling graph and the 628
candidate bridges as leads — bounded, always, by §12.4.

## Outputs
`sig_descent.json`, `sig_descent_gnomad.json`, `sig_descent_comparison.json`.

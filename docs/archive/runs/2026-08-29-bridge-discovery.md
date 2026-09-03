# Run record — annotation-blind bridge discovery (§3.3), 2026-08-29

**The program's actual output: 628 candidate bridges, function-blind. The
positive control lands correctly (LRRK2 top ~2%). These are HYPOTHESES (§12.7),
NOT validated mechanism — and interpreting the gene names by eye is the forbidden
move (§12.6/§12.3). The real validation is a preregistered §3.2 enrichment test,
below, NOT this list.**

## Method
The exact LRRK2-gate metric applied genome-wide: over the function-blind coupling
graph (STRING physical ∪ 2-hop GTEx co-expression, 14,886 nodes, PBS-weighted),
label-propagation communities → participation coefficient → degree-matched
significance per gene (fraction of ±20%-degree genes with participation ≥ its
own). Genes with degree ≥ 2 scored (13,800).

## Internal-consistency check (the load-bearing part)
- **LRRK2 rank 300 / 13,800 (top 2.2%), p = 0.024** — the genome-wide discovery
  surfaces the known bridge, at the same significance as its gate. The positive
  control is not a one-off; it holds in the full ranking.
- **NOD2 and RIPK2: participation 0, p = 1.0** — they do NOT span communities.
  This is §5.8 exactly: LRRK2 is THE bridge (joins immunity to elsewhere); NOD2/
  RIPK2 are WITHIN the immunity cluster. The anchors behave as the theory
  predicts, which is a real check that the metric is measuring the right thing.
- 628 of 13,800 genes reach p < 0.05.

## Top candidates (annotation-blind; HYPOTHESES, listed as data, not interpreted)
NPVF, PTGDS, POMK, MTCH2, AK9, A1CF, CERS6, ATP6V0A2, F5, APOBEC3A, PLG, APP,
APOBEC3H, ABCG8, ECSIT, HDLBP, ATP5F1B, CERS2, MRPL2, MTUS2, ... (full list +
scores in `bridge_discovery.json`).

## The discipline (why I am NOT interpreting the names)
Several top candidates are recognizable clearance / lipid-mediator / mitochondrial
/ amyloid genes, which is *thesis-shaped*. **That recognition is exactly the trap
(§12.6 classification-first reading, §12.3 self-licking confirmation, Appendix C):
a fluent post-hoc story that a familiar gene "fits" carries zero information and
feels like rigor.** Cherry-picking APP-is-amyloid from a top-20 is not the §3.2
falsifier; it is the failure mode the program is a critique of, performed on the
program's own output.

## The real validation (§3.2 / §10.2 — NEXT, preregistered)
The falsifier is **recovery of known annotation WITHOUT having used it**, tested
SYSTEMATICALLY: are the top-N candidate bridges enriched for known pleiotropic /
multi-disease / clearance-and-resolution genes relative to a MATCHED background
(degree- and PBS-matched), with the annotation set and the enrichment statistic
PREREGISTERED before the test runs (§10.2 contamination mitigation: declare which
annotations count as independently recovered vs plausibly upstream of the graph).
Only that number validates the pile; this list does not.

## Bounds
Still §12.4: no dynamics, so even a passing §3.2 test yields candidate mechanisms
(high prior density in an under-searched region, §12.7), never established
mechanism. And the LD/community-method caveats of the two gate records carry.

## Output
`data/e_i_r/bridge_discovery.json` — 628 candidates, full scores, control ranks.

# Run record — LRRK2 gate on the correct pipeline: FAIL (2026-08-29)

**Verdict under the preregistered criterion (7f80c91): FAIL. But the FAIL is
confounded by a bug in my own bridge-node metric, so it is not yet a clean test
of the pipeline. Owned below, with the correct next step.**

## What ran
PBS pile → gene weights (max PBS within ±25kb; anchors covered at LOW PBS —
LRRK2 0.090, NOD2 0.085, RIPK2 0.058, vs pile top ~0.49, exactly §5.8) →
function-blind coupling graph = STRING physical among 14,886 pile-weighted
candidate genes → bridge evaluation (control names only in the evaluator, §5.9).

## Result
| clause | value |
|---|---|
| NOD2–RIPK2 adjacent (structure-only) | **TRUE** — recovered |
| LRRK2 adjacent to NOD2/RIPK2 in STRING physical ≥400 | FALSE |
| LRRK2 components_joined | 1 |
| verdict | **FAIL** |

## Three findings, ranked by what they mean

1. **My clause-B metric is ILL-POSED (my bug, not a data fact).** "Distinct
   components among LRRK2's neighbors" is trivially 1 for any existing node: the
   node itself merges its neighbors into one weak component, so the clause can
   never fire. The is_bridge concept (kappa.py) tests whether ADDING an edge
   joins components; a bridge-NODE needs a cut-vertex / participation test
   instead. I applied the wrong operator in the preregistered criterion. Pinned
   as a test (`test_clause_a_couples_but_component_metric_is_illposed`).

2. **The induced STRING-physical graph is one giant component** (the recurring
   §13.4/Phase-2 substrate finding). So ANY component-joining bridge test is
   vacuous on it regardless of metric — the bridge, if present, is a WITHIN-graph
   community-spanning position, not a between-component connector.

3. **What IS recovered, function-blind: the NOD2–RIPK2 physical edge.** But
   LRRK2 is not directly STRING-physical-adjacent to NOD2/RIPK2 at score ≥400 —
   consistent with §9's biology (LRRK2 acts by *enhancing RIP2 phosphorylation*,
   a functional/kinase interaction that STRING physical need not carry as a
   high-confidence binding edge). So the LRRK2 bridge, if recoverable at all from
   PPI structure, is mediated, not a direct edge.

## The correct metric (design-mandated, not invented)
The bridge-node measure is **community participation** (carving.py:
cnm_communities → participation coefficient), degree-matched — the exact §13.4
machinery, and the §5.8 definition (a gene whose edges span two mechanism
communities). Articulation-point (does removing LRRK2 split its neighborhood) is
the discrete twin. Either is well-posed on a connected graph; component-joining
is not.

## Discipline note
The preregistered criterion's clause B is withdrawn as ILL-POSED (provably
vacuous), not as inconvenient — the same class of correction as the §13.4 broken
null. A re-run requires a FRESH preregistration with the participation metric,
and (per the deferral) the GTEx co-expression channel, before it counts. No
novel output stands until then (Law 3). Also honest: the co-expression second
channel was deferred this run for tractability (14,886-gene all-pairs
correlation, no numpy under the stdlib-only design) — a sparser graph is a
stricter test, but it also may under-resolve the communities the participation
metric needs.

## Output
`data/e_i_r/lrrk2_gate.json` — full evaluation.

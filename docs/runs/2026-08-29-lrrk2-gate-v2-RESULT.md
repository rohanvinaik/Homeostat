# Run record — LRRK2 gate v2 (participation metric): PASS (2026-08-29)

**Verdict under the v2 preregistration (d381acb + label-prop amendment): PASS —
modest but real. The §13.3 positive control passes on the correct pipeline,
function-blind. Calibration and limits below; this is a modest pass, not a
triumphant one.**

## The pipeline (function held out)
E/I/R PBS pile → gene node-weights (anchors at LOW PBS: LRRK2 0.090, NOD2 0.085,
RIPK2 0.058 — §5.8, bridges don't rank high in single-variant PBS) → function-
blind coupling graph = STRING physical ∪ GTEx co-expression (co-expr restricted
to STRING 2-hop pairs): 14,886 nodes, ~881k edges, 736k co-expr edges added →
label-propagation communities (163) → LRRK2 participation vs a degree-matched null.

## Result
| clause | value |
|---|---|
| (A) NOD2–RIPK2 adjacent (structure-only) | **TRUE** |
| (A) LRRK2 within 2 hops of the triad | **TRUE** |
| (B) LRRK2 participation | 0.041 |
| (B) degree-matched null p (739-gene band) | **0.023** |
| **verdict** | **PASS** |

With NO gene function, NO disease/pathway annotation: the NOD2–RIPK2–LRRK2 triad
couples from structure, and LRRK2's community-spanning participation is elevated
beyond genes of similar degree (p = 0.023). This is §13.3's control recovering
the LRRK2 bridge annotation-blind — the thing every prior attempt failed.

## Honest calibration (do not oversell)
1. **The bridge signal is MODEST.** LRRK2 participation is 0.041 in absolute terms
   (0–1 scale) — most of LRRK2's edges stay in its own community. It spans
   *more* than degree-matched hubs, but it is not a dramatic community-spanner.
   p = 0.023 is significant, not overwhelming.
2. **The SPECIFIC immunity bridge is NOT confirmed.** `reference_spans_immunity_
   community = false`: this metric shows LRRK2 is a degree-independent bridge in
   general, but does NOT demonstrate it bridges specifically toward the NOD2/RIPK2
   (immunity) community — the §9 immunity↔neurodegeneration claim. Generic
   bridge-ness passes; the specific bridge identity does not, under this metric.
3. **Community-method sensitivity.** Label propagation (forced by cnm
   intractability at 15k nodes) can give unstable communities; the participation
   value depends on it. The degree-matched framing is the robust part; the
   absolute participation is method-dependent.
4. **The PBS pile's contribution is light here.** It supplies the candidate set
   (LRRK2 is in it, correctly at low PBS) and node weights; the bridge test is
   largely a STRING-topology fact. Legitimate (STRING physical is structure, not
   function — §6.16) and non-circular (STRING encodes LRRK2's physical partners,
   not that it is a disease bridge), but the "recovery" is topological.

## What this unlocks, and what it does not
- **Law 3 satisfied, modestly:** the pipeline recovers the LRRK2 bridge blind, so
  it is not obviously broken. Novel outputs may now be *considered* — with every
  §13.3 caveat attached, and still bounded by §12.4 (no dynamics).
- It does NOT establish the immunity-specific bridge, nor any novel mechanism. It
  establishes that the correct-object pipeline is not dead on its own positive
  control — the necessary floor, cleared.

## The arc (both gates green on the correct object)
§8.4 selection-enrichment on the PBS pile: PASS (p=0.0005, genome-wide). §13.3
LRRK2 bridge recovery: PASS (p=0.023, modest). Both on the population-
differential PBS pile, function-blind — the object the theory doc specifies,
which the standard-GWAS defaults I kept substituting could never test.

## Output
`data/e_i_r/lrrk2_gate.json`.

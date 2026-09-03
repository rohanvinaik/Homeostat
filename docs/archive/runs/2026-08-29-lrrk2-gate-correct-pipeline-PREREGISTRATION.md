# PREREGISTRATION — LRRK2 gate on the correct pipeline (§9 / §13.3, Law 3)

**Committed before the harness runs.** Supersedes the 2026-08-28 LRRK2
preregistration, which sat on the n=1 array pile (deprioritized the anchors) and
FAILED. This one sits on the cohort E/I/R PBS pile — the correct candidate object.

## The recovery the control demands (§9)
LRRK2 is a **bridge** (§5.8): a pleiotropic gene joining the mycobacterial-
immunity/IBD cluster to a separate cluster, its effect visible only in
composition (LRRK2×NOD2 epistasis). Therefore — and this is the load-bearing
point — **LRRK2 will NOT rank high in single-variant PBS** (§5.8: bridges never
clear single-variant significance). Recovery is a graph-structural property of
the κ-coupling layer, NOT a rank in the pile. A gate that requires LRRK2 to be
top-of-pile is testing the wrong thing.

## What the derivation may consume (annotation-blind = FUNCTION held out)
1. The E/I/R PBS pile (`eir_pbs_pile.tsv.gz`) — positions and PBS only.
2. Positional gene envelopes (refGene): symbol → (chrom, span). **Positions are
   structure, not function.** Gene symbols are opaque identifiers to the derivation.
3. STRING **physical** edges (score ≥ 400) — physical PPI, structure-derived.
4. GTEx co-expression edges (cross-tissue r ≥ 0.7) — a second structure channel.
No gene function, pathway, or disease annotation enters the derivation.

## Derivation (fixed now)
- Node weight w(gene) = max PBS over the gene's pile variants within ±25 kb (the
  §10.3 selection prior; the pile's role is to weight nodes, NOT to gate them —
  a bridge must be reachable even at low PBS).
- Coupling graph G = STRING physical ∪ GTEx co-expression, over all genes.
- κ / bridge structure via `kappa.py`: weak components; `is_bridge`;
  connector genes joining ≥2 components; PageRank κ.

## PASS criterion (fixed now; function-blind)
PASSES iff, with no parameter change after this commit and no function input:
- **(A) The triad couples.** LRRK2, NOD2, RIPK2 are all in G, and NOD2–RIPK2 are
  adjacent (the canonical signaling edge) with LRRK2 adjacent to at least one of
  them — recovered from structure alone.
- **(B) LRRK2 bridges, beyond hub status.** LRRK2 joins ≥2 weak components of the
  PBS-node-weighted candidate subgraph (`is_bridge` / connector), AND its
  connector/κ signal exceeds a **degree-matched** null (§13.4 lesson: do not
  credit it merely for being high-degree), one-sided p < 0.05.

FAILS if the triad does not couple, or LRRK2 shows no degree-independent bridge
structure. NOT-EVALUABLE only if the pile does not cover the anchor loci at all
(a data fact, stated, never spun into a pass).

## NOT the pass criterion (reference only)
- The raw PBS rank / κ rank of the three genes — reported, never pass-bearing.
- The LLM/literature "knows" LRRK2; this gate uses no LLM and no function, so the
  §6.4 contamination does not apply here — the derivation is structure-only.

## Discipline
Control gene names (LRRK2/NOD2/RIPK2) appear ONLY in the evaluation function,
never in the derivation path (§5.9). No dial is tuned after this commit to
convert a fail into a pass.

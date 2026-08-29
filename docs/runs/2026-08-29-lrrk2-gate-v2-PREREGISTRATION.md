# PREREGISTRATION v2 — LRRK2 gate, participation metric (§9/§13.3, Law 3)

**Committed before the harness change.** Supersedes v1 (7f80c91), whose clause B
("distinct components among LRRK2's neighbours") was withdrawn as ILL-POSED —
an existing node's neighbours are one weak component by construction, so it can
never fire. The correct bridge-node measure is community participation (§5.8: a
gene whose edges span two mechanism communities), degree-matched (§13.4).

## What the derivation may consume (function held out)
1. E/I/R PBS pile — positions + PBS only (node weight = max PBS within ±25kb;
   NOT a gate — a bridge is reachable at low PBS, §5.8).
2. refGene positional envelopes (positions are structure).
3. STRING physical edges (score ≥ 400).
4. GTEx co-expression edges (cross-tissue r ≥ 0.7), added **only between candidate
   gene pairs within 2 STRING-physical hops** — a structure-defined, anchor- and
   PBS-agnostic restriction that is tractable without numpy. Function-blind.
No gene function / pathway / disease annotation enters the derivation.

## Derivation (fixed now)
- Coupling graph G = STRING physical ∪ (GTEx co-expression restricted to STRING
  2-hop pairs), over the pile-weighted candidate genes.
- Communities via greedy modularity (`carving.cnm_communities`, γ = 1.0).
- LRRK2 participation coefficient P = fraction of its edges leaving its own
  community (`carving.participation`).

## PASS criterion (fixed now; function-blind)
PASSES iff, with no parameter change after this commit and no function input:
- **(A) The triad couples, structure-only.** NOD2–RIPK2 adjacent in G, AND LRRK2
  within **2 hops** of NOD2 or RIPK2 in G (2 hops fixed now, to admit the
  *mediated* LRRK2→RIP2-phosphorylation interaction §9 describes — LRRK2 need not
  directly bind NOD2/RIPK2).
- **(B) LRRK2 bridges, beyond hub status.** LRRK2's participation coefficient
  exceeds a **degree-matched** null (genes with G-degree within ±20% of LRRK2's;
  §13.4 confound control), one-sided permutation p < 0.05.

FAILS if either does not hold. NOT-EVALUABLE only if the pile does not cover the
anchor loci (it does — verified structurally at v1).

## Reference only (NOT pass-bearing)
- Whether LRRK2's community differs from NOD2/RIPK2's and its participation spans
  toward theirs (the specific §5.8 immunity↔X bridge) — reported, not gated.
- Raw PBS weights / κ ranks of the three genes.

## Discipline
- Control names appear ONLY in the evaluator (§5.9). No dial tuned after this
  commit to convert a fail into a pass.
- The 2-hop co-expression restriction is a stated tractability bound, not tuned;
  its direction (adds edges only where STRING already couples) is recorded.
- The participation + degree-matched machinery is the §13.4 method, which there
  overturned a naive positive result — so it is a genuine test, not a rigged one.

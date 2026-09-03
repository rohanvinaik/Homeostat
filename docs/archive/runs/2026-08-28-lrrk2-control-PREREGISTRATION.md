# PREREGISTRATION — §13.3 LRRK2 positive control (written BEFORE the harness ran)

**Committed before any recovery code executed.** This file fixes the success
criterion so it cannot drift toward whatever the harness happens to find.
Checkpoint §13.3: "Run the full pipeline blind and check whether the
LRRK2–NOD2–RIPK2 bridge is recovered without annotation input. If it is not,
the method is not working."

## What the derivation may consume (the blind side)

1. The §13.1 E/I/R queue — positions and priorities only.
2. STRING v12 **physical** protein links (experimental/physical channel file;
   the text-mining-bearing combined file is NOT used — checkpoint §6.16:
   structure-derived carvings only, and text-mining is the annotation channel
   in disguise).
3. Positional gene envelopes from refGene (hg19): symbol → (chrom, min start,
   max end). Positions are structure, not function. Gene symbols are opaque
   identifiers to the derivation; no function, pathway, or disease input.

## Derivation (fixed before running)

1. Map every E/I/R locus (the 3,877 collapsed loci, priority > 0) to genes
   whose envelope ±25kb contains the lead position. Gene score = max lead
   priority over its loci. (Dial: flank_bp = 25_000.)
2. Candidate gene set G = genes with score > 0.
3. Build the graph on G: STRING physical edges with combined_score ≥ 400
   (STRING "medium confidence"; dial fixed here, not tuned after).
4. Bridge structure = connected components of the induced subgraph, plus, for
   every pair of components joined when ONE additional gene outside G (a
   "connector", any STRING gene) is admitted, record that connector ranked by
   how many components it joins and the summed scores it connects. This is the
   §5.7 bridge shape: a node joining otherwise-disjoint clusters.

## Success criterion (fixed now)

The control **PASSES** iff, with no parameter changes after this commit:

- **(a)** LRRK2, NOD2, and RIPK2 all receive a positional E/I/R mapping (are in
  G) — i.e., the array + queue even covers them — AND LRRK2 and NOD2 lie in
  the same connected component of the induced physical subgraph, with RIPK2 on
  a path between them or one of the two adjacent to the other; **or**
- **(b)** at least one of {LRRK2, NOD2} is in G and the OTHER (or RIPK2) is
  recovered as a top-20 connector (the bridge recovered as a bridge).

The control **FAILS** if neither holds. Partial outcomes (e.g., genes absent
from G because the array does not cover them) are reported as **NOT-EVALUABLE
for that clause**, with the coverage fact stated — a consumer array's SNP
content is itself European-calibrated (checkpoint §11.5), and absence-of-
coverage is a data fact, not a method failure; but it may NOT be spun into a
pass.

## Interpretation commitments

- PASS does not validate any novel finding; it licenses continuing (Law 8).
- FAIL means the method, at current data scale (n=1 prior + physical topology,
  no cohort, no expression), cannot see the known bridge — reported as such,
  with the §12.4 dynamics constraint as the standing explanation to test, and
  NO dial iteration to convert the fail into a pass.
- The evaluation names (LRRK2/NOD2/RIPK2, their identifiers) appear ONLY in
  the evaluation function, marked in code, never in the derivation path
  (§5.9: the confirmation channel must not feed the derivation).

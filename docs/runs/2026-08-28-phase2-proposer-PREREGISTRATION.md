# PREREGISTRATION — Phase-2 LLM proposer + selection-weighted κ (written BEFORE the run)

**Committed before the proposer fleet ran or the verifier scored anything.**
Fixes the criterion so it cannot drift toward whatever the flood produces.

## The pipeline being tested
1. **Proposer (LLM brute force, frozen artifact).** A fleet of independent
   subagents floods candidate genes that mechanistically COUPLE two abstractly-
   described regulatory processes (intracellular-pathogen / mycobacterial immune
   regulation ↔ intestinal barrier / inflammation-resolution regulation),
   proposing from model prior only (no web search), each blind to the others.
   Output frozen to `data/network/proposals.jsonl` (gene, angle, rationale,
   provenance). The GWAS gene lists and the answer are NOT given to the proposer.
2. **Firewall + grounding (§5.9/§6.4).** A proposed gene is admitted only if it
   has independent structural support to the GWAS inflammation module — a STRING
   physical edge OR a GTEx co-expression edge (τ=0.70) to a universe gene. The
   LLM's ungrounded proposals are DROPPED. Structure the LLM never saw does the
   filtering.
3. **Score = selection-weighted κ.** For each grounded proposal:
   score = κ(gene) × (1 + iHS_percentile), where κ is the PageRank hub-score in
   the module+proposal graph and iHS is the mean PopHuman SAS iHS at the gene's
   envelope (§10.3: selection as prior). Rank; stop at κ→0.

## PASS criterion (fixed now; method-level, contamination-robust)
The build PASSES iff BOTH, with no parameter change after this commit:

- **(A) The firewall demonstrably filters.** The grounding rate is strictly
  below 100% AND meaningfully below a matched random-gene grounding rate — i.e.
  structure REJECTS a real fraction of the LLM's proposals, proving the ranking
  is driven by structure, not by the LLM. (If every proposal grounds, structure
  is not filtering and the firewall is vacuous.)
- **(B) Selection-lift beyond the null, degree-matched.** The grounded proposals'
  mean iHS is higher than a DEGREE-MATCHED control set drawn from the STRING
  graph (same per-decile degree profile — the §13.4 confound control), at a
  one-sided permutation p < 0.05. This is the test that the pipeline surfaces
  population-differential bridges above generic connectivity — the thing the
  Build-1 null (generic hubs) could not do.

The build FAILS if either does not hold. A FAIL means LLM-proposal +
structure-grounding + selection-weighting, at this data scale, does not beat the
generic-hub null — reported as such, no dial iteration to convert it.

## NOT the pass criterion (reference only)
- LRRK2/NOD2/RIPK2 recovery is reported as a **labelled reference with the
  contamination caveat** (PHASE2_SIGNIFICANCE_SEARCH.md): the LLM knows these
  from the held-out literature, so their appearance proves little. Where they
  rank under selection-weighted κ is informative, never pass-bearing.

## Honesty notes
- The proposer is non-deterministic; the frozen artifact makes the VERIFICATION
  reproducible. This run's result is reported as one run (wet-lab discipline).
- Degree-matching may be conservative (real bridges are hubs) — as in §13.4, the
  defensible claim is about whether the pipeline beats the generic-hub baseline,
  not a biology verdict.

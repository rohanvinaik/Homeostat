# Decision: Phase 2 — the significance-search layer (drop n=1 prior, LLM-propose/κ-verify)

**Date:** 2026-08-28
**Status:** accepted
**Context:** §13's three results established that a per-variant, per-individual
prior cannot express composition-only bridges. Founder direction: drop the n=1
E/I/R prior as the selector, expand the significance search via an LLM-driven
semantic brute force grounded in SIGNIFICANCE_WEIGHTING's κ machinery.

## Decision (forks confirmed with founder via the AGENTS.md gate)
1. **The n=1 E/I/R prior is retired as the sole candidate selector** (not
   deleted — still valid for cohort-scale ANI/ASI regression, §7.4).
2. **Architecture = LLM proposer + deterministic κ-over-structure verifier,
   behind the §6.4 firewall.** LLM floods bridge-chain candidates; κ (over
   structure the LLM never touched) verifies. §6.4/§5.9: LLM-as-oracle collapses
   to consensus and makes L_ind undefined — so the LLM is proposer only.
3. **LLM floods bridge chains between clusters.**
4. **Verifier substrate = STRING physical + GTEx co-expression + iHS selection.**
5. **κ transported via its PageRank/hub-score form** (SIGNIFICANCE_WEIGHTING §5),
   not the reachable-set form, which degenerates on an undirected gene graph.
   `is_bridge` transports verbatim. Built on Regenesis `significance.py`
   definitions (mirrored in `kappa.py`), not reinvented.

## Build 1 result (this decision's first evidence)
Deterministic verifier baseline (`sigsearch.py`): the GWAS universe is ONE
inflammation module under STRING+co-expression; raw κ surfaces generic hubs
(RELA/STAT3); controls sit mid-pack. This is the null. See
`docs/runs/2026-08-28-phase2-verifier-baseline.md`.

## Consequences
- Full design: `docs/PHASE2_SIGNIFICANCE_SEARCH.md` (incl. the load-bearing
  LLM-proposal-contamination caveat — LRRK2-via-LLM is a weaker control than
  §13.3's annotation-blind one; the contribution is the filter + asymmetry,
  never the LLM's judgement).
- Next build: LLM proposer (out-of-universe bridge candidates, frozen artifact,
  provenance) + selection-weighted κ; preregister the positive-control criterion
  first. The bar is beating the Build-1 null.
- This is still classical AI: the LLM is a bounded proposer at the tail (Law 2
  escape hatch, §6.2 "cheap mechanical ideation"); the architecture is the
  deterministic κ-over-structure verifier.

> **⛔ SUPERSEDED (2026-08-31) — historical only.** This describes a pre-Regenesis LLM-proposer +
> κ-over-STRING/GTEx architecture. It was replaced by the confirmed role-recognition stack: the mechanism
> is grown from CONVERGENCE across computed data lenses and recognized by **Regenesis** (roles, not gene
> tokens), with NO LLM proposer and NO κ over a generic network. Current design: `docs/ETIOLOGY_ENGINE.md`.
> Kept for provenance; do NOT build from this.

# Phase 2 — the significance-search layer (Part III intelligence layer, build 1)

**Status:** design confirmed with the founder 2026-08-28 (the AGENTS.md gate:
mechanism restated, forks confirmed before architecture). This is the first
build of the THEORY_OF_THE_CASE Part III intelligence layer, which §13's three
results (13.2 null, 13.3 FAIL, 13.4 degree-confound) established as
demonstrated-necessary: a per-variant, per-individual prior cannot express
composition-only bridges.

## What changed

**The n=1 E/I/R prior is dropped as the candidate selector.** It was the
weakest link — European-calibrated array content (§11.5), single-variant,
per-individual — and §13.3/§13.4 proved it cannot carry bridge recovery. In its
place, the checkpoint's own §6.2 substitution: **cheap mechanical ideation
floods the μ-space**, exploiting the generate/verify asymmetry (constructing a
good oracle is hard; checking whether a candidate yields coherent κ-structure is
mechanical).

The E/I/R machinery is NOT deleted — it remains a valid population-differential
prior for the day cohort data exists (§7.4 regression over the ANI/ASI cline).
It is retired only as *the sole n=1 candidate gate*.

## The mechanism (confirmed data-flow)

```
  PROPOSER  ──floods──▶  candidate bridge chains  ──frozen artifact──▶  VERIFIER
  (LLM, cheap                (directed mechanistic                     (deterministic
   semantic                   links between the                        κ over external
   brute force)               disconnected clusters)                   structure)
                                                                             │
                                              ┌──────────────────────────────┘
                                              ▼
                              GROUNDING (the firewall): admit a proposed edge
                              ONLY if independent structure supports it —
                              STRING physical edge OR GTEx co-expression ≥ τ.
                              Selection (iHS) weights κ (§10.3). Ungrounded
                              LLM proposals are dropped: the LLM's fabrications
                              never enter the graph κ is read from.
                                              │
                                              ▼
                              κ = marginal coverage = hub-score = PageRank over
                              the grounded mechanism graph. Bridges = grounded
                              edges that join previously-disconnected clusters
                              (is_bridge / coverage_delta > 0 for others).
                              Rank by chain_significance × κ; carry the bracket;
                              STOP at κ → 0.
```

### Confirmed forks (founder, 2026-08-28)
1. **LLM = proposer only, behind the §6.4 firewall.** Significance (κ) is
   computed over structure the LLM never touched. Rationale is load-bearing,
   not hygiene: §6.4 — an LLM is trained on the literature that produced the
   existing partitions, so LLM-generated *oracles* collapse toward consensus and
   variance understates uncertainty; §5.9 — if the generator also confirms,
   L_ind → 1 vacuously and the central quantity is undefined. The generate/verify
   asymmetry is the whole point: the LLM floods, structure verifies.
2. **The LLM floods bridge chains between clusters** — candidate directed
   mechanistic links joining the disconnected GWAS clusters (immunity ↔ IBD),
   the §13 bridge object directly.
3. **Verifier substrate = STRING physical + GTEx co-expression + iHS selection.**
   Three independent structural channels; a proposed edge is grounded if the
   physical or co-expression channel supports it, and κ is selection-weighted.

## The load-bearing caveat — LLM-proposal contamination (record it, don't paper over it)

The firewall protects the SCORING channel, not the PROPOSAL channel. The LLM
"knows" LRRK2 is an immunity/PD gene from the same literature the program holds
out. So:
- **LRRK2 recovered via LLM proposal is a WEAKER control than §13.3's** (which
  was annotation-blind on the proposal side too). The LLM proposing LRRK2 proves
  little; what proves something is whether *independent structure* confirms the
  LLM's proposals are bridges, measured across MANY proposals where the LLM
  cannot just recite famous answers.
- **The real test is discrimination, not recall of the famous case:** does the
  grounded-κ verifier separate the LLM's real bridges from its plausible-but-
  ungrounded fabrications, and does the known bridge fall out with high κ *among*
  novel ones? A preregistered criterion (like §13.3's) governs the re-run of the
  positive control under this architecture, written before that run.
- The honest framing for the paper: the LLM is a hypothesis *firehose* whose
  precision is low and whose value is realized only through the deterministic
  structural filter. The contribution is the filter + the asymmetry, never the
  LLM's judgement.

## Substrate sourcing
- **STRING physical** — `string_physical_links.txt.gz` (have; §13.3/13.4).
- **iHS selection** — PopHuman bigwigs (have; §13.2).
- **GTEx co-expression** — computed from the v8 gene-median-TPM matrix
  (`gtex_median_tpm.gct.gz`, ~7MB): each gene → cross-tissue median-TPM vector;
  co-expression edge = correlation ≥ τ over tissues. Independent of PPI physical
  topology by construction (expression, not binding).

## Build sequence
1. **Verifier spine (this build):** the κ math (coverage, marginal_coverage,
   is_bridge, coverage_delta, greedy, chain_significance) mirroring Regenesis
   `significance.py` definitions, over a directed grounded mechanism graph;
   grounding over STRING physical + GTEx co-expression; iHS as κ weight. Pure,
   tested. Validated end-to-end on a DETERMINISTIC baseline candidate set (all
   cross-cluster gene pairs) with LRRK2 as a labeled reference — this is the null
   against which the LLM proposer's added value is later measured.
2. **LLM proposer (next):** subagent flood of candidate bridge chains, frozen to
   a versioned proposal artifact with provenance; the verifier scores it; compare
   to the deterministic baseline. Preregister the positive-control criterion
   first.
3. **Selection-weighting + bracket + κ→0 stopping**, then the cohort-scale
   I_ind read when data exists (§5.10 / §11.2).

## Why this is still classical AI, not "adding ML"
The LLM is a bounded proposer at the tail — Law 2's escape hatch, the founder's
explicit call, exactly the checkpoint's §6.2 "cheap mechanical ideation." The
architecture is the deterministic κ-over-structure verifier and the generate/
verify asymmetry; the LLM supplies proposals the same way a funded lab's PI
would, and its output is firewalled out of every load-bearing computation.

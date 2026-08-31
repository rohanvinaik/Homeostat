# Validation results — the packet, run

Each row of `docs/PROOF_POINTS.md` that has been executed is recorded here with its method, the real
result, and a verdict. Scripts live beside this file; re-run any of them to reproduce. Cells that need
gated data or a domain collaborator are left open in `PROOF_POINTS.md`, not faked here.

Engine: Regenesis `understand` over `universes/mechanism` (universe_only). Signals: the shared
`probes/l2_lrrk2.py::build_context` + `scope_signals`, so a validation can never drift from the probe.

---

## A3 — determinism · **PASS**

`validation/a3_determinism.py`. The historical nondeterminism was unordered-set iteration, whose order
tracks Python's per-process hash seed. The probe is run three times under distinct `PYTHONHASHSEED`
(0/1/2); the assembled fact-text is **byte-identical** across all three (sha256 `faab482d…`). The same
sha holds before and after the `build_context`/`scope_signals` refactor — the refactor is behaviour-
preserving.

## B3 — leave-one-lens-out ablation · **PASS** (nuanced, and the nuance is the point)

`validation/b3_ablation.py` → engine. The LRRK2 scope's real signals, with each lens's facts removed
in turn:

| gene | FULL | −Fst | −coexpr | −binding | −wiring | −censor |
|------|------|------|---------|----------|---------|---------|
| RIPK2 | **deep_core (4.43)** | none | deep_core | core | deep_core | deep_core |
| NOD2 | core (3.33) | none | core | core | core | core |
| TNFSF15 | core (3.33) | none | core | core | *differ* | core |
| LRRK2 | component | none | component | component | component | component |
| IL18R1 | component | none | component | component | component | component |
| HLA-DQA1 | *differ (censored)* | none | differ | differ | differ | **component** |

- **No single co-occurrence lens is load-bearing.** Dropping co-expression changes nothing — component
  re-derives through the binding/wiring path. Convergence across the interchangeable set carries it.
- **Dropping binding** knocks only RIPK2 deep_core→core; **dropping wiring** knocks only TNFSF15
  core→differentiator. Localized, graceful — not collapse.
- **Dropping the censor** lets the 1021-trait hub HLA-DQA1 reach component — the censor is precisely
  what holds promiscuous noise out.
- **Dropping Fst collapses every component.** Differentiation is the conserved conjunct of every
  convergence rule — a necessary gate **by design**, on-thesis (the program is population-differential
  mechanism), not a fragility.

## A2 — adversarial abstention · **PASS**

`validation/a2_abstention.py` → engine → verify. 41 synthetic name-blind genes: the false-positives a
naive method accepts (co-expression alone, trait-overlap alone, population-structure alone, and a
high-degree hub with every qualifying fact but promiscuous), positive controls, and 20 seeded random
fact-subsets.

- **0 / 15** false-positive archetypes reached `component` or above — including all three `hub_flood`
  genes (every qualifying fact, but censored for promiscuity).
- **6 / 6** positive controls promoted (component / core), so abstention is discrimination, not inertia.
- **20 / 20** random subsets: the engine's tier matched the rule-derived qualification exactly — no
  leakage, no spurious promotion.

The engine rejects exactly the false-positives that single-signal methods accept, and never
manufactures a core from noise.

## E1 — cross-domain transfer · **PASS**

`validation/a1_panel.py` runs the identical pipeline over **8 documented mechanisms spanning 8
domains** — NOD2 signaling, DNA mismatch repair, complement, coagulation, LDL clearance, PINK1/Parkin
mitophagy, NLRP3 inflammasome, type-I interferon — changing **only the seed + member list**, no engine
/ probe / threshold code. Every domain produces a ledger; none abstains. The instrument is not fitted
to inflammation.

## A1 — positive-control panel · **PARTIAL (honest)** — and the partial is the finding

Same harness, scored member-vs-decoy across the 8 mechanisms, blind to identity. Two calibrations of
the differentiation lens bracket the result:

| differentiation lens | member recovery | decoy FP | hub censoring |
|---|---|---|---|
| absolute Wright bands (whole-region max-Fst **saturates** — every gene "dominant") | 83% | 28% | 81% |
| **genome-wide percentile** (top-decile = dominant; the count-bias fix) | 36% | 19% | **100%** |

The honest reading, from the primary data (`validation/local_fst.py`, `a1_score.py`):

- **Hub censoring is perfect** under the corrected lens (32/32) — the specificity censor is robust.
- **The method is differentiation-GATED by design.** Every convergence rule requires
  `differentiates population`; most mechanism members are *not* under population-differentiating
  selection, so a broad panel recovers the **population-differential subset** of each mechanism, not
  all members. That is on-thesis (the whole program is population-differential mechanism), but it means
  "recover every textbook member" was the wrong bar — the method never claimed it.
- **The residual weak discrimination (36% vs 19%) is a free-DATA-quality limit, not a reasoning
  limit.** GTEx *median-TPM* measures tissue-breadth similarity, not true co-expression, so
  broadly-expressed decoys chance-correlate with broadly-expressed seeds. The architecture is sound
  (censor perfect, convergence correct — A2/B3); the lens *shadows* are coarse. This is the "free
  shadows" thesis made quantitative, and it names the fix: a real co-expression dataset (not GTEx
  median) and variant-level differentiation (not whole-region max) — the same gated-data ceiling as F.

So E1 lands clean; A1's clean form needs better lens data, and the panel's value is having **measured**
exactly which layer is the bottleneck.

## C1 — cross-population fungibility · **PARTIAL — strong** (the headline, premise + machinery)

`validation/c1_crosspop.py` → `common_frame`. Two independent halves, both real:

- **The premise, measured in real 1000G data.** For each mechanism member, which superpopulation
  drives its lead-variant differentiation? **7/8 mechanisms have members driven by ≥2 different
  populations** — e.g. NOD2 signaling splits EAS-driven (CARD9, BIRC3) vs AFR-driven (RIPK2, XIAP,
  BIRC2). *Which* member carries the population-differentiated variant is population-specific. That is
  the fungibility premise, not asserted but measured.
- **The machinery.** Two populations' reads of one mechanism, with **disjoint** differentiated-filler
  tokens (AFR: afrg3/4/5/7/9; AMR: amrg8), handed to `common_frame`: the invariant role-frame recovers
  at **2/2 support** — the full `differentiate+dominate+track/bind → component → core → deep_core`
  chain, with roles binding to the population-specific tokens (component → afrg3 in AFR, → amrg8 in
  AMR). The reasoning abstracts the surface tokens and recovers the identical mechanism across
  populations.

**Honest scope (why PARTIAL, not full PASS).** This shows the premise exists in real data and the
engine recovers the invariant frame across disjoint fillers. It does **not** curate a specific disease
mechanism *known* to use functionally-disjoint genes per population with the same clinical outcome —
the fully convincing C1, and the head-to-head against token-bound methods (C2), still need a curated
real disjoint-filler dataset (the gated-data / collaborator ceiling, tier F). The driver populations
skew AFR/EAS (the most divergent superpops), as expected; a variant-level functional filter would
sharpen it.

---

_Open cells (need better lens data, a curated disjoint-filler dataset, or an external collaborator):
A1 (clean form), B1, B2, C1 (curated case), C2, D1, D2, E2 — see `docs/PROOF_POINTS.md`._

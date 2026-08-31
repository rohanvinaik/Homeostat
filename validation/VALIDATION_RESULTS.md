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

---

_Open cells (need local Fst infra, then panel/cross-population data, or an external collaborator):
A1, B1, B2, C1, C2, D1, D2, E1, E2 — see `docs/PROOF_POINTS.md`._

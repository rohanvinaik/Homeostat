# SESSION_HANDOFF — spine complete, renderers next (2026-09-02)

**The governing documents are `docs/SYSTEM_DESIGN.md` (engineering) and `docs/THESIS.md` (theory).** Read
those first. This file is the compaction-survival pointer; `SYSTEM_DESIGN.md §12` is the authoritative
build state.

## ⚠ READ THIS FIRST
Engine A (population node-birth / target-pinning loops) is **retired in code**, not just the docs. There is
one clinical engine: n=1, zero-time, over a fixed prior web, two-sign, abstaining. If a post-compact summary
steers you at "node birth" or a statistical `read.py`/permutation-null path, that is stale — trust
`SYSTEM_DESIGN.md`, `THESIS.md`, and the git log.

## WHERE WE ARE — the whole mechanical layer is built and pinned (133 tests, every pure decision Detective-complete)
- **Engine (resolve-narrow):** `search.eliminate_two_sign` (+ `constraint_disposition`), `position.py`
  (signed-ternary + Discrimination Guarantee), `jeeves.py` (EIG selector), `clinic.read_presentation`,
  `ground.py`, `web.py`/`otp.py`/`signal.py`.
- **Encoding layer:** `event.py` (`Event`, `couple_verdict`, `events_to_web`, `events_to_censors`,
  `active_censors`) and `clinic.read_from_events` — the encode→resolve spine, end to end.
- **Docs:** `SYSTEM_DESIGN.md` (engineering), `THESIS.md` (the full theory, ~6k words), canon +
  `THEORY_OF_THE_CASE` + `ETIOLOGY_ENGINE` + `CONCEPTUAL_AUDIT` all reconciled to the settled design.

## THE NEXT PHASE — the renderers (external I/O + object-led; the founder's biology enters here)
Everything downstream of a renderer's `list[Event]` is built and pinned. What remains (SYSTEM_DESIGN §12):
1. **Per-network renderers:** each network → `list[Event]` (regulatory→Reactome directed,
   evolutionary→BLAST, structural/genotype-deep→Pfam/GO/AlphaFold, developmental & exposome→Regenesis
   narratives, metabolic-flux→pathway/flux). **Founder-led:** the verb vocabulary, the DB per network, the
   caching/hash-pinning.
2. **Regenesis as generate-wide:** derive candidate mechanisms + roles + trajectory from the event story.
3. **The LRRK2 positive control (canon §13.3):** recover LRRK2–NOD2–RIPK2 as coherence, blind — the first
   real-data acceptance test.

## RECONSTRUCTION TEST
From `SYSTEM_DESIGN.md` + `THESIS.md` a fresh session should recover: the inverse-read problem; the
multi-network substrate (2 poles + 5 networks, genotype-deep); networks-as-banks; Regenesis as the one
story-engine for roles + trajectory; generate-wide/resolve-narrow; two-sign + certified-⊥ + the
informational zero; and that the mechanical spine (events → web + censors → elimination → verdict) is built
and pinned while the renderers are not. If it cannot, re-read those two docs and the git log first.

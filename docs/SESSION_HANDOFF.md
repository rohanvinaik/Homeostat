# SESSION_HANDOFF — renderer phase underway (2026-09-02)

*Written to the compaction-drift discipline (`~/Projects/rohan-vinaik.github.io/papers/Core Documents/
AI_architecture_papers/compaction_drift_overconfidence_notes.md` — a PERMANENT REFERENCE, never edit it):
one imperative next action, constraints stated WITH their reasons, pointers back at verifiable sources, a
reconstruction test. Governing docs: `docs/SYSTEM_DESIGN.md` (engineering) + `docs/THESIS.md` (theory).*

## ⚠ READ THIS FIRST — provenance beats any summary
The verifiable record is **git log + the current source + these docs**, not a post-compact summary. Two
stale-by-design traps a summary may re-inject, both already killed:
- "Engine A / node-birth / grow the graph" — RETIRED in code. One clinical engine, fixed prior web, two-sign.
- "Reactome for the regulatory renderer" — SWITCHED to SIGNOR (reason below). If a summary steers you at
  Reactome-with-complex-decomposition, it is stale.

## ★ WHERE WE ARE (verify: `git log --oneline`; GitHub `origin/main` is clean and current)
The whole **mechanical engine + encoding spine is built, pinned, pushed** (139 tests, ruff+ty clean; every
pure decision Detective-complete): `search.eliminate_two_sign`, `position.py`, `jeeves.py`,
`clinic.read_presentation`/`read_from_events`, `event.py` (the L2 contract: `Event`, `couple_verdict`,
`events_to_web`, role-scoped `events_to_censors`/`active_censors`), `ground.py`, `web/otp/signal`.

**This session's renderer work:** the FIRST renderer adapter is built — `signor.py` (`row_disposition`
Detective-COMPLETE; `row_to_event`/`signor_events`), turning SIGNOR rows → regulatory `Event`s. It already
recovers `RIPK2 → TRAF6` cleanly (the edge Reactome buried in a complex). Commit `2848c1e`.

## ★ THE ONE NEXT ACTION — get the founder's effect→sign policy, then run the first SIGNOR read
The SIGNOR adapter takes an `effect_policy: Mapping[str,int]` (founder config — NOT defaulted; that is where
the activity-vs-quantity call lives). The imperative: **get the founder's effect→sign policy (activity-only,
or activity + quantity), then run the first SIGNOR → two-sign read toward the LRRK2 control.** The SIGNOR
effect vocabulary + counts are in the last assistant turn (up/down-regulates{,-activity,-quantity...},
form-complex→0, unknown→0). Do NOT author the policy yourself (compute-not-impose). The mechanical brick that
needs no biology, buildable meanwhile: the **SIGNOR fetch/cache layer** (download `getData.php?organism=9606&
format=csv`, one 21 MB TSV; cache under `paths.DATA`, gitignored, hash-pinned per `REFERENCE_MANIFEST`;
User-Agent header required — bare urllib gets 403). The dump is already fetched at
`<scratchpad>/signor_human.csv` (43,492 rows, 29 cols, tab-separated, no header).

## ★★ LOCKED DECISIONS (renderer phase) — with reasons, so they survive
- **Source = SIGNOR, not Reactome.** *Why:* Reactome's reaction model is complex-centric — gene edges are
  buried inside named complexes (`PAMP:NOD:RIP2:NEMO`), the catalyst is a complex (TRAF6 ligase), and the
  modification happens to a component *inside* the complex, so you'd need recursive complex decomposition.
  SIGNOR gives **gene-level directed causal relations** (`A --effect--> B`) as explicit *filterable columns*
  (27,325 protein→protein of 43,492), with a confidence score and a mechanism — no decomposition.
- **Parser = harmonizing, not GSE.** *Why:* bio-DB "sentences" are typed, fixed-construction, hole-filled
  AST-style templates, not open-ended NL. GSE is for open-ended NLP (wrong, expensive tool); harmonizing's
  constraint-propagation-over-a-fixed-schema is exactly the fit. Harmonizing's job is the **entity
  normalization** (proteinfamily/complex/synonym → canonical gene atomics) + the template mechanism/NL field
  — NOT the directed edge (that's SIGNOR field access). Two layers.
- **Atomics = distinct role-states** (`p-RIPK2` ≠ `RIPK2`); **scope = wider**; **cache = hash-pinned**;
  effect map: `up/down-regulates*`→±1, `form complex`→0 (physical-binding network), `unknown`→0.
- **Verb = SIGNOR `mechanism`** (phosphorylation/binding/…); could carry activity-vs-quantity as the verb so
  the two stay distinguishable downstream even if both enter the regulatory network.

## ★ THE REMAINING PIECES (SYSTEM_DESIGN §12; everything downstream of a renderer's `list[Event]` is built)
1. effect-policy (founder) → run. 2. SIGNOR fetch/cache (mechanical). 3. harmonizing entity-normalization.
4. the other network renderers (evolutionary→BLAST, structural/genotype-deep→Pfam/GO/AlphaFold,
   developmental & exposome→harmonizing over template narratives, metabolic-flux→pathway). 5. the **LRRK2
   positive control** (canon §13.3) — recover LRRK2–NOD2–RIPK2 as coherence, blind: the acceptance test.

## ★ PRIVACY — MUST SURVIVE (a real incident this session, fully remediated)
The founder's actual conditions and an ADHD/meds disclosure leaked into README + THESIS + the first handoff;
they were scrubbed from the working tree **and from git history** (filter-branch on the unpushed range +
reflog/gc), verified empty, then pushed clean. **NEVER re-introduce personal conditions/medical facts into
any committed or public-facing file.** The greenfield case IS the founder's n=1 — genericize it in docs
(THESIS/README use "a cluster of conditions across several body systems"). The `POTS`⊂`spots` / `narcolepsy`
spell-check test-vocab in `ground.py`/`test_ground.py` is acceptable per the founder (generic example).

## ★ DATA ACCESS — confirmed live this session
SIGNOR, Reactome, GO, InterPro/Pfam, NCBI/BLAST, and pypi/ty are all reachable (the earlier failures were
plane wifi). The only remaining limit is structural, not connectivity: the §12.4 gated genotype×phenotype
cohort — and the design deliberately works from the free public "shadows", which are all up.

## RECONSTRUCTION TEST
From `SYSTEM_DESIGN.md` + `THESIS.md` + this file, a fresh session should recover: (a) the mechanical engine
+ encoding spine is built/pinned/pushed; (b) the renderer phase is underway, SIGNOR adapter built; (c) source
= SIGNOR (Reactome is complex-centric), parser = harmonizing (not GSE); (d) next action = get the founder's
effect→sign policy then run toward LRRK2; (e) the privacy rule. If it cannot, re-read the two governing docs
and `git log` before doing anything — do NOT re-derive from a summary.

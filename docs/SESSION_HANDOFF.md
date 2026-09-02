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

**FOUR coupling networks + the prior-web assembly are BUILT, pinned, verified E2E** (146 tests; every pure
decision Detective-COMPLETE; each network = a `*.py` renderer + `*_fetch.py` I/O shell, data gitignored +
hash-pinned in `REFERENCE_MANIFEST`):
- **regulatory** — `signor.py` (SIGNOR, DIRECTED; earns arrows). `sign=+1` always (support, not polarity —
  polarity is the verb amplifies/inhibits); mode = activity/abundance peer marker.
- **physical** — `string.py` (STRING physical binding, UNDIRECTED vote; evidence bright line experimental|
  database → emit, textmining-only → skip). ENSP→symbol via `string_fetch.load_alias_map`.
- **evolutionary** — `homology.py` (Ensembl Compara human paralogs, UNDIRECTED vote; fungibility). Measured
  12.8% overlap with reg/phys → genuinely orthogonal.
- **metabolic** — `metabolic.py` (Reactome co-membership scoped to the Metabolism subtree via BFS, UNDIRECTED
  vote). Entrez→symbol via NCBI gene_info. Scoping is load-bearing.
- **`prior_web.py`** — the single assembly point: `all_events()` renders all four; `build_prior_web()` =
  `events_to_web(..., DIRECTED_NETWORKS={"regulatory"})`. `python -m homeostat.prior_web` → 1.5M events →
  1.44M couplings; **3,098 supported by ALL FOUR independent networks**. Also this session: the old
  statistical cluster (nodes/pbs/gnomad_pile/eir_cohort/l2_encoder) is TRASHED (Serena-verified isolated).

## ★ THE ONE NEXT ACTION — the Regenesis generate-wide engagement (Socratic, founder-reserved)
The COUPLING-network layer (events_to_web-facing) is complete. The remaining canonical networks —
**developmental, exposome** (temporal), **genotype-deep, phenotype** (poles) — are Regenesis/role/temporal/
per-person facing, NOT gene-gene couplings; forcing them into `events_to_web` would be drift. The founder
reserved this phase for **Socratic dialogue**: how the frozen multi-network web/event-stream becomes roles +
implied mechanism + the read toward the blind LRRK2 control (§13.3). So the next action is to OPEN that
Socratic engagement, pointing Regenesis at `prior_web.build_prior_web()`. (Deferred coupling network:
**co-expression** — the highest-drift-risk vote, GTEx-vs-proxy source + computed-association care, to handle
carefully, not autonomously.) Data access confirmed live: SIGNOR, STRING, Ensembl, Reactome, NCBI all 200.

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
- **Atomics = distinct role-states** (`p-RIPK2` ≠ `RIPK2`); **scope = wider**; **cache = hash-pinned**.
- **Effect grammar → (sign, verb, mode), SETTLED + BUILT (2026-09-02).** direction→**verb** `amplifies`/
  `inhibits` (the regulatory POLARITY); **`Event.sign` = +1 for EVERY SIGNOR edge** — sign is coupling
  support/censor, NOT polarity, and SIGNOR only ever asserts a relation, so a real inhibition is `inhibits`/+1,
  never a censor (a −1 would make `couple_verdict` falsely `killed`). Censors (−1) come from physics-orthogonal
  exclusions / developmental closing-off / treatment-response, never from SIGNOR. mode (`activity`/`quantity`/
  bare) → a peer `mode` marker on the SAME edge (`Event.mode`, added this session) — the GSE set-theory/density
  op (κ-density, super-additive at bridges), NOT a scalar, NOT a separate network; quantity submodes fold into
  `abundance`; bare = no marker (mode-level zero). `unknown`/`form complex` → skip. This CORRECTS the earlier
  `±1` note (it conflated polarity with support/censor). Verbs `amplifies`/`inhibits` are the ETIOLOGY §3 L2
  reserved directed verbs; mode-marker facts (`A modulates activity` / `A titrates abundance`) are the L3
  role-firing layer's job, verbs founder-authored, centroids mined from SIGNOR's `mechanism` column.

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

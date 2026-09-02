# SESSION_HANDOFF — story layer underway (2026-09-02)

*Written to the compaction-drift discipline (`~/Projects/rohan-vinaik.github.io/papers/Core Documents/
AI_architecture_papers/compaction_drift_overconfidence_notes.md` — a PERMANENT REFERENCE, never edit it):
one imperative next action, constraints stated WITH their reasons, pointers back at verifiable sources, a
reconstruction test. Governing docs: `docs/SYSTEM_DESIGN.md` (engineering) + `docs/THESIS.md` (theory) +
`docs/STORY_LAYER.md` (the Regenesis generate-wide design).*

## ⚠ READ THIS FIRST — provenance beats any summary
The verifiable record is **git log + the current source + these docs**, not a post-compact summary.
Stale-by-design traps a summary may re-inject, ALL already killed:
- "Regenesis is a PORT of story-understanding into biology" — WRONG. It is the SAME engine; biology is what
  it was always reading. The narrative-meaning theory IS the disease semantics (THESIS ch.9, STORY_LAYER.md).
- "co-metabolizes" / "cometabolizes" as the metabolic verb — RETIRED. GSE mangles the hyphen and drops the
  non-word. The metabolic verb is **"channels"** (real WordNet verb, firing-confirmed). Stale if you see it.
- The old-lens mechanism universe (differentiator/coexpressor/dominator/wirer/sensor; literal-object rules
  like `x amplifies signal`) — RETIRED with the l2_encoder. The universe is now GENE-EDGE rules over the four
  network verbs (`x amplifies y`). Do NOT restore literal-object Forms.
- "Engine A / node-birth / grow the graph" — RETIRED. One clinical engine, fixed prior web, two-sign.
- "Reactome for the REGULATORY renderer" — regulatory = SIGNOR (Reactome is complex-centric). Reactome IS
  used, but ONLY for the metabolic network (pathway co-membership). Don't cross them.

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

**THE STORY LAYER (Regenesis generate-wide) is UNDERWAY — the story is FOUND and half-built** (150 tests;
settled Socratically; THESIS ch.9 rewritten; `docs/STORY_LAYER.md` written):
- **The story: NOT a port — the SAME engine.** The narrative-meaning theory (`~/Projects/rohan-vinaik.github.
  io/papers/Core Documents/New_Work/NARRATIVE_MEANING.md`) IS the disease semantics: shadow = M3 (sub-threshold
  signals significant only in concert), convergence = H3 (orthogonal wrongs that sum), certified-⊥ = H4
  (abstention), mis-fit tracing = Baymax, generate/resolve = H2 (Dr. House). A mechanism is a GENRE (a
  meaning-mechanism, not a plot-shape). genres.index = plots · archetypes.index = roles.
- **`story.py` (the L2→L3 bridge) BUILT + pinned** — events → opaque-token SVO sentences + sidecar
  (opaque→real). Opacity forces roles from STRUCTURE (GSE can't import gene-name knowledge). Renders the RAW
  events (not collapsed couplings) so convergence is preserved.
- **`universes/mechanism/` (the ROLES / archetypes) RECONCILED + FIRING-CONFIRMED on real biology.** Gene-edge
  rules over the four verbs: amplifier/inhibitor/binder/homolog(fungibility)/metabolizer/transducer(chain-
  middle)/component(H3 edge-convergence)/zero. FIRED on the real LRRK2/inflammatory axis (68 events, opaque
  tokens): recovered BIRC2 = top component (κ 17.97), RIPK1 = transducer (the textbook TNF relay), BIRC3 =
  fungible homolog of XIAP — 29 role-facts + 52 self-written mechanism-rules, ZERO gene names in the reasoning.

## ★ THE ONE NEXT ACTION — author `universes/mechanism/genres.index` (the mechanism-genres), FIRING-confirmed
The ROLE layer is done + validated; the GENRE layer is next. Author `genres.index` + `.rules` for the four
mechanism-genres, each carrying its M/H meaning-mechanism (STORY_LAYER.md §3): **tragedy** (dysregulatory
cascade → locked doom; composes on the transducer-chain that already fires), **ironic-comedy** (a reinforcing
vicious cycle), **allegory** (isomorphic-role / different-genes = fungibility, `common_frame`), **epic-quest**
(resolution via a distant bridge). AUTHOR each, then FIRE it via `story.render_story(scoped_events)` →
`understand(kind="text", universe_root=".../universes/mechanism", universe_only=True)` on the real LRRK2 story
— **0 derivations = a WIRING failure (missing trigger centroid), NEVER trusted as abstention** (cardinal
rule). Metabolic verb = "channels". Then the wiring (`understand` → generate-wide→resolve-narrow: candidates →
`eliminate_two_sign`) and the **blind LRRK2 control** (canon §13.3). Data access live (SIGNOR/STRING/Ensembl/
Reactome/NCBI all 200); Regenesis is JVM-free (`understand_batch` mass-fires, no one-JVM concern).

## ★★ LOCKED DECISIONS — with reasons, so they survive

**Story layer (2026-09-02):**
- **Regenesis is the SAME engine, not a port.** *Why:* the narrative-meaning theory (built blind to this
  project) IS the disease semantics — the shadow is literally M3, convergence H3, abstention H4. Reframing it
  as "story-understanding applied to biology" loses the fixed point and invites re-inventing a parallel frame
  library. Point it at `universes/mechanism/`; do not build a second frame set.
- **Gene-edge rendering, not literal-object.** *Why:* `story.py` renders `Gene1 amplifies Gene2` (gene
  object), which fires role Forms (`if x amplifies y then x becomes amplifier`), same-subject convergence
  (`x amplifies y and x binds y → component`, FIRES), and causal chains (`x amplifies y and y amplifies z → y
  transducer`, y re-binds in SUBJECT position, FIRES). The old literal objects (`x amplifies signal`) were for
  the trashed lens encoder and CANNOT express chains. Firing-confirmed on the live engine.
- **Metabolic verb = "channels".** *Why:* firing showed "co-metabolizes" mangles (GSE splits the hyphen) and
  "cometabolizes" is dropped (not a word). "channels" (substrate channeling) is a real WordNet verb that
  parses + fires. Changed in `metabolic.py` (was co-metabolizes).
- **Fire before trusting (cardinal).** *Why:* 0 derivations is a WIRING failure (missing trigger centroid),
  not abstention. Trigger column = class centroids, NEVER padded synonyms, NEVER gene names, NEVER rewrite
  input to hit a verb. Author a Form THEN fire it on real data.

**Renderer phase:**
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

## ★ THE REMAINING PIECES (small — the intelligence is in the frames + geometry, not the code)
1. **`genres.index`** (the mechanism-genres: tragedy / ironic-comedy / allegory / epic-quest — the NEXT
   action, firing-confirmed).
2. **The wiring**: `understand()` over the real story → the generate-wide→resolve-narrow bridge (Regenesis
   candidates → `search.eliminate_two_sign` over the person's positioned deviations → verdict / certified-⊥).
3. **The blind LRRK2 control** (canon §13.3) — recover LRRK2–NOD2–RIPK2 as coherence, blind: the acceptance
   test. (The role read ALREADY recovers RIPK1 as transducer / BIRC2 as component on the axis.)
4. Later: the temporal networks (developmental/exposome) + the poles (genotype-deep/phenotype) + the deferred
   co-expression vote — Regenesis/temporal/per-person facing, after the four-network read is proven.

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
From `SYSTEM_DESIGN.md` + `THESIS.md` + `STORY_LAYER.md` + this file, a fresh session should recover: (a) the
engine + encoding spine + FOUR coupling-network renderers + `prior_web` are built/pinned/pushed; (b) the story
layer is underway — `story.py` (L2→L3 opaque-token bridge) built, `universes/mechanism/` ROLES reconciled +
firing-confirmed on real biology (BIRC2 = top component, RIPK1 = transducer, recovered blind); (c) Regenesis
is the SAME engine (not a port), the disease-shadow IS M3, convergence IS H3, abstention IS H4; (d) next action
= author `genres.index` and FIRE it (0-derivations = a wiring failure, never abstention), then the wiring +
blind LRRK2 control; (e) metabolic verb = "channels", NOT co-metabolizes; gene-edge rules, not literal-object;
(f) the privacy rule. If it cannot, re-read the governing docs + `git log` before acting — do NOT re-derive
from a summary.

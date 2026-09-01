# SESSION_HANDOFF — Homeostat re-architecture, 2026-09-01

*Written to the compaction-drift discipline (see `~/Projects/rohan-vinaik.github.io/papers/Core
Documents/AI_architecture_papers/compaction_drift_overconfidence_notes.md`): constraints structured with
their **why**, the next action as ONE imperative, the mechanism restated, loud pointers back at the sources.
Repo: `~/Projects/Homeostat` (`main`). Gate green: ruff + ty clean, **106 tests pass**.*

## ⚠ READ THIS FIRST — this session WAS the compaction drift, live
The session opened post-compact. I read the summary, felt it sufficient, and **confidently rebuilt the wrong
design**: I took GSE (the ternary *substrate*) for the architecture, re-derived statistics-as-method, and
carried an n=1/population confusion — for many turns, fluently, feeling like I was continuing the plan. The
founder corrected it each time by pointing me at the actual sources. **You (the fresh reader) are at maximum
risk right now.** Before you build anything: restate, in your OWN words at the MECHANISM level, what the
design is and what you're about to do, and hand it to the founder. Do not trust that you hold the plan
because you can restate its words. The smoothness is the warning sign.

## ★ WHERE WE ARE — the machinery is BUILT and pinned, in the correct (non-statistical) genus
- **The statistical genus is RIPPED** (`19cf5d1`): `kappa.py`'s pagerank/participation scorers + the whole
  `validation/` + `probes/` + `read.py` layer are GONE. *Do not resurrect them* — they are the recorded death
  (canon §15), statistics-as-method.
- **Engine** (`42d3f24`): `search.eliminate_to_survivor` + `loop.resolve_presentation` — seedless: drive
  **H = log₂|surviving sources| → 0** by candidate-elimination to a UNIQUE survivor, no protected target.
- **Container** (`df86d54`): `web.py` — the weighted-ternary relational web (`Coupling(a,b,weight,
  direction)`, direction ∈ {+1 a→b, −1 b→a, 0 undirected}; a MISSING coupling = the informational zero) +
  `kill_matrix(web, observed)`. Wired end-to-end: web → kill_matrix → `resolve_presentation` → recovered
  source (test proves it; the undirected version correctly stays plural).
- **Front door** (`ae913ed`): `ground.py` — ground-or-abstain symptom resolution, the SymbolicSpellCheck law.
  Kills the `POTS`⊂`spots` poisoning; the regression is pinned both ways.
- **Docs synced:** `THEORY_OF_THE_CASE.md` Part II "The constraint object is a weighted relational web"
  (`ce5e040`); canon `§0 Warning 2` + `§11.2` n=1 fix (`a2a11dd`); `CONCEPTUAL_AUDIT.md` §5.2 → seedless.

## ★ THE ONE NEXT ACTION — confirm node-birth's shape with the founder, then build the direction-upgrade grower
Node-birth is the last machinery piece. Building it surfaced a **forced finding** (stated with its reason —
a bare rule has no mass): a candidate is a *source* and a symptom-constraint kills sources that can't reach
it, so **adding a coupling only ADDS reachability → it can make MORE sources survive, never fewer → adding
edges cannot resolve a plural residual.** The only move that can is **earning direction** — upgrading an
undirected coupling to directed *removes* the reverse path, drops a source below "reaches all symptoms," and
collapses the plurality. So node-birth = apply an *evidence-backed* directed upgrade from a supplied pool
that separates the current residual; STUCK when the pool has nothing. It never GUESSES a direction (a wrong
arrow is DESTRUCTION — unrecoverable in eliminate-to-survivor), only applies an earned one. **Forbidden twin:
node-birth is NOT edge-adding and NOT direction-guessing.** — This was posed to the founder as a fork
(earn-direction vs. grow-genuinely-new-nodes) and **they had not answered when we compacted.** So the
imperative: restate this earn-direction mechanism to the founder for a yes/redirect, THEN build the grower.
Do NOT build it silently on this finding alone.

## ★★ WORKFLOW DISCIPLINE — each with its WHY (do not re-derive these away)
- **DATA-GEOMETRY + CLASSICAL AI, NOT STATISTICS** (the cardinal law). Every piece is elimination/coherence,
  never a frequency/participation/p-value. *Why:* the mechanism is a fungible, sub-threshold *collective
  state*; element-testing is structurally blind at any sample size (canon §2). Drift-alarm words: significant,
  enriched, associated, frequency, hub, participation.
- **N=1, zero-time, per-person** (canon §0 Warning 2). The engine reads ONE person; it needs **no**
  population, ensemble, or cross-source agreement to run. *Why:* the n=1 conflation (fixed this session) fused
  "the engine runs on one person" (true, the design) with "one person can't redefine a disease" (the ONLY
  real limit). Do not re-fuse them; the population/ensemble material is downstream *validation*, not method.
- **Serena for WIRING, Detective for PINNING.** `find_referencing_symbols` BEFORE any edit. Detective:
  `detective converge 'file.py::fn' --project-root . 2>/dev/null` for clean output; follow `DO THIS`, do not
  grind (modulo-N-unproven-equivalent = DONE); **orchestrators get hand intent tests, pure decisions get
  converge.** *Why:* the original drift was built WITHOUT the two-step — one `find_referencing_symbols` would
  have shown the σ-engine was orphaned.
- **CONVERSATIONAL register, plain words, never jargon-dense, never condescending.** *Why:* the founder is a self-described "poor oracle" (forgets, re-derives from scratch) — and
  the jargon-dense canon is *literally what hid the n=1 bug*; plain socratic conversation found it in two
  sentences. Reason WITH him; do not lecture, do not use toy/child analogies.
- **Compute-not-impose.** The constraint OBJECT (the specific couplings/nodes/roles) is author-led (canon
  §13.1), SDIS-seeded, and must NEVER be invented. The machinery is object-agnostic; the content plugs into
  the sockets (`vocab`/`valid_words` in ground.py, the couplings in web.py, the evidence pool in node-birth).
  *Why:* guessing the object is the root of the recorded death (§12.14).
- **Commit freely to `main`; gate BEFORE commit** — `ruff check` (never `| tail`, it masks the exit code) +
  `uvx ty check src` + pytest, all green.

## ★ THE DESIGN, at mechanism level (the anti-method-substitution artifact — the thing to write in your own words)
A person's symptoms are **deviations at nodes** of a bounded, weighted, ternary-directed **relational web**
(the couplings are PRIOR structure — known biology + coupling-evidence triangulated once; the deviations are
per-person). A candidate mechanism is a candidate **source node**; an observed symptom is a **constraint**
that kills sources that can't propagate to it; drive **H → 0**; the surviving source is the mechanism.
Coherence = **σ** (min constraints to pin it, a Blum measure), NOT a p-value. Direction is **earned**
(treatment-response probe = the Socratic-learning signal; Reactome), never guessed. Absence = the
informational zero. It's tractable because the universe is **bounded** (what makes σ finite). Toy proof: the
*Sisyphean Air Route Map* (nodes recovered purely from a weighted relational web).
Grounding stack (built by the founder, reused here): Peitho (mined-zero elimination shell) · Specification
Complexity (σ) · SSL (understanding-as-σ-trajectory) · SymbolicSpellCheck (ground-or-abstain,
non-destruction) · Regenesis (roles). **GSE/HDC is the ternary substrate, NOT the architecture — do not
re-elevate it.**

## ★ POINTERS — the sources that can contradict this handoff (trust them over this text)
- `git log --oneline`: `19cf5d1` rip → `42d3f24` spine → `ce5e040` design → `a2a11dd` n=1 fix →
  `df86d54` container → `ae913ed` front door.
- `docs/THEORY_OF_THE_CASE.md` Part II (design + the couplings section); `docs/REGULATORY_DEFICIT_PROGRAM.md`
  §0 Warning 2 + §3.4 + §13.1 + §15; `docs/CONCEPTUAL_AUDIT.md`. Founder's stack, primary sources: SSL,
  Specification Complexity, harmonizing (`~/Projects/Kaggle_Killer/competitions/harmonizing/src/
  symbolic_healing.py` — the cell-line fact table = the constraint-object precedent), COEC.
- `src/homeostat/{search,loop,web,ground}.py` — the machinery.

## ★ RECONSTRUCTION TEST
From this file alone: (a) WHERE = statistical layer ripped; engine + container + front-door built and pinned;
106 tests green. (b) NEXT = restate the earn-direction node-birth mechanism to the founder for a
yes/redirect, THEN build the direction-upgrade grower over an evidence pool. (c) MECHANISM = node-birth EARNS
a direction (removes reachability) to collapse plural sources — adding edges can't (only adds reachability);
guessing a direction is destruction. (d) DISCIPLINE = no statistics / no n=1-population / no jargon / no
imposing-the-object; Serena-wire, Detective-pin; plain conversational register. (e) FORBIDDEN = resurrect
the statistical layer; guess a direction; invent the constraint object; **read this summary and re-derive the
design instead of reading the sources.** If a fresh session cannot recover all five, STOP and re-read the git
log + `docs/THEORY_OF_THE_CASE.md` Part II before doing anything.

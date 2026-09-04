# Homeostat — Session Handoff (input layer in progress)

**Written 2026-09-05 at `f6d3cc4`.** For a fresh agent/user to complete the remaining work with zero
context loss. Read this top-to-bottom once, then work from §5 (the task list) with §3 (the discipline)
and §2 (the WHY) always in view. **Ground truth is `git log` + the source + this file's cited commits —
never a memory or summary alone** (verify before building on any claim).

---

## 1. Where it is, exactly (verifiable)

- **Branch/HEAD:** `main` @ `f6d3cc4`, clean tree, **2 unpushed** (`93a135a`, `f6d3cc4`). Push only with
  Rohan's explicit say-so.
- **Scale:** 48 modules · 462 tests green · ruff + ty clean · every pure decision Detective-pinned
  (residuals read; see §3).
- **Canonical as-built map:** `ARCHITECTURE.md` (traced from source, layer by layer — **read it first**
  for the full wiring). This file is the *forward* plan; ARCHITECTURE.md is the *current* state.

**What is LIVE (built, pinned, wired into the apex read `driver.drive`):**
the two-sign elimination engine (`search`/`clinic`/`polarity`) → the story-read (`narrative` + the four
genres `tragedy`/`comedy`/`fungibility`(allegory)/`quest` + `topology` + `lament`) → the resolve-narrow
recommendation engine (`resolve.rank_clusters`: coverage × internal-coherence × the calibrated
predictive **meter** `meter.py` SSL §9.3) → the **σ_sem completeness** read (`completeness.py`) → the
**operator hypothesis** (`operator.py`, incr.3a) → the **mechanism-level Jeeves** (`resolve.cluster_-
discriminant`, incr.3b). The whole thing runs on pure-Python "potato compute," deterministic and
auditable, with Regenesis's narrative universe reached via the pure `kind='contracts'` path (no JVM/GSE
subprocess).

**The INPUT LAYER (the current build) — 2 of ~4 increments done:**
- **incr.1 DONE** (`93a135a`) — `relevance.py`: `trait_gene_index(rows)` (the GWAS-catalog trait→gene
  reference) + `relevant_subspace(diagnosis, trait_index, fungible)` (canonical genes widened by earned
  fungibility). Both Detective-COMPLETE.
- **incr.2 DONE** (`f6d3cc4`) — `person.py`: `read_person(...)` = ONE TURN of the interface (§2). Plus
  `relevance.fungible_map(...)` and `drive`'s new **`relevant=` param (option B)**: it restricts the
  eligible mechanism SOURCES to the subspace while the observed shadow stays sacrosanct; a certified-⊥ or
  abstain results if no relevant source explains the shadow (the label "falls out"). Integration-tested.

---

## 2. The WHY — the epistemology you must not break

**Homeostat is FIRST a theory-validation instrument, medicine second.** The thesis: a classical-AI stack
(symbolic elimination + data-geometry + Patrick Winston's strong-story understanding, **NO ML, no model,
nothing trained**) beats label-level medicine at its own game, on potato compute, deterministically and
auditably, producing plural/certified-abstaining reads a neural net structurally cannot. **Do not ever
"add a small model for the hard part" — that demolishes the whole point.** The intelligence is in the
correctness of the geometry, not the size of a network.

**Homeostat *is* σ_sem applied to biology** — the direct instantiation of Rohan's Semantic Specification
Learning (SSL) thesis. The four grounding papers (READ THEM before touching resolve/meter/completeness):
- `~/resume/Specification_Complexity_Paper/specification_complexity_paper.md` — σ = teaching dimension;
  the bulk/tail = statistical→exact learning.
- `~/Projects/rohan-vinaik.github.io/papers/Core Documents/SIGNIFICANCE_WEIGHTING.md` — κ = marginal
  coverage; significance = surprise normalized by branching freedom (a bracket, never a point).
- `~/tools/Detective/docs/theory/NEGATIVE_SPECIFICATION.md` — the two-sign μ⁻; the automation boundary.
- `~/Projects/rohan-vinaik.github.io/papers/Core Documents/Semantic_Specification_Learning/01_PAPER_SKELETON.md`
  — the MASTER: understanding = the σ_sem-trajectory; §9.3 the NML/KT coherence meter; **medicine is
  named as an instance of the theory**.

**THE INTERFACE PRINCIPLE (locked with Rohan — this is what the input layer instantiates).** The
prototype is **Detective's CLI** (`~/tools/Detective/Detective/cli.py`; the load-bearing functions are
`_completeness_verdict`, `candidate_equivalent_caveat`, `converge_next_action`). It is a **call-and-
response constitutional separation of epistemic authority**:
- **The COMPUTER's domain** = the decidable, mechanical geometry, computed COMPLETELY, and it **abstains
  PRECISELY at the undecidable** (Detective refuses to claim equivalence — "candidate-equivalent,
  UNPROVEN"; Homeostat returns certified-⊥ / honest abstention / a surviving plurality). It never
  fabricates.
- **The OPERATOR's domain** = intent / what only the person holds — the diagnosis (label), the labs
  (measured observations), the notes (lived experience), the hypotheses (intuition), and **the answer to
  the Jeeves DO-THIS** (the discriminating measurement). The operator never computes the mechanism.
- **The INTERFACE** = a call-and-response. The read's output is the precise CALL (verdict + story + ranked
  mechanisms + σ_sem completeness + the mechanism-level Jeeves DO-THIS = the machine's one typed
  counter-ask). The operator RESPONDS in their domain; each abstains wholly from the other's competence;
  together they reach a **settled truth** (RESOLVED / certified-⊥ / honest abstention) neither could reach
  alone.
- **PROOF BEATS JUDGEMENT.** Every operator input is a **TESTED proposal**, never ground truth: it falls
  out if the geometry contradicts it. The diagnosis (a lossy label) is `option B`: it restricts the
  *search for the cause* (the mechanism SOURCES), and the observed **shadow stays sacrosanct** — a label
  never censors an observation. This is why `read_person` passes the subspace as `drive(relevant=...)`,
  never as a shadow filter. (Rohan, verbatim: *"screw the operators, correctness stays in the code."*)

**`read_person` is one TURN of that loop.** The full loop (operator measures the Jeeves DO-THIS → adds it
as a lab → calls `read_person` again → repeat until settled) is external; making the loop ergonomic is a
remaining task (§5).

---

## 3. The WORKFLOW discipline — non-negotiable, this is how every piece was built

**The two-step (ONE loop, not two habits — dropping either collapses correctness):**
1. **DIAGNOSE with Serena FIRST**, never read-and-infer. `get_symbols_overview` / `find_symbol` (with
   `include_body`) / **`find_referencing_symbols` before every edit** (the load-bearing call: is it wired,
   or defined-but-unused?). Grep is deprioritized; the `no-grep-python` hook BLOCKS reading `.py` as text
   via bash (`cat`/`tail`/`grep file.py`) — use `Read`/Serena. `uvx ty check <file>` after non-trivial
   edits (advisory; it caught a real `list`-invariance bug this session).
2. **PIN with Detective**: `detective converge 'src/homeostat/FILE.py::func'`. Extract the **pure decision**
   (total function over str/int/bool/list/dict/set → named string codes, not bools) so `--input` can
   express it; orchestration over pinned pieces is intent-tested instead.

**READ THE RESIDUAL REPORT — never trust the `FINAL`/`COMPLETE` headline** (`.detective/reports/converge_
<func>.txt`). `killable` / `candidate-equivalent (UNPROVEN)` / `structural caveat` / `fixture caveat` are
**OBLIGATIONS, not the leave-it category**. Detective's search *misses distinguishers* — this session it
mis-filed **6+ genuinely-killable mutants as "candidate-equivalent"** (an OPPOSE-majority direction, an
out-of-cluster dilution, a malformed EIG partition, a positive-gain-floor at scale, boundary/type cases).
**Verify-don't-infer:** construct the distinguishing `--input` (or a differential test) before you accept
equivalence; `detective flag <mutant> --note "proof"` ONLY when you've *proven* equivalence (e.g. a
crash-mutant that never returns a different value, or `log2(1)=0` making a boundary inert). "value-
complete modulo N crash-only" is an honest COMPLETE (run-kills bank nothing toward value completeness).

**The pre-commit gate — run BEFORE every commit, and NEVER pipe ruff before `&& commit`** (a `| head`/
`| tail` masks the exit code — this session committed over a ruff failure once by doing exactly that):
`ruff check .` && `ruff format --check <files>` && `uvx ty check <files>` && `PYTHONPATH=src pytest -q`.
**E501 (line > 100) is the recurring time-sink** — unicode `— × σ → ≥ ₊` each count as 1 char; wrap
docstrings/comments to ~85 to leave margin. Run `ruff check .` (no pipe) and fix ALL before committing.

**Other standing rules:** commit freely to `main` (solo repo, no branches — a local commit is a cheap
checkpoint); **push only with explicit permission**. Socratic design mode: surface **ONE fork with a
lean**, let Rohan adjudicate — do not do the hard design solo. Tools are **PascalCase** (Homeostat,
Detective, Regenesis, ModelAtlas, LintGate). Detective flags live in `.detective/` (gitignored, local).

---

## 4. The code map (where everything is)

- **Apex:** `driver.py` — `drive(events, positions, verb_sign, active_roles, probes, proteins,
  hypotheses, min_weight, band, relevant)` → `DriverRead(verdict, story, ranked, completeness, probe,
  trajectory, censored, dropped, operator)`. The one composed read; holds no biology of its own (Law 11).
- **Elimination (L4):** `search.eliminate_two_sign`, `clinic` (verdicts + full-C cert), `polarity`
  (`net_polarities`/`polarity_censors`/`signed_adjacency`), `jeeves` (`expected_information_gain`/
  `select_probe`), `web` (`kill_matrix`/`ancestor_cone`/`induced_subweb`).
- **Story (L5):** `narrative.read_story`, `tragedy`/`comedy`/`fungibility`/`quest`/`lament`,
  `topology.signed_adjacency` (OTP-ternary nested dict — the genre substrate).
- **Resolve (L5):** `resolve.py` (`connected_components`/`story_clusters`/`cluster_coverage`/
  `cluster_coherence`/`cluster_meter`/`rank_clusters`/`cluster_discriminant`), `meter.py`
  (`coherence_meter`/`source_outcomes`/`nml_regret`), `recommend.score_candidate`.
- **Completeness (L6):** `completeness.py` (`resolution_entropy`/`spec_completeness`/`top_band`/
  `read_completeness` → `SpecCompleteness(h0, h_residual, resolved, i_solve)`; `i_solve` = the
  mechanism-Jeeves NODE).
- **Operator:** `operator.py` (`edge_outcome`/`operator_ledger` → `DriverRead.operator`).
- **INPUT LAYER:** `relevance.py` (`trait_gene_index`/`relevant_subspace`/`fungible_map`),
  `person.py` (`read_person`).
- **Positions/banks:** `producer.signals_to_positions` (labs→positions), `position`, `trait_wiring`
  (GWAS catalog cols `MAPPED_GENE`=14, `MAPPED_TRAIT`=34; parsers reused by `relevance`), the six banks
  `signor`/`string`/`homology`/`metabolic`/`coexpression`/`trait_wiring` + `*_fetch.py` IO shells.
- **Canonical docs:** `ARCHITECTURE.md`, `docs/SYSTEM_DESIGN.md` (the 11 laws; **§7 = the treatment-
  response / negative-sign censor** for notes — VERIFY it before building incr.3), `docs/THESIS.md`,
  `docs/STORY_LAYER.md`, `docs/REGULATORY_DEFICIT_PROGRAM.md`.

---

## 5. WHAT'S LEFT — the exact remaining tasks (in dependency order)

**A. Input layer increment 3 — notes → directionality (NEXT).** A free-text note like *"responds to
caffeine"* is a treatment-response = a DIRECTIONALITY signal → a negative-sign **censor** (rules a
mechanism in or out). **FIRST verify `docs/SYSTEM_DESIGN.md §7`** as the primary source for the exact
semantics (memory says "negative-sign censor" — confirm). Design fork to surface Socratically: does a
note map to (i) a censor event (`Event` with `sign<0`, entering `active_censors`/the elimination), or
(ii) an operator hypothesis (PREFER-only)? A treatment-response that *rules out* a pathway is a censor
(REQUIRE); a "these are connected" note is a hypothesis (PREFER). Likely needs a drug→target reference
(the hardest sub-part — may defer the drug-mapping, do the directionality mechanic first). Pure decision
to extract + pin; wire into `read_person`'s `notes` param + `drive`.

**B. Input layer increment 4 — the clean-etiology cassette.** A diagnosis with a KNOWN clean mechanism →
a pre-built form/cassette directly (the degenerate "(2)-lite" efficiency case). Rohan's words: *"a nice
little efficiency hack, not the core system design"* — SECONDARY. A cassette is a canonical
(events/positions) bundle a clean-etiology diagnosis resolves to without the full search. Grounding =
canonical-gene + fungibility (option 2, blessed), NOT hand-enumerated subtypes (REFUSED — combinatorial,
unknowable).

**C. incr.3c — GWAS relevance-SEEDING.** Deferred here on purpose (it was an orphan without a generate-
wide consumer; `read_person` is now that consumer). The `trait_wiring` pleiotropy COUNT (a gene's
distinct-trait count = a bridge-prior) ORDERS generation *within* the subspace — a **SEARCH-ORDER PRIOR
ONLY, never significance** (Law 1's one sanctioned use of a population statistic). Small: order the
candidates/clusters by pleiotropy; κ still does significance.

**D. The LOOP (call-and-response ergonomics).** `read_person` is ONE turn. Build the loop: the read's
`completeness.i_solve` (the Jeeves node) is the machine's ask → the operator measures it → it becomes a
new lab → `read_person` again → until SETTLED (RESOLVED / certified-⊥ / non-DEGENERATE abstain, or the
operator declines). Likely a thin `converse`/`resolve_iteratively` helper + a rendering of the DO-THIS.

**E. The greenfield-workflow BASELINE (the theory-validation ORACLE — Rohan's headline ask).** A few
realistic user workflows → `read_person` → the read. Ideally **Rohan's OWN profile (ADHD/AuDHD,
multimodal) resolving to the ADHD read** = the functional-validation oracle + the baseline to assess the
recommendation engine against. **CARDINAL PRIVACY: NEVER commit anything derived from
`~/MentalAtlas/biodata`** (personal genetics/clinical/neuroimaging; SDIS = Rohan's dopaminergic
hypothesis). Scratchpad / in-conversation ONLY.

**F. A rendering of `DriverRead`.** The read is computed but never surfaced to a human. No CLI/render
exists (`__init__.py` exports only `__version__`; `drive`/`read_person` are reachable only from tests).
This is the other half of the call-and-response surface.

**G. Prune the parked orphans.** `driver.rank_candidates`, `driver.proximity_coherence`,
`web.node_convergence` = the OLD gene-ranking PREFER path (the subject-fallacy), now dead (tests-only),
superseded by the story-read + resolve. Removal candidates — verify with `find_referencing_symbols`
(production callers = 0) before deleting.

**H. The blind LRRK2 acceptance control.** Recover LRRK2–NOD2–RIPK2 as coherence, blind (≥2 networks +
Regenesis) — the end-to-end proof that "each part proven + the whole runs" becomes "the whole recovers a
mechanism it was not told." This is the ultimate validation (canon §13.3).

**Recommended order:** A (notes) → C (GWAS seeding, trivial once A's in) → E (the greenfield oracle, the
payoff) → D+F (the loop + rendering, the interface surface) → B (cassette) → G (prune) → H (blind control).
Confirm the order with Rohan; lead each new piece with a Socratic design fork.

---

## 6. Immediate next action

Start **task A (notes → directionality)**: (1) `Read docs/SYSTEM_DESIGN.md` and find §7 to VERIFY the
treatment-response/negative-sign-censor semantics from the primary source; (2) surface the one design fork
(note → censor vs hypothesis, and how to handle the drug→target mapping) with a lean; (3) on Rohan's
adjudication, build the pure decision + pin it (READ the residual) + wire the `notes` param into
`read_person`. Then push when Rohan authorizes (currently 2 unpushed).

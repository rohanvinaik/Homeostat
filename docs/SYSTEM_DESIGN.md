# Homeostat — Full System Design: the OTP-native, two-sign etiology engine

**Author of record:** Rohan Vinaik · **Status:** Settled system design, 2026-09-01, worked through end to
end with the founder. Self-contained; written to be reconstructed cold.

**Voice (SSL):** measured; humble is stronger. This document does not invent an information theory — it
recognizes that biology already computes one, and specifies an instrument that reads the projection biology
already stores. *"I'm using what my betters built — including a four-billion-year-old one — and giving it the
fuel line and telling it what to look at."*

---

## 0. What this supersedes, and what it does not

- **Supersedes:** the two-engine ambiguity in `THEORY_OF_THE_CASE.md` (top line: *"grows its own mechanism
  graph by node birth/death"*) and canon `REGULATORY_DEFICIT_PROGRAM.md` §3.4's *"node birth = induction on
  a cross-population dyad."* That is **Engine A — retired.** See §3. There is one engine, and it does not
  birth nodes.
- **Does not supersede:** the canon's formal substrate (§4 σ, §5 κ, §6 the oracle) or the pathology record
  (§15, the recorded death). Those are carried forward unchanged. Where this document and the canon disagree
  on the *method's shape*, this document governs, per the founder's 2026-09-01 statements; where they disagree
  on a *proved theorem*, the theorem governs.
- **Action item this creates (not executed here):** `THEORY_OF_THE_CASE.md` Part II and the canon's §3.4
  carry the retired Engine-A framing and should be reconciled to this document.

---

## 1. The one-paragraph version

A disease is a **shadow**: a coherent state that many weak, sub-threshold signals *cast in concert*, stored
in no single one of them, materialized on demand and de-materialized when the coupling tips. Homeostat reads
that shadow for **one person, zero-time**, over a **fixed, bounded web of known regulatory mechanisms** whose
node-roles and couplings are *prior* (proven biology, extracted once — never learned from the person). The
person's presentation is a set of **signed-ternary deviations off their own mined baseline**; the mechanism is
the survivor of **two-sign elimination** — positive candidate-elimination (what could cast this shadow) and
negative censors (what is ruled out); "no disease" is a **certified ⊥ with a proof**, not a failed search. The
engine works because biology is *already* an Orthogonal Ternary Projection geometry — gene roles are
physically-orthogonal projection axes — so the instrument is OTP-native on an OTP-native substrate.

---

## 2. The recognition: a disease is a shadow (the shadow-MCP identity)

A disease mechanism and a "shadow MCP" (`New_Work/shadow_mcps_position.md`) are the **same object**, not an
analogy:

- **Sub-threshold signals = individually-useless platonic tools.** Each is below threshold — exactly what a
  single-variant test correctly reports as "nothing here."
- **The disease = the shadow they cast together.** Real, but encoded in no component. *"Materialized on demand,
  not stored as a feature"* = the meta-stable state that holds while the coupling is intact and tips when it
  shifts (canon §2.2/§2.4).
- **"Convergence as meaning; partial states are honestly partial"** = the informational zero + the σ_sem > 0
  guard. Until the parts converge, the engine says *partial*; it does not fabricate the shadow.

This is *why statistics is blind by construction*: a shadow is invisible to single-tool inspection — you cannot
find it by examining light sources one at a time, at any sample size. The blindness is structural, not a power
problem.

## 3. One engine, not two — Engine A is retired

- **Engine A (retired):** a research engine that *grows* a mechanism graph by inducing new nodes from
  cross-population residuals. This is the population-statistics reflex wearing Peitho's clothes, and it is the
  mistake. Killed by the founder, 2026-09-01.
- **Engine B (the engine):** a **clinical** engine. It reads *one* person, *zero-time*, over a **prior** web.
  It does not learn the wiring from them (you cannot fit a wiring diagram to a single snapshot). The web —
  which regulatory things couple to which — is prior structure: proven biology, extracted once (§11). What is
  per-person is the **deviations** that propagate through it.

Population data, cross-source convergence, and the oracle ensemble belong to **downstream validation** (does a
per-person read generalize?), never to the per-person read. Treating them as the method is the drift that keeps
burying the engine (canon §0 Warning 2).

## 4. The substrate is already an OTP geometry (why any of this works)

The load-bearing recognition, and the reason §§5–7 all resolve on one fact. Biology is not something we impose
a data geometry on; **biology is an Orthogonal Ternary Projection code, and the engine is OTP-native**
(`AI:HDC/ORTHOGONAL_TERNARY_PROJECTION_THEORY_PART2.md`).

- **DNA is the base-2² OTP code.** The OTP paper's founding example: {A,T,G,C} decomposes into two orthogonal
  ternary dimensions — AT-vs-GC (A=+1,T=−1,G=0,C=0) and purine-vs-pyrimidine (G=+1,C=−1,A=0,T=0). The zeros are
  not absence; they are *"positive information through exclusion."*
- **Gene roles are physically-orthogonal projection axes.** A membrane transporter and a DNA polymerase are
  mutually exclusive *by physics* — they fold and stay stable in different electrochemical environments and
  cannot co-localize. In OTP terms they are **orthogonal**: each is transparent to the other's dimension. That
  transparency **is** the informational zero, and the informational zero **is** the negative-sign censor (§5).
- **DNA repair is multi-lens holography in molecules.** Proofreading/mismatch repair does not store a backup
  base; it reads the **complementary strand** — an orthogonal projection of the same information — and
  reconstructs the survivor. Two lossy views combining into a truth neither holds alone: the founder's
  holographic principle, running as a polymerase. Orthogonal projection is how biology fights the second law
  locally.

So the instrument reads the projection biology already computes, in the alphabet biology already writes in.
This is the mechanistic ground for §§5–7.

## 5. Two-sign specification — the disease "or lack thereof" (NEGATIVE_SPECIFICATION)

σ = teaching dimension, and **teaching dimension is defined over labeled examples of BOTH signs** {+,−}.
Every candidate-elimination is a *positive* policy μ ("this variant is distinguishable from P"). That is one
sign. The negative sign μ⁻ is a **censor** — a non-example, an output no correct instance of the concept may
produce. Two structural facts (NEGATIVE_SPECIFICATION §5, §10):

- **The channels are information-theoretically isolated.** You cannot recover "this is not disease X, and here
  is the proof" from any amount of positive-channel evidence. The negative sign is non-redundant.
- **Certified non-membership (typed ⊥) is a primitive the positive channel lacks.** "No disease here" is not a
  failed search (positive channel empty); it is a **positive certificate on the negative sign** — a proof that
  this presentation has no lawful mechanism. Medicine is *half-signed*: "you meet 8/10 criteria" is pure
  positive channel, and the entire negative sign (the isolated, non-recoverable half) is absent from its
  instrument.

**Where the negative sign comes from — for free, from the OTP substrate.** Physics-orthogonal exclusions
(different folding environment, no co-localization) are censors with **zero abstention tax** — a geometric
orthogonality is never a wrong guess. Softer category exclusions (incomplete annotation) carry the tax,
handled by the informational zero firing *"diagnostic — needs a finer lens."* So the negative oracle is
**tiered**: physics-orthogonal (free, absolute, the majority) + category-soft (abstention-taxed). The
crown-jewel evidence — treatment-response ("one drug resolved several symptoms") — is itself a **negative-sign**
observation: it *rules out* every mechanism where the drug's target is not upstream of the resolved symptoms.

A disease phenotype is therefore the two-sign object **σ(P, μ ∪ μ⁻)**, and completeness is measured over both.

## 6. Non-idempotence, made exact — the composition gap γ = the bridges

The phenotype construction is definitionally non-idempotent, and the math is the composition gap
(Specification-Complexity Thm 3.15; NEGATIVE_SPECIFICATION §10; Significance-Weighting §13):

$$\sigma(A \circ B) \le \sigma(A) + \sigma(B) + \gamma(A,B), \quad \gamma > 0 \text{ at bridges.}$$

The construction splits into two regimes:

- **Idempotent part = the bulk.** Redundant, submodular, κ = 0 marginal coverage → safe to forget with proof.
  Lose a bulk part, the shadow re-casts. `f(A ∪ {redundant}) = f(A)`.
- **Non-idempotent part = the bridges.** γ > 0, super-additive: the pleiotropic connector joining two clusters
  that were separately cheap and jointly expensive. `f∘f ≠ f` here.

This is the rigorous form of *"differential phenotype from 9, 8, 7 parts."* **It is never the count.** Two
people each missing "1 of 10 parts" present differently if one lost redundant bulk (mild) and the other lost a
bridge (a subsystem detaches, change in kind). **Completeness is scored by κ-coverage of the shadow, never by
fraction-of-parts** — counting criteria is the frequency proxy in its most clinical-looking disguise, and it
is exactly blind to γ.

**d is bounded — deterministically.** d (the supermodular degree, the number of bridges) is bounded by the
**proven semantic-category structure of gene function** (GO/Reactome/Pfam/EC — established, incomplete-but-not-
*wrong* biology). Most genes are single-category → single-cluster → not bridges; a bridge is the rare
multi-category gene (LRRK2: kinase *and* immune regulator *and* mitochondrial). So d = |multi-category genes|,
bounded by biochemistry, not a free parameter — and d small means the problem is not merely tractable but
**focused**: the mechanism concentrates in the few bridges, exactly where the disease lives (§5.8), which is
where you can afford to look hard. The bounded-bridge greedy guarantee (§5.7) is a conjecture in general; its
antecedent (d bounded) *holds in this domain by the nature of gene function*, and d is measured on the real
derivation graph, never assumed.

## 7. Directionality is a negative-sign censor-shadow (Bellman-Ford, free and safe)

An arrow is **not** a positive assertion ("X drives Y") — which, if wrong, is *destruction* (an unrecoverable
false elimination in eliminate-to-survivor). An arrow is a **censor**: "Y does not drive X," negative-sign.

- **You never guess an arrow.** Direction is the *residue* of accumulated censors: T→A is what "no mechanism
  with A upstream of T survived the treatment-response" leaves standing. Computed, never imposed.
- **A censor from a real observation cannot be a wrong guess.** So the destruction risk was an artifact of the
  positive framing.
- **The channels are isolated (§5), so the directed overlay never corrupts the safe undirected base.** You get
  the **Bellman-Ford bidirectional-descent speedup of a directed graph without the destruction risk of a
  directed graph** — the two live in orthogonal channels. Undirected co-movement is the safe positive base;
  direction is a negative-channel overlay that buys search efficiency, never correctness.

## 8. The metric / dynamics / significance / exact-learning stack

- **Metric — σ, two-sign, a Blum measure.** σ(P, μ ∪ μ⁻) = minimum constraints to pin a unique mechanism
  (SC=1), equal to the teaching dimension. *Not* a frequency. Coherence = minimum-σ, structure-resolved.
- **Dynamics — the σ-trajectory (SSL).** Understanding is driving H = log₂|surviving candidate mechanisms| → 0
  by candidate-elimination; the mechanism is the trajectory's terminus, a point-read only its endpoint. The
  driver is **surprise** — the divergence between naive and context-constrained resolution (one quantity read
  three ways: `surprise_triple_identity`). *Learn at the residual: the informative constraint kills a rival,
  never confirms the leader.*
- **Significance — κ / the bracket (Significance-Weighting).** Rank the surviving shadow by *improbable-AND-
  coherent* (κ = marginal coverage over the derivation graph; the bracket [bᴺ, Cᴺ·N!] with the error bar =
  bracket width). A meta-stable coherent state is **not frequent by construction**, so a p-value measures the
  wrong quantity; κ measures the right one. **κ only over the mechanism-derivation graph, never a generic
  interactome** (canon §5.12 — a graph measure over the wrong graph is a statistic in disguise).
- **Exact-learning map — SSL completeness.** The Semantic Completeness Equation dH/dt = −(N + C(H)) gives, for
  the domain, (H₀, L, H*, I_solve, Completeness) — a measurable specification of "how much of this is solvable
  by structure vs must be taught." Medicine is a closed *artifact* (a mechanism's specification) inside an open
  *field* (biology); the theory claims the artifact (SSL §1.4c).
- **The one binding law — σ_sem > 0.** Never collapse to a single self-confirming mechanism (that IS SDIS:
  σ_sem = 0, 100% retrodiction, memorization not resolution). Keep plurality; a constraint that only confirms
  the leader has value zero. The dual guard (NEGATIVE_SPECIFICATION §7): the negative sign must not over-censor
  to a *false* ⊥. Halt at the **κ-knee** (pabkit; past it is memorizing the presentation).

## 9. The control-flow loop (Peitho: fixed nodes, discriminate by dimension)

A node in Peitho is **fixed at zero-time** — the roster is the bounded universe; Peitho never *births* a node
(*"a node absent from the data is absent here"*). What is computed is the **mined zero** and each node's
**signed-ternary position** off it; discrimination failure is repaired by **adding a dimension, never a model,
never a threshold** (`position.py::discriminates` — the Discrimination Guarantee). The clinical loop:

1. **Mine the person's zero.** Their own baseline per axis (median-of-active, not a population range) — the
   prakriti/vikriti step allopathy structurally lacks. *The data geometry has a baseline*, so a sub-threshold
   input is a small *positioned* deviation, not an invisible one; nothing must clear significance to be read.
2. **Position the presentation.** Each symptom / lab / vital / treatment-response → a signed-ternary deviation
   (+1/−1/0) off that zero, on its dimension. `0` = the informational zero (the axis abstains).
3. **Two-sign eliminate** over the fixed prior web: positive candidate-elimination (sources that could cast
   the shadow) ∧ negative censors (physics-orthogonal exclusions + treatment-response rulings).
4. **Discriminate.** Unique survivor → the mechanism to interrogate (+ its κ-load-bearing bridge). Plural
   survivors (signatures collide) → compute the single unmeasured dimension with the highest expected
   information gain and **ask for it** — *Jeeves mode is the "add a dimension" step made conversational*
   ("do you also have allergies? persistent tachycardia?"), choosing between "what would confirm?" (positive)
   and "what would rule out?" (negative) by whichever has higher EIG on the current survivor set.
5. **Halt** on a unique survivor, on a **certified ⊥** (no lawful mechanism — proven, not an empty search), or
   on honest abstention ("cannot separate X from Y without measuring Z, which you don't have").

## 10. Fungibility falls out; roles fire by semantic class on physically-real centroids

Fungibility — gene X here, gene Y there, same mechanism — is not a problem to solve; it is what the OTP
category geometry *hands you*: X and Y hitting +1 on the same orthogonal dimension are the same symbol *on that
channel*, whatever their token. This is Genesis **semantic-class firing** (the cardinal rule) moved from verbs
to genes: a role-Form fires on the **class centroid**, never the token — and the centroids are the *physically-
real projection axes* (folding environment, co-localization, chemistry), never hand-drawn to fit. Two genes
share a role when their relational signatures land in one centroid. Cross-population recovery is Regenesis
`common_frame([understand(pop_A), …])` returning the invariant role-structure the several filler-sets realized
— use Regenesis, do not rebuild it. The one residual — a gene's category-set is proven-but-*incomplete* — is
the room where **surprise** lives: the disease's non-canonical role-usage registers as surprise against the
proven baseline, and where a gene genuinely cannot be placed the informational zero abstains (non-recovery,
never a wrong category).

## 11. The data pipeline — the blocker, resolved into two halves

- **The web substrate (free, buildable now).** The prior web's node-roles, established mechanisms, and physics-
  orthogonal exclusions come from **UniProt / GO / Reactome / Pfam / EC** — curated, deterministic, wiki-shaped
  public data. Ingested by the existing **Genesis/SparseWiki mass-wiki pipeline** (confirm exact entry point at
  build); **`harmonizing`** (`Kaggle_Killer/competitions/harmonizing/src/symbolic_healing.py`) is already
  constraint-propagation over a biological-metadata fact table — repurpose it (strip the competition format,
  tweak the parser). **BLAST / NCBI** supply the fungibility layer (a founder-isolate gene filling a role is a
  homolog/paralog — what BLAST finds). *Bright line (the genus guard):* an edge enters only as **proven
  deterministic mechanism** (authored, category-defining, incomplete-but-not-wrong), never as a **computed
  association** (a frequency/enrichment — the forbidden statistic). This is the seam the `CONCEPTUAL_AUDIT`
  proved is slippery; the bright line is what keeps it shut.
- **The per-person dynamic (self-reported).** §12.4 named dynamics "the binding constraint," but that binds
  *population-scale validation*, not the per-person read. **Treatment-response is self-reported state-transition
  data** ("stimulants resolved my migraines" is a before/after), and the person carries their own longitudinal
  history (Jeeves-elicited). The clinical read gets its dynamical axis from the person; only cohort-scale
  generalization stays gated (Genes & Health, NCT04698291 — canon §13.5).

So the data blocker is downgraded from "binding on the program" to "a public-bioinformatics pipeline for the
web + the person's own history for the dynamics," with population validation the only genuinely gated piece.

## 12. Build state — what is built, what is next

**Built and pinned (2026-09-02, 149 tests green; every pure decision Detective-complete):**
- **The engine (resolve-narrow):** `search.eliminate_two_sign` + `constraint_disposition` (two-sign
  σ-elimination — positive constraints ∧ negative censors, certified-⊥); `position.py` (per-person
  signed-ternary off the mined zero + the Discrimination Guarantee); `jeeves.py` (the EIG discrimination-
  dimension selector); `clinic.read_presentation` (the end-to-end two-sign read); `ground.py` (the
  SymbolicSpellCheck front door); `web.py` / `otp.py` / `signal.py` (the substrate).
- **The encoding layer:** `event.py` — the L2 event contract (`Event`, now three-axis: `sign`
  support/censor, `verb` polarity+role-class, `mode` a peer κ-density marker; `couple_verdict` cross-network
  resolution; `events_to_web` positive; `events_to_censors` + `active_censors` role-scoped negative);
  `clinic.read_from_events` (the encode→resolve spine, end to end).
- **The FIRST renderer — regulatory, on SIGNOR:** `signor.py` (`parse_effect` decomposes SIGNOR's effect
  grammar into direction→verb `amplifies`/`inhibits` + mode `activity`/`abundance`/bare; **every edge
  `sign=+1`** — SIGNOR only asserts, so a real inhibition is `inhibits`/+1, never a censor); `signor_fetch.py`
  (the I/O shell: download/cache/sha256-pin/stream, hash-pinned in `REFERENCE_MANIFEST`). Verified E2E on the
  real 21 MB dump: 26,340 regulatory `Event`s → 19,026 couplings; the LRRK2–NOD2–RIPK2 axis is present.
- Engine A (the node-birth / target-pinning loops) is **retired in code**; the statistical genus is ripped.

**Next — the remaining renderers + the generate-wide half (§11; the founder's biology enters here):**
1. **The other per-network renderers (§11):** each renders its DB slice into `list[Event]` at its bright-line
   tier (Law 9) — evolutionary→BLAST (undirected homology/fungibility), structural/genotype-deep→Pfam/GO/
   AlphaFold, developmental & exposome→ordered narratives (Regenesis), metabolic-flux→pathway/flux,
   co-expression/binding→undirected mechanistic votes, trait-wiring→calibration prior. Founder-led: the verb
   vocabulary, source, and caching per network.
2. **Regenesis as the generate-wide half:** derive the implied candidate mechanisms + roles + trajectory
   from the multi-network event story, feeding the resolve-narrow engine.
3. **The LRRK2 positive control (canon §13.3):** recover the LRRK2–NOD2–RIPK2 shadow as coherence, blind —
   the first real-data acceptance test (needs ≥2 networks + Regenesis; the regulatory slice alone is not it).

Everything downstream of a renderer's `list[Event]` is built and pinned.

## 13. The laws (the discipline, mirrored)

1. **Data-geometry + classical AI, NOT statistics.** A frequency/enrichment/participation/p-value is at most a
   cheap search-order prior — never the method, the significance, or the object.
2. **One engine, clinical, n=1, zero-time, over a PRIOR web.** No node-birth. Engine A is retired.
3. **Two-sign, always.** σ(P, μ ∪ μ⁻); "no disease" is a certified ⊥ with a proof, never an empty search.
4. **Completeness is κ-coverage of the shadow, NEVER a count of criteria.** The count is blind to γ.
5. **Never guess a direction.** Direction is a negative-sign censor-shadow, earned from real observation
   (treatment-response most of all), never asserted (a wrong arrow is destruction).
6. **Per-individual baseline first (mined zero); discriminate by a NEW DIMENSION, never a model or threshold.**
7. **σ_sem > 0.** Keep plurality; never collapse to a self-confirming single mechanism (that is SDIS). The
   negative dual: never over-censor to a false ⊥. Halt at the κ-knee.
8. **Roles by semantic class on physically-real centroids** (folding/co-localization/chemistry), never token
   identity, never a learned embedding fit to the answer. Regenesis is the role engine — use it.
9. **The bright line for the web is THREE-TIER, set by how much a witness may assert.** (i) *Directed proven
   mechanism* (regulatory/SIGNOR) — object-eligible, EARNS direction. (ii) *Undirected mechanistic vote*
   (co-expression, physical binding) — object-eligible for a coupling's EXISTENCE, never its direction;
   promiscuous hubs killed by the specificity censor. (iii) *Calibration prior* (trait-wiring/GWAS) — a
   node-weight, NOT an edge. Forbidden across all three: a computed association as the *object of the verdict*
   (co-expression frequency AS significance, a correlation drawn as an arrow). Significance is κ, never a
   vote's own frequency; incomplete-but-not-wrong is legitimate, a statistic-as-object is not.
10. **Abstention is load-bearing.** Category incompleteness → informational zero → non-recovery, never a wrong
    placement (SymbolicSpellCheck). The data gates the *validation* claim, not the per-person read.
11. **Reads a FROZEN world; touches NO creativity.** The engine reads the zero-time crystallization of
    biology — where both arbitrary (intentional) and structured (evolutionary/regulatory) creativity are
    already frozen into static structure — and reconstructs none of the process that produced it. It imposes
    no prior it did not extract, fits no dynamics it cannot observe, admits no homunculus. This refusal IS the
    guarantee: only a read that adds nothing of its own reflects the biology rather than the reader. κ is an
    endogenous oracle (a theory of *reading*, not creating), which is exactly why it fits a frozen capture.

## 14. Primary sources (read these, not this summary)

- **σ / two-sign:** `Specification_Complexity_Paper/specification_complexity_paper.md`;
  `Detective/docs/theory/NEGATIVE_SPECIFICATION.md` (μ⁻, channel isolation §5, γ/bridges §10, certified ⊥).
- **Construction dynamics:** `Semantic_Specification_Learning/01_PAPER_SKELETON.md` (σ-trajectory, the
  Completeness Equation §2.5, surprise §3, the σ_sem>0 guard §4.3).
- **Significance:** `Regenesis/docs/SIGNIFICANCE_WEIGHTING.md` (κ, the bracket, bulk/tail, submodularity-fails-
  at-bridges §13).
- **The OTP substrate:** `AI:HDC/ORTHOGONAL_TERNARY_PROJECTION_THEORY_PART2.md` (informational zeros, the
  {A,T,G,C} base-2² decomposition, the light-filter/lens intuition, genomic encoding §13).
- **The shadow identity:** `New_Work/shadow_mcps_position.md`.
- **The node model / decision shell:** `Peitho` (`network.py`, `position.py` — fixed nodes, mined zero,
  signed-ternary, the Discrimination Guarantee).
- **The role engine:** Regenesis (`mcp__Regenesis__*`); the biological-metadata instrument precedent:
  `harmonizing/src/symbolic_healing.py`.
- **The canon and its pathology record:** `docs/REGULATORY_DEFICIT_PROGRAM.md` (§4 σ, §5 κ, §6 oracle, §15 the
  recorded death); the corrected-conception companion `docs/THEORY_OF_THE_CASE.md`; the build spec
  `docs/ETIOLOGY_ENGINE.md`; the Serena-traced `docs/CONCEPTUAL_AUDIT.md`.

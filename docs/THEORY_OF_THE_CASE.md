# Theory of the Case — Homeostat

**Homeostat is a mechanism-unearthing engine: it imputes the causal mechanism under a symptom
presentation — the combination of weak, fungible, sub-threshold signals holding a coherent state —
by a Peitho-style parsimony search that grows its own mechanism graph (node birth/death) and reads
candidates by convergence across many lossy lenses (a holographic projection). Data geometry and
classical AI, not statistics.** (The medicine critique below and the σ/κ formalism are the
motivation and the scaffolding; the build is the search.)

**Status:** Canonical derived design, REWRITTEN 2026-08-30 across a working-through with the founder.
The arc of that day: rewrite 1 established "data-geometry, not statistics"; rewrite 2 sharpened *why*
statistics fails (power, not bias — a fungible, sub-threshold, coherence-borne etiology); and this
final pass encodes the **confirmed method architecture** — Homeostat is **Peitho with automated node
birth/death**, the search is the founder's **σ-trajectory** (Specification Complexity), the
**coherence measure is σ** (a Blum measure, not a statistic), the **σ_sem > 0 falsifiability guard**
is what keeps it from collapsing into SDIS-style memorization, and **early stopping at the κ-knee**
(pabkit) is the parsimony halt. Part II is that architecture. The founding canon is
`docs/REGULATORY_DEFICIT_PROGRAM.md` (authoritative). This document is the *instantiation*: the
corrected conception, the confirmed method, the pathology record, and the two things still open (the
object's computed content, and the data). The build proceeds from here WITH the founder.

**Supremacy clause.** DERIVED. Where silent, ambiguous, or wrong, canon governs, in order:
(1) the founder's statements; (2) `docs/REGULATORY_DEFICIT_PROGRAM.md`; (3) the sources pinned
in `docs/REFERENCE_MANIFEST.yaml`. The portfolio data-geometry reference is
`~/Projects/Kaggle_Killer/DATA_GEOMETRY_ARCHITECTURE.md` (OTP, Informational Zero, COEC, GSE,
HDC). The mechanism this project reuses is spread across the founder's built projects — those
are named in Part II and are primary sources, not this summary.

**What is confirmed, and what is still open — named up front so it is not blurred.** The *method
architecture* is confirmed (Part II): a σ-trajectory search over an automatically-grown mechanism
graph, driven by data-geometry constraints, guarded by σ_sem > 0, halted at the κ-knee. What remains
open is (a) the object's **content** — the mechanism graph is *computed by the search*, not authored,
so it is grown, not written, and seeding it from guesses (including SDIS's) is the drift the founder
corrected; and (b) the **data** — the population co-variation and symptom co-presentation geometries
the search runs over (§12.4). The founder's **SDIS** document is now in hand as a *characterization
target* (recover its defensible core, reject its overfit — from the data), never as the object.

---

## Part I — The Case (the conception, corrected)

**The clinical claim (canon §1).** Allopathic medicine scores you against a *population* average;
it has no step that establishes *your own* baseline first. For **regulatory** disease — a control
dial set slightly wrong — the entire signal IS the deviation from your own setpoint, so these
conditions are structurally invisible and get filed idiopathic / functional / medically
unexplained. (For *lesional* disease — a tumor — the baseline does not matter; a discontinuity in
kind is detectable against anything.)

**Why standard genetics cannot see it — and the correction that matters.** The phenotype is
produced by a *combination* of sub-threshold signals. Control over any regulatory/flux pathway is
distributed (metabolic-control summation theorem); most heritability is in the long sub-threshold
tail (omnigenic). So the effect **does not exist at any single locus — it exists only in the
composition.**

The correction (founder, 2026-08-30): **statistics is not the villain, and it is not biased. It
is priorless, and priorless is honest — it looks for significance without deciding in advance what
it wants to find.** The problem is that it is **too weak** to pull a mechanism out of the noise
when the etiology has this exact shape:

- the contributing elements are only **weakly associated** individually, and
- they are **fungible** — no single one is necessary; a different-but-equivalent element can stand
  in for it in a given individual, so each element looks weak-or-absent on its own, while the
  mechanism is present in all of them, and
- the mechanism itself exists as a **meta-stable state of coherence** among those elements: a
  collectively locked state that holds until enough of the coupling shifts and it tips.

An element-by-element association test is *structurally blind* to this, no matter how much data
you feed it, because the thing it is testing (the element) is not where the mechanism lives. The
mechanism is one level up, in the collective state the elements hold together. This is not an
underpowered version of the right method; it is the wrong level of description.

**The enemy the project exists to defeat.** For ADHD, the dopamine-synthesis and uptake genes
light up every statistic; everyone has already found them. The problem is that those **loud
signals become the noise that drowns out the other etiologies** — the ones that only matter in
combination, the ones shared with autism (AuDHD), the ones that never clear a threshold alone. The
goal is to stop letting the loud, obvious signal hide the quiet, coherent one. (No "initiation vs.
resolution / switch-off" axis is assumed anywhere — that framing was never the founder's and is
dropped. Initiation is as worth studying as anything else; there is no privileged axis.)

**Diagnosis is a story (Winston) — and the honest split.** The allopathic *diagnosis* is a
post-hoc, motivated, meaning-imposing stage — a *story* laid over the data — treated as a necessary
prior when it is not. That story-imposition, and the motivated reasoning of imperfect
practitioners, is the part that is "directional." The **statistical significance engine underneath
is not** — it is priorless and honest, just too weak (above). Keep the two separate: the critique
is of the diagnosis-as-prior and of underpowered element-testing, not of statistics being
dishonest. The engine for meaning-as-story is Regenesis (Winston's Genesis, ported).

**Ayurveda is a decorrelated carving-source, never an authority (canon §6).** Not "traditional
good, allopathic bad." A systematic tradition is a **battle-tested empirical system that has been
groping at these combinatorial mechanisms by construction** — centuries of raw outcome-feedback,
precisely because it never had the loud single-gene story to lean on. Its *explanations* are wrong
("heat," "spirits," "energy") and that does not matter, because its *carvings* — how it groups what
combines with what — are **candidate constraints** on which sub-threshold things lock together,
causally independent of the statistical-diagnostic frame that produced the partitions under test.
Unani (Galenic → allopathic ancestor) enters at zero weight, as the negative control. Convergence
across lineages that never touched is signal; convergence within a lineage is shared descent.

---

## Part II — The Method: the confirmed architecture (σ-trajectory search with node birth/death)

> Confirmed with the founder 2026-08-30. The *architecture* is settled and encoded below. Two things
> remain genuinely open and are marked as such: the object's **content** (which is computed by the
> search, not authored — that is the whole point) and the **data** that feeds it (§12.4). Build the
> architecture; do not fabricate the object content and do not assume the data exists.

### It is Peitho, with one addition

Peitho searches a *limited state space* for the most parsimonious configuration that reaches a
defined goal state, and reads it with a signed-ternary decision core (mined zero, informational-zero
abstention, elimination, discrimination by a new orthogonal dimension). Homeostat is the same
machine, with the goal state being **a parsimonious mechanistic etiology for a complex symptom
presentation**. The one piece Peitho did not need is **automated node birth and death**: Peitho
knows its state space ahead of time (its stores and SKUs); Homeostat does not know the shape of the
mechanism, so the search must *grow and prune the state space itself*.

### The search is the σ-trajectory (SSL / Specification Complexity — the founder's own theory)

Understanding a presentation is driving its conceptual entropy to zero under constraint:
- Let **H = log₂(number of candidate mechanisms still consistent with the evidence)**. A *surviving
  candidate* is a mechanism the evidence has not yet ruled out — an unresolved degree of freedom
  (a "surviving mutant").
- Each constraint from the **data geometry** is a *test* that kills candidate mechanisms: a
  **population co-variation** (sub-threshold signals that lock together across genomes) and a
  **symptom co-presentation** (symptoms that cluster together across people). The mechanism is where
  the two geometries *lock*. This is candidate-elimination — the constraints come from the data,
  never from a hand-authored edge list.
- The etiology is the *terminus* of the trajectory: the mechanism reading left standing once the
  constraints have peeled the rivals off.

### The coherence measure is σ — a Blum measure, not a statistic (the load-bearing resolution)

σ = the minimum number of data-geometry constraints needed to pin a *unique* mechanism (SC = 1). It
is the founder's specification complexity: a Blum measure, provably equal to the teaching dimension
and four further studied quantities (the Five-Field Identification), and **independent of frequency
by construction**. It is the opposite of "gene X in 87% of cases." The **bulk/tail phase transition
is the collective-state signal** earlier gestured at as an "order parameter": candidate mechanisms
die in correlated clusters (the *bulk* — structure resolving many at once) until each remaining rival
needs its own targeted constraint (the *tail* — PAC-limited, must be taught). A *parsimonious,
coherent* mechanism is one that reaches SC = 1 in the bulk. That is the coherence: minimum-σ,
structure-resolved.

### Node birth and death — the novel piece — is induction + negative learning (already built: SSL, Regenesis IV-G)

- **Birth (induction).** A residual — co-variation or symptom co-presentation the current mechanism
  graph does not account for — *births* a node: a recurring cross-population dyad posits a mechanism
  component (SSL induction / the m2 confidence-accrual mechanism).
- **Death (negative learning).** A candidate node that meets a **near-miss** — a population where the
  coupling fails, a presentation that breaks it — is *withdrawn before it fires*
  (withdraw-on-"does-not"). You learn at the **residual**: the informative constraint is the one that
  KILLS a rival, never the one that confirms the leader (Winston's near-miss).
- **Consolidation (safe forgetting).** A node banking zero marginal coverage (κ = 0) is redundant and
  can be forgotten *with proof* it changed no significance-weighted survivor (canon §5.11).

### The one law that keeps this from becoming SDIS — the falsifiability guard

A frame that makes every observation *confirm* it reports **σ_sem = 0**: zero information, Quixote
seeing giants — *memorization, not resolution* (canon §5.9; machine-checked as
`self_confirming_cannot_certify`). **SDIS's "31/31 symptoms predicted, 100% accuracy" is σ_sem = 0
by construction** — the dopamine frame was allowed to overwrite every reading rather than be
breakable by one. So the search's binding law is:
- **σ_sem must stay > 0.** The search may NOT collapse to a single self-confirming mechanism; more
  than one lawful mechanism-reading must survive the leading frame (plurality = regime-multiplicity,
  H3 — plural but not mushy).
- **Learn at the residual, never at the confirmation.** A constraint whose every outcome leaves the
  leading mechanism unchanged has value zero by construction (Howard's value-of-information).

This is the exact, formal statement of *why SDIS is wrong* and *what the machine must do
differently*.

### Early stopping is the parsimony halt (pabkit — Process-Aware Benchmarking)

Judge the *process*, not the endpoint. Grow the node graph while κ is high (the bulk is still
amplifying — structure resolving rivals for free); **stop at the knee where κ → 0.** Past the knee,
each new node resolves only one tail rival — the search is *memorizing the presentation*, i.e.
becoming SDIS. pabkit's "halt at the test-loss minimum" is that knee, and it is the overfitting guard
for small-n: the search's own trajectory (structured, stable rule-formation vs. abrupt memorization)
tells you which regime you are in. κ → 0 is the stopping rule (canon §5.5, §10.4).

### The decision shell is Peitho, and it is built

Signals reach the search as tiered, signed-ternary positions off a per-individual mined zero, the
informational zero carrying honest abstention. Built and Detective-pinned this session: `otp.py`
(the ternary / informational-zero projection) and `signal.py` (the ✓/○/absent tiering). Decisions
are elimination over those axes; discrimination is a new orthogonal dimension, never a tuned
threshold. The mined zero is canon §1.1's missing per-individual reference step (= prakriti/vikriti,
§6.7).

### Where the constraints come from — multi-lens triangulation (the co-occurrence geometry)

The kill-matrix the search runs over is **not read off any single source** — least of all a fixed,
pre-drawn network. (STRING participation over the generic interactome was the Act-2 death: a map with
no person and no phenotype in it, whose *shape* is the same whatever data you feed it, so reading its
hubs told you about the drawing, not the biology.) Instead each data-geometry constraint is
**triangulated across several partially-orthogonal free lenses**, each a lossy shadow of the lock we
cannot buy (the gated genotype×phenotype cohort):

- variants that **co-travel across populations** (gnomAD / 1000G),
- each **wiring to the presentation's traits** (the GWAS catalog),
- genes that **co-move in expression** across people (GTEx),
- and — allowed but demoted to one vote among many — physical/functional interaction (STRING).

A candidate mechanism survives only where **independent lenses converge**, and is killed the moment
they disagree (the near-miss — learn at the residual). This is the founder's holographic principle and
canon §6.9: convergence across sources that never touched is signal; one source alone is not. STRING
is not banned — it is one lossy witness that cannot drown anything, because a hub only it likes gets
outvoted and eliminated.

**Why imperfect orthogonality is fine — the load-bearing distinction: we GENERATE, not CALCULATE.**
The lenses need not be independent, only *somewhat* orthogonal. In a statistical stack this would be
fatal — correlated inputs → correlated errors → false confidence (a tight estimate that is
systematically wrong; how the old arc died). But the search computes no number to trust; it
**eliminates rivals**. A lens is a *kill-opportunity*, not an estimator. Two partly-overlapping lenses
sometimes kill the same rival — *redundant*, never *wrong*; there is no estimate to bias.
Information-theoretically, partial orthogonality yields **between n and 2n bits (non-inclusive)** —
strictly more than any one lens, always net-additive. So imperfect orthogonality is fine here and
fatal in a stat stack, and that difference *is* generate-vs-calculate.

**The engine already embodies this.** κ (`search.marginal_kill`) is *marginal* coverage — it counts
only the rivals a lens kills that were not already dead — so overlapping lenses do not double-count;
redundancy shows up as κ = 0 (a wasted, ignored kill), never as inflated confidence. And greedy max-κ
selection reaches for the **most orthogonal** next lens each step (the one that kills the most *new*
rivals). "Don't pick heavily-overlapping lenses" is therefore not a rule to enforce by hand — the
search prefers orthogonal lenses by construction and shrugs off the overlap.

### The generalization (2026-08-31): the partition is a free variable, and the unit is the ROLE — not the gene

Worked out with the founder 2026-08-31; the deepest statement of the design. The SA-vs-EUR contrast
that seeded the population lens was **the coarsest, lowest-resolution filter available** — a motivating
example (the founder's n=1 irritation), never the architecture. Two coupled generalizations replace it.

**(1) The partition is searched, not fixed.** A population lens is not "South Asian vs European." It is
*differentiation across **any legitimately-isolatable group*** — ancestry at any zoom (continent →
sub-continent → a single founder/caste isolate), a phenotypic sub-section (has-the-presentation vs not,
endemic-region vs not), an exposure — anything genuinely distinguishable. The read is **differentiation
magnitude, direction-free** (e.g. max pairwise Fst across the groups), never a hardcoded axis or a
`SAS>EUR` direction. The partition itself is a first-class *searched* dimension.

- **Why this is the right level — measured 2026-08-31.** The bare `SAS>EUR` binary is ~a coin flip (44%
  of variants "shift"), so it births junk (153/289 genes, 60% named-hub survival). Replacing it with
  differentiation across the five 1000G superpopulations (top-decile max-Fst via `pbs.hudson_fst`)
  restores specificity (86/289 born, 20% hub survival) and cleanly recovers **NOD2** (Fst 0.431, rank
  29/242) and **RIPK2** (Fst 0.453, rank 22) as strongly population-structured. **LRRK2 falls to rank
  143/242 (Fst 0.148) — robustly mid-pack, not a threshold casualty** — because its signal is *finer
  than a continent*: the SAS superpopulation average washes out the specific South-Asian founder signal
  the leprosy literature found in *Indian* cohorts. The lens is not failing LRRK2; it is correctly
  reporting that LRRK2's signal lives at a **finer partition** (sub-continental founder/caste groups).
  *The threshold was NOT lowered to force LRRK2 back — an honest mid-pack rank IS the finding.*
- **The discipline, one level up.** If the partition is free, the space of partitions is nearly
  unbounded (any subset of people is a "group"), and an engine allowed to carve any partition always
  finds one that "explains" anything — σ_sem = 0 self-confirmation, one level up. A partition is
  admissible only if **independently isolatable** (a real genetic cluster, a real phenotype, a real
  exposure), never carved to fit the answer. This is the §6 oracle discipline and the σ_sem > 0 guard,
  applied to the *partition*.

**(2) The unit of recognition is the ROLE, not the gene — fungibility across populations.** A causative
mechanism may be realized by gene-pool {X} in one population and a *different* pool {Y} in a founder/
caste isolate, while the **mechanism is the same** — the genes are just whatever that population's deck
had to fill the roles. A gene-identity lookup ("is *LRRK2* significant?") is a **token match** at the
wrong level; it will always miss the sub-population that solved the same problem with a different token.
The instrument must pull out **the genes filling each mechanistic *role*, whatever they are called
here** — recognizing a candidate by the **role it plays**, never its name.

- **This is semantic-class firing** (the Genesis/Regenesis cardinal rule) moved from verbs to genes: a
  frame fires on `shun/dodge/sidestep` because they hit one **class centroid**, never because a token
  matched; here LRRK2 and a different kinase in a founder isolate both fire the "amplify NOD2→RIP2
  signaling" role-class. **Never the token, always the class.**
- **A gene's "role" is its relational signature** — its position in the mechanism-derivation graph
  (what it couples to / activates / inhibits / co-varies with), not its name. This re-homes STRING/GTEx
  **correctly**: not the map whose hubs are the answer (the Act-2 death), but the **relational context
  that defines the roles**. Two genes share a role when their relational signatures land in one centroid.
- **The populations are the lossy lenses at the right level.** Each projects the mechanism onto *its*
  filler-set; combine the projections and you recover the **role-structure** — the holographic truth no
  single population's gene-list contains. The founder's "lossy lenses → holographic projection" now sits
  at the role layer.

**Regenesis IS the role engine — use it, do not rebuild it.** A pure-data-geometry role encoder is
buildable (σ + learning theory + significance-weighting), but Regenesis (the founder's ported Winston
Genesis, `mcp__Regenesis__*`) already does deterministic, provenance-carrying role recognition,
plug-a-domain, today. Stand up a **mechanism universe** whose semantic classes are mechanistic roles,
register the role-class anchors in the universe's `.index` trigger column (the one-step domain stand-up),
and the native stack fires roles over genes by class. The cross-population holographic combine becomes
Regenesis **deriving the role-structure** from the several lossy per-population filler-projections. σ
specifies the role-structure; κ scores it over the relational graph; the nodes are roles. **Deterministic
(GSE/HDC vector-symbolic binding), NEVER a learned embedding fit to the answer** — centroids come from
real relational geometry, the way a Genesis universe registers class anchors, never hand-drawn to fit.

**The meta-thesis (founder, 2026-08-31) — why the "woo-sounding" engine is the rigorous one.** Any
statistical approach — or a high-level read of macronutrients/vitals that ignores the other available
signals — is **inherently asserting an individual mechanism from population-scale statistics**. That
substitution is the error the whole program refuses, and **differential outcomes for the same clinical
presentation across populations are a clean ledger of its body count.** So the story-understanding engine
that would make a twitchy reviewer uncomfortable is, in fact, the **most conceptually and mathematically
rigorous, objective approach to medical practice, medical research, and individual/population
bioinformatics** — the one that does *not* silently impute the individual from the population. Homeostat
is the clean application domain demonstrating that "stories" are a **computable information-theoretic
principle** — entropy reduction through applied intent, beyond what the static data alone indicates —
not a very elaborate SparkNotes.

**Communication (Winston, the thesis applied to itself).** Reception *is* the story you tell. Lead the
paper in the vocabulary reviewers already trust — population differentiation, specification complexity,
significance-weighting — and let the Genesis/Winston machinery live, fully disclosed, in a deep methods
section. That is framing (ordering and emphasis), not hiding. The one guardrail: the narrative must be
one the instrument actually **computes out to** — σ_sem > 0 at the meta-level; the framing may not
retrodict a result the run did not produce.

### Primary sources (read these, not this summary)

The σ / trajectory / bulk-tail / σ_sem-guard machinery — the founder's **SSL paper**
(`Semantic_Specification_Learning/00_CONCEPTUAL_FRAMING`, `01_PAPER_SKELETON`) and its exact-learning
sibling (`06_EXACT_SPECIFICATION_LEARNING`), plus `SIGNIFICANCE_WEIGHTING.md` (κ). Early stopping /
process-not-endpoint — **pabkit** (`~/Projects/pabkit`, `docs/process_makes_perfect.md`,
`docs/mathematical_formalism.md`). The decision shell — **Peitho**. The constraint-elimination +
committee + OTP substrate — harmonizing, genomevault / orthogonal-validators, gse / HDC. The
constraint-trajectory vocabulary — **COEC**.

### What is STILL open (marked, so it is not quietly filled in)

1. **The object's CONTENT is computed, not authored — and it is not built yet.** The mechanism graph
   is *grown by the search* (node birth/death) from the data geometry; it is NOT a hand-written edge
   list, and seeding it from SDIS's guesses is the error the founder corrected. **SDIS is a
   characterization target** (can the search recover SDIS's defensible core and reject its overfit,
   from the data?), never the object.
2. **The data — resolved in principle, not yet built.** The gold (one dataset with each person's genes
   AND symptoms, so the phenotype visibly moves with the combination) is gated (§12.4). But we do NOT
   buy it: the kill-matrix is **triangulated from free shadows** (the multi-lens section above), and
   the `propose` hook is an **active-learning probe** — the search's own residual says *which* discriminating
   constraint to go fetch (argmax expected-information-gain, per the SSL active-learning frame), so
   acquisition is residual-driven, not a bulk download. What remains is to *build the lenses* (gnomAD
   co-travel, GWAS trait-wiring, GTEx co-expression, STRING-as-one-vote) and run them. First target: the
   LRRK2 positive control (§13.3) — where, measured 2026-08-30, every single-locus statistic (frequency,
   pleiotropy count, specificity) MISSES the mechanism (recovers HLA hubs, or demotes LRRK2 at hub-count
   36), because the mechanism is compositional. That is the thesis on real data, and the real test the
   multi-lens engine must pass.
3. **σ depends on μ — the oracle.** σ is only as good as the space of *alternative* mechanisms it is
   measured against (the mutation policy). This is canon §4.3 / §6, the oracle problem — and it is
   where the Ayurvedic / cross-tradition ensemble re-enters, NOT as edges to seed but as
   **μ-diversification**: independent ways of enumerating "what else could this mechanism be," so σ is
   not measured against a consensus-collapsed alternative set (§6.4, §6.9).

### The honest cautions (each measured on real data, not asserted)

- **Coherence is not automatically signal — build it on the right object and MEASURE it.** In
  TriageGeist, the one place a "Kuramoto coherence" layer was built and honestly ablated, it was
  inert-to-negative on the metric (the layer computes a confidence-weighted variance across banks,
  not a true order parameter, and its phase features were *benchmarked and removed*). Assuming
  coherence carries signal is the same error as assuming a statistic does.
- **The intelligence is in the correctness of the constraint graph, not an automated trick.**
  harmonizing *removed* three constraint rules that over-fired and collapsed real distinctions
  (Disease→Organ, Instrument→Fragmentation, CellType), and its single biggest gain came from
  cell-by-cell domain-expert curation. "Domain knowledge IS the algorithm." An over-general
  constraint that collapses distinctions is **removed, not tuned** — the same discipline as Peitho's
  "a collapsed signature is a missing dimension, not a mis-set threshold."
- **No ML as the method.** The gradient-boosted tails in the *competition* instantiations
  (TriageGeist's CatBoost/LightGBM) are founder-placed, metric-chasing Kaggle moves — not a template
  for Homeostat. This is classical AI. A bounded model is at most a founder-placed tail on some
  irreducible residual, never the method, never the default (see the DATA_GEOMETRY_ARCHITECTURE
  Architecture-Primacy banner).
- **The binding data constraint (canon §12.4).** Without dynamic / state-resolved measurement, every
  output is a *hypothesis*, not established mechanism. A meta-stable coherence is a dynamical state;
  static allele frequencies may not carry it at all. This caps what the static program can claim, and
  it is a data problem, not a method problem. Do not oversell a static-data result.

---

## Part III — What is kept vs. ripped out (the rebuild inventory)

The founder's assessment: the current design is almost a complete write-off. Honest inventory:

- **Keep (wiring / substrate):** the ingestion machinery (`eir_cohort.py`, `gnomad_pile.py`,
  resumable downloads, `HOMEOSTAT_TAG` cohort-namespacing), `pbs.py` (as a **search-order prior**
  only — it bounds which candidates enter, never the object, never the significance), the GRCh37
  reference data, and the lint/type/test/Detective discipline. `kappa.py` (the κ engine) is
  *potentially* keepable — but only re-homed onto the mechanism-derivation graph, never the generic
  interactome.
- **Rip out (statistics wearing the method's clothes):** the entire gate/validator layer that treated
  the PBS pile as the *object* and network participation / enrichment / pleiotropy as the
  *significance* — `bridge_discovery.py`, `lrrk2_gate.py`'s participation gate,
  `annotation_recovery*.py`, `eir_enrich*.py`, `pbs_restricted.py`, `sig_descent.py` as *methods*.
  They are the Part V pathology, preserved in git history, not the design.

The rebuild replaces the statistical method layer with the constraint-elimination coherence
instrument (Part II), on the kept substrate, **over an object designed with the founder**. That is the
post-this-document work.

---

## Part IV — The Laws (mirror of the auto-loaded CLAUDE.md)

1. **Data-geometry + classical AI, NOT statistics.** Statistics is priorless and honest but too weak
   for a fungible, sub-threshold, coherence-borne etiology; it is at most a cheap search-order prior,
   never the method, the significance, or the object.
2. **The method is a σ-trajectory search; the coherence measure is σ, a Blum measure — not a
   statistic.** Drive H = log₂(surviving candidate mechanisms) → 0 by candidate-elimination, the
   "tests" being data-geometry constraints: population **co-variation** + symptom **co-presentation**.
   σ = min constraints to a unique mechanism (SC = 1); it equals the teaching dimension, not a
   frequency. The **bulk/tail phase transition** is the collective-state / parsimony signal.
3. **The object (the mechanism graph) is GROWN, never authored.** Node **birth** = induction on a
   residual; node **death** = negative learning on a near-miss (kill rivals, learn at the residual);
   **consolidation** = safe-forget a κ = 0 node. Never a hand-written edge list, never seeded from
   guesses — including SDIS's. This is the one piece beyond Peitho.
4. **The falsifiability guard: σ_sem must stay > 0.** Never collapse to a single self-confirming
   mechanism — that IS SDIS (σ_sem = 0, 100% retrodiction, *memorization not resolution*). Keep
   plurality (regime-multiplicity, H3); a constraint that confirms the leader has value zero.
5. **Early stopping at the κ-knee is the parsimony halt.** Grow nodes while the bulk amplifies (κ
   high); stop at κ → 0. Past the knee is memorizing the presentation. Judge the *process*, not the
   endpoint (pabkit). This is the overfitting guard for small-n.
6. **Per-individual baseline first; the decision shell is Peitho.** Mine the person's own setpoint
   (mined zero = prakriti/vikriti), read signed-ternary deviation, abstain via the informational
   zero, decide by elimination, discriminate by a *new orthogonal dimension* — never a tuned threshold.
7. **Diagnosis is a story; the traditions are μ-diversification (the oracle), not edges to seed; the
   population/E-I-R signal is a search-order prior** — none is the method or an authority. σ is only as
   good as μ (the alternative-mechanism space); diversify the oracle (§6.4, §6.9).
8. **Abstention is load-bearing; no ML as the method; the data gates the claim.** The informational
   zero and σ_sem > 0 are load-bearing. A bounded model is at most a founder-placed tail. Without
   dynamic / co-variation / co-presentation data, outputs are hypotheses (canon §12.4).
9. **The partition is a free variable, legitimately-isolatable — not a hardcoded axis.** A population/
   phenotype lens is *differentiation across any independently-isolatable group* (ancestry at any
   resolution, a phenotypic sub-section, an exposure), read **direction-free** (magnitude, e.g. max
   pairwise Fst), never `SAS>EUR`. Partitions are *searched*; a partition carved to fit the answer is
   σ_sem = 0 one level up. SA-vs-EUR was the coarsest instance, not the architecture (measured
   2026-08-31: the bare binary is a 44% coin flip; differentiation restores specificity).
10. **Recognize ROLES, not genes (semantic class, never token); Regenesis is the role engine.** The
    mechanism is invariant; genes are population-local, *fungible* fillers. Pull out the genes filling
    each role by the *role they play* (relational signature → class centroid), never by gene-identity —
    Genesis **semantic-class firing** over genes, deterministic (GSE/HDC), never a learned embedding.
    Regenesis is the working engine: **use it, do not rebuild it.** STRING/GTEx are the role-defining
    relational context, never the map-as-answer (the Act-2 death).
11. **Statistics-or-thin-signal imputes the individual from the population; that is the error, and
    cross-population differential outcomes are its body count.** The story-understanding engine is the
    *most* rigorous, objective approach precisely because it refuses that substitution. Frame the paper
    in accepted vocabulary (methods discloses Genesis/Winston, fully); never let the framing outrun what
    the instrument computes (σ_sem > 0 at the meta-level).

---

## Part V — The Pathology Record (kept, and extended with this session's correction)

**The original death, in four acts — statistics substituted for data geometry.** The 2026-08-30
empirical arc tried, exhaustively and honestly (all preregistered, all committed), to make the
population signal do mechanism-recovery work — and every attempt was a *statistic*, on a generic
network, with no coherence-of-combination and no phenotype in the computation.

- **Act 1 — the object was a statistic.** The E/I/R "PBS pile" (a population-differentiation
  statistic) was treated as *the candidate object*. PBS is a search-order prior (§7), one input — not
  the object.
- **Act 2 — the "mechanism" was generic topology.** Variants were mapped to the universal human
  interactome (STRING ∪ GTEx) — a fixed map with no person, no phenotype — and "bridges" were read as
  community-**participation** (a topology statistic). The gnomAD-vs-Pan-UKBB replication proved it:
  swap the whole cohort and 98.7% of participation values are identical while PBS differs greatly —
  the passing gates were graph-topology, the population signal inert.
- **Act 3 — the validators were statistics.** §8.4 selection-**enrichment** FAILED under honest LD
  correction (p 0.0005 → 0.985); §3.2 used **pleiotropy count** (a frequency proxy) and "passed" only
  because it too measured the generic graph.
- **Act 4 — making the statistic load-bearing broke everything.** Restricting to the top of the PBS
  ranking made the population signal load-bearing but broke the gates (0/8 configs replicated); feeding
  PBS softly as a κ prior *demoted* the known bridges. Across four operationalizations, there is **no
  configuration where a statistic does the work AND the analysis holds.**

**This session's added diagnosis (the sharper version).** Three refinements the four acts did not yet
name:

1. **Statistics is not biased — it is underpowered for *this shape*.** The failure is not that
   statistics lies; it is that a fungible, sub-threshold, coherence-borne mechanism is invisible to
   element-by-element association at any sample size. Calling statistics "motivated" mislocated the
   fault; the motivated part is the *diagnosis-labeling* stage, not the significance engine.
2. **The coherence detector was mis-imagined as a graph statistic.** Act 2 (κ / participation over the
   generic interactome) *felt* like data geometry because it was a graph. It is not: reading the
   built portfolio shows the real coherence mechanism is **constraint elimination over a
   domain-knowledge graph** (harmonizing) plus **committee-collective abstention** (genomevault) — not
   coverage over a pre-existing network. A graph measure over the wrong graph is a statistic in
   disguise.
3. **The object is the unspecified work, and substituting a statistic for it is the drift.** Every
   past failure quietly *guessed* the object (the PBS pile, the generic interactome) instead of
   building the mechanistic constraint graph. The honest state is that the object is not yet specified;
   the fix is the design conversation and SDIS, never another statistic that fills the gap while
   looking like rigor.

**What survives as an honest static-data deliverable (do not oversell):** a rigorous, multi-cohort,
preregistered demonstration that statistics on static allele frequencies over a generic network cannot
recover regulatory mechanism (canon §12.4 / §15 NAMED RISK — shown, not asserted). The real advance is
the constraint-elimination instrument (Part II) over the right object, and ultimately the dynamic,
state-resolved data §12.4 names as the binding constraint.

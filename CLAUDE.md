# Homeostat — project laws (auto-loaded; these bind every session)

**Homeostat is a mechanism-unearthing engine: it imputes the causal mechanism under a symptom
presentation — the combination of weak, fungible, sub-threshold signals holding a coherent state (a
*shadow* the signals cast in concert) — by reading ONE person, zero-time, over a FIXED PRIOR web of
known regulatory mechanisms, eliminating candidates by TWO signs (positive candidate-elimination +
negative censors) and reading convergence across many lossy lenses (a holographic projection). Data
geometry, not statistics.** These laws exist because an agent (me) repeatedly installed **statistics**
where that coherence search belongs — and an earlier version of these laws *enshrined* the mistake.
The design is **SETTLED (2026-09-01): `docs/SYSTEM_DESIGN.md` is the governing document** — one
clinical engine over a prior web (Engine A, population node-birth, is RETIRED), two-sign σ-elimination,
biology read as an OTP geometry. Read it before any analysis, then the canon
`docs/REGULATORY_DEFICIT_PROGRAM.md` (σ §4, κ §5, the falsifiability guard §5.9).

**LAW 1 — DATA-GEOMETRY + CLASSICAL AI, NOT STATISTICS.** Statistics is priorless and honest but
**too weak** for this problem: a phenotype from many weak, *fungible* (interchangeable),
sub-threshold signals holding a meta-stable collective state is invisible to element-by-element
association at any sample size (§2.4). A statistic (PBS, a frequency, an enrichment) is at most one
cheap **search-order prior** — never the method, the significance, or the object. Alarm words:
"significant / enriched / associated / frequency / hub / participation / p-value."

**LAW 2 — THE METHOD IS A σ-TRAJECTORY SEARCH; THE COHERENCE MEASURE IS σ (a Blum measure), NOT a
statistic.** Drive **H = log₂(surviving candidate mechanisms) → 0** by candidate-elimination. Each
"test" is a **data-geometry constraint**: a population **co-variation** (signals that lock together
across genomes) or a symptom **co-presentation** (symptoms that cluster across people) — the
mechanism is where the two geometries lock. **σ = the minimum constraints to pin a unique mechanism
(SC=1)**; it equals the teaching dimension (Five-Field Identification), NOT a frequency. The
**bulk/tail phase transition** is the collective-state / parsimony signal (structure resolves rivals
in clusters, then the tail is PAC-limited). Primary sources: the founder's **SSL paper** + κ
(`SIGNIFICANCE_WEIGHTING.md`).

**LAW 3 — THE OBJECT IS A PRIOR WEB — extracted from proven biology, NEVER grown per-read, NEVER
guessed.** The web (which regulatory things couple to which, and each node's role) is PRIOR structure:
proven deterministic mechanism (UniProt/GO/Reactome/Pfam), extracted **once** — not learned from the
person (you cannot fit a wiring diagram to one snapshot), not a hand-written edge list, and NEVER
seeded from guesses (the PBS pile, the generic interactome, SDIS's edges — the recorded death §15,
§12.14). **The bright line (the genus guard):** an edge enters only as *proven deterministic mechanism*
(authored/extracted, incomplete-but-not-wrong), never as a *computed association* (a frequency/
enrichment — the forbidden statistic). Node *birth* by population induction (Engine A) is **RETIRED**;
node *death* (negative learning / near-miss) is promoted to the negative sign (LAW 3b);
**consolidation** = safe-forget a κ=0 node (the idempotent bulk) survives. Per-person growth is
**DIMENSIONAL** — discriminate by adding a *measurement dimension*, never by growing nodes (Peitho: the
node set is fixed and bounded; `position.py::discriminates` — add a dimension, never a model or
threshold).

**LAW 3b — SPECIFICATION IS TWO-SIGN; "no disease" is a certified ⊥, not an empty search.** σ = teaching
dimension is defined over BOTH signs: positive candidate-elimination (μ: what could cast this shadow)
AND negative censors (μ⁻: what is ruled out — physics-orthogonal role exclusions; and treatment-
response, which *rules out* every mechanism where the drug's target isn't upstream of the resolved
symptoms). The channels are information-theoretically isolated — "this is not disease X, *with proof*"
cannot be recovered from the positive side. **Completeness is κ-coverage of the shadow, NEVER a count
of criteria** (a count is blind to the composition gap γ, which lives at the bridges — the non-idempotent
part). Score the phenotype as σ(P, μ ∪ μ⁻). Primary source: `NEGATIVE_SPECIFICATION.md`.

**LAW 3c — BIOLOGY IS ALREADY AN OTP GEOMETRY; the engine is OTP-native.** Gene roles are physically-
orthogonal projection axes (a membrane transporter and a polymerase fold in different electrochemical
environments — mutually transparent = the informational zero = the negative-sign censor, at *zero*
abstention tax). Consequences that fall out for free: **d** (the bridge count) is bounded by the proven
semantic-category structure of gene function; **fungibility** is a free consequence (same-category genes
are fungible fillers = one class centroid); **direction is never guessed** (it is the residue of
negative-sign censors — free and safe, the Bellman-Ford bidirectional speedup without the destruction
risk). DNA is the base-2² OTP code (`ORTHOGONAL_TERNARY_PROJECTION_THEORY_PART2.md`); the instrument
reads the projection biology already stores.

**LAW 4 — THE FALSIFIABILITY GUARD: σ_sem MUST STAY > 0.** A frame that makes every observation
*confirm* it reports **σ_sem = 0** — zero information, Quixote's windmills, **memorization not
resolution** (`self_confirming_cannot_certify`). **SDIS's "31/31 symptoms, 100% accuracy" is σ_sem=0
by construction.** So: NEVER collapse to a single self-confirming mechanism; keep plurality
(regime-multiplicity, H3); and **learn at the residual** — the informative constraint KILLS a rival,
never confirms the leader (a confirming constraint has value zero, Howard).

**LAW 5 — EARLY STOPPING AT THE κ-KNEE IS THE PARSIMONY HALT.** Drive the elimination/discrimination
trajectory while the bulk amplifies (κ high — structure resolving rivals in clusters); **stop at
κ → 0** (§5.5, §10.4). Past the knee, each further constraint resolves only one tail rival — the search
is *memorizing the presentation*, i.e. becoming SDIS. Judge the **process**, not the endpoint (pabkit —
the trajectory tells you structured coherence vs. overfit). This is the overfitting guard for small-n.

**LAW 6 — THE DECISION SHELL IS PEITHO; the oracle (μ) is diversified; no ML; the data gates the
claim.** Signals enter as tiered, signed-ternary positions off a **per-individual mined zero**
(= prakriti/vikriti, §6.7), the informational zero carrying honest abstention; decide by elimination;
discriminate by a **new orthogonal dimension**, never a tuned threshold (built: `otp.py`,
`signal.py`). σ is only as good as **μ** — the alternative-mechanism space — so the Ayurvedic /
cross-tradition ensemble enters as **μ-diversification** (independent ways to enumerate "what else
could this be"), NOT as edges to seed (§6.4, §6.9). Diagnosis is a Winston *story*; the
population/E-I-R signal is a search-order prior. No ML as the method (a bounded model is at most a
founder-placed tail). Without co-variation / co-presentation / dynamic data, outputs are hypotheses
(§12.4).

**LAW 7 — CONSTRAINTS ARE TRIANGULATED ACROSS PARTLY-ORTHOGONAL LENSES; WE GENERATE, NOT CALCULATE.**
The kill-matrix is never read off one source — a fixed pre-drawn map (STRING participation over the
generic interactome) was the Act-2 death: no person, no phenotype, the same shape whatever you feed
it. Each constraint is **triangulated across several partly-orthogonal free lenses** — variants
co-travel (gnomAD/1000G), each wires to the traits (GWAS), genes co-express (GTEx), STRING as ONE
demoted vote — and a candidate survives only where independent lenses **converge**, killed the moment
they **disagree** (§6.9, the holographic principle). **Imperfect orthogonality is fine because we
GENERATE (eliminate rivals), not CALCULATE (estimate a number):** correlated-errors → false-confidence
is a *statistics-stack* disease; a lens is a kill-opportunity, so overlap is redundant, never wrong
(partial orthogonality → between n and 2n bits, non-inclusive — always net-additive). The engine
already embodies it: κ is **marginal** coverage (overlap → κ = 0, ignored, never inflated), and greedy
max-κ reaches for the most-orthogonal next lens by construction. Never read a single source's *shape*
(hubs/participation) as significance; triangulate.

**LAW 8 — THE PARTITION IS A FREE VARIABLE (any legitimately-isolatable group), NOT A HARDCODED AXIS.**
A population/phenotype lens is *differentiation across any independently-isolatable group* — ancestry
at ANY resolution (continent → sub-continent → founder/caste isolate), a phenotypic sub-section, an
exposure — read **direction-free** (magnitude, e.g. max pairwise Fst), never `SAS>EUR`. The partition
is *searched*; a partition carved to fit the answer is σ_sem = 0 one level up (admit only genuinely
isolatable groups). SA-vs-EUR was the coarsest, dumbest instance — the motivating example, not the
architecture (measured 2026-08-31: the bare binary is a 44% coin flip; differentiation restores
specificity; LRRK2's signal is sub-continental, so it needs a *finer* partition — NOT a lowered
threshold).

**LAW 9 — RECOGNIZE ROLES, NOT GENES (semantic class, never token); REGENESIS IS THE ROLE ENGINE.** The
mechanism is invariant; genes are population-local, **fungible fillers** (one pool in group A, a
different pool in a founder isolate, same mechanism). Pull out the genes filling each **role** by the
*role they play* (relational signature → class centroid), NEVER by gene-identity — this is Genesis
**semantic-class firing** over genes (fire on the class, never the surface token), deterministic
(GSE/HDC vector-symbolic binding), NEVER a learned embedding. **Regenesis (`mcp__Regenesis__*`) is the
working engine — use it, do not rebuild it**: a mechanism universe whose classes are roles, centroids
from real relational geometry (STRING/GTEx as role-defining *context*, never the map-as-answer). The
holographic combine (per-population lossy filler-projections → the role-structure) is Regenesis
deriving. **Meta-thesis:** any statistics-or-thin-signal read imputes the individual from the
population — cross-population differential outcomes are its body count — so the story engine is the
*most* rigorous, objective approach; frame the paper in accepted vocabulary (methods discloses
Genesis/Winston fully) but never let framing outrun the computed result (σ_sem > 0 at the meta-level).

**NO HARD-CODED GENE→ROLE BINDINGS (cardinal; ONE correct version).** The substrate authors role
VOCABULARY — the rules/Forms (`if x amplifies signal then x becomes amplifier`) — NEVER *which gene
fills which role*. Asserting `NOD2 amplifies signal` as an input fact is purposivistic role-assignment
(canon §3.3), the annotation-as-ground-truth premise the program inverts. The mechanism is GROWN from
data convergence; a directed signaling role enters only when real directed evidence (Reactome) supplies
it, as data. There is no "positive-control version" that gets to hard-code and a "true version" that
computes — one correct version, and it computes the fillers.

The recurring failure has one root: reaching for a statistic, seeding/guessing the object, reading
one map's shape as the answer, **matching gene tokens instead of roles**, or **hard-coding a gene→role
binding** — because it feels like progress — instead of running the two-sign σ-trajectory elimination
over the *prior* web, discriminating by new dimensions, and recognizing roles by class. Recognizing the
reflex and refusing it is the only fix.

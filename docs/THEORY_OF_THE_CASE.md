# Theory of the Case — Homeostat

**Regulatory-deficit medicine as a data-geometry / classical-AI problem: imputing a
mechanism from the coherence of many weak, fungible, sub-threshold signals — not from
statistics.**

**Status:** Canonical derived design, REWRITTEN 2026-08-30 after a working-through with the
founder that corrected the conception a second time. The first rewrite (earlier the same day)
established "data-geometry, not statistics." This one sharpens *what that actually means* — why
statistics fails (power, not bias), what the coherence detector concretely IS (constraint
elimination, not a frequency and not a bare order parameter), and where the one unbuilt piece
sits. The founding canon is `docs/REGULATORY_DEFICIT_PROGRAM.md` (verbatim, authoritative, do
not edit). This document is the *instantiation*: the corrected conception, the method's shape
grounded in the founder's existing built code, the pathology record, and an explicitly DEFERRED
object. The rebuild is post-this-document and is designed WITH the founder — do not build the
method from this page as if it were fully specified.

**Supremacy clause.** DERIVED. Where silent, ambiguous, or wrong, canon governs, in order:
(1) the founder's statements; (2) `docs/REGULATORY_DEFICIT_PROGRAM.md`; (3) the sources pinned
in `docs/REFERENCE_MANIFEST.yaml`. The portfolio data-geometry reference is
`~/Projects/Kaggle_Killer/DATA_GEOMETRY_ARCHITECTURE.md` (OTP, Informational Zero, COEC, GSE,
HDC). The mechanism this project reuses is spread across the founder's built projects — those
are named in Part II and are primary sources, not this summary.

**The one deferred thing, named up front so it is not quietly filled in.** The concrete
**object** — the mechanistic constraint structure that says *which sub-threshold signals must
lock together* (Homeostat's equivalent of harmonizing's ATCC/Cellosaurus cell-line fact table)
— is NOT specified in this document and must not be invented from it. It is the design
conversation with the founder, and the founder's **SDIS grounding document** (their own attempt
to sketch the mechanism-with-a-prior) is where it starts. Every "what is the object" question
below is deliberately left open.

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

## Part II — The Method: shape and grounding (the concrete OBJECT is DEFERRED)

> This part says what the instrument IS, grounded in the founder's *existing built and measured*
> code, and what it is NOT. It does **not** specify the object it runs over — that is the design
> conversation (see the callout at the top). Do not build from this part as if the object were
> given.

### What the coherence detector concretely is — read off the built portfolio, not imagined

The signal is the **coherence of a combination**: the sub-threshold elements are not independently
significant — they are locked together by the mechanism's structure, so observing part of the
pattern lets you impute the coherent whole, and *the coherence itself is the evidence of
mechanism*. Improbable-and-coherent, never frequent.

The important correction, from reading every place this is actually built in the portfolio: the
working coherence detector is **constraint elimination over a domain-knowledge graph, with honest
abstention** — NOT a frequency, and NOT a bare synchronization order parameter. Kuramoto /
metastability is the right *conceptual shape* for the target (a collectively locked state), but in
every instantiation that has actually been built and measured, the running instrument is
constraint-propagation-and-elimination. The primary sources:

- **harmonizing** (`~/Projects/Kaggle_Killer/competitions/harmonizing/src/symbolic_healing.py`) —
  the mechanism run on *biological* data. Know one thing confidently (a cell line, MCF-7) and a
  whole coherent set of coupled facts falls out by domain physics: human, female, breast
  adenocarcinoma, breast, cell-line material. The constraints come from ATCC/Cellosaurus fact
  tables, not from any statistic; observing part of the pattern eliminates the incompatible options
  and concentrates the rest (the Monty-Hall move). It fills only what nothing else has spoken to,
  and abstains otherwise. **This is the closest existing thing to the Homeostat instrument.**
- **genomevault clinical committee** (validated on 3.7M positions) and its domain-agnostic
  extraction **orthogonal-validators** — independent readers each vote with a confidence margin;
  the signal is the *collective* state, and where every reader has zero margin (nothing coheres)
  the decision **escalates/abstains rather than guessing**. Fungibility-friendly: no single reader
  must fire; you read the whole.
- **Peitho** (`~/Projects/Peitho`) — the per-individual baseline + decision half, built and
  mutation-pinned: a **mined zero** (a norm mined from *this* data, robust to non-signal), a
  **signed-ternary position** off it, an **informational zero** that is honest abstention, and a
  decision by **elimination/interference** — a single confident exclusion removes more of the
  answer space than a confirmation adds — with discrimination fixed by **adding a new orthogonal
  dimension, never tuning a threshold**. The mined zero is, structurally, canon §1.1's missing
  per-individual reference step (= prakriti/vikriti, §6.7).
- **Regenesis κ** (`SIGNIFICANCE_WEIGHTING.md`) — a math measure of *coherent-and-improbable* vs.
  elaborate coincidence. Usable, with one standing caution: κ is coverage/PageRank over a *graph*,
  so it is only data-geometry if that graph is the **mechanism-derivation graph**, never a generic
  network. Pointed at a generic interactome it silently becomes a topology statistic — which is
  precisely Act 2 of the pathology below.
- **gse / HDC OTP** — the ternary substrate where "0 = orthogonal / abstain" is exact.
- **COEC** (`~/Projects/COEC-Framework`) — the theory/vocabulary: computation as a trajectory under
  many simultaneous constraints, **metastable** configurations as holding states, an order
  parameter, and the residual that "emerges from their collective interaction" and cannot be
  attributed to any single component. This is the conception, stated formally. Vocabulary, not code
  to lift.

### The two halves of the instrument (both grounded in built code)

1. **State estimator + decision** — per-individual mined baseline, signed-ternary axes,
   informational-zero abstention, decision by elimination, discrimination by new orthogonal
   dimension. Built in **Peitho**.
2. **Coherence of the combination** — constraint propagation over a domain-knowledge graph
   (**harmonizing**), plus committee-collective-state / all-zero-margin abstention (**genomevault**,
   **orthogonal-validators**), with **κ** available as the coherence measure and **OTP/HDC** as the
   ternary substrate. Kuramoto/COEC is the conceptual shape of the locked state; the running
   instrument is constraint-elimination.

### The DEFERRED object — the one thing that is not specified here

The instrument is only as good as the **constraint graph it runs over** — Homeostat's equivalent of
harmonizing's ATCC fact table: the mechanistic structure that says *which sub-threshold variants
must lock together in a coherent mechanism*. This is **not** specified in this document, must not be
invented from it, and is the design conversation with the founder. It is where known biology and the
Ayurvedic/cross-tradition carvings enter as candidate constraints, and it is where the founder's
**SDIS** document was headed. Naming a concrete graph here — or substituting a statistic for it —
is the recurring drift (Part V).

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
   for a fungible, sub-threshold, multi-variant etiology; it is at most a cheap search-order prior,
   never the method, the significance, or the object.
2. **The signal is a coherent combination locking into a meta-stable state** — not any element's
   frequency or association. The elements are weakly-associated and fungible; the mechanism lives one
   level up, in the collective locked state.
3. **The coherence detector is constraint-elimination over a domain-knowledge graph, with honest
   abstention** — not a frequency, not a bare order parameter, and not participation/coverage over a
   generic network. Kuramoto/metastability is the conceptual shape; the working instrument is
   constraint-elimination. (κ is allowed only over the mechanism-derivation graph.)
4. **Per-individual baseline first.** Mine the person's own setpoint (the mined zero =
   prakriti/vikriti) and read deviation from it — never a population reference.
5. **The intelligence is in the constraint graph.** An over-firing constraint that collapses real
   distinctions is *removed, not tuned*; a missed discrimination is a *missing orthogonal dimension*,
   never a mis-set threshold. Domain knowledge is the algorithm.
6. **Diagnosis is a story; the traditions are decorrelated candidate-constraint sources; the
   population/E-I-R signal is a search-order prior** — none is the method or an authority.
7. **Coherence is not automatically signal — measure it on the right object.** Abstention (the
   informational zero) is load-bearing. No ML as the method; a bounded model is at most a founder-placed
   tail. Without dynamic data, outputs are hypotheses (canon §12.4).

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

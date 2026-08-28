# Theory of the Case — Homeostat

**Regulatory-deficit medicine: annotation-blind mechanism discovery under an oracle ensemble.**

**Status:** Canonical derived design (2026-08-28). The founding canon is
`docs/REGULATORY_DEFICIT_PROGRAM.md` (verbatim, authoritative, do not edit) — a
self-contained reconstruction checkpoint written to be handed to an agent cold. This
document is the *instantiation*: the mechanism restated, the project shape, the laws,
and what folds in from sibling projects. Read the checkpoint in full before nontrivial
work; this document does not replace it.

**Supremacy clause.** This document is DERIVED. Where it is silent, ambiguous, or wrong,
the canon governs, in this order: (1) the founder's statements; (2)
`docs/REGULATORY_DEFICIT_PROGRAM.md`; (3) the source documents pinned in
`docs/REFERENCE_MANIFEST.yaml`. The checkpoint's own status ledger (§15) governs what may
be cited as proved vs. designed vs. conjectured — do not promote a conjecture to a premise.

## Canonical references

Machine-checkable list with sha256 pins: `docs/REFERENCE_MANIFEST.yaml`. Key entries:

| Source | Role | Location |
|---|---|---|
| REGULATORY DEFICIT PROGRAM (checkpoint) | The founding canon | `docs/REGULATORY_DEFICIT_PROGRAM.md` |
| Specification Complexity paper (σ) | Formal substrate I | `~/resume/Specification_Complexity_Paper/specification_complexity_paper.md` |
| SIGNIFICANCE_WEIGHTING (κ, the bracket, bridges) | Formal substrate II | `~/Projects/Regenesis/docs/SIGNIFICANCE_WEIGHTING.md` |
| Knowability paper (footprints, oracle-relativity, pseudo-testing) | Carving-audit discipline | `~/tools/Detective/docs/theory/operator_completeness/submission/knowability_ieee.pdf` |
| Peitho | Existence proof of the control structure (signed axes + abstention + elimination) | `~/Projects/Peitho` |
| GenomeVault | Genomics substrate machinery (variant parsing, GDiff differential encoding, reference builders, HDC experimentation) | `~/Projects/genomevault` |
| AVS catalog + interaction model | One enumerable carving source for the oracle ensemble | `~/MentalAtlas/biodata/clinical/ayurveda/` |
| Index genotype R (screening-grade — see Law 3) | Sampling-frame specification | `~/MentalAtlas/biodata/genetics/` |
| AuDHD_Correlation_Study | SUBSUMED — salvage only, per `docs/SALVAGE_MANIFEST.md` | `~/Projects/AuDHD_Correlation_Study` |

## Part I — The Case (mechanism restated; founder to confirm)

**The claim (checkpoint §1).** Allopathic diagnostics has no per-individual
reference-establishment step: every value is scored against a population-derived
distribution, and there is no representation for "this axis has no opinion about this
individual." That failure is invisible for lesional disease (a discontinuity in kind is
detectable against any baseline) and maximal for regulatory disease (a deviation in
degree is detectable only against the correct baseline). The blind spot is derivable
from the instrument's construction, and it predicts, by mechanism, the residual
categories of clinical medicine: idiopathic, functional, atypical, medically unexplained.
The name **Homeostat** (Ashby's self-equilibrating device) states the thesis: regulation,
per individual, as the object of study.

**Why the standard instrument cannot see it (§2).** Metabolic control analysis: flux
control coefficients sum to one and redistribute toward saturation under load — so for
flux phenotypes the effect being sought *does not exist at the locus being tested*; it
exists in the composition, and baseline measurement is least sensitive exactly where the
mechanism lives. The omnigenic model is the literature's name for the long-tail half of
this; cite it, never re-derive it. Single-variant association on this phenotype class is
a method mismatch, not an underpowered version of the right method.

**The inversion (§3).** Do not ask "does variant X associate with phenotype Y given X's
annotated function." Recover coupling structure from data *with annotation held out*;
then check whether known gene function falls out of the recovered structure. **The
preregistered falsifier: recovery of known annotation without having used it.**

**The formal machinery (§4–§5).** σ (specification complexity) transports as "how many
independent constraints pin a mechanism down"; a surviving mutant is an unconstrained
degree of freedom in the mechanistic account. σ is parameterized by μ — the oracle,
which mechanistic alternatives are considered at all — and μ is where the unformalizable
judgment lives. κ (marginal coverage / hub score) is the significance weight and the
induction prior; deep chains are ranked by improbability-given-branching, carried as an
explicit widening bracket, never a point estimate. **Bridges** — promotions joining
previously-disjoint clusters — break the submodularity that makes greedy descent
tractable, and in biology a bridge is a **pleiotropic gene joining two mechanism
clusters**. Bridges are simultaneously the target and the obstruction: their effect
exists only in composition, which is exactly why they never clear single-variant
significance. The tractability claim is quantitative, degrading in the supermodular
degree *d*, and *d* is bounded *by construction* via the candidate-set filter.

**The oracle ensemble (§6).** A single expert-built μ is a point estimate; the program
refuses point estimates everywhere else and must refuse this one. σ-variance across a
genuinely diverse μ-ensemble is the measurement: a bridge stable across widely-varying
carvings is structurally real; one appearing under a narrow band of μ is a partition
artifact. LLM-generated ensembles collapse toward the consensus that produced the
existing partitions — hence *causally independent* carving sources, phylogeny-weighted:
Ayurveda and TCM at full weight (independent lineages; their convergence is signal),
Sowa Rigpa partial (Ayurveda-descended), **Unani at zero weight as the negative control**
(Galenic ancestor of allopathic medicine — agreement is inheritance, not convergence).
Structure-derived partitions (co-expression, PPI topology, selection signatures) enter
on the same terms and are formally preferable (they factor through the mechanism, not
its description). The knowability discipline audits every carving: no binary partition
asserted as complete (the n=2 trap), no reading of the observed set O as the reachable
set I, validators characterized as oracles ω *before* their results are read.

**The candidate-set filter (§7).** E/I/R: European reference pool, Indic pool, index
individual R (genome-wide Euro-shifted, phenotype Indic-typical and severe). Variants
where R matches I and differs from E are enriched; R-matches-E-differs-from-I are
deprioritized. Formalized as PBS (population branch statistic) — a continuous per-locus
ranking, a **prior over search order, not a hypothesis test**. It bounds *d* before the
descent runs. At population scale the deconvolution is a regression over the ANI/ASI
cline, and "tracks neither" is the most interesting outcome (differentially penetrant
regulation on shared variants).

**Validation (§10).** Two primary validators that fail differently: selection-signature
enrichment of the candidate pile (uses no annotation — fully legitimate) and
annotation-recovery (partially contaminated — usable only with the preregistered list of
which annotations count as independently recovered). Annotation-derived confirmation of
annotation-blind modules is self-licking and excluded. Stopping rule: **κ → 0**, made
binding in advance, because no review board will say when to stop.

**The positive control (§9, §13.3).** LRRK2 — annotated "Parkinson's gene," actually an
inflammatory-regulation hub (LRRK2–NOD2–RIPK2, leprosy/Crohn's/T1R overlap, antagonistic
pleiotropy, effect visible only in the epistatic composition), recovered only from the
South Asian pathogen-genetics direction. **Any pipeline that cannot recover the LRRK2
bridge from annotation-blind data is not working. Run this before trusting any novel
output.**

## Part II — The Data Layer (the substrate)

Deterministic machinery that turns raw inputs into the ranked, tiered substrate the
intelligence layer descends on. Nothing here decides; it narrows and encodes.

- **II.1 Index genotype ingestion.** Parse the consumer array export (v5 GSA, ~600k
  SNPs) into tiered records: directly-observed genotypes vs. report-layer
  interpretation (not independently verifiable — tier separately, §11.5). The array's
  SNP content is itself a normalization artifact of the European discovery literature —
  carry that as metadata, not a footnote. GenomeVault's parsing/PGx machinery is the
  starting point.
- **II.2 Population frequency layer.** 1000 Genomes + gnomAD stratified SAS/EUR
  frequencies joined to the index variants.
- **II.3 The E/I/R filter.** PBS per variant across E, I, R → the scored priority
  queue. Per-variant F_ST as the cruder fallback. Output: the bounded-*d* candidate set
  (§13.1 — first experiment, zero cost, days).
- **II.4 Selection-scan overlay.** Published iHS / XP-EHH / CLR scans for SAS and EUR
  joined to the pile; enrichment test vs. matched control sets (§13.2 — validator #1).
- **II.5 Network topology layer.** STRING / Reactome / BioGRID adjacency — the
  structure-derived partition source and the graph κ is read from. GTEx co-expression
  for module recovery (annotation inspected only *afterward*, as the §3.2 check).
- **II.6 Carving compiler.** Each oracle source compiled to the same shape: a partition
  of mechanism space with signed axes and an explicit abstention state (the Peitho
  shape). The AVS catalog (518 products / 8,406 constituents,
  `avs_formulas_2023.json`) plus the classical category system (ama / dhatu / srotas /
  dosha / agni / prakriti-vikriti) is the first enumerable source; TCM and Unani
  (negative control) follow; structure-derived carvings from II.5 enter on the same
  terms. Phylogeny weights attached per §6.9. Exclusion line: mechanistically disproven
  (out) vs. dismissed-by-association (in).

## Part III — The Intelligence Layer (classical AI on top)

The σ/κ machinery run over the substrate. Sketch — to be designed against measured
Phase-1 output, not before:

- σ-structure per carving; σ-variance across the ensemble (bridge vs. partition
  artifact, §6.3); over-flexible carvings self-police as low-σ (§6.11).
- κ-weighted coherence descent over the candidate set; the bracket carried explicitly;
  bulk/tail split; stopping at κ → 0.
- Elimination over signed axes with abstention (Peitho is the existence proof that this
  control structure runs; the domain there is inventory — the architecture is the
  argument).
- The self-confirmation guard as structure, not discipline: confirmation only from the
  stated spine (the data layers of Part II), never from the engine's own derivations.

## Part IV — The Laws

1. **The architecture is classical AI / deterministic data-geometry, not ML.**
   Population-genetic *statistics* (PBS, F_ST, iHS, enrichment tests) are statistics,
   not gradient-fit models; they are the substrate. No model is proposed as
   architecture. The global AI-IS-NOT-ML law governs.
2. **Ayurveda (and every tradition) is a hypothesis-generating carving source, never an
   authority.** Nothing in the program depends on any Ayurvedic claim being true
   (checkpoint Warning 1). Convergence is scored under oracle phylogeny; Unani is the
   negative control. The claim is about *search strategy over partition space* — high
   prior density in an under-searched region — never about outcomes (§12.7).
3. **The n=1 case is a sampling-frame specification, never evidence** (Warning 2). The
   index genotype is screening-grade; no variant carries clinical or analytic weight
   until WGS. Report-layer claims are tiered below observed genotypes. The
   marker-count-implies-severity argument is recorded as internally inconsistent
   (§11.3); do not re-derive it.
4. **The confirmation channel must not have been used in the derivation** (§5.9, §10.1).
   Preregister the annotation-recovery list before running. Annotation-confirmed
   annotation-blind modules are self-licking and excluded.
5. **No carving may be asserted as complete; no dichotomy assumed** (§6.13, §12.9).
   Asserting a binary partition is a bet that n = 2 and produces a provably deficient
   regime. The honest form is the relative certificate: failures confined to the
   guarded modes are caught, with the guarded set named. Initiation/termination is a
   candidate carving — the *most* contaminated one — never "the axis."
6. **Constants do not transfer across regimes** (§12.5). SSL's dense-graph constants
   (L = 0.528, ~3% knee, 28× drop) are never cited for the sparse pathway/rule graph.
   Structure transfers; constants are re-measured.
7. **Measurement precedes proof** (§14.1). *d* is measured on the actual graph before
   anything is proved about bounded-bridge greedy. Nothing in §15's DESIGN+CONJECTURE
   tier is used as a premise.
8. **LRRK2 gates everything** (§13.3). The pipeline earns trust by recovering the
   LRRK2–NOD2–RIPK2 bridge blind. Until then, no novel output is reported as a finding.
9. **Ancestry is a measurable, continuous covariate** (§12.8) — ANI fraction or
   characterized endogamous founder groups. Never a language family, never a folk
   category, never appearance.
10. **Stopping rule κ → 0, binding in advance** (§10.4). There is no review board; this
    is its replacement.

## Part V — The Pathology Record

Failure modes recorded so they stay recognizable (checkpoint §12 + Appendix C, plus
this project's own):

- **Classification-first reading** — sorting the program by surface features
  (traditional medicine, consumer genetics, n=1, unfamiliar formalism) and processing
  everything downstream as evidence about the classification. Fluent, structured,
  confident output carrying zero information. This is the failure the thesis is about,
  one level up — and it is why the project is named Homeostat and not anything
  tradition-marked: the name must read as control theory to the skeptical reader,
  because the Ayurvedic ingredient is an idea-generating surface for coherence and
  mechanism imputation, not a medical epistemology.
- **Self-licking confirmation** — the most dangerous, because it looks like rigor:
  objections, caveats, fast descent, zero information. Guard structurally.
- **Oracle collapse** — LLM-generated carvings correlate with consensus; variance
  understates uncertainty. Persona prompting does not fix it.
- **Reading O as I** — "pharmacology covers initiation" is a fact about what has agents
  pointed at it, not about which failure modes exist.
- **Pseudo-tested mechanisms** — CRP, flare/no-flare, and composite indices are
  non-injective oracles; a mechanism that moves the state but not the assay reads as
  un-implicated regardless of truth. Characterize every readout as an ω first. The
  measured 43%/6% spread is the scale of the effect.
- **Missing dynamics is the binding constraint** (§12.4) — a static array has no time
  axis; longitudinal multi-omic sampling through state changes is what the method
  actually needs. Everything in Phase 1 is what can be done before that exists. Do not
  oversell Phase-1 output as the full program.
- **Re-litigating settled ground** — the genetic-testing limitation (array vs WGS) is
  known and accepted; the standard objections (identifiability, falsifiability, n=1,
  outcome data) are answered at §12.2, §3.2, §11.2, §12.7. Re-raising them is not rigor.

## The first experiments (checkpoint §13 — the actual work queue)

1. **§13.1 E/I/R filter** — PBS over 1000G/gnomAD + index export. Zero cost, days. Everything descends on its output.
2. **§13.2 Selection-signature enrichment** on the resulting pile — validator #1, available now.
3. **§13.3 LRRK2 positive control** — blind recovery of the LRRK2–NOD2–RIPK2 bridge. Gates all novel claims.
4. **§13.4 Oracle-ensemble σ-variance calibration** on the known leprosy/Crohn's/T1R partition, with Unani as negative control.

Target cohort horizon: Genes & Health (~50k British Pakistani/Bangladeshi, applied-for
access) and NCT04698291 (SPM regulation profiling in that cohort — the resolution axis,
right population, already collecting). Reference panels: GenomeAsia 100K, IndiGen, SARGAM.

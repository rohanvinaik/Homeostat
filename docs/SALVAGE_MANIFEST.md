# Salvage Manifest — what crosses over, and how

**Rule: nothing crosses by copy. Everything crosses by re-derivation against this
project's laws** (`docs/THEORY_OF_THE_CASE.md` Part IV). A candidate is listed here,
inspected, and either re-derived into Homeostat (status → `absorbed`, with the commit)
or rejected (status → `rejected`, with the reason). Unlisted material does not cross.

## From `~/Projects/Predecessor_Study` (SUBSUMED — founder's verdict: "not all that good")

| Candidate | What it is | Why it might cross | Status |
|---|---|---|---|
| Baseline-deviation-topology framework | The old project's core framing | Directly aligned with the per-individual-reference thesis (§1.1); inspect whether its formalization adds anything the σ/κ machinery lacks, or is a weaker duplicate | `candidate` |
| GWAS summary-statistics plumbing | Download/parse/harmonize for large psychiatric-GWAS meta-analyses | §13 needs sumstats handling for OpenGWAS/IEU; reuse the data plumbing, NOT the analyses | `candidate` |
| H-MAGMA integration | Variant-to-gene mapping via chromatin interaction | A structure-derived mapping (annotation-adjacent — audit which side of the §10.2 line it falls on before use) | `candidate` |
| Data acquisition scripts (`data/`, `scripts/`) | Cohort/reference downloads | Mechanical reuse where they fetch resources §13.5 names | `candidate` |
| The 7-subtype findings | Neurotransmitter-pathway subtypes | **Do not cross as findings.** Derived under annotation-first, single-variant logic — the method this program inverts. At most: a known-answer test case for §13.4-style calibration | `rejected-as-findings` |

## From `~/Projects/genomevault` (+ `genomevault_enhanced`, `genomevault_recovery`)

| Candidate | What it is | Why it might cross | Status |
|---|---|---|---|
| Variant parsing / consumer-array ingestion | 23andMe/array → structured records | Part II.1 directly | `candidate` |
| GDiff differential encoding + reference builders | Population-aware template, subtract-against-reference | The per-individual-baseline move, already implemented for genomes; candidate substrate for Part II | `candidate` |
| HDC experimentation (OTP lenses, margin-as-signal) | Deterministic encode/decode machinery | Only if Part III design calls for it — do not presuppose | `candidate` |
| Privacy/blockchain/deployment layers | GenomeVault's product surface | Out of scope for Homeostat | `rejected` |

## From `~/MentalAtlas/biodata/clinical/ayurveda`

| Candidate | What it is | Why it might cross | Status |
|---|---|---|---|
| `avs_formulas_2023.json` + `parse_avs_index.py` | 518-product catalog, deterministic parser | First enumerable carving source (Part II.6); consume in place (manifest-pinned), re-run parser if source changes | `candidate` |
| `interaction_model.json` / `interaction_engine.py` | Typed logic-gate graph + propagator | The carving-compiler prototype: signed axes, gates, state variables | `candidate` |
| `constituent_monographs.json`, `interaction_matrix.json` | Web-grounded constituent + edge layer | Reference layer for carving construction; provenance already recorded there | `candidate` |
| Regimen/assessment files (`regimen_*.json`, `ASSESSMENT.md`) | Personal clinical sandbox | Stays in MentalAtlas — personal health data, quarantined by that directory's own charter; Homeostat consumes the *catalog and model shapes*, not the personal regimen | `rejected` |

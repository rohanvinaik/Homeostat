# Session handoff — Homeostat, 2026-08-29 (pre-compact, reconstruction-complete)

*Written to the discipline of `compaction_drift_overconfidence_notes.md`:
constraints structured WITH their reasons (a bare rule has no mass), the next
action as ONE imperative (NOT an open question — that is the attractor that
causes drift), resolved questions stated RESOLVED, and loud pointers back at the
on-disk sources that can contradict this summary. If a fresh you can't recover
the enumerations + the ONE next action + the forbidden moves from this alone,
re-read `git log --oneline` and the sources named at the bottom BEFORE building.*

## ★ THE ONE NEXT ACTION (imperative — do exactly this, do not re-explore)
**Preregister, then run, the §3.2 annotation-recovery enrichment validator on the
628 candidate bridges already produced in `data/e_i_r/bridge_discovery.json`.**
- MECHANISM (restate in your OWN words before coding, per note 3): take the
  ranked candidate-bridge genes (degree-matched participation p, function-blind,
  already computed). Test whether the top-N are ENRICHED for a PREREGISTERED set
  of known pleiotropic / multi-disease / clearance-and-resolution genes, vs a
  **degree- AND PBS-matched** background, with the annotation set + the statistic
  fixed in a committed preregistration file BEFORE the test runs. Reuse the
  degree-matched permutation shape from `eir_enrich.py` / `bridge_discovery.py`.
- WHY this and not something else: §3.2 is the program's PRIMARY FALSIFIER
  ("recovery of known annotation without having used it"). The 628 candidates are
  hypotheses; only this systematic test validates them. §10.2 contamination rule:
  declare which annotations count as independently-recovered vs plausibly upstream
  of the PPI graph, IN the preregistration.
- This is NOT open. The method is fixed above. Do not re-derive an approach.

## ★ RESOLVED — do NOT reopen these (each with its reason, so it keeps mass)
1. **The candidate object is the E/I/R PBS pile** (`eir_cohort.py`:
   PBS(CSA;EUR,EAS) over Pan-UKBB allele freqs), NOT a p-value-selected set.
   REASON: single-variant significance is a METHOD MISMATCH here (§2.4 — the
   effect is in composition, not at the locus). This is Law 2. RESOLVED.
2. **The bridge-node metric is community PARTICIPATION, degree-matched**
   (`lrrk2_gate.py`/`carving.participation` + label propagation). NOT
   component-joining — that was ILL-POSED (an existing node's neighbours are one
   component by construction). RESOLVED (v2 prereg + amendment).
3. **Both Phase-1 gates PASS on the correct object:** §8.4 selection-enrichment
   on the pile p=0.0005 (genome-wide, drift-excluded); §13.3 LRRK2 recovery
   p=0.024 (degree-matched, function-blind). LRRK2 discovery rank 300/13800 (top
   2%); NOD2/RIPK2 participation 0 (within-cluster, §5.8). RESOLVED. p=0.024 is
   STRONG for structural genetic data (not "modest") — the user corrected my
   over-hedge; keep that calibration.
4. **Data access is free-ware.** Pan-UKBB open S3 (`s3://pan-ukb-us-east-1`),
   1000G, STRING physical, GTEx, PopHuman iHS, GWAS Catalog bulk. Genes & Health
   individual data is affiliation+fee gated → NOT the path. RESOLVED
   (`docs/DATA_ACCESS_LANDSCAPE.md`).

## ★ FORBIDDEN (with WHY — these are the drift attractors; name the twin)
- **Single-variant genome-wide significance (p≤5e-8), PRS/top-hit portability,
  LD-clumping to lead SNPs** as the analytic object. WHY: the program is a
  STRUCTURAL CRITIQUE of exactly that (§2). I substituted it ~4× this session;
  it is the fluent default. Significance is κ/participation over composition;
  the object is the PBS pile. (CLAUDE.md Law 2 — it auto-loads; obey it.)
- **Interpreting candidate-bridge gene names by eye** ("APP is amyloid, thesis
  confirmed!"). WHY: §12.6 classification-first / §12.3 self-licking — a fluent
  post-hoc story that a familiar gene "fits" carries ZERO information and feels
  like rigor. Only the systematic §3.2 enrichment validates. The 628 names are
  data, not evidence.
- **Overwriting canonical docs** (THEORY_OF_THE_CASE.md is sufficient — verified;
  do not "improve" it). Append run records; do not edit the theory doc or the
  compaction-drift notes.

## ★ THE MECHANISM IN ONE PARAGRAPH (own-words anchor; if you can't write the
next one from scratch, you've drifted — STOP and re-read the theory doc)
Regulatory disease is invisible to population-referenced medicine because the
effect is in the COMPOSITION, not at any locus (§2). So: build a population-
DIFFERENTIAL candidate set (PBS pile, §7, a search-order prior not a test),
recover COUPLING structure with function held out (STRING physical + GTEx
co-expr), and read bridges — pleiotropic genes spanning mechanism communities
(participation, §5.8), which never clear single-variant significance. Validate,
annotation-blind, by (a) selection-enrichment on the pile (§8.4, DONE, p=0.0005)
and (b) known-annotation-recovery WITHOUT using it (§3.2, NEXT). LRRK2 is the
positive control (DONE, recovered). Everything is HYPOTHESIS (§12.7), bounded by
missing dynamics (§12.4) — never established mechanism.

## ★ SOURCES (the record that can contradict this summary — read on doubt)
- `CLAUDE.md` — the 4 auto-loaded laws (anti-default guardrail). READ FIRST.
- `docs/THEORY_OF_THE_CASE.md` (derived) + `docs/REGULATORY_DEFICIT_PROGRAM.md`
  (canon). The full theory. Read before analysis — actually read, not skim.
- `docs/runs/2026-08-29-*` — the four run records (PBS pile+enrichment, LRRK2
  v2 PASS, bridge discovery) with all preregistrations + caveats.
- `git log --oneline` — verifiable state. Latest: `d242e52` (bridge discovery).
- Make targets: `eir-pile`, `eir-enrich`, `lrrk2-gate`, `bridge-discovery`.
- Tests: `make test` (54 pass). Gate before commit: ruff + `uvx ty check src`.

## ★ RECONSTRUCTION TEST
From this alone recover: (a) where = both Phase-1 gates PASS on the PBS pile,
628 candidate bridges produced, LRRK2 control cleared; (b) the ONE next action =
preregister + run the §3.2 annotation-recovery enrichment on the 628 candidates,
degree+PBS-matched; (c) forbidden = single-variant/p-value object, eyeballing
gene names, editing the theory doc; (d) the object = the PBS pile, never a
p-value set, because single-variant is a method mismatch. If any is unclear,
`git log` + the sources above BEFORE building.

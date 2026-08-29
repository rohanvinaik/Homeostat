# Homeostat — project laws (auto-loaded; these bind every session)

These four laws exist because an agent repeatedly ripped out the design and installed
standard-GWAS defaults — a worse version of a workflow the field has run for a decade,
which is the one thing this program is a structural critique of. They are the sharp
anti-drift set. The full theory is `docs/THEORY_OF_THE_CASE.md` (derived) and
`docs/REGULATORY_DEFICIT_PROGRAM.md` (canon). Read them — actually read them, every line,
not skim — before any analysis. Not having read them is not an excuse; it is the failure.

**LAW 1 — The doc outranks your instinct, always.** If what you are about to build is what
everyone else already uses (single-variant GWAS, PRS, top-hit anything), you have
substituted your training prior for the spec. That instinct is exactly what the program
exists to escape. Stop and re-read the relevant section before writing a line.

**LAW 2 — Single-variant statistical genetics is the WRONG OBJECT here, by construction
(§2.4).** The effect does not exist at the locus being tested; it lives in the composition
and the sub-threshold tail (metabolic control analysis + omnigenic). Therefore BANNED as
the analytic object: genome-wide significance (p ≤ 5e-8) used as "significance"; LD-clumping
to lead SNPs; PRS / top-hit portability used as the pipeline (that is only the §8.1
*indictment* of the standard apparatus, never our method). **Significance is κ over
recovered coupling structure. The candidate object is the PBS-ranked E/I/R pile. Stopping
rule is κ → 0, never a p-value threshold** (§5, §7, §10.4).

**LAW 3 — The validator runs on the E/I/R population-differential pile, annotation-blind**
(§8.4, §10.2). Selection-signature enrichment of *that* pile (PBS-ranked, R∩I-not-E),
MAF-matched — never on a p-value-selected set, never using gene annotation in the
derivation. Confirmation channel must be independent of the derivation (§5.9). LRRK2–NOD2–
RIPK2 recovered blind gates every novel claim (§9, §13.3).

**LAW 4 — The method is: recover coupling with annotation HELD OUT, then check whether known
function falls out** (§3). Not "does variant X associate given X's annotation." The
decision layer, when it exists, is Peitho's shape — signed axes ±1/0 off a mined norm,
verdict by elimination, abstention load-bearing; discrimination is a NEW ORTHOGONAL
DIMENSION, never a tuned threshold, never a [0,1] score through a cutoff.

The recurring failure has one root: not reading, then defaulting. No further law fixes that
— reading the canon and obeying it does.

# SESSION_HANDOFF — six banks + the native genre/interpretive layer (2026-09-03)

*Written to the compaction-drift discipline (`~/Projects/rohan-vinaik.github.io/papers/Core Documents/
AI_architecture_papers/compaction_drift_overconfidence_notes.md` — a PERMANENT REFERENCE, never edit it):
one imperative next action, constraints WITH reasons, pointers to verifiable sources, a reconstruction
test. Governing docs: `docs/SYSTEM_DESIGN.md` · `docs/THESIS.md` · `docs/STORY_LAYER.md`.*

## ★★★ HOW TO GROUND — the gate the traps below CANNOT replace (read this, then obey it)
This handoff is **tokens** — conclusions. Grounding is the **meaning** — the re-derivation of each
conclusion's PURPOSE. **Meaning is not in the tokens (M1, this project's own thesis).** So reading this
document does NOT ground you; it hands you destinations. The failure that keeps recurring is NOT
fact-drift (the traps handle that) — it is **operationalization-drift**: taking a correct conclusion
("allegory = fungibility") and building a wrong DESIGN from it ("find two tragedies"), because a
conclusion under-determines its design and the prior fills the gap. Reading a conclusion is teleporting
to the destination; grounding is re-walking the path. THREE rules, non-negotiable:
1. **PURPOSE GATE — before you operationalize/build ANY element, write its PURPOSE in your own words
   (what it is FOR in the thesis) and cite the PRIMARY source that establishes it (a THESIS chapter,
   NARRATIVE_MEANING reading, the actual data file — NOT this handoff). If you cannot state the purpose,
   you have NOT grounded: stop and derive. This is the Socratic "what is the POINT of X" as a gate.**
2. **READ ORDER — derive the state from the PRIMARY sources + `git log` FIRST; read this handoff LAST,
   as a CHECK on your derivation. If they disagree, the sources win. Reading the handoff first frames
   every later read as confirmation, not derivation — it poisons grounding.**
3. **The traps below catch FACT-drift only. Operationalization-drift is generative (a new wrong design
   each time) and cannot be enumerated. Only the purpose gate covers it.**

## ⚠ READ THIS FIRST — provenance beats any summary
The verifiable record is **git log + current source + these docs**, not a post-compact summary.
Stale-by-design traps a summary WILL try to re-inject — ALL already killed this session:
- **"Author `genres.index` via Regenesis" (the OLD handoff's one-next-action) — SUPERSEDED.** Regenesis's
  genre knob is its off-the-shelf **diction classifier** (GSE labels whole-text prose as NARRATIVE/
  EXPOSITORY) — the WRONG substrate. Mechanism-genres are **relational TOPOLOGIES**, read NATIVE off the
  coupling web in `src/homeostat/` (tragedy.py, comedy.py), never diction. Do NOT author genre `.rules`.
- **"Allegory is a mechanism-genre (a detector)" — WRONG.** Allegory is the **fungibility INTERPRETIVE
  LAYER** (`fungibility.py`), not a story-frame. Fungibility is EARNED by multi-bank traversal convergence
  (Jordan-vs-Jordan disambiguation, inverted: fan-IN), the `resembles` edge only a seed.
- **"Quest is a distant-bridge detector" — WRONG.** Quest is the **reading/traversal genre** — the read
  itself (the generate-wide→resolve-narrow loop / grail-quest journey), NOT a peer detector module.
- **"Co-expression is a correlation vote" — WRONG.** A Spearman correlation is the statistical slop LAW 1
  forbids. Co-expression is **OTP ternary CO-DEVIATION under perturbation** (GTEx samples are perturbations),
  dynamics not statistics; significance is κ, never the co-deviation count.
- **Regenesis is the SAME engine, not a port** — it stays for ROLE + meaning derivation (roles fire on it),
  called AS NEEDED; the genre layer is native. Metabolic verb = **"channels"** (co-metabolizes mangles).
  Engine A / node-birth = retired; regulatory = SIGNOR not Reactome (Reactome = metabolic only).

## ★ WHERE WE ARE (verify: `git log --oneline`; origin/main is clean + current)
**Engine + encoding spine: built/pinned/pushed** — `search.eliminate_two_sign`, `position`, `jeeves`,
`clinic.read_from_events`, `event.py` (L2 contract + `events_to_web` / role-scoped censors), `web/otp/signal`.

**SIX banks built/pinned/pushed** (every pure decision Detective-COMPLETE; each = a renderer + an `*_fetch`
I/O shell, data gitignored + hash-pinned). The first four emit EDGES into `prior_web.all_events()`; the last
two are new SHAPES:
- **regulatory** `signor.py` (SIGNOR, DIRECTED) · **physical** `string.py` (STRING binding, undirected vote)
  · **evolutionary** `homology.py` (Compara paralogs, undirected vote / fungibility seed) · **metabolic**
  `metabolic.py` (Reactome Metabolism-subtree co-membership, verb "channels"). `prior_web` → 1.5M events,
  3,098 four-network-supported.
- **co-expression** `coexpression.py` + `gtex_fetch.py` — the first bank that COMPUTES, and reads RAW
  geometry. OTP ternary co-deviation over the GTEx v8 per-sample matrix (1.63 GB), tissue riding
  `Event.mode`; `read_coexpression` is **user-amortized** (stream once per gene-set, cache the scoped expr;
  measured 32s→0.10s, 331×). Fired on the LRRK2 axis: 320 events, RIPK/IAP module co-varying across tissues.
- **trait-wiring** `trait_wiring.py` + `trait_wiring_fetch.py` — the tier-3 CALIBRATION PRIOR: a per-gene
  distinct-trait PLEIOTROPY node-weight (a cheap bridge-prior), NOT an edge, from GWAS. Fired: LRRK2 (50) and
  NOD2 (21) top the axis — its true bridges. Application (biasing search order) lands in the driver.

**Native genre + interpretive layer built/pinned/pushed:**
- **`topology.py`** — shared substrate: `otp_combine` (OTP merge → info-zero on disagreement),
  `signed_adjacency` (regulatory graph, amplify=+1/inhibit=−1/mixed=0).
- **`tragedy.py`** — mechanism genre: an amplify-cascade into an absorbing SINK, verdict by the OTP net
  sign propagated along the path (doomed / suppressed[H4] / indeterminate[info-zero]). Fired on LRRK2:
  origins converge on TRAF6 [doomed]; BIRC3's arc [indeterminate] (it both amplifies AND inhibits RIPK1).
- **`comedy.py`** — mechanism genre: a mutual-regulation cycle, verdict by loop-gain (vicious / homeostatic
  / indeterminate). Fired on SIGNOR: 372 cycles (249 vicious, 111 homeostatic, 12 indeterminate).
- **`fungibility.py`** — the ALLEGORY interpretive layer: a paralog seed is fungible where its traversals
  converge on shared partners across ≥2 INDEPENDENT banks (H3). Fired on LRRK2: BIRC3~XIAP and RIPK1~RIPK2
  fungible; LRRK2~RIPK1/RIPK2 REFUSED (paths diverge) — the over-merge dissolved by the geometry.
- **Roles** (`universes/mechanism/`, fired via Regenesis `understand`) still live — Regenesis is the role +
  meaning engine, `story.py` the opaque-token L2→L3 bridge into it. Genres are native; roles are Regenesis.

## ★ THE ONE NEXT ACTION — build the genotype-deep pole (design SETTLED), banks-first

**→ CANONICAL DESIGN (paper, 2026-09-04): `docs/PROTEIN_ROLE_GEOMETRY.md`.** RESOLVED this session: the
genotype/structural pole is a **CENSOR BANK on node ROLE** — deterministic sequence-biophysics → *negative*
constraints (MUST-NOTs) over the existing `universes/mechanism/` roles (amplifier / binder / component /
homolog / inhibitor / metabolizer / transducer / zero_signal), native to `search.eliminate_two_sign`. It
does NOT predict a fold and imports no measured structure; structure-prediction + the fenced solver = a
**separate project**, out of scope. **Role-fence first**, edge-fence (compartment-incompatible couplings)
later. GenomeVault grounding is DONE (Z₂×Z₂ lenses; StWk = −(PuPy×AmKe); lens-disagreement → 46× DNase,
p<1e-15 — reported). Remaining grounding gate before fixing the censor's output shape (paper §10.1): read how
`eliminate_two_sign` / `position` represent a role candidate + how the existing negative-sign / candidate-
censor compiler is wired — the fence must be expressible in exactly the terms the eliminator already eats.
Banks-first is load-bearing (founder): the driver reasons over a BOUNDED universe, so a *pole* — which
REDEFINES the semantic bounds, not just adds to them — must exist before the driver. Order after: developmental
(FIRST censor bank — the native negative sign; commitment = a cell closing off transcription) → exposome →
phenotype pole (with the driver). THEN the **driver** (a `converge`-shaped loop ported near-1:1 from
Detective's CLI: `_converge_impl`→`eliminate_two_sign`, `converge_next_action`→`jeeves`, `certificate_standing`
→`clinical_verdict` — orchestration; where fungibility folds + trait-wiring biases + co-expression enters;
**Harmonizer** wires gene-symbol dialects here). THEN the **blind LRRK2 control** (canon §13.3).

**GENOTYPE-DEEP POLE — SETTLED design (structure WITHOUT structure):** NOT AlphaFold, NOT curated Pfam/GO.
*Why (derive it, don't just read it):* crystallography is in-vitro diffraction ≠ in-vivo; a recorded structure
imports someone's lossy, possibly-wrong measurement — using it forfeits the no-hard-coded / no-imported-prior
guarantee. Instead the **deterministic part of the fold falls out of the raw NUCLEOTIDE SEQUENCE's biophysics
read against its environment gradient** (the "inverse Romeo": a protein by any *other* name carries *fewer*
bits — the right encoding of the gene IS its structure-map; traced by data-geometry traversal, Jordan-vs-
Jordan for folding). **v1 = the PURELY-DETERMINISTIC biophysical fingerprint** (founder's own scoping — NOT
the full fold, which is the horizon), two readouts, each a PURE decision Detective-pinnable on synthetic
sequences before any data: (1) **base-pairing STABILITY** — GC/AT, H-bond count, Hoogsteen → dynamism /
transcribability (the GenomeVault p=1e-15 result); (2) **HYDROPHOBICITY-profile environment traversal** —
codon→AA→hydrophobicity along the sequence → transmembrane topology / the stepwise electrochemical shifts →
which ALSO yields the physics-orthogonal **censor** (two genes whose *derived* environments can't co-exist
can't couple). Data-layer after: **Ensembl CDS FASTA** (verify the real format first). **★ FIRST GROUNDING
for next session (before designing the readouts): READ THE GenomeVault PROJECT DIRECTLY** — canonical
`~/Projects/GenomeVault` (PascalCase; also lowercase `genomevault` / `_enhanced` / `_recovery` variants —
disambiguate which holds the current biophysics kernel). The AT/GC/Hoogsteen → functional-enrichment (p=1e-15)
result was PROVEN there; ground in its actual code/method, not this summary of it. Each bank: PURPOSE-gate →
design fork Socratically → build → Detective-pin the pure decision → FIRE on real data.

## ★★ LOCKED DECISIONS — with reasons, so they survive
- **Genres are NATIVE topology reads, not Regenesis frames.** *Why:* Regenesis's genre substrate is a
  diction classifier (surface prose), the opposite of reading STRUCTURE. A genre is a relational topology a
  ruleset fires on — buildable in-project over the coupling web. (Founder: "build native, only call Regenesis
  as needed; waste not want not.")
- **Allegory = fungibility layer, not a detector.** *Why:* fungibility defeats population-medicine's token-
  matching blindness — recover the mechanism whose CAST varies ({X} in one person, paralog {Y} in another).
  It's woven into the read (fold paralogs into role-equivalence), not a findings-emitter. Earned by traversal
  convergence across independent banks (H3), the `resembles` edge only the seed — so subfunctionalized
  paralogs (resemble but diverge) are NOT folded; the geometry decides, compute-not-impose.
- **Quest = the traversal (reading genre), not a mechanism-pattern.** *Why:* the grail-quest — tracing sub-
  threshold clues through the universe, the journey the value — is the project's canonical query. The read
  IS the quest (generate-wide→resolve-narrow). The "epic-quest / distant-bridge cure" is a property that
  emerges along a roundabout path, not a static predicate.
- **Co-expression = OTP co-deviation, NOT correlation.** *Why:* a population correlation is Law-1 slop. GTEx
  samples are perturbations; two genes couple where they consistently co-deviate off their tissue mined-zero
  (`otp.ternary`, the person's own primitive); baseline samples drop as the informational zero; significance
  is κ. (Founder's adversarial refinement killed the Spearman design.)
- **Trait-wiring = a NODE-WEIGHT (pleiotropy), not an edge.** *Why:* LAW 9 tier-3 — GWAS tunes the search
  order (never a coupling, never significance). Distinct-trait pleiotropy = a cheap bridge-prior κ confirms.
  This is Law 1's one sanctioned use of a population statistic.
- **Genotype-deep pole = structure WITHOUT structure (deterministic sequence biophysics), NOT AlphaFold/
  curated.** *Why:* recorded structure = in-vitro crystallography ≠ in-vivo, a lossy possibly-wrong prior;
  importing it forfeits the guarantee. The deterministic fold-part falls out of nucleotide biophysics read
  against the environment gradient (GenomeVault-proven kernel). v1 = the biophysical fingerprint (stability +
  hydrophobicity-environment), the founder's "purely deterministic" part; the full fold is the horizon.
- **Fire before trusting; verify data formats from PRIMARY sources.** *Why:* GTEx filenames, GWAS MAPPED_GENE
  grammar (`", "` multi / `" - "` intergenic, NOT bare hyphen — MIR9-2HG stays whole) were verified against
  the real files/manifests, not a prior. 0 output = a wiring failure, never trusted as abstention.

## ★ THE REMAINING PIECES
1. **Banks:** genotype-deep pole · developmental (the censor bank) · exposome · phenotype pole.
2. **The driver** — the generate-wide→resolve-narrow read (ported from Detective's `converge`): roles
   (Regenesis) + native genres (tragedy/comedy) + the fungibility fold + trait-wiring bias + co-expression →
   candidates → `eliminate_two_sign` → verdict / certified-⊥ / Jeeves probe. Where Harmonizer wires in.
3. **The blind LRRK2 control** (canon §13.3) — recover LRRK2–NOD2–RIPK2 as coherence, blind: the acceptance
   test. (The role read already recovers RIPK1=transducer / BIRC2=component; tragedy/comedy/fungibility/co-
   expression/trait-wiring all light up the axis coherently.)

## ★ PRIVACY — MUST SURVIVE (a real incident an earlier session, fully remediated)
The founder's actual conditions + an ADHD/meds disclosure once leaked into README + THESIS + a handoff;
scrubbed from the working tree AND git history, verified empty, pushed clean. **NEVER re-introduce personal
conditions/medical facts into any committed or public-facing file.** The greenfield case IS the founder's
n=1 — genericize it ("a cluster of conditions across several body systems"). The `POTS`/`narcolepsy` spell-
check test-vocab in `ground.py` is acceptable per the founder (generic example).

## ★ DATA ACCESS — confirmed live
SIGNOR · STRING · Ensembl Compara · Reactome · NCBI · GTEx (GCS bucket) · GWAS Catalog (EBI) — all 200.
Regenesis is JVM-free (`understand_batch` mass-fires). The only structural limit is the §12.4 genotype×
phenotype cohort; the design works from the free public "shadows", all up.

## RECONSTRUCTION TEST
From `SYSTEM_DESIGN.md` + `THESIS.md` + `STORY_LAYER.md` + this file, a fresh session should recover: (a)
engine + encoding spine + SIX banks (regulatory/physical/evolutionary/metabolic + co-expression + trait-
wiring) built/pinned/pushed; (b) the native genre layer — tragedy + comedy detectors, the fungibility
interpretive layer, topology.py substrate — all fired on real biology; (c) **genres are NATIVE (not Regenesis
frames); allegory is the fungibility layer; quest is the traversal; co-expression is OTP co-deviation not
correlation; trait-wiring is a node-weight not an edge**; (d) Regenesis stays for roles + meaning (story.py +
universes/mechanism), called as needed; (e) next = the deferred banks (genotype-deep / developmental[censors]
/ exposome / phenotype) → the driver (Detective-`converge` port) → the blind LRRK2 control; (f) the privacy
rule; (g) fire-before-trusting + primary-source data verification. If it cannot, re-read the governing docs +
`git log` before acting — do NOT re-derive from a summary.

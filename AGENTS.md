# For agents (and humans) arriving fresh — read before proposing anything

## ⛔ WHAT HOMEOSTAT IS — A MECHANISM-UNEARTHING ENGINE (and the law that protects it)

**The build, first.** Homeostat imputes the causal mechanism under a symptom presentation — the
combination of weak, fungible, sub-threshold signals holding a coherent state — by a **Peitho-style
parsimony search that grows its own mechanism graph (node birth/death) and reads candidates by
convergence across many lossy lenses (a holographic projection)**. It is a *positive* construction
(unearth mechanism), not a critique of medicine. The medicine critique is motivation; the σ/κ
formalism is scaffolding; the build is the search.

**THE LOAD-BEARING LAW that protects the build: DATA-GEOMETRY + CLASSICAL AI, NOT STATISTICS.**

Homeostat is a **classical-AI data-geometry** project. Its method is CONFIRMED (2026-08-30):
**Peitho with automated node birth/death — a σ-trajectory search for the most parsimonious
mechanism that resolves a symptom presentation**, driving H = log₂(surviving candidate mechanisms)
→ 0 by candidate-elimination, the "tests" being **data-geometry constraints** (population
co-variation + symptom co-presentation). The **coherence measure is σ** — a Blum measure equal to
the teaching dimension, NOT a frequency (`docs/THEORY_OF_THE_CASE.md` Part II). It is **NOT
statistics.** A statistical test (a frequency, an enrichment, a population-differentiation score, a
network hub/participation score) is at most **one cheap search-order prior**; it is **NEVER the
method, the significance, or the object of study.**

**Statistics is not the villain — that framing is itself a mistake to avoid.** Statistics is
**priorless, and priorless is honest.** Its problem here is not bias; it is **power**: an
element-by-element significance test is structurally blind to a mechanism carried by many weak,
*fungible* (interchangeable) sub-threshold signals holding a collective coherent state. So the
critique is precise — do not say statistics is "motivated" (the motivated part is the
*diagnosis-labeling* stage and imperfect practitioners, not the significance engine). The drift
to refuse is **statistics-as-method**, and it arrives dressed as respectable rigor. The word
that should trigger your alarm is not only "model" but **"significant," "enriched,"
"associated," "frequency," "p-value," "hub," "participation."**

**Why statistics is the wrong genus here (the whole thesis, in one paragraph).** The phenotype
is produced by a *combination* of sub-threshold signals that are individually weak and mutually
fungible — no single one is necessary, an equivalent substitutes in a given person, so each
looks weak-or-absent alone while the mechanism is present in all of them. The loud,
statistically-obvious signals (the dopamine genes for a polygenic condition; the classic hits) **drown out** the
quiet etiologies, whose contribution exists only in composition. The mechanism itself lives
**one level up**, as a **meta-stable state of coherence** among those elements — a
collectively-locked configuration (Kuramoto in shape) that holds until enough load shifts and
it tips. Statistics tests the element; the mechanism is the collective state. So the method is
**data geometry**: read the coherence of the combination *itself* as the evidence of mechanism.
**Improbable-AND-coherent, not frequent.** (Canon §2, §3.4, §5; the informational zero §5.4.)

**The architecture, concretely (confirmed; grounded in built code).** The search runs the founder's
**σ-trajectory** (Specification Complexity, the SSL paper): candidate mechanisms are eliminated by
data-geometry constraints until a unique, parsimonious reading survives; σ (min constraints to
SC=1, a Blum measure) is the coherence measure, and the **bulk/tail phase transition** is the
collective-state signal. The **object is GROWN, not authored** — the one piece beyond Peitho:
**node birth** (induction on a residual), **node death** (negative learning on a near-miss),
**consolidation** (safe-forget a κ=0 node). Two laws keep it honest: the **σ_sem > 0
falsifiability guard** (never collapse to a self-confirming single mechanism — that IS SDIS,
σ_sem=0, *memorization*; `self_confirming_cannot_certify`), and **early stopping at the κ-knee**
(pabkit — grow while the bulk amplifies, stop at κ→0, judge the *process* not the endpoint). The
decision shell is built: **Peitho**-style signed-ternary off a mined zero, informational-zero
abstention (`otp.py`, `signal.py`). It is **NOT** a frequency, **NOT** κ/participation over a
*generic* network (a topology statistic in disguise — canon §5.12, Act 2 of the death), and **NOT**
a hand-authored or SDIS-seeded edge list (§12.14).

**Four different things, never collapsed:**
- **AI** — the genus (reasoning, representation, symbolic and vector-symbolic computation).
- **ML** — one narrow, avoidable species (gradient-fit models). Not the method here.
- **Statistics** — a *tool* (a cheap search-order prior), **not a genus of method** and never
  the architecture. This is the species that poisons THIS project.
- **Classical AI / data-geometry** — OTP, the Informational Zero, COEC, GSE, HDC, constraint
  elimination, the κ engine (Regenesis). **The architecture here.** Portfolio reference:
  `~/Projects/Kaggle_Killer/DATA_GEOMETRY_ARCHITECTURE.md`.
- **Story-understanding intelligence** — Regenesis (Winston's Genesis, ported). A diagnosis is
  a *story* laid over data (below), and this is the engine for it.

**Know your own bias (this is why the gate exists).** You — and LLMs generally — reach
reflexively for statistics on any genomics/medicine problem, because the training corpus equates
"rigor" with "a p-value." It *feels* like domain knowledge; it is a prior overriding what the
founder specified. The tells: "is this enriched vs a matched background?"; "let's rank by the
differentiation statistic"; "the mechanism is the network hub"; "we need a significance test."
Every one is the drift. When a result plateaus, the first hypothesis is **"the coherence object
/ the constraint graph is wrong,"** never "add a better statistic."

## The two misreadings that also kill this project

**"This is a traditional-medicine project."** No (canon §12.6). Ayurveda enters for ONE
technical reason: it is a **causally independent source of candidate constraints** — a
decorrelated way of proposing which sub-threshold things lock together, uncontaminated by the
allopathic statistical-diagnostic frame. **The point about diagnosis:** the allopathic
"diagnosis" is a post-hoc, motivated meaning-imposing *story* (Winston), treated as ground-truth
prior when it is not — but note that the *statistics* underneath is honest and priorless; the
story is the labeling stage, not the engine. Ayurveda's stories are "wrong" at the explanation
level (heat / spirits / energy) and it does not matter, because its *carvings* are candidate
constraints, never authority. If you find yourself defending OR debunking traditional medicine,
you have left the program.

**"n=1 consumer genetics can't establish anything."** Correct, and the program says so first
(canon §11, Warning 2): the index case is a sampling-frame specification, not evidence.
Re-raising it is canon §12.3, not rigor.

**The one escape hatch:** the founder may deliberately place a small bounded model — or a single
statistical test as a cheap search-order prior — at some tail. That is the founder's explicit
call, named as a bounded utility, never your default, never the method, never "the architecture."

## The gate — every time, before proposing ANY approach

1. Read this file → `docs/THEORY_OF_THE_CASE.md` (the derived design + the Part V pathology
   record) → `docs/REGULATORY_DEFICIT_PROGRAM.md` (founding canon, authoritative; its Appendix C
   is the cold-pickup anti-pattern list).
2. **Restate the mechanism in your own words** and have the founder confirm it — the test is not a
   fluent paraphrase, it is: *is the coherence measure σ (a Blum measure) and not a statistic; is
   the object GROWN by the search (node birth/death) and not authored/seeded; are the constraints
   TRIANGULATED across several partly-orthogonal lenses (generate-not-calculate), never read off one
   map's shape; does the σ_sem > 0 guard hold so it cannot collapse into SDIS-style self-confirmation;
   and does it stop at the κ-knee?* If you cannot point at those, you have not understood it yet.
3. **The object is GROWN by the search, NEVER authored or seeded.** The mechanism graph is computed
   by node birth/death from the data geometry (LAW 3) — it is not a hand-written edge list, and
   seeding it (a PBS pile, a generic interactome, **SDIS's edges**) is the root of the 2026-08-30
   death (canon §12.14, §15). SDIS is a *characterization target*, never the object. What is still
   open is the object's **content** (grown, once the data is in hand) and the **data** itself
   (co-variation + co-presentation, §12.4) — not the architecture, which is confirmed (Part II).
4. Never reframe the coherence design as statistics-with-extra-steps. Never rank by a
   frequency/association/differentiation/participation score as the answer. Iterate the
   **constraint graph / the coherence object / the encoder**, never "a better statistic."

## Working method

- The founder's global two-step governs: DIAGNOSE symbolically (Serena, never grep Python
  source) before touching anything; PIN behavior after (Detective converge on pure decision
  functions). Genomics reference machinery: `~/Projects/genomevault`. Coherence engine:
  Regenesis (`mcp__Regenesis__*`). The built coherence-instrument primary sources are in canon
  Appendix B (harmonizing, genomevault, Peitho, COEC) — read those, not a summary.
- **Laws live in `docs/THEORY_OF_THE_CASE.md` Part IV** and in the always-loaded `CLAUDE.md`.
  Check `decisions/` before architectural changes.
- `~/Projects/Predecessor_Study` is SUBSUMED — crosses only by re-derivation via
  `docs/SALVAGE_MANIFEST.md`, never by copy.

Canonical, fully-worked example of this apparatus:
`~/Projects/Kaggle_Killer/competitions/RSNA_Knee/` and the portfolio reference
`~/Projects/Kaggle_Killer/DATA_GEOMETRY_ARCHITECTURE.md`. Global law: `~/.claude/CLAUDE.md`
("AI IS NOT ML" — here, sharpened to "AI IS NOT STATISTICS").

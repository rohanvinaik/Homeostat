# For agents (and humans) arriving fresh — read before proposing anything

## ⛔ THE LOAD-BEARING LAW: DATA-GEOMETRY, NOT STATISTICS

Homeostat is a **classical-AI data-geometry** project. Its method is finding
**information-theoretic coherence — combinations of sub-threshold signals that hang
together** — in the *geometry* of the data. It is **NOT statistics.** A statistical
test (a frequency, an association, an enrichment, a population-differentiation score,
a network hub-score) is at most **one cheap input among many**; it is **NEVER the
method, never the significance, never the object of study.**

**This is the deeper law, and "not ML" was necessary but not sufficient.** An earlier
version of this file said *"population-genetic statistics (PBS, iHS, enrichment tests)
… are welcome"* — that line was the poison, and it licensed the entire failed arc of
2026-08-30 (Part V of `docs/THEORY_OF_THE_CASE.md`). The drift here does not arrive
dressed as a neural net. It arrives dressed as **respectable statistics** — the "cheap
hack that substitutes for actual engagement with the problem," in the founder's words.
The word that should trigger your alarm is not only "model" but **"significant,"
"enriched," "associated," "frequency," "p-value," "hub."**

**Why statistics is the wrong genus here (the whole thesis, in one paragraph).** The
phenotype is produced by a *combination* of sub-threshold signals. The loud,
statistically-obvious signals (the dopamine genes for a polygenic condition; the classic GWAS hits)
**drown out** the other etiologies, whose contribution exists only in composition and
therefore never clears a frequency threshold in isolation. Statistics can only tell
you "gene X appears in 87% of condition Y." It structurally *cannot* see a mechanism
that exists only as a coherent combination of quiet parts. So the method is not
statistics at all — it is **data geometry**: treat the data as a geometric object,
find the local **entropy minima / points of information-theoretic coherence**, and
read that coherence *itself* as the evidence of mechanism. **Improbable-AND-coherent,
not frequent.** The coherence is the signal (canon §2, §3, §5; the significance layer
§5.1 "surprise = −log P turned inward"; the informational zero §5.4).

**Four different things, never collapsed:**
- **AI** — the genus (reasoning, representation, symbolic and vector-symbolic computation).
- **ML** — one narrow, avoidable species (gradient-fit models).
- **Statistics** — a *tool* (a cheap prior, a narrowing input), **not a genus of method**
  and never the architecture. This is the species that poisons THIS project.
- **Classical AI / data-geometry** — OTP, Informational Zero, COEC, GSE, HDC, the
  κ-coherence engine (Regenesis). **The architecture here.** (Portfolio reference:
  `~/Projects/Kaggle_Killer/DATA_GEOMETRY_ARCHITECTURE.md`.)
- **Story-understanding intelligence** — Regenesis (Winston's Genesis, ported). A
  diagnosis is a *story* laid over data (see below), and this is the engine for it.

**Know your own bias (this is why the gate exists).** You — and LLMs generally — reach
reflexively for statistics on any genomics/medicine problem, because the training
corpus equates "rigor" with "a p-value." It *feels* like domain knowledge; it is a
prior overriding what the founder specified. The tells: "is this enriched vs a matched
background?"; "let's rank by the differentiation statistic"; "the bridges are the
network hubs"; "we need a significance test for that." Every one of those is the drift.
When a result plateaus, the first hypothesis is **"the data geometry is wrong / the
coherence object is missing,"** never "add a better statistic."

## The two misreadings that also kill this project

**"This is a traditional-medicine project."** No (canon §12.6, classification-first
reading). Ayurveda enters for ONE technical reason: it is a **causally independent,
empirically battle-tested source of carvings** — a decorrelated *story* about how
sub-threshold things combine, uncontaminated by the allopathic statistical-diagnostic
frame. **The point about diagnosis:** the allopathic "diagnosis" is itself just a
post-hoc, motivated meaning-imposing stage — a Winston-style *story* about what the
data means — treated as ground-truth prior when it is not. Ayurveda's stories are
"wrong" at the explanation level (heat / spirits / energy) but that does not matter,
because they were built from centuries of raw outcome-feedback groping at exactly the
combinatorial mechanisms statistics cannot see. It is a prior on combination, never an
authority. If you find yourself defending OR debunking traditional medicine, you have
left the program.

**"n=1 consumer genetics can't establish anything."** Correct, and the program says so
first (canon §11, Warning 2): the index case is a sampling-frame specification, not
evidence. Re-raising it is canon §12.3, not rigor.

**The one escape hatch:** the founder may deliberately place a small bounded model — or
a single statistical test as a cheap narrowing prior — at some tail. That is the
founder's explicit call, named as a bounded utility, never your default, never the
method, never "the architecture."

## The gate — every time, before proposing ANY approach

1. Read this file → `docs/THEORY_OF_THE_CASE.md` (the derived design + the Part V
   pathology record) → `docs/REGULATORY_DEFICIT_PROGRAM.md` (founding canon, verbatim,
   authoritative; its Appendix C is the cold-pickup anti-pattern list).
2. **Restate the mechanism in your own words** and have the founder confirm it — and
   the test is not a fluent paraphrase, it is: *where in what I am about to build does
   the coherence-of-a-combination live, and where have I substituted a statistic for
   it?* If you cannot point at the geometry, you have not understood it yet.
3. Never reframe the data-geometry / coherence design as statistics-with-extra-steps.
   Never rank by a frequency/association/differentiation score as the answer. Iterate
   the **encoder / the geometry / the coherence object**, never "a better statistic."

## Working method

- The founder's global two-step governs: DIAGNOSE symbolically (Serena, never grep
  Python source) before touching anything; PIN behavior after (Detective converge on
  pure decision functions). Genomics reference machinery: `~/Projects/genomevault`
  (GDiff, HDC/OTP, superposition reference). Coherence engine: Regenesis (`mcp__Regenesis__*`).
- **Laws live in `docs/THEORY_OF_THE_CASE.md` Part IV** and in the always-loaded
  `CLAUDE.md`. Check `decisions/` before architectural changes.
- `~/Projects/Predecessor_Study` is SUBSUMED — crosses only by re-derivation via
  `docs/SALVAGE_MANIFEST.md`, never by copy.

Canonical, fully-worked example of this apparatus:
`~/Projects/Kaggle_Killer/competitions/RSNA_Knee/` (and the portfolio data-geometry
reference `~/Projects/Kaggle_Killer/DATA_GEOMETRY_ARCHITECTURE.md`). Global law:
`~/.claude/CLAUDE.md` ("AI IS NOT ML" — here, sharpened to "AI IS NOT STATISTICS").

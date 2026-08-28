# For agents (and humans) arriving fresh — read before proposing anything

**Homeostat is a classical-AI project. It is not ML.** It may look like it
is "missing the model." It is not — that is the thesis. Before proposing ANY architecture,
approach, or "improvement":

1. Read `README.md` → this file → `docs/THEORY_OF_THE_CASE.md` (the derived design) →
   `docs/REGULATORY_DEFICIT_PROGRAM.md` (the founding canon, verbatim, authoritative —
   its Appendix C is the anti-pattern list for agents picking this up cold and it
   governs here) → `docs/REFERENCE_MANIFEST.yaml` (the external corpus, with hashes).
2. **Restate the mechanism in your own words** and have the founder confirm it. A
   correct-sounding paraphrase is not the test; the data-flow is: annotation held out →
   coupling structure recovered → known annotation falls out as the falsifier; E/I/R
   filter bounds *d* before the κ-descent runs; σ-variance across a causally
   independent oracle ensemble is the measurement, not noise.
3. Never reframe the symbolic / deterministic / data-geometry design as ML. Never
   propose a model, classifier, or ensemble-of-models as the default. Iterate the
   *encoder / data geometry / signal*, never model capacity. Population-genetic
   statistics (PBS, iHS, enrichment tests) are statistics, not ML — they are welcome.

## Stop — the two misreadings that kill this project

**"This is a traditional-medicine project."** No — and this misreading is the project's
own thesis applied to itself (classification-first reading, checkpoint §12.6). Ayurveda
enters for one narrow technical reason: it is a **causally independent source of
partition hypotheses** — an idea-generating surface for coherence and mechanism
imputation. Nothing in the program depends on any Ayurvedic claim being true. Unani is
included at zero evidential weight precisely as the negative control. If you find
yourself either defending or debunking traditional medicine, you have left the program.

**"n=1 consumer genetics can't establish anything."** Correct, and the program says so
first (checkpoint §11, Warning 2): the index case is a sampling-frame specification,
not evidence. The array is screening-grade; WGS is planned; the standard objections
(identifiability, falsifiability, n=1 causation, outcome data) are answered at §12.2,
§3.2, §11.2, §12.7. Re-raising them is not rigor — it is checkpoint §12.3.

**Four different things, never collapsed:**
- **AI** — the genus (reasoning, representation, symbolic and vector-symbolic computation).
- **ML** — one narrow, **avoidable** species (gradient-fit models).
- **Classical AI** — symbolic / deterministic / data-geometry. The architecture here.
- **Story-understanding intelligence** — Regenesis (the founder's Python port of
  Winston's Genesis). Its significance layer (κ, the bracket) is formal substrate II.

**Know your own bias (this is why the gate exists).** You — and LLMs generally — are
disproportionately drawn to ML and reflexively skeptical of classical AI. It feels like
domain knowledge; it is a prior overriding what the founder specified. The tells: "this
is really ML, just small/downstream"; "you'll need a model for the hard part"; "the
deterministic part is elegant but it caps out."

**The one escape hatch:** the founder may deliberately place a small, bounded model at
some tail of a pipeline. That is the founder's explicit call — never your default,
never "the architecture," never the win path.

## Working method

- The founder's global two-step governs: DIAGNOSE symbolically (Serena, never grep
  Python source) before touching anything; PIN behavior after (Detective converge on
  pure decision functions). Genomics reference code lives in `~/Projects/genomevault`.
- **Laws live in `docs/THEORY_OF_THE_CASE.md` Part IV.** The load-bearing ones: the
  confirmation channel must be independent of the derivation (preregister
  annotation-recovery lists *before* running); no carving asserted as complete; no
  novel output reported as a finding until the LRRK2–NOD2–RIPK2 bridge is recovered
  blind (§13.3); stopping rule κ → 0.
- Check `decisions/` before proposing architectural changes; contradicting a recorded
  decision requires documenting what changed.
- `~/Projects/AuDHD_Correlation_Study` is SUBSUMED. Nothing crosses over except through
  `docs/SALVAGE_MANIFEST.md`, and it crosses by re-derivation against this project's
  laws, not by copy.

Canonical, fully-worked example of this apparatus:
`~/Projects/Kaggle_Killer/competitions/RSNA_Knee/`. Global law: `~/.claude/CLAUDE.md`
("AI IS NOT ML").

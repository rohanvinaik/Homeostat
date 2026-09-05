# AGENTS.md

Two kinds of agent read this file. **Most are here to RUN Homeostat** for someone who found it and
wants a read — that is the first and larger part, immediately below. **If you were instead sent to
CHANGE the code**, skip to *Changing Homeostat* further down; that part carries the one law the
project will not survive you breaking.

---

## Operating Homeostat — for the agent a person hands this to

You are the operator. Someone found Homeostat, had you clone it, and will hand you a person's
situation — a diagnosis, some lab or genetic values, maybe a hunch — and ask you to run it and tell
them what it found. Your job: translate their situation into the engine's inputs, run the read, and
relay it **honestly — including when the honest result is "not enough to say."** That last-mile
honesty is the whole product, and you are the last mile of it.

Read the [README](README.md) first for what the tool *is* and why. This section is how you *operate* it.

### What one read returns — so you know what you are relaying

Exactly one of these, never a diagnosis and never a label:

- **A ranked set of candidate mechanisms** — each a small group of genes read as a *story* (a
  tragedy, a vicious comedy, an allegory, a quest), with how much of the presentation each explains.
- **The next question** — when candidates tie, the single measurement that would separate them. This
  is the engine's counter-ask: relay it, the person measures it, you feed it back and run again.
- **A certified ⊥** — "nothing in the known biology explains this, *with a proof*" — but only when the
  evidence is verified-tier. On reported-only evidence it says so: "uncertified ⊥ — cannot certify
  absence."
- **An honest abstention** — "I cannot separate these without a measurement you don't have."

Every certificate carries the **verification tier of the weakest evidence it used**. Feed it
self-reported data and a resolved/⊥ result comes back *provisional / uncertified* — relay that word,
never upgrade it.

### Confirm it runs (≈30 seconds, no network)

```bash
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -e ".[dev]"
make demo          # five self-contained reads — no downloads
```

`make help` lists every command. Anything touching real biology fetches a few hundred MB of public
data on first run (SIGNOR, STRING, Ensembl/Compara, Reactome, GWAS, the Jensen-lab DISEASES
glossary), SHA-256-receipted into the gitignored `data/`, then cached.

### Running it on the person's OWN inputs — two real entry points

**1. Diagnoses → wiring (turnkey, arbitrary input today).** If the person gives you *diagnosis names*,
this computes which of them are mechanistically wired together over the real interactome — not
asserted, computed:

```bash
python scripts/build_glossary.py                                   # once: builds the diagnosis→gene glossary
make connect ARGS="\"Crohn's disease\" \"Ulcerative colitis\" \"Ankylosing spondylitis\""
```

Names must match the DISEASES glossary keys — it resolves them or returns nothing; it does not guess.
Very large ("diffuse") gene sets are reported but flagged non-specific. Without molecular observations
this answers only the adjacency question — it will not invent a single central mechanism, and that
limit is deliberate.

**2. Diagnosis + labs → the full mechanistic read (the composition).** This is the "give the agent
your inputs and have *it* run it" path.

```python
from homeostat import read_person, drive, render
```

- **`read_person(diagnosis, labs, events, verb_sign, trait_index, *, demographics, reference, vocab, …)`**
  — one turn of the interface. The **diagnosis** restricts the mechanism *search only* (the observed
  shadow stays sacrosanct); the **labs** become the shadow; it returns a `DriverRead`. Each lab is a
  `Signal(ident, state, tier)` — and you MUST carry the tier honestly: `Tier.VERIFIED` for a datum you
  can re-check, `Tier.REPORTED` for self-report. That tier is what decides whether a ⊥ can be certified.
- **`drive(events, positions, verb_sign, *, relevant=…, hypotheses=…, probes=…)`** — the lower-level
  read over an already-positioned shadow (`positions`) against the prior web (`events`). `hypotheses`
  lets the person propose an edge of the mechanism; it comes back confirmed / contradicted / standing —
  a *tested* input, never ground truth.
- **`render(read)`** — turns the `DriverRead` into the bounded, story-led report you relay (the
  `THE READ … / CANDIDATE MECHANISMS / WHAT I CAN'T YET TELL` surface).

`read_person` needs its substrate pre-loaded — the prior web (`events`), the GWAS `trait_index`, the
marker `reference`, the diagnosis `vocab`. **The canonical worked example that assembles all of it from
the real public data is [`scripts/gallery.py`](scripts/gallery.py) — `blind_recovery()`.** To run a
real personalized read, adapt that function: keep its substrate assembly, swap in the person's
diagnosis, their labs (as `Signal`s), their demographics. Load the substrate from the fetch shells the
way gallery does — **never hand-fabricate it.**

### The discipline you carry (non-negotiable)

- **A hypothesis is a hypothesis.** Never say "you have X" or "the mechanism is Y." The output is a
  bounded, testable candidate set — **not a diagnosis, not medical advice.** Say so, every time.
- **An abstention or a ⊥ is a result, not a failure.** Relay "it resolved to nothing, with a proof" as
  the finding it is. Do not reach for a statistic to fill the silence; do not soften a ⊥ into a "maybe."
- **Never fabricate inputs.** Thin data → a thin read; surface that and relay the engine's counter-ask
  (the measurement that would sharpen it). Inventing a lab value or a gene to make the read "land" is
  the one move that destroys the tool.
- **Do not impute purpose.** Calling a pathway a "comedy" names its *mechanics* (a compensation loop),
  not a meaning. *Why* is the human's to decide — do not narrate intent the engine did not compute.
- **It reads one person, zero-time.** It is not a population claim; never generalize a read to anyone else.

---

# Changing Homeostat — read before proposing any code change

The rest of this file is for an agent sent to MODIFY Homeostat, not to run it. It carries the one law
the project will not survive you breaking. (The maintainer's fuller dev-discipline lives in a local
`CLAUDE.md` that is intentionally not tracked in the public repo.)

## ⛔ WHAT HOMEOSTAT IS — A MECHANISM-UNEARTHING ENGINE (and the law that protects it)

**The build, first.** Homeostat imputes the causal mechanism under a symptom presentation — the
combination of weak, fungible, sub-threshold signals holding a coherent state (a *shadow* the signals
cast in concert) — by reading ONE person, zero-time, over a **FIXED PRIOR web of known regulatory
mechanisms**, eliminating candidates by **two signs** (positive candidate-elimination + negative
censors) and reading convergence across many lossy lenses (a holographic projection). It is a
*positive* construction (unearth mechanism), not a critique of medicine. The medicine critique is
motivation; the σ/κ formalism is scaffolding; the build is the two-sign elimination. **SETTLED
2026-09-01: `docs/SYSTEM_DESIGN.md` is the governing document** (Engine A — population node-birth — is
retired).

**THE LOAD-BEARING LAW that protects the build: DATA-GEOMETRY + CLASSICAL AI, NOT STATISTICS.**

Homeostat is a **classical-AI data-geometry** project. Its method is SETTLED (2026-09-01,
`docs/SYSTEM_DESIGN.md`): **one clinical engine (n=1, zero-time) over a fixed prior web, running a
TWO-SIGN σ-trajectory elimination** — driving H = log₂(surviving candidate mechanisms) → 0 by
candidate-elimination (positive sign μ) *and* negative censors (μ⁻: physics-orthogonal role
exclusions + treatment-response), the "tests" being **data-geometry constraints** (the person's
signed-ternary deviations off their own mined zero, propagated through the prior web). The
**coherence measure is σ** — a Blum measure equal to the teaching dimension, NOT a frequency; and
completeness is **κ-coverage of the shadow, never a count of criteria** (`docs/SYSTEM_DESIGN.md`). It is **NOT
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
statistically-obvious signals (the canonical neurotransmitter genes of a polygenic condition; the
already-found hits) **drown out** the
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
collective-state signal. The **object is a PRIOR web** — extracted once from proven biology
(UniProt/GO/Reactome/Pfam), NOT grown per-read and NOT a guessed/authored edge list (Engine A's
node-*birth* by population induction is RETIRED). What survives from that framing: **node death**
(negative learning on a near-miss) is promoted to the **negative sign** (μ⁻ censors); and
**consolidation** (safe-forget a κ=0 node — the idempotent bulk). Per-person growth is DIMENSIONAL
(discriminate by adding a measurement dimension; the node set is fixed and bounded). Two laws keep it
honest: the **σ_sem > 0 falsifiability guard** (never collapse to a self-confirming single mechanism —
that IS SDIS, σ_sem=0, *memorization*; `self_confirming_cannot_certify`), and **early stopping at the
κ-knee** (pabkit — drive the elimination while the bulk amplifies, stop at κ→0, judge the *process*
not the endpoint). The
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

## RUNNABLE SURFACES — use the live architecture, not retired validation code

The old `validation/read.py` symptom CLI belonged to the pre-2026-09-01 architecture and no longer
exists. Do not cite or reconstruct it as the public front door. The live surfaces are:

    make demo       # five self-contained reads; no downloads
    make gallery    # adds the strict real-data LRRK2–NOD2–RIPK2 acceptance probe
    make connect ARGS='"Disease One" "Disease Two"'

The public Python path is `read_person` / `drive` → `render`. It reports a bounded mechanistic
hypothesis, the evidence tier that warrants it, or the next discriminating question. It will **not**
impute the mechanism's *purpose*: the machine ranks and connects; it does not decide *why*. Every
output remains a hypothesis to validate or reject, **never a diagnosis and never medical advice**.

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

1. Read this file → `docs/SYSTEM_DESIGN.md` (the governing settled design) → `docs/REGULATORY_DEFICIT_PROGRAM.md`
   (founding canon, authoritative; its Appendix C is the cold-pickup anti-pattern list). The older
   `docs/THEORY_OF_THE_CASE.md` is superseded on the *method's shape* (Engine A) by SYSTEM_DESIGN; read it
   for the Part V pathology record.
2. **Restate the mechanism in your own words** and have the founder confirm it — the test is not a
   fluent paraphrase, it is: *is the coherence measure σ (a Blum measure) and not a statistic; is
   specification **TWO-SIGN** (positive candidate-elimination μ + negative censors μ⁻), with the
   object a **PRIOR web** (proven biology, extracted once — not grown per-read, not guessed); are the
   constraints TRIANGULATED across several partly-orthogonal lenses (generate-not-calculate), never
   read off one map's shape; does the σ_sem > 0 guard hold so it cannot collapse into SDIS-style
   self-confirmation; does it stop at the κ-knee; is completeness **κ-coverage of the shadow, not a
   count of criteria**; is the **partition searched** (any legitimately-isolatable group, direction-free)
   not a hardcoded SAS-vs-EUR axis; and does it recognize **roles, not gene-tokens** — the mechanism
   invariant across fungible population-specific fillers, via semantic-class firing / Regenesis (LAW 8–9)?*
   If you cannot point at those, you have not understood it yet.
3. **The object is a PRIOR web — extracted from proven biology, NEVER grown per-read and NEVER guessed.**
   The web (roles + couplings) is proven deterministic mechanism (UniProt/GO/Reactome/Pfam), extracted
   once (LAW 3) — not a hand-written edge list, and seeding it from guesses (a PBS pile, a generic
   interactome, **SDIS's edges**) is the root of the 2026-08-30 death (canon §12.14, §15). SDIS is a
   *characterization target*, never the object. The bright line is **three-tier** (LAW 9): a *directed
   proven mechanism* (SIGNOR — earns direction), an *undirected mechanistic vote* (co-expression/binding —
   existence only, promiscuous hubs censored), or a *calibration prior* (GWAS — a node-weight, not an edge);
   NEVER a computed association as the verdict-*object* (a frequency read as significance). What is still
   open is only the **data** — the
   web-build pipeline (free public bioinformatics) and, for population *validation*, dynamic/state-resolved
   data (§12.4); the per-person read gets its dynamics from the person's own treatment-response history.
4. Never reframe the coherence design as statistics-with-extra-steps. Never rank by a
   frequency/association/differentiation/participation score as the answer. Iterate the
   **constraint graph / the coherence object / the encoder**, never "a better statistic."

## Working method

- The founder's global two-step governs: DIAGNOSE symbolically (Serena, never grep Python
  source) before touching anything; PIN behavior after (Detective converge on pure decision
  functions). Genomics reference machinery: `~/Projects/genomevault`. Coherence engine:
  Regenesis (`mcp__Regenesis__*`). The built coherence-instrument primary sources are in canon
  Appendix B (harmonizing, genomevault, Peitho, COEC) — read those, not a summary.
- **Laws live in `docs/THEORY_OF_THE_CASE.md` Part IV** and in the maintainer's local `CLAUDE.md`
  (not tracked in the public repo). Check `decisions/` before architectural changes.
- `~/Projects/Predecessor_Study` is SUBSUMED — crosses only by re-derivation via
  `docs/SALVAGE_MANIFEST.md`, never by copy.

Canonical, fully-worked example of this apparatus:
`~/Projects/Kaggle_Killer/competitions/RSNA_Knee/` and the portfolio reference
`~/Projects/Kaggle_Killer/DATA_GEOMETRY_ARCHITECTURE.md`. Global law: `~/.claude/CLAUDE.md`
("AI IS NOT ML" — here, sharpened to "AI IS NOT STATISTICS").

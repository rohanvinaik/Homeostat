# Conceptual Audit — Homeostat vs. its own spec (2026-09-01)

*Primary-source audit, traced from code with Serena, not from the docs' claims. The finding is
uncomfortable and load-bearing: the intended data-geometry method is built, tested, and **orphaned**,
while the live read-paths drift into exactly the statistical genus the project exists to defeat.*

> **Note (2026-09-01, post-design):** the *wiring findings* below (the orphaned σ-engine, the statistical
> live-paths, `kappa.py`'s topology statistics) remain accurate and still drive the build. But where this
> audit describes "the intended method" as **node birth/death growing a mechanism graph** (§1, §5.2), that
> framing is **Engine A, retired** — see `docs/SYSTEM_DESIGN.md` (the governing doc): the node set is a
> fixed prior web, specification is **two-sign**, and per-person growth is dimensional. The re-architecture
> in §5 is correct in genus (wire the σ-engine, ground resolution, demote lenses, retire the p-value); read
> it as "positive-sign," with SYSTEM_DESIGN §12 adding the negative-sign censor layer and the OTP positioning
> core as the next build.

---

## 1. The spec (the intended design, from `AGENTS.md` cardinal law + `THEORY_OF_THE_CASE.md`)

The method is supposed to be **data-geometry + classical AI, never statistics**:

- **Grow, don't score.** A candidate mechanism graph is *grown* by **node birth / death** and
  parsimony-searched — the **σ-trajectory**: drive H = log₂(surviving candidate mechanisms) → 0 by
  **candidate elimination** against data-geometry constraints.
- **Coherence, not frequency.** The measure is **σ** (a Blum measure = teaching dimension) and
  **chain-κ** (improbable-yet-coherent significance over the *rule* graph) — **not** a p-value, **not**
  an enrichment, **not** a frequency.
- **Roles, not tokens.** Recognition is **Regenesis** semantic-class firing (what a gene *does*), with
  the **informational zero** for abstention, the **σ_sem > 0** guard against self-confirmation, and
  **κ-knee** parsimony halting.
- Named forbidden, verbatim: *"a frequency, an enrichment, a population-differentiation score, a
  network hub/participation score … is at most one cheap search-order prior; NEVER the method … NOT
  κ/participation over a generic network (a topology statistic in disguise — Act 2 of the death)."*

## 2. The verified wiring (Serena `find_referencing_symbols`, not the docs)

| intended-method component | file / symbol | who actually calls it |
|---|---|---|
| **σ-trajectory parsimony search** | `search.py::sigma_trajectory` | `loop.py` + **tests only** |
| **the parsimony loop** (birth/death, κ-knee, budget) | `loop.py::run` | **`tests/test_loop.py` only — ZERO production consumers** |
| **coherence-κ** (improbable-yet-coherent) | `kappa.py::chain_significance` | **`tests/test_kappa.py` only — ZERO production consumers** |
| node birth convergence | `nodes.py::node_status` | `grow` (wired — but only as a ≥2-lens count, not the σ-search) |
| Regenesis role-recognition | mechanism universe | wired (the one on-thesis live piece) |

**The core of the intended method is orphaned scaffolding.** `run` and `sigma_trajectory` (the whole
Peitho σ-trajectory / node-birth-death engine) and `chain_significance` (the coherence measure that is
supposed to *replace* significance) are fully built and unit-tested and **nothing in a live path calls
them.** The memory/doc claim "data-geometry engine BUILT end-to-end" is true at the *unit* level and
false at the *wiring* level.

And `kappa.py` — the file named for the coherence measure — literally contains `pagerank`,
`personalized_pagerank`, `is_bridge`, `coverage`, participation: **the topology statistics the canon
names as "Act 2 of the death,"** sitting in the same module as the intended `chain_significance`.

## 3. What the live paths actually do (the genus-violation, in three layers)

**a) The mechanism read** (`probes/l2_lrrk2` → `grow` → `l2_encoder` → Regenesis). Partly on-thesis
(Regenesis role-recognition + the informational zero *are* the right genus), but its **lenses are
statistics used as the signal**: **Fst = population-differentiation** (forbidden *by name*), GTEx
co-expression = a correlation, STRING binding = network participation. These are fed as the read's
evidence, not demoted to a cheap prior. `grow` is STRING-neighbor expansion gated by a ≥2-lens count —
a convergence *heuristic*, not the σ-trajectory parsimony search.

**b) The symptom-read CLI** (`validation/read.py`) — the newest and worst offender, and it is **mine**.
It uses **GWAS gene sets** (frequency), a **STRING bridge** (network participation — "the topology
statistic in disguise"), and a **degree-matched permutation null → p-value** (significance-as-method).
It touches **none** of the engine. It is a network-enrichment-with-a-null tool wearing a mechanism
reader's coat — the exact drift `CLAUDE.md` flags as my reflex ("is this enriched vs a matched
background?").

**c) The coherence measure is absent from both.** Neither path computes σ or chain-κ; the p-value
stands in for coherence, which is the precise inversion the spec forbids (improbable-AND-coherent, not
frequent).

## 4. Why the mechanism reveal fails (the consequence, not a coincidence)

- **It builds from the loud genes.** GWAS sets *are* the already-found single-locus signals your canon
  says **drown out** the quiet combinatorial etiology — so the bridge surfaces generic signaling hubs
  (HSP90B1/AKT1/TRAF6) and calls them the read.
- **It asks the wrong question.** "Denser than *chance frequency*?" A meta-stable coherent state among
  fungible weak elements is *not frequent by construction* — so the honest p≈1.0 is the tool correctly
  measuring the wrong quantity. σ is the right quantity, and it is never computed.
- **No graph is grown.** The presentation never becomes a *searched, parsimonious mechanism graph*; it
  stays a fixed STRING neighborhood with a significance test bolted on.

## 5. The principled re-architecture — mostly WIRING, not rebuilding

The good news the trace also delivers: the right engine **exists and is tested**. The job is to connect
it and retire the statistical bypass.

1. **Resolution (grounding, not substring).** Map a symptom → canonical medical entity via a
   SymbolicSpellCheck-style **ground-or-abstain** gate over a medical vocabulary (HPO/DISEASES/UMLS
   synonyms + the GSE entity substrate). Kills the substring-collision class (a short symptom
   abbreviation matching a longer unrelated word) *and* is itself a data-geometry move (grounding +
   informational-zero abstention). No hard-coded conditions.
2. **Grow the mechanism, don't score a network.** From the resolved presentation, run the **seedless**
   `resolve_presentation` / `eliminate_to_survivor` (built 2026-09-01) — node birth/death growing a
   candidate mechanism graph, σ-trajectory parsimony (H→0) against the lenses **as elimination
   constraints**, κ-knee halt. There is **no protected target**: the survivor of elimination *is* the
   mechanism, computed **zero-time on the one person** (Peitho on one body — not population-dependent;
   see canon §0 Warning 2). This is wiring the orphan in, not writing it.
3. **Coherence replaces significance.** Score the surviving mechanism with **`chain_significance`** (σ /
   improbable-yet-coherent over the grown rule graph). **Delete the permutation p-value from the read
   path entirely** — it is the genus violation in one line.
4. **Roles via Regenesis** (already wired) + **abstain via the informational zero** (`signal.py` /
   `otp.py`).
5. **Demote the lenses.** Fst / co-expression / STRING stop being "the signal" and become **constraints
   the σ-search eliminates against** (data-geometry genus). Then **add the data-geometry banks** the
   biodata affords — vitals as an autonomic **signal-trajectory**, treatment-response as a
   **propagation** (one drug, many symptoms resolve → shared target), labs as **deviation-from-setpoint**
   — composed by Wayfinder's `confidence_weighted` product (`∏ scoreᵢ^confᵢ`) for graceful degradation.
   Same multi-bank architecture, opposite genus: readings, not enrichment scores.
6. **Quarantine the topology statistics.** `kappa.py`'s `pagerank`/participation are either purged or
   explicitly relegated to "cheap search-order prior," never the coherence measure and never `κ`.

## 6. The honest bottom line

The project's own law says the coherence engine is the method and statistics is at most a prior. The
code does the reverse: the coherence engine (`sigma_trajectory`, `run`, `chain_significance`) is
orphaned, and frequency/participation/significance run the live reads. **The re-architecture is
therefore a realignment, not a rewrite** — wire the σ/κ engine into a seedless presentation-grower,
make coherence (not a p-value) the verdict, ground the resolution, demote the lenses to constraints,
and retire `read.py`'s statistical path. The parts that are on-thesis today (Regenesis roles, the
informational zero, node-birth convergence) survive; the statistical scaffolding I and the free-data
plumbing accreted comes out.

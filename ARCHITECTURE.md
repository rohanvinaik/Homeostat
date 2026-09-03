# Homeostat — Architecture (as-built wiring map)

**Status:** Canonical engineering map (2026-09-04), companion to `docs/THESIS.md` and
`docs/SYSTEM_DESIGN.md` (the *why*; this is the *what and how*). Traced from source — the AST import
graph + the language server (references, call graph), not memory. **It is the definition of the live
system: anything not reachable here is, by construction, archive/rejected residue (see §9).**

**Legend:** ✅ built and pinned (Detective-complete + intent-tested) · 🔧 built, refinement flagged ·
⬜ designed, not yet wired · ⛔ superseded/rejected (removed or archive-bound).

Homeostat is a per-person, **zero-time, two-sign elimination read** over a multi-network coupling web.
A disease is a *shadow* — a sub-threshold combination of deviations that no single criterion names.
The engine reads *one person's* deviations against a prior web of couplings and **eliminates** candidate
mechanisms to a survivor, a certified ⊥ (a proof of "no such mechanism"), an honest abstention, or the
next discriminating question. It reads a FROZEN world and adds nothing of its own (Law 11); its
significance is κ (coverage of the shadow), never any statistic (Law 1).

---

## 1. System overview

```
   FRONT DOOR   ✅ ground — symptom text → concept | abstain (SymbolicSpellCheck, no guess)
   ──────────────────────────────────────────────────────────────────────────────────────
   L5  READ      ✅ genres (tragedy/comedy) · ✅ fungibility (+ structural eliminator)
                 ✅ story→Regenesis roles · ⬜ Regenesis generate-wide IN-LOOP · ⬜ the DRIVER
   L4  ENGINE    ✅ eliminate_two_sign → clinical_verdict (BOTTOM/RESOLVED/DEGENERATE/ASK/ABSTAIN)
   L3  POSITION  ✅ per-person signed-ternary off the mined zero + discrimination guarantee
                 ⬜ the positions PRODUCER (genotype/state → Position; signal-tier feed)
   L2  BANKS     ✅ 4 global edge (signor/string/homology/metabolic) · ✅ 2 scoped (coexpr/trait) ⬜wire
   L1  EVENT     ✅ the one typed contract: Event → events_to_web + events_to_censors/active_censors
   L0  SUBSTRATE ✅ otp (ternary) · web (RelationalWeb/kill_matrix) · kappa · signal 🔧unwired · paths/util
   ──────────────────────────────────────────────────────────────────────────────────────
   ⬜ THE DRIVER: generate-wide (Regenesis over the multi-network story) → resolve-narrow
      (eliminate_two_sign). Zero judgment in the glue; the Reading is the only judge (Law 11).
```

The engine's judgment lives in exactly one place: the elimination read over the web + the Regenesis
role/mechanism derivation. Everything at L0–L4 is mechanical and pinned; L5 consumes it through the
typed `Event`/`ClinicalResult` contracts (§3).

---

## 2. Layer contracts

### L0 SUBSTRATE — ✅ (`otp.py`, `web.py`, `kappa.py`, `paths.py`, `util.py`) · `signal.py` 🔧
- **OWNS:** the signed-ternary algebra, the positive graph type, the reachability/κ machinery, IO paths.
- **`otp.py`** — `ternary` (value → {−1,0,+1} off a zero), `interference`/`tally` (the elimination
  primitive: a single opposing sign vetoes a pile of weak supports; "the Monty-Hall move").
- **`web.py`** — `RelationalWeb`, `Coupling(a,b,weight,direction)`, `kill_matrix(web, observed)`
  (candidates = the whole bounded node set; for each observed symptom `S`, `explains:S` kills every
  source that CANNOT reach `S` — the survivor is the mechanism), `reaches`/`web_adjacency`.
- **`kappa.py`** — `reachable`/`coverage`/`marginal_coverage`/`is_bridge`/`chain_significance` (κ =
  marginal coverage; the significance object, Law 4).
- **`signal.py`** 🔧 — `Signal(ident, state, tier)` + `Tier` (VERIFIED/REPORTED/…), the genotype-
  provenance tier. **Built + tested but wired to nothing** (§9): the intended person-genotype input the
  read presumes, awaiting its producer.
- **DOES NOT:** interpret. `paths`/`util` are IO-only.

### L1 EVENT — ✅ `event.py` (the one typed contract)
- **OWNS:** the L2 record every bank emits and every read consumes; the compilers to web + censors.
- **`Event(network, verb, subject, target, sign, mode)`** — `sign` = +1 assert / −1 censor / 0 abstain
  (coupling support, NOT regulatory polarity — activation/inhibition rides `verb`); `mode` = a peer
  κ-density channel marker.
- **`events_to_web`** → group by coupling, `couple_verdict(support, censor)` (coupling / **killed**
  (cross-network contradiction) / censor / abstain), draw only convergent-uncontradicted edges;
  direction = +1 iff a *directed* network asserts it (Law 5, 9-i).
- **`events_to_censors` → `active_censors(active_roles)`** — the role-scoped negative sign: a `sign<0`
  event rules its subject out FOR role `target`, fired only where that role is active.
- **Gate PASSED:** `couple_verdict`, `events_to_web`, `events_to_censors`, `active_censors` all pinned;
  `test_event.py`.

### L2 BANKS — ✅ 4 global edge, ✅ 2 scoped (⬜ driver-wired). The three-tier bright line (Law 9)
Each bank = a pure renderer (`X.py`) + an IO shell (`X_fetch.py`, data gitignored + sha-pinned).
| Bank | Tier (Law 9) | Module | Renders |
|---|---|---|---|
| regulatory | (i) directed proven mechanism — EARNS direction | `signor.py` | SIGNOR effect grammar → `amplifies`/`inhibits`, all `sign=+1` |
| physical | (ii) undirected mechanistic vote | `string.py` | STRING binding → undirected coupling votes |
| evolutionary | (ii) undirected / the fungibility seed | `homology.py` | Compara paralogs → `resembles` seeds |
| metabolic | (ii) undirected | `metabolic.py` | Reactome metabolic co-membership → `channels` |
| co-expression | (ii) — COMPUTES (dynamics not statistics) | `coexpression.py` | GTEx OTP co-deviation; ⬜ enters at the driver |
| trait-wiring | (iii) calibration prior — a NODE-WEIGHT, not an edge | `trait_wiring.py` | GWAS pleiotropy; ⬜ enters at the driver |
- **`prior_web.py`** — `all_events` assembles the 4 global edge banks → `build_prior_web` →
  `RelationalWeb`. The 2 scoped banks are NOT here (they enter per-gene-set at the driver).
- **Forbidden across all three (Law 9):** a computed association AS the object of the verdict
  (correlation drawn as an arrow, frequency AS significance). Significance is κ.
- **Gate PASSED:** every renderer's pure decision pinned; each fired on its real dump.

### L3 POSITION — ✅ `position.py` · the producer ⬜
- **OWNS:** the per-person placement — each measured property → signed-ternary off a **mined** zero
  (a norm computed from the data, never a fixed threshold), + the discrimination guarantee.
- **`Position`**, `mine_zero`, `deviation`, `signature`, `discriminates` (two operationally-different
  states MUST have different signatures; the fix for a collapse is a NEW orthogonal dimension, never a
  tuned threshold — Law 6).
- **⬜ The producer:** the person's genotype/state → `dict[node, Position]`. The read *takes* positions
  (object-led); nothing yet *produces* them from a real person (`signal.py` is the tier abstraction that
  feed will carry).
- **Gate PASSED:** `discriminates`/`position`/`mine_zero` pinned; `test_position.py`.

### L4 ENGINE (resolve-narrow) — ✅ `search.py`, `clinic.py`, `jeeves.py`
- **OWNS:** the two-sign σ-elimination and the clinical verdict.
- **`search.eliminate_two_sign(candidates, constraints, censors)`** — positive elimination (μ) ∧
  negative censors (μ⁻) driving H→0. Ends on: a unique survivor (the mechanism), a **certified ⊥** (a
  censor rules out the sole survivor = a proof of non-membership, checked FIRST), or a STUCK plurality
  (the selector's cue to add a dimension). Never empties on a positive constraint (the survivor IS the
  reading); a censor emptying it is ⊥, not failure.
- **`clinic.read_from_events` → `read_presentation`** — `observed_symptoms(positions)` (sign≠0 nodes;
  baseline abstains) → `kill_matrix(web)` → `eliminate_two_sign` → `select_probe` if stuck →
  `clinical_verdict(bottom, resolved, falsifiable, has_probe)`: **BOTTOM** (certified ⊥) / **RESOLVED**
  (unique survivor, σ_sem>0) / **DEGENERATE** (self-confirming, σ_sem=0, Law 7) / **ASK** (Jeeves has a
  discriminating probe) / **ABSTAIN** (no dimension separates the survivors, Law 10). → `ClinicalResult`.
- **`jeeves.py`** — `Probe`, `expected_information_gain`, `select_probe` (the STUCK-branch: which new
  dimension best discriminates the surviving plurality).
- **Gate PASSED:** `eliminate_two_sign`, `clinical_verdict`, `select_probe`, `kill_matrix` pinned;
  `test_search.py`, `test_clinic.py`, `test_jeeves.py`, `test_two_sign.py`.

### L5 READ (generate-wide) — genres/fungibility/story ✅ · Regenesis in-loop ⬜ · the DRIVER ⬜
- **✅ `topology.py`** — the shared genre substrate: `otp_combine` (merge → info-zero on disagreement),
  `signed_adjacency`.
- **✅ `tragedy.py`** — an amplify-cascade into an absorbing SINK; verdict by the OTP net-sign along the
  path (doomed / suppressed / indeterminate).
- **✅ `comedy.py`** — a mutual-regulation cycle; verdict by loop-gain sign (vicious / homeostatic / 0).
- **✅ `fungibility.py`** — the allegory layer: paralog role-equivalence EARNED by ≥2-bank convergence
  on shared partners (Jordan-vs-Jordan inverted, fan-IN), **GATED by the structural eliminator** (L4b):
  a fundamental physical conflict removes a merge, but structure NEVER promotes (Law 8; the coupling
  convergence carries the positive, the read decides).
- **✅ `story.py`** — the L2→L3 bridge: events → opaque-token SVO for Regenesis, which fires ROLES over
  `universes/mechanism/` by semantic class on physically-real centroids (Law 8), never gene tokens.
- **⬜ Regenesis generate-wide in-loop** — derive the implied candidate mechanisms + roles + trajectory
  from the multi-network story, feeding the resolve-narrow engine.
- **⬜ THE DRIVER** — the generate-wide → resolve-narrow orchestrator (ported near-1:1 from Detective's
  `converge`): where the scoped banks (co-expr/trait) enter, fungibility folds, the genres fire,
  Regenesis names candidates, and Harmonizer wires gene-symbol dialects. Nothing calls the L5 readers or
  the scoped banks yet — they are apex leaves awaiting this glue.

### L4b STRUCTURAL POLE — ✅ `structural.py`, `structural_fetch.py`
- **OWNS:** the biophysics eliminator feeding fungibility. Deterministic sequence → a FUNDAMENTAL-
  blocker read; no fold predicted, no measured structure imported ("structure without structure").
- **`structural_class`** (confidence-gated: multi-pass membrane / soluble / uncertain — abstains on the
  ambiguous middle) + **`structural_compatibility`** — membrane-integral vs soluble = a physical
  can't-coexist → bar the merge; everything moderate → abstain; **never promotes.** (The full rationale
  and the Socratic reframe — filter *cleans*, story engine *decides*; global similarity is not
  pathway-fungibility — is `docs/PROTEIN_ROLE_GEOMETRY.md` §★DESIGN UPDATE.)
- **`structural_fetch.py`** — Ensembl CDS: per-gene REST `ensure` + bulk `ensure_bulk`/`load_proteins_bulk`.
- **Built-but-UNUSED primitive:** the multi-feature global signature (`composition`/`gravy`/`net_charge`/
  `aromaticity` + `feature_agreement`/`signature_verdict`/`signature_compatibility`). The global-composite-
  for-fungibility frame was REJECTED (a filter that promotes is deciding); kept for a future *extreme
  fold-class blocker* (elimination-only). Wired to nothing.
- **Gate PASSED:** every pure decision pinned; fired on the real LRRK2 axis (0 promotions, 0 regressions).

---

## 3. The two typed contracts — everything flows through these

```
Event {                                   # L1 — what every bank emits, what every compiler eats
  network:  str    # provenance/genus (which bank witnessed it) -- also the directed/undirected tier
  verb:     str    # role-action class (amplifies/inhibits/binds/channels/resembles/isolates…) — data
  subject:  str    # coupled atomic id (gene / role)
  target:   str    # coupled atomic id (gene / role)
  sign:     int    # +1 assert coupling · -1 CENSOR · 0 abstain (the informational zero)
  mode:     str    # optional peer channel marker (activity/abundance/tissue…) — the GSE density op
}

ClinicalResult {                          # L4 — what the read returns; the only judgment object
  verdict:   BOTTOM | RESOLVED | DEGENERATE | ASK | ABSTAIN
  mechanism: the surviving source (only when RESOLVED)
  probe:     the next discriminating dimension (only when ASK; from Jeeves)
  trajectory: the σ-elimination Trajectory (steps, survivors, bottom, falsifiable)
}
```
Every read is `events + positions + active_roles → ClinicalResult`. No consumer reaches around the
`Event` stream or the `ClinicalResult`. Abstention (ABSTAIN / sign-0) is a real answer, never a default.

---

## 4. The read (the spine, end to end)

```
symptom text ──ground.ground──▶ concept + active_roles       # front door; abstains, never guesses
person state ──────────────────▶ positions {node: Position}  # ⬜ producer; signed-ternary off mined zero

banks ──▶ [Event]  ──events_to_web──────────────────────────▶ web        # convergent, uncontradicted
                   ──active_censors(events_to_censors, active_roles)──▶ censors   # role-scoped negative

clinic.read_from_events:
  observed              = observed_symptoms(positions)            # sign ≠ 0
  candidates, constraints = kill_matrix(web, observed)            # explains:S kills non-reaching sources
  trajectory            = eliminate_two_sign(candidates, constraints, censors)
  verdict               = clinical_verdict(bottom, resolved, falsifiable, has_probe)
  → ClinicalResult(verdict, mechanism, probe, trajectory)
```
The glue holds no branch that inspects a gene, a weight, or a threshold (Law 11). The judgment is the
elimination + (⬜) the Regenesis read; the loop only routes.

---

## 5. The laws (the discipline, mechanized — `docs/SYSTEM_DESIGN.md` §13)

1. **Data-geometry + classical AI, NOT statistics** — a frequency/p-value is at most a search-order
   prior. *Enforced:* significance is `kappa`; no renderer emits an association as a verdict object.
2. **One engine, clinical, n=1, zero-time, over a PRIOR web** — no node-birth (Engine A retired, ⛔).
3. **Two-sign, always** — σ(P, μ ∪ μ⁻); "no disease" is a certified ⊥ with a proof. *Enforced:*
   `eliminate_two_sign` checks ⊥ first.
4. **Completeness is κ-coverage of the shadow, never a criteria count** — the count is blind to γ (the
   bridges). *Enforced:* `kappa`.
5. **Never guess a direction** — direction is a negative-sign censor-shadow, earned. *Enforced:*
   `events_to_web` draws +1 direction only where a *directed* network asserts.
6. **Per-individual mined zero; discriminate by a NEW DIMENSION, never a model/threshold** — *Enforced:*
   `position.discriminates`, `jeeves.select_probe`.
7. **σ_sem > 0** — keep plurality, never collapse to a self-confirming mechanism; the dual: never
   over-censor to a false ⊥; halt at the κ-knee. *Enforced:* the DEGENERATE verdict, the falsifiable guard.
8. **Roles by semantic class on physically-real centroids, never token identity** — *Enforced:* Regenesis
   over `universes/mechanism/` (verb-class centroids); fungibility earned by convergence; the structural
   eliminator on real biophysics.
9. **The bright line is THREE-TIER** — directed proven / undirected vote / calibration node-weight (§2 L2).
10. **Abstention is load-bearing** — category incompleteness → informational zero → non-recovery, never a
    wrong placement. *Enforced:* `ground` (front door), the ABSTAIN verdict, sign-0 events.
11. **Reads a FROZEN world; touches NO creativity** — imposes no prior it did not extract, fits no
    dynamics it cannot observe. This refusal IS the guarantee; κ is an endogenous oracle. *Enforced:* the
    glue holds no decision; every judgment traces to the web, the censors, or the Regenesis read.

---

## 6. Build order (each step gated; no step before its gate is green)

1. ✅ **The engine + the event contract + the 6 banks + the genre/interpretive/structural layers** —
   done. Gate: every pure decision Detective-complete; each bank fired on its real dump; 207 tests green.
2. ⬜ **The positions producer** — a real person's genotype/state → `dict[node, Position]` (the
   `signal`-tier feed). Gate: `read_from_events` runs on a real n=1 with provenance, not synthetic
   positions.
3. ⬜ **The driver** (generate-wide → resolve-narrow) — the scoped banks + fungibility + genres +
   Regenesis roles enter; Harmonizer wires symbols. Gate: a scoped read on a real gene set traces every
   verdict element to a bank/role/censor with provenance and honest abstention.
4. ⬜ **The blind LRRK2 control** (canon §13.3) — recover LRRK2–NOD2–RIPK2 as coherence, blind. Gate:
   the acceptance test passes with ≥2 networks + Regenesis (the regulatory slice alone is not it).
5. ⬜ **The remaining banks** — developmental (the first CENSOR bank — the native negative sign),
   exposome, phenotype pole.

---

## 7. Status ledger

| Component | State | Evidence |
|---|---|---|
| L0 substrate (otp/web/kappa/paths/util) | ✅ | pinned; `test_otp/web/kappa` |
| `signal.py` (genotype tier) | 🔧 | built + tested, wired to nothing — pending producer or archive |
| L1 event contract | ✅ | `couple_verdict`/`events_to_web`/`events_to_censors`/`active_censors` pinned |
| L2 banks — 4 global edge | ✅ | pinned; each fired on its real dump (SIGNOR/STRING/Compara/Reactome) |
| L2 banks — 2 scoped (coexpr/trait) | ✅ built ⬜ wired | fired scoped; enter at the driver |
| L3 position | ✅ | `discriminates`/`mine_zero` pinned · producer ⬜ |
| L4 engine (eliminate/clinic/jeeves) | ✅ | certified-⊥, DEGENERATE/ASK/ABSTAIN pinned; `test_two_sign` |
| L5 genres (tragedy/comedy/topology) | ✅ | pinned; fired on the real regulatory web (372 cycles) |
| L5 fungibility + structural eliminator | ✅ | pinned; LRRK2 axis 0-promotions/0-regressions |
| L4b structural pole | ✅ | eliminator wired; Ensembl CDS fetch (per-gene + bulk) |
| structural multi-feature signature | 🔧 | built, UNUSED (rejected decider frame; kept per founder) |
| front door `ground` | ✅ | SymbolicSpellCheck ground-or-abstain; `test_ground` |
| Regenesis generate-wide in-loop | ⬜ | roles fire offline; in-loop wiring absent |
| **The driver** | ⬜ | the generate-wide→resolve-narrow orchestrator — does not exist yet |
| Blind LRRK2 control | ⬜ | the acceptance test |

---

## 8. Reachability method

The live set above was traced deterministically: `scratchpad/trace_wiring.py` (AST import graph — module
→ internal deps, reverse importers, `__main__` entry points) + the language server (`find_symbol` /
`find_referencing_symbols` for the call graph). Entry points: `prior_web.__main__` (assemble the web),
`clinic.read_from_events` (the apex read), `ground.ground` (the front door). 28 `tests/test_*.py` cover
every live module; every pure decision is Detective-pinned under `tests/detective/`.

## 9. NOT in this map — archive / toss candidates (⛔; founder to confirm before any cut)

By the definition at the top, these are unreachable from the live design. **Not deleted unilaterally** —
they are your records; confirm archive-vs-delete per group (proposed: `git mv` to `docs/archive/`).

- **`docs/runs/*` (~30 files, 2026-08-28…30)** — experiment logs of the RIPPED statistical genus (EIR
  cohort, PBS pile, gnomAD/panUKBB replication, phase-2 proposer/verifier, sig-descent, LD block/thin,
  annotation-recovery). The engine they document was trashed (`19cf5d1`, `2fa895c`).
- **Pre-refounding docs (each to confirm, dates straddle the 09-01 re-founding):** `CONCEPTUAL_AUDIT`,
  `PHASE2_SIGNIFICANCE_SEARCH`, `PROOF_POINTS`, `PROBE_STATE`, `SALVAGE_MANIFEST`, `DENSITY_PROTOCOL`,
  `DATA_ACCESS_LANDSCAPE`, `REGULATORY_DEFICIT_PROGRAM`, `decisions/*`. **Current canon:** `THESIS`,
  `SYSTEM_DESIGN`, `ETIOLOGY_ENGINE`, `STORY_LAYER`, `THEORY_OF_THE_CASE`, `PROTEIN_ROLE_GEOMETRY`, this file.
- **`signal.py`** — archive only if the genotype-tier input is not the intended positions producer (L3).
- **The unused multi-feature signature in `structural.py`** — kept per founder (future extreme blocker);
  listed for completeness, NOT a toss candidate.
```

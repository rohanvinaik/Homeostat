# Homeostat — Architecture (as-built wiring map)

**Status:** Canonical engineering map, traced from source at `2118c48` (2026-09-05). Companion to
`docs/THESIS.md` and `docs/SYSTEM_DESIGN.md` (the *why*; this is the *what and how*). Every claim below
was traced with the language server — `get_symbols_overview` for the inventory, `find_referencing_symbols`
for the call graph — not from memory. **It is the definition of the live system: anything not reachable
from an apex read here is, by construction, parked or archived residue (see §9–§10).**

**Legend:** ✅ built and pinned (Detective-complete + intent-tested) · 🔧 built, refinement flagged ·
🅿️ built + pinned but PARKED (reachable only from tests — no live consumer yet) · ⬜ designed, not built ·
⛔ superseded/removed.

Homeostat is a per-person, **zero-time, two-sign elimination read** over a multi-network coupling web,
whose surviving structure is then **read as a story**. A disease is a *shadow* — a sub-threshold
combination of deviations that no single criterion names. The engine reads *one person's* deviations
against a prior web of couplings and **eliminates** candidate mechanisms to a survivor, a certified ⊥ (a
proof of "no such mechanism"), an honest abstention, or the next discriminating question — then reads the
surviving structure through the four **dynamics genres** and Regenesis's narrative universe, closes that
wide story NARROW into ranked candidate MECHANISMS, and reports its own **σ_sem completeness** ("how much
of the mechanism-uncertainty did structure resolve?"). It reads a FROZEN world and adds nothing of its own
(Law 11); its significance is κ (coverage of the shadow), never a statistic (Law 1). The answer is a
**story resolved to ranked mechanisms, never a ranked gene** (the subject-fallacy, cut `5c30e65`).

**Scale (counts primary-sourced, not remembered):** 45 modules · 42 `tests/test_*.py` · **429 tests**, of
which **80 are Detective-generated** across 47 `tests/detective/*` synth files. Clean tree, `main`,
unpushed.

---

## 1. System overview

```
   FRONT DOOR   ✅ ground — symptom text → concept | abstain (SymbolicSpellCheck, no guess)
   ──────────────────────────────────────────────────────────────────────────────────────
   APEX         ✅ driver.drive — the COMPOSED read: scope → eliminate → STORY → resolve-narrow → σ_sem
                ✅ clinic.read_from_events — the elimination-only read (pre-story core; still live)
   ──────────────────────────────────────────────────────────────────────────────────────
   L6  COMPLETE ✅ completeness.read_completeness — σ_sem: H₀→H_residual, resolved fraction, I_solve
   L5  RESOLVE  ✅ resolve.rank_clusters — candidate MECHANISMS scored coverage × coherence × meter
                ✅ meter — the NML/KT-calibrated predictive coherence (SSL §9.3) · ⬜ resolve incr.3
   L5  STORY    ✅ narrative.read_story: 4 dynamics genres → tier-2 Regenesis account → tier-3 lament
                ✅ tragedy · comedy · allegory(fungibility+structural) · epic-quest(Kuramoto)
   L4  ENGINE   ✅ eliminate_two_sign → clinical_verdict (BOTTOM/RESOLVED/DEGENERATE/ASK/ABSTAIN)
                ✅ full-C: tier gates cert (certified iff observed all-VERIFIED; else TAG, code kept)
                ✅ polarity censor (mechanistic contradiction = negative sign) · jeeves probe
   L3  POSITION ✅ per-person signed-ternary off the mined zero + discrimination guarantee
                ✅ marker PRODUCER + structured Differential · ⬜ genotype/state producer
   L2  BANKS    ✅ 4 global edge (signor/string/homology/metabolic) · 🅿️ 2 scoped (coexpr/trait)
   L1  EVENT    ✅ the one typed contract: Event → events_to_web + events_to_censors/active_censors
   L0  SUBSTRATE✅ otp (ternary) · web (RelationalWeb/kill_matrix/cone) · kappa · signal(tier) · paths/util
   ──────────────────────────────────────────────────────────────────────────────────────
   THE COMPOSED READ (driver.drive): relevance-scope (directed ancestor cone) → two-sign elimination
   (polarity + role censors) → STORY-read → resolve-narrow ranking of MECHANISMS → σ_sem completeness.
   Zero judgment in the glue.
```

The engine's judgment lives in exactly two places: the elimination read over the web, and the
story-understanding derivation over the surviving structure (the genres + Regenesis's narrative universe).
The resolve-narrow ranking and the σ_sem completeness are mechanical reads *over* those two (κ-coverage,
the calibrated meter, Hartley entropy — no new judgment). Everything at L0–L4 is mechanical and pinned;
L5/L6 consume it through the typed `Event` / `StoryRead` / `DriverRead` contracts (§3).

---

## 2. Layer contracts

### L0 SUBSTRATE — ✅ (`otp.py`, `web.py`, `kappa.py`, `paths.py`, `util.py`, `signal.py`)
- **OWNS:** the signed-ternary algebra, the positive graph type, reachability/κ/cone machinery, IO paths.
- **`otp.py`** — `SUPPORT`/`OPPOSE`/`ORTHOGONAL` (the ternary alphabet) + `ternary(value, zero)` → the
  signed value off a mined zero. The elimination primitive: a single opposing sign vetoes a pile of weak
  supports (the "Monty-Hall move"). ORTHOGONAL is the informational zero — a first-class value.
- **`web.py`** — `Coupling(a,b,weight,direction)`, `RelationalWeb`, `kill_matrix(web, observed)`
  (candidates = the whole bounded node set; `explains:S` kills every source that CANNOT reach `S`);
  `nodes`/`web_adjacency`/`reaches`/`reverse_adjacency`/`reachers`; **`ancestor_cone`/`induced_subweb`**
  (the directed-reachability relevance scope the driver uses); `distances_to` (reverse-BFS);
  `node_convergence` (🅿️ mean coupling weight — the old tie-breaker, parked).
- **`kappa.py`** — `reachable`/`coverage`/`marginal_coverage`/`weak_components`/`is_bridge`/
  `components_joined`/`chain_significance` (κ = marginal coverage; the significance object, Law 4).
- **`signal.py`** ✅ — `Signal(ident, state, tier)` + `Tier` (VERIFIED/REPORTED/ABSENT). **WIRED (full-C):**
  `Tier` gates certification in `clinic` and rides on every `Position`. A VERIFIED value-kill can certify;
  a REPORTED run-kill constrains but banks nothing toward a certified verdict (NEGATIVE_SPECIFICATION 1.4).
- **`paths.py`** — every data-file location + SHA + URL (SIGNOR/STRING/Compara/Reactome/GTEx/GWAS/Ensembl-
  CDS/HMDB/genotype), the single source of truth for the IO shells. **`util.py`** — `sha256`,
  `atomic_write_text/json`. IO-only; interpret nothing.

### L1 EVENT — ✅ `event.py` (the one typed contract)
- **OWNS:** the record every bank emits and every read consumes; the compilers to web + censors.
- **`Event(network, verb, subject, target, sign, mode)`** — `sign` = +1 assert / −1 censor / 0 abstain
  (coupling support, NOT regulatory polarity — activation/inhibition rides `verb`); `mode` = a peer
  κ-density channel marker.
- **`events_to_web`** → group by coupling, `couple_verdict(support, censor)` (coupling / **killed**
  (cross-network contradiction) / censor / abstain), draw only convergent-uncontradicted edges;
  direction = +1 iff a *directed* network asserts it (Law 5, 9-i).
- **`events_to_censors` → `active_censors(active_roles)`** — the role-scoped negative sign: a `sign<0`
  event rules its subject out FOR role `target`, fired only where that role is active.
- **Gate PASSED:** `couple_verdict`/`events_to_web`/`events_to_censors`/`active_censors` pinned (`test_event`).

### L2 BANKS — ✅ 4 global edge · 🅿️ 2 scoped. The three-tier bright line (Law 9)
Each bank = a pure renderer (`X.py`) + an IO shell (`X_fetch.py`; data gitignored + SHA-pinned via `paths`).

| Bank | Tier (Law 9) | Renderer | Fetch shell | Renders |
|---|---|---|---|---|
| regulatory | (i) directed proven mechanism — EARNS direction | `signor.py` | `signor_fetch.py` | SIGNOR effect grammar → `amplifies`/`inhibits`, all `sign=+1` |
| physical | (ii) undirected mechanistic vote | `string.py` | `string_fetch.py` | STRING binding → undirected coupling votes |
| evolutionary | (ii) undirected / the fungibility seed | `homology.py` | `homology_fetch.py` | Compara paralogs → `resembles` seeds |
| metabolic | (ii) undirected | `metabolic.py` | `metabolic_fetch.py` | Reactome metabolic co-membership → `channels` |
| co-expression | (ii) — COMPUTES (dynamics not statistics) | `coexpression.py` 🅿️ | `gtex_fetch.py` | GTEx OTP co-deviation; enters at the driver |
| trait-wiring | (iii) calibration prior — a NODE-WEIGHT, not an edge | `trait_wiring.py` 🅿️ | `trait_wiring_fetch.py` | GWAS pleiotropy count per gene |

- **`prior_web.py`** — `all_events` assembles the 4 global edge banks → `build_prior_web` → `RelationalWeb`;
  `_main` is the assemble-the-web entry point. The 2 scoped banks are NOT here (they enter per-gene-set at
  the driver — `coexpression.read_coexpression` and `trait_wiring` have **zero live consumers**, 🅿️).
- **Forbidden across all three (Law 9):** a computed association AS the object of a verdict. Significance is κ.
- **Gate PASSED:** every renderer's pure decision pinned; each global bank fired on its real dump.

### L3 POSITION — ✅ `position.py`, `differential.py`, `producer.py` (+ `reference_fetch.py`) · genotype producer ⬜
- **OWNS:** the per-person placement — each measured property → signed-ternary off a **mined** zero (a norm
  from the data, never a fixed threshold), the discrimination guarantee, and the typed
  information-weighted departure that rides alongside the sign.
- **`Position`** (carries `tier` + `differential`), `mine_zero`, `deviation`, `signature`, `hamming`,
  `discriminates` (two operationally-different states MUST have different signatures — the fix for a
  collapse is a NEW orthogonal dimension, never a tuned threshold, Law 6). **`place`** composes the sign
  (`ternary`) and the differential (`make_differential`) from one reference band.
- **`differential.py`** ✅ — `Differential(kind, surprise, spread)`, `surprise = |value−center|/spread`
  (monotone in −log P); `mine_spread`/`surprise`/`differential_kind`/`make_differential`. The SICP
  coordinate-vs-provenance split: elimination reads only the `sign`; the interpretive layer gets the
  differential. Wired into `Position` via `place`.
- **The MARKER producer** (`producer.signals_to_positions`): `signal → reference_center_spread → parse_marker
  → place`; ungroundable / non-numeric / unreferenced signals honestly dropped. Its reference is a GIVEN
  published demographic interval (the one sanctioned population read — the shadow, never the mechanism),
  served by **`reference_fetch.py`** (HMDB serum, PARSE-LOCAL). **Built & pinned but PARKED** (🅿️ — zero
  production consumers; `clinic`/`driver` still take a positions object; it enters at the driver).
- **⬜ The genotype/state producer:** genotype → `dict[node, Position]` via the consequence-vector prior
  (the genotype pole below) — designed, not built.
- **Gate PASSED:** `discriminates`/`position`/`mine_zero`/`place`/`make_differential`/`signals_to_positions`
  pinned (`test_position`, `test_differential`, `test_producer`, `test_reference_fetch`).

### L4 ENGINE (two-sign elimination) — ✅ `search.py`, `clinic.py`, `jeeves.py`, `polarity.py`
- **OWNS:** the σ-elimination, the clinical verdict, the polarity (mechanistic-contradiction) censor.
- **`search.eliminate_two_sign(candidates, constraints, censors)`** — positive elimination (μ) ∧ negative
  censors (μ⁻) driving H→0. Ends on: a unique survivor (the mechanism), a **certified ⊥** (a censor rules
  out the sole survivor = a proof of non-membership, checked FIRST), or a STUCK plurality. Never empties on
  a positive constraint (the survivor IS the reading). Companions: `survivors`/`entropy_bits`/`resolved`/
  `survivors_killed`/`constraint_disposition`/`falsifiable`/`knee_index`/`covers_shadow`/`coverage`/
  `max_coverage_survivors`; `Step`/`Trajectory` (the σ-trajectory record).
- **`polarity.py`** — the mechanistic-contradiction censor. **`signed_adjacency(events, verb_sign)`** →
  `SignedAdj = {subject: [(target, ±1)]}` (adjacency-LIST; sign-ambiguous edges dropped); `net_polarities`;
  **`polarity_censors`** — a candidate whose net regulatory polarity to an observed node CONTRADICTS the
  observed sign is ruled out (a strong censor, applied conservatively). *NB: this is a DIFFERENT function
  from `topology.signed_adjacency` — see §5's note on the two signed-adjacency shapes.*
- **`clinic.read_from_events` → `read_presentation`** — the **elimination-only apex** (pre-story core; still
  live): `observed_symptoms(positions)` → `kill_matrix(web)` → `eliminate_two_sign` → `select_probe` if
  stuck → **`clinical_verdict`**: **BOTTOM** (certified ⊥) / **RESOLVED** (unique survivor) / **DEGENERATE**
  (self-confirming, σ_sem=0, Law 7) / **ASK** (Jeeves probe) / **ABSTAIN** (no dimension separates the
  survivors, Law 10) → `ClinicalResult`. Verdict-code constants `RESOLVED`/`DEGENERATE`/`BOTTOM`/`ASK`/
  `ABSTAIN` live here.
- **Full-C certification** (`clinic.weakest_tier`/`is_certified`) — a verdict is `certified` only when it is
  a value-kill (BOTTOM/RESOLVED) AND every observed position is `Tier.VERIFIED`; a REPORTED-grade input
  keeps the verdict CODE (TAG, never collapse) with `certified=False` and `certification_tier` naming the
  weakest link.
- **`jeeves.py`** — `Probe`, `expected_information_gain`, `probe_gain`, `select_probe` (the STUCK-branch:
  which new dimension best discriminates the surviving plurality — the Jeeves DO-THIS).
- **Gate PASSED:** `eliminate_two_sign`/`clinical_verdict`/`select_probe`/`kill_matrix`/`polarity_censors`
  pinned (`test_search`, `test_clinic`, `test_jeeves`, `test_two_sign`, `test_certification`, `test_polarity`).

### L4b STRUCTURAL POLE — ✅ `structural.py`, `structural_fetch.py`
- **OWNS:** the biophysics eliminator feeding fungibility. Deterministic sequence → a FUNDAMENTAL-blocker
  read; no fold predicted, no measured structure imported ("structure without structure").
- **`structural_class`** (confidence-gated: membrane / soluble / uncertain — abstains on the ambiguous
  middle; `translate`/`tm_segments`/`_window_means` + `TM_*`/`KYTE_DOOLITTLE`/`CODON_TABLE`) +
  **`structural_compatibility`** — membrane-integral vs soluble = a physical can't-coexist → bar the merge;
  moderate → abstain; **never promotes** (Law 8).
- **`structural_fetch.py`** — Ensembl CDS (per-gene REST + bulk).
- **🔧 Built-but-UNUSED primitive:** the multi-feature global signature (`composition`/`gravy`/`net_charge`/
  `aromaticity` + `feature_agreement`/`signature_verdict`/`signature_compatibility`). The global-composite-
  for-fungibility frame was REJECTED (a filter that promotes is deciding); kept for a future *extreme
  fold-class blocker* (elimination-only). Wired to nothing.
- **Gate PASSED:** every pure decision pinned; fired on the real LRRK2 axis (0 promotions, 0 regressions).

### GENOTYPE POLE (the prior) — ✅ `consequence.py`, `biophysics.py` · producer/projection ⬜
- **OWNS:** a variant's deterministic CONSEQUENCE as a dense vector — the genotype as a PRIOR on the
  mechanism (a source-prior/node-weight, the person-structural twin of `trait_wiring`), NEVER an
  observation; it never resolves alone (`docs/GENOTYPE_POLE.md`).
- **`consequence.consequence_vector`** (design A, dense): structural-consequence deltas (reusing
  `structural.py`: `class_shift` + composition/gravy/charge/aromaticity) ⊕ DNA structural mechanics
  (`biophysics.py`: `bendability` [Bolshoy] + `yr_ry_balance` [Drew-Travers/Trifonov], ported from
  GenomeVault) ⊕ rarity. **`consequence_similarity`** = fungibility-by-cosine, interpretive-layer only,
  never in the elimination gate.
- **Built & pinned but PARKED** (🅿️ — zero consumers): the genotype PRODUCER, the PROJECTION to a
  source-prior, and the Law-7-safe ENTRY (shared with `trait_wiring`) land at the driver.
- **Gate PASSED:** `consequence_vector`/`consequence_similarity`/`bendability`/`yr_ry_balance` pinned
  (`test_consequence`, `test_biophysics`).

---

## 3. The typed contracts — everything flows through these

```
Event {                                   # L1 — what every bank emits, what every compiler eats
  network:  str    # provenance/genus (which bank witnessed it) — also the directed/undirected tier
  verb:     str    # role-action class (amplifies/inhibits/binds/channels/resembles/isolates…) — data
  subject:  str    # coupled atomic id (gene / role)
  target:   str    # coupled atomic id (gene / role)
  sign:     int    # +1 assert coupling · -1 CENSOR · 0 abstain (the informational zero)
  mode:     str    # optional peer channel marker — the GSE density op
}

ClinicalResult {                          # L4 — what the elimination-only read returns
  verdict:   BOTTOM | RESOLVED | DEGENERATE | ASK | ABSTAIN
  mechanism: the surviving source (only when RESOLVED)
  probe:     the next discriminating dimension (only when ASK; from Jeeves)
  trajectory: the σ-elimination Trajectory (steps, survivors, bottom, falsifiable)
  certified: bool  # full-C: a value-kill AND every observed position VERIFIED
  certification_tier: the weakest observed tier — names the trust boundary (TAG, not collapse)
}

StoryRead {                               # L5 — the presentation-level read (the answer is a STORY)
  genres:    dict[str, list]   # tier-1 dynamics instances: comedy/tragedy/allegory/quest
  account:   dict | None       # tier-2 Regenesis derivation-over-derivations, or None (graceful)
  treatment: list[Lament]      # tier-3 therapeutic read (POC)
}

DriverRead {                              # the composed-read output (driver.drive)
  verdict:      the clinic code (RESOLVED/BOTTOM/DEGENERATE/ASK/ABSTAIN)
  story:        StoryRead       # the genre account over the surviving structure (not a ranked gene)
  ranked:       list[(Cluster, float)]  # resolve-narrow: candidate MECHANISMS scored, descending
  completeness: SpecCompleteness  # σ_sem: h0, h_residual, resolved fraction, i_solve (§L6)
  probe:        the Jeeves DO-THIS (on ASK)
  trajectory:   the two-sign σ-trajectory
  censored:     dict[str, list[str]]  # what each censor ruled out
  dropped:      list[str]       # observed deviations with no directed context
}

SpecCompleteness {                        # L6 — the σ_sem "how solved is this mechanism?" read
  h0:         float   # log₂(candidate mechanisms) — initial mechanism-uncertainty, bits
  h_residual: float   # log₂(surviving mechanisms) — the plurality = I_solve, still to measure
  resolved:   float   # (h0 - h_residual)/h0 — SSL's L, fraction structure resolved for free
  i_solve:    Probe | None  # the Jeeves measurement owed when a plurality survives
}
```
No consumer reaches around the `Event` stream. Abstention (ABSTAIN / sign-0 / ORTHOGONAL) is a real answer,
never a default.

---

## 4. The two apex reads

There are **two entry points**, both currently reachable only from tests (no CLI/`__init__` export yet —
`__init__.py` exposes only `__version__`):

**(a) `clinic.read_from_events` — the elimination-only read (the pre-story core).**
```
events + positions + active_roles + probes + directed_networks
  → events_to_web → kill_matrix → eliminate_two_sign(+ active_censors) → clinical_verdict
  → ClinicalResult
```
Positions-object-led, no directed-cone scoping, no polarity censor, no story. Used by `test_clinic`,
`test_certification`, `test_producer`. This is the "a human stands in for the driver" path.

**(b) `driver.drive` — the composed read (the apex, the Dr. House protocol).**
```
drive(events, positions, verb_sign, active_roles=(), probes=(), proteins=None, min_weight=0.0):
  web       = events_to_web(events, DIRECTED_NETWORKS)
  directed  = the direction≠0 sub-web
  observed  = observed_symptoms(positions)
  scoped    = induced_subweb(directed, ancestor_cone(directed, observed))   # RELEVANCE (directed cone)
  observed_scoped, dropped = split observed by in-cone
  candidates, constraints  = kill_matrix(scoped, observed_scoped)
  signed    = polarity.signed_adjacency(events, verb_sign)
  censors   = {polarity: polarity_censors(signed, candidates, obs_signs)} ∪ active_censors(...)
  traj      = eliminate_two_sign(candidates, constraints, censors)          # REQUIRE (two-sign)
  probe     = select_probe(...) if stuck
  verdict   = clinical_verdict(bottom, resolved, falsifiable, has_probe)
  story     = read_story(scoped_events, observed_scoped, proteins)          # PREFER (the story)
  → DriverRead(verdict, story, probe, traj, censors, dropped)
```
The glue holds no branch that inspects a gene, a weight, or a threshold (Law 11). REQUIRE is the two-sign
elimination (unchanged); PREFER is the story-read, which **replaced the old gene ranking** (cut `5c30e65`).

---

## 5. The story-read layer (L5, `narrative.py` + the genre readers) — ✅ wired into `drive`

`narrative.read_story(events, observed, proteins) → StoryRead` fires the four native genre readers over the
caller-scoped events, composes their opinionated instances into the tier-2 account, and reads the tier-3
treatment. Three tiers, plural, **no single subject**:

**Tier-1 — the four dynamics genres** (the shape of the motion; each a few hand-pinned definitions,
Winston's method). All consumed by `read_story`:
- **`tragedy.py`** — `read_tragedy` → `Tragedy(origin, sink, verdict)`: a cascade from a fatal flaw
  locking an absorbing SINK; verdict by OTP net-sign along the path (`doomed` / `suppressed` /
  `indeterminate`). Helpers: `reach_graph`/`sources`/`is_sink`/`net_signs`/`doom_verdict`.
- **`comedy.py`** — `read_comedy` → `Comedy(a, b, verdict)`: a mutual-regulation cycle; verdict by
  loop-gain sign (`vicious` / `homeostatic` / `indeterminate`). Helper: `loop_verdict`.
- **`fungibility.py`** (the **allegory** genre) — `read_fungibility` → `Fungible(a, b, verdict, banks)`:
  paralog role-equivalence EARNED by ≥2-bank convergence on shared partners, GATED by the structural
  eliminator (`fungible` / `coincidental` / `seed-only`). Structure bars a merge but NEVER promotes (Law 8).
- **`quest.py`** (the **epic quest** genre, built this session) — `read_quest` → `Quest(hero, joined,
  coherence, verdict)`: the roundabout cure — a distant hero-bridge resolving the observed parts, scored by
  a **true Kuramoto order parameter** `r = |mean phasor| ∈ [0,1]` over OTP phasors (`part_vector` embeds the
  balanced-ternary phase circle: SUPPORT→in-phase, OPPOSE→antiphase, ORTHOGONAL→the ZERO VECTOR;
  `order_parameter`; `quest_verdict` → `resolving` / `entangling` / `indeterminate`, the `opinionated`
  count distinguishing destructive cancellation from abstention).
- **`topology.py`** — the shared genre substrate: `otp_combine` (merge → informational-zero on disagreement)
  and **`signed_adjacency(events) → {subject: {target: ±1/0}}`** (nested-dict, OTP-combined). Consumed by
  comedy, tragedy, quest.

**Tier-2 — the dramatic account** (`_compose(genre_triples(genres))`): each opinionated genre verdict maps
(hand-authored linkage, the `_TRAGEDY_VERB`/`_COMEDY_VERB`/`_ALLEGORY_VERB`/`_QUEST_VERB` tables) to its
Polti dramatic verb (tragedy→`harm`, vicious comedy→`betray`, resolving quest→`seize`, entangling→`pursue`;
homeostatic + allegory emit none). `triples_to_contracts` renders these to contract-JSONL, fired through
**Regenesis's narrative universe via the pure `kind='contracts'` path** — *the same engine that reads
Shakespeare* — so a multi-system mechanism comes back as pursuit + revenge + obtaining. Lazy import →
`account=None` when Regenesis is absent (**graceful degradation** to the native genres — the greenfield
default). No GSE/JVM subprocess.

**Tier-3 — the treatment (`lament.py`, POC):** `read_lament(genres)` → `Lament(mourned, substitute,
verdict)`: a doomed tragedy with no resolving quest → grieve the lost function and either route around it
with a fungible stand-in (`substituted`) or palliate a structured decline (`palliative`). `lament_verdict`
pinned.

> **The two `signed_adjacency` (a real structural fact, not a bug):** `topology.signed_adjacency(events)`
> returns the **nested dict** `{subject: {target: ±1/0}}` (OTP-combined ternary; ambiguous edges dilute as
> informational zeros) for the genre readers and `cluster_coherence`. `polarity.signed_adjacency(events,
> verb_sign)` returns the **adjacency list** `{subject: [(target, ±1)]}` (sign-definite only) for the
> polarity censor and the predictive `meter`. Different purpose, different shape — kept distinct on purpose
> (collapsing them destroys the ambiguous-edge dilution). `drive` computes BOTH and feeds each factor its
> correct producer (seam resolved `801448b`).

### L5 RESOLVE — the resolve-narrow recommendation engine (`resolve.py` + `meter.py` + `recommend.py`) — ✅ LIVE
Where `read_story` generates the story WIDE, the resolve engine closes it NARROW: it ranks candidate
MECHANISMS (connected story-clusters — NOT genes) by THREE orthogonal signals, driving H = log₂(clusters)
→ 0. **Wired into `drive` (`8a17a21`) — the engine RUNS; `DriverRead.ranked` carries the result.**
- **Enumeration** — `connected_components` (merge genre instances sharing entities into candidate
  mechanisms; Detective 5/6, 1 proven-equivalent), `story_clusters`/`Cluster`/`_tagged`. `cluster_coverage`
  (fraction of the shadow spanned; Detective 9/9).
- **Internal coherence** — `cluster_coherence` (Kuramoto order parameter over the cluster's OTP-ternary
  sub-web edge-signs: reinforcing cascade phase-locks → high r; balancing/contradictory destructively
  interferes → low r). **Detective-COMPLETE** (the incr.2 tracked debt, now closed `801448b`).
- **The predictive METER** (`meter.py`, SSL §9.3) — the calibrated, small-sample-honest coherence. A
  candidate's predictions against the shadow are a rate process over m=3 outcomes (confirmed / contradicted
  / standing = the OTP ternary read as an ELIMINATION track record, not a vote-tally). `coherence_meter(c,
  x, s) = (c−x)/(n+m/2)` — the Krichevsky–Trofimov (add-½) minimax-regret predictor's net confirmation
  (regret `(m-1)/2·log₂n = log₂n`); the calibrated form of the raw order parameter (COMPLETE 18/18).
  `source_outcomes` derives (c, x, s) via the SAME `net_polarities` as the polarity censor — "contradicted"
  here IS the censor's contradiction (value-complete). `cluster_meter` = the best member-source's meter
  (≥ 0 by persuasion-before-execution; the negative pole is the censor's domain). `nml_regret` reports the
  calibration cost in bits (auditability).
- **The blend** — `rank_clusters` = `score_candidate([coverage, cluster_coherence, max(0, cluster_meter)],
  [])` (`recommend.py`'s ModelAtlas blend, `∏(alignment) × submodular_combine(soft)`). The `max(0,·)` is a
  directional-gate guard at the ranking boundary. `recommend.score_candidate` is now LIVE (via
  `rank_clusters`); the parked `driver.rank_candidates` also consumes it.
- **⬜ incr.3 (designed, not built):** the operator-injected hypothesis (fluid intelligence as a tested
  input, never ground truth), the mechanism-level Jeeves DO-THIS on a surviving plurality, GWAS
  relevance-seeding.

### L6 COMPLETENESS — `completeness.py` — ✅ LIVE
The σ_sem read (SSL §2.5): "how solved is this person's mechanism?" as a NUMBER, over the ranked mechanisms.
`resolution_entropy(count) = log₂(count)` (the Hartley conceptual entropy; COMPLETE, 2 proven-equivalent);
`spec_completeness(initial, survivors)` → `(h0, h_residual, resolved)` where survivors = the mechanisms
structure did NOT rule out (score > 0), `h0 = log₂(initial)`, `h_residual = log₂(survivors)` = I_solve,
`resolved = (h0−h_residual)/h0` = SSL's L (COMPLETE 16/16). `read_completeness(ranked, probe)` carries the
Jeeves `probe` as `i_solve` only when a plurality survives. Wired into `drive` (`2118c48`);
`DriverRead.completeness`. *(The `i_solve` probe is currently the elimination-level Jeeves; the
mechanism-level one is resolve incr.3.)* A neural net structurally cannot emit this read.

---

## 6. The laws (the discipline, mechanized — `docs/SYSTEM_DESIGN.md` §13)

1. **Data-geometry + classical AI, NOT statistics** — a frequency/p-value is at most a search-order prior.
   *Enforced:* significance is `kappa`; no renderer emits an association as a verdict object.
2. **One engine, clinical, n=1, zero-time, over a PRIOR web** — no node-birth (Engine A retired, ⛔).
3. **Two-sign, always** — σ(P, μ ∪ μ⁻); "no disease" is a certified ⊥ with a proof. *Enforced:*
   `eliminate_two_sign` checks ⊥ first; the polarity censor is the mechanistic negative sign.
4. **Completeness is κ-coverage of the shadow, never a criteria count.** *Enforced:* `kappa`.
5. **Never guess a direction** — direction is earned. *Enforced:* `events_to_web` draws +1 direction only
   where a *directed* network asserts; the driver scopes over the directed sub-web only.
6. **Per-individual mined zero; discriminate by a NEW DIMENSION, never a model/threshold.** *Enforced:*
   `position.discriminates`, `jeeves.select_probe`.
7. **σ_sem > 0** — keep plurality, never collapse to a self-confirming mechanism; the story is read over the
   whole surviving plurality, never collapsed to one subject. *Enforced:* DEGENERATE, the falsifiable guard.
8. **Roles by semantic class on physically-real centroids, never token identity.** *Enforced:* Regenesis
   over the narrative universe (Polti class centroids); fungibility earned by convergence; the structural
   eliminator on real biophysics.
9. **The bright line is THREE-TIER** — directed proven / undirected vote / calibration node-weight (§2 L2).
10. **Abstention is load-bearing** — category incompleteness → informational zero → non-recovery. *Enforced:*
    `ground` (front door), the ABSTAIN verdict, sign-0 events, ORTHOGONAL genre verdicts.
11. **Reads a FROZEN world; touches NO creativity** — imposes no prior it did not extract. This refusal IS
    the guarantee; κ is an endogenous oracle. *Enforced:* the glue holds no decision; every judgment traces
    to the web, the censors, or the story-understanding read.

---

## 7. Build order (each step gated; no step before its gate is green)

1. ✅ **The engine + event contract + 6 banks + genre/interpretive/structural layers** — done; every pure
   decision Detective-complete, each global bank fired on its real dump.
2. ✅ **The story-read** (this session) — the 4 dynamics genres, the tier-2 Regenesis account (contracts
   path), the tier-3 lament, composed by `narrative.read_story` and **wired into `driver.drive`** (`4ed3d9b`).
   The old gene-ranking PREFER path was cut (`5c30e65`).
3. ✅ **The driver** (`drive`) — the composed read: directed-cone relevance scope + two-sign elimination
   (polarity + role censors) + story + resolve-narrow + σ_sem completeness. Discriminates (TP53 #1).
   Reachable from tests only (no CLI yet).
4. ✅ **The resolve-narrow engine + the predictive meter + the σ_sem completeness** — `resolve.rank_clusters`
   (coverage × internal-coherence × the SSL §9.3 calibrated `meter`), wired into `drive` (`8a17a21`); the
   `completeness.read_completeness` σ_sem read wired in (`2118c48`). Every pure decision Detective-pinned.
   ⬜ **incr.3 remains:** the operator-injected hypothesis, the mechanism-level Jeeves DO-THIS, GWAS seeding.
5. ⬜ **The input layer** — clean-etiology diagnosis → form-cassette (degenerate) + multimodal diagnosis →
   relevance filter feeding the resolve engine; the marker producer + genotype pole projected into the live
   read; the scoped banks (coexpr/trait) entering per-gene-set.
6. ⬜ **The greenfield-workflow baseline + a rendering of `DriverRead`** — a few realistic workflows → drive
   → story, the functional-validation oracle. No CLI/render exists yet.
7. ⬜ **The blind LRRK2 control** — recover LRRK2–NOD2–RIPK2 as coherence, blind (≥2 networks + Regenesis).

---

## 8. Status ledger

| Component | State | Evidence |
|---|---|---|
| L0 substrate (otp/web/kappa/paths/util) | ✅ | pinned; `test_otp/web/kappa` |
| `signal.py` (verification tier) | ✅ | Tier GATES certification (full-C); `test_certification` |
| L1 event contract | ✅ | `couple_verdict`/`events_to_web`/`events_to_censors`/`active_censors` pinned |
| L2 banks — 4 global edge | ✅ | pinned; each fired on its real dump (SIGNOR/STRING/Compara/Reactome) |
| L2 banks — 2 scoped (coexpr/trait) | 🅿️ | built + pinned; **no live consumer** — enter at the driver |
| L3 position + `differential` | ✅ | `discriminates`/`mine_zero`/`place` pinned; `Position` carries tier + differential |
| marker producer + HMDB reference | 🅿️ | `producer.signals_to_positions` + `reference_fetch` pinned; **not wired** |
| genotype consequence vector | 🅿️ | `consequence.py` + `biophysics.py` pinned; producer/projection at driver |
| L4 engine (search/clinic/jeeves) | ✅ | certified-⊥, DEGENERATE/ASK/ABSTAIN + full-C pinned; `test_two_sign`/`test_certification` |
| L4 polarity censor | ✅ | `polarity_censors`/`signed_adjacency`/`net_polarities` pinned; `test_polarity` |
| L4b structural pole | ✅ | eliminator wired into fungibility; Ensembl CDS fetch |
| structural multi-feature signature | 🔧 | built, UNUSED (rejected decider frame; kept per founder) |
| front door `ground` | ✅ | SymbolicSpellCheck ground-or-abstain; `test_ground` |
| **L5 story-read** (narrative + 4 genres + topology) | ✅ | wired into `drive`; `test_narrative`/`test_comedy`/`test_tragedy`/`test_fungibility`/`test_quest` |
| tier-2 Regenesis account (contracts path) | ✅ | `_compose` fires the narrative universe; graceful `None` when absent |
| tier-3 lament (treatment POC) | ✅ | `lament_verdict` pinned; `test_lament` |
| **`clinic.read_from_events`** (elimination-only read) | ✅ | live via `test_clinic`/`test_certification`/`test_producer` |
| **`driver.drive`** (composed read: story + resolve-narrow + σ_sem) | ✅ | discriminates (TP53 #1); `test_driver`; reachable from tests only |
| **L5 resolve-narrow engine** (enumeration + coverage + coherence) | ✅ **LIVE** | `connected_components`/`cluster_coverage`/`cluster_coherence` Detective-COMPLETE; wired into `drive` |
| **L5 predictive meter** (`meter.py`, SSL §9.3) | ✅ | `coherence_meter` 18/18, `source_outcomes` value-complete, `nml_regret` COMPLETE; `cluster_meter` in `rank_clusters` |
| **L6 σ_sem completeness** (`completeness.py`) | ✅ **LIVE** | `resolution_entropy`/`spec_completeness` Detective-COMPLETE; `read_completeness` wired into `drive` |
| resolve incr.3 / input layer / greenfield baseline / CLI-render | ⬜ | designed, not built |
| Blind LRRK2 control | ⬜ | the acceptance test |

---

## 9. Reachability method & the parked set

Traced with the language server: `get_symbols_overview` for the inventory, `find_referencing_symbols` for
the call graph, from the two apex reads (`clinic.read_from_events`, `driver.drive`) + `prior_web._main`
(assemble the web) + `ground.ground` (front door). 42 `tests/test_*.py` (429 tests) cover every live module;
every pure decision on the live elimination + story + resolve + completeness path is Detective-pinned under
`tests/detective/` (47 synth files, 80 tests) — the incr.2 `cluster_coherence` debt is now closed
(Detective-COMPLETE, `801448b`).

**PARKED (🅿️ — built + pinned, but reachable ONLY from tests; no live consumer):** these are apex leaves
awaiting the wiring in §7.5–§7.6, NOT dead code:
- `driver.rank_candidates`, `driver.proximity_coherence`, `web.node_convergence` — the **old gene-ranking
  PREFER path** (the subject-fallacy). Superseded by the story-read + resolve-narrow; kept as scaffolding.
  **Candidate for removal** now that `resolve` is live (the mechanism ranker replaced the gene ranker).
- `producer.signals_to_positions` + `reference_fetch` (marker producer), `consequence.py`/`biophysics.py`
  (genotype pole), `coexpression.read_coexpression`, `trait_wiring` (scoped banks) — the input paths.
- `structural` multi-feature signature (rejected decider frame; kept for a future extreme blocker).

---

## 10. Removed / archived residue

**Removed this session** (`git rm`, history kept) — unreachable from the live design after the story-read
re-founding:
- **`story.py`** (⛔ `5c30e65`) — the old opaque-token-SVO → GSE bridge; superseded by `narrative.py`'s pure
  contracts path.
- **`coherence.py`** (⛔ `5c30e65`) — the coherence-via-single-role-significance PREFER path; wrong layer
  (used the domain-general reasoner for a single-gene ranking) and the subject-fallacy.
- **`universes/mechanism/`** (⛔ `5c30e65`) — the project-local Regenesis universe for the dumped coherence
  path; the tier-2 account now fires Regenesis's own native narrative universe.

**Archived earlier** (`docs/archive/`, 2026-09-04) — the RIPPED statistical genus (EIR cohort, gnomAD/
panUKBB, phase-2 proposer/verifier, sig-descent) + the pre-refounding orphaning audit; the engine they
document was trashed (`19cf5d1`, `2fa895c`).

**KEPT as canon / records:** `THESIS`, `SYSTEM_DESIGN`, `ETIOLOGY_ENGINE`, `STORY_LAYER`,
`THEORY_OF_THE_CASE`, `PROTEIN_ROLE_GEOMETRY`, `REGULATORY_DEFICIT_PROGRAM`, `GENOTYPE_POLE`,
`DENSITY_PROTOCOL`, `PROBE_STATE`/`PROOF_POINTS`/`DATA_ACCESS_LANDSCAPE`, `decisions/*`, this file.

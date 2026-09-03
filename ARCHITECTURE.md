# Homeostat — Architecture (as-built wiring map, 2026-09-04)

The engineering map of what is **actually wired**, traced from the source (AST import graph +
language-server references), not from memory. It is the definition of the live system: anything not
reachable here is, by construction, archive/rejected residue (see the last section). The *theory* is in
`docs/THESIS.md` / `docs/SYSTEM_DESIGN.md` / `docs/ETIOLOGY_ENGINE.md`; this file is the *instrument*.

The system is a per-person, zero-time **two-sign elimination read** over a multi-network coupling web:
banks render evidence into one event stream; the stream compiles to a positive web + a negative
(censor) set; the engine eliminates candidate mechanisms to a survivor, a certified ⊥, an honest
abstention, or the next discriminating question. Native genre / interpretive / story layers read the
same web; a front door grounds the symptom; a driver (pending) orchestrates the whole read.

## The spine (data flow)

```
symptom text ──ground──▶ resolved concept + active_roles ─┐
                                                          │
person genotype/state ──▶ positions {atomic: Position} ───┤
                                                          ▼
  banks ──▶ Event stream ──┬─ events_to_web ─────────────▶ RelationalWeb (positive couplings)
  (evidence renderers)     └─ events_to_censors ─▶ active_censors(active_roles) ─▶ role censors
                                                          │
                                    clinic.read_from_events / read_presentation
                                                          ▼
        observed_symptoms(positions) ─▶ kill_matrix(web) ─▶ (candidates, positive constraints)
                                                          ▼
             search.eliminate_two_sign(candidates, constraints, censors)  ── the σ-trajectory
                                                          ▼
   clinical_verdict:  BOTTOM (certified ⊥) │ RESOLVED / DEGENERATE │ ASK (jeeves probe) │ ABSTAIN
```

## Layers (module-anchored)

**L0 — primitives (no internal deps).** `otp.py` (Orthogonal Ternary Projection: `ternary`,
`interference` — the signed-ternary algebra); `web.py` (`RelationalWeb`, `Coupling` — the positive
graph); `search.py` (`eliminate_two_sign`, the σ-trajectory `Step`/`Trajectory`, `constraint_disposition`,
`survivors`, `falsifiable`); `jeeves.py` (`Probe`, `select_probe`, `expected_information_gain` — the
STUCK-branch discrimination selector); `kappa.py` (`reachable`/`coverage`/`marginal_coverage`/`is_bridge`
— the κ significance machinery); `paths.py`, `util.py` (repo paths, atomic-write/sha helpers).

**L1 — the event contract + compilers.** `event.py`: `Event` (the L2 record: `network, verb, subject,
target, sign, mode`; `sign` = +1 assert / −1 censor / 0 abstain), `events_to_web` (group by coupling →
`couple_verdict` → draw only convergent-uncontradicted edges), `events_to_censors` + `active_censors`
(the role-scoped negative sign), `couple_verdict` (support/censor tally → coupling / killed / censor /
abstain).

**L2 — the banks (evidence → Events).** Each = a pure renderer + an `*_fetch` I/O shell (data
gitignored, sha-pinned).
- *Global edge banks* (assembled by `prior_web.all_events` → `build_prior_web`): `signor.py` (regulatory,
  DIRECTED), `string.py` (physical binding, undirected vote), `homology.py` (evolutionary / paralog
  `resembles` seeds), `metabolic.py` (Reactome metabolic co-membership). Fetches: `signor_fetch`,
  `string_fetch`, `homology_fetch`, `metabolic_fetch`.
- *Scoped banks* (NOT in `all_events` — they enter per-gene-set at the driver): `coexpression.py`
  (GTEx OTP co-deviation; `gtex_fetch`), `trait_wiring.py` (GWAS pleiotropy node-weight;
  `trait_wiring_fetch`).

**L3 — the engine (the two-sign read).** `position.py` (`Position`, `mine_zero`, `deviation`,
`signature`, `discriminates` — the per-person signed-ternary placement + the discrimination guarantee);
`clinic.py` the apex: `read_from_events` (events + positions + active_roles + probes → compile → read),
`read_presentation` (`observed_symptoms` → `kill_matrix` → `eliminate_two_sign` → `select_probe` →
`clinical_verdict`), `clinical_verdict` (BOTTOM / RESOLVED / DEGENERATE / ASK / ABSTAIN), `ClinicalResult`.

**L4 — native genre + interpretive layers (read the web/events).** `topology.py` (`otp_combine`,
`signed_adjacency` — shared substrate); `tragedy.py` (amplify-cascade → absorbing sink, OTP net-sign);
`comedy.py` (mutual-regulation cycle, loop-gain sign); `fungibility.py` (the allegory layer — paralog
role-equivalence EARNED by ≥2-bank convergence, GATED by the structural eliminator below).

**L4b — the structural pole (biophysics eliminator).** `structural.py`: `translate`, `tm_segments`, the
confidence-gated `structural_class` (membrane / soluble / uncertain) + `structural_compatibility` — the
FUNDAMENTAL-blocker eliminator `fungibility` consumes (membrane-integral vs soluble → bar the merge;
abstain otherwise; NEVER promotes). Also a built-but-UNUSED multi-feature signature primitive
(`composition`/`gravy`/`net_charge`/`aromaticity`/`feature_agreement`/`signature_verdict`/
`signature_compatibility`) — kept for a future *extreme fold-class blocker*, wired to nothing now.
`structural_fetch.py`: Ensembl CDS (per-gene REST `ensure` + bulk `ensure_bulk`/`load_proteins_bulk`).

**L5 — the story bridge + the front door.** `story.py` (events → opaque-token SVO for Regenesis, which
fires ROLES over `universes/mechanism/` — the `.rules` + `archetypes.index`); `ground.py` (the front
door: `ground` = ground-or-abstain symptom resolution, `is_opaque`/`edit_within_1`, `Resolution`).

**Role universe (Regenesis substrate).** `universes/mechanism/rules/*.rules` (amplifier, inhibitor,
binder, homolog, metabolizer, transducer, component, zero_signal) + `archetypes.index`. Roles fire on
verb-class centroids, never gene tokens.

## Entry points & tested surface

- **`prior_web.py`** has the only `__main__` — the CLI that assembles + prints the 4-edge-bank web.
- **`clinic.read_from_events`** is the apex read (the driver/CLI/tests call it; it takes positions +
  active_roles from the caller — object-led, nothing here decides what's active).
- **`ground.ground`** is the symptom front door.
- 28 `tests/test_*.py` cover every live module (+ `test_two_sign.py`, an integration test of the
  eliminate-to-survivor read); every pure decision is Detective-pinned under `tests/detective/`.

## Pending (designed, not yet wired — NOT residue)

- **The driver** — the generate-wide → resolve-narrow orchestrator (ported from Detective's `converge`):
  where the scoped banks (`coexpression`, `trait_wiring`) enter, `fungibility` folds, the genre reads
  fire, and Harmonizer wires gene-symbol dialects. Nothing calls the scoped banks or `fungibility`/
  `tragedy`/`comedy`/`story` yet — they are apex leaves awaiting this orchestrator.
- **The genotype-tier input** — `signal.py` (`Signal`, `Tier`: VERIFIED/REPORTED/…) is built + tested but
  wired to nothing; it is the person-genotype→positions feed the read presumes but no module yet
  produces. *Either* the pending input layer *or* archive — founder to confirm (see below).
- **The blind LRRK2 control** (canon §13.3) — the acceptance test.

## NOT in this map — archive / toss candidates (founder to confirm before I cut)

By the definition at the top, everything below is unreachable from the live design. **I will not delete
these unilaterally** — they are your records; confirm archive-vs-delete for each group:

- **`docs/runs/*` (~30 files, 2026-08-28…08-30)** — pre-refounding experiment logs of the RIPPED
  statistical genus (EIR cohort, PBS pile, gnomAD/panUKBB replication, phase2 proposer/verifier,
  sig-descent, LD block/thin, annotation-recovery). The engine they document was trashed
  (`19cf5d1` "rip the statistical genus", `2fa895c` "trash the old statistical cluster").
- **Pre-refounding docs (verify each):** `CONCEPTUAL_AUDIT.md`, `PHASE2_SIGNIFICANCE_SEARCH.md`,
  `PROOF_POINTS.md`, `PROBE_STATE.md`, `SALVAGE_MANIFEST.md`, `DENSITY_PROTOCOL.md`,
  `DATA_ACCESS_LANDSCAPE.md`, `REGULATORY_DEFICIT_PROGRAM.md`, `decisions/*` — likely statistical-era;
  the current canon is `THESIS.md` / `SYSTEM_DESIGN.md` / `ETIOLOGY_ENGINE.md` / `STORY_LAYER.md` /
  `THEORY_OF_THE_CASE.md` / `PROTEIN_ROLE_GEOMETRY.md` / this file.
- **`signal.py`** — see Pending; archive only if the genotype-tier input is not the intended design.
- **The unused multi-feature signature in `structural.py`** — kept per founder (future extreme blocker);
  listed for completeness, NOT a toss candidate.
```

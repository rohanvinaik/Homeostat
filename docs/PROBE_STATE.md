# PROBE STATE — the multi-lens LRRK2 control + the generalization (2026-08-31)

*Live-experiment record. The confirmed design + the generalization worked out this session are in
`docs/THEORY_OF_THE_CASE.md` (Part II + "The generalization (2026-08-31)") and the auto-loaded
`CLAUDE.md`/`AGENTS.md` (LAW 8–9) — read those first; this is only the running-experiment state.*

## What the control has shown (all measured, real numbers)

The object-agnostic engine is BUILT + pinned (`src/homeostat/{otp,signal,search,nodes,loop}.py`, 74
tests). The first real data run is the **multi-lens LRRK2 positive control** (canon §13.3) — a KNOWN
mechanism, so this is Rung-1 *instrument-validation*, not a novel finding.

- **Slices 1–4** (`probes/lrrk2_slice{1..4}.py`): **no single lens recovers LRRK2.** 3-lens convergence
  (STRING-700, specificity, GTEx co-expression) births NOD2 + RIPK2 and kills most hubs (triad 67% vs
  hub 20%). LRRK2 stays out of the physical/expression lenses — its relationship is genetic.
- **Slice 5 genetic lens over gnomAD EXOMES** (`lrrk2_slice5.py`): **ABSTAINED on LRRK2 & RIPK2** — 0 of
  their variants are in an exome sites file (their disease variants are non-coding). The §12.4 data wall,
  concretely: free exome AF misses the regulatory layer the mechanism lives in. (Abstain ≠ no — the
  informational zero; the vote function now distinguishes them.)
- **1000G via Ensembl, `SAS>EUR` binary, risk-allele polarity** (`lrrk2_slice5_1000g.py`): LRRK2 → **3/3
  born**, but the binary is a **44% coin flip** → noisy (153/289 born, 60% named-hub survival). LRRK2's
  SA-shift is real on its risk allele (`rs11175593` 3.31×), but the lens is not specific.
- **Generalized differentiation lens** (`lrrk2_genetic_diff.py`; max pairwise Fst across the 5 1000G
  superpops via `pbs.hudson_fst`, top-decile vote): **specificity restored** (86/289 born, 20% hub
  survival). Recovers **NOD2** (Fst 0.431, rank 29/242) and **RIPK2** (Fst 0.453, rank 22) as strongly
  population-structured. **LRRK2 → rank 143/242 (Fst 0.148), robustly mid-pack** — its signal is *finer
  than a continent* (the SAS average washes out the Indian-cohort founder signal). **The threshold was
  NOT lowered to force LRRK2 back — the mid-pack rank IS the finding**, and it is exactly what motivates
  the generalization.

## The generalization (recorded in the theory doc this session)

Two coupled moves, both in `docs/THEORY_OF_THE_CASE.md`:
1. **The partition is a free variable** — differentiation across *any legitimately-isolatable group*
   (ancestry at any resolution, a phenotypic sub-section, an exposure), direction-free. SA-vs-EUR was the
   coarsest instance. LRRK2 needs a **finer partition** (sub-continental founder/caste groups).
2. **The unit is the ROLE, not the gene** — the mechanism is invariant; genes are population-local
   *fungible fillers*. Recognize by role (semantic-class firing), never gene-token. **Regenesis is the
   role engine** — use it, don't rebuild it.

## MINIMAL PROOF — PASSED (2026-08-31, `universes/mechanism/`)
The Regenesis role-recognition proof (ETIOLOGY_ENGINE §8) **fires**. Two partitions with DISJOINT filler
genes (amplifier = `genea3` in A, `geneb9` in B) → `common_frame` recovers the invariant role-structure
(sensor, transducer, amplifier, differentiator, component; all 2/2) with no gene-identity correspondence.
Roles fire on the VERB not the token (opaque `Gene*` names); convergence = conjunction (`component`, top
significance 1.39); informational-zero works (`genea4 lacks data → diagnostic`, abstain≠no). **Two
authoring lessons baked in:** (1) align rule objects to the EMITTED lemma (GSE lemmatizes `signaling`→
`signal`) or the rule silently doesn't fire; (2) the copula `is absent` emits NO fact — express the
informational-zero TRANSITIVELY (`lacks data`). What is proven is the REASONING layer on hand-rendered
facts; the censor/node-death was not exercised (needs contradictory input).

## L2 v1 — DONE, end-to-end on REAL data (2026-08-31, `src/homeostat/l2_encoder.py` + `probes/l2_lrrk2.py`)
The L2 role encoder runs the real signals (Fst differentiation over 1000G + GTEx co-expression) → L3
facts → the mechanism universe, composed with the known-mechanism substrate (§2b). Pure core
`data_facts` Detective-pinned (12/12). Result (triad + hubs, opaque tokens): **RIPK2 is the sole
confirmed component** (known transducer role + real population-differentiation converge, top significance
2.30); **NOD2** (rank 29) and **LRRK2** (rank 143) are recognized as their roles but NOT confirmed (not
differentiated at continental resolution) — the §7 finding carried through the FULL stack. Informational-
zero fires (HLA-DRB1, IL1RL1 → diagnostic). **Three authoring lessons (add to the lemma/copula pair):**
(3) a rule verb must be a clean WordNet verb or its object won't bind (`coexpress` → `∅`; use `tracks`).
**Determinism bug fixed:** `cloud_rsids` assigned shared rsIDs via unordered-set iteration (hash-random) →
`diff_data` flipped run-to-run; now `sorted(genes)`. Verified stable across `PYTHONHASHSEED`.

## GRADED INTENSITY — DONE (2026-08-31), the GSE-native way
The flat-`ln 2` degeneracy is solved. GSE (read from primary sources) does NOT carry a continuous scalar
— it stacks discrete ORDINAL markers on a base primitive, and that only reaches significance by becoming
STRUCTURE (significance is κ over the rule graph, magnitude-blind; the emit contract has no magnitude
slot; `world_epa` is emitted-but-unread). So `l2_encoder.diff_tier` bins Fst into ordinal tiers (Wright
bands: dominant ≥0.25, moderate ≥0.05) and a dominant gene STACKS `dominates population` on the base
`differentiates population`; `component.rules` deepens a dominant component into **core** (extra hop).
Result: significance now grades — **core 2.996 (NOD2, RIPK2: dominant Fst + known role) > component 2.303
(LRRK2 moderate; two co-expressing hubs) > differentiator 1.609 > role 0.693 > zero 0.0**. The engine
induced its own graded rules (`sense ∧ differentiate ∧ dominate ⇒ core`). `diff_tier`/`data_facts`
Detective-pinned (26/26). Honest caveats: intensity needs ABSOLUTE Fst bands (not the relative decile),
which lands LRRK2 as a *moderate* (not core) component — the honest nuance, not tuning; and the
co-expression lens is permissive (hubs reach moderate component but never core).

## DENSITY + EVIDENCE-THRESHOLDS + NO HARD-CODING — DONE (2026-08-31)
**Hard-coded gene→role bindings NUKED** (founder, cardinal: one correct version, no purposivistic
role-assignment). The L2 shell no longer authors `NOD2 senses pathogen` etc.; the mechanism emerges
PURELY from CONVERGENCE across the computed data lenses — population differentiation (Fst ordinal tier),
GTEx co-expression, STRING physical binding, informational zero. The signaling-role vocabulary stays in
the universe but only fires when real directed evidence (Reactome) supplies it, as data.
Lenses/thresholds: STRING ≥700 (evidence tier); co-expression cutoff = GTEx-null 95th percentile
(**0.266**, deterministic permutation — not 0.5). Result (no roles authored): **core 3.178 = NOD2, RIPK2**
(dominant diff + co-expression converge; RIPK2 also binds); **component 2.485 = LRRK2 + two co-expressing
hubs**; TNFSF15 differentiated-but-unconverged (not a component); HLA-DRB1/IL1RL1 → diagnostic. The engine
induced its own core rules from the data. `diff_tier`/`data_facts` Detective-pinned (29/29).
**Honest:** without a *computed* directed-signaling lens, co-expression is permissive (hubs reach moderate
component) — the Reactome lens would sharpen it FROM EVIDENCE, never by authoring. Ranking "3 lenses > 2"
still needs a lens-count stack (`core ∧ binds ⇒ deep-core`).

## THE NEXT ACTION — lens-count stack + more surfaces + a geneticist
(1) The lens-count stack (deep-core) so more converging surfaces rank higher. (2) More lenses:
trait-wiring (in hand), Reactome-directed roles (needs pull), the measuring_agi perturbation panel.
(3) Derive the remaining thresholds from evidence (Fst tiers from the cloud's own distribution). (4) The
real populate-the-surfaces work is a doctor/geneticist filling the frame/rule set with recorded evidence.
Do NOT fake intensities, invent role-facts, or plug conventional-default thresholds (evidence-derived per
lens). The full design is recorded in **`docs/ETIOLOGY_ENGINE.md`** (self-contained
— thesis + two-layer architecture + the mechanism-universe design, distilled from the founder's working
universes: ARC_AGI_3 L2/L3 render→speak split, MentalAtlas `zero_signal`/marker taxonomy, Regenesis
`UNIVERSE_AUTHORING.md`). **Next = build the minimal proof (ETIOLOGY_ENGINE §8):** hand-render
NOD2–RIP2–LRRK2 as L3 facts for two contrasting partitions, author ~4 role-Forms + convergence
conjunction + zero-signal + censor twin, run `understand()` per partition, and check `common_frame`
recovers the invariant role-structure while the filler genes differ. Do NOT fabricate role anchors or
rewrite input to hit a rule's verbs (fix the centroid, never the input).

## Discipline (do not drift)
- Statistics/differentiation is a **lens vote**, never the significance; the significance is convergence /
  σ. Never read one map's shape (STRING hubs) as the answer (Act-2 death).
- **Never tune a threshold to make LRRK2 survive.** An honest negative (or a finer-partition need) is the
  finding, not a failure to fix.
- Roles are **semantic classes with centroids from relational geometry** — deterministic (GSE/HDC), never
  a learned embedding, never hand-drawn to fit (that is σ_sem = 0 one level up).

## Pointers / artifacts
Probes: `probes/lrrk2_slice{1..5}.py`, `lrrk2_slice5_1000g.py`, `lrrk2_genetic_diff.py`. Fetch/extract
scripts live in the session scratchpad (Ensembl 1000G 5-superpop pull; `/tmp/1000g_5pop_af.tsv` cache is
ephemeral, re-fetchable). **Debt (the JIT-fix):** the 1000G AF pull is now a fast one-time Ensembl call;
gnomAD-genomes-by-rsID (option **D**, non-coding-inclusive, matches like the exomes did) is deferred by
the founder. Engine: `src/homeostat/{otp,signal,search,nodes,loop,pbs}.py`.

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

## THE NEXT ACTION
**Scale the L2 encoder:** derive the role-events (`amplifies signal`, `differentiates population`, …)
from the REAL relational geometry (Fst differentiation in hand; GTEx co-expression in hand; directed
`amplifies/inhibits` needs Reactome/directed pathway data) instead of hand-rendering them, then run the
LRRK2 mechanism through the universe for real. The reasoning layer is validated; the encoder is the work.
The full design is recorded in **`docs/ETIOLOGY_ENGINE.md`** (self-contained
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

# The Genotype-Deep Pole — a person-structural PRIOR on the mechanism (design)

Status: DESIGN (settled 2026-09-04, Socratic). Not yet built. Companion to `docs/PROTEIN_ROLE_GEOMETRY.md`
(the structural eliminator, built) and `docs/decisions/marker_reference.md` (the marker producer, built).
Grounded on: `src/homeostat/structural.py` (read), GenomeVault's complementary-pair HDV encoding
(`docs/guides/Key Guides/HDV_research/HDC_Complementary_Pair_Genomic_Encoding.md`, read), and the
built marker producer / certification gate (this session).

## 1. What a genotype IS — a PRIOR on the mechanism, not an observation

A **marker** is a *downstream observation* — a measured readout, a lit pixel of the shadow; it deviates
against a demographic **population norm** (is this abnormal *for you*), and it enters the read as an
observed symptom (`producer.signals_to_positions`).

A **genotype is not that.** A germline variant is an *upstream determinant*: it does not *observe* that
a gene is perturbed, it *predicts* the protein is functionally altered. Marker : genotype :: effect :
cause. So a genotype enters the read as a **prior on the mechanism** — a per-gene **source-prior /
node-weight** biasing *which* source the elimination favors, **never a symptom, never a lit pixel.**

It is the **person-structural twin of `trait_wiring`**: `trait_wiring` is the *population* prior (GWAS
pleiotropy, a tier-3 Law-9 node-weight); the genotype pole is the same *type* of object (a per-gene
node-weight) with *person-structural* provenance (the variant's own consequence). Two node-weights,
same role, opposite provenance — and **neither resolves anything alone.** The mechanism is where the
genotype prior CONVERGES with the coupling banks and the shadow.

## 2. The register — non-statistical by design (the load-bearing premise)

The project is predicated on the fact that **single points of truth do not generalize into an
etiology** — if a single variant could resolve the mechanism cleanly, this system would not need to
exist. So the genotype prior is *evidence that converges*, never a decider. Consequences:

- **Sacrificing the population/statistical read costs some S/N on the above-threshold signal.** Accepted.
- **The clear signals still resolve** — a nonsense variant flipping `structural_class`, a massive
  composition change, are *definitionally* clear, so the pole still emits them, just at lower valence
  than a p-value would assign.
- **It recovers what population statistics structurally CANNOT** — the sub-threshold, fungible-cast, n=1
  signal population methods smear. A hit we take on purpose.
- Anyone using this system is not reaching for the standard statistical toolkit; that already exists.

## 3. The shape — a consequence VECTOR (HDV), deterministic VSA

The genotype prior is a **vector**, not a scalar — because the value of a vector is the **algebra** it
enables (compare / bundle / project). It is built with GenomeVault's **deterministic** Vector-Symbolic
Architecture (complementary-pair encoding + bind/bundle) — **NOT** the learned-codebook / gradient
variant GenomeVault floats as a footnote (that is the ML detour; we do not take it). GenomeVault has
already done the hard design work; Homeostat builds a **tight local version**, reusing their mechanisms.

### 3.1 The three axes (bundled into the consequence-HDV)

1. **structural-consequence** — the functional change. Apply the variant to the CDS, re-read the class
   and features (`structural.py`: `structural_class`, `composition_distance`, `gravy`, `net_charge`,
   `aromaticity`), measure the DELTA vs the reference protein. Confidence-gated: clear change -> strong,
   ambiguous -> abstain.
2. **biophysics — DNA structural mechanics from sequence** (verified from source; supersedes the
   earlier "encoding-difficulty" framing). The variant's effect on the LOCAL DNA's mechanical
   structure, read via literature dinucleotide scales (GenomeVault `biophysical_properties.py`, ported
   tight to `biophysics.py`): the rigid<->flexible phase signal -- YR/RY balance and bendability
   (Bolshoy 1991). RY-biased = rigid, YR-biased = flexible. Deterministic, annotation-free -- "structure
   without structure" in its tightest form. The axis is the property DELTA (variant vs reference local
   sequence). (The complementary-pair *encoding-difficulty* signal -- errors-as-detectors, 44x genic
   p<1e-90 -- is a related but HEAVIER signal, deferred; the structural-mechanics scales are the tight
   reusable kernel, and v1 is a DENSE feature vector (design A), not a full HDV/VSA (design B, deferred).)
3. **presence/rarity** — reference-departure (hom-ref = no prior; het/hom-alt = present) + the noise
   gate (private/novel = maybe error -> weaker prior / lower tier). This is the observation/tier gate,
   not the magnitude.

### 3.2 The split (design B) — signals only where they belong

The elimination is a **pure logic gate** (two-sign sigma over the web); cosine math has no place inside
it. So, exactly as the marker's `Differential` rides alongside the lean `Position` coordinate:

- **The HDV -> the interpretive layer.** The rich consequence-vector feeds fungibility, role-recognition
  (Regenesis), and variant clustering — where similarity/composition are the native operations.
- **A projected source-prior -> the elimination.** The HDV projects down to a clean ternary/scalar
  per-gene prior (the gate's currency). No vector enters the logic gate.

## 4. Fungibility at the genotype level — cosine of consequence-vectors

The elegant payoff: two variants (in two paralogs) whose **consequence-HDVs are similar** are **fungible
for the mechanism** — the same fan-in role-equivalence `fungibility.py` earns by bank-convergence, now
native as *cosine similarity in HDV space*. The genotype vector makes genotype-level fungibility a
one-line comparison, and it lives at the interpretive layer (per the split), never in the gate.

## 5. Entry into the read — shared with `trait_wiring` (a DRIVER concern)

How a source-prior biases the elimination *without deciding it* (Law 7: never collapse plurality by a
prior) is the same problem `trait_wiring` has, and `trait_wiring`'s "application lands in the driver."
So both node-weight priors — population (`trait_wiring`) and person-structural (genotype) — enter the
read the same way, at the **driver** (thread 3). The genotype pole PRODUCES the prior; the driver WIRES
it. That keeps this pole's scope to production.

## 6. Build plan — a tight local version reusing GenomeVault's VSA

Order, each gated (ruff/ty/pytest/Detective), pure decisions pinned:
1. **Ground first (two-step):** read GenomeVault's actual VSA (`biophysical_properties.py`, the
   complementary-pair encoder) and `structural.py`'s feature functions from SOURCE — reuse their
   mechanisms, do not reinvent HDC. (`hdc_experimentation/` is untracked in GenomeVault's git but present
   locally; verify the p<1e-90 / p=1e-15 kernel figure from source, online repo if the local is partial.)
2. **The consequence encoder** — variant -> the three axes -> a bundled HDV (deterministic VSA).
3. **The projection** — HDV -> the per-gene source-prior (the gate's ternary/scalar).
4. **Fungibility-by-cosine** — the interpretive-layer comparison over consequence-HDVs.
5. **FIRE** on a real variant axis; DEFER the driver-side entry to thread 3.

## 7. Deferred / to-verify

- The exact GenomeVault biophysics kernel (the p=1e-15 oncogenic-enrichment figure) — verify from source
  when building axis (2); the online GenomeVault repo if the local `hdc_experimentation/` copy is partial.
- The mechanistic-prediction SECOND marker reference (docs/decisions/marker_reference.md) — a clinician's
  call; the disagreement between it and the population norm is the cross-network operator. Still deferred.
- The driver-side prior entry (Law 7-safe biasing) — thread 3, shared with `trait_wiring`.

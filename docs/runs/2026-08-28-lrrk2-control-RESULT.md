# Run record — §13.3 LRRK2 positive control: **FAIL** (2026-08-28)

**Verdict under the preregistered criterion (commit ff8808e): FAIL — anchors
array-covered but not recovered.** Per the preregistration's interpretation
commitments: the method at its current data scale cannot see the known bridge,
this is reported as such, no dial was iterated to convert the fail into a
pass, and Law 8 remains in force — no novel output of the pipeline is a
finding.

## The derivation (blind side, as preregistered)
3,877 E/I/R loci → positional mapping (26,969 refGene envelopes, ±25kb) →
G = 4,041 scored genes → STRING physical subgraph (score ≥ 400; 15,809
proteins) → 774 components (largest 1,652) → top-20 connectors. LRRK2, NOD2,
RIPK2: absent from G. Clause (a) false, clause (b) false.

## Why it failed — three stacked data facts (diagnosed after, evaluation-side)

1. **The known variant is not typed.** rs1873613 (the Indian-cohort
   LRRK2/leprosy variant, checkpoint §9) is absent from the v5 array. The
   array's SNP content is itself calibrated against the European discovery
   literature — §11.5's point, now bitten concretely.
2. **The E/I/R prior actively deprioritizes NOD2 for this individual.** All 25
   array variants in the NOD2 envelope have priority 0: R matches the European
   allele or the site shows no SAS-positive divergence. §7.1 operating as
   specified — and specifying away a bridge anchor.
3. **LRRK2/RIPK2 signal is weak and got absorbed.** In-envelope maxima 0.024 /
   0.039 (queue top: 1.17); under 500kb positional clumping those variants were
   absorbed by stronger leads 200–660kb away, so no lead position mapped to
   either gene. Lead-only gene mapping is a recorded resolution artifact.

## What this means (and does not mean)

- **This is the checkpoint's own §5.8 prediction, demonstrated on its own
  positive control:** the bridge's effect exists only in composition
  (LRRK2×NOD2 epistasis); a per-variant prior — which is exactly what the
  Phase-1 E/I/R queue is — is a single-variant object and cannot express it.
  "The genes where the search guarantee is weakest are the same genes that
  will never clear single-variant significance."
- The failure therefore does NOT falsify the program; it falsifies the hope
  that Phase-1 machinery alone could pass §13.3. The "full pipeline" the
  checkpoint demands includes the composition/coherence layer (κ-descent) over
  population-scale data (I_ind is population-latent, §5.10/§11.2) and richer
  coupling channels (co-expression, dynamics — §12.4). Those are now the
  demonstrated-necessary next work, not optional extensions.
- It also does not license re-running with looser dials until the control
  passes. The control re-runs when the machinery materially changes (new
  coupling channel, cohort data, composition layer), each time preregistered.

## Process note
After the first run returned NOT-EVALUABLE, the evaluation was made STRICTER
(coverage-aware): NOT-EVALUABLE is reserved for genuine array non-coverage;
since the array covers all three envelopes (56/25/18 variants), the verdict is
FAIL. A post-hoc evaluation change was permitted here only because it can
downgrade verdicts, never upgrade them.

## Consequences for §13.2's null
The validator-sensitivity caveat in the §13.2 record gains force: the same
resolution limits (windowed stats, positional clumping, array content) bound
both results. The two records should be read together as: **Phase-1 output is
a search-order prior with no demonstrated selection enrichment and no
demonstrated bridge recovery — machinery, not findings.**

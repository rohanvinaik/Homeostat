# Run record — Phase-2 LLM proposer + selection-weighted κ: **FAIL** (2026-08-28)

**Verdict under the preregistered criterion (3109b3f): FAIL.** The
LLM-propose / structure-verify / selection-weight pipeline does not beat the
generic-connectivity null at this data scale. Reported as-is; no dial iterated
to flip it.

## The flood worked; the verifier could not confirm
- 6 independent proposer angles → **219 proposals, 135 distinct genes**, frozen
  to `data/network/proposals.jsonl`. Plausible biology throughout (autophagy,
  UPR, efferocytosis, inflammasome). The generate side is a real firehose.
- The FAILURE is entirely on the VERIFY side.

## Criterion A (firewall) — PASSES LITERALLY, but the pass is HOLLOW
| | rate |
|---|---|
| LLM out-of-universe grounding | 0.973 |
| random-gene grounding | 0.955 |

LLM grounds above random and below 100%, so the corrected criterion A is met —
but **95% of RANDOM genes also ground.** On the one dense inflammation module
(Build-1 finding), "has any STRING/co-expression edge to the 1,299-gene
universe" admits nearly everything, so grounding is **non-discriminating**. The
generate/verify asymmetry cannot bite when the verifier accepts almost all
inputs. Recorded as a hollow pass, not a real filter.

## Criterion B (selection-lift, degree-matched) — FAILS, decisive
- 107 grounded out-of-universe proposals; 62 with iHS data; mean iHS 0.795.
- Degree-matched permutation **p = 0.344** — not enriched beyond equally-
  connected control genes. Consistent with §13.2's null and §13.4's degree
  confound: gene-level iHS, degree-controlled, does not separate these
  candidates.

## Contamination — confirmed empirically (why LRRK2-via-LLM was never a control)
NOD2 and RIPK2 were proposed by **all 6** angles, LRRK2 by **5** — the LLM
recalls the famous held-out bridges trivially. This is exactly the §6.4/PHASE2
contamination the pass criterion was built to not depend on. (All three are
in-universe, so they sit outside the out-of-universe ranking; iHS: NOD2 1.21,
RIPK2 0.75, LRRK2 no envelope data.)

## Top selection-weighted out-of-universe hits (candidates, NOT findings)
CALCOCO2, ATF6, EPG5, ATF4, MTOR, AXL, TBK1, CASP1, GBP1, ATG12 — high-iHS
autophagy/UPR/efferocytosis genes. Plausible, unvalidated, and — given criterion
B — not distinguished from degree-matched chance. Reported as leads only.

## The through-line (four phases now agree)
§13.2 (null), §13.3 (FAIL), §13.4 (degree confound), Phase-2 (FAIL): at this
data scale and substrate — PPI + co-expression module, gene-level iHS, **no
cohort, no dynamics** — NO method, deterministic or LLM-proposed, separates the
known bridges from generic connectivity. Expanding the *proposal* space does not
help because the *verifier's* discriminating power is the binding constraint.
That is checkpoint **§12.4**: the missing dynamics/cohort data, arrived at
independently from four directions. The generate/verify architecture is sound;
its verify substrate is too weak until cohort-scale, state-resolved data exists
(I_ind is population-latent, §5.10/§11.2).

## What this does and does not license
- Does NOT license iterating the firewall/threshold to force a pass (that is the
  p-hack the preregistration exists to prevent). A stronger firewall (multi-
  channel edges, bridge-only admission, κ-threshold) is only worth building
  once a substrate exists on which it can discriminate — i.e. after §13.5-grade
  cohort data (Genes & Health / NCT04698291), not before.
- DOES establish, honestly, that the Phase-1/Phase-2 program on public + n=1
  data is a hypothesis-generation and method-validation exercise whose binding
  constraint is now precisely located. That is a publishable negative result
  about method, not a failure of nerve.

## Outputs
- `data/network/proposals.jsonl` — frozen flood (219 rows, provenance per angle).
- `data/e_i_r/propose_verify.json` — full result, both criteria, controls, leads.

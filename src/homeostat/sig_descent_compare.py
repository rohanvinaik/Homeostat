"""Cross-cohort comparison of the selection-weighted κ (§III) — the coherence test.

Reads both sig_descent JSONs and asks: (1) does the control-lift REPLICATE (κ_PBS
ranks the bridges better than κ_unweighted in both cohorts)? (2) does the top-κ_PBS
set DIVERGE across cohorts (PBS load-bearing)? (3) does the top-N pleiotropy
enrichment replicate? Divergent-yet-replicating is the coherent outcome the hard
PBS-restriction failed to reach. Run: make sig-descent-compare.
"""

import json
import sys

from homeostat import paths
from homeostat.util import atomic_write_json

PK = paths.EIR / "sig_descent.json"
GN = paths.EIR / "sig_descent_gnomad.json"
OUT = paths.EIR / "sig_descent_comparison.json"


def main() -> None:
    for f in (PK, GN):
        if not f.exists():
            sys.exit(f"[sig-compare] missing {f.name} — run sig-descent for both cohorts first")
    with open(PK) as fh:
        pk = json.load(fh)
    with open(GN) as fh:
        gn = json.load(fh)

    top_pk, top_gn = set(pk["top_kappa_pbs"]), set(gn["top_kappa_pbs"])
    jac = round(len(top_pk & top_gn) / len(top_pk | top_gn), 4)

    lift_pk = pk["control_lift"]["_mean_control_rank"]
    lift_gn = gn["control_lift"]["_mean_control_rank"]
    lift_replicates = lift_pk["lift_vs_unweighted"] > 0 and lift_gn["lift_vs_unweighted"] > 0
    beats_raw = lift_pk["lift_vs_raw_pbs"] > 0 and lift_gn["lift_vs_raw_pbs"] > 0

    p_pk = pk["top_pleiotropy_s32"].get("p")
    p_gn = gn["top_pleiotropy_s32"].get("p")
    pleio_replicates = (p_pk or 1) < 0.05 and (p_gn or 1) < 0.05

    result = {
        "stage": "§III selection-weighted κ — cross-cohort coherence test",
        "top_kappa_pbs_jaccard": jac,
        "control_lift_vs_unweighted": {
            "pan_ukbb": lift_pk["lift_vs_unweighted"],
            "gnomad": lift_gn["lift_vs_unweighted"],
        },
        "control_lift_replicates": lift_replicates,
        "beats_raw_pbs_both": beats_raw,
        "top_pleiotropy_p": {"pan_ukbb": p_pk, "gnomad": p_gn},
        "pleiotropy_replicates": pleio_replicates,
        "control_mean_rank_pk": lift_pk,
        "control_mean_rank_gn": lift_gn,
        "verdict": _verdict(lift_replicates, beats_raw, pleio_replicates),
    }
    atomic_write_json(OUT, result)
    print(
        f"[sig-compare] control-lift vs unweighted: pk={lift_pk['lift_vs_unweighted']} "
        f"gn={lift_gn['lift_vs_unweighted']} (replicates={lift_replicates})"
    )
    print(f"[sig-compare] beats raw-PBS both: {beats_raw}")
    print(f"[sig-compare] top-κ_PBS Jaccard across cohorts: {jac} (lower = more load-bearing)")
    print(f"[sig-compare] top-N pleiotropy p: pk={p_pk} gn={p_gn} (replicates={pleio_replicates})")
    print(f"[sig-compare] verdict: {result['verdict']}")
    print(f"[sig-compare] complete -> {OUT}")


def _verdict(lift: bool, beats_raw: bool, pleio: bool) -> str:
    if lift and beats_raw and pleio:
        return (
            "COHERENT: selection-weighted κ lifts the bridges (replicated), beats raw PBS "
            "and unweighted κ alone, and its top is pleiotropy-enriched in both cohorts. "
            "The §III layer is the operationalization the gates could not provide."
        )
    if lift and beats_raw:
        return (
            "PARTIAL: the control-lift replicates and beats both components, but the top-N "
            "pleiotropy did not replicate. Selection-weighting helps the known bridges; "
            "broad enrichment is not established."
        )
    return (
        "NEGATIVE: soft PBS-weighting does not coherently lift the bridges across cohorts. "
        "Strengthens the §12.4 (missing-dynamics) conclusion: static data cannot make the "
        "population signal do coherent work. Recorded honestly, not tuned."
    )


if __name__ == "__main__":
    main()

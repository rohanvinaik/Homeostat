"""Cross-cohort comparison of the PBS-restricted sweeps — the load-bearing test.

Under the OLD all-genes candidate set, Pan-UKBB and gnomAD overlapped 99.7% and
gave ~identical gate results (PBS not load-bearing). If restricting the candidate
set to the top-K PBS ranking makes PBS load-bearing, the two cohorts' top-K seed
sets should overlap MUCH less, and the LRRK2 / §3.2 results should diverge.

Reads both sweep JSONs (Pan-UKBB `pbs_restricted_sweep.json` + gnomAD
`pbs_restricted_sweep_gnomad.json`) and reports per (mode, K): seed-set Jaccard,
LRRK2 verdict agreement, §3.2 result divergence. Run: make pbs-restricted-compare.
"""

import json
import sys

from homeostat import paths
from homeostat.util import atomic_write_json

PK = paths.EIR / "pbs_restricted_sweep.json"
GN = paths.EIR / "pbs_restricted_sweep_gnomad.json"
OUT = paths.EIR / "pbs_restricted_comparison.json"


def jaccard(a: list[str], b: list[str]) -> float:
    sa, sb = set(a), set(b)
    return len(sa & sb) / len(sa | sb) if (sa or sb) else 1.0


def main() -> None:
    for f in (PK, GN):
        if not f.exists():
            sys.exit(f"[compare] missing {f.name} — run the sweep for both cohorts first")
    with open(PK) as fh:
        pk = {(r["mode"], r["k"]): r for r in json.load(fh)["runs"]}
    with open(GN) as fh:
        gn = {(r["mode"], r["k"]): r for r in json.load(fh)["runs"]}

    rows = []
    for key in sorted(set(pk) & set(gn)):
        mode, k = key
        a, b = pk[key], gn[key]
        seed_j = jaccard(a["seeds"], b["seeds"])
        rows.append(
            {
                "mode": mode,
                "k": k,
                "seed_jaccard": round(seed_j, 4),
                "lrrk2_verdict_pk": a["lrrk2_gate"]["verdict"],
                "lrrk2_verdict_gn": b["lrrk2_gate"]["verdict"],
                "lrrk2_agree": a["lrrk2_gate"]["verdict"] == b["lrrk2_gate"]["verdict"],
                "s32_p_pk": a["s32_pleiotropy"].get("p"),
                "s32_p_gn": b["s32_pleiotropy"].get("p"),
                "s32_obs_pk": a["s32_pleiotropy"].get("observed_mean"),
                "s32_obs_gn": b["s32_pleiotropy"].get("observed_mean"),
                "n_cand_pk": a["n_candidates_bridges"],
                "n_cand_gn": b["n_candidates_bridges"],
            }
        )

    mean_seed_j = round(sum(r["seed_jaccard"] for r in rows) / len(rows), 4) if rows else None
    result = {
        "stage": "PBS-restricted cross-cohort comparison (is PBS now load-bearing?)",
        "baseline_all_genes_overlap": 0.997,  # the old, PBS-not-load-bearing overlap
        "mean_seed_jaccard": mean_seed_j,
        "interpretation": (
            "seed_jaccard << 0.997 means the top-K PBS candidate set is genuinely "
            "cohort-dependent -> PBS is load-bearing. Divergent LRRK2/§3.2 results "
            "across cohorts confirm the population signal now drives the gates."
        ),
        "rows": rows,
    }
    atomic_write_json(OUT, result)
    print(
        f"[compare] mean top-K PBS seed Jaccard across cohorts: {mean_seed_j} (was 0.997 all-genes)"
    )
    print(
        f"{'mode':<8}{'K':>6}{'seedJ':>8}{'LRRK2 pk/gn':>16}{'§3.2 p pk/gn':>18}{'obs pk/gn':>16}"
    )
    for r in rows:
        print(
            f"{r['mode']:<8}{r['k']:>6}{r['seed_jaccard']:>8}"
            f"{r['lrrk2_verdict_pk'][:4] + '/' + r['lrrk2_verdict_gn'][:4]:>16}"
            f"{str(r['s32_p_pk']) + '/' + str(r['s32_p_gn']):>18}"
            f"{str(r['s32_obs_pk']) + '/' + str(r['s32_obs_gn']):>16}"
        )
    print(f"[compare] complete -> {OUT}")


if __name__ == "__main__":
    main()

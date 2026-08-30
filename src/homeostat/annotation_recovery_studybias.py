"""§3.2 study-bias control — re-run the annotation-recovery test with a THIRD
matching stratum: PubMed-citation tertile (study intensity), alongside degree and
PBS. Closes the named residual confound of the passed §3.2 (candidates are ~2×
more studied). Does the pleiotropy enrichment survive?

Criterion FROZEN in docs/runs/2026-08-30-annotation-recovery-studybias-PREREGISTRATION.md.
Run: make annotation-recovery-studybias.
"""

import datetime
import random
import sys

from homeostat import paths
from homeostat.annotation_recovery import (
    GWAS,
    N_PERM,
    P_CANDIDATE,
    SEED,
    load_pleiotropy,
    load_scores,
    matched_null_test,
)
from homeostat.bridge_discovery import SCORES_FULL
from homeostat.litcount import load_pubmed_counts
from homeostat.util import atomic_write_json

DEGREE_BAND = 0.20
PBS_TOL = 0.02
OUT = paths.EIR / "annotation_recovery_studybias.json"


def tertiles(values: list[int]) -> tuple[int, int]:
    """The n//3 and 2n//3 order statistics (deterministic tertile cuts)."""
    s = sorted(values)
    n = len(s)
    return s[n // 3], s[2 * n // 3]


def eligible_3way(
    candidates: list[str],
    background: list[str],
    scores: dict[str, tuple[int, float, float, float]],
    tertile: dict[str, int],
) -> dict[str, list[str]]:
    """Per candidate: background genes matched on degree ±BAND AND pbs ±TOL AND
    same PubMed tertile."""
    out: dict[str, list[str]] = {}
    for c in candidates:
        dc, _pc, pbc, _ = scores[c]
        tc = tertile[c]
        lo, hi = 0.8 * dc, 1.2 * dc
        out[c] = [
            g
            for g in background
            if lo <= scores[g][0] <= hi and abs(scores[g][2] - pbc) <= PBS_TOL and tertile[g] == tc
        ]
    return out


def main() -> None:
    if OUT.exists():
        print(f"[studybias] already complete ({OUT}); delete to re-run")
        return
    for req in (SCORES_FULL, GWAS):
        if not req.exists():
            sys.exit(f"[studybias] missing input: {req}")

    print("[studybias] loading scores, pleiotropy, pubmed counts ...")
    scores = load_scores(SCORES_FULL)
    ranked = sorted(scores, key=lambda g: (scores[g][3], -scores[g][1], g))
    candidates = [g for g in ranked if scores[g][3] < P_CANDIDATE]
    background = [g for g in ranked if scores[g][3] >= P_CANDIDATE]

    pleio = {g: float(v) for g, v in load_pleiotropy(GWAS).items()}
    pubmed = load_pubmed_counts()
    pc = {g: pubmed.get(g, 0) for g in scores}
    t1, t2 = tertiles(list(pc.values()))
    tertile = {g: (0 if v <= t1 else (1 if v <= t2 else 2)) for g, v in pc.items()}

    cand_mean_pub = sum(pc[g] for g in candidates) / len(candidates)
    bg_mean_pub = sum(pc[g] for g in background) / len(background)
    print(
        f"[studybias] candidate pubmed mean {cand_mean_pub:.1f} vs background "
        f"{bg_mean_pub:.1f}; tertile cuts {t1},{t2}"
    )

    eligible = eligible_3way(candidates, background, scores, tertile)
    primary = matched_null_test(candidates, eligible, pleio, N_PERM, random.Random(SEED))

    sens_size = {}
    for n in (100, 300):
        subset = candidates[:n]
        sens_size[f"top_{n}"] = matched_null_test(
            subset, {c: eligible[c] for c in subset}, pleio, N_PERM, random.Random(SEED)
        )
    no_lrrk2 = [c for c in candidates if c != "LRRK2"]
    sens_no_lrrk2 = matched_null_test(
        no_lrrk2, {c: eligible[c] for c in no_lrrk2}, pleio, N_PERM, random.Random(SEED)
    )

    p = primary.get("p", 1.0)
    verdict = (
        "§3.2 SURVIVES study-bias control (pleiotropy enriched beyond degree+PBS+study)"
        if p < 0.05
        else "§3.2 does NOT survive study-bias control (study intensity explains it)"
    )

    result = {
        "stage": "§3.2 annotation-recovery — study-bias-controlled (degree+PBS+pubmed-tertile)",
        "completed": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "preregistration": "docs/runs/2026-08-30-annotation-recovery-studybias-PREREGISTRATION.md",
        "verdict": verdict,
        "confound_magnitude": {
            "candidate_mean_pubmed": round(cand_mean_pub, 1),
            "background_mean_pubmed": round(bg_mean_pub, 1),
            "pubmed_tertile_cuts": [t1, t2],
        },
        "dials": {
            "p_candidate": P_CANDIDATE,
            "degree_band": DEGREE_BAND,
            "pbs_tol": PBS_TOL,
            "n_perm": N_PERM,
            "seed": SEED,
            "third_stratum": "pubmed tertile",
        },
        "primary_pleiotropy_3way": primary,
        "sensitivity_candidate_size": sens_size,
        "sensitivity_leave_lrrk2_out": sens_no_lrrk2,
    }
    atomic_write_json(OUT, result)
    print(f"[studybias] verdict: {verdict}")
    print(
        f"[studybias] primary 3-way: observed {primary.get('observed_mean')} vs null "
        f"{primary.get('null_mean_avg')}, p={primary.get('p')} "
        f"(dropped={primary.get('n_dropped_no_match')})"
    )
    print(f"[studybias] complete -> {OUT}")


if __name__ == "__main__":
    main()

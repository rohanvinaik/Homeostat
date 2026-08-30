"""§3.2 — annotation-recovery validator on the §3.3 candidate bridges.

The program's PRIMARY FALSIFIER (§3.2): recovery of known annotation WITHOUT
having used it. The §3.3 bridge discovery ranked genes by degree-matched
community participation over a function-blind coupling graph (PBS + STRING
physical + GTEx co-expression) — no trait/disease annotation anywhere. This asks,
systematically (never by eye — §12.6): are the 628 candidate bridges enriched for
GWAS multi-trait PLEIOTROPY vs a degree- AND PBS-matched background? Pleiotropy is
phenotype-level annotation the derivation never saw, so enrichment = §3.2 holds.

Criterion FROZEN in docs/runs/2026-08-30-annotation-recovery-PREREGISTRATION.md
(committed 16ddddf, before this file existed). Run: make annotation-recovery.
"""

import datetime
import gzip
import random
import sys

from homeostat import paths
from homeostat.bridge_discovery import SCORES_FULL
from homeostat.util import atomic_write_json

GWAS = paths.DATA / "network" / "gwas-catalog-download-associations-alt-full.tsv"
OUT = paths.EIR / "annotation_recovery.json"

# Dials — fixed by the preregistration; do not tune after.
P_CANDIDATE = 0.05  # candidate = degree_matched_p < this (the frozen 628)
DEGREE_BAND = 0.20  # ±20% degree match (the LRRK2-gate null)
PBS_TOL = 0.02  # ±0.02 pbs_weight match
N_PERM = 10_000
SEED = 20_260_830

# §6 exploratory clearance/resolution set (hand-picked, function-derived, small —
# a LEAD, never the falsifier; the "ama" clearance category, §1.3/§6.7).
CLEARANCE = frozenset(
    {"MERTK", "GAS6", "ELMO1", "ABCA1", "ALOX5", "ALOX15", "ALOX15B", "LGMN", "ATG7", "RUBCN"}
)


def load_scores(path) -> dict[str, tuple[int, float, float, float]]:
    """gene -> (degree, participation, pbs_weight, degree_matched_p)."""
    out: dict[str, tuple[int, float, float, float]] = {}
    with gzip.open(path, "rt", encoding="utf-8") as f:
        next(f)  # header
        for line in f:
            g, deg, part, pbs, p = line.rstrip("\n").split("\t")
            out[g] = (int(deg), float(part), float(pbs), float(p))
    return out


def load_pleiotropy(gwas_tsv) -> dict[str, int]:
    """gene -> number of DISTINCT EFO mapped-trait URIs (phenotype pleiotropy).

    Trait associations were never used in the derivation, so this is the clean
    §3.2 channel. MAPPED_GENE splits on ', ' and ' - ' (intergenic flanks);
    MAPPED_TRAIT_URI splits on ', '. A gene absent from the catalog -> 0.
    """
    traits: dict[str, set[str]] = {}
    with open(gwas_tsv, encoding="utf-8", errors="replace") as f:
        header = f.readline().rstrip("\n").split("\t")
        gi = header.index("MAPPED_GENE")
        ui = header.index("MAPPED_TRAIT_URI")
        for line in f:
            fld = line.rstrip("\n").split("\t")
            if len(fld) <= max(gi, ui):
                continue
            uris = [u.strip() for u in fld[ui].split(",") if u.strip()]
            if not uris:
                continue
            for gene in fld[gi].replace(" - ", ",").split(","):
                g = gene.strip()
                if g:
                    traits.setdefault(g, set()).update(uris)
    return {g: len(u) for g, u in traits.items()}


def eligible_matches(
    candidates: list[str],
    background: list[str],
    scores: dict[str, tuple[int, float, float, float]],
) -> dict[str, list[str]]:
    """Per candidate: background genes within ±DEGREE_BAND degree AND ±PBS_TOL
    pbs_weight. Empty pools -> candidate dropped from the test (reported)."""
    out: dict[str, list[str]] = {}
    for c in candidates:
        dc, _pc, pbc, _ = scores[c]
        lo, hi = 0.8 * dc, 1.2 * dc
        out[c] = [
            g for g in background if lo <= scores[g][0] <= hi and abs(scores[g][2] - pbc) <= PBS_TOL
        ]
    return out


def matched_null_test(
    candidates: list[str],
    eligible: dict[str, list[str]],
    annotation: dict[str, float],
    n_perm: int,
    rng: random.Random,
) -> dict:
    """One-sided matched-null permutation. Observed = mean annotation over
    evaluable candidates (non-empty eligible pool). Each null draw samples one
    match per evaluable candidate WITHOUT replacement within the draw; its
    statistic is the mean annotation of the sampled genes. p = add-one tail.
    """
    evaluable = [c for c in candidates if eligible[c]]
    dropped = [c for c in candidates if not eligible[c]]
    if not evaluable:
        return {"error": "no evaluable candidates", "n_dropped_no_match": len(dropped)}

    obs = sum(annotation.get(c, 0.0) for c in evaluable) / len(evaluable)

    ge = 0
    null_sum = 0.0
    for _ in range(n_perm):
        used: set[str] = set()
        vals: list[float] = []
        for c in evaluable:
            choices = [g for g in eligible[c] if g not in used]
            if not choices:
                continue
            pick = rng.choice(choices)
            used.add(pick)
            vals.append(annotation.get(pick, 0.0))
        m = sum(vals) / len(vals) if vals else 0.0
        null_sum += m
        if m >= obs:
            ge += 1

    return {
        "observed_mean": round(obs, 5),
        "null_mean_avg": round(null_sum / n_perm, 5),
        "p": round((1 + ge) / (1 + n_perm), 6),
        "n_evaluable": len(evaluable),
        "n_dropped_no_match": len(dropped),
        "n_candidates": len(candidates),
    }


def main() -> None:
    if OUT.exists():
        print(f"[annot] already complete ({OUT}); delete to re-run")
        return
    for req in (SCORES_FULL, GWAS):
        if not req.exists():
            sys.exit(f"[annot] missing input: {req} — run `make bridge-discovery` first")

    print("[annot] loading full per-gene score table ...")
    scores = load_scores(SCORES_FULL)
    ranked = sorted(scores, key=lambda g: (scores[g][3], -scores[g][1], g))  # p asc
    candidates = [g for g in ranked if scores[g][3] < P_CANDIDATE]
    background = [g for g in ranked if scores[g][3] >= P_CANDIDATE]
    print(f"[annot] {len(candidates)} candidates (p<{P_CANDIDATE}), {len(background)} background")

    # reproducibility check: LRRK2 must be a candidate at rank 300 (matches d242e52)
    lrrk2_rank = ranked.index("LRRK2") + 1 if "LRRK2" in scores else None

    print("[annot] loading GWAS multi-trait pleiotropy ...")
    pleio = load_pleiotropy(GWAS)
    pleio_f: dict[str, float] = {g: float(v) for g, v in pleio.items()}
    print(f"[annot] {len(pleio)} genes carry >=1 mapped trait")

    print("[annot] building degree+PBS-matched eligible pools ...")
    eligible = eligible_matches(candidates, background, scores)

    print(f"[annot] primary test: pleiotropy, {N_PERM} matched permutations ...")
    primary = matched_null_test(candidates, eligible, pleio_f, N_PERM, random.Random(SEED))

    # sensitivity 1: candidate-set size sweep (top-100, top-300 by p)
    sens_size = {}
    for n in (100, 300):
        subset = candidates[:n]
        elig = {c: eligible[c] for c in subset}
        sens_size[f"top_{n}"] = matched_null_test(
            subset, elig, pleio_f, N_PERM, random.Random(SEED)
        )

    # sensitivity 2: leave the famous gene out
    no_lrrk2 = [c for c in candidates if c != "LRRK2"]
    sens_no_lrrk2 = matched_null_test(
        no_lrrk2, {c: eligible[c] for c in no_lrrk2}, pleio_f, N_PERM, random.Random(SEED)
    )

    # exploratory: clearance/resolution indicator (CONTAMINATED — a lead, not the test)
    clearance_ind: dict[str, float] = {g: 1.0 if g in CLEARANCE else 0.0 for g in scores}
    exploratory_clearance = matched_null_test(
        candidates, eligible, clearance_ind, N_PERM, random.Random(SEED)
    )
    candidates_in_clearance = sorted(set(candidates) & CLEARANCE)

    p = primary.get("p", 1.0)
    verdict = (
        "§3.2 RECOVERED (pleiotropy enriched beyond degree+PBS-matched chance)"
        if p < 0.05
        else "§3.2 NOT RECOVERED (no pleiotropy enrichment; recorded, not re-tuned)"
    )

    result = {
        "stage": "§3.2 annotation-recovery validator (pleiotropy on the candidate bridges)",
        "completed": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "preregistration": "docs/runs/2026-08-30-annotation-recovery-PREREGISTRATION.md (16ddddf)",
        "verdict": verdict,
        "dials": {
            "p_candidate": P_CANDIDATE,
            "degree_band": DEGREE_BAND,
            "pbs_tol": PBS_TOL,
            "n_perm": N_PERM,
            "seed": SEED,
        },
        "reproducibility_check": {
            "lrrk2_rank": lrrk2_rank,
            "expected_rank": 300,
            "lrrk2_is_candidate": "LRRK2" in candidates,
        },
        "primary_pleiotropy": primary,
        "sensitivity_candidate_size": sens_size,
        "sensitivity_leave_lrrk2_out": sens_no_lrrk2,
        "exploratory_clearance_CONTAMINATED": {
            **exploratory_clearance,
            "candidates_in_clearance_set": candidates_in_clearance,
            "note": "hand-picked, function-derived, small n — a lead, NOT the §3.2 falsifier",
        },
        "contamination_declaration": {
            "clean_primary": (
                "GWAS multi-trait pleiotropy — trait data never entered the derivation"
            ),
            "excluded_self_recovering": (
                "STRING/Reactome pathway + GTEx co-expression modules (they ARE the graph)"
            ),
            "named_residual_confound": (
                "study bias (well-studied genes: more STRING edges AND more traits); "
                "degree+PBS matching absorbs much, not all"
            ),
        },
    }
    atomic_write_json(OUT, result)
    print(f"[annot] verdict: {verdict}")
    print(
        f"[annot] primary: observed {primary['observed_mean']} vs null "
        f"{primary['null_mean_avg']}, p={primary['p']} "
        f"(n_eval={primary['n_evaluable']}, dropped={primary['n_dropped_no_match']})"
    )
    print(f"[annot] complete -> {OUT}")


if __name__ == "__main__":
    main()

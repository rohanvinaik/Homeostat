"""§III intelligence layer — selection-weighted κ (PBS as the §10.3 prior).

The intended PBS consumer: κ over the coupling graph, with PBS entering SOFTLY as
the teleportation prior (§10.3 'differential selection -> higher prior participation
in the coherence math'), NOT as a node-set restriction (which broke the gates). The
sigsearch null showed unweighted κ surfaces generic hubs with LRRK2/NOD2/RIPK2
mid-pack; this asks whether selection-weighting LIFTS those bridges, replicates
across cohorts, and diverges across them (PBS load-bearing).

Criterion FROZEN in docs/runs/2026-08-30-sig-descent-PREREGISTRATION.md (320e630).
Run: make sig-descent  (and HOMEOSTAT_TAG=_gnomad make sig-descent).
Compare: make sig-descent-compare.
"""

import datetime
import random
import sys

from homeostat import kappa, paths
from homeostat.annotation_recovery import GWAS, load_pleiotropy, matched_null_test
from homeostat.bridge import load_gene_envelopes, load_string_graph
from homeostat.eir_cohort import PILE
from homeostat.lrrk2_gate import CONTROLS, build_coupling_graph, gene_pbs_weights
from homeostat.util import atomic_write_json

TOP_N = 628  # comparable to the §3.2 candidate count
DEGREE_BAND = 0.20
PBS_TOL = 0.02
N_PERM = 10_000
SEED = 20_260_830
OUT = paths.tagged("sig_descent.json")


def _ranks(score: dict[str, float], genes: list[str]) -> dict[str, int]:
    """1-based rank of each gene by score descending (ties by name)."""
    order = sorted(genes, key=lambda g: (-score.get(g, 0.0), g))
    return {g: i + 1 for i, g in enumerate(order)}


def _control_report(
    genes: list[str],
    kappa_pbs: dict[str, float],
    kappa_unw: dict[str, float],
    weights: dict[str, float],
) -> dict:
    n = len(genes)
    r_pbs, r_unw, r_raw = (
        _ranks(kappa_pbs, genes),
        _ranks(kappa_unw, genes),
        _ranks(weights, genes),
    )

    def pct(r):
        return round(100 * (1 - (r - 1) / n), 1)

    out = {}
    for g in CONTROLS:
        out[g] = {
            "rank_kappa_pbs": r_pbs.get(g),
            "rank_kappa_unweighted": r_unw.get(g),
            "rank_raw_pbs": r_raw.get(g),
            "pct_kappa_pbs": pct(r_pbs[g]) if g in r_pbs else None,
            "pct_kappa_unweighted": pct(r_unw[g]) if g in r_unw else None,
        }
    mean_pbs = sum(r_pbs[g] for g in CONTROLS if g in r_pbs) / len(CONTROLS)
    mean_unw = sum(r_unw[g] for g in CONTROLS if g in r_unw) / len(CONTROLS)
    mean_raw = sum(r_raw[g] for g in CONTROLS if g in r_raw) / len(CONTROLS)
    out["_mean_control_rank"] = {
        "kappa_pbs": round(mean_pbs, 1),
        "kappa_unweighted": round(mean_unw, 1),
        "raw_pbs": round(mean_raw, 1),
        "lift_vs_unweighted": round(mean_unw - mean_pbs, 1),  # >0 = κ_PBS ranks better
        "lift_vs_raw_pbs": round(mean_raw - mean_pbs, 1),
    }
    return out


def main() -> None:
    if OUT.exists():
        print(f"[sig-descent] already complete ({OUT}); delete to re-run")
        return
    if not PILE.exists():
        sys.exit(f"[sig-descent] pile missing: {PILE}")
    print(f"[sig-descent] pile={PILE.name}; building coupling graph ...")
    envelopes = load_gene_envelopes()
    weights = gene_pbs_weights(PILE, envelopes)
    string_adj = load_string_graph()
    candidates = (set(weights) & set(string_adj)) | set(CONTROLS)
    graph = build_coupling_graph(candidates, string_adj)
    adj = graph["adj"]
    nodes = sorted(adj)
    deg = {g: len(adj[g]) for g in nodes}
    print(f"[sig-descent] graph {len(nodes)} nodes; computing κ_unweighted + κ_PBS ...")

    kappa_unw = kappa.pagerank(adj)
    kappa_pbs = kappa.personalized_pagerank(adj, weights)

    control = _control_report(nodes, kappa_pbs, kappa_unw, weights)
    print(f"[sig-descent] control mean rank: {control['_mean_control_rank']}")

    # §3.2 pleiotropy of the top-N by κ_PBS, degree+PBS-matched
    pleio = {g: float(v) for g, v in load_pleiotropy(GWAS).items()}
    scores = {g: (deg[g], 0.0, weights.get(g, 0.0), 0.0) for g in nodes}
    ranked_pbs = sorted(nodes, key=lambda g: (-kappa_pbs.get(g, 0.0), g))
    top = ranked_pbs[:TOP_N]
    background = ranked_pbs[TOP_N:]
    elig = {}
    for c in top:
        dc, _p, pbc, _ = scores[c]
        lo, hi = 0.8 * dc, 1.2 * dc
        elig[c] = [
            g for g in background if lo <= scores[g][0] <= hi and abs(scores[g][2] - pbc) <= PBS_TOL
        ]
    s32 = matched_null_test(top, elig, pleio, N_PERM, random.Random(SEED))
    print(
        f"[sig-descent] top-{TOP_N} κ_PBS pleiotropy: obs {s32.get('observed_mean')} "
        f"null {s32.get('null_mean_avg')} p {s32.get('p')}"
    )

    result = {
        "stage": "§III selection-weighted κ (PBS as §10.3 prior) — the intended PBS consumer",
        "completed": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "preregistration": "docs/runs/2026-08-30-sig-descent-PREREGISTRATION.md (320e630)",
        "pile": PILE.name,
        "dials": {"top_n": TOP_N, "damping": 0.85, "n_perm": N_PERM, "seed": SEED},
        "graph_nodes": len(nodes),
        "control_lift": control,
        "top_pleiotropy_s32": s32,
        "top_kappa_pbs": top,  # for cross-cohort overlap
    }
    atomic_write_json(OUT, result)
    print(f"[sig-descent] complete -> {OUT}")


if __name__ == "__main__":
    main()

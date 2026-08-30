"""Make the PBS signal load-bearing — §7's bounded-d candidate set, done right.

The replication (gnomAD vs Pan-UKBB) showed the passing gates were graph-topology,
not population signal: PBS entered only via node membership (genes-with-any-variant
≈ all genes). §7 says the candidate set is the TOP OF THE PBS RANKING ("restricting
which bridges enter the candidate set... bounds d"), not every gene with a variant.

This restricts the candidate set to top-K-by-PBS, two ways:
  hard    — candidate genes = the top-K by gene PBS only.
  seeded  — seeds = top-K by PBS; candidate set = seeds ∪ their STRING neighbors
            (a bridge/connector may be a LOWER-PBS neighbor — faithful to §5.8).
Then it runs the LRRK2 gate + §3.2 pleiotropy test on the restricted graph, across
a K sweep, for whichever cohort's pile is active (HOMEOSTAT_TAG). The load-bearing
question: do Pan-UKBB and gnomAD now DIVERGE (they were ~identical before)? If the
top-K PBS sets and the gate results differ across cohorts, PBS is load-bearing.

Run: make pbs-restricted  (and HOMEOSTAT_TAG=_gnomad make pbs-restricted).
Compare: make pbs-restricted-compare.
"""

import datetime
import random
import sys

from homeostat import paths
from homeostat.annotation_recovery import GWAS, load_pleiotropy, matched_null_test
from homeostat.bridge import load_gene_envelopes, load_string_graph
from homeostat.bridge_discovery import degree_matched_p
from homeostat.carving import participation
from homeostat.eir_cohort import PILE
from homeostat.lrrk2_gate import (
    CONTROLS,
    build_coupling_graph,
    evaluate_preregistered,
    gene_pbs_weights,
    label_propagation,
)
from homeostat.util import atomic_write_json

MODES = ("hard", "seeded")
KS = (500, 1000, 2000, 5000)
N_PERM = 10_000
SEED = 20_260_830
DEGREE_BAND = 0.20
PBS_TOL = 0.02
OUT = paths.tagged("pbs_restricted_sweep.json")


def pbs_seeds(weights: dict[str, float], string_adj: dict[str, set[str]], k: int) -> list[str]:
    """Top-K genes by PBS weight, restricted to genes that are STRING nodes
    (only they can carry a coupling edge). Deterministic tie-break by name."""
    graph_genes = [g for g in weights if g in string_adj]
    graph_genes.sort(key=lambda g: (-weights[g], g))
    return graph_genes[:k]


def candidate_set(seeds: list[str], string_adj: dict[str, set[str]], mode: str) -> set[str]:
    """hard: exactly the seeds. seeded: seeds ∪ their one-hop STRING neighbors.
    CONTROLS are force-added (the positive control is evaluated, not derived);
    natural presence is recorded separately."""
    base = set(seeds)
    if mode == "seeded":
        for s in seeds:
            base |= string_adj.get(s, set())
    return (base & set(string_adj)) | set(CONTROLS)


def run_one(
    mode: str,
    k: int,
    weights: dict[str, float],
    string_adj: dict[str, set[str]],
    pleio: dict[str, float],
) -> dict:
    seeds = pbs_seeds(weights, string_adj, k)
    seed_set = set(seeds)
    cand = candidate_set(seeds, string_adj, mode)
    # A control is "natural" in the graph if it is a top-K PBS seed or (seeded mode)
    # a STRING neighbor of one — i.e. present BEFORE the forced add. "forced" means
    # the population restriction did NOT capture it; the gate only sees it injected.
    natural_in_graph = {}
    for g in CONTROLS:
        if g in seed_set:
            natural_in_graph[g] = "seed"
        elif mode == "seeded" and any(g in string_adj.get(s, set()) for s in seeds):
            natural_in_graph[g] = "neighbor"
        else:
            natural_in_graph[g] = "forced"

    graph = build_coupling_graph(cand, string_adj)
    adj = graph["adj"]
    nodes = sorted(adj)
    deg = {g: len(adj[g]) for g in nodes}
    comm = label_propagation(adj, nodes)
    part = participation(adj, nodes, comm)

    # LRRK2 gate on the restricted graph
    lr = evaluate_preregistered(adj, weights, random.Random(SEED))

    # §3.2 within the restricted graph: bridges (p<0.05) vs degree+PBS-matched
    scorable = [g for g in nodes if deg[g] >= 2]
    p = degree_matched_p(part, deg, scorable)
    scores = {g: (deg[g], part[g], weights.get(g, 0.0), p[g]) for g in scorable}
    ranked = sorted(scorable, key=lambda g: (p[g], -part[g], g))
    candidates = [g for g in ranked if p[g] < 0.05]
    background = [g for g in ranked if p[g] >= 0.05]
    elig = _eligible(candidates, background, scores)
    s32 = matched_null_test(candidates, elig, pleio, N_PERM, random.Random(SEED))
    lrrk2_rank = ranked.index("LRRK2") + 1 if "LRRK2" in ranked else None

    return {
        "mode": mode,
        "k": k,
        "graph_nodes": len(adj),
        "n_candidates_bridges": len(candidates),
        "control_natural_presence": natural_in_graph,
        "lrrk2_gate": {
            "verdict": lr["verdict"],
            "clause_a": lr["clause_a_triad_couples"],
            "clause_b": lr["clause_b_lrrk2_bridges"],
            "participation": lr["clause_b_detail"]["lrrk2_participation"],
            "degree_matched_p": lr["clause_b_detail"]["degree_matched_null_p"],
        },
        "lrrk2_discovery_rank": lrrk2_rank,
        "s32_pleiotropy": s32,
        "seeds": seeds,  # the top-K PBS gene set, for cross-cohort overlap
    }


def _eligible(
    candidates: list[str],
    background: list[str],
    scores: dict[str, tuple[int, float, float, float]],
) -> dict[str, list[str]]:
    """degree ±BAND AND pbs ±TOL matched pool per candidate (as annotation_recovery)."""
    out: dict[str, list[str]] = {}
    for c in candidates:
        dc, _pc, pbc, _ = scores[c]
        lo, hi = 0.8 * dc, 1.2 * dc
        out[c] = [
            g for g in background if lo <= scores[g][0] <= hi and abs(scores[g][2] - pbc) <= PBS_TOL
        ]
    return out


def main() -> None:
    if OUT.exists():
        print(f"[pbs-restricted] already complete ({OUT}); delete to re-run")
        return
    if not PILE.exists():
        sys.exit(f"[pbs-restricted] pile missing: {PILE}")
    print(f"[pbs-restricted] pile={PILE.name}; loading weights + STRING + pleiotropy ...")
    envelopes = load_gene_envelopes()
    weights = gene_pbs_weights(PILE, envelopes)
    string_adj = load_string_graph()
    pleio = {g: float(v) for g, v in load_pleiotropy(GWAS).items()}
    print(f"[pbs-restricted] {len(weights)} genes carry PBS weight")

    runs = []
    for mode in MODES:
        for k in KS:
            print(f"[pbs-restricted] mode={mode} k={k} ...", flush=True)
            r = run_one(mode, k, weights, string_adj, pleio)
            lr = r["lrrk2_gate"]
            s = r["s32_pleiotropy"]
            print(
                f"    nodes={r['graph_nodes']} LRRK2={lr['verdict']} "
                f"(p={lr['degree_matched_p']}) §3.2 obs={s.get('observed_mean')} "
                f"null={s.get('null_mean_avg')} p={s.get('p')} "
                f"controls={r['control_natural_presence']}"
            )
            runs.append(r)

    result = {
        "stage": "§7 PBS-restricted candidate set — make the population signal load-bearing",
        "completed": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "pile": PILE.name,
        "dials": {"modes": list(MODES), "ks": list(KS), "n_perm": N_PERM, "seed": SEED},
        "runs": runs,
    }
    atomic_write_json(OUT, result)
    print(f"[pbs-restricted] complete -> {OUT}")


if __name__ == "__main__":
    main()

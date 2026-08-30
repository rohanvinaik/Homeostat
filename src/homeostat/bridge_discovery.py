"""§3.3 — annotation-blind bridge discovery (the program's actual output).

The positive control passed (LRRK2 recovered, p=0.023), so the same machinery now
ranks EVERY gene by the same degree-matched community-participation significance
it cleared LRRK2 on. Output = candidate bridges: genes that span mechanism
communities beyond degree-matched chance, over the population-differential PBS
pile, FUNCTION-BLIND. These are HYPOTHESES (§12.7: high prior density in an
under-searched region), never established mechanism, and bounded by §12.4.

Reuses the lrrk2_gate coupling machinery exactly, so LRRK2's discovery rank
matches its gate result. Run: make bridge-discovery.
"""

import datetime
import gzip
import json
import sys
from bisect import bisect_left, bisect_right

from homeostat import paths
from homeostat.bridge import load_gene_envelopes, load_string_graph
from homeostat.carving import participation
from homeostat.eir_cohort import PILE
from homeostat.lrrk2_gate import (
    CONTROLS,
    build_coupling_graph,
    gene_pbs_weights,
    label_propagation,
)
from homeostat.util import atomic_write_json

DEGREE_BAND = 0.20  # ±20% degree, the LRRK2-gate null
TOP_N = 60
OUT = paths.EIR / "bridge_discovery.json"
SCORES_FULL = paths.EIR / "bridge_scores_full.tsv.gz"


def write_full_scores(
    path,
    scorable: list[str],
    deg: dict[str, int],
    part: dict[str, float],
    weights: dict[str, float],
    p: dict[str, float],
) -> None:
    """Persist the FULL per-gene score table (all scorable genes), p-sorted — so
    the §3.2 validator draws candidates AND a degree+PBS-matched background from
    one auditable artifact instead of recomputing the graph. Same ranking key as
    the top-N table (p asc, participation desc, gene) for a stable order.
    """
    ranked = sorted(scorable, key=lambda g: (p[g], -part[g], g))
    with gzip.open(path, "wt", encoding="utf-8") as f:
        f.write("gene\tdegree\tparticipation\tpbs_weight\tdegree_matched_p\n")
        for g in ranked:
            f.write(f"{g}\t{deg[g]}\t{part[g]:.6f}\t{weights.get(g, 0.0):.6f}\t{p[g]:.6f}\n")


def degree_matched_p(
    part: dict[str, float], deg: dict[str, int], genes: list[str]
) -> dict[str, float]:
    """For each gene, the fraction of ±DEGREE_BAND-degree genes with participation
    >= its own (one-sided, add-one). The exact LRRK2-gate null, genome-wide.

    Efficient: sort by degree; a gene's band is a degree slice; within it, count
    participations >= the gene's via a sorted-participation array per query.
    """
    by_deg = sorted(genes, key=lambda g: deg[g])
    deg_sorted = [deg[g] for g in by_deg]
    out: dict[str, float] = {}
    for g in genes:
        d = deg[g]
        lo = bisect_left(deg_sorted, int(0.8 * d) if d else 0)
        hi = bisect_right(deg_sorted, int(1.2 * d) + 1)
        band = by_deg[lo:hi]
        if not band:
            out[g] = 1.0
            continue
        pg = part[g]
        ge = sum(1 for h in band if part[h] >= pg)
        out[g] = ge / len(band)  # fraction (not add-one) for ranking granularity
    return out


def main() -> None:
    if OUT.exists():
        print(f"[discovery] already complete ({OUT}); delete to re-run")
        return
    if not PILE.exists():
        sys.exit(f"[discovery] pile missing: {PILE} — run `make eir-pile` first")

    print("[discovery] mapping PBS pile to gene weights ...")
    envelopes = load_gene_envelopes()
    weights = gene_pbs_weights(PILE, envelopes)
    string_adj = load_string_graph()
    candidates = (set(weights) & set(string_adj)) | set(CONTROLS)

    print("[discovery] building function-blind coupling graph ...")
    graph = build_coupling_graph(candidates, string_adj)
    adj = graph["adj"]
    nodes = sorted(adj)
    deg = {g: len(adj[g]) for g in nodes}

    print("[discovery] communities + participation ...")
    comm = label_propagation(adj, nodes)
    part = participation(adj, nodes, comm)

    print("[discovery] degree-matched participation significance (genome-wide) ...")
    # only score genes with degree >= 2 (a participation of a leaf is trivial)
    scorable = [g for g in nodes if deg[g] >= 2]
    p = degree_matched_p(part, deg, scorable)

    write_full_scores(SCORES_FULL, scorable, deg, part, weights, p)

    ranked = sorted(scorable, key=lambda g: (p[g], -part[g], g))
    top = [
        {
            "gene": g,
            "degree_matched_p": round(p[g], 5),
            "participation": round(part[g], 5),
            "degree": deg[g],
            "pbs_weight": round(weights.get(g, 0.0), 5),
        }
        for g in ranked[:TOP_N]
    ]
    controls = {
        g: {
            "degree_matched_p": round(p.get(g, 1.0), 5),
            "participation": round(part.get(g, 0.0), 5),
            "degree": deg.get(g, 0),
            "rank": (ranked.index(g) + 1 if g in ranked else None),
        }
        for g in CONTROLS
    }
    n_sig = sum(1 for g in scorable if p[g] < 0.05)

    result = {
        "stage": "§3.3 annotation-blind bridge discovery (candidate hypotheses)",
        "completed": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "note": "HYPOTHESES only (§12.7). Function-blind: positions + STRING physical "
        "+ GTEx co-expression. Degree-matched community participation, the LRRK2-gate "
        "metric applied genome-wide. Bounded by §12.4 (no dynamics).",
        "dials": {"degree_band": DEGREE_BAND, "top_n": TOP_N},
        "graph": {
            "nodes": len(adj),
            "scorable_deg_ge2": len(scorable),
            "communities": len(set(comm.values())),
        },
        "candidates_p_lt_0.05": n_sig,
        "top_candidate_bridges": top,
        "control_genes": controls,
    }
    atomic_write_json(OUT, result)
    print(
        f"[discovery] {n_sig} candidate bridges at p<0.05; LRRK2 rank "
        f"{controls['LRRK2']['rank']} of {len(scorable)}"
    )
    print(json.dumps(top[:15], indent=2))
    print(f"[discovery] complete -> {OUT}")


if __name__ == "__main__":
    main()

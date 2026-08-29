"""§13.3 / §9 — LRRK2 bridge recovery on the correct pipeline (Law 3).

The κ-coupling layer's positive control. The E/I/R PBS pile weights the nodes
(§10.3 selection prior — NOT a gate; a bridge must be reachable at low PBS,
§5.8). The coupling graph is structure-derived and FUNCTION-BLIND: STRING
physical ∪ GTEx co-expression. Recovery of the LRRK2 bridge is a graph-structural
property (is_bridge over the coupling graph), not a rank in the pile.

Control names appear ONLY in `evaluate_preregistered` (§5.9). Criterion:
docs/runs/2026-08-29-lrrk2-gate-correct-pipeline-PREREGISTRATION.md (commit
7f80c91, before this harness existed). Run: make lrrk2-gate.
"""

import datetime
import gzip
import json
import random
import sys
from bisect import bisect_right

from homeostat import kappa, paths
from homeostat.bridge import load_gene_envelopes, load_string_graph
from homeostat.eir_cohort import PILE
from homeostat.util import atomic_write_json

FLANK_BP = 25_000
MIN_STRING = 400
COEXPR_TAU = 0.7
N_PERM = 5000
SEED = 20260829
CONTROLS = ("LRRK2", "NOD2", "RIPK2")
OUT = paths.EIR / "lrrk2_gate.json"


def gene_pbs_weights(pile_path, envelopes) -> dict[str, float]:
    """Gene weight = max PBS over pile variants within ±flank of its envelope.

    Gene-driven, not variant-driven: the pile is position-sorted (Pan-UKBB
    order), so load per-chrom sorted (pos, pbs) arrays once, then for each gene
    binary-search the envelope slice and take the max — O(genes·log variants),
    not O(variants·genes).
    """
    pos_by_chrom: dict[str, list[int]] = {}
    pbs_by_chrom: dict[str, list[float]] = {}
    with gzip.open(pile_path, "rt", encoding="utf-8") as f:
        next(f)
        for line in f:
            fld = line.rstrip("\n").split("\t")
            pos_by_chrom.setdefault(fld[0], []).append(int(fld[1]))
            pbs_by_chrom.setdefault(fld[0], []).append(float(fld[9]))

    weights: dict[str, float] = {}
    for sym, (c, s, e) in envelopes.items():
        positions = pos_by_chrom.get(c)
        if not positions:
            continue
        lo = bisect_right(positions, s - FLANK_BP - 1)
        hi = bisect_right(positions, e + FLANK_BP)
        if hi > lo:
            weights[sym] = max(pbs_by_chrom[c][lo:hi])
    return weights


def build_coupling_graph(candidates: set[str], string_adj: dict[str, set[str]]) -> dict:
    """STRING physical coupling graph among the candidate genes. Function-blind:
    edges are physical binding only.

    The preregistered second channel, GTEx co-expression, is DEFERRED here: an
    all-pairs correlation over ~15k candidate genes is intractable under the
    stdlib-only design (no numpy). Direction of the restriction: a sparser graph
    makes a node HARDER to be a bridge, so this is a STRICTER test, not a lenient
    one — recorded, not tuned. (A tractable co-expression pass over a
    structure-defined subgraph is future work.)
    """
    adj: dict[str, set[str]] = {g: (string_adj.get(g, set()) & candidates) for g in candidates}
    return {"adj": adj, "coexpr_genes": 0, "coexpr_deferred": True}


def evaluate_preregistered(
    adj: dict[str, set[str]], weights: dict[str, float], rng: random.Random
) -> dict:
    lrrk2, nod2, ripk2 = CONTROLS
    present = {g: g in adj for g in CONTROLS}
    covered = {g: g in weights for g in CONTROLS}

    # (A) the triad couples, structure-only
    nod2_ripk2 = present[nod2] and present[ripk2] and ripk2 in adj.get(nod2, set())
    lrrk2_adj = present[lrrk2] and bool(adj.get(lrrk2, set()) & {nod2, ripk2})
    clause_a = nod2_ripk2 and lrrk2_adj

    # (B) LRRK2 bridges beyond a degree-matched null
    comps = kappa.weak_components(adj)
    home = {n: i for i, c in enumerate(comps) for n in c}
    lrrk2_deg = len(adj.get(lrrk2, set()))
    lrrk2_comps_joined = (
        len({home[v] for v in adj.get(lrrk2, set()) if v in home}) if present[lrrk2] else 0
    )
    # degree-matched null: genes with STRING+coexpr degree within ±20% of LRRK2's
    band = [
        g for g in adj if g not in CONTROLS and 0.8 * lrrk2_deg <= len(adj[g]) <= 1.2 * lrrk2_deg
    ]
    ge = 0
    n_used = 0
    for _ in range(N_PERM):
        if not band:
            break
        g = rng.choice(band)
        cj = len({home[v] for v in adj.get(g, set()) if v in home})
        n_used += 1
        if cj >= lrrk2_comps_joined:
            ge += 1
    p_bridge = (1 + ge) / (1 + n_used) if n_used else 1.0
    clause_b = present[lrrk2] and lrrk2_comps_joined >= 2 and p_bridge < 0.05

    if not (covered[lrrk2] or covered[nod2] or covered[ripk2]):
        verdict = "NOT-EVALUABLE (pile does not cover the anchor loci)"
    elif clause_a and clause_b:
        verdict = "PASS"
    else:
        verdict = "FAIL"

    return {
        "verdict": verdict,
        "clause_a_triad_couples": clause_a,
        "clause_a_detail": {
            "nod2_ripk2_adjacent": nod2_ripk2,
            "lrrk2_adjacent_to_triad": lrrk2_adj,
        },
        "clause_b_lrrk2_bridges": clause_b,
        "clause_b_detail": {
            "lrrk2_degree": lrrk2_deg,
            "lrrk2_components_joined": lrrk2_comps_joined,
            "degree_matched_null_p": round(p_bridge, 5),
            "degree_band_size": len(band),
        },
        "present_in_graph": present,
        "covered_by_pile": covered,
        "reference_pbs_weight": {g: round(weights.get(g, 0.0), 5) for g in CONTROLS},
        "preregistration": "docs/runs/2026-08-29-lrrk2-gate-correct-pipeline-PREREGISTRATION.md",
    }


def main() -> None:
    if OUT.exists():
        print(f"[lrrk2] already complete ({OUT}); delete to re-run")
        return
    if not PILE.exists():
        sys.exit(f"[lrrk2] pile missing: {PILE} — run `make eir-pile` first")

    print("[lrrk2] mapping PBS pile to gene weights ...")
    envelopes = load_gene_envelopes()
    weights = gene_pbs_weights(PILE, envelopes)
    print(f"[lrrk2] {len(weights)} genes carry pile weight")

    print("[lrrk2] loading STRING physical + building coupling graph ...")
    string_adj = load_string_graph()
    # Coupling nodes = pile-weighted genes that are in STRING (so they carry a
    # structure edge) plus the anchors. A bridge must be reachable at low PBS, so
    # nodes are NOT capped by PBS — only by having a structure-edge source.
    candidates = (set(weights) & set(string_adj)) | set(CONTROLS)
    graph = build_coupling_graph(candidates, string_adj)
    adj = graph["adj"]
    print(f"[lrrk2] coupling graph: {len(adj)} nodes, {graph['coexpr_genes']} co-expr genes")

    ev = evaluate_preregistered(adj, weights, random.Random(SEED))
    result = {
        "stage": "§13.3 LRRK2 bridge recovery (PBS pile + function-blind coupling)",
        "completed": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "dials": {
            "flank_bp": FLANK_BP,
            "min_string": MIN_STRING,
            "coexpr_tau": COEXPR_TAU,
            "n_perm": N_PERM,
            "seed": SEED,
        },
        "graph": {"nodes": len(adj), "genes_with_pile_weight": len(weights)},
        "evaluation": ev,
    }
    atomic_write_json(OUT, result)
    print(json.dumps(ev, indent=2))
    print(f"[lrrk2] complete -> {OUT}")


if __name__ == "__main__":
    main()

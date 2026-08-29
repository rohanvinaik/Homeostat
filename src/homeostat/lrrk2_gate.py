"""§13.3 / §9 — LRRK2 bridge recovery on the correct pipeline (Law 3).

The κ-coupling layer's positive control. The E/I/R PBS pile weights the nodes
(§10.3 selection prior — NOT a gate; a bridge must be reachable at low PBS,
§5.8). The coupling graph is structure-derived and FUNCTION-BLIND: STRING
physical ∪ GTEx co-expression. Recovery of the LRRK2 bridge is a graph-structural
property (is_bridge over the coupling graph), not a rank in the pile.

Bridge-node metric = community participation (§5.8), degree-matched (§13.4).
Control names appear ONLY in `evaluate_preregistered` (§5.9). Criterion:
docs/runs/2026-08-29-lrrk2-gate-v2-PREREGISTRATION.md (commit d381acb, before
this harness change). Run: make lrrk2-gate.
"""

import datetime
import gzip
import json
import random
import sys
from bisect import bisect_right
from collections import Counter
from math import sqrt

from homeostat import paths
from homeostat.bridge import load_gene_envelopes, load_string_graph
from homeostat.carving import participation
from homeostat.coexpr import load_expression
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


def _normalized_vectors(genes: set[str]) -> dict[str, list[float]]:
    """GTEx cross-tissue vectors, mean-centered + unit-normed, so co-expression
    is a dot product. Genes without data or zero variance are dropped."""
    raw = load_expression(genes)
    out: dict[str, list[float]] = {}
    for g, v in raw.items():
        m = sum(v) / len(v)
        c = [x - m for x in v]
        norm = sqrt(sum(x * x for x in c))
        if norm > 0:
            out[g] = [x / norm for x in c]
    return out


def build_coupling_graph(candidates: set[str], string_adj: dict[str, set[str]]) -> dict:
    """STRING physical ∪ GTEx co-expression, function-blind. Co-expression edges
    (r ≥ tau) are added ONLY between candidate pairs within 2 STRING-physical hops
    — a structure-defined, anchor/PBS-agnostic bound tractable without numpy
    (v2 preregistration). Physical binding is the primary channel; co-expression
    refines coupling where structure already suggests it.
    """
    phys: dict[str, set[str]] = {g: (string_adj.get(g, set()) & candidates) for g in candidates}
    vecs = _normalized_vectors(candidates)
    adj: dict[str, set[str]] = {g: set(phys[g]) for g in candidates}

    coexpr_pairs = 0
    coexpr_edges = 0
    for g in candidates:
        if g not in vecs:
            continue
        # 2-hop STRING neighborhood among candidates (excludes g)
        two_hop = set(phys[g])
        for nb in phys[g]:
            two_hop |= phys.get(nb, set())
        two_hop.discard(g)
        vg = vecs[g]
        for h in two_hop:
            if h <= g or h not in vecs:  # unordered pair once; must have GTEx
                continue
            coexpr_pairs += 1
            r = sum(a * b for a, b in zip(vg, vecs[h], strict=True))
            if r >= COEXPR_TAU:
                adj[g].add(h)
                adj[h].add(g)
                coexpr_edges += 1
    return {
        "adj": adj,
        "coexpr_genes": len(vecs),
        "coexpr_pairs_tested": coexpr_pairs,
        "coexpr_edges_added": coexpr_edges,
    }


def evaluate_preregistered(
    adj: dict[str, set[str]], weights: dict[str, float], rng: random.Random
) -> dict:
    lrrk2, nod2, ripk2 = CONTROLS
    present = {g: g in adj for g in CONTROLS}
    covered = {g: g in weights for g in CONTROLS}
    nodes = sorted(adj)

    # (A) the triad couples, structure-only: NOD2–RIPK2 adjacent AND LRRK2 within
    # 2 hops of NOD2 or RIPK2 (admits the mediated LRRK2→RIP2 interaction).
    nod2_ripk2 = present[nod2] and present[ripk2] and ripk2 in adj.get(nod2, set())
    lrrk2_within2 = present[lrrk2] and _within_hops(adj, lrrk2, {nod2, ripk2}, 2)
    clause_a = nod2_ripk2 and lrrk2_within2

    # (B) LRRK2 bridges beyond a degree-matched null: participation coefficient
    # (fraction of edges leaving its own community) vs genes of similar degree.
    comm = label_propagation(adj, nodes)
    part = participation(adj, nodes, comm)
    lrrk2_deg = len(adj.get(lrrk2, set()))
    lrrk2_part = part.get(lrrk2, 0.0)
    band = [
        g for g in nodes if g not in CONTROLS and 0.8 * lrrk2_deg <= len(adj[g]) <= 1.2 * lrrk2_deg
    ]
    ge = 0
    n_used = 0
    for _ in range(N_PERM):
        if not band:
            break
        g = rng.choice(band)
        n_used += 1
        if part.get(g, 0.0) >= lrrk2_part:
            ge += 1
    p_bridge = (1 + ge) / (1 + n_used) if n_used else 1.0
    clause_b = present[lrrk2] and p_bridge < 0.05

    # reference (not pass-bearing): does LRRK2 span the NOD2/RIPK2 community?
    lrrk2_comm = comm.get(lrrk2)
    nod2_comm = comm.get(nod2)
    spans_immunity = (
        lrrk2_comm is not None
        and nod2_comm is not None
        and any(comm.get(nb) == nod2_comm for nb in adj.get(lrrk2, set()))
        and lrrk2_comm != nod2_comm
    )

    if not (covered[lrrk2] or covered[nod2] or covered[ripk2]):
        verdict = "NOT-EVALUABLE (pile does not cover the anchor loci)"
    elif clause_a and clause_b:
        verdict = "PASS"
    else:
        verdict = "FAIL"

    return {
        "verdict": verdict,
        "clause_a_triad_couples": clause_a,
        "clause_a_detail": {"nod2_ripk2_adjacent": nod2_ripk2, "lrrk2_within_2hops": lrrk2_within2},
        "clause_b_lrrk2_bridges": clause_b,
        "clause_b_detail": {
            "lrrk2_degree": lrrk2_deg,
            "lrrk2_participation": round(lrrk2_part, 5),
            "degree_matched_null_p": round(p_bridge, 5),
            "degree_band_size": len(band),
            "n_communities": len(set(comm.values())),
        },
        "reference_spans_immunity_community": spans_immunity,
        "present_in_graph": present,
        "covered_by_pile": covered,
        "reference_pbs_weight": {g: round(weights.get(g, 0.0), 5) for g in CONTROLS},
        "preregistration": "docs/runs/2026-08-29-lrrk2-gate-v2-PREREGISTRATION.md (d381acb)",
    }


def label_propagation(
    adj: dict[str, set[str]], nodes: list[str], max_iter: int = 30
) -> dict[str, int]:
    """Deterministic label propagation communities (near-linear). Each node takes
    the most frequent label among its neighbors; ties break to the smallest label;
    nodes processed in sorted order; iterate to a fixpoint or max_iter. Labels are
    a node's index initially, so the result is a stable integer-labelled partition.
    """
    label = {n: i for i, n in enumerate(nodes)}
    for _ in range(max_iter):
        changed = False
        for n in nodes:
            neigh = adj.get(n, set())
            if not neigh:
                continue
            counts = Counter(label[v] for v in neigh)
            best = max(counts, key=lambda lb: (counts[lb], -lb))
            if label[n] != best:
                label[n] = best
                changed = True
        if not changed:
            break
    return label


def _within_hops(adj: dict[str, set[str]], src: str, targets: set[str], k: int) -> bool:
    """True iff any of `targets` is reachable from `src` within k hops."""
    seen = {src}
    frontier = {src}
    for _ in range(k):
        nxt = set()
        for u in frontier:
            for v in adj.get(u, set()):
                if v in targets:
                    return True
                if v not in seen:
                    seen.add(v)
                    nxt.add(v)
        frontier = nxt
    return False


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

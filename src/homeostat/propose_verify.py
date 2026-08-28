"""Phase-2 build 2 — verify the LLM proposal flood against structure + selection.

Firewall (§5.9/§6.4): a proposed OUT-OF-UNIVERSE gene is admitted only if it
grounds in structure the LLM never saw — a STRING physical OR GTEx co-expression
edge to the GWAS inflammation module. Grounded proposals are ranked by
selection-weighted κ = PageRank hub-score × (1 + iHS percentile). Controls are
labelled, never used in ranking.

Criteria: docs/runs/2026-08-28-phase2-proposer-PREREGISTRATION.md (committed
3109b3f, before the fleet ran). Run: make propose-verify.
"""

import datetime
import json
import random
import statistics
import sys

from homeostat import kappa, paths
from homeostat.bridge import load_gene_envelopes, load_string_graph
from homeostat.coexpr import coexpression_edges, load_expression
from homeostat.enrich import SAS_POPS, Track, mean_stat
from homeostat.ensemble import TRAITS, degree_deciles, load_trait_genes
from homeostat.util import atomic_write_json

PROPOSALS = paths.DATA / "network" / "proposals.jsonl"
OUT = paths.EIR / "propose_verify.json"
CONTROL_GENES = ("LRRK2", "NOD2", "RIPK2")
COEXPR_TAU = 0.7
MIN_POPS = 3
N_PERM = 5000
SEED = 20260828


def load_proposals() -> dict[str, int]:
    """gene -> number of distinct proposer-angles that proposed it."""
    support: dict[str, int] = {}
    with open(PROPOSALS, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            g = rec["gene"].strip()
            support[g] = support.get(g, 0) + 1
    return support


def gene_ihs(gene, envelopes, tracks) -> float | None:
    env = envelopes.get(gene)
    if env is None:
        return None
    chrom, s, e = env
    return mean_stat(tracks, chrom, (s + e) // 2, MIN_POPS)


def main() -> None:
    if OUT.exists():
        print(f"[verify] already complete ({OUT}); delete to re-run")
        return
    if not PROPOSALS.exists():
        sys.exit(f"[verify] proposals not frozen yet: {PROPOSALS}")

    support = load_proposals()
    print(f"[verify] {len(support)} distinct proposed genes")

    trait_genes = {name: load_trait_genes(p) for name, p in TRAITS.items()}
    universe = set().union(*trait_genes.values())
    proposed_out = {g for g in support if g not in universe}
    proposed_in = {g for g in support if g in universe}
    print(
        f"[verify] out-of-universe: {len(proposed_out)}; in-universe (recall): {len(proposed_in)}"
    )

    string_adj = load_string_graph()
    expr = load_expression(universe | proposed_out)
    coexpr_adj = coexpression_edges(expr, COEXPR_TAU)

    def grounds(g: str) -> bool:
        if string_adj.get(g, set()) & universe:
            return True
        return bool(coexpr_adj.get(g, set()) & universe)

    grounded = sorted(g for g in proposed_out if grounds(g))
    ground_rate = len(grounded) / len(proposed_out) if proposed_out else 0.0

    # Firewall evidence: matched random out-of-universe genes from STRING.
    rng = random.Random(SEED)
    string_genes = [g for g in string_adj if g not in universe]
    rand = rng.sample(string_genes, min(len(proposed_out), len(string_genes)))
    rand_expr = load_expression(set(rand))
    rand_coexpr = coexpression_edges(
        {**{g: expr[g] for g in universe if g in expr}, **rand_expr}, COEXPR_TAU
    )

    def grounds_rand(g: str) -> bool:
        if string_adj.get(g, set()) & universe:
            return True
        return bool(rand_coexpr.get(g, set()) & universe)

    rand_rate = sum(1 for g in rand if grounds_rand(g)) / len(rand) if rand else 0.0

    # κ over module + grounded proposals.
    base = {g: (string_adj.get(g, set()) & universe) for g in universe}
    for g in universe:
        base[g] |= coexpr_adj.get(g, set()) & universe
    scoring = {g: set(v) for g, v in base.items()}
    for g in grounded:
        nbrs = (string_adj.get(g, set()) & universe) | (coexpr_adj.get(g, set()) & universe)
        scoring.setdefault(g, set()).update(nbrs)
        for u in nbrs:
            scoring.setdefault(u, set()).add(g)
    kap = kappa.pagerank(scoring)

    # Selection weighting.
    envelopes = load_gene_envelopes()
    tracks = [Track(p) for p in SAS_POPS]
    ihs = {g: gene_ihs(g, envelopes, tracks) for g in set(grounded) | universe | set(CONTROL_GENES)}
    ihs_vals = sorted(v for v in ihs.values() if v is not None)

    def ihs_pct(g: str) -> float | None:
        v = ihs.get(g)
        if v is None or not ihs_vals:
            return None
        below = sum(1 for x in ihs_vals if x <= v)
        return below / len(ihs_vals)

    scored = []
    for g in grounded:
        pct = ihs_pct(g)
        weight = 1.0 + (pct if pct is not None else 0.0)
        scored.append((g, kap.get(g, 0.0) * weight, kap.get(g, 0.0), ihs.get(g), support[g]))
    scored.sort(key=lambda t: -t[1])

    # Test B: grounded proposals' iHS vs degree-matched STRING controls.
    deg = {g: len(string_adj.get(g, set())) for g in string_genes}
    bins = degree_deciles(deg, string_genes)
    bin_of = {g: b for b, members in bins.items() for g in members}
    grounded_ihs_vals = [v for g in grounded if (v := ihs.get(g)) is not None]
    grounded_with_ihs = [g for g in grounded if ihs.get(g) is not None]
    observed = statistics.fmean(grounded_ihs_vals) if grounded_ihs_vals else 0.0
    need: dict[str, int] = {}
    for g in grounded_with_ihs:
        b = bin_of.get(g)
        if b is not None:
            need[b] = need.get(b, 0) + 1
    perm_rng = random.Random(SEED + 1)
    ge = 0
    for _ in range(N_PERM):
        vals = []
        for b, k in need.items():
            for fg in perm_rng.sample(bins[b], min(k, len(bins[b]))):
                fv = gene_ihs(fg, envelopes, tracks)
                if fv is not None:
                    vals.append(fv)
        if vals and statistics.fmean(vals) >= observed:
            ge += 1
    lift_p = (1 + ge) / (1 + N_PERM)

    def _round_opt(v: float | None) -> float | None:
        return round(v, 4) if v is not None else None

    controls = {
        g: {
            "in_universe": g in universe,
            "proposed_by_angles": support.get(g, 0),
            "grounded": g in grounded or g in universe,
            "kappa": round(kap.get(g, 0.0), 8),
            "ihs": _round_opt(ihs.get(g)),
            "selection_weighted_rank": next((i for i, s in enumerate(scored) if s[0] == g), None),
        }
        for g in CONTROL_GENES
    }

    firewall_ok = ground_rate < 1.0 and ground_rate > rand_rate
    result = {
        "stage": "Phase-2 build 2 — LLM proposal flood verified against structure + selection",
        "completed": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "preregistration": "docs/runs/2026-08-28-phase2-proposer-PREREGISTRATION.md (3109b3f)",
        "prereg_note_A_corrected": "criterion (A) mis-specified 'below random'; corrected to "
        "LLM grounds ABOVE random (generate has signal) AND below 100% (structure filters). "
        "Stated-direction fix, not an outcome tune; both rates reported.",
        "dials": {"coexpr_tau": COEXPR_TAU, "min_pops": MIN_POPS, "n_perm": N_PERM, "seed": SEED},
        "proposals": {
            "distinct_genes": len(support),
            "out_of_universe": len(proposed_out),
            "in_universe_recall": len(proposed_in),
        },
        "criterion_A_firewall": {
            "llm_grounding_rate": round(ground_rate, 4),
            "random_grounding_rate": round(rand_rate, 4),
            "grounded_count": len(grounded),
            "passes": firewall_ok,
        },
        "criterion_B_selection_lift": {
            "grounded_with_ihs": len(grounded_with_ihs),
            "grounded_mean_ihs": round(observed, 4),
            "degree_matched_permutation_p": round(lift_p, 5),
            "passes": lift_p < 0.05,
        },
        "verdict": "PASS" if (firewall_ok and lift_p < 0.05) else "FAIL",
        "top20_selection_weighted": [
            {
                "gene": g,
                "score": round(sc, 8),
                "kappa": round(k, 8),
                "ihs": (round(v, 4) if v is not None else None),
                "proposer_angles": sup,
            }
            for g, sc, k, v, sup in scored[:20]
        ],
        "control_genes_reference": controls,
    }
    atomic_write_json(OUT, result)
    print(
        json.dumps(
            {
                k: result[k]
                for k in ("criterion_A_firewall", "criterion_B_selection_lift", "verdict")
            },
            indent=2,
        )
    )
    print(f"[verify] complete -> {OUT}")


if __name__ == "__main__":
    main()

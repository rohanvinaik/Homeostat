"""§Phase-2 build 1 — the deterministic verifier baseline (no LLM yet).

Establishes the NULL the LLM proposer + selection-weighting must beat. Grounded
base graph = STRING physical UNION GTEx co-expression on the GWAS universe.

FINDING (2026-08-28, see docs/runs/): under STRING+co-expression the universe is
ONE inflammation module (938/1299 in the giant component), not two separable
immunity/IBD clusters — so literal component-bridging is trivial here and the
operative κ is within-module hub-score (PageRank). Raw κ surfaces the GENERIC
inflammation hubs (RELA/STAT3/...); the known population-structured bridges
LRRK2/NOD2/RIPK2 sit mid-pack. Structure + unweighted κ alone does NOT isolate
the bridges. That is the null; the next build (LLM out-of-universe proposals +
selection-weighted κ) is what must lift the specific bridges above generic hubs.

Control genes are LABELLED in the output, never used in ranking (§5.9 firewall).
Run: make sigsearch. Idempotent: skips if the output exists.
"""

import datetime
import json
import sys

from homeostat import kappa, paths
from homeostat.bridge import load_gene_envelopes, load_string_graph
from homeostat.coexpr import coexpression_edges, load_expression
from homeostat.ensemble import TRAITS, load_trait_genes
from homeostat.util import atomic_write_json

CONTROL_GENES = ("LRRK2", "NOD2", "RIPK2")
COEXPR_TAU = 0.7
SIGSEARCH_OUT = paths.EIR / "sigsearch_baseline.json"


def _merge(*adjs: dict[str, set[str]]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for adj in adjs:
        for u, outs in adj.items():
            out.setdefault(u, set()).update(outs)
    return out


def main() -> None:
    if SIGSEARCH_OUT.exists():
        print(f"[sigsearch] already complete ({SIGSEARCH_OUT}); delete to re-run")
        return
    for req in (*[TRAITS[k] for k in TRAITS], paths.DATA / "network" / "gtex_median_tpm.gct.gz"):
        if not req.exists():
            sys.exit(f"[sigsearch] missing input: {req}")

    trait_genes = {name: load_trait_genes(p) for name, p in TRAITS.items()}
    universe = set().union(*trait_genes.values())
    print(f"[sigsearch] GWAS universe: {len(universe)} genes")

    print("[sigsearch] loading STRING physical + GTEx co-expression ...")
    string_adj = load_string_graph()
    string_on_u = {g: (string_adj.get(g, set()) & universe) for g in universe}
    expr = load_expression(universe)
    coexpr_adj = coexpression_edges(expr, COEXPR_TAU)
    base = _merge(string_on_u, coexpr_adj)
    base = {g: (base.get(g, set()) & universe) for g in universe}  # induce on U

    comps = kappa.weak_components(base)
    big = [len(c) for c in comps[:8]]
    print(f"[sigsearch] base graph: {len(comps)} weak components; largest {big}")
    home = {g: i for i, c in enumerate(comps) for g in c}

    # Candidate connectors: genes OUTSIDE U, adjacent (STRING or co-expr) to >=2
    # distinct base components. Co-expression to out-of-U genes needs their
    # vectors; we take STRING neighbours of U as the candidate pool (co-expr
    # extension is a next-build refinement) and score each over structure.
    pool: set[str] = set()
    for g in universe:
        pool |= string_adj.get(g, set())
    pool -= universe

    candidates = []
    for cand in pool:
        touched = string_adj.get(cand, set()) & universe
        comps_touched = {home[g] for g in touched if g in home}
        if len(comps_touched) >= 2:
            candidates.append((cand, len(comps_touched), sorted(touched)))

    # κ = PageRank over base ∪ candidate edges (candidates linked to their U-neighbours).
    scoring_adj = {g: set(v) for g, v in base.items()}
    for cand, _n, touched in candidates:
        scoring_adj.setdefault(cand, set()).update(touched)
        for g in touched:
            scoring_adj.setdefault(g, set()).add(cand)
    rank = kappa.pagerank(scoring_adj)

    scored = sorted(
        ((c, n, rank.get(c, 0.0), touched) for c, n, touched in candidates),
        key=lambda t: (-t[1], -t[2], t[0]),
    )

    # The substrate is one module, not two clusters (finding below), so the
    # operative κ is within-module hub-score, not component-joining. Rank every
    # universe gene by base-graph PageRank κ and report where the controls sit.
    base_kappa = kappa.pagerank(base)
    kappa_order = sorted(universe, key=lambda g: (-base_kappa.get(g, 0.0), g))
    kappa_pos = {g: i for i, g in enumerate(kappa_order)}
    top_hubs = [{"gene": g, "kappa": round(base_kappa[g], 8)} for g in kappa_order[:30]]

    envelopes = load_gene_envelopes()
    control = {
        g: {
            "in_universe": g in universe,
            "in_candidate_pool": g in pool,
            "components_joined_as_external": next((n for c, n, _t in candidates if c == g), 0),
            "base_kappa": round(base_kappa.get(g, 0.0), 8),
            "base_kappa_rank": kappa_pos.get(g),
            "base_kappa_percentile": (
                round(100 * (1 - kappa_pos[g] / len(universe)), 1) if g in kappa_pos else None
            ),
            "has_envelope": g in envelopes,
        }
        for g in CONTROL_GENES
    }

    result = {
        "stage": "Phase-2 build 1 — deterministic verifier baseline",
        "completed": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "dials": {"coexpr_tau": COEXPR_TAU, "control_genes": list(CONTROL_GENES)},
        "base_graph": {
            "universe": len(universe),
            "weak_components": len(comps),
            "largest_components": big,
            "coexpr_genes_loaded": len(expr),
        },
        "external_connector_candidates_total": len(scored),
        "top_kappa_hubs_in_module": top_hubs,
        "control_genes": control,
    }
    atomic_write_json(SIGSEARCH_OUT, result)
    print(json.dumps({"candidates_total": len(scored), "control_genes": control}, indent=2))
    print(f"[sigsearch] complete -> {SIGSEARCH_OUT}")


if __name__ == "__main__":
    main()

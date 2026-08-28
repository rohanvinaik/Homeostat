"""§13.4 — oracle-ensemble calibration on the known leprosy/Crohn's/IBD partition.

Question (checkpoint §6.3): does bridge signal survive across a varying oracle?
Here the oracle ensemble is a resolution sweep of modularity carvings on the
real STRING physical subgraph induced on the union of GWAS genes for leprosy,
Crohn's, and IBD. The KNOWN answer is the documented overlap (§9): genes
associated with >= 2 of the three traits are the bridges between the immunity
and IBD clusters. Prediction: bridge genes sit at high participation
(cross-community) STABLY across the resolution ensemble, and the signal
collapses under a label-shuffled null carving (§6.9 negative-control shape).

SCOPE (cheap-pass): this calibrates the STRUCTURE-DERIVED slice of the
ensemble. The traditional-tradition carvings (Ayurveda/TCM constituent-target
maps, Unani negative control) require the §6 carving compiler (THEORY Part
II.6, deferred) and are NOT in this run. This measures whether ensemble
variance behaves as §6.3 predicts before that compiler is built.

Run: make ensemble. Idempotent: skips if the output exists.
"""

import csv
import datetime
import json
import random
import statistics
import sys

from homeostat import paths
from homeostat.bridge import load_string_graph
from homeostat.carving import cnm_communities, participation, shuffle_labels
from homeostat.util import atomic_write_json

GAMMAS = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
N_PERM = 2000
SEED = 20260828
NULL_SEED = 424242

NETWORK = paths.DATA / "network"
TRAITS = {
    "leprosy": NETWORK / "gwas_leprosy.tsv",
    "crohns": NETWORK / "gwas_crohns_disease.tsv",
    "ibd": NETWORK / "gwas_inflammatory_bowel_disease.tsv",
}
ENSEMBLE_OUT = paths.EIR / "ensemble_calibration.json"


def load_trait_genes(path) -> set[str]:
    """MAPPED_GENE column of a GWAS Catalog association download -> gene set."""
    genes: set[str] = set()
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            raw = (row.get("MAPPED_GENE") or "").replace(" - ", ", ")
            for g in raw.split(", "):
                g = g.strip()
                if g and g != "NR":
                    genes.add(g)
    return genes


def separation(part_scores: dict[str, float], bridges: set[str], universe: list[str]) -> float:
    """mean participation of bridge genes - mean of the rest."""
    b = [part_scores[g] for g in universe if g in bridges]
    nb = [part_scores[g] for g in universe if g not in bridges]
    if not b or not nb:
        return 0.0
    return statistics.fmean(b) - statistics.fmean(nb)


def permutation_p(
    part_scores: dict[str, float], bridges: set[str], universe: list[str], rng: random.Random
) -> float:
    """One-sided p: shuffle which |bridges| genes are labelled bridge."""
    observed = separation(part_scores, bridges, universe)
    k = len([g for g in universe if g in bridges])
    ge = 0
    for _ in range(N_PERM):
        fake = set(rng.sample(universe, k))
        if separation(part_scores, fake, universe) >= observed:
            ge += 1
    return (1 + ge) / (1 + N_PERM)


def main() -> None:
    if ENSEMBLE_OUT.exists():
        print(f"[ensemble] already complete ({ENSEMBLE_OUT}); delete to re-run")
        return
    missing = [name for name, p in TRAITS.items() if not p.exists()]
    if missing:
        sys.exit(f"[ensemble] missing GWAS trait files: {missing}")

    trait_genes = {name: load_trait_genes(p) for name, p in TRAITS.items()}
    for name, g in trait_genes.items():
        print(f"[ensemble] {name}: {len(g)} mapped genes")

    counts: dict[str, int] = {}
    for genes in trait_genes.values():
        for g in genes:
            counts[g] = counts.get(g, 0) + 1
    universe_all = set(counts)
    bridges_all = {g for g, c in counts.items() if c >= 2}
    print(f"[ensemble] universe {len(universe_all)}; bridge genes (>=2 traits) {len(bridges_all)}")

    print("[ensemble] loading STRING physical graph ...")
    adj = load_string_graph()
    universe = sorted(universe_all & set(adj))
    bridges = bridges_all & set(universe)
    print(f"[ensemble] in-graph universe {len(universe)}; in-graph bridges {len(bridges)}")
    if len(bridges) < 3:
        sys.exit(f"[ensemble] too few in-graph bridge genes ({len(bridges)}) to calibrate")

    rng = random.Random(SEED)
    per_gamma = []
    for gamma in GAMMAS:
        comm = cnm_communities(adj, universe, gamma)
        n_comm = len(set(comm.values()))
        part = participation(adj, universe, comm)
        sep = separation(part, bridges, universe)
        p = permutation_p(part, bridges, universe, rng)

        null_comm = shuffle_labels(comm, NULL_SEED + int(gamma * 100))
        null_part = participation(adj, universe, null_comm)
        null_sep = separation(null_part, bridges, universe)

        per_gamma.append(
            {
                "gamma": gamma,
                "n_communities": n_comm,
                "bridge_vs_rest_separation": round(sep, 5),
                "permutation_p": round(p, 5),
                "null_carving_separation": round(null_sep, 5),
            }
        )
        print(
            f"[ensemble] gamma={gamma}: {n_comm} communities, "
            f"sep={sep:+.4f} p={p:.4f} null_sep={null_sep:+.4f}"
        )

    seps = [r["bridge_vs_rest_separation"] for r in per_gamma]
    null_seps = [r["null_carving_separation"] for r in per_gamma]
    n_sig = sum(
        1 for r in per_gamma if r["permutation_p"] < 0.05 and r["bridge_vs_rest_separation"] > 0
    )
    result = {
        "stage": "13.4 oracle-ensemble calibration (structure-derived slice)",
        "completed": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "scope_note": "structure-derived carvings only; traditional-tradition "
        "carvings deferred to the §6 carving compiler (THEORY Part II.6)",
        "dials": {"gammas": GAMMAS, "n_perm": N_PERM, "seed": SEED, "null_seed": NULL_SEED},
        "inputs": {
            "trait_gene_counts": {k: len(v) for k, v in trait_genes.items()},
            "universe_in_graph": len(universe),
            "bridge_genes_in_graph": len(bridges),
            "bridge_genes": sorted(bridges),
        },
        "per_gamma": per_gamma,
        "readout": {
            "mean_separation": round(statistics.fmean(seps), 5),
            "sd_separation": round(statistics.stdev(seps), 5),
            "gammas_significant": f"{n_sig}/{len(GAMMAS)}",
            "mean_null_separation": round(statistics.fmean(null_seps), 5),
            "sixthree_prediction_holds": n_sig >= len(GAMMAS) - 1
            and statistics.fmean(seps) > 2 * statistics.fmean(null_seps),
        },
    }
    atomic_write_json(ENSEMBLE_OUT, result)
    print(json.dumps(result["readout"], indent=2))
    print(f"[ensemble] complete -> {ENSEMBLE_OUT}")


if __name__ == "__main__":
    main()

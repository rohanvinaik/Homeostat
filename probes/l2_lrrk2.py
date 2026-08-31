"""probes/l2_lrrk2.py — L2 role encoder over REAL data, composed with the known-mechanism substrate.

Computes each gene's real data-signals (Fst differentiation over 1000G, GTEx co-expression with the
NOD2 seed), emits L2 facts (homeostat.l2_encoder.data_facts) with OPAQUE gene tokens (name-blind
reasoning — read back via the printed map), adds the known NOD2->RIP2->LRRK2 signaling roles as the
substrate (docs/ETIOLOGY_ENGINE.md §2b), and prints the assembled L3 fact-text to feed Regenesis
understand(universe_root=universes/mechanism). Prereq cache: /tmp/1000g_5pop_af.tsv (Ensembl 5-pop pull).

    PYTHONPATH=src python3 probes/l2_lrrk2.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lrrk2_genetic_diff import load_gene_diff  # noqa: E402
from lrrk2_slice2 import SEED, grow, presentation_genes, string_adjacency  # noqa: E402
from lrrk2_slice4 import gtex_profiles, pearson  # noqa: E402
from lrrk2_slice5 import cloud_rsids  # noqa: E402

from homeostat.l2_encoder import data_facts  # noqa: E402

COEXPR_MIN = 0.5
TRIAD_ROLE = {"NOD2": "senses pathogen", "RIPK2": "relays signal", "LRRK2": "amplifies signal"}
HUBS = ["HLA-DRB1", "HLA-DQA1", "IL18R1", "IL1RL1", "TNFSF15"]


def main() -> None:
    pres = presentation_genes()
    cloud, _ = grow(SEED, string_adjacency(400), pres)
    prof = gtex_profiles(cloud)
    nod2 = prof.get("NOD2")
    gene_fst, _ = load_gene_diff(cloud_rsids(cloud))
    with_data = [g for g in cloud if g in gene_fst]
    ranked = sorted(with_data, key=lambda g: gene_fst[g], reverse=True)
    diff_yes = set(ranked[: max(1, len(with_data) // 10)])  # top-decile differentiation

    scope = [g for g in list(TRIAD_ROLE) + HUBS if g in cloud]
    token = {g: f"gene{i + 1}" for i, g in enumerate(scope)}

    facts: list[str] = []
    for g, role in TRIAD_ROLE.items():  # substrate (§2b): authored known signaling roles
        if g in token:
            facts.append(f"{token[g]} {role}")
    audit = []
    for g in scope:  # L2 (§3b): data-derived roles from real Fst + GTEx
        diff_data = g in gene_fst
        differentiated = g in diff_yes
        coexp = bool(nod2 and g in prof and pearson(prof[g], nod2) >= COEXPR_MIN)
        facts.extend(data_facts(token[g], diff_data, differentiated, coexp))
        audit.append((token[g], g, diff_data, differentiated, coexp))

    print("=== token -> gene ===")
    for g in scope:
        print(f"  {token[g]:<7} = {g}")
    print("\n=== per-gene REAL signals (diff_data, differentiated, coexpresses) ===")
    for t, g, d, df, c in audit:
        print(f"  {t:<7} {g:<10} diff_data={d!s:<5} differentiated={df!s:<5} coexpresses={c}")
    print("\n=== ASSEMBLED FACT TEXT (feed to understand) ===")
    print(". ".join(facts) + ".")


if __name__ == "__main__":
    main()

"""probes/l2_lrrk2.py — L2 role encoder over REAL data ONLY (no hard-coded gene→role bindings).

Computes each gene's real data-signals and emits L2 facts (homeostat.l2_encoder.data_facts) with OPAQUE
gene tokens (name-blind reasoning — read back via the printed map): population differentiation (Fst,
ordinal tier), co-expression with the NOD2 seed (GTEx, evidence-derived cutoff), physical binding
(STRING high-confidence), and the informational zero. Mechanism components emerge from CONVERGENCE across
these computed lenses — there are NO authored gene→role facts (`NOD2 senses pathogen` etc. would be
purposivistic role-assignment, canon §3.3, and are FORBIDDEN; docs/ETIOLOGY_ENGINE.md §2b). Directed
signaling roles enter only when real directed evidence (Reactome) supplies them, as data.
Prereq cache: /tmp/1000g_5pop_af.tsv (Ensembl 5-pop pull).

    PYTHONPATH=src python3 probes/l2_lrrk2.py
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lrrk2_genetic_diff import load_gene_diff  # noqa: E402
from lrrk2_slice2 import SEED, grow, presentation_genes, string_adjacency  # noqa: E402
from lrrk2_slice4 import gtex_profiles, pearson  # noqa: E402
from lrrk2_slice5 import cloud_rsids  # noqa: E402

from homeostat.l2_encoder import data_facts, diff_tier  # noqa: E402

STRING_HI = 700  # STRING benchmark-calibrated high-confidence tier (evidence-derived, not a guess)
NULL_PCT = 95  # evidence-derived co-expression cutoff = this percentile of the GTEx correlation null
NULL_PERMS = 200
TRIAD = ["NOD2", "RIPK2", "LRRK2"]  # genes of interest to scope the read (NOT role-assigned)
HUBS = ["HLA-DRB1", "HLA-DQA1", "IL18R1", "IL1RL1", "TNFSF15"]


def gtex_null_cutoff(seed_vec: list[float], profiles: dict[str, list[float]]) -> float:
    """Evidence-derived co-expression cutoff (founder: derive thresholds from recorded evidence, not a
    default). The NULL_PCT-th percentile of |pearson| between a SHUFFLED seed profile and every real gene
    profile — the correlation you would see by chance in THIS GTEx data. Deterministic (seeded)."""
    rng = random.Random(0)
    base = list(seed_vec)
    null: list[float] = []
    for _ in range(NULL_PERMS):
        rng.shuffle(base)
        null.extend(abs(pearson(base, vec)) for vec in profiles.values())
    null.sort()
    return null[min(len(null) - 1, len(null) * NULL_PCT // 100)]


def main() -> None:
    pres = presentation_genes()
    cloud, _ = grow(SEED, string_adjacency(400), pres)
    prof = gtex_profiles(cloud)
    nod2 = prof.get("NOD2")
    gene_fst, _ = load_gene_diff(cloud_rsids(cloud))
    binders = string_adjacency(STRING_HI).get(SEED, set())  # STRING high-conf physical partners of seed
    coexpr_cut = gtex_null_cutoff(nod2, prof) if nod2 else 1.0

    scope = [g for g in TRIAD + HUBS if g in cloud]
    token = {g: f"gene{i + 1}" for i, g in enumerate(scope)}

    facts: list[str] = []
    audit = []
    for g in scope:  # L2: ONLY computed data lenses — Fst tier + GTEx co-expr + STRING bind + GWAS wiring
        tier = diff_tier(gene_fst.get(g))
        coexp = bool(nod2 and g in prof and pearson(prof[g], nod2) >= coexpr_cut)
        binds = g in binders and g != SEED
        wires = g in pres  # trait-wiring: gene associates with the presentation's disease traits (GWAS)
        facts.extend(data_facts(token[g], tier, coexp, binds, wires))
        audit.append((token[g], g, gene_fst.get(g), tier, coexp, binds, wires))

    print(f"=== evidence-derived GTEx co-expression cutoff (p{NULL_PCT} of null): {coexpr_cut:.3f} ===")
    print("=== token -> gene ===")
    for g in scope:
        print(f"  {token[g]:<7} = {g}")
    print("\n=== per-gene REAL signals (Fst, tier, coexpr, binds, wires) ===")
    for t, g, fst, tier, c, b, w in audit:
        fs = f"{fst:.3f}" if fst is not None else "  -  "
        print(f"  {t:<7} {g:<10} Fst={fs:<7} tier={tier:<9} coexpr={c!s:<5} binds={b!s:<5} wires={w}")
    print("\n=== ASSEMBLED FACT TEXT (feed to understand) ===")
    print(". ".join(facts) + ".")


if __name__ == "__main__":
    main()

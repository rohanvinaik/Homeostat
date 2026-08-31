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
from lrrk2_slice3 import hub_counts  # noqa: E402
from lrrk2_slice4 import gtex_profiles, pearson  # noqa: E402
from lrrk2_slice5 import cloud_rsids  # noqa: E402

from homeostat.l2_encoder import data_facts, diff_tier  # noqa: E402

STRING_HI = 700  # STRING benchmark-calibrated high-confidence tier (evidence-derived, not a guess)
NULL_PCT = (
    95  # evidence-derived co-expression cutoff = this percentile of the GTEx correlation null
)
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


def build_context(seed: str = SEED, string_lo: int = 400, string_hi: int = STRING_HI) -> dict:
    """Compute the mechanism-general lens context around a seed, ONCE, for reuse across a scope.

    Returns the cloud grown from the seed plus every genome-wide signal source the L2 encoder reads:
    per-gene population differentiation (Fst), the GTEx co-expression seed vector + evidence-derived
    cutoff, the seed's high-confidence STRING binders, the presentation (trait-wiring) set, and the
    GWAS-promiscuity counts + top-decile flood cutoff. Nothing here is LRRK2-specific except the seed
    argument — point it at any seed to build that mechanism's context (the A1/E1/C1 entry point)."""
    pres = presentation_genes()
    cloud, _ = grow(seed, string_adjacency(string_lo), pres)
    prof = gtex_profiles(cloud)
    seed_vec = prof.get(seed)
    gene_fst, _ = load_gene_diff(cloud_rsids(cloud))
    binders = string_adjacency(string_hi).get(
        seed, set()
    )  # STRING high-conf physical partners of seed
    coexpr_cut = gtex_null_cutoff(seed_vec, prof) if seed_vec else 1.0
    hc = hub_counts(
        cloud
    )  # promiscuity: distinct traits per gene in the full GWAS catalog (BOUNDARY)
    prom = sorted(hc.values(), reverse=True)
    prom_cut = (
        prom[max(1, len(prom) // 10) - 1] if prom else 10**9
    )  # evidence: top-decile of the cloud
    return {
        "seed": seed,
        "pres": pres,
        "cloud": cloud,
        "prof": prof,
        "seed_vec": seed_vec,
        "gene_fst": gene_fst,
        "binders": binders,
        "coexpr_cut": coexpr_cut,
        "hc": hc,
        "prom_cut": prom_cut,
    }


def scope_signals(scope: list[str], ctx: dict) -> list[tuple]:
    """The real per-gene L2 signals for a scope, in the given context — the SINGLE computation the
    probe and every validation script share, so a validation can never drift from the probe's numbers.
    Row: (gene, fst, tier, coexpr, binds, wires, traits, floods)."""
    out = []
    for g in scope:
        tier = diff_tier(ctx["gene_fst"].get(g))
        coexp = bool(
            ctx["seed_vec"]
            and g in ctx["prof"]
            and pearson(ctx["prof"][g], ctx["seed_vec"]) >= ctx["coexpr_cut"]
        )
        binds = g in ctx["binders"] and g != ctx["seed"]
        wires = (
            g in ctx["pres"]
        )  # trait-wiring: gene associates with the presentation's disease traits
        floods = (
            ctx["hc"].get(g, 0) >= ctx["prom_cut"]
        )  # specificity CENSOR: top-decile-promiscuous hub
        out.append(
            (g, ctx["gene_fst"].get(g), tier, coexp, binds, wires, ctx["hc"].get(g, 0), floods)
        )
    return out


def main() -> None:
    ctx = build_context()
    cloud, coexpr_cut, prom_cut = ctx["cloud"], ctx["coexpr_cut"], ctx["prom_cut"]

    scope = [g for g in TRIAD + HUBS if g in cloud]
    token = {g: f"gene{i + 1}" for i, g in enumerate(scope)}

    facts: list[str] = []
    audit = []
    for g, fst, tier, coexp, binds, wires, traits, floods in scope_signals(scope, ctx):
        facts.extend(data_facts(token[g], tier, coexp, binds, wires, floods))
        audit.append((token[g], g, fst, tier, coexp, binds, wires, traits, floods))

    print(
        f"=== GTEx co-expr cutoff p{NULL_PCT} null={coexpr_cut:.3f} | promiscuity flood cut (top decile)>={prom_cut} ==="
    )
    print("=== token -> gene ===")
    for g in scope:
        print(f"  {token[g]:<7} = {g}")
    print("\n=== per-gene REAL signals (Fst, tier, coexpr, binds, wires, promiscuity/floods) ===")
    for t, g, fst, tier, c, b, w, hcount, fl in audit:
        fs = f"{fst:.3f}" if fst is not None else "  -  "
        print(
            f"  {t:<7} {g:<10} Fst={fs:<7} tier={tier:<9} coexpr={c!s:<5} binds={b!s:<5} wires={w!s:<5} traits={hcount:<5} floods={fl}"
        )
    print("\n=== ASSEMBLED FACT TEXT (feed to understand) ===")
    print(". ".join(facts) + ".")


if __name__ == "__main__":
    main()

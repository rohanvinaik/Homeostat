"""homeostat.relevance — the input layer's RELEVANCE FILTER: a diagnosis → the possibly-relevant
gene subspace that scopes generate-wide.

The first turn-component of the operator/computer interface (Detective's CLI, transposed): a
DIAGNOSIS is an operator-domain label — a lossy projection the person holds. So it enters as a
TESTED relevance, never ground truth: it says "look HERE" (which subspace of the interactome could
possibly matter for this trait), and κ inside that subspace does the actual significance. If nothing
in the relevant subspace explains the shadow, `drive` returns a certified-⊥ — the label falls out,
exactly as a wrong operator hypothesis does. The computer never trusts the label as significance
(that would trespass the operator's domain AND launder a population statistic into a verdict); the
operator never computes the mechanism.

The reference is the GWAS catalog trait→gene index (`trait_wiring.py`'s columns/parsers), widened by
role-equivalence (fungibility — a paralog doing the same job is in-scope). GWAS-as-search-prior is
Law 1's one sanctioned use of a population statistic: never the method, the object, or the verdict.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from homeostat.fungibility import Fungible
from homeostat.trait_wiring import (
    MAPPED_GENE_COL,
    MAPPED_TRAIT_COL,
    parse_genes,
    parse_traits,
)


def trait_gene_index(rows: Iterable[list[str]]) -> dict[str, set[str]]:
    """The diagnosis→gene reference: per EFO trait, the set of genes GWAS associates with it (the
    catalog's MAPPED_TRAIT → MAPPED_GENE). A RELEVANCE reference (the operator's "look here"), never
    significance — it scopes generate-wide, κ inside does the significance. Orchestration over
    `trait_wiring.parse_traits` / `parse_genes`; intent-tested.
    """
    index: dict[str, set[str]] = {}
    for row in rows:
        if len(row) <= MAPPED_TRAIT_COL:
            continue
        genes = parse_genes(row[MAPPED_GENE_COL])
        for trait in parse_traits(row[MAPPED_TRAIT_COL]):
            index.setdefault(trait, set()).update(genes)
    return index


def relevant_subspace(
    diagnosis: str,
    trait_index: Mapping[str, set[str]],
    fungible: Mapping[str, set[str]],
) -> set[str]:
    """The relevance filter: a diagnosis → the possibly-relevant gene subspace = its GWAS-associated
    canonical genes (`trait_index`) WIDENED by role-equivalence (`fungible` — each gene's earned
    fungible partners, so a paralog doing the same job is in-scope). TESTED relevance, never truth:
    it scopes generate-wide, and `drive` returns a certified-⊥ if nothing in the subspace explains
    the shadow (the label falls out, like a wrong hypothesis). Empty when the diagnosis is unknown —
    an honest miss (the operator named a trait the catalog does not carry). Pure over the maps.
    """
    canonical = trait_index.get(diagnosis, set())
    subspace = set(canonical)
    for gene in canonical:
        subspace |= fungible.get(gene, set())
    return subspace


def fungible_map(fungibles: Iterable[Fungible]) -> dict[str, set[str]]:
    """The earned-fungible adjacency ``{gene: {role-equivalent partners}}`` from `read_fungibility`
    verdicts — ONLY the EARNED ``"fungible"`` pairs (≥2 banks converged), symmetric. This is what
    `relevant_subspace` widens by: a paralog doing the same job is in-scope. The unearned verdicts
    (``"coincidental"`` / ``"seed-only"``) do NOT widen. Orchestration over the Fungible list.
    """
    adj: dict[str, set[str]] = {}
    for f in fungibles:
        if f.verdict == "fungible":
            adj.setdefault(f.a, set()).add(f.b)
            adj.setdefault(f.b, set()).add(f.a)
    return adj

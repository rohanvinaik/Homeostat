"""homeostat.metabolic — Reactome metabolic pathways → metabolic-flux L2 Events.

The metabolic-flux network (THESIS ch.8): a level below regulatory, the passive energy-state
coupling where the summation theorem lives (control distributed across a pathway). Instantiated as
co-membership in a Reactome METABOLIC pathway — two enzymes in one metabolic pathway are coupled.
An UNDIRECTED vote (LAW 9): `Event("metabolic","channels",A,B,+1,"")`, emitted in both
orderings (an undirected vote supports a coupling in either direction).

Scoping to the Metabolism subtree is LOAD-BEARING: unscoped pathway co-membership is dominated by
signaling and merely re-states regulatory (zero orthogonality), so only pathways descended from
Metabolism (R-HSA-1430728) count. Entrez ids are normalized to gene symbols via NCBI gene_info;
unmapped genes are dropped.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from homeostat.event import Event

METABOLISM_ROOT = "R-HSA-1430728"
# NCBI2Reactome columns (tab): entrez pathway_stId url name evidence species
ENTREZ, PATHWAY, SPECIES = 0, 1, 5
_HUMAN = "Homo sapiens"


def metabolic_pathways(relation_rows: Iterable[list[str]], root: str = METABOLISM_ROOT) -> set[str]:
    """BFS the Reactome parent→child relation from `root`; return `root` + all descendant pathway
    stIds (the metabolic subtree). Pure over the `[parent, child]` rows.
    """
    children: dict[str, list[str]] = {}
    for r in relation_rows:
        if len(r) >= 2:
            children.setdefault(r[0], []).append(r[1])
    seen = {root}
    stack = [root]
    while stack:
        for c in children.get(stack.pop(), []):
            if c not in seen:
                seen.add(c)
                stack.append(c)
    return seen


def pair_up(members: list[str]) -> list[tuple[str, str]]:
    """All unordered pairs of a DISTINCT-sorted member list — the co-membership edges. Pure.
    Deduped + sorted so a pathway's edge set is deterministic; each pair appears once as (A<B).
    """
    uniq = sorted(set(members))
    return [(uniq[i], uniq[j]) for i in range(len(uniq)) for j in range(i + 1, len(uniq))]


def co_metabolism_events(
    reactome_rows: Iterable[list[str]],
    metabolic_ids: set[str],
    entrez_symbol: Mapping[str, str],
) -> list[Event]:
    """Group human genes by METABOLIC pathway (Entrez→symbol), then emit each within-pathway pair as
    an undirected metabolic Event in BOTH orderings. Orchestration; intent-tested.
    """
    by_pathway: dict[str, set[str]] = {}
    for r in reactome_rows:
        if len(r) <= SPECIES or r[SPECIES] != _HUMAN or r[PATHWAY] not in metabolic_ids:
            continue
        sym = entrez_symbol.get(r[ENTREZ])
        if sym is not None:
            by_pathway.setdefault(r[PATHWAY], set()).add(sym)
    out: list[Event] = []
    for genes in by_pathway.values():
        for a, b in pair_up(list(genes)):
            out.append(Event("metabolic", "channels", a, b, 1, ""))
            out.append(Event("metabolic", "channels", b, a, 1, ""))
    return out

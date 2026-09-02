"""homeostat.homology — the Ensembl Compara adapter: human paralogs → evolutionary L2 Events.

The evolutionary network is the role-FUNGIBILITY geometry (THESIS ch.8): homologs are fungible
role-fillers, so a within-species paralog pair (gene A and its paralog B) can fill the same role in
different people — the invariant Regenesis later recovers with `common_frame`. It is an UNDIRECTED
mechanistic vote (LAW 9): every edge is `Event("evolutionary", "resembles", A, B, sign=+1, mode="")`
— `sign=+1` asserts the homology relation exists (a proven descent relation, not a computed
correlation — low bright-line risk), and `evolutionary` is NOT a directed network, so it earns no
arrow. By design it rarely converges with regulatory/physical (homologs seldom co-regulate) — that
orthogonality is the point; its payoff is fungibility at the Regenesis stage, not per-edge weight.

The Compara file is human-vs-all-species; the bright line keeps only human WITHIN-species paralogs
(`homology_type` contains `paralog` AND `homology_species` is `homo_sapiens`) — cross-species
orthologs are skipped. Endpoints are Ensembl protein ids normalized to gene symbols via the shared
STRING info map (`string_fetch.load_alias_map`, keyed with the `9606.` prefix); an unmapped endpoint
is dropped.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from homeostat.event import Event

# Compara homologies TSV columns (tab-separated):
# gene_stable_id protein_stable_id species identity homology_type
# homology_gene_stable_id homology_protein_stable_id homology_species ...
PROTEIN_A, HOMOLOGY_TYPE, PROTEIN_B, HOMOLOGY_SPECIES = 1, 4, 6, 7
_MIN_COLS = 8  # we read through homology_species (index 7)
_PREFIX = "9606."  # STRING alias keys are 9606.ENSP…; Compara ids are bare ENSP…


def homology_disposition(homology_type: str, homology_species: str) -> str:
    """Keep/skip for one Compara row, from its homology type + species. Pure over (str, str).

    ``"emit"`` iff it is a human WITHIN-species paralog — `homology_type` contains ``"paralog"``
    AND `homology_species` is ``"homo_sapiens"`` (the fungibility substrate). Else
    ``"skip-ortholog"``: a cross-species ortholog (or non-paralog), outside the human n=1 geometry.
    """
    if "paralog" in homology_type and homology_species == "homo_sapiens":
        return "emit"
    return "skip-ortholog"


def row_to_event(fields: list[str], alias: Mapping[str, str]) -> Event | None:
    """One Compara row → an undirected evolutionary `Event`, or None (bad / filtered / unmapped).

    Emits `Event("evolutionary","resembles",A,B,+1,"")` for a human paralog pair whose both Ensembl
    protein ids normalize to gene symbols via `alias`. Over the pinned `homology_disposition`.
    """
    if len(fields) < _MIN_COLS:
        return None
    if homology_disposition(fields[HOMOLOGY_TYPE], fields[HOMOLOGY_SPECIES]) != "emit":
        return None
    a = alias.get(_PREFIX + fields[PROTEIN_A])
    b = alias.get(_PREFIX + fields[PROTEIN_B])
    if a is None or b is None:
        return None
    return Event("evolutionary", "resembles", a, b, 1, "")


def homology_events(rows: Iterable[list[str]], alias: Mapping[str, str]) -> list[Event]:
    """Render a stream of Compara rows into undirected evolutionary `Event`s, normalized by `alias`.
    I/O-free orchestration over `row_to_event`; intent-tested.
    """
    out: list[Event] = []
    for r in rows:
        e = row_to_event(r, alias)
        if e is not None:
            out.append(e)
    return out

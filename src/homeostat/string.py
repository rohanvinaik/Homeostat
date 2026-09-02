"""homeostat.string — the STRING adapter: physical interactions → undirected L2 Events.

STRING's physical subnetwork is the physical-BINDING network — an UNDIRECTED mechanistic
vote (LAW 9, the three-tier bright line): object-eligible for a coupling's EXISTENCE, never
its direction. Every edge is `Event("physical", "binds", geneA, geneB, sign=+1, mode="")` —
`sign=+1` asserts the interaction exists (STRING never says "A does not bind B"), and
`physical` is NOT a directed network, so the edge earns no arrow (direction is regulatory's
alone; two networks converging on one coupling raise its κ).

The `physical.links.detailed` file carries three evidence channels (`experimental database
textmining`), and the bright line applies DIRECTLY: an edge is a proven mechanism iff it has
EXPERIMENTAL or curated DATABASE evidence; a `textmining`-only edge is a computed association
(text co-occurrence) and is skipped — never an object. Ensembl protein ids are normalized to
gene symbols via the STRING info map (`string_fetch.load_alias_map`); an endpoint with no
mapping is dropped (no canonical atomic → it cannot converge with the other networks).
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from homeostat.event import Event

# STRING physical.links.detailed columns (space-separated):
# protein1 protein2 experimental database textmining combined_score
P1, P2, EXPERIMENTAL, DATABASE, TEXTMINING, COMBINED = 0, 1, 2, 3, 4, 5
_MIN_COLS = 4  # the fields we read run through DATABASE (index 3)


def edge_disposition(experimental: int, database: int) -> str:
    """Keep/skip for one STRING physical edge, from its evidence channels. Pure over (int, int).

    ``"emit"`` iff the edge has EXPERIMENTAL or curated DATABASE evidence — a proven physical
    binding, object-eligible as an undirected vote (LAW 9). Else ``"skip-textmining-only"``: it
    rests on text co-occurrence alone, a computed association that may never be the verdict-object.
    (`combined_score` is a confidence, never significance — significance is κ — so it never gates.)
    """
    if experimental > 0 or database > 0:
        return "emit"
    return "skip-textmining-only"


def row_to_event(fields: list[str], alias: Mapping[str, str]) -> Event | None:
    """One STRING physical row → an undirected physical `Event`, or None (bad/filtered/unmapped).

    Emits `Event("physical","binds",A,B,+1,"")` when the edge has experimental or database evidence
    AND both Ensembl ids normalize via `alias`. Composition over the pinned `edge_disposition`.
    """
    if len(fields) < _MIN_COLS:
        return None
    try:
        experimental = int(fields[EXPERIMENTAL])
        database = int(fields[DATABASE])
    except ValueError:
        return None
    if edge_disposition(experimental, database) != "emit":
        return None
    a = alias.get(fields[P1])
    b = alias.get(fields[P2])
    if a is None or b is None:
        return None
    return Event("physical", "binds", a, b, 1, "")


def string_events(rows: Iterable[list[str]], alias: Mapping[str, str]) -> list[Event]:
    """Render a stream of STRING physical rows into undirected physical `Event`s, normalized by
    `alias`. I/O-free orchestration over `row_to_event`; intent-tested.
    """
    out: list[Event] = []
    for r in rows:
        e = row_to_event(r, alias)
        if e is not None:
            out.append(e)
    return out

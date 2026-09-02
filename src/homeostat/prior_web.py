"""homeostat.prior_web — assemble the multi-network prior web from all renderers.

The "prior web" (SYSTEM_DESIGN §11): the fixed, bounded web of known regulatory mechanisms the
engine resolves over — built ONCE from proven biology, never learned from the person. This is the
single assembly point: ensure each network's data is cached, render each into `list[Event]`, and
compile the combined stream into the `RelationalWeb` via `events_to_web`. `DIRECTED_NETWORKS` names
the one directed-mechanism network (regulatory) that earns arrows; every other network is an
undirected vote, so convergence across independent networks — not any one score — raises a coupling.

I/O orchestration (downloads on first run); the pure per-network decisions are pinned in each
renderer. Adding a network is one entry here + its renderer/fetch pair — nothing else changes.
"""

from __future__ import annotations

from homeostat import (
    homology,
    homology_fetch,
    metabolic,
    metabolic_fetch,
    signor,
    signor_fetch,
    string,
    string_fetch,
)
from homeostat.event import Event, events_to_web
from homeostat.web import RelationalWeb

# The only directed-mechanism network — it alone earns arrows (LAW 5); the rest are undirected.
DIRECTED_NETWORKS = frozenset({"regulatory"})


def all_events() -> list[Event]:
    """Ensure every network's data is cached, render each into Events, return the combined stream.

    regulatory (SIGNOR, directed) + physical (STRING, undirected) + evolutionary (Compara paralogs,
    undirected) + metabolic (Reactome metabolic co-membership, undirected). STRING's ENSP→symbol map
    is shared with the homology renderer.
    """
    signor_fetch.ensure()
    _, info = string_fetch.ensure_all()
    alias = string_fetch.load_alias_map(info)
    homology_fetch.ensure()
    ncbi, rel, gi = metabolic_fetch.ensure_all()
    metabolic_ids = metabolic.metabolic_pathways(metabolic_fetch.load_tsv(rel))
    entrez_symbol = metabolic_fetch.load_entrez_symbol(gi)
    return [
        *signor.signor_events(signor_fetch.load_rows()),
        *string.string_events(string_fetch.load_rows(), alias),
        *homology.homology_events(homology_fetch.load_rows(), alias),
        *metabolic.co_metabolism_events(
            metabolic_fetch.load_tsv(ncbi), metabolic_ids, entrez_symbol
        ),
    ]


def build_prior_web(events: list[Event] | None = None) -> RelationalWeb:
    """Compile the multi-network event stream into the prior `RelationalWeb` (regulatory directed,
    the rest undirected votes). Pass `events` to skip rendering; else `all_events()` renders live.
    """
    stream = all_events() if events is None else events
    return events_to_web(stream, directed_networks=DIRECTED_NETWORKS)


def _main() -> None:  # pragma: no cover - reproducible multi-network read, not unit-tested
    events = all_events()
    web = build_prior_web(events)
    print(f"events: {len(events)}  couplings: {len(web.couplings)}")
    for k in (2, 3, 4):
        n = len([c for c in web.couplings if c.weight >= k])
        print(f"  couplings with >={k} network support: {n}")


if __name__ == "__main__":
    _main()

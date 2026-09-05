"""Intent tests for the STRING adapter — from the three-tier bright line and real STRING shapes.

Physical binding is an UNDIRECTED vote: sign=+1 (existence), verb "binds", mode "", net "physical"
(never directed). Evidence bright line: experimental OR database → emit; textmining-only → skip
(computed association). ENSP ids are normalized to gene symbols via the alias map."""

from homeostat.string import (
    DATABASE,
    EXPERIMENTAL,
    P1,
    P2,
    edge_disposition,
    row_to_event,
    string_events,
)

# a tiny ENSP -> gene-symbol map, as string_fetch.load_alias_map would build
ALIAS = {
    "9606.ENSP_RIPK2": "RIPK2",
    "9606.ENSP_TRAF6": "TRAF6",
    "9606.ENSP_NOD2": "NOD2",
}


def _row(p1, p2, experimental, database, textmining=0, combined=0):
    r = [""] * 6
    r[P1], r[P2] = p1, p2
    r[EXPERIMENTAL], r[DATABASE] = str(experimental), str(database)
    r[4], r[5] = str(textmining), str(combined)
    return r


# ---- the pure evidence-channel bright line ---------------------------------------


def test_edge_disposition_is_the_bright_line():
    assert edge_disposition(312, 0) == "emit"  # experimental
    assert edge_disposition(0, 500) == "emit"  # curated database
    assert edge_disposition(312, 500) == "emit"  # both
    assert edge_disposition(0, 0) == "skip-textmining-only"  # neither -> textmining-only, forbidden


# ---- row -> Event on real STRING shapes ------------------------------------------


def test_experimental_edge_becomes_an_undirected_physical_vote():
    row = _row("9606.ENSP_RIPK2", "9606.ENSP_TRAF6", experimental=312, database=0, combined=311)
    e = row_to_event(row, ALIAS)
    assert e is not None
    assert (e.network, e.verb, e.subject, e.target, e.sign, e.mode) == (
        "physical",
        "binds",
        "RIPK2",
        "TRAF6",
        1,  # existence, NOT direction — "physical" is never a directed network
        "",
    )


def test_database_edge_emits_too():
    row = _row("9606.ENSP_NOD2", "9606.ENSP_RIPK2", experimental=0, database=500)
    e = row_to_event(row, ALIAS)
    assert e is not None
    assert (e.subject, e.target, e.sign) == ("NOD2", "RIPK2", 1)


def test_textmining_only_edge_is_skipped():
    row = _row("9606.ENSP_RIPK2", "9606.ENSP_TRAF6", experimental=0, database=0, textmining=800)
    assert row_to_event(row, ALIAS) is None


def test_unmapped_endpoint_is_dropped():
    # no canonical atomic for the second protein -> cannot converge, so drop
    row = _row("9606.ENSP_RIPK2", "9606.ENSP_UNKNOWN", experimental=312, database=0)
    assert row_to_event(row, ALIAS) is None


def test_string_events_filters_the_stream():
    rows = [
        _row("9606.ENSP_RIPK2", "9606.ENSP_TRAF6", 312, 0),  # kept (experimental)
        _row("9606.ENSP_NOD2", "9606.ENSP_RIPK2", 0, 0, textmining=900),  # drop (textmining-only)
        _row("9606.ENSP_RIPK2", "9606.ENSP_UNKNOWN", 312, 0),  # dropped (unmapped)
    ]
    events = string_events(rows, ALIAS)
    assert [(e.subject, e.target, e.network, e.sign) for e in events] == [
        ("RIPK2", "TRAF6", "physical", 1),
    ]

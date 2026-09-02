"""Intent tests for the Compara homology adapter — the evolutionary/fungibility network.

An undirected vote: sign=+1 (existence), verb "resembles", mode "", network "evolutionary". Bright
line: human WITHIN-species paralog (type contains "paralog" AND species homo_sapiens) → emit;
cross-species ortholog → skip. Endpoints are Ensembl protein ids normalized to symbols via the
STRING alias map (keyed with the 9606. prefix)."""

from homeostat.homology import (
    HOMOLOGY_SPECIES,
    HOMOLOGY_TYPE,
    PROTEIN_A,
    PROTEIN_B,
    homology_disposition,
    homology_events,
    row_to_event,
)

# STRING-style alias keys carry the 9606. prefix; Compara protein ids are bare.
ALIAS = {"9606.ENSP_LRRK1": "LRRK1", "9606.ENSP_LRRK2": "LRRK2", "9606.ENSP_NOD1": "NOD1"}


def _row(protein_a, homology_type, protein_b, homology_species):
    r = [""] * 15
    r[PROTEIN_A], r[HOMOLOGY_TYPE] = protein_a, homology_type
    r[PROTEIN_B], r[HOMOLOGY_SPECIES] = protein_b, homology_species
    return r


# ---- the pure bright line --------------------------------------------------------


def test_homology_disposition_keeps_human_paralogs_only():
    assert homology_disposition("within_species_paralog", "homo_sapiens") == "emit"
    assert homology_disposition("other_paralog", "homo_sapiens") == "emit"
    assert homology_disposition("ortholog_one2one", "pan_paniscus") == "skip-ortholog"
    assert homology_disposition("ortholog_many2many", "pongo_abelii") == "skip-ortholog"


# ---- row -> Event on real Compara shapes -----------------------------------------


def test_paralog_becomes_an_undirected_evolutionary_event():
    # LRRK2 ~ LRRK1 (a real within-species paralog pair)
    row = _row("ENSP_LRRK2", "within_species_paralog", "ENSP_LRRK1", "homo_sapiens")
    e = row_to_event(row, ALIAS)
    assert e is not None
    assert (e.network, e.verb, e.subject, e.target, e.sign, e.mode) == (
        "evolutionary",
        "resembles",
        "LRRK2",
        "LRRK1",
        1,
        "",
    )


def test_cross_species_ortholog_is_skipped():
    row = _row("ENSP_LRRK2", "ortholog_one2one", "ENSPPTRG_X", "pan_troglodytes")
    assert row_to_event(row, ALIAS) is None


def test_unmapped_endpoint_is_dropped():
    row = _row("ENSP_LRRK2", "within_species_paralog", "ENSP_UNKNOWN", "homo_sapiens")
    assert row_to_event(row, ALIAS) is None


def test_homology_events_filters_the_stream():
    rows = [
        _row("ENSP_LRRK2", "within_species_paralog", "ENSP_LRRK1", "homo_sapiens"),  # kept
        _row("ENSP_NOD1", "within_species_paralog", "ENSP_LRRK2", "homo_sapiens"),  # kept
        _row("ENSP_LRRK2", "ortholog_one2one", "ENSPPTRG_X", "pan_troglodytes"),  # drop (ortholog)
    ]
    events = homology_events(rows, ALIAS)
    assert [(e.subject, e.target, e.network, e.sign) for e in events] == [
        ("LRRK2", "LRRK1", "evolutionary", 1),
        ("NOD1", "LRRK2", "evolutionary", 1),
    ]

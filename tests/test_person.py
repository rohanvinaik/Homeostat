"""Integration tests for the input-layer assembly (`read_person`) — one turn of the operator/
computer call-and-response, driven end to end through the real read."""

from homeostat.event import Event
from homeostat.person import read_person
from homeostat.signal import Signal, Tier

_EVENTS = [
    Event("regulatory", "amplifies", "source", "A", 1),
    Event("regulatory", "amplifies", "source", "B", 1),
    Event("regulatory", "amplifies", "decoy", "A", 1),
]
VS = {"amplifies": 1, "inhibits": -1}
_REF = {"A": (70.0, 100.0), "B": (70.0, 100.0), "source": (0.0, 1e9), "decoy": (0.0, 1e9)}
_VOCAB = {n: n for n in ("A", "B", "source", "decoy")}


def _reference(node, demographics):
    return _REF.get(node)


def _labs():
    return [
        Signal("A", "120", Tier.VERIFIED),  # above the band -> a symptom (up)
        Signal("B", "120", Tier.VERIFIED),  # up
        Signal("source", "1", Tier.VERIFIED),  # in-band -> the informational zero, not a symptom
        Signal("decoy", "1", Tier.VERIFIED),
    ]


def _read(diagnosis, trait_index):
    return read_person(
        diagnosis,
        _labs(),
        _EVENTS,
        VS,
        trait_index,
        demographics={"age": "40"},
        reference=_reference,
        vocab=_VOCAB,
    )


def test_read_person_resolves_when_the_diagnosis_scopes_to_the_source():
    # diagnosis "adhd" -> {source, decoy} (a genuine plurality); labs show A,B up. drive falsifies
    # decoy (reaches A only) and resolves to source (reaches both) -- a FALSIFIABLE resolution.
    read = _read("adhd", {"adhd": {"source", "decoy"}})
    assert read.verdict == "resolved" and read.trajectory.survivors_left == ["source"]


def test_read_person_single_gene_subspace_is_degenerate_not_resolved():
    # a diagnosis scoping to ONE gene resolves to it self-confirmingly (nothing was falsified) ->
    # the honest verdict is DEGENERATE (σ_sem = 0, Law 7), never a spurious RESOLVED.
    read = _read("adhd", {"adhd": {"source"}})
    assert read.verdict == "degenerate"


def test_read_person_label_falls_out_when_it_scopes_away_the_source():
    # diagnosis scopes to {decoy} (excludes source); decoy cannot explain B, and the shadow stays
    # observed truth -> the read does NOT resolve, the excluded source is never surfaced.
    read = _read("adhd", {"adhd": {"decoy"}})
    assert read.verdict != "resolved"
    assert "source" not in read.trajectory.survivors_left


def test_read_person_unknown_diagnosis_is_an_honest_miss():
    # the operator names a trait the catalog does not carry -> empty subspace -> nothing to search.
    read = _read("unknown", {"adhd": {"source"}})
    assert read.verdict != "resolved"

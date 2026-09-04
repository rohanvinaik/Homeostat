"""Intent tests for the story-read composer — the four dynamics genres -> tier-2 dramatic account
-> tier-3 treatment. Authored from the design; `triples_to_contracts` is Detective-pinned. The
tier-2 (Regenesis) is validated end-to-end separately; here it degrades gracefully (engine gone)."""

import json

from homeostat.comedy import Comedy
from homeostat.event import Event
from homeostat.fungibility import Fungible
from homeostat.lament import Lament
from homeostat.narrative import StoryRead, genre_triples, read_story, triples_to_contracts
from homeostat.quest import Quest
from homeostat.tragedy import Tragedy


def _amp(u, v):
    return Event("regulatory", "amplifies", u, v, 1)


# ---- the hand-authored genre -> Polti linkage ------------------------------------


def test_genre_triples_maps_each_genre_to_its_polti_situation():
    genres = {
        "tragedy": [Tragedy("A", "B", "doomed")],  # pursuit
        "comedy": [Comedy("C", "D", "vicious")],  # revenge
        "quest": [Quest("H", ("X", "Y"), 1.0, "resolving")],  # obtaining, per joined part
        "allegory": [Fungible("E", "F", "fungible", 2)],  # a lens, NOT a dramatic situation
    }
    tr = genre_triples(genres)
    assert ("A", "harm", "B") in tr
    assert ("C", "betray", "D") in tr
    assert ("H", "seize", "X") in tr and ("H", "seize", "Y") in tr
    assert all(subj != "E" for subj, _, _ in tr)  # allegory emits NO dramatic fact


def test_genre_triples_skips_the_non_dramatic_verdicts():
    # homeostatic comedy is the benign ending; indeterminate tragedy has no dramatic relation.
    genres = {
        "comedy": [Comedy("A", "B", "homeostatic")],
        "tragedy": [Tragedy("C", "D", "indeterminate")],
    }
    assert genre_triples(genres) == []


def test_genre_triples_entangling_quest_is_a_failed_pursuit():
    genres = {"quest": [Quest("H", ("X",), 0.1, "entangling")]}
    assert genre_triples(genres) == [("H", "pursue", "X")]


# ---- the pure contract emitter (the GSE-free tier-2 input) ------------------------


def test_triples_to_contracts_builds_coreferent_event_contracts():
    nodes = [
        json.loads(line)
        for line in triples_to_contracts([("A", "harm", "B"), ("A", "seize", "C")]).splitlines()
    ]
    assert len(nodes) == 2
    # A is ONE entity across both facts (coreference -> the meta-narrative's arc).
    a_ids = {n["predicate"]["args"][0]["entity_id"] for n in nodes}
    assert len(a_ids) == 1
    # verb_classes=[verb] is what the narrative universe fires on (the literal Polti trigger).
    assert nodes[0]["predicate"]["features"]["verb_classes"] == ["harm"]


def test_triples_to_contracts_empty_is_empty():
    assert triples_to_contracts([]) == ""


# ---- the composed read -----------------------------------------------------------


def test_read_story_yields_the_three_tiers():
    # FLAW -> MID -> SINK is a doomed cascade, no rescue. tier-1 dynamics + tier-3 treatment stand
    # regardless of the engine; tier-2 `account` fires if Regenesis present, else None (graceful).
    sr = read_story([_amp("FLAW", "MID"), _amp("MID", "SINK")], observed=["SINK"])
    assert isinstance(sr, StoryRead)
    assert sr.genres["tragedy"] == [Tragedy("FLAW", "SINK", "doomed")]
    assert sr.treatment == [Lament("SINK", None, "palliative")]
    assert sr.account is None or isinstance(
        sr.account, dict
    )  # None (engine absent) or the tier-2 read

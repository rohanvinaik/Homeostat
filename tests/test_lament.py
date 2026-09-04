"""Intent tests for the lament genre — the treatment-tier read over the dynamics genres.
Authored from the design; `lament_verdict` is Detective-pinned."""

from homeostat.fungibility import Fungible
from homeostat.lament import Lament, lament_verdict, read_lament
from homeostat.quest import Quest
from homeostat.tragedy import Tragedy


def test_lament_verdict_curable_when_a_quest_addresses_it():
    # a resolving quest is a cure -> not a lament, and a cure trumps a mere workaround.
    assert lament_verdict(addressed=True, has_substitute=False) == "curable"
    assert lament_verdict(addressed=True, has_substitute=True) == "curable"


def test_lament_verdict_substituted_when_a_fungible_stand_in_exists():
    assert lament_verdict(addressed=False, has_substitute=True) == "substituted"


def test_lament_verdict_palliative_when_neither():
    assert lament_verdict(addressed=False, has_substitute=False) == "palliative"


def test_read_lament_doomed_with_no_cure_is_palliative():
    genres = {"tragedy": [Tragedy("FLAW", "SINK", "doomed")], "quest": [], "allegory": []}
    assert read_lament(genres) == [Lament("SINK", None, "palliative")]


def test_read_lament_a_resolving_quest_makes_it_curable_and_dropped():
    genres = {
        "tragedy": [Tragedy("FLAW", "SINK", "doomed")],
        "quest": [Quest("HERO", ("SINK",), 1.0, "resolving")],
        "allegory": [],
    }
    assert read_lament(genres) == []  # a cure exists -> not a lament


def test_read_lament_a_fungible_stand_in_routes_around_the_loss():
    genres = {
        "tragedy": [Tragedy("FLAW", "SINK", "doomed")],
        "quest": [],
        "allegory": [Fungible("SINK", "PARALOG", "fungible", 2)],
    }
    assert read_lament(genres) == [Lament("SINK", "PARALOG", "substituted")]


def test_read_lament_ignores_a_suppressed_tragedy():
    # only DOOMED (a locked loss) is mourned; suppressed is a held-down state, not a death.
    genres = {"tragedy": [Tragedy("FLAW", "SINK", "suppressed")], "quest": [], "allegory": []}
    assert read_lament(genres) == []

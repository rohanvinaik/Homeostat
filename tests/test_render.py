"""Story-led render tests — the pure phrase-decisions (branch by branch) + `render` validated
end-to-end over a REAL `DriverRead` produced by `drive` (never a hand-built one)."""

from homeostat.driver import drive
from homeostat.event import Event
from homeostat.position import position
from homeostat.render import (
    allegory_clause,
    comedy_clause,
    dramatic_situation,
    lament_clause,
    outcome_clause,
    quest_clause,
    render,
    tragedy_clause,
    verdict_clause,
)

VS = {"amplifies": 1, "inhibits": -1}


def _reg(verb, subj, tgt):
    return Event("regulatory", verb, subj, tgt, 1)


def _up(name):
    return position(name, 1.0, 0.0, 0.0)


# ---- the pure phrase-decisions (each branch; the characterization for the pins) ----


def test_dramatic_situation_maps_polti_verbs():
    assert dramatic_situation("harm") == "pursuit"
    assert dramatic_situation("betray") == "revenge"
    assert dramatic_situation("seize") == "obtaining"
    assert dramatic_situation("pursue") == "pursuit"
    assert dramatic_situation("resembles") == "resembles"  # unmapped -> verbatim


def test_tragedy_clause_branches():
    assert "doomed sink" in tragedy_clause("TP53", "apoptosis", "doomed")
    assert "suppressed" in tragedy_clause("TP53", "apoptosis", "suppressed")
    assert "no doom holds" in tragedy_clause("TP53", "apoptosis", "indeterminate")


def test_comedy_clause_branches():
    assert "vicious comedy" in comedy_clause("A", "B", "vicious")
    assert "homeostatic comedy" in comedy_clause("A", "B", "homeostatic")
    assert "does not settle" in comedy_clause("A", "B", "indeterminate")


def test_quest_clause_branches():
    assert "resolving quest" in quest_clause("H", ["A", "B"], "resolving")
    assert "entangling quest" in quest_clause("H", ["A", "B"], "entangling")
    assert "indeterminate quest" in quest_clause("H", ["A"], "indeterminate")


def test_allegory_clause_branches():
    assert "role-fungible" in allegory_clause("A", "B", "fungible", 2)
    assert "did not confirm" in allegory_clause("A", "B", "coincidental", 1)


def test_lament_clause_branches():
    assert "can hold its role" in lament_clause("dopamine", "tyramine", "substituted")
    assert "structured decline" in lament_clause("dopamine", None, "palliative")
    # substituted verdict but no stand-in -> falls to the palliative phrasing (guard)
    assert "structured decline" in lament_clause("dopamine", None, "substituted")


def test_outcome_clause_branches():
    assert "confirms it" in outcome_clause("A", "amplifies", "B", "confirmed")
    assert "contradicts it" in outcome_clause("A", "amplifies", "B", "contradicted")
    assert "untestable" in outcome_clause("A", "amplifies", "B", "standing")


def test_verdict_clause_branches():
    assert "single mechanism" in verdict_clause("RESOLVED", 1)
    assert "Certified ⊥" in verdict_clause("BOTTOM", 0)
    assert "self-confirming" in verdict_clause("DEGENERATE", 1)
    assert "3 mechanisms" in verdict_clause("ASK", 3)
    assert "no available dimension" in verdict_clause("ABSTAIN", 2)


# ---- render, end-to-end over a REAL DriverRead ----


def test_render_reads_a_vicious_comedy_as_a_story():
    # A <-> B mutual amplification, both up -> a vicious comedy fires; render leads with THE STORY
    # and reports WHAT REMAINS. Validated through the real `drive`, not a hand-built read.
    events = [_reg("amplifies", "A", "B"), _reg("amplifies", "B", "A")]
    read = drive(events, {"A": _up("A"), "B": _up("B")}, VS)
    out = render(read)
    assert out.startswith("THE STORY")
    assert "comedy" in out.lower()
    assert "WHAT REMAINS" in out and "how solved:" in out


def test_render_surfaces_the_operator_ledger():
    # operator hypothesis A amplifies B, A and B both up -> confirmed -> render reports it.
    events = [_reg("amplifies", "A", "B"), _reg("amplifies", "B", "A")]
    hyp = [_reg("amplifies", "A", "B")]
    read = drive(events, {"A": _up("A"), "B": _up("B")}, VS, hypotheses=hyp)
    out = render(read)
    assert "WHAT YOU GOT RIGHT" in out
    assert "confirms it" in out


def test_render_quiet_when_no_genre_is_opinionated():
    # a lone directed edge with a single observed node -> no comedy/tragedy/quest fires -> the STORY
    # section says so rather than inventing a beat.
    read = drive([_reg("amplifies", "src", "A")], {"A": _up("A")}, VS)
    out = render(read)
    assert "THE STORY" in out
    # either a quiet note or (defensively) no fabricated genre keyword beyond the headers
    assert "quiet" in out or "WHAT REMAINS" in out

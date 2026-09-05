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
    # the clinic verdict CODES are lowercase ("resolved"/"abstain"/…) -- match those, not uppercase.
    assert "single mechanism" in verdict_clause("resolved", 1)
    assert "certified ⊥" in verdict_clause("bottom", 0)
    assert "self-confirming" in verdict_clause("degenerate", 1)
    assert "3 candidate mechanisms" in verdict_clause("ask", 3)
    assert "separable" in verdict_clause("abstain", 2)


# ---- render, end-to-end over a REAL DriverRead ----


def test_render_reads_a_vicious_comedy_as_a_story():
    # A <-> B mutual amplification, both up -> a vicious comedy fires; render leads with THE READ
    # and surfaces the {A,B} candidate mechanism with its story. Through the real `drive`.
    events = [_reg("amplifies", "A", "B"), _reg("amplifies", "B", "A")]
    read = drive(events, {"A": _up("A"), "B": _up("B")}, VS)
    out = render(read)
    assert out.startswith("THE READ")
    assert "CANDIDATE MECHANISMS" in out
    assert "comedy" in out.lower()


def test_render_surfaces_the_operator_ledger():
    # operator hypothesis A amplifies B, A and B both up -> confirmed -> render reports it.
    events = [_reg("amplifies", "A", "B"), _reg("amplifies", "B", "A")]
    hyp = [_reg("amplifies", "A", "B")]
    read = drive(events, {"A": _up("A"), "B": _up("B")}, VS, hypotheses=hyp)
    out = render(read)
    assert "WHAT YOU GOT RIGHT" in out
    assert "confirms it" in out


def test_render_quiet_when_no_genre_is_opinionated():
    # a lone directed edge with a single observed node -> no opinionated genre fires, but the read
    # is still legible (it does not invent a mechanism it cannot support).
    read = drive([_reg("amplifies", "src", "A")], {"A": _up("A")}, VS)
    out = render(read)
    assert out.startswith("THE READ")


def test_render_surfaces_a_resolving_quest_under_a_candidate():
    # source amplifies A and B (both up) -> the {source,A,B} mechanism reads as a resolving quest;
    # render exercises that quest beat under the candidate (the read renders cleanly either way).
    events = [_reg("amplifies", "source", "A"), _reg("amplifies", "source", "B")]
    out = render(drive(events, {"A": _up("A"), "B": _up("B")}, VS))
    assert out.startswith("THE READ") and "CANDIDATE MECHANISMS" in out


def test_render_groups_a_fungibility_allegory_into_the_mechanism():
    # GENE_A and GENE_B resemble each other AND both drive MARKER across two banks (regulatory +
    # physical) -> read_fungibility earns "fungible", and story_clusters groups that ALLEGORY into
    # the {GENE_A,GENE_B,MARKER} mechanism (the allegory branch of story_clusters).
    from homeostat.fungibility import read_fungibility

    events = [
        Event("evolutionary", "resembles", "GENE_A", "GENE_B", 1, ""),
        _reg("amplifies", "GENE_A", "MARKER"),
        _reg("amplifies", "GENE_B", "MARKER"),
        Event("physical", "binds", "GENE_A", "MARKER", 1),
        Event("physical", "binds", "GENE_B", "MARKER", 1),
    ]
    assert any(f.verdict == "fungible" for f in read_fungibility(events))  # earned from geometry
    assert render(drive(events, {"MARKER": _up("MARKER")}, VS)).startswith("THE READ")


def test_render_names_the_elimination_probe_when_stuck():
    # two directed sources both amplify S (S observed up); neither is eliminated -> a stuck
    # plurality. A probe reading oppositely on A vs B separates them -> render names the measure.
    from homeostat.jeeves import Probe

    events = [_reg("amplifies", "A", "S"), _reg("amplifies", "B", "S")]
    probe = Probe("marker", "confirm", {"A": 1, "B": -1, "S": 0})
    out = render(drive(events, {"S": _up("S")}, VS, probes=[probe]))
    assert "WHAT I CAN'T YET TELL" in out  # the counter-ask (i_solve or the elimination probe)


def test_render_bounds_a_many_mechanism_tie_and_names_the_measurement():
    # seven independent mutual-amplification pairs, all observed up -> seven candidate mechanisms
    # tie on coverage. render BOUNDS the set (top-K + "… and N more") rather than dumping the wall,
    # and fires the counter-ask (the mechanism-Jeeves / probe measurement that would separate them).
    events, pos = [], {}
    for i in range(7):
        a, b = f"A{i}", f"B{i}"
        events += [_reg("amplifies", a, b), _reg("amplifies", b, a)]
        pos[a], pos[b] = _up(a), _up(b)
    out = render(drive(events, pos, VS))
    assert "more that partially explain" in out  # the bounded-set tail (top-K exceeded)
    assert "WHAT I CAN'T YET TELL" in out  # the counter-ask fires

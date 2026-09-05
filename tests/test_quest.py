"""Intent tests for the Epic Quest genre — the roundabout resolution read as Kuramoto coherence.
Authored from the design (THESIS ch.9 / STORY_LAYER §3); the pure decisions are Detective-pinned."""

import pytest

from homeostat.event import Event
from homeostat.otp import OPPOSE, ORTHOGONAL, SUPPORT
from homeostat.quest import order_parameter, part_vector, quest_verdict, read_quest


def _amp(u, v):
    return Event("regulatory", "amplifies", u, v, 1)


def _inh(u, v):
    return Event("regulatory", "inhibits", u, v, 1)


# ---- part_vector: the OTP ternary -> phasor embedding ------------------------------


def test_part_vector_support_is_in_phase():
    x, y = part_vector(SUPPORT, 0, 0)
    assert x == pytest.approx(1.0)
    assert y == pytest.approx(0.0)


def test_part_vector_oppose_is_antiphase():
    # inhibition -> angle pi -> the real -1 axis (so support + oppose destructively cancel).
    x, y = part_vector(OPPOSE, 0, 0)
    assert x == pytest.approx(-1.0)
    assert y == pytest.approx(0.0)


def test_part_vector_orthogonal_is_the_zero_vector():
    # the informational zero is NO phasor: no opinion neither reinforces nor cancels.
    assert part_vector(ORTHOGONAL, 0, 0) == (0.0, 0.0)
    assert part_vector(ORTHOGONAL, 3, 5) == (0.0, 0.0)  # depth is irrelevant to a non-opinion


def test_part_vector_depth_rotates_on_the_ordered_ring():
    # same sign, half the ring away (depth = max_depth/2) -> antiphase (the ring is ordered).
    x, y = part_vector(SUPPORT, 1, 2)  # rotation 2*pi*1/2 = pi
    assert x == pytest.approx(-1.0)
    assert y == pytest.approx(0.0, abs=1e-9)


# ---- order_parameter: the Kuramoto coherence, transported -------------------------


def test_order_parameter_aligned_is_fully_coherent():
    assert order_parameter([(1.0, 0.0), (1.0, 0.0)]) == pytest.approx(1.0)


def test_order_parameter_opposed_destructively_cancels():
    # the elegance: opposing phasors SUBTRACT -> r = 0 (destructive interference from addition).
    assert order_parameter([(1.0, 0.0), (-1.0, 0.0)]) == pytest.approx(0.0)


def test_order_parameter_zero_vectors_are_no_coherence_not_false_coherence():
    # all informational zeros -> r = 0 (NOT 1: the zero-vector fix -- abstention is not synchrony).
    assert order_parameter([(0.0, 0.0), (0.0, 0.0)]) == pytest.approx(0.0)


def test_order_parameter_one_opinion_one_abstain_is_diluted():
    # a zero vector adds nothing but still COUNTS in N -> one opinion among two parts -> r = 0.5.
    assert order_parameter([(1.0, 0.0), (0.0, 0.0)]) == pytest.approx(0.5)


def test_order_parameter_empty_is_zero():
    assert order_parameter([]) == 0.0


# ---- quest_verdict: opinions-exist distinguishes entangling from indeterminate ----


def test_quest_verdict_no_opinions_is_indeterminate():
    # every joined part the informational zero -> no coherence axis (abstention, not a low score).
    assert quest_verdict(0.0, 0.5, opinionated=0) == "indeterminate"


def test_quest_verdict_locked_is_resolving():
    assert quest_verdict(0.9, 0.5, opinionated=2) == "resolving"
    assert quest_verdict(0.5, 0.5, opinionated=2) == "resolving"  # boundary: >= floor


def test_quest_verdict_destructive_cancellation_is_entangling_not_indeterminate():
    # opinions EXIST but cancel (r=0) -> a real connection that does not resolve -- NOT abstention.
    assert quest_verdict(0.0, 0.5, opinionated=2) == "entangling"


# ---- read_quest: the composed read over the observed shadow ------------------------


def test_read_quest_a_distant_bridge_that_coheres_is_resolving():
    # H reaches two disjoint observed (A, B), both amplified -> in phase -> a coherent roundabout.
    quests = read_quest([_amp("H", "A"), _amp("H", "B")], observed=["A", "B"])
    assert len(quests) == 1
    q = quests[0]
    assert q.hero == "H"
    assert q.joined == ("A", "B")
    assert q.verdict == "resolving"
    assert q.coherence == pytest.approx(1.0)


def test_read_quest_a_bridge_with_opposing_signs_is_entangling():
    # H amplifies A but inhibits B -> antiphase -> destructive -> couples but does not resolve.
    quests = read_quest([_amp("H", "A"), _inh("H", "B")], observed=["A", "B"])
    assert len(quests) == 1
    assert quests[0].verdict == "entangling"


def test_read_quest_declines_a_hero_reaching_fewer_than_two_observed():
    assert read_quest([_amp("H", "A"), _amp("H", "X")], observed=["A"]) == []


def test_read_quest_declines_when_the_parts_are_connected_without_the_hero():
    # A and B already connected (A->B) -> H is not the sole bridge -> not a roundabout quest.
    ev = [_amp("H", "A"), _amp("H", "B"), _amp("A", "B")]
    assert read_quest(ev, observed=["A", "B"]) == []


def test_read_quest_hero_must_be_distant_not_one_of_the_observed():
    # every node is phenotype-adjacent (observed) -> no DISTANT hero -> no quest.
    assert read_quest([_amp("A", "B"), _amp("A", "C")], observed=["A", "B", "C"]) == []

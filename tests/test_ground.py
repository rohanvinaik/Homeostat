"""Intent tests for the front door — ground-or-abstain symptom resolution. Authored from the design
(SymbolicSpellCheck's non-destruction law), not generated."""

from homeostat.ground import Resolution, edit_within_1, ground, is_opaque

VOCAB = {"pots": "POTS", "postural orthostatic tachycardia syndrome": "POTS", "narcolepsy": "NARC"}


# ---- pure decisions --------------------------------------------------------------


def test_edit_within_1():
    assert edit_within_1("pots", "pots") is True  # equal
    assert edit_within_1("pods", "pots") is True  # substitution
    assert edit_within_1("ptos", "pots") is True  # adjacent transposition
    assert edit_within_1("spots", "pots") is True  # deletion (the dangerous one — 1 edit apart!)
    assert edit_within_1("poats", "pots") is True  # insertion
    assert edit_within_1("cat", "dog") is False  # far
    assert edit_within_1("abcd", "badc") is False  # two transpositions, not 1 edit
    assert edit_within_1("axb", "bxa") is False  # swapped chars but NON-adjacent → 2 edits
    assert edit_within_1("ab", "bc") is False  # adjacent diffs, only the 2nd half of a swap holds
    assert edit_within_1("ab", "ca") is False  # adjacent diffs, only the 1st half of a swap holds


def test_is_opaque_shape_gate():
    assert is_opaque("POTS") is True  # acronym
    assert is_opaque("HLA-B27") is True  # code (hyphen)
    assert is_opaque("mast-cell") is True  # hyphen alone (no digit to short-circuit on)
    assert is_opaque("rs1873613") is True  # code (digits)
    assert is_opaque("narcolepsy") is False  # ordinary word
    assert is_opaque("a") is False  # too short


# ---- the door: the disaster is designed out --------------------------------------


def test_spots_never_becomes_pots_without_a_validity_dict():
    # "spots" is one deletion from "pots" — a naive typo leg would recommit the original disaster.
    r = ground("spots", VOCAB)  # no valid_words → typo leg withheld
    assert r.node is None  # NOT committed to POTS
    assert "withheld" in r.reason


def test_spots_never_becomes_pots_with_the_validity_guard():
    # With the validity dictionary, "spots" is a real word → left untouched, never rewritten.
    r = ground("spots", VOCAB, valid_words={"spots", "the"})
    assert r.node is None
    assert "untouched" in r.reason


def test_exact_acronym_grounds():
    assert ground("POTS", VOCAB).node == "POTS"  # normalizes to "pots", exact match
    assert ground("Postural Orthostatic Tachycardia Syndrome", VOCAB).node == "POTS"  # exact alias


def test_ordinary_typo_grounds_only_when_guarded():
    # a real misspelling of a symptom, with the validity guard supplied
    r = ground("narcolepsyy", VOCAB, valid_words={"the", "dog"})
    assert r.node == "NARC"
    assert "typo" in r.reason


def test_acronym_typo_is_offered_never_committed():
    # "PTOS" is a transposition of "POTS" but an acronym shape → offered, never auto-rewritten
    r = ground("PTOS", VOCAB, valid_words={"the"})
    assert r.node is None
    assert r.offered == ("POTS",)
    assert "offered" in r.reason


def test_ambiguous_typo_abstains_with_offers():
    r = ground("cat", {"bat": "BAT", "car": "CAR"}, valid_words={"the"})
    assert r.node is None  # two grounded candidates → abstain
    assert set(r.offered) == {"BAT", "CAR"}


def test_unknown_symptom_abstains_cleanly():
    r = ground("zzzzz", VOCAB, valid_words={"the"})
    assert isinstance(r, Resolution)
    assert r.node is None
    assert r.offered == ()
    assert "node-birth" in r.reason

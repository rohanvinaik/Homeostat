"""Targeted abstain-branch tests — the malformed/short/degenerate inputs the happy-path suites do
not reach. Each pins a documented `-> None` / skip / else branch of a pure decision. Authored from
intent (a bank renderer abstains on a malformed row; a too-short row is skipped), not generated."""

from __future__ import annotations

import json

from homeostat import homology, signor, string, structural, trait_wiring, util


def test_homology_row_to_event_abstains_on_a_short_row():
    # fewer than the required columns -> None (never an IndexError on a truncated Compara line).
    assert homology.row_to_event([], {}) is None


def test_signor_row_to_event_abstains_on_a_short_row():
    assert signor.row_to_event([]) is None  # SIGNOR uses gene symbols directly -- no alias arg


def test_string_row_to_event_abstains_on_non_integer_evidence():
    # long enough to clear the column guard, but the evidence columns are non-numeric -> ValueError
    # is caught and the row abstains (a malformed STRING line never crashes the stream).
    assert string.row_to_event(["x"] * 24, {}) is None


def test_trait_wiring_skips_a_row_too_short_for_the_trait_column():
    # a row without the MAPPED_TRAIT column is skipped, not indexed into (no IndexError).
    assert trait_wiring.trait_wiring([["x"]]) == {}


def test_structural_composition_stats_abstain_to_zero_on_empty_sequence():
    # no residues to average over -> 0.0, never a ZeroDivision on an empty protein.
    assert structural.gravy("") == 0.0
    assert structural.aromaticity("") == 0.0
    assert structural.net_charge("") == 0.0


def test_atomic_write_json_roundtrips(tmp_path):
    p = tmp_path / "out.json"
    util.atomic_write_json(p, {"b": 2, "a": 1})
    assert json.loads(p.read_text()) == {"a": 1, "b": 2}  # sorted keys, atomically replaced

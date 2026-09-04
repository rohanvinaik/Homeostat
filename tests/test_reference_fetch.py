"""Intent + integration tests for the HMDB reference-range shell. Pure decisions (parse_interval,
is_normal, age_bucket, hmdb_age_bucket) are paired with the Detective characterization; the I/O half
(load_serum / ensure / make_reference) is exercised on a tiny synthetic serum XML fixture.
"""

import zipfile

import pytest

from homeostat.reference_fetch import (
    age_bucket,
    ensure,
    hmdb_age_bucket,
    is_normal,
    load_serum,
    make_reference,
    parse_interval,
)


def test_parse_interval_mean_sd_becomes_k_sd_band():
    assert parse_interval("10 +/- 2", 2.0) == (6.0, 14.0)  # mean 10 +/- 2 SD
    assert parse_interval("10 +/- 2", 1.0) == (8.0, 12.0)  # k=1 -> +/- 1 SD


def test_parse_interval_explicit_range_used_directly():
    assert parse_interval("4.0-6.0", 2.0) == (4.0, 6.0)  # bare range = a given interval
    assert parse_interval("5.0 (4.0-6.0)", 2.0) == (4.0, 6.0)  # parenthetical range
    assert parse_interval("5.0(4.0-6.0)", 2.0) == (4.0, 6.0)


def test_parse_interval_abstains_on_unpinnable_forms():
    assert parse_interval("5.0", 2.0) is None  # bare value -> no spread
    assert parse_interval("5.0 (0.5)", 2.0) is None  # value + unclear parenthetical
    assert parse_interval("<5.0", 2.0) is None  # less-than
    assert parse_interval("6.0-4.0", 2.0) is None  # degenerate (low >= high)
    assert parse_interval("", 2.0) is None


def test_is_normal_only_the_healthy_baseline():
    assert is_normal("Normal") is True
    assert is_normal("normal") is True  # the lowercase variant
    assert is_normal(" Normal ") is True
    assert is_normal("Taking drug identified by DrugBank entry X") is False
    assert is_normal("") is False


def test_age_bucket_follows_hmdb_boundaries():
    assert age_bucket(0.05) == "newborn"  # < 30 days
    assert age_bucket(0.5) == "infant"  # < 1 year
    assert age_bucket(5.0) == "children"
    assert age_bucket(15.0) == "adolescent"
    assert age_bucket(40.0) == "adult"


def test_hmdb_age_bucket_normalizes_to_the_same_buckets():
    assert hmdb_age_bucket("Adult (>18 years old)") == "adult"
    assert hmdb_age_bucket("Children (1 - 13 years old)") == "children"  # spacing variant
    assert hmdb_age_bucket("Newborn (0-30 days old)") == "newborn"
    assert hmdb_age_bucket("Not Specified") == "not"  # matches no numeric bucket
    assert hmdb_age_bucket("") == "unspecified"


# ---- the I/O half, on a synthetic serum XML fixture -------------------------------

_FIXTURE = (
    '<?xml version="1.0"?><hmdb xmlns="http://www.hmdb.ca">'
    "<metabolite><name>D-Glucose</name><normal_concentrations>"
    "<concentration><biospecimen>Blood</biospecimen>"
    "<concentration_value>5.0 +/- 0.5</concentration_value>"
    "<subject_age>Adult (&gt;18 years old)</subject_age><subject_sex>Both</subject_sex>"
    "<subject_condition>Normal</subject_condition></concentration>"
    "<concentration><biospecimen>Blood</biospecimen>"
    "<concentration_value>9.9 +/- 9.9</concentration_value>"  # a 2nd study -> ignored (first-wins)
    "<subject_age>Adult (&gt;18 years old)</subject_age><subject_sex>Both</subject_sex>"
    "<subject_condition>Normal</subject_condition></concentration>"
    "<concentration><biospecimen>Blood</biospecimen>"
    "<concentration_value>2.0 +/- 0.1</concentration_value>"  # a DISEASE study -> excluded
    "<subject_age>Adult (&gt;18 years old)</subject_age><subject_sex>Both</subject_sex>"
    "<subject_condition>Diabetic</subject_condition></concentration>"
    "</normal_concentrations></metabolite></hmdb>"
)


def _fixture_zip(tmp_path):
    z = tmp_path / "serum.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("serum_metabolites.xml", _FIXTURE)
    return z


def test_load_serum_takes_first_normal_study_never_aggregates(tmp_path):
    table = load_serum(_fixture_zip(tmp_path))
    # first Normal study (5.0 +/- 0.5 -> +/-2SD); the 2nd Normal study and the Diabetic one ignored.
    assert table[("d-glucose", "both", "adult")] == (4.0, 6.0)


def test_make_reference_matches_with_sex_fallback_and_abstains(tmp_path):
    ref = make_reference(load_serum(_fixture_zip(tmp_path)))
    assert ref("D-Glucose", {"sex": "Male", "age": "40"}) == (4.0, 6.0)  # no Male -> falls to Both
    assert ref("unknown-marker", {"age": "40"}) is None  # no metabolite -> abstain


def test_ensure_is_parse_local_never_downloads(tmp_path):
    with pytest.raises(FileNotFoundError, match="Cloudflare-gated"):
        ensure(tmp_path / "nope.zip")
    present = tmp_path / "serum.zip"
    present.write_bytes(b"x")
    assert ensure(present) == present

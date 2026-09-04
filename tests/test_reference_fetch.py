"""Intent tests for the HMDB reference-range shell's pure decisions: `parse_interval` (value string
-> [low, high] or abstain), `is_normal`, `age_bucket`, `hmdb_age_bucket`. Paired with the Detective
characterization per the two-step. None/abstain cases are isolated from value assertions.
"""

from homeostat.reference_fetch import age_bucket, hmdb_age_bucket, is_normal, parse_interval


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

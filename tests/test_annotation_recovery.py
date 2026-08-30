"""Intent tests for the §3.2 annotation-recovery validator — authored from what
the test MUST do, not characterized from what the code happens to do."""

import random

from homeostat.annotation_recovery import (
    eligible_matches,
    load_pleiotropy,
    matched_null_test,
)


def _scores(rows):
    # gene -> (degree, participation, pbs_weight, p)
    return {g: (d, part, pbs, p) for g, d, part, pbs, p in rows}


def test_matching_respects_degree_and_pbs_bands():
    scores = _scores(
        [
            ("C", 100, 0.5, 0.05, 0.01),  # candidate
            ("G_ok", 110, 0.1, 0.06, 0.5),  # in both bands
            ("G_degoff", 50, 0.1, 0.06, 0.5),  # degree out of ±20%
            ("G_pbsoff", 105, 0.1, 0.30, 0.5),  # pbs out of ±0.02
        ]
    )
    elig = eligible_matches(["C"], ["G_ok", "G_degoff", "G_pbsoff"], scores)
    assert elig["C"] == ["G_ok"]


def test_enrichment_detected_when_candidates_carry_more_signal():
    # candidate has high pleiotropy; matched background all zero -> strong, p small.
    scores = _scores(
        [("C", 10, 0.5, 0.05, 0.01)] + [(f"B{i}", 10, 0.1, 0.05, 0.9) for i in range(50)]
    )
    annotation = {"C": 20.0}  # background genes default to 0.0
    res = matched_null_test(
        ["C"],
        eligible_matches(["C"], [f"B{i}" for i in range(50)], scores),
        annotation,
        1000,
        random.Random(0),
    )
    assert res["observed_mean"] == 20.0
    assert res["null_mean_avg"] == 0.0
    assert res["p"] < 0.05  # candidate strictly exceeds every null draw


def test_null_when_candidate_matches_background():
    # candidate annotation equals what the background carries -> not enriched.
    scores = _scores(
        [("C", 10, 0.5, 0.05, 0.01)] + [(f"B{i}", 10, 0.1, 0.05, 0.9) for i in range(50)]
    )
    annotation = {"C": 3.0, **{f"B{i}": 3.0 for i in range(50)}}
    res = matched_null_test(
        ["C"],
        eligible_matches(["C"], [f"B{i}" for i in range(50)], scores),
        annotation,
        1000,
        random.Random(0),
    )
    assert res["observed_mean"] == 3.0
    assert res["p"] > 0.05  # every null draw ties -> p == 1.0 by add-one


def test_candidate_with_no_match_is_dropped_not_forced():
    scores = _scores([("C", 100, 0.5, 0.05, 0.01), ("B", 10, 0.1, 0.05, 0.9)])
    res = matched_null_test(
        ["C"], eligible_matches(["C"], ["B"], scores), {"C": 5.0}, 100, random.Random(0)
    )
    assert res["n_dropped_no_match"] == 1
    assert res["error"] == "no evaluable candidates"


def test_load_pleiotropy_counts_distinct_uris_and_splits_genes(tmp_path):
    tsv = tmp_path / "gwas.tsv"
    tsv.write_text(
        "MAPPED_GENE\tMAPPED_TRAIT_URI\n"
        "GENEA\thttp://efo/EFO_1\n"
        "GENEA\thttp://efo/EFO_2\n"
        "GENEA\thttp://efo/EFO_1\n"  # duplicate URI -> not double-counted
        "GENEB - GENEC\thttp://efo/EFO_9\n"  # intergenic split
        "GENED, GENEE\thttp://efo/EFO_3, http://efo/EFO_4\n",  # multi-gene, multi-uri
        encoding="utf-8",
    )
    p = load_pleiotropy(tsv)
    assert p["GENEA"] == 2  # EFO_1, EFO_2 distinct
    assert p["GENEB"] == 1 and p["GENEC"] == 1  # both flanks credited
    assert p["GENED"] == 2 and p["GENEE"] == 2  # both genes, both URIs

"""End-to-end §7 pile build on a synthetic Pan-UKBB-shaped file: real PBS math,
tiny data. Confirms the population-differential ranking and the polymorphic /
missing-AF filtering, with no p-value or annotation anywhere in the object."""

import gzip

from homeostat import eir_cohort, paths


def _write_src(tmp_path, rows):
    p = tmp_path / "src.tsv.bgz"
    header = "chr\tpos\tref\talt\taf_EUR\taf_CSA\taf_EAS\n"
    with gzip.open(p, "wt") as f:
        f.write(header)
        for r in rows:
            f.write("\t".join(str(x) for x in r) + "\n")
    return p


def test_pile_ranks_by_csa_divergence(tmp_path, monkeypatch):
    monkeypatch.setattr(paths, "EIR", tmp_path)
    monkeypatch.setattr(eir_cohort, "PILE", tmp_path / "pile.tsv.gz")
    monkeypatch.setattr(eir_cohort, "SUMMARY", tmp_path / "summary.json")
    src = _write_src(
        tmp_path,
        [
            # CSA strongly diverged from EUR/EAS -> high PBS (the pile leader)
            ("1", 100, "A", "G", 0.10, 0.90, 0.12),
            # CSA sits with EUR/EAS -> low/negative PBS
            ("1", 200, "A", "G", 0.50, 0.52, 0.50),
            # AF missing -> skipped
            ("1", 300, "A", "G", "NA", 0.4, 0.4),
            # monomorphic in CSA and EUR -> skipped
            ("1", 400, "A", "G", 0.0, 0.0, 0.3),
        ],
    )
    result = eir_cohort.build(str(src))
    assert result["counts"]["written"] == 2
    assert result["counts"]["af_missing"] == 1
    assert result["counts"]["monomorphic"] == 1
    # The diverged variant leads the PBS ranking.
    assert result["top30_by_pbs"][0]["pos"] == 100
    assert result["top30_by_pbs"][0]["pbs"] > result["top30_by_pbs"][1]["pbs"]

    with gzip.open(tmp_path / "pile.tsv.gz", "rt") as f:
        lines = f.read().splitlines()
    assert lines[0].startswith("chrom\tpos")
    assert len(lines) == 3  # header + 2 variants

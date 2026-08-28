"""End-to-end §13.1 on a synthetic fixture: real scan + real rank, tiny data.

Exercises the actual streaming join and ranking (not internals): matching,
skip-counting, chromosome finalization, early stop after the last autosome,
crash-resume via done-markers, and the §7.1 ordering of the output queue.
"""

import gzip
import json

import pytest

from homeostat import genotype, paths, rank, scan

VCF_HEADER = "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n"


def _info(eur, sas, eas=0.5, afr=0.5, amr=0.5):
    return (
        f"AC=1;AF=0.5;AN=5008;EAS_AF={eas};AMR_AF={amr};AFR_AF={afr}"
        f";EUR_AF={eur};SAS_AF={sas};VT=SNP"
    )


@pytest.fixture
def fixture_paths(tmp_path, monkeypatch):
    """Repoint every artifact path at tmp_path and build the synthetic inputs."""
    monkeypatch.setattr(paths, "AUTOSOMES", ["1", "2"])
    monkeypatch.setattr(scan, "AUTOSOMES", ["1", "2"])
    monkeypatch.setattr(rank, "AUTOSOMES", ["1", "2"])
    monkeypatch.setattr(paths, "SHARDS", tmp_path / "shards")
    monkeypatch.setattr(paths, "SCAN_PROGRESS", tmp_path / "scan_progress.json")
    monkeypatch.setattr(paths, "SITES_VCF", tmp_path / "sites.vcf.gz")
    monkeypatch.setattr(paths, "CANDIDATES", tmp_path / "candidates.tsv.gz")
    monkeypatch.setattr(paths, "SUMMARY", tmp_path / "summary.json")

    export = tmp_path / "genome.txt"
    export.write_text(
        "# comment\n"
        "rs_hit2\t1\t100\tGG\n"  # SAS-shifted alt G, R homozygous alt -> top
        "rs_hit0\t1\t200\tAA\n"  # SAS-shifted alt G, R matches EUR -> priority 0
        "rs_mism\t1\t300\tTT\n"  # alleles disagree with VCF A/G -> skipped
        "rs_nocall\t1\t400\t--\n"  # no-call -> dropped at parse
        "rs_hit1\t2\t100\tAG\n"  # SAS-shifted alt G, R heterozygous -> middle
        "rs_x\tX\t100\tAA\n"  # non-autosomal -> dropped at parse
    )

    vcf_lines = [
        VCF_HEADER,
        f"1\t100\trs_hit2\tA\tG\t100\tPASS\t{_info(0.1, 0.9)}\n",
        f"1\t200\trs_hit0\tA\tG\t100\tPASS\t{_info(0.1, 0.9)}\n",
        "1\t250\trs_multi\tA\tG,T\t100\tPASS\tAC=1,1\n",  # multiallelic
        f"1\t260\trs_indel\tAT\tA\t100\tPASS\t{_info(0.1, 0.2)}\n",  # non-SNP
        f"1\t300\trs_mism\tA\tG\t100\tPASS\t{_info(0.1, 0.9)}\n",
        f"2\t100\trs_hit1\tA\tG\t100\tPASS\t{_info(0.1, 0.9)}\n",
        f"X\t100\trs_x\tA\tG\t100\tPASS\t{_info(0.1, 0.9)}\n",
    ]
    with gzip.open(tmp_path / "sites.vcf.gz", "wt") as f:
        f.writelines(vcf_lines)
    return tmp_path, export


def test_scan_and_rank_end_to_end(fixture_paths):
    tmp_path, export = fixture_paths
    r_index, counts = genotype.parse_export(export)
    assert counts["kept"] == 4
    assert counts["no_call"] == 1
    assert counts["non_autosomal"] == 1

    scan.scan(r_index)
    assert scan.done_chroms() == ["1", "2"]
    chr1 = json.loads((tmp_path / "shards" / "chr1.done").read_text())
    assert chr1["matched"] == 2
    assert chr1["multiallelic_skipped"] == 1
    assert chr1["non_snp_skipped"] == 1
    assert chr1["allele_mismatch_skipped"] == 1
    # Early stop: the trailing X contig must not have produced a shard.
    assert not (tmp_path / "shards" / "chrX.tsv").exists()

    summary = rank.rank(counts, "deadbeef")
    assert summary["candidates_total"] == 3
    assert summary["candidates_priority_gt0"] == 2

    with gzip.open(tmp_path / "candidates.tsv.gz", "rt") as f:
        rows = [line.split("\t") for line in f.read().splitlines()[1:]]
    # §7.1 ordering: R-matches-I homozygote > heterozygote > R-matches-E (zero).
    assert [r[8] for r in rows] == ["rs_hit2", "rs_hit1", "rs_hit0"]
    assert float(rows[0][0]) == pytest.approx(2 * float(rows[1][0]), rel=1e-6)
    assert float(rows[2][0]) == 0.0


def test_scan_resumes_from_done_markers(fixture_paths):
    tmp_path, export = fixture_paths
    r_index, _ = genotype.parse_export(export)
    scan.scan(r_index)
    # Simulate a crash that lost chr2's marker: only chr2 should be rebuilt.
    (tmp_path / "shards" / "chr2.done").unlink()
    (tmp_path / "shards" / "chr2.tsv").unlink()
    chr1_mtime = (tmp_path / "shards" / "chr1.tsv").stat().st_mtime_ns
    scan.scan(r_index)
    assert scan.done_chroms() == ["1", "2"]
    assert (tmp_path / "shards" / "chr2.tsv").exists()
    assert (tmp_path / "shards" / "chr1.tsv").stat().st_mtime_ns == chr1_mtime


def test_scan_noop_when_all_done(fixture_paths):
    tmp_path, export = fixture_paths
    r_index, _ = genotype.parse_export(export)
    scan.scan(r_index)
    progress_before = (tmp_path / "scan_progress.json").read_text()
    scan.scan(r_index)  # must return without touching anything
    assert (tmp_path / "scan_progress.json").read_text() == progress_before

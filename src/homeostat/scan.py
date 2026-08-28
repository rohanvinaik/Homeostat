"""Stream the 1000G sites VCF and join it against R's array sites.

Restartability: one shard per chromosome, finalized (tmp -> rename + .done
marker with counts) the moment the stream leaves that chromosome. On restart,
chromosomes with a .done marker are fast-forwarded — a crash costs at most the
decompress-skip time, and no partial shard is ever visible under its final name.
"""

import datetime
import gzip
import os

from homeostat import paths
from homeostat.paths import AUTOSOMES
from homeostat.util import atomic_write_json

SHARD_HEADER = (
    "chrom\tpos\trsid_r\trsid_kg\tref\talt\tgenotype_r"
    "\taf_eur\taf_sas\taf_eas\taf_afr\taf_amr\tambiguous_strand\tfilter\n"
)
BASES = frozenset("ACGT")
AMBIGUOUS_PAIRS = ({"A", "T"}, {"C", "G"})
PROGRESS_EVERY = 2_000_000  # lines between progress-file updates


def _info_af(info: str, key: str) -> str:
    start = info.find(key + "=")
    if start < 0:
        return ""
    start += len(key) + 1
    end = info.find(";", start)
    return info[start:] if end < 0 else info[start:end]


def _write_progress(lines: int, chrom: str, matched: int, done: list[str]) -> None:
    atomic_write_json(
        paths.SCAN_PROGRESS,
        {
            "lines_scanned": lines,
            "current_chrom": chrom,
            "matched_total": matched,
            "chroms_done": done,
            "updated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        },
    )


class _Shard:
    """One chromosome's output file, written to .tmp and finalized atomically."""

    def __init__(self, chrom: str):
        self.chrom = chrom
        self.path = paths.SHARDS / f"chr{chrom}.tsv"
        self.tmp = paths.SHARDS / f"chr{chrom}.tsv.tmp"
        # noqa rationale: the handle outlives this scope by design — the shard
        # stays open across the streaming loop and closes in finalize().
        self.handle = open(self.tmp, "w", encoding="utf-8")  # noqa: SIM115
        self.handle.write(SHARD_HEADER)
        self.counts = {
            "kg_biallelic_snps_seen": 0,
            "matched": 0,
            "multiallelic_skipped": 0,
            "non_snp_skipped": 0,
            "allele_mismatch_skipped": 0,
            "ambiguous_strand_kept": 0,
        }

    def finalize(self) -> None:
        self.handle.close()
        os.replace(self.tmp, self.path)
        atomic_write_json(paths.SHARDS / f"chr{self.chrom}.done", self.counts)


def done_chroms() -> list[str]:
    return [c for c in AUTOSOMES if (paths.SHARDS / f"chr{c}.done").exists()]


def scan(r_index: dict[str, dict[int, tuple[str, str]]]) -> None:
    """Single pass over the sites VCF; resumable at chromosome granularity."""
    paths.SHARDS.mkdir(parents=True, exist_ok=True)
    done = set(done_chroms())
    if len(done) == len(AUTOSOMES):
        return
    matched_total = 0
    lines = 0
    shard: _Shard | None = None
    current: str | None = None

    with gzip.open(paths.SITES_VCF, "rt", encoding="utf-8") as f:
        for line in f:
            lines += 1
            if lines % PROGRESS_EVERY == 0:
                _write_progress(lines, current or "?", matched_total, sorted(done))
            if line.startswith("#"):
                continue
            chrom, _, rest = line.partition("\t")
            if chrom != current:
                if shard is not None:
                    shard.finalize()
                    done.add(shard.chrom)
                    shard = None
                current = chrom
                if len(done) == len(AUTOSOMES):
                    break  # all autosomes finalized; trailing contigs irrelevant
                if chrom in done or chrom not in r_index:
                    pass  # fast-forward this chromosome
                else:
                    shard = _Shard(chrom)
            if shard is None:
                continue

            pos_s, _, rest = rest.partition("\t")
            rsid_kg, _, rest = rest.partition("\t")
            ref, _, rest = rest.partition("\t")
            alt, _, rest = rest.partition("\t")
            if "," in alt:
                shard.counts["multiallelic_skipped"] += 1
                continue
            if len(ref) != 1 or len(alt) != 1 or ref not in BASES or alt not in BASES:
                shard.counts["non_snp_skipped"] += 1
                continue
            shard.counts["kg_biallelic_snps_seen"] += 1
            hit = r_index[chrom].get(int(pos_s))
            if hit is None:
                continue
            rsid_r, genotype = hit
            alleles = {ref, alt}
            if any(a not in alleles for a in genotype):
                shard.counts["allele_mismatch_skipped"] += 1
                continue
            _qual, _, rest = rest.partition("\t")
            filt, _, info = rest.partition("\t")
            ambiguous = alleles in AMBIGUOUS_PAIRS
            if ambiguous:
                shard.counts["ambiguous_strand_kept"] += 1
            shard.handle.write(
                f"{chrom}\t{pos_s}\t{rsid_r}\t{rsid_kg}\t{ref}\t{alt}\t{genotype}"
                f"\t{_info_af(info, 'EUR_AF')}\t{_info_af(info, 'SAS_AF')}"
                f"\t{_info_af(info, 'EAS_AF')}\t{_info_af(info, 'AFR_AF')}"
                f"\t{_info_af(info, 'AMR_AF')}\t{int(ambiguous)}\t{filt}\n"
            )
            shard.counts["matched"] += 1
            matched_total += 1

    if shard is not None:
        shard.finalize()
        done.add(shard.chrom)
    _write_progress(lines, "complete", matched_total, sorted(done))

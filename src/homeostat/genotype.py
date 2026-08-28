"""Parse the raw 23andMe v5 export (build 37, plus-strand, tab-separated).

Directly-observed tier only (checkpoint §11.5): this reads the raw array
export, never the promethease report layer.
"""

from pathlib import Path

from homeostat.paths import AUTOSOMES

VALID_BASES = frozenset("ACGT")


def parse_export(path: Path) -> tuple[dict[str, dict[int, tuple[str, str]]], dict[str, int]]:
    """Parse the export into {chrom: {pos: (rsid, genotype)}} plus skip-counts.

    Keeps autosomal, diploid, ACGT-only calls. Everything dropped is counted,
    never silently truncated: no-calls (--), indel calls (II/DD/DI), hemizygous
    or non-diploid strings, and non-autosomal chromosomes (X/Y/MT).
    """
    index: dict[str, dict[int, tuple[str, str]]] = {c: {} for c in AUTOSOMES}
    counts = {
        "total": 0,
        "kept": 0,
        "no_call": 0,
        "indel_call": 0,
        "non_diploid_or_nonbase": 0,
        "non_autosomal": 0,
    }
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            fields = line.rstrip("\n").split("\t")
            if len(fields) != 4:
                continue
            rsid, chrom, pos, genotype = fields
            counts["total"] += 1
            if chrom not in index:
                counts["non_autosomal"] += 1
                continue
            if genotype == "--":
                counts["no_call"] += 1
                continue
            if any(a in "IDN" for a in genotype):
                counts["indel_call"] += 1
                continue
            if len(genotype) != 2 or any(a not in VALID_BASES for a in genotype):
                counts["non_diploid_or_nonbase"] += 1
                continue
            index[chrom][int(pos)] = (rsid, genotype)
            counts["kept"] += 1
    return index, counts

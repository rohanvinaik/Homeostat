"""Reproducible sourcing of the §13.4 trait gene sets from the GWAS Catalog
bulk associations file.

Why the bulk file and not the query endpoint: the /gwas/api/search/downloads
Solr endpoint threw a server-side Tomcat exception during this work
(2026-08-28); the FTP bulk release is the SAME primary source via a working
code path. Filter is by MAPPED_TRAIT (the EFO-mapped trait), EXACT single-trait
match — see `trait_matches`. Run: make gwas-extract.
"""

import csv
import sys

from homeostat.ensemble import TRAITS

# Exact EFO MAPPED_TRAIT strings for the three diseases (verified present in the
# 2026-08 release). Exact match only: compound/co-mapped rows (e.g.
# "Crohn disease, leprosy", pleiotropy dumps) are excluded so a bridge means
# independent association in separate focused studies, not one shared study.
TRAIT_MAPPED = {
    "leprosy": "leprosy",
    "crohns": "Crohn disease",
    "ibd": "inflammatory bowel disease",
}


def trait_matches(mapped_trait: str, trait_key: str) -> bool:
    """True iff the association's MAPPED_TRAIT is EXACTLY this trait's EFO term."""
    return mapped_trait.strip() == TRAIT_MAPPED[trait_key]


def extract(bulk_tsv) -> dict[str, int]:
    """Write one per-trait TSV (header + matching rows) per TRAITS entry.

    Matched rows (a few thousand) are collected in memory then written, so no
    nest of simultaneously-open output files is required.
    """
    matched: dict[str, list[list[str]]] = {key: [] for key in TRAITS}
    with open(bulk_tsv, encoding="utf-8", errors="replace") as fh:
        reader = csv.reader(fh, delimiter="\t")
        header = next(reader)
        mt_idx = header.index("MAPPED_TRAIT")
        for row in reader:
            if len(row) <= mt_idx:
                continue
            mt = row[mt_idx]
            for key in TRAITS:
                if trait_matches(mt, key):
                    matched[key].append(row)
    counts = {}
    for key, out_path in TRAITS.items():
        with open(out_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerow(header)
            writer.writerows(matched[key])
        counts[key] = len(matched[key])
    return counts


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: python -m homeostat.gwas_extract <bulk_associations.tsv>")
    counts = extract(sys.argv[1])
    for key, n in counts.items():
        print(f"[gwas-extract] {key}: {n} associations -> {TRAITS[key].name}")


if __name__ == "__main__":
    main()

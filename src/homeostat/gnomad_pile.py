"""§7 replication — E/I/R PBS pile from gnomAD v2.1.1 exomes (a real SA cohort).

Independent replication of the Pan-UKBB pile on a DIFFERENT South Asian reference.
gnomAD v2.1.1 is GRCh37 (matches refGene_hg19 / 1000G — no liftover); its INFO
carries per-variant AF/AN for SAS (focal), NFE (close European), EAS (outgroup).
PBS(SAS; NFE, EAS) per variant, using the per-variant AN as the haploid size
(better than a fixed HAP_N). Coding variants only (exomes) — a gene-centric
replication aligned with the live gates (§3.2, LRRK2), not a genome-wide swap.

Streams the LOCAL sites VCF (downloaded resumably to data/gnomad/) once, O(1)
memory, same pile format + column order as eir_cohort so the gates consume it
unchanged. Run: HOMEOSTAT_TAG=_gnomad make gnomad-pile.
"""

import datetime
import gzip
import heapq
import sys

from homeostat import paths, pbs
from homeostat.util import atomic_write_json

SRC = paths.DATA / "gnomad" / "gnomad.exomes.r2.1.1.sites.vcf.bgz"
PILE = paths.tagged("eir_pbs_pile.tsv.gz")
SUMMARY = paths.tagged("eir_pbs_pile_summary.json")
PILE_HEADER = "chrom\tpos\tref\talt\taf_sas\taf_nfe\taf_eas\tmaf_sas\tfst_sas_nfe\tpbs_sas\n"
MIN_AN = 2  # hudson_fst uses (n-1); AN>=2 keeps it finite
AUTOSOMES = frozenset(str(c) for c in range(1, 23))


def info_get(info: str, key: str) -> str | None:
    """Value of INFO key `key`, anchored at a field boundary so 'AF_sas' does not
    match 'controls_AF_sas' or 'AF_sas_male'. None if absent."""
    marker = ";" + key + "="
    s = ";" + info
    i = s.find(marker)
    if i < 0:
        return None
    start = i + len(marker)
    j = s.find(";", start)
    return s[start:] if j < 0 else s[start:j]


def _f(s: str | None) -> float | None:
    if s is None:
        return None
    try:
        v = float(s)
    except ValueError:
        return None
    return None if v != v else v  # NaN guard


def parse_line(line: str) -> tuple | None:
    """A gnomAD VCF data line -> (chrom,pos,ref,alt,af_sas,af_nfe,af_eas,
    an_sas,an_nfe,an_eas), or None if it should be dropped.

    Drops: non-PASS FILTER; any of the 3 pops missing AF or AN; AN<2 in any pop;
    focal (SAS) or close (NFE) monomorphic (no branch signal); non-autosome.
    """
    f = line.rstrip("\n").split("\t")
    if len(f) < 8 or f[6] != "PASS" or f[0] not in AUTOSOMES:
        return None
    info = f[7]
    an_sas, an_nfe, an_eas = (
        _f(info_get(info, "AN_sas")),
        _f(info_get(info, "AN_nfe")),
        _f(info_get(info, "AN_eas")),
    )
    if an_sas is None or an_nfe is None or an_eas is None:
        return None
    if an_sas < MIN_AN or an_nfe < MIN_AN or an_eas < MIN_AN:
        return None
    af_sas, af_nfe, af_eas = (
        _f(info_get(info, "AF_sas")),
        _f(info_get(info, "AF_nfe")),
        _f(info_get(info, "AF_eas")),
    )
    if af_sas is None or af_nfe is None or af_eas is None:
        return None
    if not (0.0 < af_sas < 1.0) or not (0.0 < af_nfe < 1.0):
        return None
    return (f[0], f[1], f[3], f[4], af_sas, af_nfe, af_eas, int(an_sas), int(an_nfe), int(an_eas))


def pile_row(rec: tuple) -> tuple[str, float, str, int]:
    """Record -> (pile TSV line, pbs, chrom, pos). Same column order as eir_cohort
    so downstream index-based readers (gene_pbs_weights, eir_enrich) are unchanged."""
    chrom, pos, ref, alt, af_sas, af_nfe, af_eas, an_sas, an_nfe, an_eas = rec
    fst = pbs.hudson_fst(af_sas, an_sas, af_nfe, an_nfe)
    p = pbs.pbs(af_sas, af_nfe, af_eas, an_sas, an_nfe, an_eas)
    maf = min(af_sas, 1.0 - af_sas)
    row = (
        f"{chrom}\t{pos}\t{ref}\t{alt}\t{af_sas:.6g}\t{af_nfe:.6g}\t{af_eas:.6g}"
        f"\t{maf:.4f}\t{fst:.6g}\t{p:.6g}\n"
    )
    return row, p, chrom, int(pos)


def build(src) -> dict:
    counts = {"streamed": 0, "written": 0, "dropped": 0}
    top: list[tuple[float, str, int]] = []
    tmp = PILE.with_suffix(PILE.suffix + ".tmp")
    with (
        gzip.open(src, "rt", encoding="utf-8", errors="replace") as f,
        gzip.open(tmp, "wt", encoding="utf-8") as out,
    ):
        out.write(PILE_HEADER)
        for line in f:
            if line.startswith("#"):
                continue
            counts["streamed"] += 1
            rec = parse_line(line)
            if rec is None:
                counts["dropped"] += 1
                continue
            row, p, chrom, pos = pile_row(rec)
            out.write(row)
            counts["written"] += 1
            if len(top) < 30:
                heapq.heappush(top, (p, chrom, pos))
            elif p > top[0][0]:
                heapq.heapreplace(top, (p, chrom, pos))
            if counts["streamed"] % 2_000_000 == 0:
                print(
                    f"[gnomad] streamed {counts['streamed']:,} written {counts['written']:,}",
                    flush=True,
                )
    tmp.replace(PILE)
    top_sorted = sorted(top, reverse=True)
    return {
        "stage": "§7 E/I/R PBS pile — gnomAD v2.1.1 exomes (SA-cohort replication)",
        "completed": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source": str(src),
        "note": "PBS(SAS focal, NFE close, EAS outgroup) from gnomAD v2.1.1 exome AFs. "
        "GRCh37, PASS-only, per-variant AN as haploid size. Coding variants only. "
        "Independent replication of the Pan-UKBB pile; Law 2 (no p-value, no annotation).",
        "counts": counts,
        "top30_by_pbs": [{"chrom": c, "pos": p_, "pbs": round(pv, 5)} for pv, c, p_ in top_sorted],
        "output": str(PILE),
    }


def main() -> None:
    if PILE.exists() and SUMMARY.exists():
        print(f"[gnomad] pile already built ({PILE}); delete to rebuild")
        return
    if not SRC.exists():
        sys.exit(f"[gnomad] source missing: {SRC} — download it first")
    if not paths.EIR.exists():
        paths.EIR.mkdir(parents=True, exist_ok=True)
    result = build(SRC)
    atomic_write_json(SUMMARY, result)
    c = result["counts"]
    print(f"[gnomad] pile: {c['written']:,} variants -> {PILE}")
    print(f"[gnomad] streamed {c['streamed']:,}, dropped {c['dropped']:,}")


if __name__ == "__main__":
    main()

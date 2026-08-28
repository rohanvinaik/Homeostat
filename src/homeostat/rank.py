"""Score the matched sites and emit the ranked E/I/R candidate queue.

Re-scoring is cheap and never touches the scan: all frequency columns are in
the shards, all dials are recorded in the summary, and the output carries every
component of the score so downstream re-weighting needs no re-run.
"""

import datetime
import gzip
from pathlib import Path

from homeostat import paths
from homeostat import pbs as pbsmod
from homeostat.paths import AUTOSOMES
from homeostat.util import atomic_write_json

OUT_HEADER = (
    "priority\tpbs_sas_eas_out\tpbs_sas_afr_out\tdelta_sas_eur\ti_allele\tr_dosage_i"
    "\tchrom\tpos\trsid_r\trsid_kg\tref\talt\tgenotype_r"
    "\taf_eur\taf_sas\taf_eas\taf_afr\taf_amp_unused\tambiguous_strand\tfilter\n"
)


def _score_row(fields: list[str]) -> tuple[float, str] | None:
    (
        chrom,
        pos,
        rsid_r,
        rsid_kg,
        ref,
        alt,
        genotype,
        af_eur_s,
        af_sas_s,
        af_eas_s,
        af_afr_s,
        af_amr_s,
        ambiguous,
        filt,
    ) = fields
    try:
        af_eur, af_sas = float(af_eur_s), float(af_sas_s)
        af_eas, af_afr = float(af_eas_s), float(af_afr_s)
    except ValueError:
        return None
    n = pbsmod.HAP_N
    pbs_eas = pbsmod.pbs(af_sas, af_eur, af_eas, n["SAS"], n["EUR"], n["EAS"])
    pbs_afr = pbsmod.pbs(af_sas, af_eur, af_afr, n["SAS"], n["EUR"], n["AFR"])
    i_allele = pbsmod.i_shifted_allele(af_sas, af_eur, ref, alt)
    dosage = 0 if i_allele == "none" else pbsmod.r_dosage(genotype, i_allele)
    score = pbsmod.priority(pbs_eas, dosage)
    delta = af_sas - af_eur
    row = (
        f"{score:.6g}\t{pbs_eas:.6g}\t{pbs_afr:.6g}\t{delta:.4f}\t{i_allele}\t{dosage}"
        f"\t{chrom}\t{pos}\t{rsid_r}\t{rsid_kg}\t{ref}\t{alt}\t{genotype}"
        f"\t{af_eur_s}\t{af_sas_s}\t{af_eas_s}\t{af_afr_s}\t{af_amr_s}\t{ambiguous}\t{filt}\n"
    )
    return score, row


def rank(genotype_counts: dict[str, int], genotype_sha256: str) -> dict:
    scored: list[tuple[float, str]] = []
    unparseable = 0
    for chrom in AUTOSOMES:
        shard = paths.SHARDS / f"chr{chrom}.tsv"
        with open(shard, encoding="utf-8") as f:
            next(f)  # header
            for line in f:
                result = _score_row(line.rstrip("\n").split("\t"))
                if result is None:
                    unparseable += 1
                else:
                    scored.append(result)
    scored.sort(key=lambda t: t[0], reverse=True)

    tmp = Path(str(paths.CANDIDATES) + ".tmp")
    with gzip.open(tmp, "wt", encoding="utf-8") as out:
        out.write(OUT_HEADER)
        for _, row in scored:
            out.write(row)
    tmp.replace(paths.CANDIDATES)

    nonzero = sum(1 for s, _ in scored if s > 0)
    top = [line.rstrip("\n").split("\t")[:9] for _, line in scored[:25]]
    summary = {
        "stage": "13.1 E/I/R filter",
        "completed": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "dials": dict(pbsmod.DIALS),
        "hap_n": dict(pbsmod.HAP_N),
        "genotype_input": {"sha256": genotype_sha256, "counts": genotype_counts},
        "candidates_total": len(scored),
        "candidates_priority_gt0": nonzero,
        "unparseable_af_rows": unparseable,
        "top25_preview": [
            dict(
                zip(
                    [
                        "priority",
                        "pbs_sas_eas_out",
                        "pbs_sas_afr_out",
                        "delta_sas_eur",
                        "i_allele",
                        "r_dosage_i",
                        "chrom",
                        "pos",
                        "rsid_r",
                    ],
                    t,
                    strict=True,
                )
            )
            for t in top
        ],
        "output": str(paths.CANDIDATES),
    }
    atomic_write_json(paths.SUMMARY, summary)
    return summary

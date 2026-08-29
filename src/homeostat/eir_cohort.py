"""§7 — the cohort-scale E/I/R candidate-set filter (the PBS pile).

The candidate object of the whole program (Law 2): a population-DIFFERENTIAL
priority queue, NOT a p-value-selected set. E = EUR, I = CSA (South Asian),
outgroup = EAS. Per variant, PBS(CSA focal; EUR, EAS) — "which population (CSA)
diverged at this locus" (§7.3). Ranked descending. This is a PRIOR OVER SEARCH
ORDER, not a hypothesis test (§7.2); it bounds the bridge count d before any
descent runs. No p-value, no gene annotation, no n=1 R (the n=1 index is dropped
at cohort scale, §7.4).

Source: Pan-UKBB per-phenotype file allele-frequency columns (af_EUR/af_CSA/
af_EAS are population frequencies, phenotype-independent), free (AWS Registry of
Open Data). Reuses pbs.py (Hudson F_ST + PBS).

Run: make eir-pile. Streams the file once, O(1) memory. Idempotent.
"""

import datetime
import gzip
import heapq
import math
import sys

from homeostat import paths, pbs
from homeostat.util import atomic_write_json

# Pan-UKBB continuous-trait cohort haploid sizes (2N), as dials. Large-N: Hudson
# F_ST's finite-sample correction is negligible; recorded, not hidden.
HAP_N = {"EUR": 838000, "CSA": 17400, "EAS": 5000}
PBS_OUTGROUP = "EAS"

PILE = paths.EIR / "eir_pbs_pile.tsv.gz"
SUMMARY = paths.EIR / "eir_pbs_pile_summary.json"
DEFAULT_SRC = paths.DATA / "panukbb" / "eos_30150.tsv.bgz"

PILE_HEADER = "chrom\tpos\tref\talt\taf_csa\taf_eur\taf_eas\tmaf_csa\tfst_csa_eur\tpbs_csa\n"


def _fnum(s: str) -> float | None:
    try:
        v = float(s)
    except (ValueError, TypeError):
        return None
    return None if math.isnan(v) else v


def build(src) -> dict:
    """Stream Pan-UKBB AFs -> PBS(CSA;EUR,EAS) pile, written as a gzipped TSV."""
    n = HAP_N
    counts = {"streamed": 0, "written": 0, "af_missing": 0, "monomorphic": 0}
    top = []  # bounded max-heap preview of highest-PBS variants
    tmp = PILE.with_suffix(PILE.suffix + ".tmp")

    with gzip.open(src, "rt", encoding="utf-8") as f, gzip.open(tmp, "wt", encoding="utf-8") as out:
        header = f.readline().rstrip("\n").split("\t")
        idx = {c: i for i, c in enumerate(header)}
        for col in ("chr", "pos", "ref", "alt", "af_EUR", "af_CSA", "af_EAS"):
            if col not in idx:
                sys.exit(f"[eir] column missing: {col}")
        out.write(PILE_HEADER)

        for line in f:
            counts["streamed"] += 1
            fld = line.rstrip("\n").split("\t")
            af_eur = _fnum(fld[idx["af_EUR"]])
            af_csa = _fnum(fld[idx["af_CSA"]])
            af_eas = _fnum(fld[idx["af_EAS"]])
            if af_eur is None or af_csa is None or af_eas is None:
                counts["af_missing"] += 1
                continue
            # A variant must actually vary in the focal and close pools to carry
            # a population-branch signal; monomorphic-both is PBS-uninformative.
            if not (0.0 < af_csa < 1.0) or not (0.0 < af_eur < 1.0):
                counts["monomorphic"] += 1
                continue
            fst = pbs.hudson_fst(af_csa, n["CSA"], af_eur, n["EUR"])
            p = pbs.pbs(af_csa, af_eur, af_eas, n["CSA"], n["EUR"], n["EAS"])
            maf = min(af_csa, 1.0 - af_csa)
            chrom, pos = fld[idx["chr"]], fld[idx["pos"]]
            out.write(
                f"{chrom}\t{pos}\t{fld[idx['ref']]}\t{fld[idx['alt']]}"
                f"\t{af_csa:.6g}\t{af_eur:.6g}\t{af_eas:.6g}\t{maf:.4f}\t{fst:.6g}\t{p:.6g}\n"
            )
            counts["written"] += 1
            if len(top) < 30:
                heapq.heappush(top, (p, chrom, int(pos)))
            elif p > top[0][0]:
                heapq.heapreplace(top, (p, chrom, int(pos)))
    tmp.replace(PILE)

    top_sorted = sorted(top, reverse=True)
    return {
        "stage": "§7 E/I/R cohort PBS pile (population-differential candidate set)",
        "completed": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source": str(src),
        "note": "PBS(CSA focal, EUR close, EAS outgroup). Search-order prior, not a "
        "hypothesis test. No p-value gate, no annotation, no n=1. Law 2.",
        "dials": {"hap_n": HAP_N, "pbs_outgroup": PBS_OUTGROUP},
        "counts": counts,
        "top30_by_pbs": [{"chrom": c, "pos": p_, "pbs": round(pv, 5)} for pv, c, p_ in top_sorted],
        "output": str(PILE),
    }


def main() -> None:
    if PILE.exists() and SUMMARY.exists():
        print(f"[eir] pile already built ({PILE}); delete to rebuild")
        return
    src = sys.argv[1] if len(sys.argv) > 1 else str(DEFAULT_SRC)
    if not paths.EIR.exists():
        paths.EIR.mkdir(parents=True, exist_ok=True)
    result = build(src)
    atomic_write_json(SUMMARY, result)
    c = result["counts"]
    print(f"[eir] pile: {c['written']} variants -> {PILE}")
    print(f"[eir] streamed {c['streamed']}, af_missing {c['af_missing']}, mono {c['monomorphic']}")


if __name__ == "__main__":
    main()

"""Analyse a Pan-UK Biobank per-phenotype sumstats file for the EUR-vs-CSA
(European vs Central/South-Asian) contrast — the cohort-scale replacement for
the n=1 E/I/R prior.

Two measurements the n=1 genome could NOT support:
  1. EFFECT-SIZE TRANSFERABILITY (§8.1): for variants genome-wide significant
     in EUR, do beta_EUR and beta_CSA agree in sign and magnitude? Portability
     of European-discovered effects into the South-Asian population.
  2. POPULATION DIVERGENCE at trait loci (§7/§8.1): are the trait-associated
     variants more population-differentiated (F_ST / PBS, CSA focal) than the
     genome-wide background?

Streams the bgzipped TSV once (stdlib gzip reads bgzip). Pure stat helpers are
in `panukbb` and tested; `pbs.hudson_fst` / `pbs.pbs` are reused.

Run: make panukbb PHENO=<path>. Free data (AWS Registry of Open Data).
"""

import datetime
import gzip
import math
import sys

from homeostat import paths, pbs
from homeostat.util import atomic_write_json

# Approx haploid sample sizes for the UKB continuous-trait cohorts (2N).
# Large-N: Hudson F_ST's finite-sample correction is negligible here; recorded
# as a dial, not a hidden constant.
HAP_N = {"EUR": 838000, "CSA": 17400, "EAS": 5000}
GW_SIG = 7.30103  # -log10(5e-8)
OUT = paths.EIR / "panukbb_eos_eur_vs_csa.json"


def sign_concordance(betas: list[tuple[float, float]]) -> float:
    """Fraction of (beta_a, beta_b) pairs that share sign (0 excluded)."""
    ok = [(a, b) for a, b in betas if a != 0 and b != 0]
    if not ok:
        return 0.0
    return sum(1 for a, b in ok if (a > 0) == (b > 0)) / len(ok)


def pearson(xy: list[tuple[float, float]]) -> float:
    n = len(xy)
    if n < 2:
        return 0.0
    mx = sum(x for x, _ in xy) / n
    my = sum(y for _, y in xy) / n
    sx = sum((x - mx) ** 2 for x, _ in xy)
    sy = sum((y - my) ** 2 for _, y in xy)
    if sx == 0 or sy == 0:
        return 0.0
    cov = sum((x - mx) * (y - my) for x, y in xy)
    return cov / math.sqrt(sx * sy)


def _fnum(s: str) -> float | None:
    try:
        v = float(s)
    except (ValueError, TypeError):
        return None
    return None if math.isnan(v) else v


def analyse(path: str) -> dict:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        header = f.readline().rstrip("\n").split("\t")
        idx = {c: i for i, c in enumerate(header)}
        need = [
            "chr",
            "pos",
            "af_EUR",
            "af_CSA",
            "af_EAS",
            "beta_EUR",
            "beta_CSA",
            "neglog10_pval_EUR",
            "neglog10_pval_CSA",
            "low_confidence_EUR",
            "low_confidence_CSA",
        ]
        for c in need:
            if c not in idx:
                sys.exit(f"[panukbb] column missing: {c}")

        gw_beta_pairs: list[tuple[float, float]] = []
        fst_bg_sum = 0.0
        fst_bg_n = 0
        sig_variants = []  # EUR-significant, both-confident
        n_lines = 0

        for line in f:
            n_lines += 1
            fld = line.rstrip("\n").split("\t")
            if fld[idx["low_confidence_EUR"]] == "true":
                continue
            b_eur = _fnum(fld[idx["beta_EUR"]])
            b_csa = _fnum(fld[idx["beta_CSA"]])
            af_eur = _fnum(fld[idx["af_EUR"]])
            af_csa = _fnum(fld[idx["af_CSA"]])
            low_csa = fld[idx["low_confidence_CSA"]] == "true"

            if b_eur is not None and b_csa is not None and not low_csa:
                gw_beta_pairs.append((b_eur, b_csa))
            if af_eur is not None and af_csa is not None and not low_csa:
                fst = pbs.hudson_fst(af_csa, HAP_N["CSA"], af_eur, HAP_N["EUR"])
                fst_bg_sum += fst
                fst_bg_n += 1

            p_eur = _fnum(fld[idx["neglog10_pval_EUR"]])
            if p_eur is not None and p_eur >= GW_SIG and not low_csa:
                af_eas = _fnum(fld[idx["af_EAS"]])
                if None not in (b_eur, b_csa, af_eur, af_csa):
                    sig_variants.append(
                        {
                            "chr": fld[idx["chr"]],
                            "pos": int(fld[idx["pos"]]),
                            "af_eur": af_eur,
                            "af_csa": af_csa,
                            "af_eas": af_eas,
                            "beta_eur": b_eur,
                            "beta_csa": b_csa,
                            "p_csa": _fnum(fld[idx["neglog10_pval_CSA"]]),
                        }
                    )

    # Transferability among EUR-significant variants.
    sig_pairs = [(v["beta_eur"], v["beta_csa"]) for v in sig_variants]
    concord = sign_concordance(sig_pairs)
    r_sig = pearson(sig_pairs)
    replicated = sum(
        1
        for v in sig_variants
        if v["p_csa"] is not None
        and v["p_csa"] >= -math.log10(0.05)
        and (v["beta_eur"] > 0) == (v["beta_csa"] > 0)
    )

    # Divergence at trait loci vs background.
    fst_sig = []
    pbs_sig = []
    for v in sig_variants:
        fst_sig.append(pbs.hudson_fst(v["af_csa"], HAP_N["CSA"], v["af_eur"], HAP_N["EUR"]))
        if v["af_eas"] is not None:
            pbs_sig.append(
                pbs.pbs(
                    v["af_csa"], v["af_eur"], v["af_eas"], HAP_N["CSA"], HAP_N["EUR"], HAP_N["EAS"]
                )
            )
    mean_fst_sig = sum(fst_sig) / len(fst_sig) if fst_sig else 0.0
    mean_fst_bg = fst_bg_sum / fst_bg_n if fst_bg_n else 0.0

    return {
        "stage": "Pan-UKBB eosinophil-count EUR vs CSA (cohort-scale E/I contrast)",
        "completed": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source": "s3://pan-ukb-us-east-1 (AWS Registry of Open Data; free, no affiliation)",
        "phenotype": "continuous-30150 eosinophil count (irnt)",
        "dials": {"hap_n": HAP_N, "gw_sig_neglog10p": GW_SIG},
        "counts": {
            "variants_streamed": n_lines,
            "eur_confident_with_csa_beta": len(gw_beta_pairs),
            "eur_genomewide_sig_both_confident": len(sig_variants),
        },
        "transferability_sec8_1": {
            "genomewide_beta_pearson_EUR_CSA": round(pearson(gw_beta_pairs), 4),
            "sig_beta_pearson_EUR_CSA": round(r_sig, 4),
            "sig_sign_concordance": round(concord, 4),
            "sig_replicated_dir_p05": replicated,
            "sig_total": len(sig_variants),
        },
        "divergence_sec7": {
            "mean_fst_csa_eur_at_sig_loci": round(mean_fst_sig, 5),
            "mean_fst_csa_eur_background": round(mean_fst_bg, 5),
            "fst_enrichment_ratio": round(mean_fst_sig / mean_fst_bg, 3) if mean_fst_bg else None,
            "mean_pbs_csa_at_sig_loci": round(sum(pbs_sig) / len(pbs_sig), 5) if pbs_sig else None,
        },
    }


def main() -> None:
    if OUT.exists():
        print(f"[panukbb] already complete ({OUT}); delete to re-run")
        return
    path = sys.argv[1] if len(sys.argv) > 1 else str(paths.DATA / "panukbb" / "eos_30150.tsv.bgz")
    result = analyse(path)
    atomic_write_json(OUT, result)
    import json

    print(
        json.dumps(
            {k: result[k] for k in ("counts", "transferability_sec8_1", "divergence_sec7")},
            indent=2,
        )
    )
    print(f"[panukbb] complete -> {OUT}")


if __name__ == "__main__":
    main()

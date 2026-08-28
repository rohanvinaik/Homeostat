"""Pure PBS / F_ST math. No I/O — the Detective-pinnable decision core.

All dials are explicit parameters with the defaults recorded in DIALS, so the
ranking is re-scorable without re-scanning (checkpoint §7.3: a continuous
per-locus ranking — a prior over search order, not a hypothesis test).
"""

import math

# 1000 Genomes phase 3 haploid sample sizes (2N), per superpopulation.
HAP_N = {"EUR": 1006, "SAS": 978, "EAS": 1008, "AFR": 1322, "AMR": 694}

# Default dials for the priority score. Every assumption is a dial.
DIALS = {
    "outgroup": "EAS",  # PBS outgroup; AFR column also emitted
    "fst_clamp": 0.999999,  # keeps -log(1 - fst) finite
    "pbs_floor": 0.0,  # negative PBS floors to 0 in the priority product
}


def hudson_fst(p1: float, n1: int, p2: float, n2: int) -> float:
    """Hudson's F_ST estimator for one site (Bhatia et al. 2013, eq. 10).

    p1, p2: alternate-allele frequencies; n1, n2: haploid sample sizes.
    Returns the ratio-of-site estimates value, clamped to [0, 1].
    """
    num = (p1 - p2) ** 2 - p1 * (1 - p1) / (n1 - 1) - p2 * (1 - p2) / (n2 - 1)
    den = p1 * (1 - p2) + p2 * (1 - p1)
    if den <= 0.0:
        return 0.0
    return min(max(num / den, 0.0), 1.0)


def _branch(fst: float, clamp: float) -> float:
    """Population branch length T = -log(1 - F_ST), with F_ST clamped."""
    return -math.log(1.0 - min(fst, clamp))


def pbs(
    p_focal: float,
    p_close: float,
    p_out: float,
    n_focal: int,
    n_close: int,
    n_out: int,
    clamp: float = DIALS["fst_clamp"],
) -> float:
    """Population branch statistic for the focal population.

    PBS = (T(focal,close) + T(focal,out) - T(close,out)) / 2. Can be negative
    (branch shortening); callers decide whether to floor it.
    """
    t_fc = _branch(hudson_fst(p_focal, n_focal, p_close, n_close), clamp)
    t_fo = _branch(hudson_fst(p_focal, n_focal, p_out, n_out), clamp)
    t_co = _branch(hudson_fst(p_close, n_close, p_out, n_out), clamp)
    return (t_fc + t_fo - t_co) / 2.0


def i_shifted_allele(af_sas: float, af_eur: float, ref: str, alt: str) -> str:
    """The allele whose frequency is elevated in I (SAS) relative to E (EUR).

    Ties (delta == 0) resolve to "none": the site carries no E/I direction.
    """
    delta = af_sas - af_eur
    if delta > 0:
        return alt
    if delta < 0:
        return ref
    return "none"


def r_dosage(genotype: str, allele: str) -> int:
    """Copies of `allele` carried by R's diploid genotype string (e.g. 'AG')."""
    return sum(1 for a in genotype if a == allele)


def priority(
    pbs_value: float,
    dosage_i: int,
    pbs_floor: float = DIALS["pbs_floor"],
) -> float:
    """The E/I/R priority score: divergence weighted by R's sharing with I.

    R matching I on an I-shifted, high-PBS allele -> enriched (§7.1);
    R matching E (dosage 0) -> deprioritized to 0. A ranking, not a test.
    """
    return max(pbs_value, pbs_floor) * (dosage_i / 2.0)

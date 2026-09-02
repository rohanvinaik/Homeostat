"""homeostat.coexpression — the co-expression bank, read as DYNAMICS not statistics.

A co-expression coupling is NOT a correlation (a population statistic is the slop LAW 1 forbids).
Every GTEx sample is a natural PERTURBATION (a donor at a different point in condition/genotype
space), so co-expression is read as **OTP ternary CO-DEVIATION under perturbation**: each gene's
per-sample expression is positioned as a signed-ternary deviation off its tissue mined-zero
(`otp.ternary` — the primitive the engine uses on the person), and two genes couple where they
CONSISTENTLY co-deviate. A sample where either gene sits at baseline is the informational zero and
drops out (the Monty-Hall move — baseline noise never dilutes the read). Significance is κ
(convergence across banks), NEVER the co-deviation count; this bank only VOTES.

The GTEx render (position per tissue, co-deviation for scoped genes, emit `Event("coexpression",
…, mode=<tissue>)`) is below; the fetch/cache lives in `gtex_fetch`.
"""

from __future__ import annotations

import math
import statistics
from collections.abc import Mapping, Sequence

from homeostat.event import Event
from homeostat.otp import ternary

COEXPRESSION = "coexpression"
_EPS = 1.0  # TPM pseudocount so the log2 ratio is defined at zero expression


def codeviation(a: Sequence[int], b: Sequence[int]) -> tuple[int, int]:
    """Over two aligned per-sample ternary sequences (each entry −1/0/+1, a gene's deviation off its
    tissue mined-zero per sample), count the JOINT perturbations and how many ALIGN. Returns
    ``(n_codeviate, n_aligned)``: a sample counts only where BOTH genes are off baseline (the
    informational zero drops the rest), and aligns when both deviate the SAME direction. Pure.
    """
    n_codeviate = 0
    n_aligned = 0
    for x, y in zip(a, b, strict=True):
        if x != 0 and y != 0:
            n_codeviate += 1
            if (x > 0) == (y > 0):
                n_aligned += 1
    return n_codeviate, n_aligned


def codeviation_verdict(
    n_codeviate: int, n_aligned: int, min_support: int, consistency: float
) -> str:
    """The pure co-expression decision from a pair's co-deviation counts. Named codes, never bools:
    - ``"insufficient"`` — fewer than `min_support` joint perturbations;
    - ``"co-varies"`` — at least `consistency` of the joints align: driven together;
    - ``"counter-varies"`` — at least `consistency` are OPPOSED: coupled in antiphase;
    - ``"uncoupled"`` — the joint deviations are mixed, no consistent coupling.
    The consistency band is a deterministic noise tolerance (OTP-style), not a statistical cutoff;
    significance stays κ. Pure over the counts and the two thresholds.
    """
    if n_codeviate < min_support or n_codeviate <= 0:
        return "insufficient"
    aligned_frac = n_aligned / n_codeviate
    if aligned_frac >= consistency:
        return "co-varies"
    if (1.0 - aligned_frac) >= consistency:
        return "counter-varies"
    return "uncoupled"


def tissue_ternary(values: Sequence[float], tol_log: float) -> list[int]:
    """Position a gene's per-sample TPM WITHIN one tissue as OTP ternary off the tissue MEDIAN (the
    mined-zero), on the log2 ratio: above +`tol_log` log-fold is +1, below −`tol_log` is −1, within
    the band is the informational zero. Pure over the value list and the log-fold tolerance."""
    if not values:
        return []
    base = statistics.median(values)
    return [ternary(math.log2((v + _EPS) / (base + _EPS)), tol_log) for v in values]


def coexpression_events(
    sample_ids: Sequence[str],
    expr: Mapping[str, Sequence[float]],
    sample_tissue: Mapping[str, str],
    tol_log: float = 1.0,
    min_support: int = 5,
    consistency: float = 0.8,
) -> list[Event]:
    """Render scoped per-sample expression into co-expression Events, tissue as `mode`.

    Within each tissue, position every gene as OTP ternary off its tissue median, then read each
    pair's co-deviation verdict. A ``"co-varies"`` pair emits ``Event("coexpression","tracks",…)``
    and a ``"counter-varies"`` pair ``Event("coexpression","opposes",…)`` — both `sign=+1` (an
    undirected vote that the coupling EXISTS; κ is significance), `mode=<tissue>` so convergence
    across tissues raises κ. Each unordered pair once (a < b). Orchestration over the pinned
    decisions; intent-tested.
    """
    by_tissue: dict[str, list[int]] = {}
    for i, sid in enumerate(sample_ids):
        tissue = sample_tissue.get(sid)
        if tissue:
            by_tissue.setdefault(tissue, []).append(i)
    genes = sorted(expr)
    out: list[Event] = []
    for tissue, idx in sorted(by_tissue.items()):
        tern = {g: tissue_ternary([expr[g][i] for i in idx], tol_log) for g in genes}
        for j in range(len(genes)):
            for k in range(j + 1, len(genes)):
                a, b = genes[j], genes[k]
                n_codeviate, n_aligned = codeviation(tern[a], tern[b])
                verdict = codeviation_verdict(n_codeviate, n_aligned, min_support, consistency)
                if verdict == "co-varies":
                    out.append(Event(COEXPRESSION, "tracks", a, b, 1, tissue))
                elif verdict == "counter-varies":
                    out.append(Event(COEXPRESSION, "opposes", a, b, 1, tissue))
    return out

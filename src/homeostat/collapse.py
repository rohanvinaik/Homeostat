"""LD-collapse: greedy window-max clumping of the per-variant queue.

Pure decision core, no I/O. Deterministic: highest-priority variant claims its
window; everything within +/- window_bp of a claimed lead on the same chromosome
is absorbed into that lead's locus. Ties break by (chrom, pos) for
reproducibility. This is positional clumping, not genotype-LD clumping —
window_bp is the dial standing in for LD structure until an LD reference is
added (see 2026-08-28 run record).
"""

import bisect
from dataclasses import dataclass

DEFAULT_WINDOW_BP = 500_000


@dataclass(frozen=True)
class Locus:
    chrom: str
    pos: int
    priority: float
    n_absorbed: int  # variants absorbed into this locus (including the lead)


def collapse(
    variants: list[tuple[str, int, float]],
    window_bp: int = DEFAULT_WINDOW_BP,
) -> list[Locus]:
    """(chrom, pos, priority) list -> loci, sorted by descending priority.

    O(n log k) via per-chromosome sorted lead positions: a variant can only be
    absorbed by the nearest lead on either side, found by bisection.
    """
    order = sorted(variants, key=lambda v: (-v[2], v[0], v[1]))
    lead_positions: dict[str, list[int]] = {}  # sorted lead positions per chrom
    lead_index: dict[tuple[str, int], int] = {}  # (chrom, lead_pos) -> leads idx
    leads: list[tuple[str, int, float]] = []
    absorbed: list[int] = []
    for chrom, pos, priority in order:
        positions = lead_positions.setdefault(chrom, [])
        i = bisect.bisect_left(positions, pos)
        owner_pos = None
        if i > 0 and pos - positions[i - 1] <= window_bp:
            owner_pos = positions[i - 1]
        if owner_pos is None and i < len(positions) and positions[i] - pos <= window_bp:
            owner_pos = positions[i]
        if owner_pos is None:
            bisect.insort(positions, pos)
            lead_index[(chrom, pos)] = len(leads)
            leads.append((chrom, pos, priority))
            absorbed.append(1)
        else:
            absorbed[lead_index[(chrom, owner_pos)]] += 1
    return [
        Locus(chrom, pos, priority, absorbed[i]) for i, (chrom, pos, priority) in enumerate(leads)
    ]

"""homeostat.search — the σ-trajectory search: candidate-elimination to a parsimonious mechanism.

The confirmed core (`docs/THEORY_OF_THE_CASE.md` Part II): drive **H = log₂(surviving candidate
mechanisms) → 0** by candidate-elimination, each "test" a **data-geometry constraint** that kills
a subset of candidates. **σ = the minimum constraints to pin a UNIQUE mechanism (SC=1)** — the
teaching dimension, a Blum measure, NOT a frequency. This module is the **object-agnostic engine**:
the candidates and their kill-sets are DATA plugged in; nothing here is a statistic and nothing
here authors the object.

The only interface is the **kill-matrix**: a constraint is the set of candidate-ids it KILLS. So
the data geometry (population co-variation + symptom co-presentation) enters *solely* as "which
candidate mechanisms does this constraint eliminate" — never as a frequency, an association, or a
hand-written edge.

Two of the founder's laws are enforced here:
- **The σ_sem > 0 falsifiability guard** (`falsifiable`): a resolution reached without genuine
  plurality to start, or without every step killing a rival (κ > 0), is the self-confirming
  degenerate case — the SDIS failure (100% retrodiction = memorization). Learn at the residual,
  never at the confirmation.
- **Early stopping at the κ-knee** (`knee_index`): κ is antitone under greedy selection; the bulk
  (κ > 1, clusters die at once) gives way to the tail (κ = 1, one rival at a time). The knee is the
  parsimony halt — past it, the search is memorizing the presentation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

# ---- the atomic pure decisions (Detective-pinnable) --------------------------------------


def survivors(candidates: list[str], applied_kills: list[list[str]]) -> list[str]:
    """The candidate mechanisms not eliminated by any applied constraint.

    `applied_kills` is the list of kill-sets (one per applied constraint); a candidate survives iff
    it appears in `candidates` and in none of the kill-sets. Order-preserving over `candidates`,
    with duplicate candidate-ids collapsed to their first occurrence. Pure over
    `(list[str], list[list[str]])`.
    """
    killed: set[str] = set()
    for ks in applied_kills:
        killed.update(ks)
    seen: set[str] = set()
    out: list[str] = []
    for c in candidates:
        if c not in killed and c not in seen:
            seen.add(c)
            out.append(c)
    return out


def entropy_bits(n_survivors: int) -> float:
    """Conceptual entropy H = log₂(n_survivors) over the surviving candidate mechanisms.

    H = 0 when a unique mechanism remains (n = 1, SC=1 — resolution) and, degenerately, when none
    does (n ≤ 0 — nothing coheres, the abstention case; kept 0.0 rather than undefined). H > 0
    exactly while plural candidates survive. Pure over `int`.
    """
    if n_survivors <= 1:
        return 0.0
    return math.log2(n_survivors)


def resolved(n_survivors: int) -> bool:
    """True iff exactly one candidate mechanism survives — SC=1, a unique reading. n = 0 (nothing
    coheres) is NOT resolution; it is abstention. Pure over `int`."""
    return n_survivors == 1


def marginal_kill(kill_set: list[str], already_killed: list[str]) -> int:
    """κ — the marginal coverage of a constraint: how many NEW candidates it eliminates beyond those
    already killed. A constraint with κ = 0 *confirms* rather than *resolves* (value zero, Howard)
    and must never count toward a resolution (the σ_sem guard). Pure over `(list[str], list[str])`.
    """
    seen = set(already_killed)
    new: set[str] = set()
    for c in kill_set:
        if c not in seen:
            new.add(c)
    return len(new)


def survivors_killed(kill_set: list[str], alive: list[str]) -> int:
    """κ for **seedless** elimination: how many CURRENT survivors a constraint eliminates —
    |alive ∩ kill_set|, measured against the live survivor set (so it is the marginal coverage at
    this step). A constraint with κ = 0 *confirms* rather than *resolves* (value zero, Howard); a
    constraint with κ = |alive| would empty the set — an over-constrained contradiction, never a
    resolution — so seedless admissibility is 0 < κ < |alive|. Pure over `(list[str], list[str])`.
    """
    return len(set(alive) & set(kill_set))


def constraint_disposition(kill_count: int, alive_count: int, is_censor: bool) -> str:
    """The two-sign admissibility decision for one constraint against the live survivor set.

    `kill_count` = κ = |alive ∩ kill_set|; `alive_count` = |alive|. Returns a named code (never a
    bool — two conditions that mean different things must not collapse into one truthy check):

    - ``"inert"`` — κ ≤ 0: kills no live survivor (a positive constraint confirms nothing; a censor
      rules nothing out). Value zero (Howard) — skip it.
    - ``"bottom"`` — κ ≥ alive_count AND `is_censor`: a negative censor rules out every surviving
      candidate → certified non-membership, the typed ⊥ (a proof that no lawful mechanism explains
      the presentation; NEGATIVE_SPECIFICATION §5 — the positive channel cannot produce this).
    - ``"inadmissible"`` — κ ≥ alive_count AND not `is_censor`: a positive constraint may not empty
      the set (the survivor of elimination IS the reading; emptying is the censor's job).
    - ``"eliminate"`` — 0 < κ < alive_count: a partial elimination, admissible on either sign.

    The whole two-sign asymmetry in one function: the positive sign may never empty the survivor
    set; the negative sign emptying it is the ⊥ certificate. Pure over `(int, int, bool)`.
    """
    if kill_count <= 0:
        return "inert"
    if kill_count >= alive_count:
        return "bottom" if is_censor else "inadmissible"
    return "eliminate"


def falsifiable(n_candidates_start: int, kappas: list[int]) -> bool:
    """The σ_sem > 0 guard, as a decision over a completed trajectory.

    True iff (a) there was **genuine plurality** to resolve at the start (`n_candidates_start > 1`)
    and (b) **every step learned at the residual** — each chosen constraint had κ > 0, actually
    killing a surviving rival. A resolution reached from no plurality, or via any κ ≤ 0 (confirming)
    step, is the self-confirming degenerate frame (σ_sem = 0) — the SDIS failure. An empty
    trajectory is not falsifiable (nothing resolved). Pure over `(int, list[int])`.
    """
    if n_candidates_start <= 1:
        return False
    if not kappas:
        return False
    return all(k > 0 for k in kappas)


def knee_index(kappas: list[int]) -> int:
    """The κ-knee: the index of the first step whose marginal coverage has fallen into the **tail**
    (κ ≤ 1 — the constraint resolves only a single rival). Under greedy selection κ is antitone, so
    this is the bulk→tail transition and the parsimony halt: grow while in the bulk (before the
    knee), stop here. Returns `len(kappas)` if the whole trajectory stayed in the bulk (κ > 1
    throughout). Pure over `list[int]`.
    """
    for i, k in enumerate(kappas):
        if k <= 1:
            return i
    return len(kappas)


# ---- the trajectory (orchestration over the pure decisions) --------------------------------


@dataclass(frozen=True)
class Step:
    """One step of the σ-trajectory: the chosen constraint and its marginal coverage κ."""

    constraint: str
    kappa: int


@dataclass(frozen=True)
class Trajectory:
    """The result of a σ-trajectory search.

    `steps` is the ordered greedy sequence (each carrying its κ). `sigma` = len(steps) when the
    search resolved to the sole survivor, else `None` — a **STUCK** plural residual no available
    constraint separates (where the discrimination selector adds a new dimension), OR a certified
    **⊥** when `bottom` is set. `survivors_left` is what remains (empty on ⊥). `falsifiable` is the
    σ_sem > 0 guard evaluated over the run. `bottom` = a negative censor ruled out every surviving
    candidate — certified non-membership ("no lawful mechanism, with proof"), reachable only on the
    two-sign path (`eliminate_two_sign`), never the positive-only one.
    """

    steps: list[Step]
    sigma: int | None
    survivors_left: list[str]
    falsifiable: bool
    bottom: bool = False


def sigma_trajectory(
    candidates: list[str], constraints: dict[str, list[str]], target: str
) -> Trajectory:
    """Greedy σ-trajectory: apply max-κ constraints until `target` uniquely survives.

    `constraints` maps a constraint-id to its kill-set. At each step the admissible constraint with
    the greatest marginal coverage κ is chosen — *admissible* means κ > 0 (it kills a surviving
    rival: learn at the residual) AND it does not kill `target` (never eliminate the reading being
    pinned); ties break by constraint-id for determinism. The run ends when `target` is the sole
    survivor (`sigma` = number of steps) or no admissible constraint remains (`sigma` = None — a
    STUCK residual for node birth). The σ_sem > 0 guard is evaluated via `falsifiable`. I/O-free
    orchestration over the pinned pure decisions; validated by hand-authored intent tests.
    """
    n_start = len(set(candidates))
    remaining = dict(constraints)
    applied: list[list[str]] = []
    killed_flat: list[str] = []
    steps: list[Step] = []

    while True:
        alive = survivors(candidates, applied)
        if resolved(len(alive)):
            break
        # score the admissible constraints by marginal coverage κ
        best_id: str | None = None
        best_kappa = 0
        for cid in sorted(remaining):
            kset = remaining[cid]
            if target in kset:  # never eliminate the reading we are pinning
                continue
            k = marginal_kill(kset, killed_flat)
            if k > best_kappa:
                best_kappa = k
                best_id = cid
        if best_id is None:  # no admissible κ>0 constraint — STUCK; node birth is needed
            alive = survivors(candidates, applied)
            return Trajectory(steps, None, alive, False)
        kset = remaining.pop(best_id)
        applied.append(kset)
        killed_flat.extend(kset)
        steps.append(Step(best_id, best_kappa))

    alive = survivors(candidates, applied)
    kappas = [s.kappa for s in steps]
    return Trajectory(steps, len(steps), alive, falsifiable(n_start, kappas))


def eliminate_to_survivor(candidates: list[str], constraints: dict[str, list[str]]) -> Trajectory:
    """Seedless σ-trajectory: drive **H = log₂|survivors| → 0** by candidate-elimination until a
    UNIQUE mechanism survives — **no protected target** (the SURVIVOR of elimination *is* the
    reading, per SSL: understanding is candidate-elimination to a unique or plural-stable survivor).

    `constraints` maps a constraint-id to its kill-set. At each step the admissible constraint with
    the greatest marginal coverage κ = |alive ∩ kill_set| is chosen — *admissible* means it kills
    ≥1 current survivor AND leaves ≥1 (`0 < κ < |alive|`: learn at the residual, never eliminate to
    the empty set); ties break by constraint-id for determinism. The run ends when one candidate
    survives (`sigma` = number of steps, and `survivors_left` is the pinned mechanism) or no
    admissible constraint remains while survivors are plural (`sigma` = None — a STUCK residual for
    node birth, or a genuine σ_sem > 0 plurality that no constraint separates). The σ_sem > 0 guard
    is evaluated via `falsifiable`. I/O-free orchestration over the pinned pure decisions; validated
    by hand-authored intent tests.
    """
    n_start = len(set(candidates))
    remaining = dict(constraints)
    applied: list[list[str]] = []
    steps: list[Step] = []

    while True:
        alive = survivors(candidates, applied)
        if resolved(len(alive)):
            break
        # score the admissible constraints by marginal coverage κ over the LIVE survivor set
        best_id: str | None = None
        best_kappa = 0
        for cid in sorted(remaining):
            k = survivors_killed(remaining[cid], alive)
            if k <= 0 or k >= len(alive):  # confirms nothing, or would empty the set
                continue
            if k > best_kappa:
                best_kappa = k
                best_id = cid
        if (
            best_id is None
        ):  # no admissible constraint — STUCK plural residual (node birth / σ_sem>0)
            return Trajectory(steps, None, alive, False)
        applied.append(remaining.pop(best_id))
        steps.append(Step(best_id, best_kappa))

    alive = survivors(candidates, applied)
    kappas = [s.kappa for s in steps]
    return Trajectory(steps, len(steps), alive, falsifiable(n_start, kappas))


def eliminate_two_sign(
    candidates: list[str],
    constraints: dict[str, list[str]],
    censors: dict[str, list[str]],
) -> Trajectory:
    """Two-sign σ-trajectory: positive candidate-elimination (μ, `constraints`) ∧ negative censors
    (μ⁻, `censors`) — driving H → 0 to a unique survivor, a certified ⊥, or a stuck plurality.

    Both signs eliminate by the same greedy max-κ rule (`constraint_disposition`), with one
    asymmetry: a **positive** constraint may never empty the survivor set (``"inadmissible"`` — the
    survivor of elimination IS the reading), while a **censor** that rules out every remaining
    survivor is not a failure but the **certified ⊥** — a proof of non-membership
    (`bottom=True`, `survivors_left=[]`; NEGATIVE_SPECIFICATION). The ⊥ check precedes the resolved
    check, so a censor ruling out the *sole* remaining candidate is ⊥, never a false RESOLVED. A
    censor may also act as a partial eliminator (0 < κ < |alive|), competing with positive
    constraints for the greedy step. Ends on: a unique survivor (`sigma` = steps, with `falsifiable`
    the σ_sem>0 guard); a certified ⊥ (`bottom=True`); or a STUCK plurality that no admissible
    constraint of either sign can separate (`sigma=None`, survivors plural — the selector's cue to
    add a new dimension). I/O-free orchestration over the pinned `constraint_disposition`; validated
    by hand-authored intent tests.
    """
    n_start = len(set(candidates))
    remaining_pos = dict(constraints)
    remaining_neg = dict(censors)
    applied: list[list[str]] = []
    steps: list[Step] = []

    while True:
        alive = survivors(candidates, applied)
        n = len(alive)
        # 1. certified ⊥ — a censor that now rules out EVERY surviving candidate (checked first, so
        #    a censor killing the sole survivor is ⊥, never a false resolution).
        for cid in sorted(remaining_neg):
            k = survivors_killed(remaining_neg[cid], alive)
            if constraint_disposition(k, n, is_censor=True) == "bottom":
                steps.append(Step(cid, k))
                return Trajectory(steps, None, [], False, bottom=True)
        # 2. a unique survivor is the resolved mechanism
        if resolved(n):
            break
        # 3. greedy max-κ admissible eliminator across BOTH signs (positive before negative on ties,
        #    then sorted id — deterministic).
        best_id: str | None = None
        best_kappa = 0
        best_kill: list[str] | None = None
        for cid in sorted(remaining_pos):
            k = survivors_killed(remaining_pos[cid], alive)
            if constraint_disposition(k, n, is_censor=False) == "eliminate" and k > best_kappa:
                best_id, best_kappa, best_kill = cid, k, remaining_pos[cid]
        for cid in sorted(remaining_neg):
            k = survivors_killed(remaining_neg[cid], alive)
            if constraint_disposition(k, n, is_censor=True) == "eliminate" and k > best_kappa:
                best_id, best_kappa, best_kill = cid, k, remaining_neg[cid]
        if best_id is None:  # STUCK plural residual — no dimension separates the survivors
            return Trajectory(steps, None, alive, False)
        applied.append(best_kill if best_kill is not None else [])
        steps.append(Step(best_id, best_kappa))
        remaining_pos.pop(best_id, None)
        remaining_neg.pop(best_id, None)

    alive = survivors(candidates, applied)
    kappas = [s.kappa for s in steps]
    return Trajectory(steps, len(steps), alive, falsifiable(n_start, kappas))

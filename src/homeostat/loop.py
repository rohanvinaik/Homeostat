"""homeostat.loop — the search-and-grow fixpoint that ties the σ-trajectory search to node birth.

The confirmed loop (`docs/THEORY_OF_THE_CASE.md` Part II): run the σ-trajectory search; if it is
STUCK on a residual it cannot resolve, **birth a node** from that residual and re-run; stop when a
parsimonious mechanism is pinned (resolved AND falsifiable), when the κ-knee says node birth has
stopped making bulk progress (growing further would memorize the tail), when node birth can grow no
more (a genuine residual with no data), or when the round budget is hit.

**Object-agnostic, with one seam.** The loop drives the fixpoint; the single data-dependent step —
*what node does a residual propose?* — is the `propose` callback the caller supplies. That callback
is where the data geometry enters (and where `nodes.py`'s lifecycle decides which proposed component
is BORN). The loop itself contains no statistic and authors no object; it only sequences search and
growth and applies the founder's two stopping laws:
- **The σ_sem > 0 guard.** A "resolution" that is not falsifiable (no plurality to resolve, or a
  confirming step) is the self-confirming SDIS case; the loop returns `DEGENERATE`, not a mechanism.
- **Early stopping at the κ-knee.** The knee here is over the *growth* trajectory: when a birth
  round reduces the residual by ≤ 1, node birth is resolving the tail one bespoke rival at a time
  (memorization), so the loop stops (`KNEE`) rather than keep growing.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeostat.search import Trajectory, sigma_trajectory

# Loop verdicts — named string codes.
RESOLVED = "RESOLVED"  # a unique mechanism, pinned AND falsifiable — the real finding
DEGENERATE = "DEGENERATE"  # resolved but NOT falsifiable — self-confirming (SDIS); not a finding
CONTINUE = "CONTINUE"  # stuck, still in the bulk, and node birth grew the state — re-run
KNEE = "KNEE"  # stuck and node birth stopped making bulk progress — parsimony halt
STUCK = "STUCK"  # stuck and node birth could not grow — a residual with no data (honest dead-end)
BUDGET = "BUDGET"  # the round budget was hit before resolution — a safety stop

# The `propose` seam: given the residual (survivors the search could not distinguish) and the round,
# return new candidates and new constraints to add (node birth's content). Returns empty when it
# cannot grow the state. This is the object/data-dependent hook; the loop treats it as a black box.
Propose = Callable[[list[str], int], tuple[list[str], dict[str, list[str]]]]


def loop_verdict(
    resolved: bool,
    falsifiable: bool,
    grew: bool,
    round_: int,
    max_rounds: int,
    at_knee: bool,
) -> str:
    """The loop's per-round decision, as a total function over named codes.

    A resolved search yields `RESOLVED` if the σ_sem guard holds (`falsifiable`), else `DEGENERATE`
    (a self-confirming, SDIS-shaped "resolution" — never a real finding). An unresolved search stops
    on `BUDGET` (round budget hit) or `KNEE` (node birth is past the parsimony knee — that outranks
    growth); otherwise it `CONTINUE`s iff node birth grew the state (`grew`), and is a genuine
    `STUCK` residual if it could not. Pure over `(bool, bool, bool, int, int, bool)`.
    """
    if resolved:
        return RESOLVED if falsifiable else DEGENERATE
    if round_ >= max_rounds:
        return BUDGET
    if at_knee:
        return KNEE
    if grew:
        return CONTINUE
    return STUCK


@dataclass(frozen=True)
class Result:
    """The outcome of a search-and-grow run.

    `verdict` is one of the loop codes. `mechanism` is the pinned target when `verdict == RESOLVED`,
    else `None`. `rounds` is how many growth rounds ran. `trajectory` is the final search trajectory
    (its `survivors_left` is the residual when the loop did not resolve).
    """

    verdict: str
    mechanism: str | None
    rounds: int
    trajectory: Trajectory


def run(
    candidates: list[str],
    constraints: dict[str, list[str]],
    target: str,
    propose: Propose,
    max_rounds: int,
) -> Result:
    """Drive the search-and-grow fixpoint to a verdict.

    Each round runs `sigma_trajectory`; if it does not resolve, `propose` is asked to grow the state
    (node birth) from the residual. The growth-κ knee is tracked as the drop in residual size across
    birth rounds: a round that reduces the residual by ≤ 1 is past the knee. `loop_verdict` decides;
    on `CONTINUE` the new candidates and constraints are merged and the round repeats, any other
    verdict returns. I/O-free orchestration over the pinned `loop_verdict` and the search; validated
    by hand-authored intent tests with a synthetic `propose`.
    """
    cands = list(candidates)
    cons = dict(constraints)
    round_ = 0
    prev_residual: int | None = None

    while True:
        traj = sigma_trajectory(cands, cons, target)
        resolved = traj.sigma is not None
        residual = len(traj.survivors_left)
        # the growth-κ knee: node birth is past the knee once its last round stopped making bulk
        # progress — a residual drop of ≤ 1 means it resolves the tail one bespoke rival at a time.
        at_knee = prev_residual is not None and (prev_residual - residual) <= 1

        grew = False
        new_cands: list[str] = []
        new_cons: dict[str, list[str]] = {}
        if not resolved:
            new_cands, new_cons = propose(traj.survivors_left, round_)
            grew = bool(new_cands) or bool(new_cons)

        verdict = loop_verdict(resolved, traj.falsifiable, grew, round_, max_rounds, at_knee)
        if verdict != CONTINUE:
            mechanism = target if verdict == RESOLVED else None
            return Result(verdict, mechanism, round_, traj)

        prev_residual = residual  # the residual before this birth, for the next round's knee test
        for c in new_cands:  # node birth: merge the grown state
            if c not in cands:
                cands.append(c)
        cons.update(new_cons)
        round_ += 1

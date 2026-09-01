"""homeostat.clinic — the end-to-end clinical read, for ONE person over a PRIOR web.

Composes the engine primitives into SYSTEM_DESIGN.md §9's control flow, replacing the retired
node-birth loop (`loop.resolve_presentation`): there is NO growing — a plural residual is resolved
by ASKING for the highest-value dimension (Jeeves), never by inventing a node.

The flow (each step a built, pinned piece):
1. **Position** the presentation off the person's own mined zero (`position.py`, upstream — the
   caller supplies `positions`; the peer-set that feeds `mine_zero` is object-led, §13.1).
2. **Observed = sign ≠ 0.** A node at baseline (the informational zero) abstains, not a symptom.
3. **Positive constraints** from reachability over the web (`web.kill_matrix` — the web's directed
   couplings already carry the earned directions).
4. **Two-sign eliminate** (`search.eliminate_two_sign`): positive constraints ∧ negative `censors`.
5. **Verdict**: a unique falsifiable survivor is the mechanism; a certified ⊥ is "no lawful
   mechanism"; a plural residual becomes the Jeeves question (`select_probe`) or an abstention.

Object-agnostic: `positions`, `censors`, and `probes` are DATA the caller supplies (the web-build
pipeline will produce the censors from GO/Reactome physics-orthogonality + treatment-response).
"""

from __future__ import annotations

from dataclasses import dataclass

from homeostat.jeeves import Probe, select_probe
from homeostat.position import Position
from homeostat.search import Trajectory, eliminate_two_sign
from homeostat.web import RelationalWeb, kill_matrix

RESOLVED = "resolved"  # a unique, falsifiable survivor — the mechanism to interrogate
DEGENERATE = "degenerate"  # a lone survivor, no plurality to falsify — self-confirming, no finding
BOTTOM = "bottom"  # a censor ruled out every candidate — certified non-membership ("no mechanism")
ASK = "ask"  # a plural residual, and a probe would discriminate it — the Jeeves question
ABSTAIN = "abstain"  # a plural residual no available dimension separates — the informational zero


@dataclass(frozen=True)
class ClinicalResult:
    """The outcome of a clinical read. `verdict` is one of the codes above. `mechanism` is the
    survivor on RESOLVED, else None; `probe` is the next question on ASK, else None; `trajectory`
    is the two-sign trajectory (its `survivors_left` is the residual, empty on BOTTOM).
    """

    verdict: str
    mechanism: str | None
    probe: Probe | None
    trajectory: Trajectory


def observed_symptoms(positions: dict[str, Position]) -> list[str]:
    """The nodes with a real deviation — sign ≠ 0, sorted. A node at baseline (the informational
    zero, sign 0) is NOT an observed symptom: it abstains. Pure over `dict[str, Position]`.
    """
    return [node for node in sorted(positions) if positions[node].sign != 0]


def clinical_verdict(bottom: bool, is_resolved: bool, is_falsifiable: bool, has_probe: bool) -> str:
    """Map the two-sign trajectory (+ whether Jeeves found a probe) to a clinical verdict code.

    A certified ⊥ outranks all (BOTTOM). A unique survivor is RESOLVED if the σ_sem>0 guard holds,
    else DEGENERATE (self-confirming). A plural residual becomes ASK when a probe would discriminate
    it, else ABSTAIN (no available dimension separates the survivors). Total over `(bool,)*4`.
    """
    if bottom:
        return BOTTOM
    if is_resolved:
        return RESOLVED if is_falsifiable else DEGENERATE
    return ASK if has_probe else ABSTAIN


def read_presentation(
    web: RelationalWeb,
    positions: dict[str, Position],
    censors: dict[str, list[str]],
    probes: list[Probe],
    min_weight: float = 0.0,
) -> ClinicalResult:
    """Read one person's positioned presentation over the prior web, two-sign, returning the
    verdict (the mechanism, a certified ⊥, the next Jeeves question, or an honest abstention).
    I/O-free orchestration over the pinned `kill_matrix` / `eliminate_two_sign` /
    `clinical_verdict` / `select_probe`; validated by hand-authored intent tests.
    """
    observed = observed_symptoms(positions)
    candidates, constraints = kill_matrix(web, observed, min_weight)
    traj = eliminate_two_sign(candidates, constraints, dict(censors))
    is_resolved = traj.sigma is not None
    stuck = not is_resolved and not traj.bottom
    probe = select_probe(traj.survivors_left, list(probes)) if stuck else None
    verdict = clinical_verdict(traj.bottom, is_resolved, traj.falsifiable, probe is not None)
    mechanism = traj.survivors_left[0] if verdict == RESOLVED else None
    return ClinicalResult(verdict, mechanism, probe, traj)

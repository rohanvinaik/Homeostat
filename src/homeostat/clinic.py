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

from collections.abc import Collection, Iterable
from dataclasses import dataclass

from homeostat.event import Event, active_censors, events_to_censors, events_to_web
from homeostat.jeeves import Probe, select_probe
from homeostat.position import Position
from homeostat.search import Trajectory, eliminate_two_sign
from homeostat.signal import Tier
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
    is the two-sign trajectory (its `survivors_left` is the residual, empty on BOTTOM). `certified`
    is True only when the verdict is a certificate (BOTTOM/RESOLVED) resting on VERIFIED evidence;
    `certification_tier` is the weakest-link tier of the observations the read consumed — the read
    naming its own trust boundary (TAG: the verdict code is never collapsed to a weaker one).
    """

    verdict: str
    mechanism: str | None
    probe: Probe | None
    trajectory: Trajectory
    certified: bool = False
    certification_tier: Tier = Tier.VERIFIED


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


_TIER_RANK = {Tier.VERIFIED.value: 2, Tier.REPORTED.value: 1, Tier.ABSENT.value: 0}


def weakest_tier(tiers: list[str]) -> str:
    """The weakest (least-certifying) tier among the observations — VERIFIED > REPORTED > ABSENT.
    An empty set has no weakening evidence, so it is vacuously VERIFIED. Pure over the Tier values;
    the weakest-link envelope warrant (Regenesis SSL: a chain is as warranted as its weakest datum).
    """
    weakest = Tier.VERIFIED.value
    for t in tiers:
        if _TIER_RANK.get(t, 0) < _TIER_RANK.get(weakest, 0):
            weakest = t
    return weakest


def is_certified(verdict: str, weakest: str) -> bool:
    """CERTIFIED only if the verdict is a certificate (BOTTOM or RESOLVED) AND its weakest
    load-bearing observation is VERIFIED. A REPORTED datum is a run-kill — it constrains the read
    but banks nothing toward certification (NEGATIVE_SPECIFICATION Def. 1.4). Pure `(str, str)`.
    """
    return verdict in (BOTTOM, RESOLVED) and weakest == Tier.VERIFIED.value


def read_presentation(
    web: RelationalWeb,
    positions: dict[str, Position],
    censors: dict[str, list[str]],
    probes: list[Probe],
    min_weight: float = 0.0,
) -> ClinicalResult:
    """Read one person's positioned presentation over the prior web, two-sign, returning the
    verdict (the mechanism, a certified ⊥, the next Jeeves question, or an honest abstention),
    TAGGED with whether it is certified — a certificate resting on any REPORTED observation is
    reported UNCERTIFIED, never silently collapsed. I/O-free orchestration over the pinned
    `kill_matrix` / `eliminate_two_sign` / `clinical_verdict` / `select_probe` / `is_certified`;
    validated by hand-authored intent tests.
    """
    observed = observed_symptoms(positions)
    candidates, constraints = kill_matrix(web, observed, min_weight)
    traj = eliminate_two_sign(candidates, constraints, dict(censors))
    is_resolved = traj.sigma is not None
    stuck = not is_resolved and not traj.bottom
    probe = select_probe(traj.survivors_left, list(probes)) if stuck else None
    verdict = clinical_verdict(traj.bottom, is_resolved, traj.falsifiable, probe is not None)
    mechanism = traj.survivors_left[0] if verdict == RESOLVED else None
    weakest = weakest_tier([positions[n].tier.value for n in observed])
    certified = is_certified(verdict, weakest)
    return ClinicalResult(verdict, mechanism, probe, traj, certified, Tier(weakest))


def read_from_events(
    events: Iterable[Event],
    positions: dict[str, Position],
    active_roles: Collection[str],
    probes: list[Probe],
    directed_networks: Collection[str],
    min_weight: float = 0.0,
) -> ClinicalResult:
    """End-to-end read from a multi-network event stream — SYSTEM_DESIGN.md §10's encode → resolve.

    Compiles the events into the positive web (`events_to_web`) and the role-scoped censors
    active in this presentation (`events_to_censors` then `active_censors`), then runs the
    two-sign `read_presentation`. `active_roles` (the roles this presentation implicates) is
    supplied by the caller (object-led); nothing here decides what makes a role active. I/O-free
    orchestration over the pinned encoders and read; intent-tested.
    """
    web = events_to_web(events, directed_networks)
    censors = active_censors(events_to_censors(events), active_roles)
    return read_presentation(web, positions, censors, probes, min_weight)

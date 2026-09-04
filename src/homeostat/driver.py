"""homeostat.driver — the read as a RECOMMENDATION over mechanisms (the Dr. House protocol).

Generate wide, resolve narrow (H2): from one person's positioned deviations, the driver produces the
ranked candidate mechanisms, a certified ⊥, or an honest abstention -- never a single predicted
answer. The composition, all judgment-free glue over pinned pieces:

  REQUIRE (hard) -- relevance = the DIRECTED-reachability ancestor cone of the observed shadow
     (`ancestor_cone`/`induced_subweb` over the directed sub-web); `kill_matrix` is positive
     elimination; the polarity censor (`polarity_censors`) + role censors are the negative
     sign. `eliminate_two_sign` runs both signs to a survivor / certified ⊥ / plurality.
  PREFER (soft) -- `rank_candidates` orders the survivors by kappa-coverage through the ModelAtlas
     blend (`score_candidate`); convergence / rarity / absence / coherence fold in as wired.

The verdict names its own trust boundary; a plural residual yields the Jeeves DO-THIS probe. This is
the ONE place all the layers meet; it holds no biology of its own.
"""

from __future__ import annotations

from collections.abc import Collection, Iterable, Mapping
from dataclasses import dataclass

from homeostat.clinic import clinical_verdict, observed_symptoms
from homeostat.event import Event, active_censors, events_to_censors, events_to_web
from homeostat.jeeves import Probe, select_probe
from homeostat.polarity import polarity_censors, signed_adjacency
from homeostat.position import Position
from homeostat.recommend import score_candidate
from homeostat.search import Trajectory, coverage, eliminate_two_sign
from homeostat.web import RelationalWeb, ancestor_cone, induced_subweb, kill_matrix, nodes

DIRECTED_NETWORKS = frozenset(
    {"regulatory"}
)  # the one directed-mechanism tier (Law 5); shared w/ prior_web


def rank_candidates(
    survivors: list[str], positive_kill_sets: list[list[str]], n_observed: int
) -> list[tuple[str, float]]:
    """Rank surviving candidates into the recommendation: each scored by its kappa-coverage
    alignment (`coverage / n_observed`, in [0, 1]) through the PREFER blend, descending. Soft
    signals (convergence, rarity, absence, coherence) fold into `score_candidate` as they wire in.
    Ties keep input order (stable sort). `n_observed <= 0` -> every score 0.0. Pure.
    """
    if n_observed <= 0:
        return [(s, 0.0) for s in survivors]
    scored = [
        (s, score_candidate([coverage(s, positive_kill_sets) / n_observed], [])) for s in survivors
    ]
    return sorted(scored, key=lambda t: t[1], reverse=True)


@dataclass(frozen=True)
class DriverRead:
    """The driver's output. `verdict` is the clinic code (RESOLVED/BOTTOM/DEGENERATE/ASK/ABSTAIN);
    `ranked` is the recommendation (candidate, prefer-score) descending -- the mechanism on
    RESOLVED, the plurality on ASK/ABSTAIN, empty on BOTTOM; `probe` is the DO-THIS on ASK;
    `trajectory` is the two-sign σ-trajectory; `censored` is what each censor ruled out; `dropped`
    are observed deviations with no directed context (not explainable by a directed mechanism).
    """

    verdict: str
    ranked: list[tuple[str, float]]
    probe: Probe | None
    trajectory: Trajectory
    censored: dict[str, list[str]]
    dropped: list[str]


def drive(
    events: Iterable[Event],
    positions: Mapping[str, Position],
    verb_sign: Mapping[str, int],
    active_roles: Collection[str] = (),
    probes: Iterable[Probe] = (),
    min_weight: float = 0.0,
) -> DriverRead:
    """Read one person's positioned deviations end-to-end (generate-wide → resolve-narrow → rank).

    Scopes to the DIRECTED-reachability cone of the observed (relevance, never declared), runs
    two-sign elimination with the polarity-opposition + role censors, and ranks the survivors by
    kappa-coverage. Observed deviations with no directed context are dropped and reported. I/O-free
    orchestration over the pinned pieces; intent-tested + validated end-to-end.
    """
    events = list(events)
    web = events_to_web(events, DIRECTED_NETWORKS)
    directed = RelationalWeb(tuple(c for c in web.couplings if c.direction != 0))
    observed = observed_symptoms(dict(positions))

    scoped = induced_subweb(directed, ancestor_cone(directed, observed, min_weight))
    in_web = set(nodes(scoped))
    observed_scoped = [o for o in observed if o in in_web]
    dropped = [o for o in observed if o not in in_web]

    candidates, constraints = kill_matrix(scoped, observed_scoped, min_weight)
    signed = signed_adjacency(events, verb_sign)
    obs_signs = {o: positions[o].sign for o in observed_scoped}
    censors: dict[str, list[str]] = {"polarity": polarity_censors(signed, candidates, obs_signs)}
    censors.update(active_censors(events_to_censors(events), active_roles))

    traj = eliminate_two_sign(candidates, constraints, censors)
    is_resolved = traj.sigma is not None
    stuck = not is_resolved and not traj.bottom
    probe = select_probe(traj.survivors_left, list(probes)) if stuck else None
    verdict = clinical_verdict(traj.bottom, is_resolved, traj.falsifiable, probe is not None)
    ranked = rank_candidates(traj.survivors_left, list(constraints.values()), len(observed_scoped))
    return DriverRead(verdict, ranked, probe, traj, censors, dropped)

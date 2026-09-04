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
from homeostat.narrative import StoryRead, read_story
from homeostat.polarity import polarity_censors, signed_adjacency
from homeostat.position import Position
from homeostat.recommend import score_candidate
from homeostat.search import Trajectory, coverage, eliminate_two_sign
from homeostat.web import (
    RelationalWeb,
    ancestor_cone,
    distances_to,
    induced_subweb,
    kill_matrix,
    nodes,
)

DIRECTED_NETWORKS = frozenset(
    {"regulatory"}
)  # the one directed-mechanism tier (Law 5); shared w/ prior_web


def rank_candidates(
    survivors: list[str],
    positive_kill_sets: list[list[str]],
    n_observed: int,
    convergence: Mapping[str, float] | None = None,
    coherence: Mapping[str, float] | None = None,
) -> list[tuple[str, float]]:
    """Rank surviving candidates into the recommendation: each scored by its kappa-coverage
    alignment (`coverage / n_observed`, in [0, 1]), optionally TIMES a COHERENCE alignment factor (a
    candidate that coheres as a mechanism for the shadow is boosted, one that does not is demoted),
    TIMES the PREFER soft blend. CONVERGENCE (normalized by its max) is the soft tie-breaker.
    Descending; ties keep input order. Absent coherence/convergence for a candidate -> that factor
    is neutral. `n_observed <= 0` -> alignment 0 -> every score 0.0. Pure.
    """
    conv = convergence or {}
    coh = coherence or {}
    max_conv = max(conv.values(), default=0.0)

    def _score(s: str) -> float:
        align = [coverage(s, positive_kill_sets) / n_observed if n_observed > 0 else 0.0]
        if s in coh:
            align.append(coh[s])
        soft = [conv[s] / max_conv] if s in conv and max_conv > 0 else []
        return score_candidate(align, soft)

    return sorted(((s, _score(s)) for s in survivors), key=lambda t: t[1], reverse=True)


def proximity_coherence(observed: list[str], reverse_adj: dict[str, list[str]]) -> dict[str, float]:
    """Local STRUCTURAL coherence -- the self-contained default (a Regenesis-native SEMANTIC
    coherence can be supplied to `drive` to override it). A candidate regulating the shadow through
    SHORT/direct paths tells a more parsimonious mechanism than a distant, entangled one:
    coherence(C) = mean over the observed C reaches of `1 / (1 + dist(C, O))`, in (0, 1]. One
    reverse-BFS per observed; a candidate reaching no observed is absent. Pure.
    """
    total: dict[str, float] = {}
    count: dict[str, int] = {}
    for o in observed:
        for c, d in distances_to(reverse_adj, o).items():
            total[c] = total.get(c, 0.0) + 1.0 / (1 + d)
            count[c] = count.get(c, 0) + 1
    return {c: total[c] / count[c] for c in total}


@dataclass(frozen=True)
class DriverRead:
    """The driver's output. `verdict` is the clinic code (RESOLVED/BOTTOM/DEGENERATE/ASK/ABSTAIN);
    `story` is the presentation-level STORY-READ over the surviving structure -- the genre account,
    plural, no single subject (the answer is a story, not a ranked gene); `probe` is the DO-THIS on
    ASK; `trajectory` is the two-sign σ-trajectory; `censored` is what each censor ruled out;
    `dropped` are observed deviations with no directed context (not explainable by a directed
    mechanism).
    """

    verdict: str
    story: StoryRead
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
    proteins: Mapping[str, str] | None = None,
    min_weight: float = 0.0,
) -> DriverRead:
    """Read one person's positioned deviations end-to-end (generate-wide → resolve-narrow → STORY).

    Scopes to the DIRECTED-reachability cone of the observed (relevance, never declared), runs
    two-sign elimination with the polarity-opposition + role censors, then reads the surviving
    structure as a STORY (`narrative.read_story` over the scoped events) -- the presentation-level
    genre account, not a ranked gene. Observed deviations with no directed context are dropped and
    reported. I/O-free orchestration over the pinned pieces; intent-tested + validated end-to-end.
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
    # PREFER: read the surviving structure as a STORY -- the genre account over the scoped events
    # (the events whose coupling lives inside the observed cone), not a ranked gene. The story is
    # read over the WHOLE scoped structure (the plurality is what it is read over, never collapsed).
    scoped_events = [e for e in events if e.subject in in_web and e.target in in_web]
    story = read_story(scoped_events, observed_scoped, proteins)
    return DriverRead(verdict, story, probe, traj, censors, dropped)

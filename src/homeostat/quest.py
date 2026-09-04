"""homeostat.quest — the Epic Quest mechanism-genre: the roundabout resolution, read native.

Where tragedy is the doom-cascade and comedy the mutual loop, the **epic quest** is the INDIRECT
cure: a DISTANT node (the hero, not phenotype-adjacent) that resolves the presentation by BRIDGING
otherwise-disjoint parts of the observed shadow — the κ-super-additive move, "stimulants reaching
inflammation", the hero arriving from the unexpected direction (THESIS ch.9; STORY_LAYER §3). It is
the one genre that needs the OBSERVED shadow: a bridge is only an epic quest if the disjoint parts
it joins ARE the presentation.

The verdict is the COHERENCE of the roundabout resolution, read as a Kuramoto ORDER PARAMETER over
the ouroboros ring (THESIS: "frozen is not atemporal … the ring is ordered"):

- Each observed part the hero joins sits at a PHASE on the ring — a PHASOR whose angle is its OTP
  net-sign from the hero (SUPPORT → 0 in-phase; OPPOSE → π ANTIPHASE, inhibition) rotated by its
  causal-ring position (Bellman-Ford `depth`), so same-sign parts at different depths fall out of
  phase — time-agnostic but NOT time-blind. The informational zero (ORTHOGONAL) is the ZERO VECTOR:
  no opinion is no phasor — it neither reinforces nor cancels, yet still COUNTS (it dilutes r; never
  excluded).
- Coherence = the TRUE order parameter r = |mean phasor| ∈ [0, 1] (transported native, like kappa
  transported significance — NOT a confidence-weighted variance, the ablated TriageGeist fake).
  Destructive interference falls out of vector ADDITION: opposing phases subtract. r ≈ 1 phase-LOCKS
  the joined loops (a coherent, minimal-entropy stable resolution); r ≈ 0 couples without locking.

CAUTION (THEORY_OF_THE_CASE, honest cautions): a Kuramoto coherence layer was once ablated as
inert-to-negative — because it was a fake order parameter used as a ranking metric. Here it is a
STRUCTURAL genre verdict read off the mechanism. Never assume it carries ranking signal: when the
recommendation layer later sorts story-reads, THAT is where `min_coherence` must be MEASURED (not
assumed). The genre reader computes coherence honestly; the ranker earns the right to trust it.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from math import cos, hypot, pi, sin

from homeostat.event import Event
from homeostat.kappa import weak_components
from homeostat.otp import ORTHOGONAL, SUPPORT
from homeostat.topology import signed_adjacency
from homeostat.tragedy import net_signs, reach_graph


@dataclass(frozen=True)
class Quest:
    """One epic quest: the `hero` (a distant bridge) resolving the observed `joined` parts through a
    roundabout path, with the Kuramoto `coherence` (r ∈ [0, 1], the honest measurement) and the
    `verdict` — ``"resolving"`` (phase-locked: a coherent distant cure), ``"entangling"`` (coupled
    but not locked), or ``"indeterminate"`` (the informational zero: no coherence axis)."""

    hero: str
    joined: tuple[str, ...]
    coherence: float
    verdict: str


def part_vector(net_sign: int, depth: int, max_depth: int) -> tuple[float, float]:
    """One observed part's PHASOR on the ouroboros coherence ring, as an ``(x, y)`` unit vector.

    SUPPORT → angle 0 (in-phase), OPPOSE → angle π (ANTIPHASE — inhibition), each rotated by the
    part's causal-ring position (``2π·depth/max_depth``) so same-sign parts at different depths are
    out of phase (the ring is ordered — not time-blind). ORTHOGONAL (the informational zero) → the
    ZERO VECTOR ``(0.0, 0.0)``: no opinion is no phasor — it neither reinforces nor cancels the
    coherence, yet still counts when summed over the parts (dilution, never exclusion). ``max_depth
    <= 0`` → no rotation. Pure over ``(ternary, int, int)``.
    """
    if net_sign == ORTHOGONAL:
        return (0.0, 0.0)
    base = 0.0 if net_sign == SUPPORT else pi
    theta = base + (2 * pi * depth / max_depth if max_depth > 0 else 0.0)
    return (cos(theta), sin(theta))


def order_parameter(vectors: list[tuple[float, float]]) -> float:
    """The Kuramoto ORDER PARAMETER r = |mean phasor| ∈ [0, 1] over the parts' phasors — global
    phase coherence, transported native (stdlib only). Opposing phases SUBTRACT (destructive
    interference); the informational zeros add nothing but still count (dilution). r ≈ 1 (a
    coherent resolution); r ≈ 0 incoherent / all-abstain. Empty → 0.0. Pure over the phasor list.
    """
    n = len(vectors)
    if n == 0:
        return 0.0
    x = sum(v[0] for v in vectors)
    y = sum(v[1] for v in vectors)
    return hypot(x, y) / n


def quest_verdict(r: float, min_coherence: float, opinionated: int) -> str:
    """The pure quest verdict from the order parameter `r`, a coherence floor, and the count of
    OPINIONATED joined parts (net sign not the informational zero). Named codes:
    - ``"indeterminate"`` — ``opinionated <= 0``: NO coherence axis — every joined part is the
      informational zero, so there is nothing to be coherent about (abstention, not a low score);
    - ``"resolving"`` — opinions exist and ``r >= min_coherence``: the distant hero phase-LOCKS the
      joined parts (a coherent, minimal-entropy roundabout resolution);
    - ``"entangling"`` — opinions exist but ``r < min_coherence``: coupled, not locked — INCLUDING
      the r≈0 destructive-interference case (opposing opinions cancel), which is a real connection
      that does not resolve, categorically distinct from having no opinions at all.
    `min_coherence` is a PARAMETER, never a constant: per the TriageGeist ablation, the ranker that
    consumes this MUST measure it, never assume it. Pure over ``(float, float, int)``.
    """
    if opinionated <= 0:
        return "indeterminate"
    if r >= min_coherence:
        return "resolving"
    return "entangling"


def _depths(adj: dict[str, set[str]], source: str) -> dict[str, int]:
    """Forward-BFS shortest hop-depth from `source` over the reachability adjacency (the causal-ring
    position each reached node sits at). `source` is depth 0. Pure."""
    depth = {source: 0}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in adj.get(u, ()):
            if v not in depth:
                depth[v] = depth[u] + 1
                queue.append(v)
    return depth


def read_quest(
    events: Iterable[Event], observed: Iterable[str], min_coherence: float = 0.5
) -> list[Quest]:
    """Read the epic quests: for each non-observed HERO that reaches ≥2 observed parts which are in
    DIFFERENT weak components once the hero is removed (the roundabout bridge that joins otherwise-
    disjoint parts of the shadow), the Kuramoto coherence of its resolution. The hero drives an OTP
    net sign (`tragedy.net_signs`) to each joined part at its ring-`depth`; the parts' phasors
    (`part_vector`) feed the `order_parameter`, carried through the pinned `quest_verdict`.
    Orchestration over the pinned decisions + `kappa.weak_components`; intent-tested.
    """
    evs = list(events)
    obs = set(observed)
    signed = signed_adjacency(evs)
    reach = reach_graph(signed)
    out: list[Quest] = []
    for hero in sorted(reach):
        if hero in obs:
            continue  # the hero is DISTANT — not one of the observed (not phenotype-adjacent)
        depth = _depths(reach, hero)
        joined = sorted(o for o in obs if o in depth and o != hero)
        if len(joined) < 2:
            continue  # a quest bridges ≥2 observed parts
        # are the joined parts disjoint once the hero is removed? (the hero is the connector) --
        # over ALL nodes, so leaf targets (no out-edge) remain as isolated components, not dropped.
        all_nodes = set(reach) | {t for nbrs in reach.values() for t in nbrs}
        without = {u: (reach.get(u, set()) - {hero}) for u in all_nodes if u != hero}
        home = {n: i for i, comp in enumerate(weak_components(without)) for n in comp}
        if len({home.get(o) for o in joined}) < 2:
            continue  # already connected without the hero -> not a roundabout bridge
        net = net_signs(signed, hero)
        md = max(depth[o] for o in joined)
        signs = {o: net.get(o, ORTHOGONAL) for o in joined}
        vectors = [part_vector(signs[o], depth[o], md) for o in joined]
        r = order_parameter(vectors)
        opinionated = sum(1 for o in joined if signs[o] != ORTHOGONAL)
        verdict = quest_verdict(r, min_coherence, opinionated)
        out.append(Quest(hero, tuple(joined), round(r, 6), verdict))
    return sorted(out, key=lambda q: (q.hero, q.joined))

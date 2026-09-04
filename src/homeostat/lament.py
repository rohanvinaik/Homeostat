"""homeostat.lament — the TREATMENT-tier genre (POC): grieve the unfixable, route around it.

A tier-3 read OVER the dynamics genres (not the raw events) — the first treatment genre, the
template for adding more (each a few hand-pinned definitions over the dynamics reads). Where a
DOOMED tragedy has no cure — no resolving quest addresses its lost function — lament is the
therapeutic
upgrade over blind symptomatic management: recognize the loss (stop optimizing the corpse), and
cobble a FUNGIBLE stand-in (the allegory layer's role-equivalent) to hold the goal state; or, when
none exists, pure palliation — a structured steady-state decline, appeasing the dead mechanism.

The genre COMPOSES the dynamics reads: tragedy (the doom) + quest (is it curable?) + fungibility
(the stand-in). It computes the therapeutic SHAPE; it prescribes no drug and claims no purpose (that
is the clinician's, not the instrument's).
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class Lament:
    """One treatment-tier read: `mourned` is the doomed lost function; `substitute` a fungible
    stand-in that can hold its role (or None); `verdict` — ``"substituted"`` (route around the loss
    to the goal state) or ``"palliative"`` (no stand-in: recognize the loss, structured decline)."""

    mourned: str
    substitute: str | None
    verdict: str


def lament_verdict(addressed: bool, has_substitute: bool) -> str:
    """The pure treatment verdict for a doomed tragedy. Named codes:
    - ``"curable"`` — a resolving quest addresses the loss: NOT a lament, it can be fixed;
    - ``"substituted"`` — no cure, but a fungible stand-in can hold the lost role (route around it);
    - ``"palliative"`` — neither: recognize the loss and manage a structured decline.
    Pure over ``(bool, bool)``.
    """
    if addressed:
        return "curable"
    return "substituted" if has_substitute else "palliative"


def read_lament(genres: Mapping[str, list]) -> list[Lament]:
    """Read the laments: for each DOOMED tragedy whose lost function no resolving quest addresses,
    the therapeutic shape — a fungible stand-in (allegory) if one exists, else pure palliation. The
    curable ones are dropped (a quest already resolves them). Orchestration over the pinned
    `lament_verdict` + the dynamics genre instances; intent-tested.
    """
    addressed = {
        part for q in genres.get("quest", []) if q.verdict == "resolving" for part in q.joined
    }
    substitute: dict[str, str] = {}
    for f in genres.get("allegory", []):
        if f.verdict == "fungible":
            substitute.setdefault(f.a, f.b)
            substitute.setdefault(f.b, f.a)
    out: list[Lament] = []
    for t in genres.get("tragedy", []):
        if t.verdict != "doomed":
            continue
        verdict = lament_verdict(t.sink in addressed, t.sink in substitute)
        if verdict == "curable":
            continue
        out.append(Lament(t.sink, substitute.get(t.sink), verdict))
    return sorted(out, key=lambda lam: lam.mourned)

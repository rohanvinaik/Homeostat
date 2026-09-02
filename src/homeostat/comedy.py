"""homeostat.comedy — the second mechanism-genre: the mutual-regulation CYCLE, read native.

Where tragedy is the cascade that locks a sink, comedy is the LOOP — two systems that regulate each
other (a 2-cycle A<->B). Its character is the OTP **loop-gain**: the sign-PRODUCT around the ring
(the same OTP composition tragedy runs along a path, now closed on itself):

- net-SUPPORT loop -> ``"vicious"``: a reinforcing / bistable-locked cycle — mutual amplification,
  OR mutual inhibition (a mutual-disinhibition toggle, ``-1 * -1 = +1``). The ironic comedy: every
  compensation compounds.
- net-OPPOSE loop -> ``"homeostatic"``: a NEGATIVE-feedback loop that self-corrects — the classical
  comedy, perturbation -> compensation -> restored setpoint (the happy ending / certified-⊥).
- the informational zero -> ``"indeterminate"``: a mixed-polarity edge leaves the loop-gain no view.

v1 reads the atomic mutual PAIR (the 2-cycle — the founder's "two systems that mutually reinforce").
Longer directed cycles (A->B->C->A) are a real DEFERRED extension — they need the SCC/cycle
enumeration `kappa` does not yet carry — so this reports mutual pairs only, and says so.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from homeostat.event import Event
from homeostat.otp import OPPOSE, SUPPORT
from homeostat.topology import signed_adjacency


@dataclass(frozen=True)
class Comedy:
    """One mutual-regulation cycle: the pair `a` < `b` regulating each other, with the loop-gain
    verdict — ``"vicious"`` (net-SUPPORT: reinforcing/locked), ``"homeostatic"`` (net-OPPOSE:
    self-correcting negative feedback), or ``"indeterminate"`` (the informational zero)."""

    a: str
    b: str
    verdict: str


def loop_verdict(loop_gain: int) -> str:
    """The pure comedy verdict from a cycle's loop-gain (the sign-product around the ring). Named
    codes, never bools:
    - ``"vicious"`` — net-SUPPORT: the loop reinforces itself (mutual amplification or a mutual-
      inhibition toggle) and locks — the ironic comedy;
    - ``"homeostatic"`` — net-OPPOSE: negative feedback, the loop self-corrects (classical comedy);
    - ``"indeterminate"`` — the informational zero: a mixed-polarity edge, so no coherent loop-gain.
    Pure over the ternary loop-gain.
    """
    if loop_gain == SUPPORT:
        return "vicious"
    if loop_gain == OPPOSE:
        return "homeostatic"
    return "indeterminate"


def read_comedy(events: Iterable[Event]) -> list[Comedy]:
    """Read the comedies (mutual-regulation cycles) in a regulatory event stream: each pair with
    edges BOTH ways, classified by its loop-gain (the OTP sign-product of the two edges) through the
    pinned `loop_verdict`. Each unordered pair once (a < b). A feed-forward graph with no mutual
    regulation yields nothing (a cascade, not a loop). Orchestration over the pinned decision +
    `topology.signed_adjacency`; intent-tested.
    """
    signed = signed_adjacency(events)
    seen: set[tuple[str, str]] = set()
    out: list[Comedy] = []
    for u, nbrs in signed.items():
        for v, sign_uv in nbrs.items():
            if v in signed and u in signed[v]:  # the reverse edge exists -> a mutual cycle
                pair = (u, v) if u < v else (v, u)
                if pair in seen:
                    continue
                seen.add(pair)
                loop_gain = sign_uv * signed[v][u]
                out.append(Comedy(pair[0], pair[1], loop_verdict(loop_gain)))
    return sorted(out, key=lambda c: (c.a, c.b))

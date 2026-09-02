"""homeostat.topology — the shared genre-layer substrate: OTP algebra + the signed regulatory graph.

The mechanism-genres (tragedy, comedy, …) are read off the coupling web's TOPOLOGY, and they share
two primitives, hoisted here on the second genre's use so a genre depends on a shared substrate and
never sideways on a sibling genre:

- **`otp_combine`** — the OTP ternary MERGE: two drives agree, or collapse to the info zero.
- **`signed_adjacency`** — the SIGNED regulatory graph from the events (amplify=+1, inhibit=−1, a
  mixed pair = the informational zero). Existence is polarity-blind — a signed-0 edge still couples.
"""

from __future__ import annotations

from collections.abc import Iterable

from homeostat.event import Event
from homeostat.otp import OPPOSE, ORTHOGONAL, SUPPORT

REGULATORY = "regulatory"
_VERB_SIGN = {"amplifies": SUPPORT, "inhibits": OPPOSE}


def otp_combine(a: int, b: int) -> int:
    """OTP merge of two ternary contributions to one node: their shared value if they AGREE, else
    the informational zero ORTHOGONAL — two drives that disagree on sign leave the net with no view
    (the Monty-Hall move: only a coherent, agreeing drive is an opinion). Pure over the ternary
    alphabet. (Kept in the genre layer, not otp.py, which deliberately excludes combinators.)"""
    return a if a == b else ORTHOGONAL


def signed_adjacency(events: Iterable[Event]) -> dict[str, dict[str, int]]:
    """Directed regulatory adjacency `{subject: {target: net_sign}}`, self-loops dropped. An edge's
    sign is the OTP combination of its parallel regulatory verbs: pure amplify -> SUPPORT, pure
    inhibit -> OPPOSE, a mix (the same pair both amplified AND inhibited) -> the informational zero
    — an existing coupling whose POLARITY the data leaves indeterminate. Orchestration over
    `otp_combine`; intent-tested.
    """
    adj: dict[str, dict[str, int]] = {}
    for e in events:
        if e.network == REGULATORY and e.subject != e.target and e.verb in _VERB_SIGN:
            sign = _VERB_SIGN[e.verb]
            row = adj.setdefault(e.subject, {})
            row[e.target] = otp_combine(row[e.target], sign) if e.target in row else sign
    return adj

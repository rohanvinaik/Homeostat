"""homeostat.person — the input layer's ASSEMBLY: one turn of the operator/computer interface.

Take what the operator holds THIS turn — the diagnosis (a label), the labs (measured
observations), the hypotheses (intuition) — test it against the geometry, and hand back the read:
verdict + story + ranked mechanisms + the σ_sem completeness + the mechanism-level Jeeves DO-THIS
(the machine's precise counter-ask). The operator responds — measures the DO-THIS node, adds it as
a lab — and calls again; the loop runs to SETTLED (RESOLVED / certified-⊥ / honest abstention).
Every input is a TESTED operator-proposal; the diagnosis restricts the mechanism SEARCH (option B),
never the observed shadow.

I/O-free over pre-loaded substrate (the caller loads the prior web, the GWAS catalog trait-index,
the marker reference): diagnosis → the relevant subspace (`relevance`), labs → positions
(`producer`), then `drive` with `relevant=` the subspace. Integration-tested end to end.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping

from homeostat.driver import DriverRead, drive
from homeostat.event import Event
from homeostat.fungibility import read_fungibility
from homeostat.producer import signals_to_positions
from homeostat.relevance import fungible_map, relevant_subspace
from homeostat.signal import Signal


def read_person(
    diagnosis: str,
    labs: Iterable[Signal],
    events: Iterable[Event],
    verb_sign: Mapping[str, int],
    trait_index: Mapping[str, set[str]],
    *,
    demographics: Mapping[str, str],
    reference: Callable[[str, Mapping[str, str]], tuple[float, float] | None],
    vocab: dict[str, str],
    proteins: Mapping[str, str] | None = None,
    hypotheses: Iterable[Event] = (),
    band: float = 0.0,
) -> DriverRead:
    """One turn of the interface: the operator's `diagnosis` + `labs` + `hypotheses` → the read.

    The diagnosis → the possibly-relevant gene subspace (its GWAS-associated genes widened by earned
    fungibility); the labs → the shadow (`signals_to_positions`); then `drive` with `relevant=` the
    subspace, so only relevant sources are eligible mechanisms — the shadow stays sacrosanct, and a
    certified-⊥ results if the label's subspace does not explain it. The returned read carries the
    Jeeves DO-THIS — the machine's counter-ask the operator answers next turn. Orchestration.
    """
    events = list(events)
    subspace = relevant_subspace(
        diagnosis, trait_index, fungible_map(read_fungibility(events, proteins))
    )
    positions = signals_to_positions(labs, demographics, reference, vocab)
    return drive(
        events,
        positions,
        verb_sign,
        proteins=proteins,
        hypotheses=hypotheses,
        band=band,
        relevant=subspace,
    )

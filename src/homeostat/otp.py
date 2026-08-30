"""homeostat.otp — the signed-ternary / informational-zero decision substrate.

The one shared, DOMAIN-FREE primitive of the coherence instrument: a signal's state
on an axis is a signed-ternary value ``{-1, 0, +1}`` off a reference, where the **0 is
the informational zero** — honest abstention ("this axis has no opinion here"), NOT a
small or missing magnitude. It is the OTP atom of the portfolio (Peitho ``otp.py``,
gse/HDC), written fresh for this project — not repurposed statistical code.

Deliberately object-agnostic and carrying NO statistics and NO coherence mechanism.
This module is ONLY the ternary projection. The coherence combinator (constraint
elimination over the constraint object) is a separate, later layer, because
Homeostat's coherence is ELIMINATION, not a Peitho-style consensus vote-tally —
importing that tally here would be exactly the "clever repurposing" the design forbids.
"""

from __future__ import annotations

# The OTP ternary alphabet. Integers on purpose so the zero is inert under any later
# combinator: the informational zero contributes nothing and so concentrates a decision
# on the axes that DO have an opinion (the Monty-Hall move).
SUPPORT: int = 1  # +1 — above the reference by more than the tolerance band
OPPOSE: int = -1  # -1 — below the reference by more than the tolerance band
ORTHOGONAL: int = 0  # 0 — the informational zero: no opinion (out of domain, or within tolerance)


def ternary(deviation: float | None, tol: float) -> int:
    """Project a signed deviation-from-reference onto the OTP ternary ``{-1, 0, +1}``.

    The informational zero (``ORTHOGONAL``) covers the two honest-abstention cases and
    ONLY those: ``deviation is None`` (no reading on this axis — out of domain) and
    ``abs(deviation) <= band`` (at the reference, within tolerance). A deviation strictly
    above ``+band`` is ``SUPPORT`` (+1); strictly below ``-band`` is ``OPPOSE`` (-1). The
    band is ``abs(tol)``, so a negative tolerance can never invert the projection. Pure
    over ``(float | None, float)``.
    """
    if deviation is None:
        return ORTHOGONAL
    band = abs(tol)
    if deviation > band:
        return SUPPORT
    if deviation < -band:
        return OPPOSE
    return ORTHOGONAL

"""homeostat.reference_fetch — the demographic reference-range shell (HMDB serum), PARSE-LOCAL.

Feeds the marker producer's `reference(node, demographics) -> [low, high] | None` seam (Law 1's one
sanctioned population read: the reference lights a pixel of the SHADOW, never the mechanism --
docs/decisions/marker_reference.md). Source: HMDB `serum_metabolites.xml` (hmdb.ca/downloads), free
for research use (cite the HMDB paper).

HMDB is Cloudflare-gated: no client (`urllib`/`curl`/WebFetch) can download it -- only a browser
passes the challenge. So `ensure` is PARSE-LOCAL: it checks for the file a human/browser placed and
instructs, never auto-downloads. HMDB gives per-study `mean +/- sd` (or an explicit range), NOT a
single published interval, and MULTIPLE studies per metabolite/demographic; the shell takes ONE
Normal-condition study per key and NEVER aggregates across studies (that would be mining). This
module holds the pure decisions; the streaming XML load + lookup are its I/O half.
"""

from __future__ import annotations

import re

DEFAULT_K = 2.0  # mean +/- k*sd -> the 95% reference band (the standard clinical convention)

_MEAN_SD = re.compile(r"^\s*([0-9]+\.?[0-9]*)\s*\+/-\s*([0-9]+\.?[0-9]*)\s*$")
_RANGE = re.compile(r"([0-9]+\.?[0-9]*)\s*-\s*([0-9]+\.?[0-9]*)")


def parse_interval(value: str, k: float) -> tuple[float, float] | None:
    """Parse an HMDB `concentration_value` into a reference ``[low, high]``, or None (abstain). The
    two GIVEN forms: ``mean +/- sd`` -> ``[mean - k*sd, mean + k*sd]`` (a deterministic
    transform of the study's reported distribution); and an explicit range ``low-high`` (bare or
    parenthetical, e.g. ``4.2 (3.1-5.4)``) -> ``[low, high]``. A bare value, a ``<N``, or an
    unparseable/degenerate (low >= high) string abstains -- an interval is never fabricated. Pure
    over `(str, float)`.
    """
    m = _MEAN_SD.match(value)
    if m:
        mean, sd = float(m.group(1)), float(m.group(2))
        return (mean - k * sd, mean + k * sd)
    r = _RANGE.search(value)
    if r:
        low, high = float(r.group(1)), float(r.group(2))
        if low < high:
            return (low, high)
    return None


def is_normal(condition: str) -> bool:
    """True iff the condition is the healthy baseline (``Normal``, case-insensitive -- catches
    the ``normal`` lowercase variant) -- the only condition a reference range may be drawn from. A
    disease / drug / diet condition is not a reference. Pure over `str`.
    """
    return condition.strip().lower() == "normal"


def age_bucket(age: float) -> str:
    """Map a numeric age in YEARS to HMDB's coarse subject_age bucket. Boundaries follow HMDB's own
    vocabulary (newborn < 30d, infant < 1y, children < 13, adolescent < 18, else adult). Pure over
    `float`.
    """
    if age < 30.0 / 365.0:
        return "newborn"
    if age < 1.0:
        return "infant"
    if age < 13.0:
        return "children"
    if age < 18.0:
        return "adolescent"
    return "adult"


def hmdb_age_bucket(raw: str) -> str:
    """Normalize an HMDB `subject_age` string to the same bucket as `age_bucket`: the first word,
    lowercased (``"Adult (>18 years old)"`` -> ``"adult"``, ``"Children (1 - 13 years old)"`` ->
    ``"children"``). ``"Not Specified"`` -> ``"not"``; empty -> ``"unspecified"``. Pure over `str`.
    """
    head = raw.strip().split(" ", 1)[0].lower()
    return head or "unspecified"

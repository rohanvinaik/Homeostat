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
import zipfile
from collections.abc import Callable, Mapping
from pathlib import Path
from xml.etree import ElementTree as ET

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


_NS = "{http://www.hmdb.ca}"
ReferenceTable = dict[tuple[str, str, str], tuple[float, float]]


def _absorb(table: ReferenceTable, mname: str, c: ET.Element, k: float) -> None:
    """Fold one <concentration> into the table iff it is a Normal Blood reading with a parseable
    interval, keyed by (metabolite, sex, age_bucket), FIRST-WINS -- never aggregating across studies
    (that would be mining). Orchestration over the pinned parse decisions.
    """
    if not is_normal(c.findtext(f"{_NS}subject_condition") or ""):
        return
    if (c.findtext(f"{_NS}biospecimen") or "").strip().lower() not in {"blood", "serum"}:
        return
    interval = parse_interval(c.findtext(f"{_NS}concentration_value") or "", k)
    if interval is None:
        return
    sex = (c.findtext(f"{_NS}subject_sex") or "").strip().lower()
    bucket = hmdb_age_bucket(c.findtext(f"{_NS}subject_age") or "")
    table.setdefault((mname, sex, bucket), interval)


def load_serum(zip_path: str | Path, k: float = DEFAULT_K) -> ReferenceTable:
    """Stream-parse the local HMDB serum_metabolites.xml (inside its zip) into the reference table
    {(metabolite_lower, sex, age_bucket): (low, high)} over Normal Blood concentrations. Streaming
    (iterparse + clear) so the 1.3 GB XML never lands in memory. I/O over the pinned decisions.
    """
    table: ReferenceTable = {}
    with zipfile.ZipFile(zip_path) as zf, zf.open(zf.namelist()[0]) as fh:
        for _event, elem in ET.iterparse(fh, events=("end",)):
            if elem.tag != f"{_NS}metabolite":
                continue
            mname = (elem.findtext(f"{_NS}name") or "").strip().lower()
            ncs = elem.find(f"{_NS}normal_concentrations")
            if mname and ncs is not None:
                for c in ncs.findall(f"{_NS}concentration"):
                    _absorb(table, mname, c, k)
            elem.clear()
    return table


def ensure(path: str | Path) -> Path:
    """PARSE-LOCAL guard: HMDB is Cloudflare-gated, so this NEVER auto-downloads. Returns `path` if
    the serum zip is present, else raises with the exact browser-download instruction.
    """
    p = Path(path)
    if p.is_file():
        return p
    raise FileNotFoundError(
        f"HMDB serum reference data not found at {p}. HMDB is Cloudflare-gated (no client can "
        "download it): open hmdb.ca/downloads in a browser, download 'Serum Metabolites' "
        f"(serum_metabolites.zip), and place it at {p}."
    )


def make_reference(
    table: ReferenceTable,
) -> Callable[[str, Mapping[str, str]], tuple[float, float] | None]:
    """Build the marker producer's `reference(node, demographics)` closure over
    a loaded table: match the metabolite (lowercased node), then the sex (exact -> both -> not
    specified -> any) and age bucket (from demographics['age'] -> exact -> not -> unspecified),
    first hit wins; abstain on no match. Orchestration.
    """

    def reference(node: str, demographics: Mapping[str, str]) -> tuple[float, float] | None:
        mname = node.strip().lower()
        sex = str(demographics.get("sex", "")).strip().lower()
        bucket = age_bucket(float(demographics["age"])) if demographics.get("age") else ""
        for s in (sex, "both", "not specified", ""):
            for ab in (bucket, "not", "unspecified"):
                hit = table.get((mname, s, ab))
                if hit is not None:
                    return hit
        return None

    return reference

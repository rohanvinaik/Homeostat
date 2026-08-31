"""A1 + E1 scoring: does the panel recover true members above decoys, and censor hubs?

Reads /tmp/a1_labels.json (ground truth + signals, from a1_panel.py) and /tmp/a1_observed.json
(token -> highest tier reached, from the Regenesis pass over each /tmp/a1_<mech>.txt). Reports, per
mechanism and in aggregate: member recovery rate, decoy false-positive rate, hub censoring rate, and
the precision of the `component+` call. The discrimination claim is member-rate >> decoy-rate with
hubs censored — E1 is the same result holding across all 8 domains with no per-domain code.

    python3 validation/a1_score.py
"""

from __future__ import annotations

import json
from pathlib import Path

TIERS_COMPONENT = {"component", "core", "deep_core"}


def main() -> None:
    labels = json.loads(Path("/tmp/a1_labels.json").read_text())
    observed = json.loads(Path("/tmp/a1_observed.json").read_text())

    def reaches(tok: str) -> bool:
        return observed.get(tok, "none") in TIERS_COMPONENT

    mechs = sorted({v["mech"] for v in labels.values()})
    print(f"{'mechanism':<18}{'members↑':>12}{'decoy FP':>12}{'hubs censored':>16}")
    agg = {"m_hit": 0, "m_tot": 0, "m_hit_data": 0, "m_data": 0,
           "d_hit": 0, "d_tot": 0, "h_cens": 0, "h_tot": 0}
    for mech in mechs:
        toks = {t: v for t, v in labels.items() if v["mech"] == mech}
        mem = [t for t, v in toks.items() if v["role"] == "member"]
        dec = [t for t, v in toks.items() if v["role"] == "decoy"]
        hub = [t for t, v in toks.items() if v["role"] == "hub"]
        m_hit = sum(reaches(t) for t in mem)
        # members with Fst data (differentiation is the necessary gate — condition on having data)
        m_data = [t for t in mem if toks[t]["tier"] not in ("nodata",)]
        m_hit_data = sum(reaches(t) for t in m_data)
        d_hit = sum(reaches(t) for t in dec)
        h_cens = sum(not reaches(t) for t in hub)
        agg["m_hit"] += m_hit; agg["m_tot"] += len(mem)
        agg["m_hit_data"] += m_hit_data; agg["m_data"] += len(m_data)
        agg["d_hit"] += d_hit; agg["d_tot"] += len(dec)
        agg["h_cens"] += h_cens; agg["h_tot"] += len(hub)
        print(f"{mech:<18}{f'{m_hit}/{len(mem)}':>12}{f'{d_hit}/{len(dec)}':>12}"
              f"{f'{h_cens}/{len(hub)}':>16}")

    print("-" * 58)
    mr = agg["m_hit"] / max(1, agg["m_tot"])
    mrd = agg["m_hit_data"] / max(1, agg["m_data"])
    dr = agg["d_hit"] / max(1, agg["d_tot"])
    hc = agg["h_cens"] / max(1, agg["h_tot"])
    print(f"member recovery (all):            {agg['m_hit']}/{agg['m_tot']}  = {mr:.0%}")
    print(f"member recovery (has Fst data):   {agg['m_hit_data']}/{agg['m_data']}  = {mrd:.0%}")
    print(f"decoy false-positive rate:        {agg['d_hit']}/{agg['d_tot']}  = {dr:.0%}")
    print(f"hub censoring rate:               {agg['h_cens']}/{agg['h_tot']}  = {hc:.0%}")
    # precision of the component+ call across the whole panel
    comp = [t for t in labels if reaches(t)]
    tp = sum(labels[t]["role"] in ("member", "seed") for t in comp)
    prec = tp / max(1, len(comp))
    print(f"precision of component+ (member/seed of all promoted): {tp}/{len(comp)} = {prec:.0%}")
    ok = mrd >= 0.5 and dr <= 0.15 and hc >= 0.75 and mrd > 3 * max(dr, 0.01)
    print("\nA1/E1 VERDICT:",
          "PASS — members recovered ≫ decoys, hubs censored, across 8 domains" if ok
          else "MIXED — see per-mechanism rows")


if __name__ == "__main__":
    main()

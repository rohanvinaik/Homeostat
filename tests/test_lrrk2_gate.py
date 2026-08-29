"""Intent tests for the v2 LRRK2 gate: participation-based bridge metric +
within-2-hops coupling, on synthetic graphs (control names, no real data)."""

import random

from homeostat.lrrk2_gate import (
    _within_hops,
    evaluate_preregistered,
    gene_pbs_weights,
    label_propagation,
)


def test_label_propagation_recovers_two_cliques():
    a = ["A1", "A2", "A3", "A4"]
    b = ["B1", "B2", "B3", "B4"]
    edges = []
    for cl in (a, b):
        for i in range(len(cl)):
            for j in range(i + 1, len(cl)):
                edges.append((cl[i], cl[j]))
    adj = _adj(*edges)
    comm = label_propagation(adj, sorted(adj))
    assert len({comm[x] for x in a}) == 1
    assert len({comm[x] for x in b}) == 1
    assert comm["A1"] != comm["B1"]


def _adj(*edges):
    a: dict[str, set[str]] = {}
    for u, v in edges:
        a.setdefault(u, set()).add(v)
        a.setdefault(v, set()).add(u)
    return a


def test_within_hops():
    adj = _adj(("L", "M"), ("M", "N"))
    assert _within_hops(adj, "L", {"N"}, 2)
    assert not _within_hops(adj, "L", {"N"}, 1)
    assert _within_hops(adj, "L", {"M"}, 1)


def test_pass_when_lrrk2_spans_communities_beyond_degree_null():
    # Two 4-cliques; LRRK2 has one edge into each -> high participation.
    # NOD2/RIPK2 sit in clique 2 (NOD2-RIPK2 adjacent), LRRK2 within 2 hops.
    a1 = ["A1", "A2", "A3", "A4"]
    a2 = ["NOD2", "RIPK2", "B3", "B4"]
    edges = []
    for cl in (a1, a2):
        for i in range(len(cl)):
            for j in range(i + 1, len(cl)):
                edges.append((cl[i], cl[j]))
    edges += [("LRRK2", "A1"), ("LRRK2", "NOD2")]
    adj = _adj(*edges)
    w = {"LRRK2": 0.09, "NOD2": 0.08, "RIPK2": 0.05}
    ev = evaluate_preregistered(adj, w, random.Random(0))
    # LRRK2 (degree 2, edges span both cliques) has participation 0.5; the
    # degree-2 clique-internal genes... none here, band may be small — assert the
    # structural facts the metric computes, not a fragile p-threshold.
    assert ev["clause_a_triad_couples"]
    assert ev["clause_a_detail"]["nod2_ripk2_adjacent"]
    assert ev["clause_a_detail"]["lrrk2_within_2hops"]
    assert ev["clause_b_detail"]["lrrk2_participation"] > 0.4  # spans two communities


def test_fail_when_triad_disconnected():
    adj = _adj(("LRRK2", "A"), ("NOD2", "B"), ("RIPK2", "C"))
    ev = evaluate_preregistered(adj, {"LRRK2": 0.1, "NOD2": 0.1, "RIPK2": 0.1}, random.Random(0))
    assert not ev["clause_a_triad_couples"]
    assert ev["verdict"] == "FAIL"


def test_not_evaluable_when_uncovered():
    adj = _adj(("LRRK2", "A"), ("NOD2", "RIPK2"))
    ev = evaluate_preregistered(adj, {}, random.Random(0))
    assert ev["verdict"].startswith("NOT-EVALUABLE")


def test_gene_pbs_weights_takes_envelope_max(tmp_path):
    import gzip

    pile = tmp_path / "pile.tsv.gz"
    with gzip.open(pile, "wt") as f:
        f.write("chrom\tpos\tref\talt\taf_csa\taf_eur\taf_eas\tmaf_csa\tfst_csa_eur\tpbs_csa\n")
        for pos, pbs in [(1000, 0.2), (1500, 0.5), (9_000_000, 0.9)]:
            f.write(f"1\t{pos}\tA\tG\t0.3\t0.2\t0.25\t0.3\t0.05\t{pbs}\n")
    envelopes = {"GENEX": ("1", 1200, 1400)}
    w = gene_pbs_weights(str(pile), envelopes)
    assert w["GENEX"] == 0.5

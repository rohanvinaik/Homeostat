"""Intent tests for the LRRK2-gate evaluation on synthetic graphs — the
preregistered clauses, with the control names, no real data."""

import random

from homeostat.lrrk2_gate import evaluate_preregistered, gene_pbs_weights


def _adj(*edges):
    a: dict[str, set[str]] = {}
    for u, v in edges:
        a.setdefault(u, set()).add(v)
        a.setdefault(v, set()).add(u)
    return a


def test_clause_a_couples_but_component_metric_is_illposed():
    # LRRK2 edges to A (cluster {A,B}) and NOD2 (cluster {NOD2,RIPK2}); NOD2-RIPK2
    # adjacent. Clause A holds. But clause B's "distinct components among LRRK2's
    # neighbors" is ILL-POSED for an existing node: LRRK2 itself merges the two
    # clusters into ONE weak component, so components_joined == 1, never >= 2.
    # This documents the metric bug (see run record) — the correct measure is a
    # cut-vertex / participation test, not neighbor-component counting.
    adj = _adj(("A", "B"), ("NOD2", "RIPK2"), ("LRRK2", "A"), ("LRRK2", "NOD2"))
    w = {"LRRK2": 0.09, "NOD2": 0.08, "RIPK2": 0.05}
    ev = evaluate_preregistered(adj, w, random.Random(0))
    assert ev["clause_a_triad_couples"]
    assert ev["clause_a_detail"]["nod2_ripk2_adjacent"]
    assert ev["clause_b_detail"]["lrrk2_components_joined"] == 1  # the ill-posedness
    assert not ev["clause_b_lrrk2_bridges"]


def test_fail_when_triad_disconnected():
    adj = _adj(("LRRK2", "A"), ("NOD2", "B"), ("RIPK2", "C"))
    ev = evaluate_preregistered(adj, {"LRRK2": 0.1, "NOD2": 0.1, "RIPK2": 0.1}, random.Random(0))
    assert not ev["clause_a_triad_couples"]
    assert ev["verdict"] == "FAIL"


def test_not_evaluable_when_uncovered():
    adj = _adj(("LRRK2", "A"), ("NOD2", "RIPK2"))
    ev = evaluate_preregistered(adj, {}, random.Random(0))  # no pile coverage
    assert ev["verdict"].startswith("NOT-EVALUABLE")


def test_gene_pbs_weights_takes_envelope_max(tmp_path):
    import gzip

    pile = tmp_path / "pile.tsv.gz"
    with gzip.open(pile, "wt") as f:
        f.write("chrom\tpos\tref\talt\taf_csa\taf_eur\taf_eas\tmaf_csa\tfst_csa_eur\tpbs_csa\n")
        for pos, pbs in [(1000, 0.2), (1500, 0.5), (9_000_000, 0.9)]:
            f.write(f"1\t{pos}\tA\tG\t0.3\t0.2\t0.25\t0.3\t0.05\t{pbs}\n")
    envelopes = {"GENEX": ("1", 1200, 1400)}  # ±25kb window catches 1000 and 1500
    w = gene_pbs_weights(str(pile), envelopes)
    assert w["GENEX"] == 0.5  # max PBS in the envelope, not the far 0.9

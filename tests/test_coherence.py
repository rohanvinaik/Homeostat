"""Intent tests for the Regenesis semantic-coherence producer — authored from the design, not
generated. The pure scoring (`coherence_from_patterns`) is also Detective-pinned; the impure
`coherence_from_regenesis` shell is validated end-to-end through the real `drive`."""

import json

from homeostat.coherence import (
    VERB_LEMMA,
    coherence_from_patterns,
    event_contract,
    events_to_contracts,
)
from homeostat.event import Event

# subject->gene map (identity on the contracts path: subjects come back as the real gene names).
SIDECAR = {"Gene1": "TP53", "Gene2": "MDM2", "Gene3": "BAX"}


def _pat(name, subject, significance):
    return {"name": name, "subject": subject, "significance": significance}


def test_depth_ranks_the_deep_role_at_one_and_scales_the_rest():
    # A gene whose role fired on a DEEP chain (sig 4.0) coheres at 1.0; a shallow role (1.0) at 0.25
    # -- max-normalized, the same shape rank_candidates uses for convergence.
    pats = [_pat("amplifier", "Gene1", 4.0), _pat("inhibitor", "Gene2", 1.0)]
    assert coherence_from_patterns(pats, SIDECAR) == {"TP53": 1.0, "MDM2": 0.25}


def test_subject_maps_back_through_the_sidecar_to_the_gene():
    # the coherence map is keyed by the REAL gene, never the opaque story token.
    assert coherence_from_patterns([_pat("binder", "Gene3", 2.0)], SIDECAR) == {"BAX": 1.0}


def test_gse_lowercased_subject_still_maps_to_the_gene():
    # GSE emit LOWERCASES the opaque token, so `understand` returns subject='gene3' while sidecar
    # keys are 'Gene3'. The join must reconcile case or every gene silently drops (the {} bug the
    # empirical gate caught). Regression: a lowercased subject still maps.
    assert coherence_from_patterns([_pat("binder", "gene3", 2.0)], SIDECAR) == {"BAX": 1.0}


def test_subject_absent_from_the_sidecar_is_dropped():
    # a recognized subject with no sidecar entry (not a rendered gene) -> no KeyError, omit.
    pats = [_pat("amplifier", "Gene9", 3.0), _pat("inhibitor", "Gene1", 3.0)]
    assert coherence_from_patterns(pats, SIDECAR) == {"TP53": 1.0}


def test_max_role_per_gene_is_the_deepest_role_not_the_last_seen():
    # a gene subject of two Forms keeps its DEEPEST role's significance (MAX), not the last-written
    # one. Gene1's deep role (3.0) comes FIRST and its shallow role (1.0) LAST, so last-write-wins
    # would pick 1.0 -- the second gene anchors normalization so max vs last-write diverge.
    pats = [
        _pat("component", "Gene1", 3.0),  # deep role, seen FIRST
        _pat("amplifier", "Gene1", 1.0),  # shallow role, seen LAST
        _pat("inhibitor", "Gene2", 2.0),
    ]
    # max: TP53=3.0, MDM2=2.0, top=3.0 -> {1.0, 2/3}. (last-write picks TP53=1.0 -> DIFFERENT map.)
    assert coherence_from_patterns(pats, SIDECAR) == {"TP53": 1.0, "MDM2": 2.0 / 3.0}


def test_non_numeric_significance_is_treated_as_zero_and_omitted():
    # the isinstance guard's point: a significance that is not a number (a stray string) is NOT
    # coerced -> it degrades to 0.0 -> the gene is omitted, never crashes, never over-fires.
    pats = [_pat("amplifier", "Gene1", "deep"), _pat("inhibitor", "Gene2", 2.0)]
    assert coherence_from_patterns(pats, SIDECAR) == {"MDM2": 1.0}


def test_pattern_missing_the_significance_key_defaults_to_zero_and_is_omitted():
    # a recognized pattern with no `significance` field -> default 0.0 -> omitted (no role depth).
    pats = [{"name": "amplifier", "subject": "Gene1"}, _pat("inhibitor", "Gene2", 2.0)]
    assert coherence_from_patterns(pats, SIDECAR) == {"MDM2": 1.0}


def test_any_positive_significance_however_small_normalizes_and_never_abstains():
    # a lone TINY role (0.05) still normalizes to 1.0 -- the top<=0.0 guard is a zero/empty floor
    # ONLY, never an abstention/filter on genuinely-positive coherence, however small. (Kills the
    # top<=0.1 and filter>0.1 mutants -- a small-chain-improbability real role must survive.)
    assert coherence_from_patterns([_pat("amplifier", "Gene1", 0.05)], SIDECAR) == {"TP53": 1.0}


def test_non_str_subject_is_skipped_gracefully_not_crashed():
    # patterns are typed Mapping[str, object] -- subject can be any object. A non-str subject cannot
    # map to a gene, so the isinstance guard SKIPS it (never `.lower()`-crashes). Pins the guard's
    # real intent -- the differential proved `if subject`/`if True` crash here; the original omits.
    assert (
        coherence_from_patterns(
            [{"name": "amplifier", "subject": 123, "significance": 3.0}], SIDECAR
        )
        == {}
    )
    assert (
        coherence_from_patterns(
            [{"name": "amplifier", "subject": None, "significance": 3.0}], SIDECAR
        )
        == {}
    )


def test_zero_significance_is_omitted_not_zeroed():
    # a shallow over-fire (sig 0.0) has no DEPTH -> OMITTED (neutral in the ranker), never a
    # 0.0 that would multiply the candidate's coverage to zero. This is the drive() seam contract.
    pats = [_pat("amplifier", "Gene1", 0.0), _pat("inhibitor", "Gene2", 2.0)]
    assert coherence_from_patterns(pats, SIDECAR) == {"MDM2": 1.0}


def test_empty_patterns_is_no_signal():
    # abstention / nothing recognized -> {} (no coherence signal), never a crash.
    assert coherence_from_patterns([], SIDECAR) == {}


def test_all_zero_significance_is_no_signal():
    # every role a shallow over-fire -> max is 0 -> {} (guard is `> 0`, no ZeroDivision).
    pats = [_pat("amplifier", "Gene1", 0.0), _pat("inhibitor", "Gene2", 0.0)]
    assert coherence_from_patterns(pats, SIDECAR) == {}


# ---- the pure contract emitter (the subprocess-free path) ------------------------


def test_event_contract_is_the_understand_event_envelope():
    # real gene names as entity lemmas, type_thread [] (opaque, no world lookup), verb_classes=
    # [verb] (what the Form fires on), verb_thread [] (unneeded). Coreference via entity_id.
    node = event_contract("TP53", "amplify", "BAX", "e0", "e1")
    assert node == {
        "contract_version": "2.0",
        "predicate": {
            "op": "EVENT",
            "args": [
                {"entity_id": "e0", "lemma": "TP53", "type_thread": []},
                {"entity_id": "e1", "lemma": "BAX", "type_thread": []},
            ],
            "features": {"verb": "amplify", "verb_thread": [], "verb_classes": ["amplify"]},
        },
    }


def test_verb_lemma_maps_every_l2_verb_to_a_centroid():
    # the 5 distinct L2 role-verbs each map to their mechanism-universe class-centroid lemma.
    assert VERB_LEMMA == {
        "amplifies": "amplify",
        "inhibits": "inhibit",
        "binds": "bind",
        "channels": "channel",
        "resembles": "resemble",
    }


def test_events_to_contracts_lemmatizes_and_corefers_genes():
    # a gene appearing in two events gets ONE stable entity id (coreference -> multi-hop depth); the
    # surface verb is lemmatized; one JSONL line per event.
    evs = [
        Event("regulatory", "amplifies", "TP53", "BAX", 1),
        Event("regulatory", "amplifies", "TP53", "BBC3", 1),
    ]
    lines = events_to_contracts(evs).splitlines()
    assert len(lines) == 2
    nodes = [json.loads(line) for line in lines]
    # TP53 is the subject of both -> the SAME entity_id in both (coreference).
    tp53_ids = {n["predicate"]["args"][0]["entity_id"] for n in nodes}
    assert len(tp53_ids) == 1
    assert all(n["predicate"]["features"]["verb"] == "amplify" for n in nodes)  # lemmatized


def test_events_to_contracts_drops_an_unmapped_verb():
    # a verb with no VERB_LEMMA entry carries no role -> its event is skipped, never faked
    evs = [
        Event("regulatory", "amplifies", "TP53", "BAX", 1),
        Event("mystery", "frobnicates", "X", "Y", 1),  # unmapped -> dropped
    ]
    assert len(events_to_contracts(evs).splitlines()) == 1

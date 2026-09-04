"""Intent tests for the Regenesis semantic-coherence producer — authored from the design, not
generated. The pure scoring (`coherence_from_patterns`) is also Detective-pinned; the impure
`coherence_from_regenesis` shell is validated end-to-end through the real `drive`."""

from homeostat.coherence import coherence_from_patterns

# render_story sidecar is opaque-token -> real gene.
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


def test_any_positive_significance_normalizes_and_never_abstains():
    # a lone small-magnitude role (top in (0, 1]) still normalizes to 1.0 -- the top<=0.0 guard is a
    # zero/empty floor ONLY, never an abstention on genuinely-positive coherence.
    assert coherence_from_patterns([_pat("amplifier", "Gene1", 0.5)], SIDECAR) == {"TP53": 1.0}


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

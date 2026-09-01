"""Intent tests for the search-and-grow loop — authored from the design, not generated."""

from homeostat.loop import (
    BUDGET,
    CONTINUE,
    DEGENERATE,
    KNEE,
    RESOLVED,
    STUCK,
    loop_verdict,
    resolve_presentation,
    run,
)

# ---- the pure loop decision ------------------------------------------------------


def test_loop_verdict_resolved_and_falsifiable():
    assert loop_verdict(True, True, False, 0, 5, False) == RESOLVED


def test_loop_verdict_resolved_but_not_falsifiable_is_degenerate():
    assert loop_verdict(True, False, False, 0, 5, False) == DEGENERATE  # SDIS-shaped


def test_loop_verdict_continue():
    assert loop_verdict(False, False, True, 0, 5, False) == CONTINUE


def test_loop_verdict_budget_outranks_growth():
    assert loop_verdict(False, False, True, 5, 5, False) == BUDGET


def test_loop_verdict_knee_outranks_growth():
    assert loop_verdict(False, False, True, 0, 5, True) == KNEE


def test_loop_verdict_stuck_when_cannot_grow():
    assert loop_verdict(False, False, False, 0, 5, False) == STUCK


# ---- the run orchestrator --------------------------------------------------------


def _no_growth(_residual, _round):
    return [], {}


def test_run_resolves_immediately():
    r = run(["a", "b", "c"], {"k1": ["b"], "k2": ["c"]}, "a", _no_growth, max_rounds=5)
    assert r.verdict == RESOLVED
    assert r.mechanism == "a"
    assert r.rounds == 0


def test_run_degenerate_when_no_plurality():
    r = run(["a"], {}, "a", _no_growth, max_rounds=5)
    assert r.verdict == DEGENERATE
    assert r.mechanism is None


def test_run_grows_then_resolves():
    def propose(_residual, round_):
        return ([], {"g": ["b"]}) if round_ == 0 else ([], {})

    r = run(["a", "b"], {}, "a", propose, max_rounds=5)
    assert r.verdict == RESOLVED
    assert r.mechanism == "a"
    assert r.rounds == 1  # one growth round


def test_run_stuck_when_propose_cannot_grow():
    r = run(["a", "b"], {}, "a", _no_growth, max_rounds=5)
    assert r.verdict == STUCK
    assert r.mechanism is None
    assert r.trajectory.survivors_left == ["a", "b"]  # the residual


def test_run_knee_halts_tail_growth():
    # Round 0 births a constraint that kills only one rival -> residual 3->2 -> past the knee.
    def propose(_residual, round_):
        return ([], {f"k{round_}": ["b"] if round_ == 0 else ["c"]})

    r = run(["a", "b", "c"], {}, "a", propose, max_rounds=5)
    assert r.verdict == KNEE  # parsimony halt, even though propose could grow further
    assert r.rounds == 1
    assert r.trajectory.survivors_left == ["a", "c"]


def test_run_budget_stops_bulk_progress_over_time():
    # Bulk progress each round (kills two rivals -> not the knee), but the round budget bites first.
    def propose(_residual, round_):
        return ([], {f"k{round_}": ["b", "c"]})

    r = run(["a", "b", "c", "d", "e"], {}, "a", propose, max_rounds=1)
    assert r.verdict == BUDGET
    assert r.mechanism is None


# ---- the seedless presentation reader --------------------------------------------


def test_resolve_presentation_mechanism_is_the_survivor():
    # No target: eliminating a and b leaves c, and c IS the returned mechanism.
    r = resolve_presentation(["a", "b", "c"], {"k1": ["a"], "k2": ["b"]}, _no_growth, max_rounds=5)
    assert r.verdict == RESOLVED
    assert r.mechanism == "c"
    assert r.rounds == 0


def test_resolve_presentation_single_candidate_is_degenerate():
    r = resolve_presentation(["a"], {}, _no_growth, max_rounds=5)
    assert r.verdict == DEGENERATE  # a lone candidate resolves nothing (self-confirming)
    assert r.mechanism is None


def test_resolve_presentation_grows_then_resolves():
    # No constraint separates a,b at first; node birth supplies one that kills b -> a survives.
    def propose(_residual, round_):
        return ([], {"g": ["b"]}) if round_ == 0 else ([], {})

    r = resolve_presentation(["a", "b"], {}, propose, max_rounds=5)
    assert r.verdict == RESOLVED
    assert r.mechanism == "a"
    assert r.rounds == 1


def test_resolve_presentation_stuck_plural_when_cannot_grow():
    r = resolve_presentation(["a", "b"], {}, _no_growth, max_rounds=5)
    assert r.verdict == STUCK
    assert r.mechanism is None
    assert r.trajectory.survivors_left == ["a", "b"]  # the plural residual, honestly abstained

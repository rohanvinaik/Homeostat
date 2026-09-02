"""Intent tests for the L2→L3 story bridge — opaque-token SVO rendering for Regenesis.

The load-bearing property: real gene names appear ONLY in the sidecar, never in the story text —
opacity forces roles from structure, not from what GSE knows about a gene. Convergence is preserved:
the several events on one gene-pair become several sentences over the same opaque tokens."""

from homeostat.event import Event
from homeostat.story import assign_tokens, event_sentence, render_story


def test_assign_tokens_is_deterministic_deduped_sorted():
    assert assign_tokens(["TRAF6", "RIPK2", "RIPK2"]) == {"RIPK2": "Gene1", "TRAF6": "Gene2"}
    assert assign_tokens(["b", "a"]) == {"a": "Gene1", "b": "Gene2"}  # sorted, not insertion order


def test_event_sentence_is_transitive_svo():
    assert event_sentence("amplifies", "Gene1", "Gene2") == "Gene1 amplifies Gene2."


def test_render_story_hides_real_genes_in_the_sidecar_only():
    events = [Event("regulatory", "amplifies", "RIPK2", "TRAF6", 1)]
    text, sidecar = render_story(events)
    # opacity: no real gene name leaks into the reasoning text
    assert "RIPK2" not in text and "TRAF6" not in text
    # the sidecar inverts back to the real genes
    assert set(sidecar.values()) == {"RIPK2", "TRAF6"}
    # the sentence is the opaque SVO
    sub, tgt = sidecar_inverse(sidecar, "RIPK2"), sidecar_inverse(sidecar, "TRAF6")
    assert text == f"{sub} amplifies {tgt}."


def test_render_story_preserves_convergence():
    # RIPK2-TRAF6 asserted by TWO networks -> TWO sentences over the SAME tokens (conjunction fires)
    events = [
        Event("regulatory", "amplifies", "RIPK2", "TRAF6", 1),
        Event("physical", "binds", "RIPK2", "TRAF6", 1),
    ]
    text, sidecar = render_story(events)
    ripk2 = sidecar_inverse(sidecar, "RIPK2")
    traf6 = sidecar_inverse(sidecar, "TRAF6")
    assert text == f"{ripk2} amplifies {traf6}. {ripk2} binds {traf6}."


def sidecar_inverse(sidecar: dict[str, str], gene: str) -> str:
    return next(tok for tok, real in sidecar.items() if real == gene)

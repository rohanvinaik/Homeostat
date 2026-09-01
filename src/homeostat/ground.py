"""homeostat.ground — the front door: resolve a symptom to a web node, or abstain. Never guess.

The statistical poisoning got in HERE before: a substring matcher mapped "POTS" ⊂ "spots" and
pulled the wrong genes. The fix is the SymbolicSpellCheck law — **ground-or-abstain, failure
confined to NON-RECOVERY, never DESTRUCTION**. A symptom is committed to a node only when it grounds
against the web's own vocabulary; otherwise it is offered or abstained, never silently rewritten. NO
substring containment, NO frequency, NO statistics — resolution is exact grounding + a *guarded*
deterministic typo leg + a shape gate.

The load-bearing guard (a naive edit-distance leg gets this wrong): "spots" is one deletion from
"pots", so a bare typo leg would recommit the exact disaster. SSC's actual law prevents it — **a
token that is itself valid is never rewritten**. So the typo leg fires only on a token that does not
already ground as a real word, and only when a validity dictionary is supplied to prove it. Without
one, the front door is exact-ground-or-abstain — it cannot destroy a valid token, only fail a typo.

Object-AGNOSTIC: the medical `vocab` (surface form / alias → canonical node) and the `valid_words`
dictionary are DATA plugged in (the content step). Nothing here authors a symptom or a node.
"""

from __future__ import annotations

from collections.abc import Collection
from dataclasses import dataclass


@dataclass(frozen=True)
class Resolution:
    """The front door's verdict on one symptom string.

    `node` is the committed canonical node, or None when the door did not commit. `offered` is the
    rank-free set of grounded candidates surfaced for a human/next-lens to choose (never
    auto-applied). `reason` names which gate fired. A None `node` is the informational zero — an
    honest abstention, never a silent rewrite.
    """

    node: str | None
    offered: tuple[str, ...]
    reason: str


def _norm(s: str) -> str:
    """Case-fold, collapse internal whitespace, strip. Pure over `str`."""
    return " ".join(s.strip().casefold().split())


def is_opaque(token: str) -> bool:
    """A token whose *shape* forbids an auto-committed rewrite — an acronym (all-caps ≥2 letters),
    or a code shape (a digit, a hyphen/underscore, or internal caps). Such tokens are offered, never
    silently corrected (the SSC shape gate — where confident correctors do most damage). Pure over
    `str`."""
    t = token.strip()
    if len(t) < 2:
        return False
    if t.isalpha() and t.isupper():
        return True
    if any(ch.isdigit() for ch in t):
        return True
    if "-" in t or "_" in t:
        return True
    return not t.isupper() and any(ch.isupper() for ch in t[1:])


def edit_within_1(a: str, b: str) -> bool:
    """Damerau edit distance ≤ 1: equal, or one insertion / deletion / substitution / adjacent
    transposition. Deterministic and bounded (no scores, no ratios). Pure over `(str, str)`."""
    if a == b:
        return True
    la, lb = len(a), len(b)
    if abs(la - lb) > 1:
        return False
    if la == lb:
        diffs = [i for i in range(la) if a[i] != b[i]]
        if len(diffs) == 1:
            return True  # substitution
        if len(diffs) == 2 and diffs[1] == diffs[0] + 1:
            i, j = diffs
            return a[i] == b[j] and a[j] == b[i]  # adjacent transposition
        return False
    short, long = (a, b) if la < lb else (b, a)  # differ by one → insertion/deletion
    return any(short == long[:k] + long[k + 1 :] for k in range(len(long)))


def ground(query: str, vocab: dict[str, str], valid_words: Collection[str] = ()) -> Resolution:
    """Resolve `query` to a canonical node via `vocab` (surface/alias → node), or abstain.

    The gates, in order: (1) **exact** — a normalized query in `vocab` commits its node; (2) **the
    valid-token guard** — a query that is itself a real word (`valid_words`) is left UNTOUCHED,
    never rewritten (this is what keeps "spots" from ever becoming "POTS"); (3) **the shape gate** —
    an opaque token (acronym/code) is only ever *offered*, never auto-rewritten; (4) **the guarded
    typo leg** — for a non-word, non-opaque query, edit-1 aliases are collected: one grounds
    (commit), several offer (abstain-ambiguous). The typo leg fires only when `valid_words` is
    supplied, because rewriting is safe only when the guard proves the query is not already valid;
    otherwise the door is exact-or-abstain. A None `node` is an honest abstention. Bridge —
    intent-tested.
    """
    q = _norm(query)
    norm_vocab: dict[str, str] = {}
    for k, v in vocab.items():
        norm_vocab.setdefault(_norm(k), v)
    if q in norm_vocab:
        return Resolution(norm_vocab[q], (), "exact")

    guarded = len(valid_words) > 0
    if guarded and q in {_norm(w) for w in valid_words}:
        return Resolution(
            None, (), "valid token, not in the medical vocab — left untouched (no rewrite)"
        )

    cands = tuple(sorted({v for nk, v in norm_vocab.items() if edit_within_1(q, nk)}))
    if is_opaque(query):
        r = "opaque shape: offered, not committed" if cands else "opaque shape: ungrounded"
        return Resolution(None, cands, r)
    if not guarded:
        return Resolution(None, (), "no validity dictionary: exact-or-abstain (typo leg withheld)")
    if len(cands) == 1:
        return Resolution(cands[0], (), "typo → grounded")
    if len(cands) > 1:
        return Resolution(None, cands, "ambiguous: offered")
    return Resolution(None, (), "ungrounded — needs a finer lens or node-birth")

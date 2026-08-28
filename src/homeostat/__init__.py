"""Homeostat — regulatory-deficit medicine. Phase 13.1: the E/I/R PBS filter.

Stdlib-only by design: deterministic, zero-venv, crash-stable. The filesystem is
the state — every stage is idempotent and derives "what remains" from artifacts
plus done-markers, never from a mutable database.
"""

__version__ = "0.1.0"

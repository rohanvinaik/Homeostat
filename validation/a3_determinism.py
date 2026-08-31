"""A3 — determinism: same input -> byte-identical ledger, robust to hash randomization.

The historical nondeterminism bug was unordered-set iteration (cloud_rsids), whose order
varies with Python's per-process hash seed; the fix was `for g in sorted(...)`. This runs the
full probe TWICE in separate processes — which by default carry DIFFERENT PYTHONHASHSEED values
— and asserts the assembled fact-text is byte-identical. If the sorted() discipline ever
regresses, the two hash seeds will diverge and this fails.

    PYTHONPATH=src python3 validation/a3_determinism.py     # exit 0 = PASS
"""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PROBE = REPO / "probes" / "l2_lrrk2.py"
N_RUNS = 3


def _run(seed: str) -> str:
    """Run the probe with an explicit (differing) hash seed; return the assembled fact-text line."""
    env = dict(os.environ, PYTHONPATH="src", PYTHONHASHSEED=seed)
    out = subprocess.run(
        [sys.executable, str(PROBE)], cwd=REPO, env=env, capture_output=True, text=True, check=True
    ).stdout
    return out.strip().splitlines()[-1]  # the ". "-joined ASSEMBLED FACT TEXT line


def main() -> int:
    seeds = [str(s) for s in range(N_RUNS)]  # 0,1,2 -> three distinct hash seeds
    texts = [_run(s) for s in seeds]
    shas = [hashlib.sha256(t.encode()).hexdigest() for t in texts]
    ok = len(set(shas)) == 1
    print(f"A3 determinism — {N_RUNS} runs under distinct PYTHONHASHSEED ({', '.join(seeds)})")
    for s, sha in zip(seeds, shas):
        print(f"  seed={s}  sha256={sha[:16]}…")
    print(
        "PASS — byte-identical across all hash seeds"
        if ok
        else "FAIL — ledger is hash-order dependent"
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

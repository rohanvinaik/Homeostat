"""Atomic-write + hashing helpers. A crash mid-write can never leave a torn artifact."""

import hashlib
import json
import os
from pathlib import Path


def sha256(path: Path) -> str:
    """The sha256 hex digest of a file, read in 1 MB chunks (the dumps are tens of MB)."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def atomic_write_text(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def atomic_write_json(path: Path, obj: object) -> None:
    atomic_write_text(path, json.dumps(obj, indent=2, sort_keys=True) + "\n")

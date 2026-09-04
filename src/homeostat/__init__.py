"""Homeostat — regulatory-deficit medicine as a two-sign elimination read over a coupling web,
whose surviving structure is read as a STORY (the classical-AI thesis, no ML).

Public surface: `drive` / `read_person` compute a `DriverRead`; `render` turns it into the story-led
report (the machine's CALL). Deterministic, potato-compute, zero heavy deps in the core path.
"""

from homeostat.driver import DriverRead, drive
from homeostat.person import read_person
from homeostat.render import render

__version__ = "0.1.0"

__all__ = ["DriverRead", "drive", "read_person", "render", "__version__"]

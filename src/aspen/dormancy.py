# CLASSIFICATION: INTERNAL // RESTRICTED // ASPEN-COMPARTMENTED
"""Dormancy and fire events.

After a wildfire, an aspen stand can look completely dead. The rhizome
underneath survives, and it sends up new suckers faster than any seedling
could grow. ASPEN treats mass ramet loss (outage, rollback, forced
shutdown) the same way: the trunks burn, the roots remain.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from aspen.colony import Colony


@dataclass
class FireReport:
    severity: float
    burned: List[str]
    survivors: int
    rhizome_nutrients_retained: float


def fire_event(colony: "Colony", severity: float, rng: random.Random) -> FireReport:
    """Destroy roughly `severity` of all ramets. The rhizome is left as is."""
    if not 0.0 <= severity <= 1.0:
        raise ValueError("severity must be between 0 and 1")
    burned: List[str] = []
    for ramet in list(colony.ramets):
        if rng.random() < severity:
            burned.append(ramet.id)
            colony.remove(ramet)
    return FireReport(
        severity=severity,
        burned=burned,
        survivors=len(colony.ramets),
        rhizome_nutrients_retained=sum(colony.rhizome.nutrients.values()),
    )

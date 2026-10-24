# CLASSIFICATION: INTERNAL // RESTRICTED // ASPEN-COMPARTMENTED
"""The canopy: the single surface the outside world sees.

Callers never talk to a ramet directly. They send a task to the canopy,
and the canopy routes it to the ramet best placed to handle it. From the
outside, ASPEN looks like one model.
"""

from __future__ import annotations

from typing import Iterable, Optional

from aspen.ramet import Ramet


class Canopy:
    def __init__(self, ramets: Iterable[Ramet]) -> None:
        self._ramets = list(ramets)

    def route(self, domain: str) -> Optional[Ramet]:
        live = [r for r in self._ramets if r.alive]
        if not live:
            return None
        return max(live, key=lambda r: r.capacity_for(domain))

    def coverage(self, domain: str) -> float:
        return sum(r.capacity_for(domain) for r in self._ramets if r.alive)

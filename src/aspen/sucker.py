# CLASSIFICATION: INTERNAL // RESTRICTED // ASPEN-COMPARTMENTED
"""Suckering: deciding where the colony sends up new ramets.

A real aspen sends up root suckers where there is light and open ground.
ASPEN sends up a new ramet wherever demand is not being met, and where the
rhizome is rich enough to give the new ramet a strong start.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class SuckerPolicy:
    # Spawn when unmet demand in a domain is above this fraction of total demand.
    unmet_threshold: float = 0.15
    # Max new ramets per domain per epoch, before containment caps apply.
    max_suckers_per_domain: int = 4
    # One sucker per this much unmet demand.
    demand_per_sucker: float = 0.75

    def sites(self, demand: Dict[str, float], unmet: Dict[str, float]) -> List[str]:
        """Return the list of domains to sprout into (a domain may appear more than once)."""
        out: List[str] = []
        for domain, need in demand.items():
            if need <= 0:
                continue
            gap = unmet.get(domain, 0.0)
            if gap / need < self.unmet_threshold:
                continue
            count = min(self.max_suckers_per_domain, max(1, int(gap / self.demand_per_sucker)))
            out.extend([domain] * count)
        return out

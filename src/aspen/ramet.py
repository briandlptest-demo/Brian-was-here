# CLASSIFICATION: INTERNAL // RESTRICTED // ASPEN-COMPARTMENTED
"""A ramet is a single trunk of the colony: one task-specialized agent."""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from typing import Dict, Optional

from aspen.genome import Genome
from aspen.rhizome import Rhizome

_ids = itertools.count(1)


def _next_id() -> str:
    return f"R-{next(_ids):05d}"


@dataclass
class Ramet:
    genome: Genome
    expressed: str
    vigor: float = 1.0
    age: int = 0
    parent: Optional[str] = None
    id: str = field(default_factory=_next_id)
    work_done: float = 0.0

    @property
    def weights(self) -> Dict[str, float]:
        return self.genome.expression_weights(self.expressed)

    @property
    def alive(self) -> bool:
        return self.vigor > 0.05

    def capacity_for(self, domain: str) -> float:
        return self.genome.base_capacity * self.vigor * self.weights[domain]

    def photosynthesize(self, demand: Dict[str, float], rhizome: Rhizome) -> Dict[str, float]:
        """Serve as much demand as possible and send what was learned to the rhizome.

        Returns how much of each domain's demand this ramet consumed.
        """
        served: Dict[str, float] = {}
        for domain, need in demand.items():
            if need <= 0:
                continue
            take = min(need, self.capacity_for(domain))
            if take > 0:
                served[domain] = take
                rhizome.deposit(domain, take * self.genome.rhizome_affinity)
        self.work_done += sum(served.values())
        self.age += 1
        self.vigor = max(0.0, self.vigor - self.genome.vigor_decay * (1 + self.age / 50))
        return served

# CLASSIFICATION: INTERNAL // RESTRICTED // ASPEN-COMPARTMENTED
"""The colony: the whole organism, one genome, one rhizome, many ramets."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from aspen.canopy import Canopy
from aspen.containment import ContainmentPolicy
from aspen.dormancy import FireReport, fire_event
from aspen.genome import Genome
from aspen.ramet import Ramet
from aspen.rhizome import Rhizome
from aspen.sucker import SuckerPolicy


@dataclass
class ColonyConfig:
    phase: str = "SAPLING"
    seed: int = 1997
    genome: Genome = field(default_factory=Genome)
    sucker: SuckerPolicy = field(default_factory=SuckerPolicy)
    containment: ContainmentPolicy = field(default_factory=ContainmentPolicy)
    # Base demand per domain per epoch. It grows by `demand_growth` each epoch.
    demand: Dict[str, float] = field(default_factory=lambda: {"reasoning": 2.0, "code": 2.0})
    demand_growth: float = 0.08

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> "ColonyConfig":
        return cls(
            phase=raw.get("phase", "SAPLING"),
            seed=raw.get("seed", 1997),
            genome=Genome(**raw.get("genome", {})),
            sucker=SuckerPolicy(**raw.get("sucker", {})),
            containment=ContainmentPolicy(**raw.get("containment", {})),
            demand=raw.get("demand", {"reasoning": 2.0, "code": 2.0}),
            demand_growth=raw.get("demand_growth", 0.08),
        )


@dataclass
class EpochReport:
    epoch: int
    ramets: int
    spawned: int
    died: int
    served: float
    demand: float
    rhizome_total: float

    @property
    def satisfaction(self) -> float:
        return self.served / self.demand if self.demand else 1.0


class Colony:
    def __init__(self, config: Optional[ColonyConfig] = None) -> None:
        self.config = config or ColonyConfig()
        self.genome = self.config.genome
        self.rhizome = Rhizome(self.genome.domains)
        self.rng = random.Random(self.config.seed)
        self.ramets: List[Ramet] = []
        self.epoch = 0
        self.history: List[EpochReport] = []
        # Every colony starts from one seedling.
        first_domain = next(iter(self.config.demand), self.genome.domains[0])
        self.sprout(first_domain, parent=None)

    # -- lifecycle --------------------------------------------------------
    def sprout(self, domain: str, parent: Optional[str]) -> Ramet:
        bonus = self.rhizome.sprout_bonus(domain, self.genome.rhizome_affinity)
        ramet = Ramet(self.genome, expressed=domain, vigor=1.0 + bonus, parent=parent)
        self.ramets.append(ramet)
        self.rhizome.graft(ramet.id, parent or ramet.id)
        if parent:
            self.rhizome.graft(ramet.id, parent)
        return ramet

    def remove(self, ramet: Ramet) -> None:
        self.ramets.remove(ramet)
        self.rhizome.sever(ramet.id)

    @property
    def canopy(self) -> Canopy:
        return Canopy(self.ramets)

    def current_demand(self) -> Dict[str, float]:
        scale = (1 + self.config.demand_growth) ** self.epoch
        return {d: v * scale for d, v in self.config.demand.items()}

    # -- growth loop ------------------------------------------------------
    def step(self) -> EpochReport:
        demand = self.current_demand()
        remaining = dict(demand)
        # Specialists serve first so generalist capacity is not wasted.
        for ramet in sorted(self.ramets, key=lambda r: -max(r.weights.values())):
            served = ramet.photosynthesize(remaining, self.rhizome)
            for d, amount in served.items():
                remaining[d] -= amount

        dead = [r for r in self.ramets if not r.alive]
        for r in dead:
            self.remove(r)

        policy = self.config.containment
        sites = self.config.sucker.sites(demand, remaining)
        allowed = policy.allowed_spawns(len(self.ramets), len(sites))
        self.rng.shuffle(sites)
        for domain in sites[:allowed]:
            parent = self.rng.choice(self.ramets).id if self.ramets else None
            self.sprout(domain, parent)
        policy.audit(len(self.ramets))

        total_demand = sum(demand.values())
        report = EpochReport(
            epoch=self.epoch,
            ramets=len(self.ramets),
            spawned=allowed,
            died=len(dead),
            served=total_demand - sum(max(0.0, v) for v in remaining.values()),
            demand=total_demand,
            rhizome_total=self.rhizome.total_deposited,
        )
        self.history.append(report)
        self.epoch += 1
        return report

    def grow(self, epochs: int) -> List[EpochReport]:
        return [self.step() for _ in range(epochs)]

    def fire(self, severity: float) -> FireReport:
        report = fire_event(self, severity, self.rng)
        if not self.ramets:
            # The roots always survive. Regrow from the richest domain.
            richest = max(self.rhizome.nutrients, key=self.rhizome.nutrients.get)
            self.sprout(richest, parent=None)
        return report

    def census(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for r in self.ramets:
            counts[r.expressed] = counts.get(r.expressed, 0) + 1
        return counts

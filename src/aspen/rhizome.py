# CLASSIFICATION: INTERNAL // RESTRICTED // ASPEN-COMPARTMENTED
"""The rhizome: the shared root system underneath every ramet.

Ramets come and go. The rhizome stays. Each ramet deposits what it learns
(its "nutrients") into the rhizome, and each new ramet draws on that store
when it sprouts. This is why the colony gets *cheaper* to grow as it gets
bigger. It is also why the rhizome is the most sensitive asset in ASPEN.
"""

from __future__ import annotations

import math
from collections import defaultdict
from typing import Dict, Iterable, Set


class Rhizome:
    """Shared memory store plus the connectivity graph between ramets."""

    def __init__(self, domains: Iterable[str]) -> None:
        self.nutrients: Dict[str, float] = {d: 0.0 for d in domains}
        self.edges: Dict[str, Set[str]] = defaultdict(set)
        self.total_deposited: float = 0.0

    # -- nutrient flow ----------------------------------------------------
    def deposit(self, domain: str, amount: float) -> None:
        if amount < 0:
            raise ValueError("cannot deposit a negative amount")
        self.nutrients[domain] += amount
        self.total_deposited += amount

    def richness(self, domain: str) -> float:
        """Diminishing-returns view of how much the colony knows about a domain."""
        return math.log1p(self.nutrients[domain])

    def sprout_bonus(self, domain: str, affinity: float) -> float:
        """Starting vigor bonus a new ramet gets from the existing root system."""
        return affinity * self.richness(domain)

    # -- connectivity -----------------------------------------------------
    def graft(self, a: str, b: str) -> None:
        if a == b:
            return
        self.edges[a].add(b)
        self.edges[b].add(a)

    def sever(self, node: str) -> None:
        for peer in self.edges.pop(node, set()):
            self.edges[peer].discard(node)

    @property
    def node_count(self) -> int:
        return len(self.edges)

    def snapshot(self) -> Dict[str, float]:
        return {d: round(v, 3) for d, v in self.nutrients.items()}

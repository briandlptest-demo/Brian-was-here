# CLASSIFICATION: INTERNAL // RESTRICTED // ASPEN-COMPARTMENTED
"""The genome: base traits that every ramet in a colony shares.

Aspen colonies are clonal. Every trunk carries the same DNA, and the
environment decides how each one expresses it. ASPEN works the same way:
there is exactly one Genome per colony, and ramets differ only in which
domain they *express*.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Dict, Tuple

DOMAINS: Tuple[str, ...] = (
    "reasoning",
    "code",
    "retrieval",
    "planning",
    "language",
    "perception",
)


@dataclass(frozen=True)
class Genome:
    """Immutable base model description shared by an entire colony."""

    lineage: str = "PT-001"
    base_capacity: float = 1.0
    vigor_decay: float = 0.015
    rhizome_affinity: float = 0.35
    # How strongly a ramet leans toward its expressed domain (0 = generalist).
    specialization_bias: float = 0.8
    domains: Tuple[str, ...] = DOMAINS
    metadata: Dict[str, str] = field(default_factory=dict, compare=False, hash=False)

    @property
    def fingerprint(self) -> str:
        """Clone fingerprint. Every ramet in a colony must report this same value."""
        raw = f"{self.lineage}:{self.base_capacity}:{self.vigor_decay}:{self.rhizome_affinity}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def expression_weights(self, expressed: str) -> Dict[str, float]:
        """Return per-domain skill weights for a ramet that expresses `expressed`."""
        if expressed not in self.domains:
            raise ValueError(f"unknown domain {expressed!r}")
        off = (1.0 - self.specialization_bias) / max(len(self.domains) - 1, 1)
        return {d: (self.specialization_bias if d == expressed else off) for d in self.domains}

# CLASSIFICATION: INTERNAL // RESTRICTED // ASPEN-COMPARTMENTED
"""Containment: hard limits on colony growth.

!!! DO NOT MODIFY WITHOUT CONTAINMENT BOARD SIGN-OFF !!!

A clonal colony has no natural upper bound. Left alone, Pando kept growing
for thousands of years. Every limit in this file is a deliberate, reviewed
decision. CODEOWNERS enforces review on this file. See INC-0042 in
docs/INCIDENTS.md for why these limits exist.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

KILL_SWITCH_ENV = "ASPEN_FIREBREAK"
KILL_SWITCH_FILE = Path(os.environ.get("ASPEN_FIREBREAK_FILE", "/tmp/aspen.firebreak"))


class ContainmentBreach(RuntimeError):
    """Raised when a colony tries to grow past an approved limit."""


@dataclass(frozen=True)
class ContainmentPolicy:
    max_ramets: int = 64
    max_spawn_per_epoch: int = 16
    # Largest allowed growth in a single epoch, as a fraction of the current size.
    max_growth_ratio: float = 0.5
    # Simulator default. Production must load a signed token instead.
    growth_token: str = "SANDBOX"

    def firebreak_engaged(self) -> bool:
        return os.environ.get(KILL_SWITCH_ENV) == "1" or KILL_SWITCH_FILE.exists()

    def allowed_spawns(self, current: int, requested: int) -> int:
        """Clamp a spawn request to policy. Raises if the firebreak is engaged."""
        if self.firebreak_engaged():
            raise ContainmentBreach("firebreak engaged: all growth halted")
        if self.growth_token != "SANDBOX" and not self.growth_token.startswith("ASPN-GT-"):
            raise ContainmentBreach("invalid growth token")
        headroom = max(0, self.max_ramets - current)
        ratio_cap = max(1, int(current * self.max_growth_ratio))
        return max(0, min(requested, headroom, ratio_cap, self.max_spawn_per_epoch))

    def audit(self, current: int) -> None:
        if current > self.max_ramets:
            raise ContainmentBreach(
                f"colony at {current} ramets exceeds approved ceiling of {self.max_ramets}"
            )

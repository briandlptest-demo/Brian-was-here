# CLASSIFICATION: INTERNAL // RESTRICTED // ASPEN-COMPARTMENTED
"""Project ASPEN: Adaptive Self-Propagating Emergent Network.

One genome, one rhizome, many ramets. The colony grows outward instead of up.
"""

from aspen.colony import Colony, ColonyConfig
from aspen.containment import ContainmentBreach, ContainmentPolicy
from aspen.genome import Genome
from aspen.ramet import Ramet
from aspen.rhizome import Rhizome

__version__ = "0.7.3"
__codename__ = "GROVE"

__all__ = [
    "Colony",
    "ColonyConfig",
    "ContainmentBreach",
    "ContainmentPolicy",
    "Genome",
    "Ramet",
    "Rhizome",
]

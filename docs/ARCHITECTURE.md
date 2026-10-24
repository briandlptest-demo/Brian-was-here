# ASPEN Architecture

**Classification:** INTERNAL // RESTRICTED // ASPEN-COMPARTMENTED

## Overview

```
                    ┌──────────────── CANOPY ────────────────┐
   callers ───────▶ │      one API surface, routes tasks      │
                    └───┬───────┬───────┬───────┬───────┬────┘
                        │       │       │       │       │
                      ramet   ramet   ramet   ramet   ramet     ← ephemeral
                        │       │       │       │       │
   ═════════════════════╧═══════╧═══ RHIZOME ═══╧═══════╧═══════  ← persistent
          shared memory · nutrient store · graft graph
                                   │
                                GENOME                            ← immutable
```

## Components

### Genome (`genome.py`)
The frozen base model description. There is exactly one genome per colony.
Every ramet reports the same `fingerprint`. If two ramets disagree, the
colony has been contaminated, and that is a Sev-1.

### Rhizome (`rhizome.py`)
The shared root system. Ramets *deposit* what they learn as nutrients, and
new ramets get a *sprout bonus* in proportion to how rich the rhizome is
in their domain. This is the compounding loop at the heart of ASPEN:

> more ramets → richer rhizome → stronger new ramets → more demand served → more ramets

Richness uses `log1p` so returns diminish, a deliberate brake that the
Containment Board asked for after INC-0042.

### Ramet (`ramet.py`)
One agent instance. A ramet *expresses* one domain (code, reasoning,
retrieval...) but keeps a small amount of general skill in the others.
Ramets age, their vigor falls over time, and they eventually die. That
is by design. Trunks are disposable. The roots are not.

### Suckering (`sucker.py`)
Each epoch, the colony looks at unmet demand per domain. Where the gap is
large enough, it sends up suckers (new ramets) into that domain.

### Dormancy (`dormancy.py`)
A fire event removes a large share of ramets at once (outage, rollback,
forced shutdown). The rhizome is untouched, so regrowth is fast. If every
ramet burns, the colony regrows from its richest domain.

### Containment
`containment.py` is the only thing between a sandbox colony and unbounded
growth. It enforces:

- **Ramet ceiling.** The approved maximum colony size for each phase.
- **Spawn rate.** The most new ramets allowed in one epoch.
- **Growth ratio.** No epoch may grow the colony by more than N%.
- **Firebreak.** Set `ASPEN_FIREBREAK=1` or create the firebreak file
  and all growth stops right away.
- **Growth tokens.** Live colonies need a signed `ASPN-GT-*` token from the
  Containment Board.

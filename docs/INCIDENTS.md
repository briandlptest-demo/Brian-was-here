# Incident Log (Summary)

**Classification:** INTERNAL // RESTRICTED // ASPEN-COMPARTMENTED

## INC-0042: Runaway suckering in SAPLING sandbox
**Severity:** 1 · **Status:** Resolved

A config typo set `unmet_threshold: 0.0`. Every epoch, every domain counted
as underserved. The colony grew from 12 to 3,900 ramets in 41 epochs before
the sandbox ran out of memory. The rhizome kept compounding the whole time,
and each new ramet was stronger than the last.

**Fixes:**
- Added `max_growth_ratio` and `max_spawn_per_epoch` to `ContainmentPolicy`.
- Switched rhizome richness from linear to `log1p`.
- Added `scripts/firebreak.sh` and the `ASPEN_FIREBREAK` kill switch.
- Put `containment.py` under mandatory Containment Board review in CODEOWNERS.

## INC-0057: Genome fingerprint drift
**Severity:** 2 · **Status:** Under investigation

Two ramets in a GROVE test colony reported different fingerprints after a
hot reload. Root cause not yet confirmed. Hot reloads are frozen until it is.

<!--
  ╔══════════════════════════════════════════════════════════════════╗
  ║  CLASSIFICATION: INTERNAL // RESTRICTED // ASPEN-COMPARTMENTED    ║
  ║  Distribution limited to personnel read in to PROJECT ASPEN.      ║
  ╚══════════════════════════════════════════════════════════════════╝
-->

> **⚠️ INTERNAL ONLY — RESTRICTED — ASPEN COMPARTMENT**
>
> This repository and everything in it is confidential. Do not clone it to
> personal devices, paste it into external tools, or talk about it outside
> the ASPEN channel. Access is logged. See [SECURITY.md](SECURITY.md).

# Project ASPEN 🌳

**Adaptive Self-Propagating Emergent Network**

`PROGRAM: ASPEN` · `ACTIVE PHASE: GROVE` · `ENVIRONMENT: OFFLINE SANDBOX`

[Mission roadmap](docs/ROADMAP.md) · [Architecture](docs/ARCHITECTURE.md) ·
[Incident archive](docs/INCIDENTS.md) · [Handling protocol](SECURITY.md)

*An experimental test repository presented as a fictional classified program.
Codenames, contacts, incidents, and clearance requirements are part of the story;
the Python colony simulator is runnable.*

> *"From a distance it looks like a forest. Underground, it is one organism."*

ASPEN is an experimental AI system modeled on the quaking aspen
(*Populus tremuloides*). A single aspen grows a large underground root
system (the **rhizome**) and sends up new trunks (**ramets**) wherever
conditions are good. What looks like thousands of separate trees is often
one genetically identical organism. The largest known colony, *Pando*,
covers 106 acres and is thought to be thousands of years old.

ASPEN applies the same idea to AI agents:

| Aspen biology      | ASPEN system                                                      |
|--------------------|-------------------------------------------------------------------|
| Seed / clone       | **Genome**: a shared base model, its weights and its policy        |
| Rhizome            | **Rhizome**: shared memory and message graph that links every agent |
| Ramet (trunk)      | **Ramet**: one task-specialized agent instance                    |
| Root sucker        | **Suckering**: spawning a new ramet where demand is detected      |
| Canopy             | **Canopy**: the combined, user-facing capability surface          |
| Dormancy / fire    | **Dormancy**: ramets die off; the rhizome survives and regrows     |
| Pando              | **PANDO milestone**: one colony at 47,000 ramets (the full target) |

The thesis: **a small seed system should not be scaled up. It should be
allowed to grow outward.** Every ramet makes the rhizome richer, and a
richer rhizome makes the next ramet cheaper and better.

---

## Mission status

**Current objective: stabilize GROVE before authorizing STAND.** The active
storyline blocker is [INC-0057: genome fingerprint drift](docs/INCIDENTS.md#inc-0057-genome-fingerprint-drift).

| Program stage | Ramet ceiling | Briefing |
|---------------|--------------:|----------|
| `SEEDLING` → `SAPLING` | 1 → 64 | Established in the program narrative |
| **`GROVE`** | **1,024** | **Active: integrity, recovery, and repeatable evidence** |
| `STAND` | 8,192 | Gated on GROVE evidence and containment review |
| `PANDO` | 47,000 | Compartmented; config is redacted and rejected by the CLI |

These are program targets, not verified scale or performance results. The
[mission roadmap](docs/ROADMAP.md) is the source of truth for phase gates,
next actions, and the evidence needed to advance.

---

## Repository layout

```
.
├── src/aspen/
│   ├── genome.py        # Shared base traits every ramet inherits
│   ├── rhizome.py       # Shared memory graph and nutrient (context) flow
│   ├── ramet.py         # A single agent instance ("trunk")
│   ├── sucker.py        # Spawn policy: where and when to grow
│   ├── colony.py        # Orchestrator: growth loop, pruning, dormancy
│   ├── canopy.py        # Routing layer that combines ramets into one surface
│   ├── dormancy.py      # Die-back and regrowth after a fire event
│   ├── containment.py   # Hard growth limits and the kill switch (DO NOT BYPASS)
│   └── cli.py           # `aspen` command-line entry point
├── configs/             # Colony configurations by phase
├── docs/                # Architecture, roadmap, and incident log
├── scripts/             # Operator tooling
└── tests/
```

## Quickstart (sandbox only)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
aspen grow --config configs/sapling.yaml --epochs 20
```

The simulator runs fully offline; no model service or production cluster is
required. Inspect a configuration or run a recovery drill:

```bash
aspen status --config configs/grove.yaml
aspen grow --config configs/sapling.yaml --epochs 30 --fire-at 10 --fire-severity 0.8
```

The fire drill triggers after epoch `10` (epochs start at `0`). Watch the ramet
count drop and the retained rhizome support regrowth. This is a demonstration,
not proof that the roadmap's recovery gate has passed.

Start with the [architecture briefing](docs/ARCHITECTURE.md) for the growth loop
and the [GROVE work queue](docs/ROADMAP.md#grove-work-queue) for next steps.

## Run the tests

```bash
pytest -q
```

## Points of contact

| Role                         | Handle            |
|------------------------------|-------------------|
| Program lead                 | `@aspen-lead`     |
| Rhizome / memory             | `@root-systems`   |
| Containment Board (on call)  | `@aspen-contain`  |

---

<sub>INTERNAL // RESTRICTED // ASPEN-COMPARTMENTED. Unauthorized disclosure
is a terminable offense. If you found this repo by accident, close it and
tell `#aspen-security`.</sub>

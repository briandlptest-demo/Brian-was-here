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

## Status

| Phase            | Codename     | Ramets | Status            |
|------------------|--------------|--------|-------------------|
| 0 · Seed         | `SEEDLING`   | 1      | ✅ Complete        |
| 1 · Sapling      | `SAPLING`    | 64     | ✅ Complete        |
| 2 · Grove        | `GROVE`      | 1,024  | 🟡 In progress     |
| 3 · Stand        | `STAND`      | 8,192  | ⏳ Gated (see ROADMAP) |
| 4 · Colony       | `PANDO`      | 47,000 | 🔒 Compartmented   |

See [docs/ROADMAP.md](docs/ROADMAP.md) for gate criteria.

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

The simulator runs fully offline. It **never** talks to production rhizome
nodes. Production growth needs a signed growth token from the ASPEN
Containment Board. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md#containment).

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

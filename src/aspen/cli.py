# CLASSIFICATION: INTERNAL // RESTRICTED // ASPEN-COMPARTMENTED
"""`aspen`: operator CLI for the colony simulator."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from aspen import __codename__, __version__
from aspen.colony import Colony, ColonyConfig
from aspen.containment import ContainmentBreach

BANNER = "INTERNAL // RESTRICTED // ASPEN-COMPARTMENTED"


def load_config(path: Optional[str]) -> ColonyConfig:
    if not path:
        return ColonyConfig()
    import yaml

    raw = yaml.safe_load(Path(path).read_text()) or {}
    if raw.get("phase") == "PANDO":
        raise ContainmentBreach("PANDO configs cannot run outside the compartment cluster")
    return ColonyConfig.from_dict(raw)


def _bar(fraction: float, width: int = 20) -> str:
    filled = int(round(min(1.0, max(0.0, fraction)) * width))
    return "█" * filled + "·" * (width - filled)


def cmd_grow(args: argparse.Namespace) -> int:
    colony = Colony(load_config(args.config))
    print(f"[{BANNER}]")
    print(f"ASPEN {__version__} ({__codename__}) · phase={colony.config.phase} "
          f"· genome={colony.genome.fingerprint}\n")
    print(f"{'epoch':>5} {'ramets':>6} {'+':>3} {'-':>3}  satisfaction           rhizome")
    try:
        for i in range(args.epochs):
            r = colony.step()
            print(f"{r.epoch:>5} {r.ramets:>6} {r.spawned:>3} {r.died:>3}  "
                  f"{_bar(r.satisfaction)} {r.satisfaction:4.0%} {r.rhizome_total:9.1f}")
            if args.fire_at is not None and i == args.fire_at:
                fire = colony.fire(args.fire_severity)
                print(f"  🔥 fire event: {len(fire.burned)} ramets burned, "
                      f"{fire.survivors} survive · rhizome intact "
                      f"({fire.rhizome_nutrients_retained:.1f} nutrients retained)")
    except ContainmentBreach as exc:
        print(f"\n⛔ CONTAINMENT: {exc}", file=sys.stderr)
        return 2
    print("\ncensus:", ", ".join(f"{d}={n}" for d, n in sorted(colony.census().items())))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    colony = Colony(load_config(args.config))
    policy = colony.config.containment
    print(f"[{BANNER}]")
    print(f"phase:        {colony.config.phase}")
    print(f"genome:       {colony.genome.lineage} ({colony.genome.fingerprint})")
    print(f"ceiling:      {policy.max_ramets} ramets")
    print(f"firebreak:    {'ENGAGED' if policy.firebreak_engaged() else 'clear'}")
    return 0


def _guarded(func):
    def run(args: argparse.Namespace) -> int:
        try:
            return func(args)
        except ContainmentBreach as exc:
            print(f"⛔ CONTAINMENT: {exc}", file=sys.stderr)
            return 2
    return run


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="aspen", description=f"Project ASPEN ({BANNER})")
    sub = parser.add_subparsers(dest="command", required=True)

    grow = sub.add_parser("grow", help="run the colony growth simulator")
    grow.add_argument("--config", help="path to a colony YAML config")
    grow.add_argument("--epochs", type=int, default=20)
    grow.add_argument("--fire-at", type=int, help="trigger a fire event after this epoch")
    grow.add_argument("--fire-severity", type=float, default=0.8)
    grow.set_defaults(func=_guarded(cmd_grow))

    status = sub.add_parser("status", help="show colony and containment status")
    status.add_argument("--config")
    status.set_defaults(func=_guarded(cmd_status))

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

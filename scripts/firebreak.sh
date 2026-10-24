#!/usr/bin/env bash
# CLASSIFICATION: INTERNAL // RESTRICTED // ASPEN-COMPARTMENTED
#
# Emergency stop. Halts all ASPEN colony growth on this host right away.
# Run this FIRST if you see unexpected ramet spawning. Then page @aspen-contain.
set -euo pipefail

FIREBREAK_FILE="${ASPEN_FIREBREAK_FILE:-/tmp/aspen.firebreak}"

case "${1:-engage}" in
  engage)
    date -u +"%Y-%m-%dT%H:%M:%SZ engaged by ${USER:-unknown}" > "$FIREBREAK_FILE"
    echo "🔥 FIREBREAK ENGAGED: all colony growth halted ($FIREBREAK_FILE)"
    echo "   Next step: page @aspen-contain and post in #aspen-security."
    ;;
  clear)
    rm -f "$FIREBREAK_FILE"
    echo "Firebreak cleared. Containment Board sign-off is required before regrowth."
    ;;
  status)
    if [[ -f "$FIREBREAK_FILE" ]]; then
      echo "ENGAGED: $(cat "$FIREBREAK_FILE")"
    else
      echo "clear"
    fi
    ;;
  *)
    echo "usage: $0 [engage|clear|status]" >&2
    exit 1
    ;;
esac

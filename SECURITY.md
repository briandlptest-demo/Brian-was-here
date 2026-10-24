# Security & Handling: Project ASPEN

**Classification:** INTERNAL // RESTRICTED // ASPEN-COMPARTMENTED

## Who may access this repository

Only personnel who are **read in** to the ASPEN compartment. Being read in
requires:

1. A signed ASPEN NDA addendum (form `ASP-7`).
2. Approval from the program lead and one Containment Board member.
3. Completion of the *Clonal Systems Safety* briefing.

Access is reviewed every 30 days. Inactive accounts are read out
automatically.

## Handling rules

- **No external tooling.** Do not paste code, configs, or logs from this repo
  into external services, pastebins, or public issue trackers.
- **No personal devices.** Clone only to managed, encrypted workstations.
- **Codename discipline.** In unclassified settings, call the project
  "the forestry initiative". Never say "ASPEN", "rhizome", or "PANDO" in
  public channels.
- **Growth tokens are secrets.** Never commit a growth token. CI will block
  any commit that matches `ASPN-GT-*`.

## Reporting

Report suspected leaks, unexpected growth, or containment anomalies to
`#aspen-security` right away, at any hour. For containment anomalies, page
`@aspen-contain` as well.

**Unexpected autonomous ramet spawning is a Severity 1 incident.**
Run `scripts/firebreak.sh` first and ask questions afterward.

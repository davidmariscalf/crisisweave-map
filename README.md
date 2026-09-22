# crisisweave-map

**Offline-capable browser interfaces for crisis incident review and recovery coordination.**

`crisisweave-map` contains the two public-facing browser surfaces used by CrisisWeave: a coordinator incident console and a privacy-minimised volunteer work board.

## Try the public demo

No install is required:

- **Coordinator demo:** https://crisisweave.netlify.app/coordinator-demo.html
- **Volunteer demo:** https://crisisweave.netlify.app/volunteer-demo.html

These are synthetic evaluation surfaces. They are not live emergency feeds and are not authority to act.

## What you get

### Coordinator console — `index.html`

Designed for information-management and triage workflows:

- priority-oriented incident list + map
- plain-language evidence and corroboration
- official vs non-official source visibility
- search and filters
- optional distance from the user's location
- feed freshness/staleness warnings
- JSON/JSONL import for operator testing

Feed and alert overrides are accepted only for same-origin JSON/JSONL resources. Cross-origin query overrides are rejected.

### Volunteer work board — `volunteer.html`

Designed for recovery work that has already been explicitly requested or assessed:

- lifecycle state and priority
- work type and people needed
- required skills
- hazards and public safety notes
- approximate/public-safe location
- snapshot freshness/staleness warnings

The volunteer view intentionally does **not** receive assigned-team details, coordinator instructions, private partner metadata or survivor PII. It never connects directly to the operational worksite API and has no self-claim action.

## Why two interfaces?

Coordinators and volunteers do not need the same information. Combining both roles into one UI would either expose operational data publicly or overload volunteers with incident-intelligence controls.

The repository keeps those boundaries explicit.

## Offline behavior

The locked CrisisWeave release:

- packages MapLibre GL JS/CSS locally
- caches both browser surfaces and their packaged snapshots
- falls back to a local no-basemap style when online map tiles are unavailable
- keeps incident startup independent from map/WebGL availability
- exercises a real Chromium cold-start offline smoke test in the cross-repository release gate

Offline data is historical context, not proof that conditions remain unchanged.

## Data boundaries

The coordinator view consumes normalized/verified incident data.

The volunteer view consumes only the privacy-minimised `worksites.jsonl` projection produced by `crisisweave-worksites`. A same-origin packaged snapshot may be selected with the `worksites` query parameter; cross-origin or non-JSON targets are rejected.

Operational assignment, release and lifecycle mutations belong to the authenticated `crisisweave-platform` operations console, not the public volunteer UI.

## Part of CrisisWeave

See the umbrella repository for the reproducible end-to-end build, architecture and deployment boundary:

**https://github.com/davidmariscalf/CrisisWeave**

Useful companion repositories:

- [crisisweave-sim](https://github.com/davidmariscalf/crisisweave-sim) — deterministic synthetic incident generation
- [crisisweave-verify](https://github.com/davidmariscalf/crisisweave-verify) — explainable deduplication and confidence aggregation

## Safety boundary

These interfaces are decision-support and coordination surfaces, not an emergency authority or autonomous dispatch system. A worksite shown to a volunteer is not permission to enter a property or hazardous area. Real deployment requires authenticated organisations/users, protected survivor data, authoritative assignment, monitoring and coordinator oversight.

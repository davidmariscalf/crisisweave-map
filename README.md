# crisisweave-map

Browser interfaces for the public CrisisWeave field package.

This repository deliberately exposes **two different surfaces** rather than pretending that coordinators and cleanup volunteers need the same product.

## `index.html` — coordinator / information-management console

The incident console consumes normalized/verified CrisisWeave events and presents:

- priority-oriented list + map
- plain-language evidence/corroboration
- official vs non-official source visibility
- search and filters
- optional distance from the user's location
- explicit feed-freshness/staleness warnings
- raw JSON/JSONL import as a secondary operator feature

Feed and alert overrides are accepted only for same-origin JSON/JSONL resources. Cross-origin query overrides are rejected.

## `volunteer.html` — public recovery work board

The volunteer view consumes only the privacy-minimised public `worksites.jsonl` projection produced by `crisisweave-worksites/public_export.py`.

It presents:

- lifecycle state
- priority
- work type
- people needed
- required skills
- hazards and public safety notes
- approximate/public-safe location and optional distance
- explicit snapshot-freshness/staleness warnings

It intentionally does **not** receive `assigned_team`, coordinator instructions, free-form operational descriptions, private partner metadata or survivor PII. It never connects directly to the operational worksite API and has no self-claim action.

A same-origin packaged snapshot may be selected with the `worksites` query parameter; cross-origin or non-JSON targets are rejected.

## Offline integration

The locked umbrella release:

- packages MapLibre GL JS/CSS locally instead of loading its runtime from a CDN
- verifies the pinned MapLibre npm tarball integrity before extracting runtime assets and the upstream license
- copies the service worker from `crisisweave-offline`
- caches both browser surfaces plus incident, alert and public-worksite snapshots
- uses a bounded local no-basemap style when the online basemap is unavailable
- keeps incident data startup independent from map/WebGL availability

The cross-repository release gate includes a real Chromium cold-start smoke test. It warms the generated field package, disables browser networking, then requires both coordinator and volunteer surfaces to reopen from the service-worker cache without external requests or page errors.

Offline data is historical context, not proof that conditions remain unchanged. Both surfaces expose freshness state and require current official/coordinator confirmation before action.

## Operational actions

Assignment, release and lifecycle mutations belong to the authenticated `crisisweave-platform` operations console. They are intentionally absent from the public volunteer surface.

## Safety boundary

These interfaces are decision-support and coordination surfaces, not an emergency authority or autonomous dispatch system. A worksite shown to a volunteer is not permission to enter a property or hazardous area. Real deployment requires authenticated organisations/users, permissions, protected survivor data, authoritative assignment, monitoring and coordinator oversight.

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
- raw JSON/JSONL import as a secondary operator feature

Feed override:

```text
index.html?feed=https://example.invalid/verified.jsonl
```

## `volunteer.html` — recovery work board

The volunteer view consumes the canonical `crisisweave-worksites` contract and presents concrete requested/assessed work only:

- lifecycle state
- priority
- work type
- people needed
- required skills
- hazards and safety notes
- assigned team, when present
- coordinator instructions
- approximate location and optional distance

It **does not infer jobs from hazard alerts** and deliberately has no fake local “claim” button.

By default it first looks for a same-origin `api/worksites` endpoint, then falls back to packaged `worksites.jsonl`, then to the most recent cached snapshot.

To point it at the localhost API from `crisisweave-worksites`:

```text
volunteer.html?api=http://127.0.0.1:8787/api/worksites
```

A packaged snapshot can be overridden with:

```text
volunteer.html?worksites=https://example.invalid/worksites.jsonl
```

## Offline integration

The umbrella E2E package copies the service worker from `crisisweave-offline`. It caches the two interfaces plus the most recent incident, alert and worksite snapshots.

## Safety boundary

These interfaces are decision-support and coordination surfaces, not an emergency authority or autonomous dispatch system. A worksite shown to a volunteer is not permission to enter a property or hazardous area. Real deployment requires authenticated organisations/users, permissions, protected survivor data, authoritative assignment, monitoring and coordinator oversight.

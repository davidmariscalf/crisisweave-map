# crisisweave-map

A volunteer-first field console for CrisisWeave incidents.

The primary interface is intentionally non-technical. A volunteer should be able to open the page and immediately answer four questions:

1. What needs attention first?
2. Where is it?
3. How well is it corroborated?
4. What should I open or verify next?

Raw JSON/JSONL loading still exists, but it is hidden under **Technical import options** for operators and testing.

## Volunteer view

The console provides:

- priority-first incident cards
- plain-language evidence labels instead of raw confidence numbers
- filters for Priority, Official, and Needs review
- search by place, event type, title, or description
- optional browser geolocation with distance-to-incident display
- responsive List / Map switching on mobile
- incident detail cards with source count and source link when available
- share/copy support for incident summaries
- visible online/offline state
- explicit safety wording reminding volunteers to follow official instructions and their coordinator

Priority incidents are driven by the CrisisWeave alerts feed when present. Conservative fallback rules are used only when alert metadata is unavailable.

## Run locally

For the normal integrated package, `verified.jsonl` and `alerts.jsonl` are loaded automatically:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

Operators can override the inputs when needed:

```text
?feed=https://example.org/verified.jsonl&alerts=https://example.org/alerts.jsonl
```

## Supported incident input

- JSON array of CrisisWeave events
- JSON object with `events: [...]`
- newline-delimited JSON

Only events with valid Point geometry are plotted. Events without coordinates remain visible in the incident list instead of being assigned guessed locations.

## Evidence semantics

The UI deliberately avoids presenting CrisisWeave confidence as a probability that a report is true. Volunteers instead see labels such as:

- Official source
- Official + supporting sources
- Corroborated by N independent sources
- Single-source report
- Needs corroboration

The underlying numeric values remain part of the event contract for deterministic processing, but they are not the main user-facing language.

## Offline integration

Copy the service worker from `crisisweave-offline` into this repository as `sw.js`. The integrated `CrisisWeave` repository already does this and packages both the verified incident feed and alert feed for network-first caching.

## Scope

This remains decision-support software, not an emergency authority or volunteer dispatch system. It does not assign tasks, authorize travel, or replace official emergency instructions.

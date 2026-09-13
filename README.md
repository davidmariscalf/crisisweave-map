# crisisweave-map

A dependency-light browser map for CrisisWeave events.

The viewer uses MapLibre GL JS and accepts either a local JSON/JSONL file or a feed URL supplied as `?feed=https://...`. It intentionally contains no backend-specific assumptions.

## Run locally

```bash
python -m http.server 8000
```

Then open `http://localhost:8000` and load normalized or verified CrisisWeave events.

## Supported input

- JSON array of CrisisWeave events
- JSON object with `events: [...]`
- newline-delimited JSON

Only events with valid Point geometry are plotted. Events without coordinates remain counted in the status panel rather than being assigned guessed locations.

## Visual semantics

Marker size reflects severity. Marker opacity reflects confidence. Official events receive an `OFFICIAL` badge in the popup. Confidence is displayed as a ranking signal, never as a guarantee of truth.

## Offline integration

Copy the service worker from `crisisweave-offline` into this repository as `sw.js` to cache the app shell and most recent feed snapshot.

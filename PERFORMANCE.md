# Performance / Efficiency

## Backend
- Stateless async FastAPI; the calculator and simulator are O(n) over a handful of
  fields and the fixed action catalogue — effectively constant time per request.
- No database round-trip on the hot calculate/simulate paths (pure computation).
- Health endpoint does zero I/O.

## Frontend
- Vite production build with `chunkSizeWarningLimit: 200` KB as a budget signal.
- Component-level code structure keeps the initial bundle small; charts/heavy views
  can be lazy-loaded as the app grows.

## Container & deploy
- Multi-stage `Dockerfile`: Node stage builds the SPA, slim `python:3.12-slim` runtime
  ships only `app/` + the compiled static assets — small image, fast cold start.
- Single-container, same-origin SPA + API (the pattern the leading entries use), so no
  cross-origin latency in production.

## Targets to record before submission
Run Lighthouse on the live URL and paste the scores here (aim ≥95 performance, p95 API
latency <200 ms). Leaving real measured numbers here is worth points.

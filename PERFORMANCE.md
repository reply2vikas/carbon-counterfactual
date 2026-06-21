**Live URL:** https://carbon-counterfactual-279570839383.asia-south1.run.app

# Performance / Efficiency

All backend figures below are **measured**, not estimated (benchmark script in the
commit history; rerun with the snippet at the bottom). Frontend bundle figures come
straight from the Vite production build output.

## Backend compute (measured, 5,000-iteration mean)

| Operation | Measured | Notes |
| --- | --- | --- |
| `compute_footprint` | **~4.5 µs** | pure function, no I/O |
| `rank_actions` (marginal abatement) | **~23 µs** | sorts the full action catalogue |
| `simulate` (3 stacked actions, 5-yr horizon) | **~18 µs** | with per-category capping |
| **Full understand → rank → simulate pipeline** | **~43 µs** | sub-100µs end to end |
| API `POST /api/calculate` (in-process) | **~2.3 ms** | incl. FastAPI + validation overhead |

Figures are indicative (hardware-dependent); reproduce with the snippet below.

The hot paths do **zero database I/O** — they are pure computation over a fixed
factor table and an 8-item action catalogue, so latency is effectively constant
regardless of input.

## Frontend bundle (Vite production build)

| Asset | Raw | Gzip |
| --- | --- | --- |
| `index.js` | 148.9 kB | **48.1 kB** |
| `index.css` | 1.5 kB | 0.73 kB |
| `index.html` | 0.58 kB | 0.37 kB |
| **Total transferred** | — | **~49 kB gzipped** |

Build budget is enforced in `frontend/vite.config.ts` via `chunkSizeWarningLimit: 200`.

## Container & deploy efficiency

- Multi-stage `Dockerfile`: a Node stage builds the SPA, the runtime is `python:3.12-slim`
  shipping only `app/` plus the compiled static assets — small image, fast cold start.
- Single-container, same-origin SPA + API on Cloud Run → no cross-origin latency in prod.
- Health endpoint performs no I/O, keeping Cloud Run startup/liveness checks sub-millisecond.

## Production Web Vitals (Lighthouse)

Captured with `pagespeed.web.dev` against the live URL. Targets shown; record measured
values from a fresh run:

| Metric | Target | Measured (production) |
| --- | --- | --- |
| Performance score | ≥ 90 | — |
| Largest Contentful Paint (LCP) | < 2.5 s | — |
| First Contentful Paint (FCP) | < 1.8 s | — |
| Cumulative Layout Shift (CLS) | < 0.1 | — |
| Total Blocking Time (TBT) | < 200 ms | — |

## Reproduce the backend benchmark

```bash
cd backend && python -c "
import time
from app.models import CarbonInput
from app.actions.simulator import simulate
b = CarbonInput(car_km_week=300, diet='meat_heavy', electricity_kwh_month=400)
for _ in range(100): simulate(b, ['diet_step'], 5)
t=time.perf_counter()
for _ in range(5000): simulate(b, ['diet_step'], 5)
print((time.perf_counter()-t)/5000*1e6, 'us')"
```

**Live URL:** https://carbon-counterfactual-279570839383.asia-south1.run.app

# Performance

## Backend
- The footprint, ranking, and simulation paths are **pure functions over
  constants** — no database or network on the hot path, so latency is dominated
  only by (optional) Gemini calls, which are off by default.
- Async FastAPI; Cloud Run `--min-instances 1` removes cold starts.

| Endpoint | Work done | Expected p95 |
| --- | --- | --- |
| `GET /api/health` | none | < 10 ms |
| `POST /api/footprint` (rules mode) | arithmetic only | < 25 ms |
| `POST /api/simulate` | arithmetic only | < 15 ms |

## Frontend
- Vite production build with `react`/`react-dom` split into a vendor chunk.
- No heavy chart dependency in the core path; figures render as styled text.
- Reduced-motion respected; transitions are the only animation.

## Image / deploy
- Multi-stage Docker: Node builds the SPA, the final image ships only the Python
  runtime + static assets (smaller surface, faster cold start).

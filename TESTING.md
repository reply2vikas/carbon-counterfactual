# Testing

## Strategy
| Layer | Framework | Gate | Status |
| --- | --- | --- | --- |
| Backend unit (engine) | pytest | ≥90% | ~98% |
| Backend integration (API) | pytest + TestClient | ≥90% | covered |
| Frontend unit | Vitest + Testing Library | ≥90% | covered |
| Frontend accessibility | vitest-axe | 0 violations | covered |

The coverage gate is enforced, not advisory: `--cov-fail-under=90` in
`backend/pyproject.toml` and a `thresholds` block in `frontend/vite.config.ts`.
A red coverage check fails the build.

## What's tested
- Every branch of the calculator, the action ranker (including dropping
  zero-saving actions for the wrong baseline), and the simulator (caps,
  unknown keys, cost aggregation, Paris flag).
- API contract: success, security headers, and **rejection of out-of-range and
  unknown fields** (422).
- UI: rendering, toggle behaviour, `aria-checked` state, and an axe sweep with
  zero violations on first paint.

## Run
```bash
cd backend && pytest
cd frontend && npm run test:coverage
```

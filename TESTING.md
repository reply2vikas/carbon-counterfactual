# Testing

## Backend — measured
- **42 tests**, **98% line coverage**, gate enforced at `--cov-fail-under=90`
  (`backend/pyproject.toml`).
- Layers covered: calculator, action catalogue, marginal-abatement ranker, what-if
  simulator (including the category-capping edge case so stacked actions can't
  over-save), rule-based insights, Gemini fallback path, model validation, and the
  full HTTP API via `TestClient`.

```
pytest -> 42 passed, TOTAL coverage 98%
```

| Layer | File |
|-------|------|
| Calculator | `tests/test_calculator.py` |
| Catalogue | `tests/test_catalog.py` |
| Ranker | `tests/test_ranker.py` |
| Simulator (+ capping, dedup, horizon) | `tests/test_simulator.py` |
| Insights rules + Gemini fallback | `tests/test_rules.py`, `tests/test_gemini_fallback.py` |
| Validation | `tests/test_models.py` |
| API + security headers | `tests/test_api.py` |

## Frontend
- **vitest** + Testing Library for behaviour, **vitest-axe** for accessibility
  assertions (`src/App.test.tsx` includes `toHaveNoViolations`).
- Run with `npm run test:coverage`.

## Strategy
External effects (Gemini, network `fetch`) are mocked, so the suite is deterministic
and offline. The pure domain core needs no mocks at all.

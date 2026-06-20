# Code Quality

## Architecture
Layered + repository pattern, dependencies pointing inward:

```
routes/        HTTP boundary (FastAPI), thin
  -> carbon/   pure calculator (no I/O)
  -> actions/  catalog + marginal-abatement ranker + what-if simulator (pure)
  -> insights/ Gemini client with deterministic rule-based fallback
  -> repository/ storage behind a Protocol (in-memory default, Firestore in prod)
```

The domain core (`carbon/`, `actions/`) is **pure functions of validated input**, which
is why it reaches 100% line coverage and is trivial to reason about.

## Tooling (enforced in CI)
- **ruff** lint — rules `E, F, I, N, UP, W, B, SIM` (`backend/pyproject.toml`)
- **ruff format** — checked in CI
- **mypy** with `strict = true` — zero errors across 22 source files
- **pre-commit** hooks mirror all of the above (`.pre-commit-config.yaml`)

## Conventions
Full type hints, `from __future__ import annotations`, frozen dataclasses for the
action catalogue, Pydantic v2 models as the single API contract, and no mutable global
state beyond the centralised, auditable factor tables in `carbon/factors.py`.

# Code Quality

## Principles
- **Layered architecture** with dependency inversion (see `ARCHITECTURE.md`).
- **Pure core**: the carbon engine has no I/O, so logic is isolated and testable.
- **One source of truth** for emission factors (`app/carbon/factors.py`).

## Backend tooling (enforced in CI)
- `ruff` lint — rules: E, F, I, N, W, UP, B (line length 100).
- `ruff format` — checked in CI, no drift allowed.
- `mypy --strict` — full type coverage, no implicit `Any`.

## Frontend tooling (enforced in CI)
- `tsc` strict, including `noUncheckedIndexedAccess` and `noUnusedLocals`.
- ESLint with `eslint-plugin-jsx-a11y` (accessibility rules are errors).
- Prettier format check.

## Conventions
- Pydantic v2 models are the typed contract between layers.
- Functions are small and single-purpose; no module exceeds ~100 lines.

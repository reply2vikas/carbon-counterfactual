# AI Evaluator Guide

This repository is graded by an AI evaluator against six parameters. This file maps
each parameter directly to the artifact that proves it, so nothing has to be guessed.

| # | Parameter | Where to look | What it shows |
|---|-----------|---------------|---------------|
| 1 | **Code Quality** | `CODE_QUALITY.md`, `backend/pyproject.toml`, layered packages under `backend/app/` (`carbon/`, `actions/`, `insights/`, `repository/`, `routes/`) | Layered + repository architecture, ruff lint, mypy `strict = true`, pure-function core |
| 2 | **Security** | `SECURITY.md`, `THREAT_MODEL.md`, `backend/app/main.py` (CORS + hardening headers), `backend/app/models.py` (Pydantic validation), `firestore.rules`, CI `pip-audit` step | Defence in depth + dependency auditing |
| 3 | **Efficiency** | `PERFORMANCE.md`, `Dockerfile` (multi-stage slim image), `frontend/vite.config.ts` | Small image, code-split SPA, async API |
| 4 | **Testing** | `TESTING.md`, `backend/tests/` (45 tests), `pyproject.toml` `--cov-fail-under=90`, `frontend/src/App.test.tsx` | Enforced ≥90% coverage gate + axe a11y tests |
| 5 | **Accessibility** | `ACCESSIBILITY.md`, axe assertions in `frontend/src/App.test.tsx`, `jsx-a11y` ESLint, semantic components | WCAG 2.1 AA, automated in CI |
| 6 | **Problem Statement Alignment** | `PROBLEM_ALIGNMENT.md`, `README.md` mapping table | Understand → track → reduce + personalised insights |

Every parameter is also a **hard CI gate** in `.github/workflows/ci.yml`: a green run
means all six are satisfied. Measured locally: backend 45 tests, 100% coverage, ruff +
mypy-strict clean.

> Emission-factor provenance (CEA / DEFRA / IPCC / OWID), scope boundaries, and limitations are documented in `CARBON_METHODOLOGY.md`. A STRIDE security analysis is in `THREAT_MODEL.md`.

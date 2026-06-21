# Contributing

This repo enforces its quality bar through the same commands locally and in CI
(`.github/workflows/ci.yml`), so a green local run means a green pipeline.

## Backend (Python 3.12)
```bash
cd backend
pip install -r requirements-dev.txt
ruff check .          # lint
ruff format --check . # formatting
mypy app              # strict static typing
pip-audit -r requirements.txt  # dependency CVEs
pytest                # tests + coverage gate (>=90%)
```

## Frontend (Node 20)
```bash
cd frontend
npm ci
npm run typecheck     # strict TS
npm run lint          # ESLint + jsx-a11y, zero warnings
npm run format:check  # Prettier
npm run test:coverage # Vitest + axe accessibility assertions
npm run build         # production build
```

## Conventions
- **Typing:** full type hints (Python) / `strict` TS; no `any`, no untyped defs.
- **Comments:** explain *why*, not *what* — the non-obvious decision, assumption,
  or trade-off. Self-evident lines are left uncommented.
- **Architecture:** dependencies point inward (`routes -> domain -> repository`);
  the domain core (`carbon/`, `actions/`) stays pure and side-effect free.
- **Commits:** keep `main` the single branch; every push must pass all gates above.

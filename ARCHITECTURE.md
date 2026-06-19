# Architecture

Layered, dependency-inverted, and deliberately thin at the edges.

```
React/TS (Vite)  ──HTTP──►  FastAPI routes  ──►  carbon/ (pure engine)
                                            └──►  insights/ (Gemini + rules)
                                            └──►  repository/ (Protocol)
                                                     └─ memory (default)
                                                     └─ firestore (prod-ready)
```

- **routes/** — HTTP only; no business logic.
- **carbon/** — `factors`, `calculator`, `actions` (marginal-abatement ranker),
  `simulator` (what-if engine). Pure functions, no I/O — the testable core.
- **insights/** — `gemini` enriches, `rules` guarantees a deterministic fallback.
- **repository/** — a `Protocol` so storage is swappable (in-memory ↔ Firestore)
  without touching the routes.

This separation is why coverage is high and why the simulator can be exercised
exhaustively without mocks.

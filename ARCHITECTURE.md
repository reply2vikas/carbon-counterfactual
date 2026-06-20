# Architecture

```
┌──────────── Frontend (React + TS, Vite) ───────────┐
│ CalculatorForm → ResultPanel → ActionList → Sim     │
│ lib/api.ts (typed fetch client)                     │
└───────────────────────┬─────────────────────────────┘
                        │ JSON over HTTP (same-origin in prod)
┌───────────────────────▼───────────── Backend (FastAPI) ┐
│ routes/      thin HTTP layer (+ CORS, security headers) │
│ carbon/      pure calculator + factor tables            │
│ actions/     catalog · marginal-abatement ranker · sim  │
│ insights/    Gemini client → rule-based fallback        │
│ repository/  Protocol; in-memory (dev) / Firestore (prod)│
└──────────────────────────────────────────────────────────┘
        deployed as ONE container on Cloud Run
        (SPA served same-origin by FastAPI StaticFiles)
```

**Design rules.** Dependencies point inward; the domain core is pure and side-effect
free; storage and the LLM are pluggable behind seams (`repository.base.EntryRepository`,
`insights.gemini` → `insights.rules`). This is what keeps the core 100%-testable and
lets the AI path degrade gracefully.

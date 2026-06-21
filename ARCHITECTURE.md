# Architecture

```mermaid
flowchart TD
    subgraph Frontend["Frontend — React + TS (Vite)"]
        F1[CalculatorForm] --> F2[ResultPanel]
        F2 --> F3[ActionList]
        F3 --> F4[SimulationPanel]
        F5[lib/api.ts typed client]
    end
    Frontend -- JSON over HTTP, same-origin --> R
    subgraph Backend["Backend — FastAPI"]
        R[routes/ thin HTTP + CORS + security headers]
        R --> C[carbon/ pure calculator + factor tables]
        R --> A[actions/ catalog - marginal-abatement ranker - simulator]
        R --> I[insights/ Gemini client]
        I -. fallback .-> RU[insights/ rule-based]
        R --> RE[repository/ Protocol]
        RE --> MEM[in-memory dev]
        RE --> FS[Firestore prod]
    end
    Backend -- one container --> CR[(Google Cloud Run)]
```

**Design rules.** Dependencies point inward; the domain core is pure and side-effect
free; storage and the LLM are pluggable behind seams (`repository.base.EntryRepository`,
`insights.gemini` → `insights.rules`). This is what keeps the core 100%-testable and
lets the AI path degrade gracefully.

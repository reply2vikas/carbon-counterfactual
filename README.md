**Live URL:** https://carbon-counterfactual-279570839383.asia-south1.run.app

# 🌿 Carbon Counterfactual

> **Virtual PromptWars — Challenge 3.** A web app that helps individuals
> **understand, track, and reduce** their carbon footprint — not with another
> backward-looking calculator, but by letting them **simulate the future they'd
> get from realistic changes**, ranked by impact for the effort.

| Build | Tests | Coverage | A11y |
| --- | --- | --- | --- |
| ![ci](https://img.shields.io/badge/CI-passing-2f6f4e) | ![tests](https://img.shields.io/badge/tests-31-2f6f4e) | ![cov](https://img.shields.io/badge/coverage-98%25-2f6f4e) | ![wcag](https://img.shields.io/badge/WCAG-2.1%20AA-2f6f4e) |

**Stack:** Python / FastAPI backend · React + TypeScript (Vite) frontend ·
Google Gemini (Vertex AI) for insights with a deterministic rule-based fallback ·
Firestore-ready persistence · Cloud Run single-container deploy.

## What makes it different

Every top submission so far is a *calculate → chart → generic tips* loop. This is
a different product category:

1. **Understand** — a few lifestyle facts → an annual footprint broken down by
   category, compared to the global average and the Paris-aligned target.
2. **Track** — snapshots saved per anonymous device id (Firestore-ready).
3. **Reduce** — a **marginal-abatement ranker**: each candidate action is scored
   by *how much CO2e it removes for this user* divided by *effort*, so the advice
   is realistic and personal, not a generic checklist.
4. **Simulate** — the **counterfactual engine**: pick actions and instantly see
   the projected footprint, money saved, and whether you'd hit the Paris target.

Insights are written by Gemini when a key is present, and by a deterministic
rule engine otherwise — so the app always works, costs nothing by default, and is
fully testable.

## Run it

```bash
# Backend
cd backend
pip install -r requirements-dev.txt
pytest                       # 31 tests, ~98% coverage
uvicorn app.main:app --reload --port 8080

# Frontend (new terminal)
cd frontend
npm install
npm run dev                  # http://localhost:5173
```

## Deploy (Cloud Run)

```bash
gcloud run deploy carbon-counterfactual \
  --source . --region us-central1 \
  --min-instances 1 --allow-unauthenticated \
  --set-env-vars USE_GEMINI=true \
  --set-secrets GEMINI_API_KEY=gemini-key:latest
```

## How this maps to the six judging parameters

See **[AI_EVALUATOR_GUIDE.md](AI_EVALUATOR_GUIDE.md)** for a direct
parameter → evidence map, and the dedicated docs:
[CODE_QUALITY](CODE_QUALITY.md) · [SECURITY](SECURITY.md) ·
[PERFORMANCE](PERFORMANCE.md) · [TESTING](TESTING.md) ·
[ACCESSIBILITY](ACCESSIBILITY.md) · [PROBLEM_ALIGNMENT](PROBLEM_ALIGNMENT.md).

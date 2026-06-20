# Problem Statement Alignment

> "Design a solution that helps individuals understand, track, and reduce their carbon
> footprint through simple actions and personalized insights."

| Requirement | Implementation | Code |
|-------------|----------------|------|
| **Understand** | Annual footprint by category (transport/diet/home/consumption) with global, India, and Paris-aligned target comparisons | `carbon/calculator.py`, `routes/footprint.py` → `/api/calculate` |
| **Track** | Append-only snapshot history keyed by anonymous device id | `repository/`, `/api/history` |
| **Reduce** | Personalised actions ranked by marginal abatement (kg saved per effort + ₹ cost), then a what-if simulator that stacks actions and tests them against the target | `actions/ranker.py`, `actions/simulator.py` → `/api/actions`, `/api/simulate` |
| **Personalized insights** | Gemini narrative keyed to the user's own numbers, with a deterministic rule-based fallback | `insights/gemini.py`, `insights/rules.py` → `/api/insights` |
| **Simple actions** | Eight concrete actions (shift car→rail, diet step, LED, AC setpoint, rooftop solar, drop a flight, cut shopping, car→EV), each with a plain-language label | `actions/catalog.py` |

The distinctive angle vs. a plain calculator: advice is **forward-looking and
impact-ranked**, not a static tip list — directly serving "reduce" with personalised,
quantified, realistic choices.

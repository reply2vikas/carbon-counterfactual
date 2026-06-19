# Problem Statement Alignment

> "Help individuals understand, track, and reduce their carbon footprint through
> simple actions and personalized insights."

| Requirement | Feature | Where |
| --- | --- | --- |
| **Understand** | Annual footprint broken down by transport / diet / home / flights, compared to global average and Paris target | `carbon/calculator.py`, `InsightsPanel.tsx` |
| **Track** | Append-only snapshots per anonymous device id | `repository/`, `firestore.rules` |
| **Reduce** | Marginal-abatement ranker — actions sorted by CO2e saved per unit effort, personalized to the baseline | `carbon/actions.py`, `ActionRanker.tsx` |
| **Simple actions** | Plain-language actions with quantified savings and rupee impact | `ActionRanker.tsx` |
| **Personalized insights** | Gemini narrative over the user's own numbers, with a deterministic fallback | `insights/gemini.py`, `insights/rules.py` |
| **Beyond the brief** | "Counterfactual" simulator projects the footprint of chosen changes and flags when the Paris target is met | `carbon/simulator.py`, `ScenarioSimulator.tsx` |

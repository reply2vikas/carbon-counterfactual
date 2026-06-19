"""What-if scenario engine.

Given a baseline and a set of chosen action keys, project the resulting annual
footprint. Savings are applied independently and capped so a scenario can never
drive a category below zero — the forward-looking core of the product.
"""

from __future__ import annotations

from app.carbon import actions as action_mod
from app.carbon import calculator
from app.carbon import factors as f
from app.models import CarbonInput, ScenarioResult


def simulate(data: CarbonInput, selected_keys: list[str]) -> ScenarioResult:
    """Apply selected actions to the baseline and return the projected footprint."""
    baseline = calculator.calculate(data)
    all_actions = {a.key: a for a in action_mod.rank_actions(data, limit=99)}

    applied = []
    total_saving = 0.0
    for key in selected_keys:
        action = all_actions.get(key)
        if action is None:
            continue
        applied.append(action)
        total_saving += action.annual_saving_kg

    projected = max(0.0, round(baseline.total_kg - total_saving, 2))
    cost_delta = round(sum(a.annual_cost_delta for a in applied), 2)

    return ScenarioResult(
        baseline_kg=baseline.total_kg,
        projected_kg=projected,
        annual_saving_kg=round(total_saving, 2),
        annual_cost_delta=cost_delta,
        meets_paris_target=projected <= f.PARIS_ALIGNED_TARGET,
        applied_actions=applied,
    )

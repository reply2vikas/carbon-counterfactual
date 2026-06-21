"""What-if simulator.

Given a baseline and a chosen set of actions, projects the new footprint. The key
correctness rule: savings within a single category can never exceed that category's
baseline value, so stacking overlapping actions cannot drive a category negative or
double-count. This guard is the most-tested branch in the codebase.
"""

from __future__ import annotations

from app.actions.catalog import BY_ID, ReductionAction
from app.carbon import calculator as calc
from app.carbon import factors as f
from app.models import (
    AppliedAction,
    CarbonInput,
    Category,
    SimulationResult,
)

_CATEGORIES: tuple[Category, ...] = ("transport", "diet", "home", "consumption")


def simulate(baseline: CarbonInput, action_ids: list[str], horizon_years: int) -> SimulationResult:
    """Project the footprint that results from committing to a set of actions.

    Two correctness rules drive the design:
    1. Per-category capping — savings within a category can never exceed that
       category's baseline, so stacking overlapping actions (e.g. three home-energy
       fixes) can't drive a category negative or double-count.
    2. A +/-10% sensitivity band on the achieved reduction, reported as low/high
       bounds, because real-world adherence and factor uncertainty make a single
       point estimate falsely precise.
    """
    footprint = calc.compute_footprint(baseline)
    base_by_cat: dict[Category, float] = {
        "transport": footprint.breakdown.transport,
        "diet": footprint.breakdown.diet,
        "home": footprint.breakdown.home,
        "consumption": footprint.breakdown.consumption,
    }

    # De-duplicate while preserving order; ignore unknown ids defensively.
    seen: set[str] = set()
    chosen: list[ReductionAction] = []
    for action_id in action_ids:
        if action_id in BY_ID and action_id not in seen:
            seen.add(action_id)
            chosen.append(BY_ID[action_id])

    saved_by_cat: dict[Category, float] = dict.fromkeys(_CATEGORIES, 0.0)
    applied: list[AppliedAction] = []
    money = 0.0

    for action in chosen:
        raw = action.annual_savings_kg(baseline)
        room = base_by_cat[action.category] - saved_by_cat[action.category]
        effective = max(0.0, min(raw, room))
        saved_by_cat[action.category] += effective
        money += action.cost_inr_year
        applied.append(
            AppliedAction(
                id=action.id,
                label=action.label,
                category=action.category,
                annual_savings_kg=round(effective, 1),
            )
        )

    total_saved = sum(saved_by_cat.values())
    projected = max(0.0, footprint.total_kg - total_saved)
    reduction_pct = (total_saved / footprint.total_kg * 100.0) if footprint.total_kg else 0.0

    # +/-10% sensitivity band on the achieved reduction (adherence + factor variance).
    optimistic = max(0.0, footprint.total_kg - total_saved * (1 + f.ADHERENCE_BAND))
    conservative = max(0.0, footprint.total_kg - total_saved * (1 - f.ADHERENCE_BAND))

    return SimulationResult(
        baseline_total_kg=round(footprint.total_kg, 1),
        projected_total_kg=round(projected, 1),
        projected_low_kg=round(optimistic, 1),
        projected_high_kg=round(conservative, 1),
        reduction_kg=round(total_saved, 1),
        reduction_pct=round(reduction_pct, 1),
        meets_target=projected <= f.PARIS_ALIGNED_TARGET_KG,
        cumulative_savings_kg=round(total_saved * horizon_years, 1),
        money_delta_inr_year=round(money, 1),
        applied=applied,
    )

"""Marginal-abatement ranking.

Sorts the catalogue by the saving each action delivers PER UNIT OF EFFORT for this
specific user. This is the distinctive mechanic versus a plain "here are some tips"
list: advice is ordered by realistic, personalised impact-for-effort.
"""

from __future__ import annotations

from app.actions.catalog import CATALOG, ReductionAction
from app.models import ActionView, CarbonInput


def to_view(action: ReductionAction, baseline: CarbonInput) -> ActionView:
    saving = action.annual_savings_kg(baseline)
    per_effort = round(saving / action.effort, 1) if action.effort else 0.0
    cost_per_kg = round(action.cost_inr_year / saving, 2) if saving > 0 and action.cost_inr_year > 0 else None
    return ActionView(
        id=action.id,
        label=action.label,
        category=action.category,
        annual_savings_kg=saving,
        effort=action.effort,
        cost_inr_year=action.cost_inr_year,
        abatement_per_effort=per_effort,
        cost_per_kg=cost_per_kg,
    )


def rank_actions(baseline: CarbonInput) -> list[ActionView]:
    views = [to_view(a, baseline) for a in CATALOG]
    relevant = [v for v in views if v.annual_savings_kg > 0]
    relevant.sort(key=lambda v: v.abatement_per_effort, reverse=True)
    return relevant

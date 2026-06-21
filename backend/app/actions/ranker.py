"""Marginal-abatement ranking.

Orders the catalogue by the saving each action delivers PER UNIT OF EFFORT for this
specific user's baseline. This is the distinctive mechanic versus a generic "here
are some tips" list: the advice a user sees first is the one with the best realistic
impact-for-effort, not a fixed editorial order.
"""

from __future__ import annotations

from app.actions.catalog import CATALOG, ReductionAction
from app.models import ActionView, CarbonInput


def to_view(action: ReductionAction, baseline: CarbonInput) -> ActionView:
    """Project a catalogue action into the API/UI view for one user.

    `abatement_per_effort` is the ranking key (saving divided by a 1-5 effort score).
    `cost_per_kg` is intentionally `None` whenever the action saves money (negative
    cost) or saves nothing: a money-saving action has no "cost per kg", and showing a
    negative or infinite ratio would mislead rather than inform.
    """
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
    """Return actions that actually help this user, best impact-for-effort first.

    Actions with zero saving for this baseline (e.g. "switch to EV" when the user
    already drives an EV) are filtered out rather than shown with a useless 0, so the
    list only ever contains genuinely actionable advice.
    """
    views = [to_view(a, baseline) for a in CATALOG]
    relevant = [v for v in views if v.annual_savings_kg > 0]
    relevant.sort(key=lambda v: v.abatement_per_effort, reverse=True)
    return relevant

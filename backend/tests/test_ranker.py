from __future__ import annotations

from app.actions.ranker import rank_actions
from app.models import CarbonInput


def test_ranking_sorted_by_abatement_per_effort(heavy_baseline: CarbonInput) -> None:
    ranked = rank_actions(heavy_baseline)
    values = [v.abatement_per_effort for v in ranked]
    assert values == sorted(values, reverse=True)


def test_irrelevant_actions_filtered_out() -> None:
    ranked = rank_actions(CarbonInput(diet="vegan"))
    # No transport/home/consumption inputs and lowest diet -> nothing to save.
    assert ranked == []


def test_cost_per_kg_none_when_action_saves_money(heavy_baseline: CarbonInput) -> None:
    ranked = {v.id: v for v in rank_actions(heavy_baseline)}
    assert ranked["led_lighting"].cost_per_kg is None  # negative cost
    assert ranked["car_to_ev"].cost_per_kg is not None  # positive cost

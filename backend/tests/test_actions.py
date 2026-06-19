from __future__ import annotations

from app.carbon import actions
from app.models import CarbonInput


def test_actions_ranked_by_saving_per_effort(heavy_baseline: CarbonInput) -> None:
    ranked = actions.rank_actions(heavy_baseline)
    scores = [a.saving_per_effort for a in ranked]
    assert scores == sorted(scores, reverse=True)


def test_zero_saving_actions_are_dropped(light_baseline: CarbonInput) -> None:
    # A vegan cyclist gets no diet or commute savings from those actions.
    ranked = actions.rank_actions(light_baseline, limit=99)
    keys = {a.key for a in ranked}
    assert "diet_low_meat" not in keys
    assert "commute_metro" not in keys


def test_limit_is_respected(heavy_baseline: CarbonInput) -> None:
    assert len(actions.rank_actions(heavy_baseline, limit=2)) <= 2


def test_savings_are_positive(heavy_baseline: CarbonInput) -> None:
    for a in actions.rank_actions(heavy_baseline, limit=99):
        assert a.annual_saving_kg > 0
        assert a.saving_per_effort > 0

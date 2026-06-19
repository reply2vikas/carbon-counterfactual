from __future__ import annotations

from app.carbon import actions, calculator
from app.insights import rules
from app.models import CarbonInput


def test_insight_mentions_total(heavy_baseline: CarbonInput) -> None:
    result = calculator.calculate(heavy_baseline)
    ranked = actions.rank_actions(heavy_baseline)
    text = rules.build_insight(heavy_baseline, result, ranked)
    assert "kg CO2e" in text
    assert len(text) > 0


def test_insight_handles_no_actions(light_baseline: CarbonInput) -> None:
    result = calculator.calculate(light_baseline)
    text = rules.build_insight(light_baseline, result, [])
    assert isinstance(text, str) and text


def test_under_target_is_acknowledged() -> None:
    data = CarbonInput(
        transport_mode="walk_cycle",
        weekly_km=0,
        diet="vegan",
        monthly_kwh=0,
        monthly_lpg_kg=0,
        annual_flight_hours=0,
    )
    result = calculator.calculate(data)
    text = rules.build_insight(data, result, [])
    assert "Paris-aligned target" in text

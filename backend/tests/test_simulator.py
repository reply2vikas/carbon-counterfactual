from __future__ import annotations

from app.carbon import calculator, simulator
from app.models import CarbonInput


def test_no_actions_leaves_baseline_unchanged(heavy_baseline: CarbonInput) -> None:
    res = simulator.simulate(heavy_baseline, [])
    assert res.projected_kg == res.baseline_kg
    assert res.annual_saving_kg == 0.0


def test_applying_action_reduces_footprint(heavy_baseline: CarbonInput) -> None:
    res = simulator.simulate(heavy_baseline, ["diet_vegetarian"])
    assert res.projected_kg < res.baseline_kg
    assert res.annual_saving_kg > 0


def test_unknown_action_keys_are_ignored(heavy_baseline: CarbonInput) -> None:
    res = simulator.simulate(heavy_baseline, ["does_not_exist"])
    assert res.projected_kg == res.baseline_kg


def test_projection_never_negative(light_baseline: CarbonInput) -> None:
    res = simulator.simulate(light_baseline, ["electricity_10"])
    assert res.projected_kg >= 0.0


def test_cost_delta_aggregates(heavy_baseline: CarbonInput) -> None:
    res = simulator.simulate(heavy_baseline, ["commute_metro", "electricity_10"])
    assert res.annual_cost_delta == sum(a.annual_cost_delta for a in res.applied_actions)


def test_paris_flag(heavy_baseline: CarbonInput) -> None:
    baseline = calculator.calculate(heavy_baseline)
    assert baseline.total_kg > 2000  # sanity: heavy lifestyle is over target
    res = simulator.simulate(heavy_baseline, [])
    assert res.meets_paris_target is False

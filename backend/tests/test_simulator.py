from __future__ import annotations

from app.actions.simulator import simulate
from app.carbon.calculator import compute_footprint
from app.models import CarbonInput


def test_no_actions_means_no_reduction(heavy_baseline: CarbonInput) -> None:
    res = simulate(heavy_baseline, [], 1)
    assert res.reduction_kg == 0.0
    assert res.projected_total_kg == res.baseline_total_kg


def test_actions_reduce_total(heavy_baseline: CarbonInput) -> None:
    res = simulate(heavy_baseline, ["diet_step", "led_lighting"], 1)
    assert res.projected_total_kg < res.baseline_total_kg
    assert res.reduction_kg > 0
    assert len(res.applied) == 2


def test_category_savings_capped_at_baseline(heavy_baseline: CarbonInput) -> None:
    # Stack every home action; combined saving cannot exceed the home baseline.
    res = simulate(heavy_baseline, ["led_lighting", "ac_setpoint", "rooftop_solar"], 1)
    home_base = compute_footprint(heavy_baseline).breakdown.home
    home_saved = sum(a.annual_savings_kg for a in res.applied if a.category == "home")
    assert home_saved <= home_base + 0.1


def test_unknown_and_duplicate_ids_ignored(heavy_baseline: CarbonInput) -> None:
    res = simulate(heavy_baseline, ["diet_step", "diet_step", "nope"], 1)
    assert len(res.applied) == 1


def test_horizon_multiplies_cumulative(heavy_baseline: CarbonInput) -> None:
    one = simulate(heavy_baseline, ["diet_step"], 1)
    five = simulate(heavy_baseline, ["diet_step"], 5)
    assert round(five.cumulative_savings_kg, 1) == round(one.cumulative_savings_kg * 5, 1)


def test_meets_target_for_light_profile(light_baseline: CarbonInput) -> None:
    res = simulate(light_baseline, [], 1)
    assert res.meets_target is True


def test_money_delta_accumulates(heavy_baseline: CarbonInput) -> None:
    res = simulate(heavy_baseline, ["led_lighting", "car_to_ev"], 1)
    assert res.money_delta_inr_year == -1500 + 25000


def test_sensitivity_band_brackets_projection(heavy_baseline: CarbonInput) -> None:
    res = simulate(heavy_baseline, ["diet_step", "led_lighting", "shift_car_to_rail"], 1)
    # Optimistic (low) <= central <= conservative (high), all non-negative.
    assert 0.0 <= res.projected_low_kg <= res.projected_total_kg <= res.projected_high_kg
    # With actions applied the band must be non-degenerate.
    assert res.projected_high_kg > res.projected_low_kg


def test_sensitivity_band_collapses_with_no_actions(heavy_baseline: CarbonInput) -> None:
    res = simulate(heavy_baseline, [], 1)
    # No reduction -> no uncertainty -> band collapses onto the baseline.
    assert res.projected_low_kg == res.projected_high_kg == res.projected_total_kg

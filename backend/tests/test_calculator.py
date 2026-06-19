from __future__ import annotations

from app.carbon import calculator
from app.carbon import factors as f
from app.models import CarbonInput


def test_zero_input_is_zero() -> None:
    result = calculator.calculate(CarbonInput(weekly_km=0, monthly_kwh=0))
    # diet defaults to medium_meat, so total is diet-only.
    expected_diet = round(f.DIET_KG_PER_DAY["medium_meat"] * f.DAYS_PER_YEAR, 2)
    assert result.breakdown.transport == 0.0
    assert result.breakdown.diet == expected_diet
    assert result.total_kg == expected_diet


def test_components_sum_to_total(heavy_baseline: CarbonInput) -> None:
    r = calculator.calculate(heavy_baseline)
    b = r.breakdown
    assert round(b.transport + b.diet + b.home + b.flights, 2) == r.total_kg


def test_transport_matches_factor(heavy_baseline: CarbonInput) -> None:
    r = calculator.calculate(heavy_baseline)
    expected = round(f.TRANSPORT_KG_PER_KM["car_petrol"] * 300 * f.WEEKS_PER_YEAR, 2)
    assert r.breakdown.transport == expected


def test_reference_ratios(heavy_baseline: CarbonInput) -> None:
    r = calculator.calculate(heavy_baseline)
    assert r.vs_global_avg == round(r.total_kg / f.GLOBAL_AVG_ANNUAL, 3)
    assert r.vs_paris_target == round(r.total_kg / f.PARIS_ALIGNED_TARGET, 3)


def test_largest_category(heavy_baseline: CarbonInput, light_baseline: CarbonInput) -> None:
    assert calculator.largest_category(calculator.calculate(heavy_baseline)) in {
        "transport",
        "diet",
        "home",
        "flights",
    }
    # A vegan cyclist with no transport: diet is the biggest remaining driver.
    assert calculator.largest_category(calculator.calculate(light_baseline)) == "diet"

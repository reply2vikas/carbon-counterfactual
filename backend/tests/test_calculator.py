from __future__ import annotations

from app.carbon import calculator as calc
from app.carbon import factors as f
from app.models import CarbonInput


def test_zero_input_is_diet_only() -> None:
    data = CarbonInput(diet="vegan")
    fp = calc.compute_footprint(data)
    assert fp.breakdown.transport == 0
    assert fp.breakdown.diet == f.DIET_FACTORS["vegan"]
    assert fp.total_kg == f.DIET_FACTORS["vegan"]


def test_transport_uses_correct_fuel_factor() -> None:
    petrol = calc.transport_annual(CarbonInput(car_km_week=100, car_fuel="car_petrol"))
    ev = calc.transport_annual(CarbonInput(car_km_week=100, car_fuel="car_ev"))
    assert petrol > ev


def test_flights_add_to_transport() -> None:
    base = calc.transport_annual(CarbonInput(car_km_week=10))
    with_flight = calc.transport_annual(CarbonInput(car_km_week=10, flight_hours_year=5))
    assert round(with_flight - base, 1) == round(5 * f.FLIGHT_FACTOR_PER_HOUR, 1)


def test_home_combines_electricity_and_lpg() -> None:
    data = CarbonInput(electricity_kwh_month=100, lpg_cylinders_month=2)
    expected = 100 * 12 * f.GRID_FACTOR_PER_KWH + 2 * 12 * f.LPG_FACTOR_PER_CYLINDER
    assert round(calc.home_annual(data), 1) == round(expected, 1)


def test_vs_target_pct_positive_when_above() -> None:
    fp = calc.compute_footprint(CarbonInput(diet="meat_heavy", car_km_week=500))
    assert fp.vs_target_pct > 0
    assert fp.target_kg == f.PARIS_ALIGNED_TARGET_KG

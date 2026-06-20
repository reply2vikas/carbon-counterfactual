"""Catalogue of reduction actions — the heart of the "counterfactual" product.

Each action knows how to estimate its OWN annual saving from a given baseline, so
recommendations are personalised to the user's actual numbers rather than generic
tips. Savings are deterministic functions of the input, which keeps the whole
recommendation engine unit-testable.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from app.carbon import calculator as calc
from app.carbon import factors as f
from app.models import CarbonInput, Category, Diet


@dataclass(frozen=True)
class ReductionAction:
    id: str
    label: str
    category: Category
    effort: int  # 1 (easy) .. 5 (hard)
    cost_inr_year: float  # negative = saves money
    _estimate: Callable[[CarbonInput], float]

    def annual_savings_kg(self, baseline: CarbonInput) -> float:
        """Clamp at 0 so an action never reports a negative saving."""
        return max(0.0, round(self._estimate(baseline), 1))


def _shift_car_to_rail(d: CarbonInput) -> float:
    # Move 40% of car km onto rail.
    moved = d.car_km_week * 0.40
    delta = f.TRANSPORT_FACTORS[d.car_fuel] - f.TRANSPORT_FACTORS["rail"]
    return moved * delta * f.WEEKS_PER_YEAR


def _car_to_ev(d: CarbonInput) -> float:
    if d.car_fuel == "car_ev":
        return 0.0
    delta = f.TRANSPORT_FACTORS[d.car_fuel] - f.TRANSPORT_FACTORS["car_ev"]
    return d.car_km_week * delta * f.WEEKS_PER_YEAR


def _drop_one_flight(d: CarbonInput) -> float:
    # Remove up to 4 flight-hours/year.
    return min(d.flight_hours_year, 4.0) * f.FLIGHT_FACTOR_PER_HOUR


def _diet_one_step_down(d: CarbonInput) -> float:
    ladder: list[Diet] = ["meat_heavy", "meat_medium", "pescatarian", "vegetarian", "vegan"]
    i = ladder.index(d.diet)
    if i >= len(ladder) - 1:
        return 0.0
    return f.DIET_FACTORS[d.diet] - f.DIET_FACTORS[ladder[i + 1]]


def _led_lighting(d: CarbonInput) -> float:
    return calc.home_annual(d) * 0.08


def _ac_setpoint(d: CarbonInput) -> float:
    # Raising the AC setpoint ~1C trims roughly 6% of electricity.
    elec = d.electricity_kwh_month * f.MONTHS_PER_YEAR * f.GRID_FACTOR_PER_KWH
    return elec * 0.06


def _rooftop_solar(d: CarbonInput) -> float:
    elec = d.electricity_kwh_month * f.MONTHS_PER_YEAR * f.GRID_FACTOR_PER_KWH
    return elec * 0.50


def _cut_fast_fashion(d: CarbonInput) -> float:
    return calc.consumption_annual(d) * 0.20


CATALOG: tuple[ReductionAction, ...] = (
    ReductionAction(
        "shift_car_to_rail", "Shift 40% of car trips to rail", "transport", 2, -8000, _shift_car_to_rail
    ),
    ReductionAction("car_to_ev", "Switch the car to electric", "transport", 5, 25000, _car_to_ev),
    ReductionAction(
        "drop_one_flight", "Drop one short flight this year", "transport", 3, -12000, _drop_one_flight
    ),
    ReductionAction("diet_step", "Move one step down the diet ladder", "diet", 3, -6000, _diet_one_step_down),
    ReductionAction("led_lighting", "Replace all bulbs with LEDs", "home", 1, -1500, _led_lighting),
    ReductionAction("ac_setpoint", "Raise AC setpoint by 1\u00b0C", "home", 1, -2000, _ac_setpoint),
    ReductionAction("rooftop_solar", "Install rooftop solar", "home", 5, 18000, _rooftop_solar),
    ReductionAction(
        "cut_fast_fashion", "Cut discretionary shopping by 20%", "consumption", 2, -9000, _cut_fast_fashion
    ),
)

BY_ID: dict[str, ReductionAction] = {a.id: a for a in CATALOG}

"""Pure-function carbon calculator.

Takes a validated lifestyle baseline and returns an annual footprint broken down
by category. Kept free of I/O and mutable globals (beyond the factor tables) on
purpose: pure functions are trivially unit-testable to 100% and make the numbers
the rest of the app reasons about fully deterministic.

Design note: every public function returns *annual* kilograms of CO2e so the four
category functions are directly comparable and can simply be summed.
"""

from __future__ import annotations

from app.carbon import factors as f
from app.models import Breakdown, CarbonInput, FootprintResult


def transport_annual(data: CarbonInput) -> float:
    """Annual transport CO2e from weekly distances plus flights.

    Weekly distances are multiplied out to a year; flights are already entered as
    hours-per-year, so they are added after the weekly-to-annual conversion rather
    than inside it. The car factor is looked up by the chosen fuel so an EV and a
    petrol car of the same mileage produce different numbers.
    """
    car = data.car_km_week * f.TRANSPORT_FACTORS[data.car_fuel]
    bus = data.bus_km_week * f.TRANSPORT_FACTORS["bus"]
    rail = data.rail_km_week * f.TRANSPORT_FACTORS["rail"]
    bike = data.motorbike_km_week * f.TRANSPORT_FACTORS["motorbike"]
    weekly = car + bus + rail + bike
    flights = data.flight_hours_year * f.FLIGHT_FACTOR_PER_HOUR
    # Weekly modes scale to a year; flights are already annual, so add them after.
    return weekly * f.WEEKS_PER_YEAR + flights


def diet_annual(data: CarbonInput) -> float:
    """Annual diet CO2e.

    Diet is modelled as a single annual figure per eating pattern (a lookup, not a
    per-meal calculation) because reliable per-meal data is noisy; the pattern-level
    figure is both defensible and stable for the simulator to reason about.
    """
    return f.DIET_FACTORS[data.diet]


def home_annual(data: CarbonInput) -> float:
    """Annual home-energy CO2e from grid electricity and LPG cooking gas.

    The two energy sources are kept as separate terms (rather than a single blended
    factor) so a reduction action can later target electricity alone without
    disturbing the cooking-gas component.
    """
    electricity = data.electricity_kwh_month * f.MONTHS_PER_YEAR * f.GRID_FACTOR_PER_KWH
    lpg = data.lpg_cylinders_month * f.MONTHS_PER_YEAR * f.LPG_FACTOR_PER_CYLINDER
    return electricity + lpg


def consumption_annual(data: CarbonInput) -> float:
    """Annual CO2e from discretionary spending (a spend-based EEIO estimate).

    Monthly spend is annualised, then converted at a per-1000-INR factor; dividing
    by 1000 keeps the factor's units explicit and easy to audit against the source.
    """
    annual_inr = data.shopping_inr_month * f.MONTHS_PER_YEAR
    return (annual_inr / 1000.0) * f.CONSUMPTION_FACTOR_PER_1000_INR


def compute_breakdown(data: CarbonInput) -> Breakdown:
    """Per-category annual footprint.

    Values are rounded to one decimal here so every downstream consumer (API
    response, simulator, UI) sees identical, display-stable numbers rather than
    re-rounding inconsistently.
    """
    return Breakdown(
        transport=round(transport_annual(data), 1),
        diet=round(diet_annual(data), 1),
        home=round(home_annual(data), 1),
        consumption=round(consumption_annual(data), 1),
    )


def compute_footprint(data: CarbonInput) -> FootprintResult:
    """Full footprint result: total, breakdown, and context baselines.

    `vs_target_pct` expresses how far above/below the Paris-aligned target the user
    is, which the UI needs for its headline. The `if target else 0.0` guard avoids a
    divide-by-zero if the target constant is ever set to zero.
    """
    breakdown = compute_breakdown(data)
    total = breakdown.transport + breakdown.diet + breakdown.home + breakdown.consumption
    target = f.PARIS_ALIGNED_TARGET_KG
    vs_target = ((total - target) / target) * 100.0 if target else 0.0
    return FootprintResult(
        total_kg=round(total, 1),
        breakdown=breakdown,
        global_average_kg=f.GLOBAL_AVERAGE_KG,
        india_average_kg=f.INDIA_AVERAGE_KG,
        target_kg=target,
        vs_target_pct=round(vs_target, 1),
    )

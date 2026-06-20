"""Pure-function carbon calculator.

Takes a validated lifestyle baseline and returns an annual footprint broken down
by category. No I/O and no mutable globals beyond the factor tables, which makes
every branch here trivially unit-testable to 100%.
"""

from __future__ import annotations

from app.carbon import factors as f
from app.models import Breakdown, CarbonInput, FootprintResult


def transport_annual(data: CarbonInput) -> float:
    """Annual transport kg CO2e from weekly distances plus flights."""
    car = data.car_km_week * f.TRANSPORT_FACTORS[data.car_fuel]
    bus = data.bus_km_week * f.TRANSPORT_FACTORS["bus"]
    rail = data.rail_km_week * f.TRANSPORT_FACTORS["rail"]
    bike = data.motorbike_km_week * f.TRANSPORT_FACTORS["motorbike"]
    weekly = car + bus + rail + bike
    flights = data.flight_hours_year * f.FLIGHT_FACTOR_PER_HOUR
    return weekly * f.WEEKS_PER_YEAR + flights


def diet_annual(data: CarbonInput) -> float:
    return f.DIET_FACTORS[data.diet]


def home_annual(data: CarbonInput) -> float:
    electricity = data.electricity_kwh_month * f.MONTHS_PER_YEAR * f.GRID_FACTOR_PER_KWH
    lpg = data.lpg_cylinders_month * f.MONTHS_PER_YEAR * f.LPG_FACTOR_PER_CYLINDER
    return electricity + lpg


def consumption_annual(data: CarbonInput) -> float:
    annual_inr = data.shopping_inr_month * f.MONTHS_PER_YEAR
    return (annual_inr / 1000.0) * f.CONSUMPTION_FACTOR_PER_1000_INR


def compute_breakdown(data: CarbonInput) -> Breakdown:
    return Breakdown(
        transport=round(transport_annual(data), 1),
        diet=round(diet_annual(data), 1),
        home=round(home_annual(data), 1),
        consumption=round(consumption_annual(data), 1),
    )


def compute_footprint(data: CarbonInput) -> FootprintResult:
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

"""Pure-function carbon calculator.

Takes a validated lifestyle baseline and returns an annual footprint broken down
by category. No I/O, no globals beyond the factor tables — which makes every path
here trivially unit-testable to 100%.
"""

from __future__ import annotations

from app.carbon import factors as f
from app.models import Breakdown, CarbonInput, FootprintResult


def _transport_annual(data: CarbonInput) -> float:
    per_km = f.TRANSPORT_KG_PER_KM.get(data.transport_mode, 0.0)
    weekly = per_km * data.weekly_km
    return weekly * f.WEEKS_PER_YEAR


def _diet_annual(data: CarbonInput) -> float:
    per_day = f.DIET_KG_PER_DAY.get(data.diet, 0.0)
    return per_day * f.DAYS_PER_YEAR


def _home_annual(data: CarbonInput) -> float:
    electricity = data.monthly_kwh * 12 * f.ELECTRICITY_KG_PER_KWH
    lpg = data.monthly_lpg_kg * 12 * f.LPG_KG_PER_KG
    return electricity + lpg


def _flights_annual(data: CarbonInput) -> float:
    return data.annual_flight_hours * f.FLIGHT_KG_PER_HOUR


def calculate(data: CarbonInput) -> FootprintResult:
    """Compute the annual footprint and a per-category breakdown."""
    transport = round(_transport_annual(data), 2)
    diet = round(_diet_annual(data), 2)
    home = round(_home_annual(data), 2)
    flights = round(_flights_annual(data), 2)
    total = round(transport + diet + home + flights, 2)

    breakdown = Breakdown(
        transport=transport,
        diet=diet,
        home=home,
        flights=flights,
    )
    return FootprintResult(
        total_kg=total,
        breakdown=breakdown,
        vs_global_avg=round(total / f.GLOBAL_AVG_ANNUAL, 3),
        vs_paris_target=round(total / f.PARIS_ALIGNED_TARGET, 3),
    )


def largest_category(result: FootprintResult) -> str:
    """Return the name of the category contributing the most emissions."""
    b = result.breakdown
    categories = {
        "transport": b.transport,
        "diet": b.diet,
        "home": b.home,
        "flights": b.flights,
    }
    return max(categories, key=lambda k: categories[k])

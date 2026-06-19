"""Marginal-abatement action ranker.

This is the part that sets the product apart from a plain calculator. Each
candidate reduction action knows how much CO2e it removes for *this* user's
baseline, plus an effort and a rupee cost. We rank by abatement-per-effort so the
advice is realistic — biggest, easiest, cheapest wins float to the top — rather
than a generic tip list.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from app.carbon import factors as f
from app.models import ActionImpact, CarbonInput


@dataclass(frozen=True)
class _Candidate:
    key: str
    label: str
    # A function of the baseline returning annual kg CO2e saved.
    saving_fn: Callable[[CarbonInput], float]
    effort: int  # 1 (trivial) .. 5 (hard)
    annual_cost_delta: float  # negative = saves money


def _diet_saving(data: CarbonInput, target: str) -> float:
    current = f.DIET_KG_PER_DAY.get(data.diet, 0.0)
    new = f.DIET_KG_PER_DAY.get(target, current)
    return max(0.0, (current - new) * f.DAYS_PER_YEAR)


def _commute_shift_saving(data: CarbonInput, target: str) -> float:
    current = f.TRANSPORT_KG_PER_KM.get(data.transport_mode, 0.0)
    new = f.TRANSPORT_KG_PER_KM.get(target, current)
    weekly = max(0.0, (current - new) * data.weekly_km)
    return weekly * f.WEEKS_PER_YEAR


def _electricity_saving(data: CarbonInput, fraction: float) -> float:
    return data.monthly_kwh * 12 * f.ELECTRICITY_KG_PER_KWH * fraction


def _flight_saving(data: CarbonInput, hours_cut: float) -> float:
    cut = min(hours_cut, data.annual_flight_hours)
    return cut * f.FLIGHT_KG_PER_HOUR


def _catalogue() -> list[_Candidate]:
    return [
        _Candidate(
            "diet_low_meat",
            "Shift to a low-meat diet",
            lambda d: _diet_saving(d, "low_meat"),
            effort=2,
            annual_cost_delta=-3000.0,
        ),
        _Candidate(
            "diet_vegetarian",
            "Go vegetarian",
            lambda d: _diet_saving(d, "vegetarian"),
            effort=3,
            annual_cost_delta=-6000.0,
        ),
        _Candidate(
            "commute_metro",
            "Switch commute to metro",
            lambda d: _commute_shift_saving(d, "metro"),
            effort=2,
            annual_cost_delta=-18000.0,
        ),
        _Candidate(
            "commute_ev",
            "Switch to an EV",
            lambda d: _commute_shift_saving(d, "car_ev"),
            effort=4,
            annual_cost_delta=20000.0,
        ),
        _Candidate(
            "electricity_10",
            "Cut electricity use 10% (efficient appliances)",
            lambda d: _electricity_saving(d, 0.10),
            effort=1,
            annual_cost_delta=-2400.0,
        ),
        _Candidate(
            "one_fewer_flight",
            "Take 4 fewer flight-hours per year",
            lambda d: _flight_saving(d, 4.0),
            effort=3,
            annual_cost_delta=-12000.0,
        ),
    ]


def rank_actions(data: CarbonInput, limit: int = 4) -> list[ActionImpact]:
    """Return reduction actions ranked by abatement-per-effort, biggest first.

    Actions that save nothing for this baseline (e.g. an EV swap when the user
    already cycles) are dropped so the list stays personalized.
    """
    scored: list[ActionImpact] = []
    for c in _catalogue():
        saving = round(c.saving_fn(data), 2)
        if saving <= 0:
            continue
        scored.append(
            ActionImpact(
                key=c.key,
                label=c.label,
                annual_saving_kg=saving,
                effort=c.effort,
                annual_cost_delta=c.annual_cost_delta,
                saving_per_effort=round(saving / c.effort, 2),
            )
        )
    scored.sort(key=lambda a: a.saving_per_effort, reverse=True)
    return scored[:limit]

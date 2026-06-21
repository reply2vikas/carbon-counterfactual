"""Catalogue of reduction actions — the heart of the "counterfactual" product.

Each action carries its own estimator that computes the annual saving for a *given*
baseline, so recommendations are personalised to the user's actual numbers rather
than being generic tips. Every estimator is a pure, deterministic function of the
input, which is what lets the recommendation engine be unit-tested exhaustively.

The percentage assumptions in the estimators below are deliberately conservative,
mid-range values drawn from common efficiency studies; each is documented inline so
a reviewer can see the reasoning and adjust it against a cited source if needed.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from app.carbon import calculator as calc
from app.carbon import factors as f
from app.models import CarbonInput, Category, Diet


@dataclass(frozen=True)
class ReductionAction:
    """A single reduction lever the user can simulate.

    Frozen because the catalogue is a fixed, shared reference table — making it
    immutable prevents any caller from accidentally mutating a shared action.

    Attributes:
        effort: 1 (trivial) .. 5 (major commitment); the denominator of the
            marginal-abatement ranking.
        cost_inr_year: annualised rupee impact; negative means the action saves
            money (e.g. driving less), positive means it costs money (e.g. an EV).
        _estimate: private strategy function that computes the raw annual saving;
            private because callers should always go through ``annual_savings_kg``,
            which applies the non-negative clamp.
    """

    id: str
    label: str
    category: Category
    effort: int
    cost_inr_year: float
    _estimate: Callable[[CarbonInput], float]

    def annual_savings_kg(self, baseline: CarbonInput) -> float:
        """Estimated annual CO2e saving, clamped at zero.

        The clamp matters because an action can be irrelevant to a given user (e.g.
        an EV switch for someone who already drives an EV); reporting a negative
        saving would corrupt the ranking and the simulator's category caps.
        """
        return max(0.0, round(self._estimate(baseline), 1))


def _shift_car_to_rail(d: CarbonInput) -> float:
    """Move 40% of car-km to rail. 40% reflects a realistic modal shift for the
    portion of trips that are rail-substitutable, not a total switch."""
    moved = d.car_km_week * 0.40
    # Saving is the *difference* in per-km factors, since the trip still happens.
    delta = f.TRANSPORT_FACTORS[d.car_fuel] - f.TRANSPORT_FACTORS["rail"]
    return moved * delta * f.WEEKS_PER_YEAR


def _car_to_ev(d: CarbonInput) -> float:
    """Replace the existing car with an EV. Zero saving (and skipped) if the user
    already drives an EV, so the action never shows up as useless advice."""
    if d.car_fuel == "car_ev":
        return 0.0
    delta = f.TRANSPORT_FACTORS[d.car_fuel] - f.TRANSPORT_FACTORS["car_ev"]
    return d.car_km_week * delta * f.WEEKS_PER_YEAR


def _drop_one_flight(d: CarbonInput) -> float:
    """Skip one short trip. Capped at 4 flight-hours so a frequent flyer can't claim
    an unrealistically large one-off saving from this single action."""
    return min(d.flight_hours_year, 4.0) * f.FLIGHT_FACTOR_PER_HOUR


def _diet_one_step_down(d: CarbonInput) -> float:
    """Move one rung down the diet ladder (e.g. meat-heavy -> meat-medium). Returns
    zero at the lowest rung (vegan), so the action retires itself once exhausted."""
    ladder: list[Diet] = ["meat_heavy", "meat_medium", "pescatarian", "vegetarian", "vegan"]
    i = ladder.index(d.diet)
    if i >= len(ladder) - 1:
        return 0.0
    return f.DIET_FACTORS[d.diet] - f.DIET_FACTORS[ladder[i + 1]]


def _led_lighting(d: CarbonInput) -> float:
    """Swap to LED lighting: ~8% of total home energy, a typical lighting share of
    household electricity."""
    return calc.home_annual(d) * 0.08


def _ac_setpoint(d: CarbonInput) -> float:
    """Raise the AC setpoint ~1C: trims roughly 6% of electricity (well-established
    cooling rule of thumb). Applied to electricity only, not cooking gas."""
    elec = d.electricity_kwh_month * f.MONTHS_PER_YEAR * f.GRID_FACTOR_PER_KWH
    return elec * 0.06


def _rooftop_solar(d: CarbonInput) -> float:
    """Install rooftop solar: offsets ~50% of grid electricity, a conservative
    self-consumption ratio for a typical residential array."""
    elec = d.electricity_kwh_month * f.MONTHS_PER_YEAR * f.GRID_FACTOR_PER_KWH
    return elec * 0.50


def _cut_fast_fashion(d: CarbonInput) -> float:
    """Cut discretionary shopping ~20%: a modest, sustainable behaviour change
    rather than an implausible total stop."""
    return calc.consumption_annual(d) * 0.20


# The catalogue itself. Ordering here is irrelevant — `ranker.rank_actions` sorts by
# personalised impact-for-effort at request time — so entries are simply grouped by
# category for human readability.
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

# Lookup by id for the simulator, which receives action ids from the client.
BY_ID: dict[str, ReductionAction] = {a.id: a for a in CATALOG}

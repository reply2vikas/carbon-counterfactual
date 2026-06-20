from __future__ import annotations

import pytest

from app.actions.catalog import BY_ID, CATALOG
from app.models import CarbonInput


def test_all_ids_unique() -> None:
    ids = [a.id for a in CATALOG]
    assert len(ids) == len(set(ids))


def test_savings_never_negative() -> None:
    data = CarbonInput(diet="vegan")  # already lowest diet
    assert BY_ID["diet_step"].annual_savings_kg(data) == 0.0


def test_ev_action_zero_when_already_ev() -> None:
    data = CarbonInput(car_km_week=200, car_fuel="car_ev")
    assert BY_ID["car_to_ev"].annual_savings_kg(data) == 0.0


@pytest.mark.parametrize("action_id", list(BY_ID))
def test_every_action_returns_float(action_id: str) -> None:
    data = CarbonInput(
        car_km_week=100, flight_hours_year=8, electricity_kwh_month=200, shopping_inr_month=10000
    )
    assert BY_ID[action_id].annual_savings_kg(data) >= 0.0

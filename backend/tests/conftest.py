"""Shared fixtures."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.deps import get_repository
from app.main import app
from app.models import CarbonInput


@pytest.fixture
def client() -> TestClient:
    get_repository.cache_clear()
    return TestClient(app)


@pytest.fixture
def heavy_baseline() -> CarbonInput:
    return CarbonInput(
        car_km_week=300,
        car_fuel="car_petrol",
        rail_km_week=20,
        flight_hours_year=10,
        diet="meat_heavy",
        electricity_kwh_month=400,
        lpg_cylinders_month=1,
        shopping_inr_month=15000,
    )


@pytest.fixture
def light_baseline() -> CarbonInput:
    return CarbonInput(diet="vegan", rail_km_week=10, electricity_kwh_month=50)

"""Shared fixtures."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models import CarbonInput


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def heavy_baseline() -> CarbonInput:
    return CarbonInput(
        transport_mode="car_petrol",
        weekly_km=300,
        diet="heavy_meat",
        monthly_kwh=400,
        monthly_lpg_kg=15,
        annual_flight_hours=20,
    )


@pytest.fixture
def light_baseline() -> CarbonInput:
    return CarbonInput(
        transport_mode="walk_cycle",
        weekly_km=20,
        diet="vegan",
        monthly_kwh=80,
        monthly_lpg_kg=2,
        annual_flight_hours=0,
    )

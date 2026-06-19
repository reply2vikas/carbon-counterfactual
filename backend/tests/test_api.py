from __future__ import annotations

from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_security_headers_present(client: TestClient) -> None:
    r = client.get("/api/health")
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert r.headers["X-Frame-Options"] == "DENY"


def test_footprint_endpoint(client: TestClient) -> None:
    payload = {
        "transport_mode": "car_petrol",
        "weekly_km": 200,
        "diet": "heavy_meat",
        "monthly_kwh": 300,
        "monthly_lpg_kg": 10,
        "annual_flight_hours": 10,
    }
    r = client.post("/api/footprint", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["result"]["total_kg"] > 0
    assert len(body["ranked_actions"]) > 0
    assert isinstance(body["insight"], str)


def test_footprint_rejects_bad_input(client: TestClient) -> None:
    r = client.post("/api/footprint", json={"weekly_km": -5})
    assert r.status_code == 422


def test_footprint_rejects_unknown_field(client: TestClient) -> None:
    r = client.post("/api/footprint", json={"hacker_field": 1})
    assert r.status_code == 422


def test_simulate_endpoint(client: TestClient) -> None:
    payload = {
        "input": {
            "transport_mode": "car_petrol",
            "weekly_km": 200,
            "diet": "heavy_meat",
            "monthly_kwh": 300,
            "monthly_lpg_kg": 10,
            "annual_flight_hours": 10,
        },
        "selected_actions": ["diet_vegetarian", "commute_metro"],
    }
    r = client.post("/api/simulate", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["projected_kg"] < body["baseline_kg"]

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


def test_calculate_and_history_roundtrip(client: TestClient) -> None:
    payload = {"car_km_week": 200, "diet": "meat_heavy", "electricity_kwh_month": 300}
    r = client.post("/api/calculate", json=payload, headers={"X-Device-Id": "dev1"})
    assert r.status_code == 200
    total = r.json()["total_kg"]
    assert total > 0

    h = client.get("/api/history", headers={"X-Device-Id": "dev1"})
    assert h.status_code == 200
    assert len(h.json()) == 1
    assert h.json()[0]["total_kg"] == total


def test_actions_endpoint_ranked(client: TestClient) -> None:
    payload = {"car_km_week": 300, "diet": "meat_heavy", "electricity_kwh_month": 400}
    r = client.post("/api/actions", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert len(body) > 0
    vals = [a["abatement_per_effort"] for a in body]
    assert vals == sorted(vals, reverse=True)


def test_simulate_endpoint(client: TestClient) -> None:
    payload = {
        "baseline": {"car_km_week": 300, "diet": "meat_heavy", "electricity_kwh_month": 400},
        "action_ids": ["diet_step", "led_lighting"],
        "horizon_years": 5,
    }
    r = client.post("/api/simulate", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["projected_total_kg"] < body["baseline_total_kg"]
    assert body["cumulative_savings_kg"] == round(body["reduction_kg"] * 5, 1)


def test_insights_endpoint_fallback(client: TestClient) -> None:
    payload = {"baseline": {"car_km_week": 300, "diet": "meat_heavy"}}
    r = client.post("/api/insights", json=payload)
    assert r.status_code == 200
    assert r.json()["source"] == "rules"


def test_calculate_rejects_bad_input(client: TestClient) -> None:
    r = client.post("/api/calculate", json={"car_km_week": -5})
    assert r.status_code == 422

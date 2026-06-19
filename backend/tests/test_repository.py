from __future__ import annotations

from app.carbon import calculator
from app.models import CarbonInput
from app.repository.memory import InMemoryRepository


def test_save_and_history_roundtrip() -> None:
    repo = InMemoryRepository()
    result = calculator.calculate(CarbonInput(weekly_km=100))
    repo.save("device-1", result)
    repo.save("device-1", result)
    history = repo.history("device-1")
    assert len(history) == 2
    assert history[0].total_kg == result.total_kg


def test_history_is_scoped_by_device() -> None:
    repo = InMemoryRepository()
    repo.save("device-a", calculator.calculate(CarbonInput()))
    assert repo.history("device-b") == []


def test_history_limit() -> None:
    repo = InMemoryRepository()
    for _ in range(30):
        repo.save("d", calculator.calculate(CarbonInput()))
    assert len(repo.history("d", limit=5)) == 5

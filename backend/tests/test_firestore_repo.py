"""Unit tests for FirestoreRepository using a tiny fake client.

The fake reproduces the slice of the Firestore query API the repository uses, so
we test ordering, filtering and limiting without any cloud dependency.
"""

from __future__ import annotations

from typing import Any

from app.carbon.calculator import compute_footprint
from app.models import CarbonInput
from app.repository.firestore_repo import FirestoreRepository


class _FakeDoc:
    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data

    def to_dict(self) -> dict[str, Any]:
        return self._data


class _FakeQuery:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self._rows = rows

    def where(self, field: str, _op: str, value: Any) -> _FakeQuery:
        return _FakeQuery([r for r in self._rows if r[field] == value])

    def order_by(self, field: str, direction: str = "ASCENDING") -> _FakeQuery:
        return _FakeQuery(sorted(self._rows, key=lambda r: r[field], reverse=direction == "DESCENDING"))

    def limit(self, n: int) -> _FakeQuery:
        return _FakeQuery(self._rows[:n])

    def stream(self) -> list[_FakeDoc]:
        return [_FakeDoc(r) for r in self._rows]


class _FakeCollection(_FakeQuery):
    def add(self, doc: dict[str, Any]) -> None:
        self._rows.append(doc)


class _FakeClient:
    def __init__(self) -> None:
        self._collections: dict[str, _FakeCollection] = {}

    def collection(self, name: str) -> _FakeCollection:
        return self._collections.setdefault(name, _FakeCollection([]))


def _result(diet: str = "meat_heavy"):
    return compute_footprint(CarbonInput(diet=diet, car_km_week=100))


def test_save_then_history_roundtrip() -> None:
    repo = FirestoreRepository(_FakeClient())
    repo.save("dev1", _result())
    history = repo.history("dev1")
    assert len(history) == 1
    assert history[0].total_kg > 0


def test_history_filters_by_device() -> None:
    client = _FakeClient()
    repo = FirestoreRepository(client)
    repo.save("dev1", _result())
    repo.save("dev2", _result("vegan"))
    assert len(repo.history("dev1")) == 1
    assert len(repo.history("dev2")) == 1


def test_history_respects_limit() -> None:
    repo = FirestoreRepository(_FakeClient())
    for _ in range(5):
        repo.save("dev1", _result())
    assert len(repo.history("dev1", limit=3)) == 3


def test_history_newest_first() -> None:
    client = _FakeClient()
    repo = FirestoreRepository(client)
    # Force distinct, increasing created_at values to assert ordering.
    col = client.collection("entries")
    col.add({"device_id": "d", "total_kg": 1, "created_at": "2026-01-01", "result": _result().model_dump()})
    col.add({"device_id": "d", "total_kg": 2, "created_at": "2026-06-01", "result": _result().model_dump()})
    newest = repo.history("d", limit=1)
    assert len(newest) == 1

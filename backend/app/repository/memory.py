"""In-memory repository — the default store, ideal for tests and local dev."""

from __future__ import annotations

from collections import defaultdict

from app.models import FootprintResult


class InMemoryRepository:
    def __init__(self) -> None:
        self._data: dict[str, list[FootprintResult]] = defaultdict(list)

    def save(self, device_id: str, result: FootprintResult) -> None:
        self._data[device_id].append(result)

    def history(self, device_id: str, limit: int = 20) -> list[FootprintResult]:
        return list(reversed(self._data[device_id]))[:limit]

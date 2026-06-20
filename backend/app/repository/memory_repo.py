"""In-memory repository. Default for local/dev and fully deterministic in tests.

Swap for a Firestore implementation (see firestore.rules) in production by binding
the same protocol in app.deps.
"""

from __future__ import annotations

from collections import defaultdict

from app.models import FootprintResult


class MemoryRepository:
    def __init__(self) -> None:
        self._store: dict[str, list[FootprintResult]] = defaultdict(list)

    def save(self, device_id: str, result: FootprintResult) -> None:
        self._store[device_id].append(result)

    def history(self, device_id: str, limit: int = 20) -> list[FootprintResult]:
        return list(reversed(self._store[device_id][-limit:]))

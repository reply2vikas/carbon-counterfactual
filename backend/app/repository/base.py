"""Repository protocol — the storage contract the API depends on.

Routes depend on this abstraction, not on a concrete database, so swapping the
in-memory store for Firestore is a one-line change in main.py.
"""

from __future__ import annotations

from typing import Protocol

from app.models import FootprintResult


class FootprintRepository(Protocol):
    def save(self, device_id: str, result: FootprintResult) -> None: ...

    def history(self, device_id: str, limit: int = 20) -> list[FootprintResult]: ...

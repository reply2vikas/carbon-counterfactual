"""Repository protocol — the seam between routes and storage."""

from __future__ import annotations

from typing import Protocol

from app.models import FootprintResult


class EntryRepository(Protocol):
    def save(self, device_id: str, result: FootprintResult) -> None: ...
    def history(self, device_id: str, limit: int = 20) -> list[FootprintResult]: ...

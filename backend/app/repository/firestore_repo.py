"""Firestore-backed EntryRepository.

Deliberately imports NO google SDK: it accepts any client exposing the minimal
Firestore surface (`collection().add(...)` and
`collection().where().order_by().limit().stream()`). That keeps this module fully
unit-testable with a fake client and swappable for the real
`google.cloud.firestore.Client`, which is constructed in app.deps.

The stored shape matches firestore.rules (append-only, requires device_id /
total_kg / created_at).
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from app.models import FootprintResult


class FirestoreRepository:
    def __init__(self, client: Any, collection: str = "entries") -> None:
        self._client = client
        self._collection = collection

    def save(self, device_id: str, result: FootprintResult) -> None:
        payload = {
            "device_id": device_id,
            "total_kg": result.total_kg,
            "created_at": datetime.now(UTC).isoformat(),
            "result": result.model_dump(),
        }
        self._client.collection(self._collection).add(payload)

    def history(self, device_id: str, limit: int = 20) -> list[FootprintResult]:
        docs = (
            self._client.collection(self._collection)
            .where("device_id", "==", device_id)
            .order_by("created_at", direction="DESCENDING")
            .limit(limit)
            .stream()
        )
        return [FootprintResult(**doc.to_dict()["result"]) for doc in docs]

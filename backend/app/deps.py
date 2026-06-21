"""Dependency wiring — the single place that binds the storage implementation.

Defaults to the in-memory repository so the app runs anywhere with zero setup.
Set USE_FIRESTORE=true (and provision a Firestore database) to switch to durable,
multi-instance persistence; the real client is imported lazily so the SDK is only
touched when actually enabled.
"""

from __future__ import annotations

from functools import lru_cache

from app.config import get_settings
from app.repository.base import EntryRepository
from app.repository.memory_repo import MemoryRepository


@lru_cache
def get_repository() -> EntryRepository:
    settings = get_settings()
    if settings.use_firestore:  # pragma: no cover - requires a provisioned Firestore
        from google.cloud import firestore

        from app.repository.firestore_repo import FirestoreRepository

        client = firestore.Client(project=settings.google_cloud_project or None)
        return FirestoreRepository(client)
    return MemoryRepository()

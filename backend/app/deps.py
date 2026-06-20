"""Dependency wiring. Single place that binds the storage implementation."""

from __future__ import annotations

from functools import lru_cache

from app.repository.memory_repo import MemoryRepository


@lru_cache
def get_repository() -> MemoryRepository:
    return MemoryRepository()

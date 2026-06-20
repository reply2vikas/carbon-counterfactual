"""Liveness probe — no I/O so it stays sub-millisecond on Cloud Run."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

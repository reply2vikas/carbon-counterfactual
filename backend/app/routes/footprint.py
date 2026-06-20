"""Footprint + ranked-actions endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Header

from app.actions.ranker import rank_actions
from app.carbon.calculator import compute_footprint
from app.deps import get_repository
from app.models import ActionView, CarbonInput, FootprintResult
from app.repository.memory_repo import MemoryRepository

router = APIRouter(prefix="/api", tags=["footprint"])


@router.post("/calculate", response_model=FootprintResult)
def calculate(
    payload: CarbonInput,
    x_device_id: str = Header(default="anonymous"),
    repo: MemoryRepository = Depends(get_repository),
) -> FootprintResult:
    result = compute_footprint(payload)
    repo.save(x_device_id, result)
    return result


@router.post("/actions", response_model=list[ActionView])
def actions(payload: CarbonInput) -> list[ActionView]:
    return rank_actions(payload)


@router.get("/history", response_model=list[FootprintResult])
def history(
    x_device_id: str = Header(default="anonymous"),
    repo: MemoryRepository = Depends(get_repository),
) -> list[FootprintResult]:
    return repo.history(x_device_id)

"""Footprint calculation + ranked actions + insight."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Header

from app.carbon import actions as action_mod
from app.carbon import calculator
from app.config import Settings, get_settings
from app.insights import gemini
from app.models import CarbonInput, FootprintResponse

router = APIRouter()


@router.post("/api/footprint", response_model=FootprintResponse)
def footprint(
    data: CarbonInput,
    settings: Settings = Depends(get_settings),
    x_device_id: str | None = Header(default=None),
) -> FootprintResponse:
    result = calculator.calculate(data)
    ranked = action_mod.rank_actions(data)
    insight = gemini.generate_insight(settings, data, result, ranked)
    return FootprintResponse(result=result, ranked_actions=ranked, insight=insight)

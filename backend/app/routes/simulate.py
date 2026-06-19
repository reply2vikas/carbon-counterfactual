"""What-if scenario projection."""

from __future__ import annotations

from fastapi import APIRouter

from app.carbon import simulator
from app.models import ScenarioRequest, ScenarioResult

router = APIRouter()


@router.post("/api/simulate", response_model=ScenarioResult)
def simulate(req: ScenarioRequest) -> ScenarioResult:
    return simulator.simulate(req.input, req.selected_actions)

"""What-if simulation + insight endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from app.actions.simulator import simulate
from app.insights import gemini
from app.models import InsightRequest, InsightResponse, SimulationRequest, SimulationResult

router = APIRouter(prefix="/api", tags=["simulate"])


@router.post("/simulate", response_model=SimulationResult)
def run_simulation(payload: SimulationRequest) -> SimulationResult:
    return simulate(payload.baseline, payload.action_ids, payload.horizon_years)


@router.post("/insights", response_model=InsightResponse)
def insights(payload: InsightRequest) -> InsightResponse:
    return gemini.generate(payload.baseline, payload.simulation)

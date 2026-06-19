"""Pydantic v2 schemas — the validated contract for the API.

These models double as the first security boundary: every numeric field has a
bound, so nonsensical or hostile payloads are rejected before any logic runs.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

TransportMode = Literal[
    "car_petrol", "car_diesel", "car_ev", "bus", "metro", "motorbike", "walk_cycle"
]
Diet = Literal["heavy_meat", "medium_meat", "low_meat", "pescatarian", "vegetarian", "vegan"]


class CarbonInput(BaseModel):
    """A lightweight lifestyle baseline. All ranges are validated."""

    model_config = {"extra": "forbid"}

    transport_mode: TransportMode = "car_petrol"
    weekly_km: float = Field(0.0, ge=0, le=5_000)
    diet: Diet = "medium_meat"
    monthly_kwh: float = Field(0.0, ge=0, le=10_000)
    monthly_lpg_kg: float = Field(0.0, ge=0, le=500)
    annual_flight_hours: float = Field(0.0, ge=0, le=500)


class Breakdown(BaseModel):
    transport: float
    diet: float
    home: float
    flights: float


class FootprintResult(BaseModel):
    total_kg: float
    breakdown: Breakdown
    vs_global_avg: float
    vs_paris_target: float


class ActionImpact(BaseModel):
    key: str
    label: str
    annual_saving_kg: float
    effort: int = Field(ge=1, le=5)
    annual_cost_delta: float
    saving_per_effort: float


class ScenarioRequest(BaseModel):
    model_config = {"extra": "forbid"}

    input: CarbonInput
    selected_actions: list[str] = Field(default_factory=list, max_length=20)


class ScenarioResult(BaseModel):
    baseline_kg: float
    projected_kg: float
    annual_saving_kg: float
    annual_cost_delta: float
    meets_paris_target: bool
    applied_actions: list[ActionImpact]


class FootprintResponse(BaseModel):
    result: FootprintResult
    ranked_actions: list[ActionImpact]
    insight: str

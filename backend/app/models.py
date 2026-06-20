"""Pydantic schemas — the validated contract for the whole API.

These models double as input validation: nonsensical values (negative distances,
unknown diets) are rejected before any business logic runs, which is both a
security and a code-quality property.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

TransportMode = Literal["car_petrol", "car_diesel", "car_ev", "bus", "rail", "motorbike"]
Diet = Literal["meat_heavy", "meat_medium", "pescatarian", "vegetarian", "vegan"]
Category = Literal["transport", "diet", "home", "consumption"]


class CarbonInput(BaseModel):
    """A lightweight lifestyle baseline. Every field is bounded."""

    model_config = {"extra": "forbid"}

    car_km_week: float = Field(0.0, ge=0, le=5000)
    car_fuel: TransportMode = "car_petrol"
    bus_km_week: float = Field(0.0, ge=0, le=5000)
    rail_km_week: float = Field(0.0, ge=0, le=5000)
    motorbike_km_week: float = Field(0.0, ge=0, le=5000)
    flight_hours_year: float = Field(0.0, ge=0, le=500)
    diet: Diet = "meat_medium"
    electricity_kwh_month: float = Field(0.0, ge=0, le=10000)
    lpg_cylinders_month: float = Field(0.0, ge=0, le=20)
    shopping_inr_month: float = Field(0.0, ge=0, le=1_000_000)


class Breakdown(BaseModel):
    transport: float
    diet: float
    home: float
    consumption: float


class FootprintResult(BaseModel):
    total_kg: float
    breakdown: Breakdown
    global_average_kg: float
    india_average_kg: float
    target_kg: float
    vs_target_pct: float = Field(description="Positive = above the Paris-aligned target")


class ActionView(BaseModel):
    id: str
    label: str
    category: Category
    annual_savings_kg: float
    effort: int = Field(ge=1, le=5)
    cost_inr_year: float = Field(description="Negative means the action saves money")
    abatement_per_effort: float = Field(description="kg CO2e saved per unit of effort")
    cost_per_kg: float | None = Field(description="INR per kg CO2e; null if it saves money")


class SimulationRequest(BaseModel):
    model_config = {"extra": "forbid"}

    baseline: CarbonInput
    action_ids: list[str] = Field(default_factory=list, max_length=50)
    horizon_years: int = Field(1, ge=1, le=10)


class AppliedAction(BaseModel):
    id: str
    label: str
    category: Category
    annual_savings_kg: float


class SimulationResult(BaseModel):
    baseline_total_kg: float
    projected_total_kg: float
    reduction_kg: float
    reduction_pct: float
    meets_target: bool
    cumulative_savings_kg: float
    money_delta_inr_year: float
    applied: list[AppliedAction]


class InsightRequest(BaseModel):
    model_config = {"extra": "forbid"}

    baseline: CarbonInput
    simulation: SimulationResult | None = None


class InsightResponse(BaseModel):
    headline: str
    actions: list[str]
    source: Literal["gemini", "rules"]

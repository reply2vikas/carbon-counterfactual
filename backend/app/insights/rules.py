"""Deterministic, rule-based insight generator.

This is the always-available fallback used when Gemini is not configured or fails.
Because it is pure and deterministic it is fully unit-testable, and it guarantees
the product still gives personalised advice with zero external dependencies.
"""

from __future__ import annotations

from app.actions.ranker import rank_actions
from app.carbon.calculator import compute_footprint
from app.models import CarbonInput, InsightResponse, SimulationResult


def generate(baseline: CarbonInput, simulation: SimulationResult | None) -> InsightResponse:
    """Build a personalised headline + up to four tips from the user's own numbers.

    This is the deterministic fallback for ``gemini.generate``. It leads with the
    user's single largest emission source (the highest-leverage thing to mention
    first) and then surfaces the top-ranked actions. Keeping it deterministic means
    the product degrades gracefully — identical, sensible advice — whenever the LLM
    is unavailable, and it can be asserted exactly in tests.
    """
    footprint = compute_footprint(baseline)
    bd = footprint.breakdown
    categories = {"transport": bd.transport, "diet": bd.diet, "home": bd.home, "consumption": bd.consumption}
    # Lead with the biggest contributor — it is where the user has the most to gain.
    biggest = max(categories, key=lambda k: categories[k])

    over = footprint.total_kg - footprint.target_kg
    if over > 0:
        headline = (
            f"Your footprint is about {footprint.total_kg:.0f} kg CO2e/year, "
            f"{over:.0f} kg above the Paris-aligned target. Your largest source is {biggest}."
        )
    else:
        headline = (
            f"Your footprint is about {footprint.total_kg:.0f} kg CO2e/year, "
            f"already at or below the Paris-aligned target. Nice."
        )

    ranked = rank_actions(baseline)
    tips = [f"{v.label}: saves ~{v.annual_savings_kg:.0f} kg/year (effort {v.effort}/5)" for v in ranked[:3]]
    if simulation is not None and simulation.applied:
        tips.append(
            f"Your selected actions cut ~{simulation.reduction_pct:.0f}% "
            f"({simulation.reduction_kg:.0f} kg/year)."
        )
    if not tips:
        tips = ["No high-impact actions found for this profile — you're already lean."]

    return InsightResponse(headline=headline, actions=tips, source="rules")

"""Deterministic, rule-based insight generator.

This is the always-on fallback (and the default). It produces a personalized,
quantified narrative with zero external calls — so the product works offline,
costs nothing, and is fully testable. Gemini, when enabled, only enriches this.
"""

from __future__ import annotations

from app.carbon import calculator
from app.models import ActionImpact, CarbonInput, FootprintResult


def _phrase_for_category(name: str) -> str:
    return {
        "transport": "how you get around",
        "diet": "what you eat",
        "home": "your home energy use",
        "flights": "your flying",
    }.get(name, name)


def build_insight(data: CarbonInput, result: FootprintResult, actions: list[ActionImpact]) -> str:
    biggest = calculator.largest_category(result)
    parts: list[str] = []

    if result.vs_paris_target <= 1.0:
        parts.append(
            f"Your estimated footprint is {result.total_kg:,.0f} kg CO2e a year — "
            "already at or below the Paris-aligned target. Strong position."
        )
    else:
        over = result.total_kg - 2_000.0
        parts.append(
            f"Your estimated footprint is {result.total_kg:,.0f} kg CO2e a year, "
            f"about {over:,.0f} kg above the Paris-aligned target."
        )

    parts.append(
        f"The largest driver is {_phrase_for_category(biggest)}, so that is where "
        "a change pays off most."
    )

    if actions:
        top = actions[0]
        parts.append(
            f"Highest-leverage move: {top.label.lower()} — about "
            f"{top.annual_saving_kg:,.0f} kg CO2e saved a year for relatively low effort."
        )
    return " ".join(parts)

"""Gemini (Vertex AI) insight generator with a guaranteed fallback.

If Gemini is configured and responds, we return its narrative; on any failure we
fall back to the deterministic rules engine. This mirrors the resilient pattern the
leading hackathon repos use and means the product never hard-fails on the AI path.
"""

from __future__ import annotations

import logging

from app.config import get_settings
from app.insights import rules
from app.models import CarbonInput, InsightResponse, SimulationResult

logger = logging.getLogger(__name__)


def _build_prompt(baseline: CarbonInput, simulation: SimulationResult | None) -> str:
    lines = [
        "You are a concise sustainability coach. Given a person's annual carbon",
        "baseline and an optional simulated action set, write a one-sentence headline",
        "and 3 short, specific, encouraging next actions. Avoid guilt; be practical.",
        f"Baseline: {baseline.model_dump_json()}",
    ]
    if simulation is not None:
        lines.append(f"Simulation: {simulation.model_dump_json()}")
    return "\n".join(lines)


def generate(baseline: CarbonInput, simulation: SimulationResult | None) -> InsightResponse:
    settings = get_settings()
    if not settings.gemini_api_key:
        return rules.generate(baseline, simulation)

    try:  # pragma: no cover - network path, exercised only with real creds
        from google import genai

        client = genai.Client(api_key=settings.gemini_api_key)
        prompt = _build_prompt(baseline, simulation)
        resp = client.models.generate_content(model=settings.gemini_model, contents=prompt)
        text = (resp.text or "").strip()
        if not text:
            raise ValueError("empty response")
        head, *rest = [line for line in text.splitlines() if line.strip()]
        return InsightResponse(
            headline=head, actions=rest[:3] or ["See your ranked actions below."], source="gemini"
        )
    except Exception as exc:  # pragma: no cover - defensive
        logger.warning("Gemini insight failed, using rules fallback: %s", exc)
        return rules.generate(baseline, simulation)

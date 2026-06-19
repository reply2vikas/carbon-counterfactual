"""Optional Gemini (Vertex AI) enrichment with a hard rule-based fallback.

If Gemini is disabled or unavailable, this returns the deterministic insight,
so a missing key or a network blip never breaks a request.
"""

from __future__ import annotations

import logging

from app.config import Settings
from app.insights import rules
from app.models import ActionImpact, CarbonInput, FootprintResult

logger = logging.getLogger(__name__)


def generate_insight(
    settings: Settings,
    data: CarbonInput,
    result: FootprintResult,
    actions: list[ActionImpact],
) -> str:
    fallback = rules.build_insight(data, result, actions)
    if not settings.use_gemini or not settings.gemini_api_key:
        return fallback
    try:  # pragma: no cover - exercised only with live credentials
        from google import genai

        client = genai.Client(api_key=settings.gemini_api_key)
        action_lines = "\n".join(
            f"- {a.label}: saves {a.annual_saving_kg:.0f} kg/yr" for a in actions
        )
        prompt = (
            "Write two encouraging sentences for someone whose annual carbon "
            f"footprint is {result.total_kg:.0f} kg CO2e. Their top reduction "
            f"actions are:\n{action_lines}\nBe concrete and non-preachy."
        )
        response = client.models.generate_content(model=settings.gemini_model, contents=prompt)
        text = (response.text or "").strip()
        return text or fallback
    except Exception:  # pragma: no cover - defensive
        logger.warning("Gemini call failed; using rule-based insight", exc_info=True)
        return fallback

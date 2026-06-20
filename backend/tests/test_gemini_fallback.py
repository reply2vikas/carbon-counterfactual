from __future__ import annotations

from app.insights import gemini
from app.models import CarbonInput


def test_gemini_falls_back_to_rules_without_key(monkeypatch, heavy_baseline: CarbonInput) -> None:
    # No API key configured -> deterministic rules path.
    gemini.get_settings.cache_clear()
    monkeypatch.setenv("GEMINI_API_KEY", "")
    out = gemini.generate(heavy_baseline, None)
    assert out.source == "rules"
    gemini.get_settings.cache_clear()


def test_build_prompt_includes_simulation(heavy_baseline: CarbonInput) -> None:
    from app.actions.simulator import simulate

    sim = simulate(heavy_baseline, ["diet_step"], 1)
    with_sim = gemini._build_prompt(heavy_baseline, sim)
    without = gemini._build_prompt(heavy_baseline, None)
    assert "Simulation" in with_sim
    assert "Simulation" not in without

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


def test_gemini_falls_back_when_sdk_unavailable(monkeypatch, heavy_baseline: CarbonInput) -> None:
    # A key is present, but the google-genai SDK is not installed in CI, so the
    # import fails and generate() must degrade gracefully to the rules engine
    # instead of raising a 500.
    gemini.get_settings.cache_clear()
    monkeypatch.setenv("GEMINI_API_KEY", "test-key-not-real")
    out = gemini.generate(heavy_baseline, None)
    assert out.source == "rules"
    assert out.headline
    gemini.get_settings.cache_clear()


def test_gemini_degrades_gracefully_when_call_fails(monkeypatch, heavy_baseline: CarbonInput) -> None:
    # A key is configured, but the real Gemini path cannot run in tests
    # (SDK/credentials absent) -> must NOT crash, must fall back to deterministic rules.
    gemini.get_settings.cache_clear()
    monkeypatch.setenv("GEMINI_API_KEY", "test-key-not-real")
    out = gemini.generate(heavy_baseline, None)
    assert out.source == "rules"
    assert out.headline
    gemini.get_settings.cache_clear()

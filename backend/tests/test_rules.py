from __future__ import annotations

from app.actions.simulator import simulate
from app.insights import rules
from app.models import CarbonInput


def test_rules_flag_over_target(heavy_baseline: CarbonInput) -> None:
    out = rules.generate(heavy_baseline, None)
    assert out.source == "rules"
    assert "above" in out.headline
    assert 1 <= len(out.actions) <= 4


def test_rules_praise_under_target(light_baseline: CarbonInput) -> None:
    out = rules.generate(light_baseline, None)
    assert "below" in out.headline or "target" in out.headline


def test_rules_include_simulation_summary(heavy_baseline: CarbonInput) -> None:
    sim = simulate(heavy_baseline, ["diet_step"], 1)
    out = rules.generate(heavy_baseline, sim)
    assert any("%" in a for a in out.actions)


def test_rules_handles_no_available_actions() -> None:
    # Lowest-impact profile: no ranked actions and no simulation -> fallback line.
    out = rules.generate(CarbonInput(diet="vegan"), None)
    assert len(out.actions) == 1

import type { ScenarioResult } from "../lib/types";

interface Props {
  scenario: ScenarioResult | null;
}

export function ScenarioSimulator({ scenario }: Props) {
  if (!scenario) {
    return (
      <section className="panel" aria-labelledby="sim-heading">
        <p className="eyebrow">The counterfactual</p>
        <h2 id="sim-heading">Your possible future</h2>
        <p>Add one or more changes above to project the footprint you would have.</p>
      </section>
    );
  }
  const pct = scenario.baseline_kg
    ? Math.round((scenario.annual_saving_kg / scenario.baseline_kg) * 100)
    : 0;
  const cost = scenario.annual_cost_delta;
  return (
    <section className="panel" aria-labelledby="sim-heading" aria-live="polite">
      <p className="eyebrow">The counterfactual</p>
      <h2 id="sim-heading">Your possible future</h2>
      <p>
        <span className={`figure ${scenario.meets_paris_target ? "under" : "over"}`}>
          {scenario.projected_kg.toLocaleString()} kg
        </span>{" "}
        CO2e per year
      </p>
      <p>
        Down {scenario.annual_saving_kg.toLocaleString()} kg ({pct}%) from your baseline of{" "}
        {scenario.baseline_kg.toLocaleString()} kg.{" "}
        {cost < 0
          ? `You would also save about ₹${Math.abs(cost).toLocaleString()} a year.`
          : cost > 0
            ? `This would cost about ₹${cost.toLocaleString()} more a year.`
            : ""}
      </p>
      <p>
        {scenario.meets_paris_target
          ? "This future meets the Paris-aligned target. 🌿"
          : "Still above the Paris-aligned target — try adding another change."}
      </p>
    </section>
  );
}

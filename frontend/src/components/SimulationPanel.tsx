import { inr, kg } from "../lib/format";
import type { SimulationResult } from "../lib/types";

export function SimulationPanel({ sim }: { sim: SimulationResult }) {
  return (
    <section className="card" aria-labelledby="sim-h" aria-live="polite">
      <h2 id="sim-h">Your simulated future</h2>
      <p>
        Projected: <strong>{kg(sim.projected_total_kg)}</strong> /year — down {sim.reduction_pct}% (
        {kg(sim.reduction_kg)}).
      </p>
      <p className={sim.meets_target ? "meets" : "miss"}>
        {sim.meets_target
          ? "This reaches the Paris-aligned target."
          : "Still above target — add more actions."}
      </p>
      <p>
        Money impact: {inr(sim.money_delta_inr_year)}. Cumulative saved over horizon:{" "}
        {kg(sim.cumulative_savings_kg)}.
      </p>
    </section>
  );
}

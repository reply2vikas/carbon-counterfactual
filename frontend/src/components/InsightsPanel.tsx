import type { FootprintResult } from "../lib/types";

interface Props {
  result: FootprintResult;
  insight: string;
}

export function InsightsPanel({ result, insight }: Props) {
  const overTarget = result.vs_paris_target > 1;
  return (
    <section className="panel" aria-labelledby="insight-heading" aria-live="polite">
      <p className="eyebrow">Where you stand</p>
      <h2 id="insight-heading">
        <span className={`figure ${overTarget ? "over" : "under"}`}>
          {result.total_kg.toLocaleString()} kg
        </span>{" "}
        CO2e per year
      </h2>
      <p>{insight}</p>
      <p>
        That is {result.vs_global_avg.toFixed(2)}× the global average and{" "}
        {result.vs_paris_target.toFixed(2)}× the Paris-aligned target of 2,000 kg.
      </p>
    </section>
  );
}

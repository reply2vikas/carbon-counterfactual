import { kg } from "../lib/format";
import type { FootprintResult } from "../lib/types";

export function ResultPanel({ result }: { result: FootprintResult }) {
  const over = result.total_kg > result.target_kg;
  return (
    <section className="card" aria-labelledby="result-h" aria-live="polite">
      <h2 id="result-h">Your footprint</h2>
      <p className="total">{kg(result.total_kg)} <span style={{ fontSize: "1rem" }}>CO₂e / year</span></p>
      <p className={over ? "miss" : "meets"}>
        {over
          ? `${kg(result.total_kg - result.target_kg)} above the Paris-aligned target`
          : "At or below the Paris-aligned target"}
      </p>
      <ul>
        <li>Transport: {kg(result.breakdown.transport)}</li>
        <li>Diet: {kg(result.breakdown.diet)}</li>
        <li>Home: {kg(result.breakdown.home)}</li>
        <li>Consumption: {kg(result.breakdown.consumption)}</li>
      </ul>
    </section>
  );
}

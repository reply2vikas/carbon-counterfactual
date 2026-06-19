import { useState } from "react";
import "./theme.css";
import { ActionRanker } from "./components/ActionRanker";
import { BaselineForm } from "./components/BaselineForm";
import { InsightsPanel } from "./components/InsightsPanel";
import { ScenarioSimulator } from "./components/ScenarioSimulator";
import { getFootprint, simulate } from "./lib/api";
import type { CarbonInput, FootprintResponse, ScenarioResult } from "./lib/types";

export default function App() {
  const [data, setData] = useState<FootprintResponse | null>(null);
  const [input, setInput] = useState<CarbonInput | null>(null);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [scenario, setScenario] = useState<ScenarioResult | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(form: CarbonInput) {
    setBusy(true);
    setError(null);
    try {
      const res = await getFootprint(form);
      setData(res);
      setInput(form);
      setSelected(new Set());
      setScenario(null);
    } catch {
      setError("Could not reach the calculator. Check the API is running and try again.");
    } finally {
      setBusy(false);
    }
  }

  async function toggle(key: string) {
    if (!input) return;
    const next = new Set(selected);
    next.has(key) ? next.delete(key) : next.add(key);
    setSelected(next);
    try {
      setScenario(await simulate(input, [...next]));
    } catch {
      setError("Could not run the projection. Try again.");
    }
  }

  return (
    <main className="shell">
      <header>
        <p className="eyebrow">Carbon Counterfactual</p>
        <h1>See the footprint you could have.</h1>
        <p>
          Estimate where your emissions come from, then simulate the future you would get
          from realistic changes — ranked by impact for the effort.
        </p>
      </header>

      <BaselineForm onSubmit={handleSubmit} busy={busy} />

      {error && (
        <p className="panel over" role="alert">
          {error}
        </p>
      )}

      {data && (
        <>
          <InsightsPanel result={data.result} insight={data.insight} />
          <ActionRanker actions={data.ranked_actions} selected={selected} onToggle={toggle} />
          <ScenarioSimulator scenario={scenario} />
        </>
      )}
    </main>
  );
}

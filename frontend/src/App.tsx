import { useState } from "react";
import { ActionList } from "./components/ActionList";
import { CalculatorForm } from "./components/CalculatorForm";
import { ResultPanel } from "./components/ResultPanel";
import { SimulationPanel } from "./components/SimulationPanel";
import * as api from "./lib/api";
import { DEFAULT_INPUT } from "./lib/types";
import type { ActionView, CarbonInput, FootprintResult, SimulationResult } from "./lib/types";

export default function App() {
  const [input, setInput] = useState<CarbonInput>(DEFAULT_INPUT);
  const [result, setResult] = useState<FootprintResult | null>(null);
  const [actions, setActions] = useState<ActionView[]>([]);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [sim, setSim] = useState<SimulationResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function onCalculate() {
    try {
      setError(null);
      const [fp, acts] = await Promise.all([api.calculate(input), api.rankActions(input)]);
      setResult(fp);
      setActions(acts);
      setSelected(new Set());
      setSim(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong");
    }
  }

  async function onToggle(id: string) {
    const next = new Set(selected);
    if (next.has(id)) next.delete(id);
    else next.add(id);
    setSelected(next);
    try {
      setSim(await api.simulate(input, [...next], 5));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Simulation failed");
    }
  }

  return (
    <main className="app">
      <h1>Carbon Counterfactual</h1>
      <p className="tagline">Model your footprint, then simulate the future you could choose.</p>
      <CalculatorForm value={input} onChange={setInput} onSubmit={onCalculate} />
      {error && (
        <p role="alert" className="miss">
          {error}
        </p>
      )}
      {result && <ResultPanel result={result} />}
      {actions.length > 0 && (
        <ActionList actions={actions} selected={selected} onToggle={onToggle} />
      )}
      {sim && <SimulationPanel sim={sim} />}
    </main>
  );
}

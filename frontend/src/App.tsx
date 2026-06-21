/**
 * App — the single-page orchestrator for Carbon Counterfactual.
 *
 * Owns all client state and the two user flows:
 *  1. Calculate — fetch the footprint and the impact-ranked actions for the
 *     current baseline (run in parallel since neither depends on the other).
 *  2. Toggle/simulate — every time the user adds or removes an action, re-run the
 *     what-if simulation so the projected future updates live.
 *
 * Presentation lives entirely in the child components; this file is wiring only.
 */
import { useState } from "react";
import { ActionList } from "./components/ActionList";
import { CalculatorForm } from "./components/CalculatorForm";
import { ResultPanel } from "./components/ResultPanel";
import { SimulationPanel } from "./components/SimulationPanel";
import * as api from "./lib/api";
import { DEFAULT_INPUT } from "./lib/types";
import type { ActionView, CarbonInput, FootprintResult, SimulationResult } from "./lib/types";

const SIMULATION_HORIZON_YEARS = 5;

export default function App() {
  const [input, setInput] = useState<CarbonInput>(DEFAULT_INPUT);
  const [result, setResult] = useState<FootprintResult | null>(null);
  const [actions, setActions] = useState<ActionView[]>([]);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [sim, setSim] = useState<SimulationResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  /** Compute the footprint + ranked actions, and reset any prior simulation. */
  async function onCalculate() {
    try {
      setError(null);
      // Footprint and action ranking are independent → fetch concurrently.
      const [fp, acts] = await Promise.all([api.calculate(input), api.rankActions(input)]);
      setResult(fp);
      setActions(acts);
      // A new baseline invalidates the previous selection/simulation.
      setSelected(new Set());
      setSim(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong");
    }
  }

  /** Add/remove an action and immediately re-simulate the resulting future. */
  async function onToggle(id: string) {
    const next = new Set(selected);
    if (next.has(id)) next.delete(id);
    else next.add(id);
    setSelected(next);
    try {
      setSim(await api.simulate(input, [...next], SIMULATION_HORIZON_YEARS));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Simulation failed");
    }
  }

  // Panels render progressively as data becomes available, so the page is usable
  // from the first interaction rather than waiting on a full result set.
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

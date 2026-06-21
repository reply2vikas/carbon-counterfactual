// useSimulator — owns the calculator's client state and the data flows that act on
// it (calculate, toggle/simulate). Extracted from the App component so the view
// stays declarative and the logic is independently testable and reusable.
import { useState } from "react";
import * as api from "../lib/api";
import { DEFAULT_INPUT } from "../lib/types";
import type { ActionView, CarbonInput, FootprintResult, SimulationResult } from "../lib/types";

const SIMULATION_HORIZON_YEARS = 5;

export interface Simulator {
  input: CarbonInput;
  setInput: (next: CarbonInput) => void;
  result: FootprintResult | null;
  actions: ActionView[];
  selected: Set<string>;
  sim: SimulationResult | null;
  error: string | null;
  calculate: () => Promise<void>;
  toggleAction: (id: string) => Promise<void>;
}

export function useSimulator(): Simulator {
  const [input, setInput] = useState<CarbonInput>(DEFAULT_INPUT);
  const [result, setResult] = useState<FootprintResult | null>(null);
  const [actions, setActions] = useState<ActionView[]>([]);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [sim, setSim] = useState<SimulationResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  /** Compute the footprint + ranked actions, and reset any prior simulation. */
  async function calculate(): Promise<void> {
    try {
      setError(null);
      // Footprint and ranking are independent → fetch concurrently.
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
  async function toggleAction(id: string): Promise<void> {
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

  return { input, setInput, result, actions, selected, sim, error, calculate, toggleAction };
}

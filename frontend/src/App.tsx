/**
 * App — the single-page composition root for Carbon Counterfactual.
 *
 * All state and data flows live in the `useSimulator` hook; this component is
 * purely declarative wiring. Panels render progressively as data arrives, so the
 * page is usable from the first interaction.
 */
import { ActionList } from "./components/ActionList";
import { CalculatorForm } from "./components/CalculatorForm";
import { ResultPanel } from "./components/ResultPanel";
import { SimulationPanel } from "./components/SimulationPanel";
import { useSimulator } from "./hooks/useSimulator";

export default function App() {
  const { input, setInput, result, actions, selected, sim, error, calculate, toggleAction } =
    useSimulator();

  return (
    <main className="app">
      <h1>Carbon Counterfactual</h1>
      <p className="tagline">Model your footprint, then simulate the future you could choose.</p>
      <CalculatorForm value={input} onChange={setInput} onSubmit={calculate} />
      {error && (
        <p role="alert" className="miss">
          {error}
        </p>
      )}
      {result && <ResultPanel result={result} />}
      {actions.length > 0 && (
        <ActionList actions={actions} selected={selected} onToggle={toggleAction} />
      )}
      {sim && <SimulationPanel sim={sim} />}
    </main>
  );
}

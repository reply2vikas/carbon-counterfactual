import { inr, kg } from "../lib/format";
import type { ActionView } from "../lib/types";

interface Props {
  actions: ActionView[];
  selected: Set<string>;
  onToggle: (id: string) => void;
}

export function ActionList({ actions, selected, onToggle }: Props) {
  return (
    <section className="card" aria-labelledby="actions-h">
      <h2 id="actions-h">Reductions ranked by impact-for-effort</h2>
      <fieldset style={{ border: 0, padding: 0, margin: 0 }}>
        <legend className="sr-only">Select actions to simulate</legend>
        {actions.map((a) => (
          <label key={a.id} className="action">
            <span>
              <input type="checkbox" checked={selected.has(a.id)} onChange={() => onToggle(a.id)} />{" "}
              {a.label}
            </span>
            <span>
              {kg(a.annual_savings_kg)}/yr · effort {a.effort}/5 · {inr(a.cost_inr_year)}
            </span>
          </label>
        ))}
      </fieldset>
    </section>
  );
}

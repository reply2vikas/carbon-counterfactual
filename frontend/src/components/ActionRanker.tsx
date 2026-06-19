import type { ActionImpact } from "../lib/types";

interface Props {
  actions: ActionImpact[];
  selected: Set<string>;
  onToggle: (key: string) => void;
}

const effortWords = ["", "trivial", "easy", "moderate", "hard", "very hard"];

export function ActionRanker({ actions, selected, onToggle }: Props) {
  return (
    <section className="panel" aria-labelledby="actions-heading">
      <p className="eyebrow">Ranked by impact for the effort</p>
      <h2 id="actions-heading">Changes worth your time</h2>
      <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
        {actions.map((a) => {
          const on = selected.has(a.key);
          return (
            <li key={a.key}>
              <button
                type="button"
                className="action"
                role="checkbox"
                aria-checked={on}
                aria-pressed={on}
                onClick={() => onToggle(a.key)}
                style={{ width: "100%", background: "transparent", color: "inherit", border: "none" }}
              >
                <span>
                  <strong>{a.label}</strong>
                  <br />
                  <small>
                    saves {a.annual_saving_kg.toLocaleString()} kg/yr · effort:{" "}
                    {effortWords[a.effort]}
                  </small>
                </span>
                <span aria-hidden="true">{on ? "✓ added" : "+ add"}</span>
              </button>
            </li>
          );
        })}
      </ul>
    </section>
  );
}

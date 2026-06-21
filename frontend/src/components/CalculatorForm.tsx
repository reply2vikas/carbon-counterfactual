// CalculatorForm — accessible inputs for the lifestyle baseline. Controlled by
// the parent so all state stays in one place; emits changes via onChange.
import type { ChangeEvent } from "react";

import type { CarbonInput, Diet, TransportMode } from "../lib/types";

interface Props {
  value: CarbonInput;
  onChange: (next: CarbonInput) => void;
  onSubmit: () => void;
}

const FUELS: TransportMode[] = ["car_petrol", "car_diesel", "car_ev", "bus", "rail", "motorbike"];
const DIETS: Diet[] = ["meat_heavy", "meat_medium", "pescatarian", "vegetarian", "vegan"];

export function CalculatorForm({ value, onChange, onSubmit }: Props) {
  const num = (k: keyof CarbonInput) => (e: ChangeEvent<HTMLInputElement>) =>
    onChange({ ...value, [k]: Number(e.target.value) });

  return (
    <section className="card" aria-labelledby="form-h">
      <h2 id="form-h">Your lifestyle baseline</h2>
      <div className="grid">
        <label>
          Car km / week
          <input type="number" min={0} value={value.car_km_week} onChange={num("car_km_week")} />
        </label>
        <label>
          Car fuel
          <select
            value={value.car_fuel}
            onChange={(e) => onChange({ ...value, car_fuel: e.target.value as TransportMode })}
          >
            {FUELS.map((f) => (
              <option key={f} value={f}>
                {f.replace("_", " ")}
              </option>
            ))}
          </select>
        </label>
        <label>
          Rail km / week
          <input type="number" min={0} value={value.rail_km_week} onChange={num("rail_km_week")} />
        </label>
        <label>
          Flight hours / year
          <input
            type="number"
            min={0}
            value={value.flight_hours_year}
            onChange={num("flight_hours_year")}
          />
        </label>
        <label>
          Diet
          <select
            value={value.diet}
            onChange={(e) => onChange({ ...value, diet: e.target.value as Diet })}
          >
            {DIETS.map((d) => (
              <option key={d} value={d}>
                {d.replace("_", " ")}
              </option>
            ))}
          </select>
        </label>
        <label>
          Electricity kWh / month
          <input
            type="number"
            min={0}
            value={value.electricity_kwh_month}
            onChange={num("electricity_kwh_month")}
          />
        </label>
        <label>
          Shopping ₹ / month
          <input
            type="number"
            min={0}
            value={value.shopping_inr_month}
            onChange={num("shopping_inr_month")}
          />
        </label>
      </div>
      <p>
        <button type="button" onClick={onSubmit}>
          Calculate footprint
        </button>
      </p>
    </section>
  );
}

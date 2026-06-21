// CalculatorForm — the lifestyle baseline inputs. Composes reusable NumberField
// primitives plus two selects; fully controlled by the parent so all state lives
// in one place. Accessible by construction (labelled section + labelled fields).
import { NumberField } from "./NumberField";
import type { CarbonInput, Diet, TransportMode } from "../lib/types";

interface Props {
  value: CarbonInput;
  onChange: (next: CarbonInput) => void;
  onSubmit: () => void;
}

const FUELS: TransportMode[] = ["car_petrol", "car_diesel", "car_ev", "bus", "rail", "motorbike"];
const DIETS: Diet[] = ["meat_heavy", "meat_medium", "pescatarian", "vegetarian", "vegan"];

export function CalculatorForm({ value, onChange, onSubmit }: Props) {
  // One helper builds the per-field setter, so every numeric field stays one line.
  const set = (k: keyof CarbonInput) => (n: number) => onChange({ ...value, [k]: n });

  return (
    <section className="card" aria-labelledby="form-h">
      <h2 id="form-h">Your lifestyle baseline</h2>
      <div className="grid">
        <NumberField
          label="Car km / week"
          value={value.car_km_week}
          onValueChange={set("car_km_week")}
        />
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
        <NumberField
          label="Rail km / week"
          value={value.rail_km_week}
          onValueChange={set("rail_km_week")}
        />
        <NumberField
          label="Flight hours / year"
          value={value.flight_hours_year}
          onValueChange={set("flight_hours_year")}
        />
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
        <NumberField
          label="Electricity kWh / month"
          value={value.electricity_kwh_month}
          onValueChange={set("electricity_kwh_month")}
        />
        <NumberField
          label="Shopping ₹ / month"
          value={value.shopping_inr_month}
          onValueChange={set("shopping_inr_month")}
        />
      </div>
      <p>
        <button type="button" onClick={onSubmit}>
          Calculate footprint
        </button>
      </p>
    </section>
  );
}

import { useState } from "react";
import type { CarbonInput, Diet, TransportMode } from "../lib/types";

const TRANSPORT: { value: TransportMode; label: string }[] = [
  { value: "car_petrol", label: "Petrol car" },
  { value: "car_diesel", label: "Diesel car" },
  { value: "car_ev", label: "Electric car" },
  { value: "bus", label: "Bus" },
  { value: "metro", label: "Metro / train" },
  { value: "motorbike", label: "Motorbike" },
  { value: "walk_cycle", label: "Walk or cycle" },
];

const DIETS: { value: Diet; label: string }[] = [
  { value: "heavy_meat", label: "Meat with most meals" },
  { value: "medium_meat", label: "Meat most days" },
  { value: "low_meat", label: "A little meat" },
  { value: "pescatarian", label: "Fish, no meat" },
  { value: "vegetarian", label: "Vegetarian" },
  { value: "vegan", label: "Vegan" },
];

const DEFAULTS: CarbonInput = {
  transport_mode: "car_petrol",
  weekly_km: 150,
  diet: "medium_meat",
  monthly_kwh: 250,
  monthly_lpg_kg: 8,
  annual_flight_hours: 6,
};

interface Props {
  onSubmit: (input: CarbonInput) => void;
  busy: boolean;
}

export function BaselineForm({ onSubmit, busy }: Props) {
  const [form, setForm] = useState<CarbonInput>(DEFAULTS);

  const update = <K extends keyof CarbonInput>(key: K, value: CarbonInput[K]) =>
    setForm((prev) => ({ ...prev, [key]: value }));

  return (
    <section className="panel" aria-labelledby="baseline-heading">
      <h2 id="baseline-heading">Your week, roughly</h2>
      <div>
        <label htmlFor="transport">How you mostly travel</label>
        <select
          id="transport"
          value={form.transport_mode}
          onChange={(e) => update("transport_mode", e.target.value as TransportMode)}
        >
          {TRANSPORT.map((t) => (
            <option key={t.value} value={t.value}>
              {t.label}
            </option>
          ))}
        </select>

        <label htmlFor="weekly_km">Kilometres travelled per week</label>
        <input
          id="weekly_km"
          type="number"
          min={0}
          max={5000}
          value={form.weekly_km}
          onChange={(e) => update("weekly_km", Number(e.target.value))}
        />

        <label htmlFor="diet">What you eat</label>
        <select
          id="diet"
          value={form.diet}
          onChange={(e) => update("diet", e.target.value as Diet)}
        >
          {DIETS.map((d) => (
            <option key={d.value} value={d.value}>
              {d.label}
            </option>
          ))}
        </select>

        <label htmlFor="kwh">Home electricity per month (kWh)</label>
        <input
          id="kwh"
          type="number"
          min={0}
          max={10000}
          value={form.monthly_kwh}
          onChange={(e) => update("monthly_kwh", Number(e.target.value))}
        />

        <label htmlFor="flights">Hours flown per year</label>
        <input
          id="flights"
          type="number"
          min={0}
          max={500}
          value={form.annual_flight_hours}
          onChange={(e) => update("annual_flight_hours", Number(e.target.value))}
        />
      </div>
      <button type="button" onClick={() => onSubmit(form)} disabled={busy}>
        {busy ? "Working…" : "See my footprint"}
      </button>
    </section>
  );
}

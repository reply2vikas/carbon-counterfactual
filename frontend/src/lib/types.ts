// Shared API types — the single source of truth mirroring the backend Pydantic
// models, so the client and server agree on the contract at compile time.
export type TransportMode = "car_petrol" | "car_diesel" | "car_ev" | "bus" | "rail" | "motorbike";
export type Diet = "meat_heavy" | "meat_medium" | "pescatarian" | "vegetarian" | "vegan";
export type Category = "transport" | "diet" | "home" | "consumption";

export interface CarbonInput {
  car_km_week: number;
  car_fuel: TransportMode;
  bus_km_week: number;
  rail_km_week: number;
  motorbike_km_week: number;
  flight_hours_year: number;
  diet: Diet;
  electricity_kwh_month: number;
  lpg_cylinders_month: number;
  shopping_inr_month: number;
}

export interface Breakdown {
  transport: number;
  diet: number;
  home: number;
  consumption: number;
}
export interface FootprintResult {
  total_kg: number;
  breakdown: Breakdown;
  global_average_kg: number;
  india_average_kg: number;
  target_kg: number;
  vs_target_pct: number;
}
export interface ActionView {
  id: string;
  label: string;
  category: Category;
  annual_savings_kg: number;
  effort: number;
  cost_inr_year: number;
  abatement_per_effort: number;
  cost_per_kg: number | null;
}
export interface SimulationResult {
  baseline_total_kg: number;
  projected_total_kg: number;
  projected_low_kg: number;
  projected_high_kg: number;
  reduction_kg: number;
  reduction_pct: number;
  meets_target: boolean;
  cumulative_savings_kg: number;
  money_delta_inr_year: number;
  applied: { id: string; label: string; category: Category; annual_savings_kg: number }[];
}

export const DEFAULT_INPUT: CarbonInput = {
  car_km_week: 150,
  car_fuel: "car_petrol",
  bus_km_week: 0,
  rail_km_week: 30,
  motorbike_km_week: 0,
  flight_hours_year: 6,
  diet: "meat_medium",
  electricity_kwh_month: 250,
  lpg_cylinders_month: 1,
  shopping_inr_month: 8000,
};

export type TransportMode =
  | "car_petrol"
  | "car_diesel"
  | "car_ev"
  | "bus"
  | "metro"
  | "motorbike"
  | "walk_cycle";

export type Diet =
  | "heavy_meat"
  | "medium_meat"
  | "low_meat"
  | "pescatarian"
  | "vegetarian"
  | "vegan";

export interface CarbonInput {
  transport_mode: TransportMode;
  weekly_km: number;
  diet: Diet;
  monthly_kwh: number;
  monthly_lpg_kg: number;
  annual_flight_hours: number;
}

export interface Breakdown {
  transport: number;
  diet: number;
  home: number;
  flights: number;
}

export interface FootprintResult {
  total_kg: number;
  breakdown: Breakdown;
  vs_global_avg: number;
  vs_paris_target: number;
}

export interface ActionImpact {
  key: string;
  label: string;
  annual_saving_kg: number;
  effort: number;
  annual_cost_delta: number;
  saving_per_effort: number;
}

export interface FootprintResponse {
  result: FootprintResult;
  ranked_actions: ActionImpact[];
  insight: string;
}

export interface ScenarioResult {
  baseline_kg: number;
  projected_kg: number;
  annual_saving_kg: number;
  annual_cost_delta: number;
  meets_paris_target: boolean;
  applied_actions: ActionImpact[];
}

import type { ActionView, CarbonInput, FootprintResult, SimulationResult } from "./types";

const BASE = import.meta.env.VITE_API_BASE ?? "";

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`Request to ${path} failed (${res.status})`);
  return (await res.json()) as T;
}

export const calculate = (input: CarbonInput) => post<FootprintResult>("/api/calculate", input);
export const rankActions = (input: CarbonInput) => post<ActionView[]>("/api/actions", input);
export const simulate = (baseline: CarbonInput, action_ids: string[], horizon_years: number) =>
  post<SimulationResult>("/api/simulate", { baseline, action_ids, horizon_years });

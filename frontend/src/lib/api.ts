import type { CarbonInput, FootprintResponse, ScenarioResult } from "./types";

const BASE = import.meta.env.VITE_API_BASE ?? "";

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    throw new Error(`Request to ${path} failed (${res.status})`);
  }
  return (await res.json()) as T;
}

export const getFootprint = (input: CarbonInput): Promise<FootprintResponse> =>
  post<FootprintResponse>("/api/footprint", input);

export const simulate = (
  input: CarbonInput,
  selectedActions: string[],
): Promise<ScenarioResult> =>
  post<ScenarioResult>("/api/simulate", { input, selected_actions: selectedActions });

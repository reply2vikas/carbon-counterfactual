import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi, beforeEach } from "vitest";
import { axe } from "vitest-axe";
import App from "./App";
import type { ActionView, FootprintResult } from "./lib/types";

const fp: FootprintResult = {
  total_kg: 5000, breakdown: { transport: 2000, diet: 1900, home: 800, consumption: 300 },
  global_average_kg: 4700, india_average_kg: 1900, target_kg: 2000, vs_target_pct: 150,
};
const acts: ActionView[] = [
  { id: "diet_step", label: "Move one step down the diet ladder", category: "diet",
    annual_savings_kg: 600, effort: 3, cost_inr_year: -6000, abatement_per_effort: 200, cost_per_kg: null },
];

beforeEach(() => {
  const fetchMock = vi.fn((url: string) => {
    const body = url.includes("/actions") ? acts : url.includes("/simulate")
      ? { baseline_total_kg: 5000, projected_total_kg: 4400, reduction_kg: 600, reduction_pct: 12,
          meets_target: false, cumulative_savings_kg: 3000, money_delta_inr_year: -6000,
          applied: [{ id: "diet_step", label: "diet", category: "diet", annual_savings_kg: 600 }] }
      : fp;
    return Promise.resolve({ ok: true, json: () => Promise.resolve(body) }) as unknown as Promise<Response>;
  });
  vi.stubGlobal("fetch", fetchMock);
});

describe("App", () => {
  it("has no axe violations on load", async () => {
    const { container } = render(<App />);
    expect(await axe(container)).toHaveNoViolations();
  });

  it("calculates and shows the footprint", async () => {
    render(<App />);
    await userEvent.click(screen.getByRole("button", { name: /calculate footprint/i }));
    expect(await screen.findByText(/5,000 kg/)).toBeInTheDocument();
  });

  it("simulating an action updates the projection", async () => {
    render(<App />);
    await userEvent.click(screen.getByRole("button", { name: /calculate footprint/i }));
    await userEvent.click(await screen.findByRole("checkbox"));
    expect(await screen.findByText(/simulated future/i)).toBeInTheDocument();
  });
});

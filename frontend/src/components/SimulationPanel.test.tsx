import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { axe } from "vitest-axe";
import { SimulationPanel } from "./SimulationPanel";
import type { SimulationResult } from "../lib/types";

const sim: SimulationResult = {
  baseline_total_kg: 5000,
  projected_total_kg: 4400,
  projected_low_kg: 4340,
  projected_high_kg: 4460,
  reduction_kg: 600,
  reduction_pct: 12,
  meets_target: false,
  cumulative_savings_kg: 3000,
  money_delta_inr_year: -6000,
  applied: [{ id: "diet_step", label: "diet", category: "diet", annual_savings_kg: 600 }],
};

describe("SimulationPanel", () => {
  it("shows the simulated future heading", () => {
    render(<SimulationPanel sim={sim} />);
    expect(screen.getByText(/simulated future/i)).toBeInTheDocument();
  });

  it("has no accessibility violations", async () => {
    const { container } = render(<SimulationPanel sim={sim} />);
    expect(await axe(container)).toHaveNoViolations();
  });
});

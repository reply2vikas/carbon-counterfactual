import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { axe } from "vitest-axe";
import { ResultPanel } from "./ResultPanel";
import type { FootprintResult } from "../lib/types";

const fp: FootprintResult = {
  total_kg: 5000,
  breakdown: { transport: 2000, diet: 1900, home: 800, consumption: 300 },
  global_average_kg: 4700,
  india_average_kg: 1900,
  target_kg: 2000,
  vs_target_pct: 150,
};

describe("ResultPanel", () => {
  it("shows the footprint heading and total", () => {
    render(<ResultPanel result={fp} />);
    expect(screen.getByText(/your footprint/i)).toBeInTheDocument();
    expect(screen.getByText(/5,000 kg/)).toBeInTheDocument();
  });

  it("has no accessibility violations", async () => {
    const { container } = render(<ResultPanel result={fp} />);
    expect(await axe(container)).toHaveNoViolations();
  });
});

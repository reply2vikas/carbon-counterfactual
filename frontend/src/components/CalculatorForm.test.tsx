import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { axe } from "vitest-axe";
import { CalculatorForm } from "./CalculatorForm";
import { DEFAULT_INPUT } from "../lib/types";

describe("CalculatorForm", () => {
  it("renders the baseline fields", () => {
    render(<CalculatorForm value={DEFAULT_INPUT} onChange={() => {}} onSubmit={() => {}} />);
    expect(screen.getByLabelText(/car km \/ week/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/diet/i)).toBeInTheDocument();
  });

  it("calls onSubmit when the button is pressed", async () => {
    const onSubmit = vi.fn();
    render(<CalculatorForm value={DEFAULT_INPUT} onChange={() => {}} onSubmit={onSubmit} />);
    await userEvent.click(screen.getByRole("button", { name: /calculate footprint/i }));
    expect(onSubmit).toHaveBeenCalledOnce();
  });

  it("has no accessibility violations", async () => {
    const { container } = render(
      <CalculatorForm value={DEFAULT_INPUT} onChange={() => {}} onSubmit={() => {}} />,
    );
    expect(await axe(container)).toHaveNoViolations();
  });
});

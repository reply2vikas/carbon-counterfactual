import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { axe } from "vitest-axe";
import { NumberField } from "./NumberField";

describe("NumberField", () => {
  it("renders its label and value", () => {
    render(<NumberField label="Car km / week" value={42} onValueChange={() => {}} />);
    const input = screen.getByLabelText(/car km \/ week/i) as HTMLInputElement;
    expect(input.value).toBe("42");
  });

  it("emits a numeric value on change", async () => {
    const onChange = vi.fn();
    render(<NumberField label="Rail km" value={0} onValueChange={onChange} />);
    await userEvent.type(screen.getByLabelText(/rail km/i), "5");
    expect(onChange).toHaveBeenLastCalledWith(5);
  });

  it("has no accessibility violations", async () => {
    const { container } = render(
      <NumberField label="Flights" value={1} onValueChange={() => {}} />,
    );
    expect(await axe(container)).toHaveNoViolations();
  });
});

import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { axe } from "vitest-axe";
import { ActionList } from "./ActionList";
import type { ActionView } from "../lib/types";

const actions: ActionView[] = [
  {
    id: "diet_step",
    label: "Move one step down the diet ladder",
    category: "diet",
    annual_savings_kg: 600,
    effort: 3,
    cost_inr_year: -6000,
    abatement_per_effort: 200,
    cost_per_kg: null,
  },
];

describe("ActionList", () => {
  it("renders each action as a checkbox", () => {
    render(<ActionList actions={actions} selected={new Set()} onToggle={() => {}} />);
    expect(screen.getByRole("checkbox")).toBeInTheDocument();
  });

  it("calls onToggle with the action id when clicked", async () => {
    const onToggle = vi.fn();
    render(<ActionList actions={actions} selected={new Set()} onToggle={onToggle} />);
    await userEvent.click(screen.getByRole("checkbox"));
    expect(onToggle).toHaveBeenCalledWith("diet_step");
  });

  it("has no accessibility violations", async () => {
    const { container } = render(
      <ActionList actions={actions} selected={new Set()} onToggle={() => {}} />,
    );
    expect(await axe(container)).toHaveNoViolations();
  });
});

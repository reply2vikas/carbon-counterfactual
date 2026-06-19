import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { axe } from "vitest-axe";
import { ActionRanker } from "./ActionRanker";
import type { ActionImpact } from "../lib/types";

const actions: ActionImpact[] = [
  {
    key: "diet_vegetarian",
    label: "Go vegetarian",
    annual_saving_kg: 664,
    effort: 3,
    annual_cost_delta: -6000,
    saving_per_effort: 221,
  },
];

describe("ActionRanker", () => {
  it("renders each action with its saving", () => {
    render(<ActionRanker actions={actions} selected={new Set()} onToggle={() => {}} />);
    expect(screen.getByText("Go vegetarian")).toBeInTheDocument();
    expect(screen.getByText(/664 kg\/yr/)).toBeInTheDocument();
  });

  it("toggles an action when clicked", async () => {
    const onToggle = vi.fn();
    render(<ActionRanker actions={actions} selected={new Set()} onToggle={onToggle} />);
    await userEvent.click(screen.getByRole("checkbox"));
    expect(onToggle).toHaveBeenCalledWith("diet_vegetarian");
  });

  it("reflects selected state via aria-checked", () => {
    render(
      <ActionRanker
        actions={actions}
        selected={new Set(["diet_vegetarian"])}
        onToggle={() => {}}
      />,
    );
    expect(screen.getByRole("checkbox")).toHaveAttribute("aria-checked", "true");
  });

  it("has no detectable accessibility violations", async () => {
    const { container } = render(
      <ActionRanker actions={actions} selected={new Set()} onToggle={() => {}} />,
    );
    expect(await axe(container)).toHaveNoViolations();
  });
});

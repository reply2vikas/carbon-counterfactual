import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { axe } from "vitest-axe";
import App from "./App";

describe("App", () => {
  it("renders the hero and the baseline form", () => {
    render(<App />);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent(
      /footprint you could have/i,
    );
    expect(screen.getByLabelText(/how you mostly travel/i)).toBeInTheDocument();
  });

  it("has no detectable accessibility violations on first paint", async () => {
    const { container } = render(<App />);
    expect(await axe(container)).toHaveNoViolations();
  });
});

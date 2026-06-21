import { describe, expect, it } from "vitest";
import { inr, kg } from "./format";

describe("format helpers", () => {
  it("formats kilograms with rounding and thousands separators", () => {
    expect(kg(1234.6)).toBe("1,235 kg");
    expect(kg(0)).toBe("0 kg");
  });

  it("formats rupees with an explicit sign and /yr suffix", () => {
    expect(inr(-1500)).toBe("-\u20b91,500/yr");
    expect(inr(25000)).toBe("+\u20b925,000/yr");
  });
});

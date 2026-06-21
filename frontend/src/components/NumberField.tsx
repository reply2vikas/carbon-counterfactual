// NumberField — a reusable, accessible numeric input. Centralising the label+input
// pattern here keeps every field consistent and accessible by construction, and
// removes the duplication that otherwise repeats once per numeric field.
import type { ChangeEvent } from "react";

interface Props {
  label: string;
  value: number;
  onValueChange: (value: number) => void;
  min?: number;
}

export function NumberField({ label, value, onValueChange, min = 0 }: Props) {
  return (
    <label>
      {label}
      <input
        type="number"
        min={min}
        value={value}
        onChange={(e: ChangeEvent<HTMLInputElement>) => onValueChange(Number(e.target.value))}
      />
    </label>
  );
}

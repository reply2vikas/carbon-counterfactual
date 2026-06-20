export const kg = (n: number): string => `${Math.round(n).toLocaleString()} kg`;
export const inr = (n: number): string =>
  `${n < 0 ? "-" : "+"}\u20b9${Math.abs(Math.round(n)).toLocaleString()}/yr`;

# Accessibility — WCAG 2.1 AA

**Tools:** `eslint-plugin-jsx-a11y` (lint-time), `vitest-axe` (test-time),
manual keyboard pass.

## Measures
- **Semantic structure**: `main`, `header`, `section` with `aria-labelledby`,
  one `h1`, ordered headings.
- **Labelled controls**: every input/select has an associated `<label htmlFor>`.
- **Live results**: footprint and scenario panels use `aria-live="polite"` so
  screen readers announce updated numbers.
- **Selectable actions**: implemented as `role="checkbox"` with `aria-checked`,
  keyboard-operable.
- **Errors**: surfaced via `role="alert"`.
- **Visible focus**: a 3px focus ring on every interactive element.
- **Contrast**: ink `#14241b` on paper `#f7f5ef` and white exceeds 4.5:1.
- **Reduced motion**: transitions only apply under
  `prefers-reduced-motion: no-preference`.

## Verification
`App.test.tsx` and `ActionRanker.test.tsx` assert `toHaveNoViolations()`. The
jsx-a11y ruleset runs as part of `npm run lint` in CI.

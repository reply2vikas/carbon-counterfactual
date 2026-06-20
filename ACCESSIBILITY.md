# Accessibility — WCAG 2.1 AA

## Automated
- **axe-core** via `vitest-axe`: `src/App.test.tsx` asserts `toHaveNoViolations()`.
- **eslint-plugin-jsx-a11y** (`recommended`) runs in CI with `--max-warnings 0`.

## Built in by construction
- Semantic landmarks: `main`, `section` with `aria-labelledby` headings.
- All inputs have associated `<label>`s; the action checkboxes sit in a `fieldset`
  with a `legend` (visually-hidden `.sr-only`).
- Live regions: results and the simulation panel use `aria-live="polite"`; errors use
  `role="alert"`.
- Visible keyboard focus on every interactive element (`:focus-visible` 3px outline).
- `prefers-reduced-motion` respected — transitions are gated behind the media query.
- Colour palette chosen for ≥4.5:1 text contrast.

## Before submission
Run an axe browser scan + a manual keyboard pass on the live URL and note "0 critical
violations" here with a screenshot.

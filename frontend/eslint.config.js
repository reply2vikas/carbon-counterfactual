import js from "@eslint/js";
import jsxA11y from "eslint-plugin-jsx-a11y";

export default [
  js.configs.recommended,
  {
    files: ["src/**/*.{ts,tsx}"],
    plugins: { "jsx-a11y": jsxA11y },
    rules: {
      // Accessibility rules are enforced, not advisory.
      ...jsxA11y.configs.recommended.rules,
    },
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "module",
      parserOptions: { ecmaFeatures: { jsx: true } },
    },
  },
];

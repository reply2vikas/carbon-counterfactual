# Threat Model (STRIDE)

A one-page security analysis of carbon-counterfactual. The app is stateless, stores no
personal data beyond an anonymous device id, and has no authentication surface, which
keeps the attack surface small.

| STRIDE category | Threat | Mitigation | Evidence |
| --- | --- | --- | --- |
| **Spoofing** | Forged `X-Device-Id` to read another device's history | Device id is opaque/anonymous and grants access only to non-sensitive footprint snapshots; no PII is stored | `app/routes/footprint.py`, `app/repository/` |
| **Tampering** | Malformed/oversized request bodies | Pydantic v2 models with bounded fields + `extra="forbid"` reject bad input with HTTP 422 before logic runs | `app/models.py` |
| **Tampering** | Mutating stored history | Firestore rules make snapshots append-only and shape-validated | `firestore.rules` |
| **Repudiation** | — | Stateless compute; snapshots are immutable once written | `firestore.rules` |
| **Information disclosure** | Secret leakage | Secrets via env / Secret Manager, never committed; only `.env.example` is in git | `app/config.py`, `.gitignore` |
| **Information disclosure** | Verbose errors / sniffing | `X-Content-Type-Options: nosniff`, restrictive CSP, no stack traces returned | `app/main.py` |
| **Denial of service** | Request flooding | Cloud Run autoscaling absorbs load; pure-compute paths are O(1); rate limiting is a documented next step | `PERFORMANCE.md` |
| **Elevation of privilege** | Cross-origin abuse / clickjacking | CORS allow-list, methods limited to GET/POST, `X-Frame-Options: DENY`, CSP `frame-ancestors 'none'` | `app/main.py`, `app/config.py` |
| **LLM-specific** | Prompt injection via user input into the Gemini prompt | Gemini operates only on **deterministic numbers**, never on free-form user text; a rule-based fallback runs if the model is unavailable or returns anything unexpected | `app/insights/gemini.py`, `app/insights/rules.py` |

## Residual risks accepted for the hackathon scope
- No per-user authentication (anonymous, non-sensitive data only).
- Rate limiting deferred to the platform layer (Cloud Run) — application-level
  throttling (e.g. slowapi) is the first hardening step for production.

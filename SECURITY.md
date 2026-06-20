# Security

## Threat model & mitigations
| Threat | Mitigation | Where |
|--------|-----------|-------|
| Malformed / hostile input | Pydantic v2 models with bounded fields + `extra="forbid"` reject bad input with HTTP 422 | `backend/app/models.py` |
| XSS | React escapes output; CSP `default-src 'none'` | `frontend`, `backend/app/main.py` |
| Clickjacking | `X-Frame-Options: DENY`, CSP `frame-ancestors 'none'` | `backend/app/main.py` |
| MIME sniffing | `X-Content-Type-Options: nosniff` | `backend/app/main.py` |
| Cross-origin abuse | CORS restricted to a configured allow-list, methods limited to GET/POST | `backend/app/config.py`, `main.py` |
| Referrer leakage | `Referrer-Policy: no-referrer` | `backend/app/main.py` |
| Vulnerable dependencies | `pip-audit` runs in CI on every push | `.github/workflows/ci.yml` |
| Secret leakage | Config via pydantic-settings / env / Secret Manager; `.env` git-ignored; only `.env.example` committed | `backend/app/config.py`, `.gitignore` |
| Unauthorised data writes | Firestore rules make snapshots append-only and shape-validated | `firestore.rules` |

No secrets are committed. The Gemini key is optional — absent it, the deterministic
rules engine serves insights, so a leaked/empty key never breaks the product.

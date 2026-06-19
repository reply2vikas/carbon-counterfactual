# Security

## Threat model & mitigations
| Threat | Mitigation |
| --- | --- |
| Malformed / hostile payloads | Pydantic v2 schemas with bounded ranges and `extra="forbid"` reject anything unexpected before logic runs |
| XSS | React escapes JSX; CSP `default-src 'none'` |
| Clickjacking | `X-Frame-Options: DENY` + CSP `frame-ancestors 'none'` |
| MIME sniffing | `X-Content-Type-Options: nosniff` |
| Cross-origin abuse | CORS restricted to an explicit origin allowlist, methods limited to GET/POST |
| Referrer leakage | `Referrer-Policy: no-referrer` |
| Secret exposure | No secrets in the repo; read from env / Secret Manager via `pydantic-settings` |
| Vulnerable dependencies | `pip-audit` (backend) and `npm audit` (frontend) run in CI |
| Container privilege | Docker image runs as a non-root `appuser` |
| Tampered history | Firestore rules make snapshots append-only (`update, delete: false`) |

Security headers are applied globally in `app/main.py`; input bounds live in
`app/models.py`; storage rules in `firestore.rules`.

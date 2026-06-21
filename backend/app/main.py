"""FastAPI entry point.

Thin by design: wires restrictive CORS, security-hardening headers, and the API
routers. All domain logic lives in the carbon/ , actions/ and insights/ packages.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from pathlib import Path

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.routes import footprint, health, simulate

settings = get_settings()
app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-Device-Id"],
)


@app.middleware("http")
async def security_headers(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'"
    )
    return response


app.include_router(health.router)
app.include_router(footprint.router)
app.include_router(simulate.router)

# In the container build the compiled SPA is copied to app/static and served
# same-origin (matching the single-container Cloud Run pattern).
_static = Path(__file__).parent / "static"
if _static.is_dir():  # pragma: no cover - only present in the production image
    app.mount("/", StaticFiles(directory=_static, html=True), name="static")

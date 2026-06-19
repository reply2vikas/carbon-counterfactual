"""FastAPI application entry point.

Wires together security middleware (restrictive CORS + hardening headers) and the
API routers. Kept thin: all logic lives in the carbon/ and insights/ packages.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routes import footprint, health, simulate

settings = get_settings()
app = FastAPI(title=settings.app_name, version="1.0.0")

# CORS — restricted to configured origins only.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-Device-Id"],
)

_SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
}


@app.middleware("http")
async def add_security_headers(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    response = await call_next(request)
    for header, value in _SECURITY_HEADERS.items():
        response.headers[header] = value
    return response


app.include_router(health.router)
app.include_router(footprint.router)
app.include_router(simulate.router)

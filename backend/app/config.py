"""Centralised, validated configuration via pydantic-settings.

No secret literals live in the repo; everything is read from the environment
(injected by Cloud Run / Secret Manager in production).
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Carbon Counterfactual"
    cors_origins: str = "http://localhost:5173"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    use_gemini: bool = False

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

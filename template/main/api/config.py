from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings
from litestar.types import Method
from template.main.decoder import decode_env


class APIConfig(BaseSettings):
    NAME: str
    DESCRIPTION: str
    VERSION: str
    DEBUG: bool
    HOST: str
    PORT: int
    SCALAR_VERSION: str
    OPENAPI_PATH: str
    OPENAPI_EXISTS: bool

    CORS_ALLOW_ORIGINS: list[str]
    CORS_ALLOW_HEADERS: list[str]
    CORS_ALLOW_METHODS: list[Method | Literal["*"]]
    CORS_EXPOSE_HEADERS: list[str]
    CORS_MAX_AGE: int

    # SECURE: bool
    # HTTPONLY: bool
    # SAMESITE: Literal["lax", "strict", "none"]
    # MAX_AGE: int


@lru_cache
def load_api_config() -> APIConfig:
    return decode_env(APIConfig)

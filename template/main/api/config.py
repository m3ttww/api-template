from functools import lru_cache
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class APIConfig(BaseSettings):
    NAME: str
    DESCRIPTION: str
    VERSION: str
    DEBUG: bool

    SCALAR_VERSION: str
    OPENAPI_PATH: str
    OPENAPI_EXISTS: bool

    CORS_ALLOW_ORIGINS: list[str]
    CORS_ALLOW_HEADERS: list[str]
    CORS_ALLOW_METHODS: list[str | Literal["*"]]
    CORS_EXPOSE_HEADERS: list[str]
    CORS_MAX_AGE: int

    SESSION_STORE_KEY: str
    SECURE: bool
    HTTPONLY: bool
    SAMESITE: Literal["lax", "strict", "none"]
    MAX_AGE: int


@lru_cache
def load_api_config() -> APIConfig:
    return decode_env(APIConfig)


def decode_env[S: BaseSettings](type_: type[S]) -> S:
    load_dotenv(override=True)
    return type_()

from litestar.config.cors import CORSConfig

from .config import APIConfig


def create_cors(config: APIConfig) -> CORSConfig:
    return CORSConfig(
        allow_credentials=True,
        allow_origins=config.CORS_ALLOW_ORIGINS,
        allow_headers=config.CORS_ALLOW_HEADERS,
        allow_methods=config.CORS_ALLOW_METHODS,
        expose_headers=config.CORS_EXPOSE_HEADERS,
        max_age=config.CORS_MAX_AGE,
    )

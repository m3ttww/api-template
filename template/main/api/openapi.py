from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin

from .config import APIConfig


def create_openapi(config: APIConfig) -> OpenAPIConfig | None:
    return (
        OpenAPIConfig(
            title=config.NAME,
            description=config.DESCRIPTION,
            version=config.VERSION,
            path=config.OPENAPI_PATH,
            render_plugins=[ScalarRenderPlugin(version=config.SCALAR_VERSION)],
        )
        if config.OPENAPI_EXISTS
        else None
    )

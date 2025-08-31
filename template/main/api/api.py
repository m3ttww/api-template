import uvicorn
from dishka import AsyncContainer
from dishka.integrations.litestar import setup_dishka
from litestar import Litestar
from litestar.logging import LoggingConfig

from template.main.api.config import APIConfig, load_api_config
from template.main.api.cors import create_cors
from template.main.api.openapi import create_openapi
from template.main.ios.container import create_container
from template.main.settings import load_settings
from template.presentation.http import create_router


def create_api(container: AsyncContainer, config: APIConfig) -> Litestar:
    logging_config = LoggingConfig(
        root={"level": "INFO", "handlers": ["queue_listener"]},
        formatters={
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        },
        log_exceptions="always",
    )
    app = Litestar(
        path="",
        route_handlers=[create_router()],
        openapi_config=create_openapi(config),
        cors_config=create_cors(config),
        # exception_handlers=exception_map(),
        logging_config=logging_config,
    )

    setup_dishka(container=container, app=app)
    return app


def run_api() -> None:
    settings = load_settings()
    api_config = load_api_config()
    container = create_container(settings)

    api = create_api(container, api_config)

    uvicorn.run(
        api,
        host=api_config.HOST,
        port=api_config.PORT,
        server_header=False,
        log_level=settings.LOG_LEVEL,
    )

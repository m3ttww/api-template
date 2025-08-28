from fastapi import FastAPI
from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
import uvicorn

from template.main.api.config import load_api_config
from template.main.ios.container import create_container
from template.main.settings import Settings, load_settings

def create_api(
    config: Settings, container: AsyncContainer
) -> FastAPI:

    app = FastAPI(
        title="Template API",
        description="Template API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    setup_dishka(container=container, app=app)
    return app


async def run_api() -> None:
    config = load_settings()
    api_config = load_api_config()
    container = create_container(config)

    api = create_api(config, container)

    uvicorn.run(api, host=api_config.HOST, port=api_config.PORT, server_header=False, log_level="info")

from functools import lru_cache

from pydantic_settings import BaseSettings

from template.main.decoder import decode_env


class Settings(BaseSettings):
    POSTGRES_DRIVER: str
    POSTGRES_USER: str
    POSTGRES_PASS: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    POSTGRES_POOL_SIZE: int
    POSTGRES_MAX_OVERFLOW: int

    LOG_LEVEL: str

    def get_postgres_url(self) -> str:
        return f"postgresql+{self.POSTGRES_DRIVER}://{self.POSTGRES_USER}:{self.POSTGRES_PASS}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


@lru_cache
def load_settings() -> Settings:
    return decode_env(Settings)

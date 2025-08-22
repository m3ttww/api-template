from functools import lru_cache
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_DRIVER: str
    POSTGRES_USER: str
    POSTGRES_PASS: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str


    def get_postgres_url(self) -> str:
        return f"postgresql+{self.POSTGRES_DRIVER}://{self.POSTGRES_USER}:{self.POSTGRES_PASS}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


@lru_cache
def load_settings() -> Settings:
    return decode_env(Settings)


def decode_env[S: BaseSettings](type_: type[S]) -> S:
    load_dotenv(override=True)
    return type_()
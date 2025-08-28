from dotenv import load_dotenv
from pydantic_settings import BaseSettings


def decode_env[S: BaseSettings](type_: type[S]) -> S:
    load_dotenv(override=True)
    return type_()

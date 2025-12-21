from litestar.exceptions import InternalServerException
from litestar.types import ExceptionHandlersMap

from template.presentation.http.v1.exceptions.handlers import (
    general_exception_handler,
    internal_server_exception_handler,
)


def exception_mapper() -> ExceptionHandlersMap:
    return {
        InternalServerException: internal_server_exception_handler,
        Exception: general_exception_handler,
    }

from litestar.types import ExceptionHandlersMap

from template.presentation.http.v1.exceptions.handlers import (
    general_exception_handler,
)


def exception_mapper() -> ExceptionHandlersMap:
    return {
        Exception: general_exception_handler,
    }

import logging

from litestar import MediaType, Request, Response
from litestar.exceptions import InternalServerException
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from uuid_utils.compat import uuid4

logger = logging.getLogger(__name__)


def internal_server_exception_handler(
    request: Request, exc: InternalServerException
) -> Response:
    ticket = str(uuid4())
    status_code = getattr(exc, "status_code", InternalServerException.status_code)

    logger.error(
        f"[TICKET:{ticket}] Internal server exception: {str(exc)}",
        extra={
            "ticket": ticket,
            "path": request.url.path,
            "method": request.method,
        }
    )

    content = {
        "ticket": ticket,
        "error": f"{type(exc).__name__}: {str(exc)}",
        "path": request.url.path,
        "method": request.method,
    }

    return Response(
        media_type=MediaType.JSON,
        content=content,
        status_code=status_code,
    )


def general_exception_handler(request: Request, exc: Exception) -> Response:
    ticket = str(uuid4())

    logger.error(
        f"[TICKET:{ticket}] Unhandled exception: {str(exc)}",
        extra={
            "ticket": ticket,
            "path": request.url.path,
            "method": request.method,
        }
    )

    content = {
        "ticket": ticket,
        "error": f"{type(exc).__name__}: {str(exc)}",
        "path": request.url.path,
        "method": request.method,
    }

    return Response(
        media_type=MediaType.JSON,
        content=content,
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )

import logging

from litestar import MediaType, Request, Response
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from uuid_utils.compat import uuid4

from template.domain.errors import PublicError

logger = logging.getLogger(__name__)


def general_exception_handler(
    request: Request,
    exc: Exception,
    status_code: int | None = None,
) -> Response:
    ticket = str(uuid4())
    status_code = status_code or getattr(
        exc, "status_code", HTTP_500_INTERNAL_SERVER_ERROR
    )

    logger.error(
        f"[TICKET:{ticket}] exception: {str(exc)}",
        extra={
            "ticket": ticket,
            "path": request.url.path,
            "method": request.method,
        },
    )

    message = "An internal error occurred"
    if isinstance(exc, PublicError):
        message = str(exc.message)

    content = {
        "ticket": ticket,
        "error": f"{type(exc).__name__}",
        "message": message,
    }

    return Response(
        media_type=MediaType.JSON,
        content=content,
        status_code=status_code,
    )

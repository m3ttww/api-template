from typing import Any

from template.domain.errors import InternalError, PublicError


class ApplicationError(Exception): ...


class PublicDetailedError(ApplicationError, PublicError):
    def __init__(
        self,
        message: str,
        status_code: int,
        notes: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.notes = notes

    def __str__(self) -> str:
        return self.message


class InternalDetailedError(ApplicationError, InternalError):
    def __init__(
        self,
        message: str,
        status_code: int,
        notes: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.notes = notes


class NotFoundError(PublicDetailedError): ...


class UnauthorizedError(PublicDetailedError): ...


class ForbiddenError(PublicDetailedError): ...


class InternalServerError(PublicDetailedError): ...


class BadRequestError(PublicDetailedError): ...


class BalanceTooLowError(PublicDetailedError): ...


class ConflictError(PublicDetailedError): ...

from typing import Any


class ApplicationError(Exception): ...


class DetailedError(ApplicationError):
    def __init__(
        self,
        message: str,
        status_code: int,
        notes: dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.notes = notes

    def __str__(self) -> str:
        return self.message


class NotFoundError(DetailedError): ...


class UnauthorizedError(DetailedError): ...


class ForbiddenError(DetailedError): ...


class InternalServerError(DetailedError): ...


class BadRequestError(DetailedError): ...


class BalanceTooLowError(DetailedError): ...


class ConflictError(DetailedError): ...

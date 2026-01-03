class BaseError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class PublicError(BaseError): ...


class InternalError(BaseError): ...


class ValidationError(PublicError): ...

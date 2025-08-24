from __future__ import annotations

import re
from typing import Final

from template.domain.entities.base import Entity, entity

MIN_LOGIN_LENGTH: Final[int] = 6
MAX_LOGIN_LENGTH: Final[int] = 32

MIN_PASSWORD_LENGTH: Final[int] = 8
MAX_PASSWORD_LENGTH: Final[int] = 20
SECURE_REGEX: Final[re.Pattern[str]] = re.compile(
    r"^(?=.*[A-Z])(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>?])(?=.*[0-9])(?=.*[a-z]).*$"
)


@entity
class User(Entity):
    login: str
    password_hash: str

    def __post_init__(self) -> None:
        self._validate_login(self.login)

    def _validate_login(self, login: str) -> None:
        if not login:
            raise ValueError("Login is required")
        if len(login) < MIN_LOGIN_LENGTH:
            raise ValueError(
                f"Login must be at least {MIN_LOGIN_LENGTH} characters long"
            )
        if len(login) > MAX_LOGIN_LENGTH:
            raise ValueError(
                f"Login must be less than {MAX_LOGIN_LENGTH} characters long"
            )
        if not login.isalnum():
            raise ValueError("Login must be alphanumeric")

    def validate_plain_password(self, password: str) -> None:
        if len(password) < MIN_PASSWORD_LENGTH:
            raise ValueError(f"must be at least {MIN_PASSWORD_LENGTH} characters long.")
        if len(password) > MAX_PASSWORD_LENGTH:
            raise ValueError(f"must be at most {MAX_PASSWORD_LENGTH} characters long.")
        if re.match(SECURE_REGEX, password) is None:
            raise ValueError(
                "must contain at least one uppercase letter, one"
                "lowercase letter, one number, and one special character.",
            )

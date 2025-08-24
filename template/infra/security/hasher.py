from dataclasses import asdict
from typing import Literal

from argon2 import Parameters, PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError
from argon2.profiles import (
    CHEAPEST,
    PRE_21_2,
    RFC_9106_HIGH_MEMORY,
    RFC_9106_LOW_MEMORY,
)

from template.app.interfaces.security.hasher import Hasher

ProfileType = Literal[
    "RFC_9106_LOW_MEMORY", "RFC_9106_HIGH_MEMORY", "CHEAPEST", "PRE_21_2", "DEFAULT"
]
PROFILES: dict[str, Parameters] = {
    "RFC_9106_LOW_MEMORY": RFC_9106_LOW_MEMORY,
    "RFC_9106_HIGH_MEMORY": RFC_9106_HIGH_MEMORY,
    "CHEAPEST": CHEAPEST,
    "PRE_21_2": PRE_21_2,
}


class Argon2(Hasher):
    __slots__ = ("_hasher",)

    def __init__(self, hasher: PasswordHasher) -> None:
        self._hasher = hasher

    def hash(self, data: str) -> str:
        return self._hasher.hash(data)

    def verify(self, data: str, hash_: str) -> bool:
        try:
            return self._hasher.verify(hash_, data)
        except (VerificationError, VerifyMismatchError):
            return False


def get_argon2_hasher(profile: ProfileType = "DEFAULT") -> Argon2:
    kw = {} if profile == "DEFAULT" else asdict(PROFILES[profile])
    return Argon2(PasswordHasher(**kw))

from typing import Any, Self

from msgspec import Struct, convert, to_builtins


class DTO(Struct):
    def asdict(self) -> dict[str, Any]:
        return to_builtins(self, str_keys=True)  # type: ignore[no-any-return]

    @classmethod
    def from_(cls, entity: Struct | object) -> Self:
        return convert(entity, type=cls, from_attributes=True)

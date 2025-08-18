from typing import Any

from msgspec import Struct, to_builtins


class DTO(Struct):
    def asdict(self) -> dict[str, Any]:
        return to_builtins(self, str_keys=True)

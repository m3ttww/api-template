from dataclasses import dataclass
from typing import Any

from msgspec import to_builtins


@dataclass(slots=True)
class Entity:
    def asdict(self) -> dict[str, Any]:
        return to_builtins(self, str_keys=True)  # type: ignore[no-any-return]

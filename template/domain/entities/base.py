from dataclasses import dataclass
import uuid_utils.compat as uuid
from typing import Any

from msgspec import to_builtins

IDType = uuid.UUID

@dataclass(slots=True)
class Entity:
    def asdict(self) -> dict[str, Any]:
        return to_builtins(self, str_keys=True)  # type: ignore[no-any-return]

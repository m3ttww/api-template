from __future__ import annotations

from dataclasses import dataclass
from typing import Any, dataclass_transform

import uuid_utils.compat as uuid
from msgspec import to_builtins

IDType = uuid.UUID


@dataclass_transform()
def entity[E](cls: type[E]) -> type[E]:
    return dataclass(slots=True)(cls)


@entity
class Entity:
    id: IDType

    def asdict(self) -> dict[str, Any]:
        return to_builtins(self, str_keys=True)  # type: ignore[no-any-return]

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any, dataclass_transform

import uuid_utils.compat as uuid

IDType = uuid.UUID


@dataclass_transform()
def entity[E](cls: type[E]) -> type[E]:
    return dataclass()(cls)


@entity
class Entity:
    id: IDType

    def asdict(self) -> dict[str, Any]:
        return {f.name: getattr(self, f.name) for f in fields(self)}

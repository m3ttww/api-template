from __future__ import annotations

from abc import ABCMeta
from typing import TYPE_CHECKING, Any, ClassVar, final


@final
class SingletonMeta(ABCMeta):
    _instances: ClassVar[dict[type[SingletonMeta], SingletonMeta]] = {}

    # prevent type checkers from analyzing `__call__` and replacing class's `__init__` signature
    # related: https://github.com/microsoft/pyright/issues/5488
    if not TYPE_CHECKING:

        def __call__(cls: SingletonMeta, *args: Any, **kwargs: Any) -> SingletonMeta:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
            return cls._instances[cls]

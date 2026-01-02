from dataclasses import dataclass
from typing import Any, dataclass_transform

from .base import Command, Interactor

_COMMAND_TO_INTERACTOR: dict[type[Command], type[Interactor[Any, Any]]] = {}


@dataclass_transform()
def interactor[T: Interactor[Any, Any]](cls: type[T]) -> type[T]:
    cls = dataclass(slots=True, frozen=True, eq=False, match_args=False)(cls)
    _COMMAND_TO_INTERACTOR[cls.command_cls] = cls
    return cls


def get_defined_interactors() -> dict[type[Command], type[Interactor[Any, Any]]]:
    return _COMMAND_TO_INTERACTOR

from dataclasses import dataclass
from typing import Any, dataclass_transform

from .base import Form, Interactor

_FORM_TO_INTERACTOR: dict[type[Form], type[Interactor[Any, Any]]] = {}


@dataclass_transform()
def interactor[T: Interactor[Any, Any]](cls: type[T]) -> type[T]:
    cls = dataclass(slots=True, frozen=True, eq=False, match_args=False)(cls)
    _FORM_TO_INTERACTOR[cls.form_cls] = cls
    return cls


def get_defined_interactors() -> dict[type[Form], type[Interactor[Any, Any]]]:
    return _FORM_TO_INTERACTOR

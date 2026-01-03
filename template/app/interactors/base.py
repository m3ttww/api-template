from abc import abstractmethod
from typing import ClassVar, Protocol, get_args

from template.domain.entities.base import Entity
from template.internal.tools.dto import DTO


class Form(DTO): ...


class Interactor[F: Form, R: DTO | Entity | None](Protocol):
    form_cls: ClassVar[type[Form]]

    def __init_subclass__(cls, /) -> None:
        cls.form_cls = get_args(cls.__orig_bases__[-1])[0]  # type: ignore[attr-defined]

    async def __call__(self, form: F) -> R:
        return await self._execute(form)

    @abstractmethod
    async def _execute(self, form: F, /) -> R:
        raise NotImplementedError

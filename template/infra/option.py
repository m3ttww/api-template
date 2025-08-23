from dataclasses import dataclass

from template.app.interfaces.option import Option as BaseOption


@dataclass(slots=True)
class Option[T](BaseOption[T]):
    value: T | None

    def some(self, exc: Exception) -> T:
        if self.value is None:
            raise exc
        return self.value

    def none(self, exc: Exception) -> None:
        if self.value is not None:
            raise exc

    def some_or[R](self, default: R) -> T | R:
        if self.value is None:
            return default
        return self.value

from abc import abstractmethod
from types import TracebackType
from typing import Protocol, Self


class TransactionManager(Protocol):
    __slots__ = ()

    @abstractmethod
    async def create_transaction(self) -> None: ...

    @abstractmethod
    async def close_transaction(self) -> None: ...

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...

    @abstractmethod
    async def is_in_transaction(self) -> bool: ...

    @abstractmethod
    async def flush(self) -> None: ...


    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if await self.is_in_transaction():
            if exc_type:
                await self.rollback()
            else:
                await self.commit()

        await self.close_transaction()

    async def __aenter__(self) -> Self:
        await self.create_transaction()
        return self
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from template.app.errors import InternalServerError
from template.app.interfaces.repos.transaction_manager import TransactionManager


class TransactionManagerImpl(TransactionManager):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self) -> None:
        try:
            await self.session.commit()
        except SQLAlchemyError as err:
            raise InternalServerError(
                "Failed to commit transaction",
                500,
            ) from err

    async def rollback(self) -> None:
        try:
            await self.session.rollback()
        except SQLAlchemyError as err:
            raise InternalServerError(
                "Failed to rollback transaction",
                500,
            ) from err

    async def is_in_transaction(self) -> bool:
        return self.session.is_active and self.session.in_transaction()

    async def create_transaction(self) -> None:
        if not await self.is_in_transaction():
            await self.session.begin()

    async def close_transaction(self) -> None:
        if await self.is_in_transaction():
            await self.session.close()

    async def flush(self) -> None:
        await self.session.flush()

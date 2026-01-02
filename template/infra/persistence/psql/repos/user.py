from sqlalchemy import select

from template.app.interfaces.option import Option
from template.domain.entities.user import User
from template.infra.option import Option as OptionImpl
from template.infra.persistence.psql.repos.crud import CRUDRepoImpl
from template.infra.persistence.psql.tables import user_table
from template.app.interfaces.repos.user import UserRepo


class UserRepoImpl(UserRepo, CRUDRepoImpl[User]):
    async def get_by_login(self, login: str) -> Option[User]:
        stmt = select(User).where(user_table.c.login == login)
        result = await self._session.execute(stmt)
        return OptionImpl(result.scalar_one_or_none())

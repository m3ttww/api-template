from template.domain.entities.user import User
from template.infra.persistence.psql.repos.crud import CRUDRepoImpl
from template.app.interfaces.repos.user import UserRepo

class UserRepoImpl(UserRepo, CRUDRepoImpl[User]):
    pass
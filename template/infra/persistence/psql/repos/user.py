from template.domain.entities.user import User
from template.infra.persistence.psql.repos.crud import CRUDRepoImpl


class UserRepo(CRUDRepoImpl[User]):
    pass
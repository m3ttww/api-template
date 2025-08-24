from template.app.interfaces.repos.crud import CRUDRepo
from template.domain.entities.user import User


class UserRepo(CRUDRepo[User]):
    pass

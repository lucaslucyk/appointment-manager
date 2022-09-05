from app.crud.base import CRUDBase
from app.models import User
from app.schemas.users import UserCreate

class CRUDUser(CRUDBase[User, UserCreate]):
    pass


user = CRUDUser(User)
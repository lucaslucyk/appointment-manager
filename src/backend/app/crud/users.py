from app.crud.base import CRUDBase
from app.models import User
from app.schemas.users import UserCreate, UserUpdate

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    pass


user = CRUDUser(User)
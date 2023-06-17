from app.crud.base import CRUDBase
from app.models.user import User  # noqa
from app.schemas.user import UserCreate, UserInDBBase, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    pass


users = CRUDUser(User, UserInDBBase)

from app.crud.base import CRUDBase
from app.models.user import User  # noqa
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """
    Class for CRUD operations on the User model.

    Attributes:
        model (Type[User]): The User SQLAlchemy model.

    """


users = CRUDUser(User)

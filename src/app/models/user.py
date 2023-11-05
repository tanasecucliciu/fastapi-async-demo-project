from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    """
    SQLAlchemy model for the User table.

    Attributes:
        id (Mapped[int]): The ID column for the User table.
        email (Mapped[str]): The email column for the User table.

    """

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    email: Mapped[str] = mapped_column("email", String(length=64), nullable=False)

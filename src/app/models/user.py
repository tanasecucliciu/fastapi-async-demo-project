from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    email: Mapped[str] = mapped_column("title", String(length=64), nullable=False)

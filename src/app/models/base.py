import datetime
import json
from typing import Any, Dict

from sqlalchemy import MetaData, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    __abstract__ = True
    __name__: str

    metadata = MetaData(naming_convention=convention)

    created_at: Mapped[datetime.datetime] = mapped_column(
        "created_at", server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        "updated_at", server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def dict(self) -> Dict[str, Any]:
        return {
            k: v.isoformat() if isinstance(v, datetime.datetime) else v
            for k, v in self.__dict__.items()
            if not k.startswith("_")
        }

    def __repr__(self) -> str:
        return json.dumps(self.dict())

    # Generate __tablename__ automatically
    # pylint: disable=no-self-argument
    @declared_attr  # noqa: E301
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

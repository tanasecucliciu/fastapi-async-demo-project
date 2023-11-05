from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class UserBase(BaseModel):
    """
    Base Pydantic model for user properties.

    """

    email: Optional[str] = None


# Properties to receive on aspect creation
class UserCreate(UserBase):
    """
    Pydantic model for creating a user.

    """

    email: str


# Properties to receive on aspect update
class UserUpdate(UserBase):
    """
    Pydantic model for updating a user.

    """


# Properties shared by models stored in DB
class UserInDB(UserBase):
    """
    Pydantic model representing user stored in the database.

    """

    id: int
    email: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class User(UserInDB):
    """
    Pydantic model for returning user properties to the client.

    """

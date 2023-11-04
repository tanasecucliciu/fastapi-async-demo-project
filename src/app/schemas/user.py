from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class UserBase(BaseModel):
    email: Optional[str] = None


# Properties to receive on aspect creation
class UserCreate(UserBase):
    email: str


# Properties to receive on aspect update
class UserUpdate(UserBase):
    pass


# Properties shared by models stored in DB
class UserInDB(UserBase):
    id: int
    email: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class User(UserInDB):
    pass

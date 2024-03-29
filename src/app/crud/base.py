from typing import Any, AsyncGenerator, Dict, Generic, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for CRUD operations on a SQLAlchemy model.

    Attributes:
        model (Type[ModelType]): The SQLAlchemy model.

    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def _get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """
        Get a single object by ID without managing the database session.

        This method executes a direct query to retrieve an object, assuming the session management is handled by the caller.
        It is designed to be used internally by other methods like `get`, update` or `delete` that manage the session themselves.

        Args:
            db (AsyncSession): The asynchronous SQLAlchemy session.
            id (Any): The ID of the object to retrieve.

        Returns:
            Optional[ModelType]: The retrieved object, or None if it does not exist.
        """
        stmt = select(self.model).where(self.model.id == id)
        return await db.scalar(stmt.order_by(self.model.id))

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """
        Get a single object by ID, managing the session automatically.

        Args:
            db (AsyncSession): The asynchronous SQLAlchemy session.
            id (Any): The ID of the object to retrieve.

        Returns:
            Optional[ModelType]: The retrieved object, or None if it does not exist.
        """
        response = None
        async with db:
            response = await self._get(db=db, id=id)
        return response

    async def _get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> AsyncGenerator[ModelType, None]:
        """
        Stream objects from the database in an asynchronous manner.

        This method streams database objects directly, intended for use with external session management.

        Args:
            db (AsyncSession): The asynchronous SQLAlchemy session.
            skip (int): The number of objects to skip before starting to retrieve (offset).
            limit (int): The maximum number of objects to retrieve (batch size).

        Yields:
            AsyncGenerator[ModelType, None]: An asynchronous generator of the retrieved objects.
        """
        stmt = select(self.model).order_by(self.model.id).offset(skip).limit(limit)
        stream = await db.stream_scalars(stmt.order_by(self.model.id))
        async for row in stream:
            yield row

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> Any:
        """
        Retrieve a list of objects from the database within a managed session.

        Args:
            db (AsyncSession): The asynchronous SQLAlchemy session.
            skip (int): The number of objects to skip before starting to retrieve (offset).
            limit (int): The maximum number of objects to retrieve (batch size).

        Returns:
            List[ModelType]: A list of the retrieved objects.
        """
        response = []
        async with db:
            async for db_obj in self._get_multi(db, skip=skip, limit=limit):
                response.append(db_obj)
        return response

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new object in the database.

        Args:
            db (AsyncSession): The asynchronous SQLAlchemy session.
            obj_in (CreateSchemaType): The object to create.

        Returns:
            ModelType: The created object.

        """
        db_obj = None
        async with db.begin():
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)
            db.add(db_obj)
            await db.flush()
            # Expunge the object to decouple it from the session for independent use.
            db.expunge(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        id: Any,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> Optional[ModelType]:
        """
        Update an object in the database.

        Args:
            db (AsyncSession): The asynchronous SQLAlchemy session.
            id (Any): The ID of the object to update.
            obj_in (Union[UpdateSchemaType, Dict[str, Any]]): The updated object.

        Returns:
            Optional[ModelType]: The updated object, or None if it does not exist.

        """
        db_obj = None
        async with db.begin():
            db_obj = await self._get(db, id)
            # Check if exists
            if db_obj:
                obj_data = jsonable_encoder(db_obj)
                if isinstance(obj_in, dict):
                    update_data = obj_in
                else:
                    update_data = obj_in.dict(exclude_unset=True)
                # Update the object
                for field in obj_data:
                    if field in update_data:
                        setattr(db_obj, field, update_data[field])
                await db.flush()
                await db.refresh(db_obj)
                # Expunge the object to decouple it from the session for independent use.
                db.expunge(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: str) -> Optional[ModelType]:
        """
        Remove an object from the database.

        Args:
            db (AsyncSession): The asynchronous SQLAlchemy session.
            id (str): The ID of the object to remove.

        Returns:
            Optional[ModelType]: The removed object, or None if it does not exist.

        """
        db_obj = None
        async with db.begin():
            db_obj = await self._get(db, id)
            if db_obj:
                await db.delete(db_obj)
                await db.flush()
                # Expunge the object to decouple it from the session for independent use.
                db.expunge(db_obj)
        return db_obj

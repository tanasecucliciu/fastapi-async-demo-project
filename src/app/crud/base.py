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
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def _get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id)
        return await db.scalar(stmt.order_by(self.model.id))

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        response = None
        async with db:
            response = await self._get(db=db, id=id)
        return response

    async def _get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> AsyncGenerator[ModelType, None]:
        stmt = select(self.model).order_by(self.model.id).offset(skip).limit(limit)
        stream = await db.stream_scalars(stmt.order_by(self.model.id))
        async for row in stream:
            yield row

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> Any:
        response = []
        async with db:
            async for db_obj in self._get_multi(db, skip=skip, limit=limit):
                response.append(db_obj)
        return response

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
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
                for field in obj_data:
                    if field in update_data:
                        setattr(db_obj, field, update_data[field])
                await db.flush()
                await db.refresh(db_obj)
                # Expunge the object to decouple it from the session for independent use.
                db.expunge(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: str) -> Optional[ModelType]:
        db_obj = None
        async with db.begin():
            db_obj = await self._get(db, id)
            if db_obj:
                await db.delete(db_obj)
                await db.flush()
                # Expunge the object to decouple it from the session for independent use.
                db.expunge(db_obj)
        return db_obj

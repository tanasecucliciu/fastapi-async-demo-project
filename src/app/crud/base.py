from typing import Any, AsyncGenerator, Dict, Generic, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base
from app.util.exceptions import EntryNotFoundException

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], schema: Type[CreateSchemaType]):
        self.model = model
        self.schema = schema

    async def _get(self, session: AsyncSession, id: Any) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id)
        return await session.scalar(stmt.order_by(self.model.id))

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        response = None
        async with db() as session:
            response = await self._get(session=session, id=id)
        return self.schema.from_orm(response)

    async def _get_multi(
        self, session: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> AsyncGenerator[ModelType, None]:
        stmt = select(self.model)
        stream = await session.stream_scalars(stmt.order_by(self.model.id))
        async for row in stream:
            yield row

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> Any:
        response = []
        async with db() as session:
            async for db_obj in self._get_multi(session, skip=skip, limit=limit):
                response.append(db_obj)
        return response

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        response = None
        async with db.begin() as session:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)
            session.add(db_obj)
            await session.flush()
            response = self.schema.from_orm(db_obj)
        return response

    async def update(
        self,
        db: AsyncSession,
        *,
        id: Any,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        response = None
        async with db.begin() as session:
            db_obj = await self._get(session, id)
            # Check if exist otherwise inform user somehow.
            if not db_obj:
                raise EntryNotFoundException(id, self.model.__tablename__)
            obj_data = jsonable_encoder(db_obj)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            await session.flush()
            await session.refresh(db_obj)
            response = self.schema.from_orm(db_obj)
        return response

    async def remove(self, db: AsyncSession, *, id: str) -> ModelType:
        response = None
        async with db.begin() as session:
            db_obj = await self._get(session, id)
            if not db_obj:
                raise EntryNotFoundException(id, self.model.__tablename__)
            response = self.schema.from_orm(db_obj)
            await session.delete(db_obj)
            await session.flush()
        return response

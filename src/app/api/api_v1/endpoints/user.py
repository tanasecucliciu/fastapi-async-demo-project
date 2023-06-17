import json
from typing import Any

import aioredis
from fastapi import APIRouter, Depends, HTTPException

from app import crud, schemas
from app.api import deps
from app.core.config import settings
from app.util.exceptions import EntryNotFoundException

router = APIRouter()


@router.get("/", response_model=Any)
async def read_users(
    db: deps.AsyncSession,
    redis: aioredis.Redis = Depends(deps.get_redis),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users.
    """
    users = []
    item_id = f"user_list_{skip}:{limit}"
    users_bytes = await redis.get(item_id)
    if users_bytes is not None:
        users = json.loads(users_bytes.decode('utf-8'))
        return users

    users = await crud.users.get_multi(db, skip=skip, limit=limit)
    if users:
        # Store user in cache and set expiration time
        await redis.set(
            item_id, json.dumps([a.dict() for a in users]), ex=settings.REDIS_TTL
        )
    return users


@router.post("/", response_model=schemas.User)
async def create_user(*, db: deps.AsyncSession, obj_in: schemas.UserCreate) -> Any:
    """
    Create new user.
    """
    user = await crud.users.create(db=db, obj_in=obj_in)
    if not user:
        raise HTTPException(status_code=500, detail="Couldn't create User.")
    return user


@router.put("/{id}", response_model=schemas.User)
async def update_user(
    *, db: deps.AsyncSession, id: int, obj_in: schemas.UserUpdate
) -> Any:
    """
    Update an user.
    """
    user = None
    try:
        user = await crud.users.update(db=db, id=id, obj_in=obj_in)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    return user


@router.get("/{id}", response_model=schemas.User)
async def read_user(
    *,
    db: deps.AsyncSession,
    redis: aioredis.Redis = Depends(deps.get_redis),
    id: int,
) -> Any:
    """
    Get user by ID.
    """
    item_id = f"user_get_{id}"
    user = await redis.get(item_id)
    if user:
        return json.loads(user.decode('utf-8'))
    user = await crud.users.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Store user in cache and set expiration time
    await redis.set(item_id, json.dumps(user.dict()), ex=settings.REDIS_TTL)
    return user


@router.delete("/{id}", response_model=schemas.User)
async def delete_user(*, db: deps.AsyncSession, id: int) -> Any:
    """
    Delete an user.
    """
    user = None
    try:
        user = await crud.users.remove(db=db, id=id)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    return user

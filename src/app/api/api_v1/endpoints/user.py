import json
from typing import Any, List

from fastapi import APIRouter, HTTPException

from app import crud, schemas
from app.api import deps
from app.core.config import settings
from app.util.api import invalidate_cache

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
async def read_users(
    db: deps.async_session,
    redis: deps.redis_async_session,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users.
    """
    users = []
    tag = "user_list"
    item_id = f"{tag}_{skip}:{limit}"
    users_bytes = await redis.get(item_id)
    if users_bytes is not None:
        users = json.loads(users_bytes.decode("utf-8"))
        return users

    users = await crud.users.get_multi(db, skip=skip, limit=limit)
    if users:
        # Store user in cache and set expiration time
        await redis.set(
            item_id, json.dumps([u.dict() for u in users]), ex=settings.REDIS_TTL
        )
        await redis.sadd(tag, item_id)  # Tag the item for invalidation
    return users


@router.post("/", response_model=schemas.User)
async def create_user(
    *,
    db: deps.async_session,
    redis: deps.redis_async_session,
    obj_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    invalidate_tags = ["user_list"]
    user = await crud.users.create(db=db, obj_in=obj_in)
    if not user:
        raise HTTPException(status_code=500, detail="Couldn't create User.")
    # Invalidate cache
    await invalidate_cache(redis, invalidate_tags)
    return user


@router.put("/{id}", response_model=schemas.User)
async def update_user(
    *,
    db: deps.async_session,
    id: int,
    redis: deps.redis_async_session,
    obj_in: schemas.UserUpdate,
) -> Any:
    """
    Update an user.
    """
    invalidate_tags = ["user_list", "user_get"]
    user = await crud.users.update(db=db, id=id, obj_in=obj_in)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Invalidate cache
    await invalidate_cache(redis, invalidate_tags)
    return user


@router.get("/{id}", response_model=schemas.User)
async def read_user(
    *,
    db: deps.async_session,
    redis: deps.redis_async_session,
    id: int,
) -> Any:
    """
    Get user by ID.
    """
    tag = "user_get"
    item_id = f"{tag}_{id}"
    user = await redis.get(item_id)
    if user:
        return json.loads(user.decode("utf-8"))
    user = await crud.users.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Store user in cache and set expiration time
    await redis.set(item_id, json.dumps(user.dict()), ex=settings.REDIS_TTL)
    await redis.sadd(tag, item_id)  # Tag the item for invalidation
    return user


@router.delete("/{id}", response_model=schemas.User)
async def delete_user(
    *, db: deps.async_session, redis: deps.redis_async_session, id: int
) -> Any:
    """
    Delete an user.
    """
    invalidate_tags = ["user_list", "user_get"]
    user = await crud.users.remove(db=db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Invalidate cache
    await invalidate_cache(redis, invalidate_tags)
    return user

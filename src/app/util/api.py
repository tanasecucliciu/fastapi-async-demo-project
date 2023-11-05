from typing import List

from redis import asyncio as aioredis


async def invalidate_cache(redis: aioredis.Redis, tags: List[str]) -> None:  # type: ignore
    """
    Invalidate the cache for the given tags.

    Args:
        redis (aioredis.Redis): The Redis client.
        tags (List[str]): The list of tags to invalidate.

    Returns:
        None

    """
    for tag in tags:
        cache_keys = await redis.smembers(tag)
        if cache_keys:
            await redis.delete(*cache_keys)
        await redis.delete(tag)

from typing import List

from redis import asyncio as aioredis


async def invalidate_cache(redis: aioredis.Redis, tags: List[str]) -> None:  # type: ignore
    for tag in tags:
        cache_keys = await redis.smembers(tag)
        if cache_keys:
            await redis.delete(*cache_keys)
        await redis.delete(tag)

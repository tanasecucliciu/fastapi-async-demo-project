from typing import Callable, Coroutine, Tuple

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.db.session import async_session_factory, get_redis_session

router = APIRouter()


async def test_db_connection() -> Tuple[bool, str]:
    try:
        db = async_session_factory()
        async with db:
            # Try to create session to check if DB is awake
            db.execute("SELECT 1")
    except Exception as e:
        response = f"Unable to connect to the database. Error: {e}"
        print(response)
    finally:
        await db.close()

    return (True, "Database connection OK")


async def test_redis_connection() -> Tuple[bool, str]:
    pong = None
    try:
        redis = await get_redis_session()
        pong = await redis.ping()
    except Exception as e:
        error_msg = f"Unable to connect to Redis. Error: {e}"
        print(error_msg)
    finally:
        await redis.aclose()

    response = (
        (True, "Redis connection OK") if pong else (False, "Redis connection failed")
    )

    return response


HEALTH_TESTS = [test_db_connection, test_redis_connection]


async def _get_health(
    health_tests: list[Callable[[], Coroutine[None, None, Tuple[bool, str]]]],
    verbose: bool = False,
) -> JSONResponse:
    # Is the service healthy/ready
    status_code = 200
    status = "Service is ready."
    details = ""
    for test in health_tests:
        healthy, detail = await test()
        if verbose:
            details += f"{detail}\n"

        if not healthy:
            status_code = 500
            status = "Service is not ready."
            break

    response = {"status": status}
    if details:
        response["details"] = details
    return JSONResponse(jsonable_encoder(response), status_code=status_code)


@router.get("/_alive")
def get_alive() -> JSONResponse:
    # Is the service alive
    response = {"status": "Service is alive."}
    return JSONResponse(jsonable_encoder(response), status_code=200)


@router.get("/_health")
async def get_health() -> JSONResponse:
    return await _get_health(HEALTH_TESTS)


@router.get("/health-details")
async def get_health_details() -> JSONResponse:
    # Gives details on why service isn't ready/healthy
    return await _get_health(HEALTH_TESTS, verbose=True)

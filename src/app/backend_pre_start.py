import logging

from sqlalchemy.sql import text
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core.config import settings
from app.db.session import sync_session_factory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        logger.info(f"Establishing connection to {settings.DB_URI}")
        session = sync_session_factory()
        # Try to create session to check if DB is awake.
        session.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(e)
        raise e
    finally:
        session.close()


def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()

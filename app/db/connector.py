
# engine = create_engine("sqlite:///db.sqlite3")
"""
    sqlite:///:memory: (or, sqlite://)
    sqlite:///relative/path/to/file.db
    sqlite:////absolute/path/to/file.db
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.utils.logging import AppLogger
from sqlalchemy.ext.asyncio import AsyncSession


from app.config.setting import settings as global_settings


logger = AppLogger().get_logger()

engine = create_async_engine(
    global_settings.asyncmysql_url.unicode_string(),
    future=True,
    echo=True,
)

# expire_on_commit=False will prevent attributes from being expired
# after commit.
session_factory = async_sessionmaker(
    engine,
    # autoflush=False,
    expire_on_commit=False,
)


# Dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        logger.debug(f"ASYNC Pool: {engine.pool.status()}")
        yield session

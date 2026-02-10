import logging
from typing import AsyncIterator

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from infrastructure.db.settings import DatabaseSettings

logger = logging.getLogger(__name__)


class DatabaseProvider(Provider):
    """
    Database dishka provider
    """

    @provide(scope=Scope.APP)
    def provide_db_settings(self) -> DatabaseSettings:
        """Get database settings"""
        return DatabaseSettings()

    @provide(scope=Scope.APP)
    def provide_async_engine(self, db_settings: DatabaseSettings) -> AsyncEngine:
        engine = create_async_engine(url=db_settings.connection_url)
        logger.info("Async engine initialized")
        return engine

    @provide(scope=Scope.APP)
    def provide_async_session_factory(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        async_session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
        logger.debug("Async session maker initialized")
        return async_session_factory

    @provide(scope=Scope.REQUEST)
    async def provide_async_session(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> AsyncIterator[AsyncSession]:
        logger.debug("Starting async session...")
        async with session_factory() as session:
            logger.debug("Async session started")
            yield session
            logger.debug("Closing async session")

        logger.debug("Async session closed")

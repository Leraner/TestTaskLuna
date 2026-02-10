import logging
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from infrastructure.di.root_container import container
from infrastructure.seeders.app_seeder import AppSeeder
from infrastructure.web.exception_handling import handle_exceptions
from infrastructure.web.router import router
from infrastructure.web.settings import APISettings

logger = logging.getLogger(__name__)


class WebApplication:
    def __init__(self, settings: APISettings) -> None:
        self._settings = settings
        self._middlewares = []

    def _include_middlewares(self, application: FastAPI) -> None:
        for middleware in self._middlewares:
            application.add_middleware(middleware)

    async def _seed_database(self) -> None:
        async with container() as request_container:
            seeder = await request_container.get(AppSeeder)
            try:
                await seeder.seed()
                logger.info("Database seeded successfully")
            except Exception as e:
                logger.error(f"Error seeding database: {e}")

    def create_application(self) -> FastAPI:
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            logger.info("Application startup")
            await self._seed_database()
            yield
            logger.info("Application shutdown")

        application = FastAPI(**self._settings.model_dump(), lifespan=lifespan)

        # Setup dishka for web
        setup_dishka(app=application, container=container)
        logger.info("Dishka connected")

        # Include middlewares
        self._include_middlewares(application)
        logger.info("Middlewares included")

        # Include router
        application.include_router(router)
        logger.info("Routes included")

        # Handle exceptions
        handle_exceptions(application)

        return application

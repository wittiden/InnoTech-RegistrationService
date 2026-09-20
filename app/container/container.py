from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker, create_async_engine
from dishka import AsyncContainer, make_async_container, Provider, provide, Scope

from app.infrastructure.database.config import database_config


class DatabaseEngineProvider(Provider):
    """Провайдер по созданию движка бд"""

    @provide(scope=Scope.APP)
    async def create_engine(self) -> AsyncGenerator[AsyncEngine, None]:
        async_engine = create_async_engine(
            database_config.database_url,
            echo=False,
            pool_pre_ping=True,
            connect_args={'command_timeout': 5},
        )

        try:
            yield async_engine
        finally:
            await async_engine.dispose()


class DatabaseSessionProvider(Provider):
    """Провайдер по созданию сессий бд"""

    @provide(scope=Scope.APP)
    def create_async_session_factory(self, async_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=async_engine,
            autoflush=False,
            expire_on_commit=False,
        )

    @provide(scope=Scope.REQUEST)
    async def create_async_session(self, async_session_factory: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
        async with async_session_factory() as async_session:
            yield async_session


def build_async_container() -> AsyncContainer:
    container = make_async_container(
        DatabaseEngineProvider(),
        DatabaseSessionProvider(),
    )

    return container

async_container = build_async_container()

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker, create_async_engine
from dishka import AsyncContainer, make_async_container, Provider, provide, Scope
from keycloak import KeycloakOpenID, KeycloakAdmin

from app.infrastructure.keycloak.config import keycloak_config
from app.infrastructure.database.config import database_config
from app.modules.auth.service.use_cases import LoginUserCase, LogoutUserCase, RefreshTokenCase
from app.modules.users.service.use_cases import CreateUserCase, ShowUserCase


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


class KeycloakClientProvider(Provider):
    """Провайдер по созданию клиента Keycloak"""

    scope = Scope.APP

    @provide
    def build_keycloak_openid(self) -> KeycloakOpenID:
        return KeycloakOpenID(
            server_url=keycloak_config.KC_URL,
            realm_name=keycloak_config.KC_REALM,
            client_id=keycloak_config.KC_CLIENT_ID,
            client_secret_key=keycloak_config.KC_CLIENT_SECRET
        )

    @provide
    def build_keycloak_admin(self) -> KeycloakAdmin:
        return KeycloakAdmin(
            server_url=keycloak_config.KC_URL,
            realm_name=keycloak_config.KC_REALM,
            client_id=keycloak_config.KC_CLIENT_ID,
            client_secret_key=keycloak_config.KC_CLIENT_SECRET
        )


class AuthCaseProvider(Provider):
    """Провайдер по созданию кейсов аутентификации"""

    scope = Scope.REQUEST

    @provide
    def create_login(self, keycloak_openid: KeycloakOpenID) -> LoginUserCase:
        return LoginUserCase(keycloak_openid)

    @provide
    def create_logout(self, keycloak_openid: KeycloakOpenID) -> LogoutUserCase:
        return LogoutUserCase(keycloak_openid)

    @provide
    def create_refresh(self, keycloak_openid: KeycloakOpenID) -> RefreshTokenCase:
        return RefreshTokenCase(keycloak_openid)


class UserCaseProvider(Provider):
    """Провайдер по созданию кейсов пользователей"""

    scope = Scope.REQUEST

    @provide
    def create_user(self, keycloak_admin: KeycloakAdmin) -> CreateUserCase:
        return CreateUserCase(keycloak_admin)

    @provide
    def show_current(self, keycloak_openid: KeycloakOpenID) -> ShowUserCase:
        return ShowUserCase(keycloak_openid)


def build_async_container() -> AsyncContainer:
    container = make_async_container(
        DatabaseEngineProvider(),
        DatabaseSessionProvider(),
        KeycloakClientProvider(),
        AuthCaseProvider(),
        UserCaseProvider(),
    )

    return container

async_container = build_async_container()

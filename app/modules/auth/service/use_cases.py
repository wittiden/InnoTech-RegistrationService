from keycloak import KeycloakOpenID, KeycloakPostError, KeycloakAuthenticationError, KeycloakConnectionError, \
    KeycloakError

from app.modules.auth.contracts.dtos import LoginDTO, RefreshDTO
from app.modules.auth.exceptions import LoginError, LogoutError, RefreshError
from app.infrastructure.keycloak.excaptions import GeneralKeycloakError, KeycloakAuthError, GeneralKeycloakConnectionError


class LoginUserCase:
    """Кейс по входу пользователя в аккаунт"""

    __slots__ = ('_keycloak_openid',)

    def __init__(self, keycloak_openid: KeycloakOpenID) -> None:
        self._keycloak_openid = keycloak_openid

    async def login(self, username: str, password: str) -> LoginDTO:
        try:
            payload = await self._keycloak_openid.a_token(username, password)
        except KeycloakPostError as exc:
            raise LoginError('Invalid username or password') from exc
        except KeycloakAuthenticationError as exc:
            raise KeycloakAuthError('Keycloak auth failed') from exc
        except KeycloakConnectionError as exc:
            raise GeneralKeycloakConnectionError('Keycloak server is not available') from exc
        except KeycloakError as exc:
            raise GeneralKeycloakError(str(exc)) from exc

        return LoginDTO.model_validate(payload)


class LogoutUserCase:
    """Кейс по выходу пользователя из аккаунта"""

    __slots__ = ('_keycloak_openid',)

    def __init__(self, keycloak_openid: KeycloakOpenID) -> None:
        self._keycloak_openid = keycloak_openid

    async def logout(self, refresh_token: str) -> None:
        try:
            await self._keycloak_openid.a_logout(refresh_token)
        except KeycloakPostError as exc:
            raise LogoutError('Invalid refresh token') from exc
        except KeycloakAuthenticationError as exc:
            raise KeycloakAuthError('Keycloak auth failed') from exc
        except KeycloakConnectionError as exc:
            raise GeneralKeycloakConnectionError('Keycloak server is not available') from exc
        except KeycloakError as exc:
            raise GeneralKeycloakError(str(exc)) from exc


class RefreshTokenCase:
    """Кейс по обновлению JWT токена"""

    __slots__ = ('_keycloak_openid',)

    def __init__(self, keycloak_openid: KeycloakOpenID) -> None:
        self._keycloak_openid = keycloak_openid

    async def refresh(self, refresh_token: str) -> RefreshDTO:
        try:
            new_token = await self._keycloak_openid.a_refresh_token(refresh_token)
        except KeycloakPostError as exc:
            raise RefreshError('Burned refresh token') from exc
        except KeycloakAuthenticationError as exc:
            raise KeycloakAuthError('Keycloak auth failed') from exc
        except KeycloakConnectionError as exc:
            raise GeneralKeycloakConnectionError('Keycloak server is not available') from exc
        except KeycloakError as exc:
            raise GeneralKeycloakError(str(exc)) from exc

        return RefreshDTO.model_validate(new_token)

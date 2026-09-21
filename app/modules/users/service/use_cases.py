from uuid import UUID

from keycloak import KeycloakAdmin, KeycloakOpenID, KeycloakError, KeycloakPostError, KeycloakConnectionError, KeycloakAuthenticationError, KeycloakGetError

from app.modules.users.contracts.dtos import CreateUserDTO, FullUserInfoDTO
from app.modules.users.exceptions import CreateUserError, ShowUserError
from app.infrastructure.keycloak.excaptions import GeneralKeycloakError, KeycloakAuthError, GeneralKeycloakConnectionError


class CreateUserCase:
    """Кейс по созданию пользователей"""

    __slots__ = ('_keycloak_admin',)

    def __init__(self, keycloak_admin: KeycloakAdmin) -> None:
        self._keycloak_admin = keycloak_admin

    async def create_user(self, username: str, email: str, password: str, first_name: str | None = None, last_name: str | None = None) -> CreateUserDTO:
        try:
            user_id = await self._keycloak_admin.a_create_user(
                {
                    'username': username,
                    'email': email,
                    'firstName': first_name,
                    'lastName': last_name,
                    'enabled': True,
                    'credentials': [
                        {'type': 'password', 'value': password, 'temporary': False}
                    ],
                },
            )
        except KeycloakPostError as exc:
            raise CreateUserError('Invalid user data or duplicate key') from exc
        except KeycloakAuthenticationError as exc:
            raise KeycloakAuthError('Keycloak auth failed') from exc
        except KeycloakConnectionError as exc:
            raise GeneralKeycloakConnectionError('Keycloak server is not available') from exc
        except KeycloakError as exc:
            raise GeneralKeycloakError(str(exc)) from exc

        return CreateUserDTO(sub=UUID(user_id))


class ShowUserCase:
    """Кейс по показу пользователей"""

    __slots__ = ('_keycloak_openid',)

    def __init__(self, keycloak_openid: KeycloakOpenID) -> None:
        self._keycloak_openid = keycloak_openid

    async def show_current(self, access_token: str) -> FullUserInfoDTO:
        try:
            obj = await self._keycloak_openid.a_userinfo(access_token)

        except (KeycloakGetError, KeycloakAuthenticationError) as exc:
            raise ShowUserError('Invalid access token') from exc
        except KeycloakConnectionError as exc:
            raise GeneralKeycloakConnectionError('Keycloak server is not available') from exc
        except KeycloakError as exc:
            raise GeneralKeycloakError(str(exc)) from exc

        return FullUserInfoDTO.model_validate(obj)

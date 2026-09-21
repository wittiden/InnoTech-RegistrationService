from uuid import UUID

from keycloak import KeycloakAdmin, KeycloakError, KeycloakPostError, KeycloakConnectionError, KeycloakAuthenticationError

from app.modules.users.contracts.dtos import CreateUserDTO
from app.modules.users.exceptions import CreateUserError, CreateUserValidError, GeneralKeycloakError, GeneralKeycloakConnectionError, KeycloakAuthError


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

        try:
            return CreateUserDTO(id=UUID(user_id))
        except (ValueError, TypeError) as exc:
            raise CreateUserValidError('Unknown fields') from exc

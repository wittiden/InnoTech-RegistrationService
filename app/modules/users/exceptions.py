from app.common.handlers.utils.base import BaseError


class UserError(BaseError):
    title = 'User error'
    status_code = 400


class CreateUserError(UserError):
    title = 'Create user error'
    status_code = 409


class KeycloakAuthError(UserError):
    title = 'Keycloak auth error'
    status_code = 500


class GeneralKeycloakError(UserError):
    title = 'Keycloak error'
    status_code = 400


class GeneralKeycloakConnectionError(UserError):
    title = 'Keycloak connection error'
    status_code = 503


class ShowUserError(UserError):
    title = 'Show user error'
    status_code = 401

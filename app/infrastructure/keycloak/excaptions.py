from app.common.handlers.utils.base import BaseError


class SecurityError(BaseError):
    title = 'Security error'
    status_code = 400


class KeycloakAuthError(SecurityError):
    title = 'Keycloak auth error'
    status_code = 500


class GeneralKeycloakError(SecurityError):
    title = 'Keycloak error'
    status_code = 400


class GeneralKeycloakConnectionError(SecurityError):
    title = 'Keycloak connection error'
    status_code = 503

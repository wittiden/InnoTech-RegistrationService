from app.common.handlers.base import BaseError


class AuthError(BaseError):
    title = 'Auth error'
    status_code = 400


class LoginError(AuthError):
    title = 'Login error'
    status_code = 401


class LogoutError(AuthError):
    title = 'Logout error'
    status_code = 401


class RefreshError(AuthError):
    title = 'Refresh error'
    status_code = 401

from app.common.handlers.utils.base import BaseError


class UserError(BaseError):
    title = 'User error'
    status_code = 400


class CreateUserError(UserError):
    title = 'Create user error'
    status_code = 409


class ShowUserError(UserError):
    title = 'Show user error'
    status_code = 401

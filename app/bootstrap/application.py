from fastapi import FastAPI

from app.common.config import application_config


def setup_application() -> FastAPI:
    app = FastAPI(
        title='RegistrationService',
        version=application_config.PROJECT_VERSION,
        summary='RegistrationService API',
        description='Приложение: регистрация (логин - email, password))'
                    ' проверка email на валидность и отправляем на него ссылку,'
                    ' при переходе по ссылке - пользователь авторизуется в системе'
    )

    return app

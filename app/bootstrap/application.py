from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka

from app.common.config import application_config
from app.container.container import async_container


def setup_application() -> FastAPI:
    app = FastAPI(
        title='RegistrationService',
        version=application_config.PROJECT_VERSION,
        summary='RegistrationService API',
        description='Приложение: регистрация (логин - email, password))'
                    ' проверка email на валидность и отправляем на него ссылку,'
                    ' при переходе по ссылке - пользователь авторизуется в системе'
    )

    setup_dishka(async_container, app)

    return app

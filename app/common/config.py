from pydantic_settings import BaseSettings, SettingsConfigDict


class ApplicationConfig(BaseSettings):
    """Класс конфигурации общих настроек приложения"""

    ENVIRONMENT: str = 'dev'
    PROJECT_VERSION: str = '1.0'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

application_config = ApplicationConfig()

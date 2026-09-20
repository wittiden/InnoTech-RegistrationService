from pydantic_settings import BaseSettings, SettingsConfigDict


class KeycloakConfig(BaseSettings):
    """Класс для конфигурации настроек Keycloak"""

    KC_URL: str = 'http://keycloak:8080'
    KC_REALM: str = 'registration-service-realm'
    KC_CLIENT_ID: str = 'registration-service-client'
    KC_ADMIN_ID: str = 'registration-service-admin'
    KC_CLIENT_SECRET: str = ''
    KC_ADMIN_SECRET: str = ''

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

keycloak_config = KeycloakConfig()

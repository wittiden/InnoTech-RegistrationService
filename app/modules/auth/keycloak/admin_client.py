from keycloak import KeycloakAdmin

from app.modules.auth.keycloak.config import keycloak_config


def build_keycloak_admin() -> KeycloakAdmin:
    admin = KeycloakAdmin(
        server_url=keycloak_config.KC_URL,
        realm_name=keycloak_config.KC_REALM,
        client_id=keycloak_config.KC_ADMIN_ID,
        client_secret_key=keycloak_config.KC_ADMIN_SECRET,
        timeout=10,
    )

    return admin

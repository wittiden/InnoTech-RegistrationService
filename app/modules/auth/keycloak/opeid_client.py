from keycloak import KeycloakOpenID

from app.modules.auth.keycloak.config import keycloak_config


def build_keycloak_client() -> KeycloakOpenID:
    openid = KeycloakOpenID(
        server_url=keycloak_config.KC_URL,
        realm_name=keycloak_config.KC_REALM,
        client_id=keycloak_config.KC_CLIENT_ID,
        client_secret_key=keycloak_config.KC_CLIENT_SECRET,
        timeout=10,
    )

    return openid

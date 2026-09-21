from keycloak import KeycloakAdmin


async def send_email(keycloak_admin: KeycloakAdmin, user_id: str):
    await keycloak_admin.a_send_verify_email(user_id)

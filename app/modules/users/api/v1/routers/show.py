from fastapi import APIRouter, Depends
from dishka.integrations.fastapi import inject, FromDishka
from keycloak import KeycloakOpenID, KeycloakGetError

from app.common.security.security import get_token
from app.modules.users.contracts.dtos import FullUserInfoDTO

show_router = APIRouter(prefix='/api/v1/users', tags=['users'])


@show_router.get('/me', response_model=FullUserInfoDTO, summary='Show me')
@inject
async def show_current_user_endpoint(keycloak_openid: FromDishka[KeycloakOpenID], token: str = Depends(get_token)) -> FullUserInfoDTO:
    try:
        user = await keycloak_openid.a_userinfo(token)
    except Exception as exc:
        raise exc

    return FullUserInfoDTO.model_validate(user)

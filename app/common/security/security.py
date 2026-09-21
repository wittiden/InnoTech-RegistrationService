from typing import Annotated

from keycloak import KeycloakOpenID
from dishka.integrations.fastapi import inject, FromDishka
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends

from app.modules.users.contracts.dtos import FullUserInfoDTO

security = HTTPBearer()


def get_token(obj: HTTPAuthorizationCredentials = Depends(security)) -> str:
    return obj.credentials


@inject
async def get_current_user(keycloak_openid: FromDishka[KeycloakOpenID], token: str = Depends(get_token)) -> FullUserInfoDTO:
    user = await keycloak_openid.a_userinfo(token)
    return FullUserInfoDTO.model_validate(user)


CurrentUser = Annotated[FullUserInfoDTO, Depends(get_current_user)]

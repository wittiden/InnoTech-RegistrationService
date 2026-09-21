from fastapi import APIRouter, Depends
from dishka.integrations.fastapi import inject, FromDishka

from app.common.security.security import get_token
from app.modules.users.contracts.dtos import FullUserInfoDTO
from app.modules.users.service.use_cases import ShowUserCase

show_router = APIRouter(prefix='/api/v1/users', tags=['users'])


@show_router.get('/me', response_model=FullUserInfoDTO, summary='Show me')
@inject
async def show_current_user_endpoint(case: FromDishka[ShowUserCase], token: str = Depends(get_token)) -> FullUserInfoDTO:
    return await case.show_current(token)

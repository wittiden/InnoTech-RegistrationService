from fastapi import APIRouter, status
from dishka.integrations.fastapi import inject, FromDishka

from app.modules.auth.contracts.schemas import LoginSchema, LogoutSchema, RefreshSchema
from app.modules.auth.service.use_cases import LoginUserCase, LogoutUserCase, RefreshTokenCase
from app.modules.auth.contracts.dtos import LoginDTO, RefreshDTO

auth_router = APIRouter(prefix='/api/v1/auth', tags=['auth'])


@auth_router.post('/login', summary='Login user', response_model=LoginDTO)
@inject
async def login_endpoint(schema: LoginSchema, case: FromDishka[LoginUserCase]) -> LoginDTO:
    return await case.login(schema.username, schema.password)


@auth_router.post('/logout', summary='Logout user', status_code=status.HTTP_204_NO_CONTENT)
@inject
async def logout_endpoint(schema: LogoutSchema, case: FromDishka[LogoutUserCase]) -> None:
    await case.logout(schema.refresh_token)


@auth_router.post('/refresh', summary='Refresh user JWT', response_model=RefreshDTO)
@inject
async def refresh_endpoint(schema: RefreshSchema, case: FromDishka[RefreshTokenCase]) -> RefreshDTO:
    return await case.refresh(schema.refresh_token)

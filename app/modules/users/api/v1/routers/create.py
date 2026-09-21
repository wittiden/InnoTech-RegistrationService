from fastapi import APIRouter, status
from dishka.integrations.fastapi import inject, FromDishka

from app.modules.users.contracts.schemas import CreateSchema
from app.modules.users.contracts.dtos import CreateUserDTO
from app.modules.users.service.use_cases import CreateUserCase

create_router = APIRouter(prefix='/api/v1/users', tags=['users'])


@create_router.post('/', response_model=CreateUserDTO, summary='Create User', status_code=status.HTTP_201_CREATED)
@inject
async def create_user_endpoint(schema: CreateSchema, case: FromDishka[CreateUserCase]) -> CreateUserDTO:
    return await case.create_user(**schema.model_dump(exclude_none=True))

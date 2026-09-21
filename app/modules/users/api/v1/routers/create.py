from fastapi import APIRouter, status, BackgroundTasks
from dishka.integrations.fastapi import inject, FromDishka
from keycloak import KeycloakAdmin

from app.infrastructure.keycloak.email_sender.keycloak_sender import send_email
from app.modules.users.contracts.schemas import CreateSchema
from app.modules.users.contracts.dtos import CreateUserDTO
from app.modules.users.service.use_cases import CreateUserCase

create_router = APIRouter(prefix='/api/v1/users', tags=['users'])


@create_router.post('/', response_model=CreateUserDTO, summary='Create User', status_code=status.HTTP_201_CREATED)
@inject
async def create_user_endpoint(schema: CreateSchema, case: FromDishka[CreateUserCase], keycloak_admin: FromDishka[KeycloakAdmin], bg: BackgroundTasks) -> CreateUserDTO:
    result = await case.create_user(**schema.model_dump(exclude_none=True))

    bg.add_task(send_email, keycloak_admin=keycloak_admin, user_id=str(result.id))
    return result

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class FullUserInfoDTO(BaseModel):
    id: UUID = Field(validation_alias='sub')
    username: str = Field(validation_alias='preferred_username')
    email: str
    email_verified: bool
    first_name: str | None = Field(default=None, validation_alias='given_name')
    second_name: str | None = Field(default=None, validation_alias='family_name')

    model_config = ConfigDict(
        from_attributes=True,
    )


class CreateUserDTO(BaseModel):
    id: UUID = Field(validation_alias='sub')

    model_config = ConfigDict(
        from_attributes=True,
    )

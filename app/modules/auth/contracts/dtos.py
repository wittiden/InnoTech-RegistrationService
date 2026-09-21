from pydantic import BaseModel, Field, ConfigDict


class LoginDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = Field(default='Bearer')

    model_config = ConfigDict(
        from_attributes=True,
    )


class RefreshDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = Field(default='Bearer')

    model_config = ConfigDict(
        from_attributes=True,
    )

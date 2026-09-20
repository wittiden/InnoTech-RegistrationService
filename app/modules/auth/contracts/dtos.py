from pydantic import BaseModel, ConfigDict, Field


class LoginDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = Field(default='Bearer')


class RefreshDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = Field(default='Bearer')

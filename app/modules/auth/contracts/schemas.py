from pydantic import BaseModel, ConfigDict


class LoginSchema(BaseModel):
    username: str
    password: str


class LogoutSchema(BaseModel):
    refresh_token: str


class RefreshSchema(BaseModel):
    refresh_token: str

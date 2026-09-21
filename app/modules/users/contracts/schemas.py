from pydantic import BaseModel, Field, EmailStr


class CreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str | None = Field(examples=[None,])
    last_name: str | None = Field(examples=[None,])

from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    nome: str = Field(...)
    idade: int = Field(...)
    email: EmailStr = Field(...)

class UpdateUserModel(BaseModel):
    nome: Optional[str]
    idade: Optional[int]
    email: Optional[EmailStr]

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
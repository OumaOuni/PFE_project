from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date, datetime


class LoginRequest(BaseModel):
    username: str
    password: str


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    role: str


class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str
    role: str


class UserUpdateSchema(BaseModel):
    username: str
    email: str
    password: Optional[str] = None
    role: str

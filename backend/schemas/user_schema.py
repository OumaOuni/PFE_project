from typing import Optional

from pydantic import BaseModel, EmailStr
from datetime import date, datetime

class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        orm_mode = True


class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str
    role: str
class UserUpdateSchema(BaseModel):
    username: str
    email: str
    password: Optional[str] = None  # Optional for updates
    role: str
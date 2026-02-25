from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str


# Temporary users for testing
fake_users = {
    "oumaima": {"password": "123", "role": "ceo"},
    "sales": {"password": "123", "role": "sales_manager"},
    "inventory": {"password": "123", "role": "inventory_manager"},
}


@router.post("/login")
def login(user: LoginRequest):

    db_user = fake_users.get(user.username)

    if not db_user or db_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": "fake-token",
        "role": db_user["role"]
    }
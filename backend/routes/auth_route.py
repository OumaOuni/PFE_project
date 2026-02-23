from fastapi import APIRouter, HTTPException
from backend.schemas.user_schema import LoginRequest
from backend.controllers.auth_controller import login_controller


router = APIRouter()


@router.post("/login")
def login(request: LoginRequest):
    return login_controller(username=request.username, password=request.password)
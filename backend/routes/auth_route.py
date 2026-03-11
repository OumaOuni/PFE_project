# backend/routes/auth_route.py

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.controllers.auth_controller import login_user
from backend.schemas.user_schema import LoginRequest
from backend.dependencies.auth_dependencies import get_db

router = APIRouter(tags=["Auth"])



# Route definition
@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, request.username, request.password)
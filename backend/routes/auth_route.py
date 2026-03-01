# backend/routes/auth_route.py

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.controllers.auth_controller import login_user

router = APIRouter(tags=["Auth"])

# Request model
class LoginRequest(BaseModel):
    username: str
    password: str

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route definition
@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, request.username, request.password)
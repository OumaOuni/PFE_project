# backend/controllers/auth_controller.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.user_model import User
from backend.utils.security import verify_password, create_access_token


def login_user(db: Session, username: str, password: str):
    db_user = db.query(User).filter(User.username == username).first()
    
    if not db_user or not verify_password(password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(
        data={"sub": db_user.username, "role": db_user.role}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": db_user.role
    }
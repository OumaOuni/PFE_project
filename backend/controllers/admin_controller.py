# backend/controllers/admin_controller.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.user_model import User
from backend.schemas.user_schema import UserCreateSchema, UserUpdateSchema
from backend.utils.security import pwd_context


def get_all_users(db: Session):
    return db.query(User).all()


def create_user(db: Session, data: UserCreateSchema):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already in use")

    hashed_password = pwd_context.hash(data.password)
    new_user = User(
        username=data.username,
        email=data.email,
        password=hashed_password,
        role=data.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, user_id: int, data: UserUpdateSchema):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.username = data.username
    user.email = data.email
    user.role = data.role

    if data.password:
        user.password = pwd_context.hash(data.password)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}

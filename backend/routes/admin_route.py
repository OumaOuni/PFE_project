# backend/routes/admin_route.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from backend.dependencies.auth_dependencies import get_db, require_role
from backend.schemas.user_schema import UserResponseSchema, UserCreateSchema, UserUpdateSchema
from backend.controllers.admin_controller import (
    get_all_users,
    create_user,
    update_user,
    delete_user,
)

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=List[UserResponseSchema])
def list_users(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    return get_all_users(db)


@router.post("/users", response_model=UserResponseSchema, status_code=201)
def add_user(
    data: UserCreateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    return create_user(db, data)


@router.put("/users/{user_id}", response_model=UserResponseSchema)
def edit_user(
    user_id: int,
    data: UserUpdateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    return update_user(db, user_id, data)


@router.delete("/users/{user_id}")
def remove_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    return delete_user(db, user_id)

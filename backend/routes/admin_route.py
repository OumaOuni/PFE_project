from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.dependencies.auth_dependencies import require_role
from backend.dependencies.db_dependencies import get_db
from backend.controllers.admin_controller import (
    get_all_users,
    create_user,
    update_user,
    delete_user,
)

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users")
def list_users(
    db: Session = Depends(get_db), user=Depends(require_role("admin"))
):
    return get_all_users(db)


@router.post("/users")
def add_user(
    data: dict,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    if not data.get("username") or not data.get("password") or not data.get("role"):
        raise HTTPException(status_code=400, detail="username, password and role are required")
    return create_user(db, data)


@router.put("/users/{user_id}")
def edit_user(
    user_id: int,
    data: dict,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    if not data.get("username") or not data.get("role"):
        raise HTTPException(status_code=400, detail="username and role are required")
    return update_user(db, user_id, data)


@router.delete("/users/{user_id}")
def remove_user(
    user_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    return delete_user(db, user_id)

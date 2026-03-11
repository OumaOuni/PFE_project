from fastapi import APIRouter, Depends
from backend.dependencies.auth_dependencies import require_role

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/ceo")
def ceo_dashboard(user = Depends(require_role("ceo"))):
    return {"message": "Welcome CEO"}
@router.get("/admin")
def admin_dashboard(user = Depends(require_role("admin"))):
    return {"message": "Welcome Admin"}
@router.get("/sales")
def sales_dashboard(user = Depends(require_role("sales_manager"))):
    return {"message": "Welcome Sales Manager"}
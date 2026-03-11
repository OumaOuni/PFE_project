from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.dependencies.auth_dependencies import require_role
from backend.dependencies.db_dependencies import get_db
from backend.controllers.ceo_controller import get_ceo_kpis
from backend.controllers.sales_controller import get_sales_kpis
from backend.controllers.inventory_controller import get_inventory_kpis

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/ceo")
def ceo_dashboard(
    db: Session = Depends(get_db), user=Depends(require_role("ceo"))
):
    return get_ceo_kpis(db)


@router.get("/sales")
def sales_dashboard(
    db: Session = Depends(get_db), user=Depends(require_role("sales_manager"))
):
    return get_sales_kpis(db)


@router.get("/inventory")
def inventory_dashboard(
    db: Session = Depends(get_db), user=Depends(require_role("inventory_manager"))
):
    return get_inventory_kpis(db)

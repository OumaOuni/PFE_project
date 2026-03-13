from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.dependencies.auth_dependencies import require_role, get_db
from backend.controllers.ceo_controller import (
    get_kpi_data,
    get_monthly_sales,
    get_user_trend,
    get_distribution,
)
from backend.controllers.sales_controller import (
    get_sales_summary,
    get_top_products,
    get_sales_by_month,
)
from backend.controllers.dashboard_controller import get_inventory_summary

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/ceo")
def ceo_dashboard(
    db: Session = Depends(get_db),
    user=Depends(require_role("ceo")),
):
    return {
        "kpi": get_kpi_data(db),
        "sales": get_monthly_sales(db),
        "trend": get_user_trend(db),
        "distribution": get_distribution(db),
    }


@router.get("/admin")
def admin_dashboard(user=Depends(require_role("admin"))):
    return {"message": "Welcome Admin"}


@router.get("/sales")
def sales_dashboard(
    db: Session = Depends(get_db),
    user=Depends(require_role("sales_manager")),
):
    return {
        "summary": get_sales_summary(db),
        "top_products": get_top_products(db),
        "monthly": get_sales_by_month(db),
    }


@router.get("/inventory")
def inventory_dashboard(
    db: Session = Depends(get_db),
    user=Depends(require_role("inventory_manager")),
):
    return get_inventory_summary(db)
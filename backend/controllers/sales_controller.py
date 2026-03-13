# backend/controllers/sales_controller.py

from sqlalchemy.orm import Session
from sqlalchemy import text


def get_sales_summary(db: Session):
    total_revenue = db.execute(
        text("SELECT COALESCE(SUM(total_amount), 0) FROM openrational.orders")
    ).scalar() or 0

    total_orders = db.execute(
        text("SELECT COUNT(*) FROM openrational.orders")
    ).scalar() or 0

    avg_order_value = db.execute(
        text("SELECT COALESCE(AVG(total_amount), 0) FROM openrational.orders")
    ).scalar() or 0

    pending_orders = db.execute(
        text("SELECT COUNT(*) FROM openrational.orders WHERE status = 'pending'")
    ).scalar() or 0

    return {
        "total_revenue": round(float(total_revenue), 2),
        "total_orders": int(total_orders),
        "avg_order_value": round(float(avg_order_value), 2),
        "pending_orders": int(pending_orders),
    }


def get_top_products(db: Session):
    rows = db.execute(
        text("""
            SELECT p.product_name,
                   SUM(oi.quantity * oi.unit_price) AS revenue,
                   COUNT(DISTINCT oi.order_id) AS orders
            FROM openrational.order_items oi
            JOIN openrational.products p ON oi.product_id = p.product_id
            GROUP BY p.product_name
            ORDER BY revenue DESC
            LIMIT 10
        """)
    ).fetchall()
    return [{"name": r[0], "revenue": round(float(r[1]), 2), "orders": int(r[2])} for r in rows]


def get_sales_by_month(db: Session):
    rows = db.execute(
        text("""
            SELECT TO_CHAR(order_date, 'Mon YYYY') AS month,
                   ROUND(SUM(total_amount)::numeric, 2) AS revenue,
                   COUNT(*) AS orders
            FROM openrational.orders
            WHERE order_date >= CURRENT_DATE - INTERVAL '12 months'
            GROUP BY DATE_TRUNC('month', order_date), TO_CHAR(order_date, 'Mon YYYY')
            ORDER BY DATE_TRUNC('month', order_date)
        """)
    ).fetchall()
    return [{"month": r[0], "revenue": float(r[1]), "orders": int(r[2])} for r in rows]

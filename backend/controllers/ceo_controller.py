# backend/controllers/ceo_controller.py

from sqlalchemy.orm import Session
from sqlalchemy import text


def get_kpi_data(db: Session):
    revenue = db.execute(
        text("SELECT COALESCE(SUM(total_amount), 0) FROM openrational.orders")
    ).scalar() or 0

    users = db.execute(
        text("SELECT COUNT(*) FROM openrational.users")
    ).scalar() or 0

    orders_total = db.execute(
        text("SELECT COUNT(*) FROM openrational.orders")
    ).scalar() or 1

    orders_converted = db.execute(
        text("SELECT COUNT(*) FROM openrational.orders WHERE status = 'completed'")
    ).scalar() or 0

    conversion = round((orders_converted / max(orders_total, 1)) * 100, 1)

    growth = db.execute(
        text("""
            SELECT ROUND(
                ((curr.total - prev.total)::numeric / NULLIF(prev.total, 0)) * 100, 1
            )
            FROM (
                SELECT COALESCE(SUM(total_amount), 0) AS total
                FROM openrational.orders
                WHERE DATE_TRUNC('month', order_date) = DATE_TRUNC('month', CURRENT_DATE)
            ) curr,
            (
                SELECT COALESCE(SUM(total_amount), 0) AS total
                FROM openrational.orders
                WHERE DATE_TRUNC('month', order_date) = DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
            ) prev
        """)
    ).scalar() or 0

    return {
        "revenue": round(float(revenue) / 1000, 1),
        "users": int(users),
        "conversion": float(conversion),
        "growth": float(growth),
    }


def get_monthly_sales(db: Session):
    rows = db.execute(
        text("""
            SELECT TO_CHAR(order_date, 'Mon') AS month,
                   ROUND(SUM(total_amount)::numeric / 1000, 1) AS revenue
            FROM openrational.orders
            WHERE order_date >= CURRENT_DATE - INTERVAL '12 months'
            GROUP BY DATE_TRUNC('month', order_date), TO_CHAR(order_date, 'Mon')
            ORDER BY DATE_TRUNC('month', order_date)
        """)
    ).fetchall()
    return [{"month": r[0], "revenue": float(r[1])} for r in rows]


def get_user_trend(db: Session):
    # users table has no created_at — return count per role as a trend proxy
    rows = db.execute(
        text("""
            SELECT role, COUNT(*) AS users
            FROM openrational.users
            GROUP BY role
            ORDER BY users DESC
        """)
    ).fetchall()
    return [{"date": r[0], "users": int(r[1])} for r in rows]


def get_distribution(db: Session):
    rows = db.execute(
        text("""
            SELECT c.category_name,
                   ROUND(SUM(oi.quantity * oi.unit_price)::numeric / 1000, 1) AS value
            FROM openrational.order_items oi
            JOIN openrational.products p ON oi.product_id = p.product_id
            JOIN openrational.categories c ON p.category_id = c.category_id
            GROUP BY c.category_name
            ORDER BY value DESC
        """)
    ).fetchall()
    return [{"segment": r[0], "value": float(r[1])} for r in rows]

# backend/controllers/dashboard_controller.py

from sqlalchemy.orm import Session
from sqlalchemy import text


def get_inventory_summary(db: Session):
    total_products = db.execute(
        text("SELECT COUNT(*) FROM openrational.products WHERE is_active = true")
    ).scalar() or 0

    low_stock = db.execute(
        text("""
            SELECT COUNT(*) FROM (
                SELECT p.product_id, COALESCE(SUM(sm.quantity), 0) AS stock
                FROM openrational.products p
                LEFT JOIN openrational.stock_movements sm ON sm.product_id = p.product_id
                WHERE p.is_active = true
                GROUP BY p.product_id
                HAVING COALESCE(SUM(sm.quantity), 0) > 0
                   AND COALESCE(SUM(sm.quantity), 0) <= 10
            ) sub
        """)
    ).scalar() or 0

    out_of_stock = db.execute(
        text("""
            SELECT COUNT(*) FROM (
                SELECT p.product_id, COALESCE(SUM(sm.quantity), 0) AS stock
                FROM openrational.products p
                LEFT JOIN openrational.stock_movements sm ON sm.product_id = p.product_id
                WHERE p.is_active = true
                GROUP BY p.product_id
                HAVING COALESCE(SUM(sm.quantity), 0) = 0
            ) sub
        """)
    ).scalar() or 0

    total_stock_value = db.execute(
        text("""
            SELECT COALESCE(SUM(p.selling_price * stock.qty), 0)
            FROM openrational.products p
            JOIN (
                SELECT product_id, COALESCE(SUM(quantity), 0) AS qty
                FROM openrational.stock_movements
                GROUP BY product_id
            ) stock ON stock.product_id = p.product_id
            WHERE p.is_active = true
        """)
    ).scalar() or 0

    products = db.execute(
        text("""
            SELECT
                p.product_id,
                p.product_name,
                COALESCE(c.category_name, '') AS category_name,
                p.cost_price,
                p.selling_price,
                COALESCE(SUM(sm.quantity), 0) AS stock_quantity
            FROM openrational.products p
            LEFT JOIN openrational.categories c ON c.category_id = p.category_id
            LEFT JOIN openrational.stock_movements sm ON sm.product_id = p.product_id
            WHERE p.is_active = true
            GROUP BY p.product_id, p.product_name, c.category_name, p.cost_price, p.selling_price
            ORDER BY stock_quantity ASC
            LIMIT 100
        """)
    ).fetchall()

    return {
        "summary": {
            "total_products": int(total_products),
            "low_stock": int(low_stock),
            "out_of_stock": int(out_of_stock),
            "total_stock_value": round(float(total_stock_value), 2),
        },
        "products": [
            {
                "product_id": r[0],
                "product_name": r[1],
                "category_name": r[2],
                "cost_price": float(r[3]) if r[3] else 0.0,
                "selling_price": float(r[4]) if r[4] else 0.0,
                "stock_quantity": int(r[5]),
            }
            for r in products
        ],
    }

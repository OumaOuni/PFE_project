from sqlalchemy import text


def get_inventory_kpis(db):
    # Summary KPIs
    summary = db.execute(text("""
        SELECT
            COUNT(i.id) AS total_products,
            COALESCE(SUM(i.quantity), 0) AS total_units,
            COALESCE(SUM(i.quantity * p.cost), 0) AS total_stock_value,
            SUM(CASE WHEN i.quantity <= i.min_stock THEN 1 ELSE 0 END) AS critical_count,
            SUM(CASE WHEN i.quantity > i.min_stock
                      AND i.quantity <= i.reorder_point THEN 1 ELSE 0 END) AS low_count
        FROM luxury.inventory i
        JOIN luxury.products p ON i.product_id = p.id
    """)).fetchone()

    # Critical stock (quantity <= min_stock)
    critical = db.execute(text("""
        SELECT p.name, p.collection, c.name AS category,
               i.quantity, i.min_stock
        FROM luxury.inventory i
        JOIN luxury.products p ON i.product_id = p.id
        JOIN luxury.categories c ON p.category_id = c.id
        WHERE i.quantity <= i.min_stock
        ORDER BY i.quantity
    """)).fetchall()

    # Low stock (min_stock < quantity <= reorder_point)
    low_stock = db.execute(text("""
        SELECT p.name, p.collection, c.name AS category,
               i.quantity, i.reorder_point
        FROM luxury.inventory i
        JOIN luxury.products p ON i.product_id = p.id
        JOIN luxury.categories c ON p.category_id = c.id
        WHERE i.quantity > i.min_stock AND i.quantity <= i.reorder_point
        ORDER BY i.quantity
    """)).fetchall()

    # Stock units by category
    by_category = db.execute(text("""
        SELECT c.name AS category, SUM(i.quantity) AS units
        FROM luxury.inventory i
        JOIN luxury.products p ON i.product_id = p.id
        JOIN luxury.categories c ON p.category_id = c.id
        GROUP BY c.name
    """)).fetchall()

    # Stock movements IN vs OUT per month (last 6 months)
    movements = db.execute(text("""
        SELECT
            TO_CHAR(DATE_TRUNC('month', movement_date), 'Mon YYYY') AS month,
            SUM(CASE WHEN movement_type = 'IN' THEN quantity ELSE 0 END) AS stock_in,
            SUM(CASE WHEN movement_type = 'OUT' THEN quantity ELSE 0 END) AS stock_out
        FROM luxury.stock_movements
        WHERE movement_date >= NOW() - INTERVAL '6 months'
        GROUP BY DATE_TRUNC('month', movement_date)
        ORDER BY DATE_TRUNC('month', movement_date)
    """)).fetchall()

    # Full inventory list with status
    all_products = db.execute(text("""
        SELECT p.name, c.name AS category, p.collection, i.quantity,
               CASE
                   WHEN i.quantity <= i.min_stock THEN 'Critical'
                   WHEN i.quantity <= i.reorder_point THEN 'Low'
                   ELSE 'OK'
               END AS status
        FROM luxury.inventory i
        JOIN luxury.products p ON i.product_id = p.id
        JOIN luxury.categories c ON p.category_id = c.id
        ORDER BY i.quantity
    """)).fetchall()

    return {
        "summary": {
            "total_products": int(summary.total_products or 0),
            "total_units": int(summary.total_units or 0),
            "total_stock_value": float(summary.total_stock_value or 0),
            "critical_count": int(summary.critical_count or 0),
            "low_count": int(summary.low_count or 0),
        },
        "critical_stock": [
            {
                "name": r.name,
                "collection": r.collection,
                "category": r.category,
                "quantity": r.quantity,
                "min_stock": r.min_stock,
            }
            for r in critical
        ],
        "low_stock": [
            {
                "name": r.name,
                "collection": r.collection,
                "category": r.category,
                "quantity": r.quantity,
                "reorder_point": r.reorder_point,
            }
            for r in low_stock
        ],
        "stock_by_category": [
            {"category": r.category, "units": int(r.units)} for r in by_category
        ],
        "movements": [
            {
                "month": r.month,
                "stock_in": int(r.stock_in),
                "stock_out": int(r.stock_out),
            }
            for r in movements
        ],
        "all_products": [
            {
                "name": r.name,
                "category": r.category,
                "collection": r.collection,
                "quantity": r.quantity,
                "status": r.status,
            }
            for r in all_products
        ],
    }

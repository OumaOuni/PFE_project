from sqlalchemy import text


def get_ceo_kpis(db):
    # KPIs: monthly revenue, total revenue, total customers, monthly orders
    kpi = db.execute(text("""
        SELECT
            COALESCE(SUM(CASE
                WHEN EXTRACT(YEAR FROM sale_date) = EXTRACT(YEAR FROM NOW())
                 AND EXTRACT(MONTH FROM sale_date) = EXTRACT(MONTH FROM NOW())
                THEN total_amount ELSE 0 END), 0) AS monthly_revenue,
            COALESCE(SUM(total_amount), 0) AS total_revenue,
            (SELECT COUNT(*) FROM luxury.customers) AS total_customers,
            COUNT(CASE
                WHEN EXTRACT(YEAR FROM sale_date) = EXTRACT(YEAR FROM NOW())
                 AND EXTRACT(MONTH FROM sale_date) = EXTRACT(MONTH FROM NOW())
                THEN 1 END) AS monthly_orders
        FROM luxury.sales
    """)).fetchone()

    # Profit margin calculation
    margin = db.execute(text("""
        SELECT
            COALESCE(SUM(s.total_amount), 0) AS revenue,
            COALESCE(SUM(p.cost * s.quantity), 0) AS total_cost
        FROM luxury.sales s
        JOIN luxury.products p ON s.product_id = p.id
    """)).fetchone()

    revenue = float(margin.revenue or 0)
    cost = float(margin.total_cost or 0)
    profit_margin = round(((revenue - cost) / revenue * 100) if revenue > 0 else 0, 1)

    # Monthly revenue trend (last 6 months)
    trend = db.execute(text("""
        SELECT
            TO_CHAR(DATE_TRUNC('month', sale_date), 'Mon YYYY') AS month,
            SUM(total_amount) AS revenue
        FROM luxury.sales
        WHERE sale_date >= NOW() - INTERVAL '6 months'
        GROUP BY DATE_TRUNC('month', sale_date)
        ORDER BY DATE_TRUNC('month', sale_date)
    """)).fetchall()

    # Sales by region
    regions = db.execute(text("""
        SELECT region, SUM(total_amount) AS revenue
        FROM luxury.sales
        GROUP BY region
        ORDER BY revenue DESC
    """)).fetchall()

    # Top 5 products by revenue
    products = db.execute(text("""
        SELECT p.name, SUM(s.total_amount) AS revenue
        FROM luxury.sales s
        JOIN luxury.products p ON s.product_id = p.id
        GROUP BY p.name
        ORDER BY revenue DESC
        LIMIT 5
    """)).fetchall()

    # Low stock alerts
    low_stock = db.execute(text("""
        SELECT p.name, p.collection, c.name AS category,
               i.quantity, i.min_stock
        FROM luxury.inventory i
        JOIN luxury.products p ON i.product_id = p.id
        JOIN luxury.categories c ON p.category_id = c.id
        WHERE i.quantity <= i.min_stock
        ORDER BY i.quantity
    """)).fetchall()

    return {
        "kpis": {
            "monthly_revenue": float(kpi.monthly_revenue or 0),
            "total_revenue": float(kpi.total_revenue or 0),
            "total_customers": int(kpi.total_customers or 0),
            "monthly_orders": int(kpi.monthly_orders or 0),
            "profit_margin": profit_margin,
        },
        "monthly_trend": [
            {"month": r.month, "revenue": float(r.revenue)} for r in trend
        ],
        "sales_by_region": [
            {"region": r.region, "revenue": float(r.revenue)} for r in regions
        ],
        "top_products": [
            {"name": r.name, "revenue": float(r.revenue)} for r in products
        ],
        "low_stock": [
            {
                "name": r.name,
                "collection": r.collection,
                "category": r.category,
                "quantity": r.quantity,
                "min_stock": r.min_stock,
            }
            for r in low_stock
        ],
    }

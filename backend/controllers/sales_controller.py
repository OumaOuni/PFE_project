from sqlalchemy import text


def get_sales_kpis(db):
    # Salesperson leaderboard for current year
    leaderboard = db.execute(text("""
        SELECT sp.full_name, sp.region,
               SUM(s.total_amount) AS total_sales,
               COUNT(s.id) AS orders
        FROM luxury.sales s
        JOIN luxury.salespersons sp ON s.salesperson_id = sp.id
        WHERE EXTRACT(YEAR FROM s.sale_date) = EXTRACT(YEAR FROM NOW())
        GROUP BY sp.full_name, sp.region
        ORDER BY total_sales DESC
    """)).fetchall()

    # Revenue per product category
    categories = db.execute(text("""
        SELECT c.name, SUM(s.total_amount) AS revenue
        FROM luxury.sales s
        JOIN luxury.products p ON s.product_id = p.id
        JOIN luxury.categories c ON p.category_id = c.id
        GROUP BY c.name
        ORDER BY revenue DESC
    """)).fetchall()

    # Monthly actual vs target (current year)
    monthly_vs_target = db.execute(text("""
        SELECT
            t.month,
            TO_CHAR(TO_DATE(t.month::text, 'MM'), 'Mon') AS month_name,
            SUM(t.target_amount) AS target,
            COALESCE(SUM(s.total_amount), 0) AS actual
        FROM luxury.targets t
        LEFT JOIN luxury.sales s
            ON s.salesperson_id = t.salesperson_id
            AND EXTRACT(MONTH FROM s.sale_date) = t.month
            AND EXTRACT(YEAR FROM s.sale_date) = t.year
        WHERE t.year = EXTRACT(YEAR FROM NOW())
        GROUP BY t.month
        ORDER BY t.month
    """)).fetchall()

    # Top 10 customers by total spend
    top_customers = db.execute(text("""
        SELECT c.full_name, c.country, c.type,
               SUM(s.total_amount) AS total_spent
        FROM luxury.sales s
        JOIN luxury.customers c ON s.customer_id = c.id
        GROUP BY c.full_name, c.country, c.type
        ORDER BY total_spent DESC
        LIMIT 10
    """)).fetchall()

    # Revenue by city (top 8)
    by_city = db.execute(text("""
        SELECT city, SUM(total_amount) AS revenue
        FROM luxury.sales
        GROUP BY city
        ORDER BY revenue DESC
        LIMIT 8
    """)).fetchall()

    # Average order value
    avg = db.execute(text("""
        SELECT COALESCE(AVG(total_amount), 0) AS avg_order_value
        FROM luxury.sales
    """)).fetchone()

    return {
        "leaderboard": [
            {
                "name": r.full_name,
                "region": r.region,
                "total_sales": float(r.total_sales),
                "orders": int(r.orders),
            }
            for r in leaderboard
        ],
        "sales_by_category": [
            {"name": r.name, "revenue": float(r.revenue)} for r in categories
        ],
        "monthly_vs_target": [
            {
                "month": r.month_name,
                "actual": float(r.actual),
                "target": float(r.target),
            }
            for r in monthly_vs_target
        ],
        "top_customers": [
            {
                "name": r.full_name,
                "country": r.country,
                "type": r.type,
                "total_spent": float(r.total_spent),
            }
            for r in top_customers
        ],
        "sales_by_city": [
            {"city": r.city, "revenue": float(r.revenue)} for r in by_city
        ],
        "avg_order_value": round(float(avg.avg_order_value or 0), 2),
    }

from ..models.sales_model import get_total_revenue, get_total_profit

def get_ceo_dashboard(conn):
    revenue = get_total_revenue(conn)
    profit = get_total_profit(conn)

    return {
        "total_revenue": revenue,
        "total_profit": profit
    }
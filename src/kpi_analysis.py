def calculate_kpis(df):
    revenue = df["Revenue"].sum()
    profit = df["Profit"].sum()
    orders = df["Order ID"].nunique()
    return {
        "total_revenue": revenue,
        "total_profit": profit,
        "profit_margin": profit / revenue if revenue else 0,
        "orders": orders,
        "average_order_value": revenue / orders if orders else 0,
    }

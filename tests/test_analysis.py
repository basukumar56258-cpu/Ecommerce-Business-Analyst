import pandas as pd
from src.data_cleaning import clean_sales_data
from src.kpi_analysis import calculate_kpis

def sample():
    return pd.DataFrame({
        "Order ID": ["1", "2"],
        "Order Date": ["2026-01-01", "2026-01-02"],
        "Region": ["North", "South"],
        "Category": ["Electronics", "Furniture"],
        "Quantity": [2, 1],
        "Unit Price": [100, 200],
        "Discount": [0, 0],
    })

def test_cleaning():
    df = clean_sales_data(sample())
    assert len(df) == 2
    assert "Profit" in df.columns
    assert "Profit Margin" in df.columns

def test_kpis():
    df = clean_sales_data(sample())
    kpi = calculate_kpis(df)
    assert kpi["total_revenue"] == 400
    assert kpi["orders"] == 2

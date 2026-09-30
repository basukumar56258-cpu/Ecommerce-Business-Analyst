import pandas as pd
import numpy as np

def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy().drop_duplicates()
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    for c in ["Quantity", "Unit Price"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    if "Discount" not in df:
        df["Discount"] = 0
    df["Discount"] = pd.to_numeric(df["Discount"], errors="coerce").fillna(0)
    df = df.dropna(subset=["Order Date", "Quantity", "Unit Price"])
    df["Revenue"] = df["Quantity"] * df["Unit Price"] * (1 - df["Discount"])
    if "Cost" not in df:
        df["Cost"] = df["Revenue"] * 0.70
    df["Profit"] = df["Revenue"] - df["Cost"]
    df["Profit Margin"] = np.where(df["Revenue"] != 0, df["Profit"] / df["Revenue"], 0)
    return df

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Business Analytics Dashboard", page_icon="📊", layout="wide")

@st.cache_data
def demo_data(n=3000):
    rng = np.random.default_rng(42)
    dates = pd.date_range("2025-01-01", "2026-08-31", freq="D")
    regions = ["North", "South", "East", "West"]
    categories = ["Electronics", "Furniture", "Office Supplies", "Accessories"]
    channels = ["Online", "Retail", "Wholesale"]

    df = pd.DataFrame({
        "Order ID": [f"ORD-{100001+i}" for i in range(n)],
        "Order Date": rng.choice(dates, n),
        "Region": rng.choice(regions, n),
        "Category": rng.choice(categories, n),
        "Channel": rng.choice(channels, n, p=[.5, .3, .2]),
        "Customer ID": [f"CUST-{x}" for x in rng.integers(1000, 1800, n)],
        "Quantity": rng.integers(1, 10, n),
        "Unit Price": np.round(rng.uniform(250, 15000, n), 2),
        "Discount": np.round(rng.uniform(0, .25, n), 2),
    })
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Revenue"] = df["Quantity"] * df["Unit Price"] * (1 - df["Discount"])
    df["Cost"] = df["Revenue"] * rng.uniform(.55, .82, n)
    df["Profit"] = df["Revenue"] - df["Cost"]
    df["Profit Margin"] = np.where(df["Revenue"] != 0, df["Profit"] / df["Revenue"], 0)
    return df

def load_data(upload):
    if upload is None:
        return demo_data(), "Demo dataset"
    df = pd.read_csv(upload)
    required = ["Order Date", "Region", "Category", "Quantity", "Unit Price"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error("Missing required columns: " + ", ".join(missing))
        st.stop()

    df = df.drop_duplicates()
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    for col in ["Quantity", "Unit Price", "Discount"]:
        if col not in df.columns:
            df[col] = 0 if col == "Discount" else np.nan
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["Order Date", "Quantity", "Unit Price"])
    if "Order ID" not in df.columns:
        df["Order ID"] = [f"ORD-{i+1}" for i in range(len(df))]
    if "Customer ID" not in df.columns:
        df["Customer ID"] = "UNKNOWN"
    if "Revenue" not in df.columns:
        df["Revenue"] = df["Quantity"] * df["Unit Price"] * (1 - df["Discount"].fillna(0))
    if "Cost" not in df.columns:
        df["Cost"] = df["Revenue"] * .70
    if "Profit" not in df.columns:
        df["Profit"] = df["Revenue"] - df["Cost"]
    df["Profit Margin"] = np.where(df["Revenue"] != 0, df["Profit"] / df["Revenue"], 0)
    return df, "Uploaded CSV"

st.title("📊 Sales & Customer Performance Analytics")
st.caption("Business Analyst Portfolio Project | Python • SQL • Streamlit • Plotly")

with st.sidebar:
    st.header("Controls")
    uploaded = st.file_uploader("Upload sales CSV", type=["csv"])
    st.caption("No upload? The dashboard uses a professional demo dataset.")

df, source = load_data(uploaded)
st.sidebar.success(f"{source}: {len(df):,} rows")

min_d, max_d = df["Order Date"].min().date(), df["Order Date"].max().date()
date_range = st.sidebar.date_input("Date range", (min_d, max_d), min_value=min_d, max_value=max_d)
regions = st.sidebar.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
cats = st.sidebar.multiselect("Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))

if len(date_range) == 2:
    filtered = df[(df["Order Date"].dt.date >= date_range[0]) & (df["Order Date"].dt.date <= date_range[1])]
else:
    filtered = df.copy()
filtered = filtered[filtered["Region"].isin(regions) & filtered["Category"].isin(cats)]

revenue = filtered["Revenue"].sum()
profit = filtered["Profit"].sum()
orders = filtered["Order ID"].nunique()
customers = filtered["Customer ID"].nunique()
margin = profit / revenue if revenue else 0
aov = revenue / orders if orders else 0

k1,k2,k3,k4,k5 = st.columns(5)
k1.metric("Revenue", f"₹{revenue:,.0f}")
k2.metric("Profit", f"₹{profit:,.0f}")
k3.metric("Profit Margin", f"{margin:.1%}")
k4.metric("Orders", f"{orders:,}")
k5.metric("Avg. Order Value", f"₹{aov:,.0f}")

st.divider()
st.subheader("🎯 Executive Summary")
if len(filtered):
    top_region = filtered.groupby("Region")["Revenue"].sum().idxmax()
    top_category = filtered.groupby("Category")["Revenue"].sum().idxmax()
    low_margin = filtered.groupby("Region")["Profit Margin"].mean().idxmin()
    st.info(
        f"**Management view:** {top_region} is the highest-revenue region and "
        f"{top_category} is the leading revenue category. {low_margin} has the "
        f"lowest average margin among selected regions and should be reviewed for pricing, "
        f"discounting and product mix."
    )

st.subheader("📈 Revenue & Profit Trend")
monthly = (filtered.assign(Month=filtered["Order Date"].dt.to_period("M").astype(str))
           .groupby("Month", as_index=False)[["Revenue","Profit"]].sum())
if not monthly.empty:
    fig = px.line(monthly, x="Month", y=["Revenue","Profit"], markers=True,
                  title="Monthly Revenue and Profit")
    st.plotly_chart(fig, use_container_width=True)

c1,c2 = st.columns(2)
with c1:
    st.subheader("🌍 Regional Performance")
    region = filtered.groupby("Region", as_index=False).agg(Revenue=("Revenue","sum"), Profit=("Profit","sum"))
    fig = px.bar(region.sort_values("Revenue", ascending=False), x="Region", y="Revenue",
                 text_auto=".2s", title="Revenue by Region")
    st.plotly_chart(fig, use_container_width=True)
with c2:
    st.subheader("📦 Category Profitability")
    cat = filtered.groupby("Category", as_index=False).agg(Revenue=("Revenue","sum"), Profit=("Profit","sum"))
    fig = px.bar(cat.sort_values("Profit", ascending=False), x="Category", y="Profit",
                 text_auto=".2s", title="Profit by Category")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("👥 Customer Performance")
cust = (filtered.groupby("Customer ID", as_index=False)
        .agg(Revenue=("Revenue","sum"), Profit=("Profit","sum"), Orders=("Order ID","nunique"))
        .sort_values("Revenue", ascending=False))
st.dataframe(cust.head(20), use_container_width=True)

with st.expander("🔍 Data Quality & Business Checks"):
    checks = pd.DataFrame({
        "Check": ["Rows", "Columns", "Duplicate rows", "Missing values", "Negative revenue"],
        "Result": [len(df), len(df.columns), int(df.duplicated().sum()),
                   int(df.isna().sum().sum()), int((df["Revenue"] < 0).sum())]
    })
    st.dataframe(checks, use_container_width=True)

st.subheader("📥 Export")
st.download_button(
    "Download filtered analysis CSV",
    filtered.to_csv(index=False).encode("utf-8"),
    "filtered_business_analysis.csv",
    "text/csv"
)
st.caption("Built as a portfolio-ready Business Analyst project demonstrating data preparation, KPI analysis, visualization and decision support.")

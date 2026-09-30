def business_insights(df):
    return {
        "top_region": df.groupby("Region")["Revenue"].sum().idxmax(),
        "top_category": df.groupby("Category")["Revenue"].sum().idxmax(),
        "most_profitable_category": df.groupby("Category")["Profit"].sum().idxmax(),
    }

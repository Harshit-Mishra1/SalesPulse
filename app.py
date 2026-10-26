from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="SalesPulse | Sales Analytics", page_icon="📊", layout="wide")

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "sales_data.csv"

st.title("📊 SalesPulse")
st.caption("Business Intelligence & Sales Analytics | Interactive retail performance dashboard")
st.info("Portfolio demo: this dashboard uses synthetic sample data, not real company transactions.")

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(path, parse_dates=["Order_Date"])
    required = ["Order_ID", "Order_Date", "Region", "Category", "Product",
                "Customer_Segment", "Quantity", "Unit_Price", "Discount", "Revenue", "Profit"]
    missing = [column for column in required if column not in data.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")
    data = data.drop_duplicates()
    data["Profit_Margin"] = data["Profit"] / data["Revenue"].replace(0, pd.NA)
    data["Month"] = data["Order_Date"].dt.to_period("M").astype(str)
    return data

try:
    df = load_data(str(DATA_PATH))
except Exception as exc:
    st.error(f"Could not load data: {exc}")
    st.stop()

with st.sidebar:
    st.header("Filter data")
    min_date = df["Order_Date"].min().date()
    max_date = df["Order_Date"].max().date()
    date_range = st.date_input("Order date range", value=(min_date, max_date),
                               min_value=min_date, max_value=max_date)
    regions = st.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
    categories = st.multiselect("Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))
    segments = st.multiselect("Customer segment", sorted(df["Customer_Segment"].unique()),
                              default=sorted(df["Customer_Segment"].unique()))

filtered = df.copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
    filtered = filtered[filtered["Order_Date"].between(start, end)]
filtered = filtered[
    filtered["Region"].isin(regions)
    & filtered["Category"].isin(categories)
    & filtered["Customer_Segment"].isin(segments)
]

if filtered.empty:
    st.warning("No records match the selected filters. Change one or more filters.")
    st.stop()

revenue = filtered["Revenue"].sum()
profit = filtered["Profit"].sum()
orders = filtered["Order_ID"].nunique()
quantity = filtered["Quantity"].sum()
margin = profit / revenue if revenue else 0
aov = revenue / orders if orders else 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Revenue", f"${revenue:,.0f}")
k2.metric("Total Profit", f"${profit:,.0f}")
k3.metric("Profit Margin", f"{margin:.1%}")
k4.metric("Orders", f"{orders:,}")
k5.metric("Avg. Order Value", f"${aov:,.2f}")

st.divider()
left, right = st.columns(2)

with left:
    st.subheader("Revenue and profit over time")
    monthly = filtered.groupby("Month", as_index=False).agg(Revenue=("Revenue", "sum"), Profit=("Profit", "sum"))
    long_monthly = monthly.melt(id_vars="Month", value_vars=["Revenue", "Profit"],
                                var_name="Metric", value_name="Amount")
    fig = px.line(long_monthly, x="Month", y="Amount", color="Metric", markers=True,
                  title="Monthly performance")
    fig.update_layout(xaxis_title="", yaxis_title="Amount ($)", legend_title="")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Revenue by category")
    by_category = filtered.groupby("Category", as_index=False).agg(Revenue=("Revenue", "sum"), Profit=("Profit", "sum"))
    fig = px.bar(by_category, x="Category", y="Revenue", color="Category", title="Category revenue")
    fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Revenue ($)")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Regional performance")
    by_region = filtered.groupby("Region", as_index=False).agg(Revenue=("Revenue", "sum"), Profit=("Profit", "sum"))
    fig = px.bar(by_region, x="Region", y=["Revenue", "Profit"], barmode="group", title="Revenue vs. profit by region")
    fig.update_layout(xaxis_title="", yaxis_title="Amount ($)", legend_title="")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Top 10 products by revenue")
    top_products = (filtered.groupby("Product", as_index=False)
                    .agg(Revenue=("Revenue", "sum"), Profit=("Profit", "sum"))
                    .sort_values("Revenue", ascending=False).head(10))
    fig = px.bar(top_products.sort_values("Revenue"), x="Revenue", y="Product", orientation="h",
                 color="Profit", title="Top products")
    fig.update_layout(xaxis_title="Revenue ($)", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Customer segment performance")
by_segment = filtered.groupby("Customer_Segment", as_index=False).agg(
    Revenue=("Revenue", "sum"), Profit=("Profit", "sum"), Orders=("Order_ID", "nunique")
)
by_segment["Profit_Margin"] = by_segment["Profit"] / by_segment["Revenue"].replace(0, pd.NA)
st.dataframe(by_segment.style.format({
    "Revenue": "${:,.2f}", "Profit": "${:,.2f}", "Profit_Margin": "{:.1%}", "Orders": "{:,.0f}"
}), use_container_width=True, hide_index=True)

st.subheader("Filtered data")
st.caption(f"Showing {len(filtered):,} order lines after applying filters.")
st.dataframe(filtered.drop(columns=["Month"], errors="ignore"), use_container_width=True, hide_index=True)

csv_bytes = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download filtered data (CSV)", data=csv_bytes, file_name="salespulse_filtered_data.csv",
                   mime="text/csv")

with st.expander("Metric definitions"):
    st.markdown("""
    - **Revenue:** sum of the revenue column after discounts.
    - **Profit:** sum of the sample profit values.
    - **Profit margin:** total profit divided by total revenue.
    - **Orders:** distinct order IDs in the filtered data.
    - **Average order value:** total revenue divided by distinct order IDs.
    - **Quantity:** total units represented by the filtered order lines.
    """)

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "sales_data.csv"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

df = pd.read_csv(DATA, parse_dates=["Order_Date"])
print("=== SALES PULSE DATA QUALITY CHECK ===")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"Duplicate rows: {df.duplicated().sum()}")
print(f"Missing cells: {int(df.isna().sum().sum())}")
print(f"Date range: {df['Order_Date'].min().date()} to {df['Order_Date'].max().date()}")

df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)
kpis = pd.DataFrame([{
    "Total_Revenue": df["Revenue"].sum(),
    "Total_Profit": df["Profit"].sum(),
    "Profit_Margin": df["Profit"].sum() / df["Revenue"].sum(),
    "Orders": df["Order_ID"].nunique(),
    "Average_Order_Value": df["Revenue"].sum() / df["Order_ID"].nunique(),
    "Units_Sold": df["Quantity"].sum(),
}])
kpis.to_csv(REPORTS / "overall_kpis.csv", index=False)

for column, filename in [
    ("Region", "region_summary.csv"),
    ("Category", "category_summary.csv"),
    ("Customer_Segment", "segment_summary.csv"),
    ("Product", "product_summary.csv"),
]:
    summary = df.groupby(column, as_index=False).agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order_ID", "nunique"),
        Units_Sold=("Quantity", "sum"),
    )
    summary["Profit_Margin"] = summary["Profit"] / summary["Revenue"].replace(0, pd.NA)
    summary.sort_values("Revenue", ascending=False).to_csv(REPORTS / filename, index=False)

monthly = df.groupby("Month", as_index=False).agg(
    Revenue=("Revenue", "sum"),
    Profit=("Profit", "sum"),
    Orders=("Order_ID", "nunique"),
)
monthly.to_csv(REPORTS / "monthly_summary.csv", index=False)

print("\n=== OVERALL KPIs ===")
print(kpis.to_string(index=False, formatters={
    "Total_Revenue": "${:,.2f}".format,
    "Total_Profit": "${:,.2f}".format,
    "Profit_Margin": "{:.1%}".format,
    "Average_Order_Value": "${:,.2f}".format,
}))
print("\n=== TOP 5 PRODUCTS BY REVENUE ===")
print(pd.read_csv(REPORTS / "product_summary.csv").head(5).to_string(index=False))
print(f"\nSummary CSV files saved to: {REPORTS}")

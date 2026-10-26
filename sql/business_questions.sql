-- SalesPulse: SQL business questions
-- SQLite-compatible examples. Load data/sales_data.csv into a table named sales.
-- Column names in this dataset use underscores and are case-insensitive in SQLite.

-- 1. Overall KPIs
SELECT
    ROUND(SUM(Revenue), 2) AS total_revenue,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(100.0 * SUM(Profit) / NULLIF(SUM(Revenue), 0), 2) AS profit_margin_pct,
    COUNT(DISTINCT Order_ID) AS orders,
    ROUND(SUM(Revenue) / NULLIF(COUNT(DISTINCT Order_ID), 0), 2) AS average_order_value
FROM sales;

-- 2. Monthly revenue and profit trend
SELECT
    strftime('%Y-%m', Order_Date) AS month,
    ROUND(SUM(Revenue), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit
FROM sales
GROUP BY strftime('%Y-%m', Order_Date)
ORDER BY month;

-- 3. Revenue and profit by region
SELECT
    Region,
    ROUND(SUM(Revenue), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    ROUND(100.0 * SUM(Profit) / NULLIF(SUM(Revenue), 0), 2) AS profit_margin_pct
FROM sales
GROUP BY Region
ORDER BY revenue DESC;

-- 4. Category performance
SELECT
    Category,
    ROUND(SUM(Revenue), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    SUM(Quantity) AS units_sold
FROM sales
GROUP BY Category
ORDER BY revenue DESC;

-- 5. Top 10 products by revenue
SELECT Product, ROUND(SUM(Revenue), 2) AS revenue, ROUND(SUM(Profit), 2) AS profit
FROM sales
GROUP BY Product
ORDER BY revenue DESC
LIMIT 10;

-- 6. Customer segment performance
SELECT
    Customer_Segment,
    COUNT(DISTINCT Order_ID) AS orders,
    ROUND(SUM(Revenue), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit
FROM sales
GROUP BY Customer_Segment
ORDER BY revenue DESC;

-- 7. Discount bands and profit margin
SELECT
    CASE
        WHEN Discount = 0 THEN '0%'
        WHEN Discount <= 0.10 THEN '1-10%'
        WHEN Discount <= 0.20 THEN '11-20%'
        ELSE '21-25%'
    END AS discount_band,
    COUNT(*) AS order_lines,
    ROUND(SUM(Revenue), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    ROUND(100.0 * SUM(Profit) / NULLIF(SUM(Revenue), 0), 2) AS profit_margin_pct
FROM sales
GROUP BY discount_band
ORDER BY MIN(Discount);

-- 8. Products with positive revenue but negative total profit
SELECT Product, ROUND(SUM(Revenue), 2) AS revenue, ROUND(SUM(Profit), 2) AS profit
FROM sales
GROUP BY Product
HAVING SUM(Revenue) > 0 AND SUM(Profit) < 0
ORDER BY profit;

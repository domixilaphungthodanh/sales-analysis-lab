-- Monthly revenue (VND), completed orders only.
SELECT strftime('%Y-%m', order_date) AS month,
       SUM(revenue_vnd) AS revenue_vnd,
       COUNT(DISTINCT order_id) AS orders
FROM sales GROUP BY month ORDER BY month;

-- Product ranking: revenue and units are different measures.
SELECT product_name, category, SUM(revenue_vnd) AS revenue_vnd,
       SUM(quantity) AS units
FROM sales GROUP BY product_name, category ORDER BY revenue_vnd DESC;

-- Average order value: aggregate line items before calculating the average.
WITH order_totals AS (
    SELECT order_id, SUM(revenue_vnd) AS total_vnd
    FROM sales GROUP BY order_id
)
SELECT COUNT(*) AS completed_orders, AVG(total_vnd) AS average_order_value_vnd
FROM order_totals;

-- Monthly change using a window function.
WITH monthly AS (
    SELECT strftime('%Y-%m', order_date) AS month, SUM(revenue_vnd) AS revenue
    FROM sales GROUP BY month
), previous AS (
    SELECT *, LAG(revenue) OVER (ORDER BY month) AS previous_revenue FROM monthly
)
SELECT month, revenue,
       ROUND(100.0 * (revenue - previous_revenue) / NULLIF(previous_revenue, 0), 2) AS growth_pct
FROM previous ORDER BY month;

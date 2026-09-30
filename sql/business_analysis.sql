-- Business Analysis SQL Pack
-- Assumed table: sales_orders

SELECT SUM(revenue) AS total_revenue,
       SUM(profit) AS total_profit,
       COUNT(DISTINCT order_id) AS total_orders,
       SUM(profit) / NULLIF(SUM(revenue), 0) AS profit_margin
FROM sales_orders;

SELECT region,
       SUM(revenue) AS revenue,
       SUM(profit) AS profit,
       SUM(profit) / NULLIF(SUM(revenue), 0) AS profit_margin
FROM sales_orders
GROUP BY region
ORDER BY revenue DESC;

SELECT category,
       SUM(revenue) AS revenue,
       SUM(profit) AS profit
FROM sales_orders
GROUP BY category
ORDER BY profit DESC;

SELECT DATE_TRUNC('month', order_date) AS month,
       SUM(revenue) AS revenue,
       SUM(profit) AS profit
FROM sales_orders
GROUP BY 1
ORDER BY 1;

SELECT customer_id,
       SUM(revenue) AS revenue,
       SUM(profit) AS profit,
       COUNT(DISTINCT order_id) AS orders
FROM sales_orders
GROUP BY customer_id
ORDER BY revenue DESC
LIMIT 20;

CREATE VIEW v_customer_clv AS
SELECT
    r.customer_id,
    r.total_revenue,
    ROUND(
        r.total_revenue /
        ((julianday('now') - julianday(c.customer_since)) / 365.0),
        2
    ) AS annual_revenue,
    ROUND(
        (
            r.total_revenue /
            ((julianday('now') - julianday(c.customer_since)) / 365.0)
        ) * 5,
        2
    ) AS estimated_clv
FROM v_customer_revenue r
JOIN customers c 
    ON r.customer_id = c.customer_id
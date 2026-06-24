CREATE VIEW v_early_warning_customers AS
SELECT
    a.customer_id,
    a.account_id,
    ROUND(a.current_balance / a.credit_limit, 2) AS utilization_ratio,
    r.avg_days_late,
    CASE
        WHEN (a.current_balance / a.credit_limit) > 0.8
             AND r.avg_days_late > 15
        THEN 1
        ELSE 0
    END AS early_warning_flag
FROM accounts a
JOIN v_customer_risk r
    ON a.customer_id = r.customer_id
WHERE a.credit_limit IS NOT NULL
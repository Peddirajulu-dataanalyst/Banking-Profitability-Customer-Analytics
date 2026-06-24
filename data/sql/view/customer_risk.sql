CREATE VIEW v_customer_risk AS
SELECT 
    a.customer_id,
    AVG(p.days_late) AS avg_days_late,
    SUM(p.default_flag) AS total_defaults
FROM payments p
JOIN accounts a 
    ON p.account_id = a.account_id
GROUP BY a.customer_id
CREATE VIEW v_value_risk_segment AS
SELECT
    r.customer_id,
    r.total_revenue,
    k.avg_days_late,
    k.total_defaults,
    CASE
        WHEN r.total_revenue >= (
            SELECT AVG(total_revenue) FROM v_customer_revenue
        )
        AND k.avg_days_late <= 10
        THEN 'High Value - Low Risk'

        WHEN r.total_revenue < (
            SELECT AVG(total_revenue) FROM v_customer_revenue
        )
        AND k.avg_days_late > 15
        THEN 'Low Value - High Risk'

        ELSE 'Medium Segment'
    END AS customer_segment
FROM v_customer_revenue r
JOIN v_customer_risk k 
    ON r.customer_id = k.customer_id
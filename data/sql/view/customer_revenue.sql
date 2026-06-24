CREATE VIEW v_customer_revenue AS
SELECT 
    c.customer_id,
    SUM(
        CASE 
            WHEN a.account_type = 'credit_card'
                 AND t.transaction_type = 'debit'
                 THEN t.amount * 0.02
            WHEN a.account_type = 'loan'
                 THEN a.current_balance * (a.interest_rate / 100.0)
            ELSE 0
        END
    ) AS total_revenue
FROM customers c
JOIN accounts a 
    ON c.customer_id = a.customer_id
LEFT JOIN transactions t 
    ON a.account_id = t.account_id
GROUP BY c.customer_id
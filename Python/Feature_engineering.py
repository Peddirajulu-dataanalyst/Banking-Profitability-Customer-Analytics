# ---------------------------------------------------
# Bank Profitability SQL + Risk Segmentation Pipeline
# ---------------------------------------------------

import sqlite3
import pandas as pd
import numpy as np
import os

# Paths
DB_PATH   = r"D:\python project files\bank profitbility\data\sql\banking.db"
SCHEMA    = r"D:\python project files\bank profitbility\sql\schema.sql"
RAW_PATH  = r"D:\python project files\bank profitbility\data\Raw"
PROC_PATH = r"D:\python project files\bank profitbility\data\Processsed"

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(PROC_PATH, exist_ok=True)

def run_feature_engineering():
    # -----------------------------
    # Step 1: Create schema
    # -----------------------------
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA, "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("✅ Schema created")

    # -----------------------------
    # Step 2: Load raw CSVs into DB
    # -----------------------------
    conn = sqlite3.connect(DB_PATH)
    pd.read_csv(os.path.join(RAW_PATH,"customers.csv")).to_sql("customers", conn, if_exists="append", index=False)
    pd.read_csv(os.path.join(RAW_PATH,"accounts.csv")).to_sql("accounts", conn, if_exists="append", index=False)
    pd.read_csv(os.path.join(RAW_PATH,"transactions.csv")).to_sql("transactions", conn, if_exists="append", index=False)
    pd.read_csv(os.path.join(RAW_PATH,"payments.csv")).to_sql("payments", conn, if_exists="append", index=False)

    print(pd.read_sql("select count(*) as customers from customers", conn))
    print(pd.read_sql("select count(*) as accounts from accounts", conn))
    print(pd.read_sql("select count(*) as transactions from transactions", conn))
    print(pd.read_sql("select count(*) as payments from payments", conn))

    # -----------------------------
    # Step 3: Revenue calculation
    # -----------------------------
    df = pd.read_sql("""
    select
    c.customer_id,
    c.region,
    sum(case when a.account_type = 'credit_card' and t.transaction_type = 'debit' then t.amount * 0.02
             when a.account_type = 'loan' then a.current_balance * (a.interest_rate/100)
             else 0 end) as total_revenue
    from customers c
    join accounts a on c.customer_id = a.customer_id
    left join transactions t on a.account_id = t.account_id
    group by c.customer_id
    """, conn)

    # -----------------------------
    # Step 4: Risk metrics
    # -----------------------------
    risk = pd.read_sql("""
    select 
    a.customer_id,
    avg(p.days_late) as avg_days_late,
    sum(p.default_flag) as total_defaults,
    count(p.default_flag) as total_payment_records
    from payments p 
    join accounts a on p.account_id = a.account_id
    group by a.customer_id
    """, conn)
    conn.close()

    df = df.merge(risk, on="customer_id", how="left")
    df.fillna(0, inplace=True)

    # -----------------------------
    # Step 5–9: Risk segmentation
    # -----------------------------
    df["default_rate"] = np.where(df["total_payment_records"] > 0,
                                  df["total_defaults"]/df["total_payment_records"],0)
    df["risk_adjusted_revenue"] = df["total_revenue"] * (1 - df["default_rate"])

    df["risk_segment"] = np.where((df["avg_days_late"] > 10) | (df["total_defaults"] > 0),
                                  "High Risk","Low Risk")

    df["estimated_clv"] = df["total_revenue"] * 3

    df["customer_type"] = np.select(
        [(df["estimated_clv"] >= df["estimated_clv"].median()) & (df["risk_segment"] == "Low Risk"),
         (df["estimated_clv"] >= df["estimated_clv"].median()) & (df["risk_segment"] == "High Risk")],
        ["High value - safe","High value - Risky"],
        default="Low Value"
    )

    df["early_warning"] = np.where((df["avg_days_late"] > 5) & (df["total_defaults"] == 0),1,0)

    # -----------------------------
    # Step 10: Save processed file
    # -----------------------------
    out_file = os.path.join(PROC_PATH,"revenue_data.csv")
    df.to_csv(out_file, index=False)
    print("✅ Processed revenue data saved:", out_file)

    return df

# -----------------------------
# Runner
# -----------------------------
if __name__=="__main__":
    run_feature_engineering()

# ---------------------------------------------------
# Bank Profitability Data Generation
# ---------------------------------------------------

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

RAW_PATH = r"D:\python project files\bank profitbility\data\Raw"
os.makedirs(RAW_PATH, exist_ok=True)

def generate_customers(n_customers=5000):
    customer_ids = np.arange(100001, 100001 + n_customers)
    customers = pd.DataFrame({
        "customer_id": customer_ids,
        "age": np.random.randint(22, 66, n_customers),
        "gender": np.random.choice(["Male","Female"], n_customers),
        "region": np.random.choice(
            ["Ontario","Quebec","British Columbia","Alberta"],
            n_customers,
            p=[0.38,0.23,0.22,0.17]
        ),
        "employment_status": np.random.choice(
            ["Salaried","Self-Employed","Unemployed"],
            n_customers,
            p=[0.7,0.25,0.05]
        ),
        "income": np.random.normal(75000,25000,n_customers).clip(25000,200000).round(0),
        "customer_since": [
            datetime.now() - timedelta(days=np.random.randint(365,3650))
            for _ in range(n_customers)
        ]
    })
    customers["credit_score"] = (
        550 + (customers["income"]/200000)*300 + np.random.normal(0,30,n_customers)
    ).clip(300,900).round(0)
    customers.to_csv(os.path.join(RAW_PATH,"customers.csv"), index=False)
    print("✅ Customers generated")
    return customers

def generate_accounts(customers):
    account_rows = []
    account_id = 200001
    for _, row in customers.iterrows():
        n_accounts = np.random.choice([1, 2, 3], p=[0.4, 0.4, 0.2])
        for _ in range(n_accounts):
            acc_type = np.random.choice(["savings","credit_card","loan"], p=[0.4,0.4,0.2])
            if acc_type != "savings" and row["credit_score"] < 600:
                acc_type = "savings"
            credit_limit, interest_rate = None, None
            if acc_type == "credit_card":
                credit_limit = np.random.choice([5000,10000,20000,30000])
                interest_rate = round(np.random.uniform(15,22),2)
                balance = np.random.uniform(0.2,0.9)*credit_limit
            elif acc_type == "loan":
                credit_limit = np.random.choice([20000,50000,100000])
                interest_rate = round(np.random.uniform(6,12),2)
                balance = np.random.uniform(0.4,1.0)*credit_limit
            else:
                balance = np.random.uniform(500,50000)
            account_rows.append([
                account_id,row["customer_id"],acc_type,
                datetime.now()-timedelta(days=np.random.randint(30,3000)),
                interest_rate,credit_limit,round(balance,2)
            ])
            account_id += 1
    accounts = pd.DataFrame(account_rows,columns=[
        "account_id","customer_id","account_type","open_date",
        "interest_rate","credit_limit","current_balance"
    ])
    accounts.to_csv(os.path.join(RAW_PATH,"accounts.csv"), index=False)
    print("✅ Accounts generated")
    return accounts

def generate_transactions(accounts):
    transaction_rows = []
    transaction_id = 300001
    merchant_categories = ["Grocery","Fuel","Dining","Travel","E-commerce","Utilities","Healthcare","Entertainment","Salary","Transfer"]
    for _, acc in accounts.iterrows():
        if acc["account_type"]=="loan": continue
        n_txn = np.random.randint(80,180) if acc["account_type"]=="credit_card" else np.random.randint(30,90)
        for _ in range(n_txn):
            txn_date = datetime.now()-timedelta(days=np.random.randint(1,365))
            if acc["account_type"]=="credit_card":
                txn_type="debit"
                category=np.random.choice(merchant_categories[:-2],p=[0.18,0.12,0.16,0.08,0.18,0.1,0.08,0.1])
                amount=round(np.random.uniform(10,500),2)
            else:
                txn_type=np.random.choice(["credit","debit"],p=[0.65,0.35])
                if txn_type=="credit":
                    category=np.random.choice(["Salary","Transfer"],p=[0.7,0.3])
                    amount=round(np.random.uniform(1000,6000),2)
                else:
                    category=np.random.choice(merchant_categories[:-2],p=[0.22,0.15,0.12,0.05,0.18,0.15,0.08,0.05])
                    amount=round(np.random.uniform(20,300),2)
            transaction_rows.append([transaction_id,acc["account_id"],txn_date,amount,txn_type,category])
            transaction_id+=1
    transactions=pd.DataFrame(transaction_rows,columns=["transaction_id","account_id","transaction_date","amount","transaction_type","merchant_category"])
    transactions.to_csv(os.path.join(RAW_PATH,"transactions.csv"),index=False)
    print("✅ Transactions generated")
    return transactions

def generate_payments(accounts,customers):
    payment_rows=[]
    accounts_risk=accounts.merge(customers[["customer_id","credit_score"]],on="customer_id",how="left")
    for _,acc in accounts_risk.iterrows():
        if acc["account_type"] not in ["credit_card","loan"]: continue
        for m in range(12):
            due_date=datetime.now()-timedelta(days=30*m)
            if acc["credit_score"]<580: default_prob=0.25
            elif acc["credit_score"]<650: default_prob=0.12
            elif acc["credit_score"]<750: default_prob=0.05
            else: default_prob=0.02
            default_flag=np.random.rand()<default_prob
            if default_flag:
                days_late=np.random.randint(30,120); amount_paid=np.random.uniform(0,0.5)
            else:
                days_late=np.random.choice([0,5,10],p=[0.85,0.1,0.05]); amount_paid=np.random.uniform(0.9,1.0)
            amount_due=(acc["current_balance"]*0.05 if acc["account_type"]=="credit_card" else acc["credit_limit"]*0.01)
            payment_rows.append([acc["account_id"],due_date,due_date+timedelta(days=int(days_late)),round(amount_due,2),round(amount_due*amount_paid,2),
            days_late,int(default_flag)])
    payments=pd.DataFrame(payment_rows,columns=["account_id","due_date","payment_date","amount_due","amount_paid","days_late","default_flag"])
    payments.to_csv(os.path.join(RAW_PATH,"payments.csv"),index=False)
    print("✅ Payments generated")
    return payments

# -----------------------------
# Runner
# -----------------------------
def run_generation():
    customers = generate_customers()
    accounts = generate_accounts(customers)
    transactions = generate_transactions(accounts)
    payments = generate_payments(accounts,customers)
    print("🎯 Data generation completed successfully")

if __name__=="__main__":
    run_generation()

# ---------------------------------------------------
# Bank Profitability Data Cleaning
# ---------------------------------------------------

import pandas as pd
import os

RAW_PATH   = r"D:\python project files\bank profitbility\data\Raw"
CLEAN_PATH = r"D:\python project files\bank profitbility\data\Cleaned data"

os.makedirs(CLEAN_PATH, exist_ok=True)

def clean_file(filename):
    df = pd.read_csv(os.path.join(RAW_PATH, filename))
    df = df.drop_duplicates()
    df = df.dropna()
    # Example type fixes
    if "customer_since" in df.columns:
        df["customer_since"] = pd.to_datetime(df["customer_since"], errors="coerce")
    if "open_date" in df.columns:
        df["open_date"] = pd.to_datetime(df["open_date"], errors="coerce")
    df.to_csv(os.path.join(CLEAN_PATH, f"clean_{filename}"), index=False)
    print(f"✅ Cleaned {filename} saved")

def run_cleaning():
    for fname in ["customers.csv","accounts.csv","transactions.csv","payments.csv"]:
        clean_file(fname)
    print("🎯 Data cleaning completed successfully")

if __name__=="__main__":
    run_cleaning()

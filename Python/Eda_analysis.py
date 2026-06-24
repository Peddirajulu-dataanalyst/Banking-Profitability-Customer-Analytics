# ---------------------------------------------------
# Bank Profitability EDA Pipeline
# ---------------------------------------------------

import os
import seaborn as sns
import matplotlib.pyplot as plt

# Paths
EDA_FOLDER = r"D:\python project files\bank profitbility\data\eda"
os.makedirs(EDA_FOLDER, exist_ok=True)

def run_eda(df):
    # -----------------------------
    # Scatterplot: Revenue vs Risk
    # -----------------------------
    plt.figure(figsize=(8,6))
    sns.scatterplot(data=df, x='total_revenue', y='avg_days_late', hue='risk_segment')
    plt.title("Revenue vs Risk Trade-off")
    plt.savefig(os.path.join(EDA_FOLDER, "revenue_vs_risk.png"))
    plt.close()

    # -----------------------------
    # Countplot: Customer Type
    # -----------------------------
    plt.figure(figsize=(8,6))
    sns.countplot(data=df, x='customer_type')
    plt.title("Customer Value vs Risk Segments")
    plt.xticks(rotation=20)
    plt.savefig(os.path.join(EDA_FOLDER, "customer_type_distribution.png"))
    plt.close()

    # -----------------------------
    # Countplot: Early Warning
    # -----------------------------
    plt.figure(figsize=(6,5))
    sns.countplot(data=df, x='early_warning')
    plt.title("Early Warning Signal Distribution")
    plt.savefig(os.path.join(EDA_FOLDER, "early_warning_distribution.png"))
    plt.close()

    print("✅ EDA plots saved in:", EDA_FOLDER)

# -----------------------------
# Runner
# -----------------------------
if __name__ == "__main__":
    # Example: load processed revenue data
    import pandas as pd
    df = pd.read_csv(r"D:\python project files\bank profitbility\data\Processsed\revenue_data.csv")
    run_eda(df)

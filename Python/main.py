# ---------------------------------------------------
# Master Bank Profitability Pipeline Runner
# ---------------------------------------------------

import logging
import os

# Import functions from your four scripts
from Data_generation import run_generation
from Data_cleaning import run_cleaning
from Feature_engineering import run_feature_engineering
from Eda_analysis import run_eda

# Configure logging
LOG_FILE = r"D:\python project files\bank profitbility\data\pipeline.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    logging.info("🚀 Pipeline Started")

    # Step 1: Data Generation
    run_generation()
    logging.info("Data generation completed")

    # Step 2: Data Cleaning
    run_cleaning()
    logging.info("Data cleaning completed")

    # Step 3: SQL + Risk Segmentation
    run_feature_engineering()
    logging.info("SQL + Risk segmentation completed")

    # Step 4: EDA Visualization
    run_eda(df)
    logging.info("EDA visualization completed")

    logging.info("✅ Full pipeline finished successfully")
    print("🎯 Project completed successfully")

# -----------------------------
# Runner
# -----------------------------
if __name__ == "__main__":
    main()

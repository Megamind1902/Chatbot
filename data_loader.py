import os
import pandas as pd
from typing import Dict, Any, Optional

DEFAULT_CSV_PATHS = [
    "Analytics_loan_collection_dataset.csv",  # uploaded path
]

def _read_first_existing(paths):
    for p in paths:
        if os.path.exists(p):
            try:
                return pd.read_csv(p)
            except Exception:
                pass
    return None

def load_customer_profile(customer_id: Optional[int]) -> Dict[str, Any]:
    """
    Loads a customer's row from CSV by CustomerID.
    Falls back to a demo profile if not found or CSV missing.
    """
    df = _read_first_existing(DEFAULT_CSV_PATHS)
    if df is not None and customer_id is not None and "CustomerID" in df.columns:
        row = df[df["CustomerID"] == customer_id]
        if not row.empty:
            return row.iloc[0].to_dict()

    # Fallback demo profile
    return {
        "CustomerID": customer_id or 9999,
        "Name": "Customer",
        "Age": 32,
        "Income": 650000,
        "Location": "Urban",
        "EmploymentStatus": "Salaried",
        "LoanAmount": 250000,
        "TenureMonths": 18,
        "InterestRate": 13.5,
        "LoanType": "Personal",
        "MissedPayments": 1,
        "DelaysDays": 12,
        "PartialPayments": 0,
        "InteractionAttempts": 2,
        "SentimentScore": -0.1,
        "ResponseTimeHours": 30,
        "AppUsageFrequency": 6,
        "WebsiteVisits": 3,
        "Complaints": 0,
        "Target": 1,  # likely to miss
        "Outstanding": 18500,
        "NameFallback": "Customer"
    }

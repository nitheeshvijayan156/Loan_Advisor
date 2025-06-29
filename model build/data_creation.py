import json
import random
import pandas as pd
from typing import List, Dict

# ----------------------------
# Load Lenders Dataset
# ----------------------------

LENDERS = [
    {
        "id": 1, "name": "FastCash Inc.", "minLoanAmount": 1000, "maxLoanAmount": 5000,
        "minIncome": 20000, "employmentTypes": ["salaried", "self-employed"],
        "minCreditScore": 600, "interestRate": 12.5
    },
    {
        "id": 2, "name": "HomeFund Bank", "minLoanAmount": 50000, "maxLoanAmount": 500000,
        "minIncome": 50000, "employmentTypes": ["salaried"],
        "minCreditScore": 700, "interestRate": 8.9, "loanPurpose": "home"
    },
    {
        "id": 3, "name": "EduFinance", "minLoanAmount": 10000, "maxLoanAmount": 200000,
        "minIncome": 0, "employmentTypes": ["student"],
        "minCreditScore": 0, "interestRate": 6.5, "loanPurpose": "education"
    },
    {
        "id": 4, "name": "BizGrow Capital", "minLoanAmount": 25000, "maxLoanAmount": 1000000,
        "minIncome": 100000, "employmentTypes": ["self-employed"],
        "minCreditScore": 650, "interestRate": 10.5, "loanPurpose": "business"
    },
    {
        "id": 5, "name": "QuickPay Loans", "minLoanAmount": 500, "maxLoanAmount": 10000,
        "minIncome": 15000, "employmentTypes": ["salaried", "freelancer", "self-employed"],
        "minCreditScore": 580, "interestRate": 13.0
    },
    {
        "id": 6, "name": "CarCredit Bank", "minLoanAmount": 30000, "maxLoanAmount": 200000,
        "minIncome": 25000, "employmentTypes": ["salaried"],
        "minCreditScore": 660, "interestRate": 9.5, "loanPurpose": "vehicle"
    },
    {
        "id": 7, "name": "PersonalTrust", "minLoanAmount": 10000, "maxLoanAmount": 50000,
        "minIncome": 20000, "employmentTypes": ["salaried", "self-employed"],
        "minCreditScore": 620, "interestRate": 11.2
    },
    {
        "id": 8, "name": "StartupFund", "minLoanAmount": 50000, "maxLoanAmount": 1000000,
        "minIncome": 0, "employmentTypes": ["self-employed"],
        "minCreditScore": 0, "interestRate": 12.0, "loanPurpose": "startup"
    },
    {
        "id": 9, "name": "StudentLend", "minLoanAmount": 5000, "maxLoanAmount": 50000,
        "minIncome": 0, "employmentTypes": ["student"],
        "minCreditScore": 550, "interestRate": 7.0, "loanPurpose": "education"
    },
    {
        "id": 10, "name": "HouseEasy", "minLoanAmount": 100000, "maxLoanAmount": 1000000,
        "minIncome": 75000, "employmentTypes": ["salaried", "self-employed"],
        "minCreditScore": 720, "interestRate": 8.5, "loanPurpose": "home"
    },
    {
        "id": 11, "name": "FreelanceFlex", "minLoanAmount": 5000, "maxLoanAmount": 30000,
        "minIncome": 20000, "employmentTypes": ["freelancer"],
        "minCreditScore": 600, "interestRate": 12.7
    },
    {
        "id": 12, "name": "WomenEmpower Finance", "minLoanAmount": 10000, "maxLoanAmount": 100000,
        "minIncome": 10000, "employmentTypes": ["salaried", "self-employed"],
        "minCreditScore": 600, "interestRate": 9.8, "specialEligibility": "women"
    },
    {
        "id": 13, "name": "GreenLoan Co.", "minLoanAmount": 5000, "maxLoanAmount": 100000,
        "minIncome": 15000, "employmentTypes": ["salaried", "self-employed"],
        "minCreditScore": 640, "interestRate": 10.1, "loanPurpose": "eco"
    },
    {
        "id": 14, "name": "EmergencyFund", "minLoanAmount": 1000, "maxLoanAmount": 20000,
        "minIncome": 10000, "employmentTypes": ["any"],
        "minCreditScore": 550, "interestRate": 14.5, "loanPurpose": "emergency"
    },
    {
        "id": 15, "name": "GoldSecure Loans", "minLoanAmount": 25000, "maxLoanAmount": 150000,
        "minIncome": 30000, "employmentTypes": ["salaried", "self-employed"],
        "minCreditScore": 610, "interestRate": 9.2, "loanPurpose": "gold-backed"
    }
]

EMPLOYMENT_TYPES = ["salaried", "self-employed", "freelancer", "student"]
LOAN_PURPOSES = ["home", "education", "business", "vehicle", "startup", "eco", "emergency", "gold-backed"]
GENDERS = ["male", "female"]

# ----------------------------
# Generate a random applicant
# ----------------------------
def generate_applicant():
    return {
        "loan_amount": random.randint(1000, 1000000),
        "annual_income": random.randint(0, 200000),
        "employment_status": random.choice(EMPLOYMENT_TYPES),
        "credit_score": random.randint(500, 800),
        "loan_purpose": random.choice(LOAN_PURPOSES),
        "gender": random.choice(GENDERS)
    }

# ----------------------------
# Match logic for one lender
# ----------------------------
def match_lender(applicant: dict, lender: dict) -> bool:
    if not (lender["minLoanAmount"] <= applicant["loan_amount"] <= lender["maxLoanAmount"]):
        return False
    if applicant["annual_income"] < lender["minIncome"]:
        return False
    if "any" not in lender["employmentTypes"] and applicant["employment_status"] not in lender["employmentTypes"]:
        return False
    if applicant["credit_score"] < lender["minCreditScore"]:
        return False
    if "loanPurpose" in lender and applicant["loan_purpose"] != lender["loanPurpose"]:
        return False
    if lender.get("specialEligibility") == "women" and applicant["gender"] != "female":
        return False
    return True

# ----------------------------
# Main Dataset Generator
# ----------------------------
def generate_dataset(n_samples: int = 10000) -> pd.DataFrame:
    data = []
    for _ in range(n_samples):
        applicant = generate_applicant()
        matched = [1 if match_lender(applicant, lender) else 0 for lender in LENDERS]
        data.append({**applicant, **{f"lender_{i+1}": matched[i] for i in range(len(LENDERS))}})
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_dataset(n_samples=10000)
    df.to_csv("loan_lender_dataset.csv", index=False)
    print("✅ Synthetic dataset saved to loan_lender_dataset.csv")

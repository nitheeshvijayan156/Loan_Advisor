import joblib
import numpy as np
import pandas as pd

# ----------------------------
# Load Model
# ----------------------------
model = joblib.load("loan_lender_model.pkl")
print("✅ Model loaded successfully.")

# ----------------------------
# Lender Info (for explanation)
# ----------------------------
LENDERS = [
    {"id": 1, "name": "FastCash Inc.", "interestRate": 12.5},
    {"id": 2, "name": "HomeFund Bank", "interestRate": 8.9},
    {"id": 3, "name": "EduFinance", "interestRate": 6.5},
    {"id": 4, "name": "BizGrow Capital", "interestRate": 10.5},
    {"id": 5, "name": "QuickPay Loans", "interestRate": 13.0},
    {"id": 6, "name": "CarCredit Bank", "interestRate": 9.5},
    {"id": 7, "name": "PersonalTrust", "interestRate": 11.2},
    {"id": 8, "name": "StartupFund", "interestRate": 12.0},
    {"id": 9, "name": "StudentLend", "interestRate": 7.0},
    {"id": 10, "name": "HouseEasy", "interestRate": 8.5},
    {"id": 11, "name": "FreelanceFlex", "interestRate": 12.7},
    {"id": 12, "name": "WomenEmpower Finance", "interestRate": 9.8},
    {"id": 13, "name": "GreenLoan Co.", "interestRate": 10.1},
    {"id": 14, "name": "EmergencyFund", "interestRate": 14.5},
    {"id": 15, "name": "GoldSecure Loans", "interestRate": 9.2},
]

# ----------------------------
# Collect User Input
# ----------------------------
def collect_input():
    loan_amount = float(input("💰 Enter desired loan amount: "))
    annual_income = float(input("📈 Enter your annual income: "))
    employment_status = input("💼 Employment status [salaried/self-employed/freelancer/student]: ").strip().lower()
    credit_score = int(input("🏦 Enter your credit score (0 if unknown): "))
    loan_purpose = input("🎯 Loan purpose [home/education/business/vehicle/startup/eco/emergency/gold-backed]: ").strip().lower()
    gender = input("👤 Gender [male/female]: ").strip().lower()

    return {
        "loan_amount": loan_amount,
        "annual_income": annual_income,
        "employment_status": employment_status,
        "credit_score": credit_score,
        "loan_purpose": loan_purpose,
        "gender": gender
    }

# ----------------------------
# Get Top 3 Lenders
# ----------------------------
def predict_top_lenders(user_input):
    df = pd.DataFrame([user_input])
    probabilities = model.predict_proba(df)

    lender_scores = []
    for i, lender in enumerate(LENDERS):
        prob_array = probabilities[i]
        
        # Handle single-label and multi-label case
        if isinstance(prob_array, list) or isinstance(prob_array, np.ndarray):
            if isinstance(prob_array[0], (list, np.ndarray)):
                prob = prob_array[0][1]  # for list of list
            else:
                prob = prob_array[1]     # for direct array
        else:
            prob = float(prob_array)

        lender_scores.append((lender["name"], prob, lender["interestRate"]))

    lender_scores.sort(key=lambda x: x[1], reverse=True)
    return lender_scores[:3]


# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    print("\n🔍 Welcome to the Loan Match Predictor 🔍\n")
    user_data = collect_input()
    print("\n⏳ Finding top lender matches...\n")

    top_lenders = predict_top_lenders(user_data)

    print("🎯 Top 3 Lender Matches:\n")
    for idx, (name, score, rate) in enumerate(top_lenders, 1):
        print(f"{idx}. {name}")
        print(f"   ✅ Match Score: {round(score * 100, 2)}%")
        print(f"   💸 Interest Rate: {rate}%")
        print()

    print("📩 Thank you for using the Loan Match Predictor!\n")

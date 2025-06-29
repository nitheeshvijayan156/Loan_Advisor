import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# ----------------------------
# Load Dataset
# ----------------------------
df = pd.read_csv("loan_lender_dataset.csv")

# ----------------------------
# Feature Columns and Labels
# ----------------------------
X = df[["loan_amount", "annual_income", "employment_status", "credit_score", "loan_purpose", "gender"]]
y = df[[f"lender_{i+1}" for i in range(15)]]

# ----------------------------
# Train-Test Split
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ----------------------------
# Column Transformer
# ----------------------------
categorical_features = ["employment_status", "loan_purpose", "gender"]
numeric_features = ["loan_amount", "annual_income", "credit_score"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", "passthrough", numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
)

# ----------------------------
# ML Model Pipeline
# ----------------------------
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42)))
])

# ----------------------------
# Train Model
# ----------------------------
model.fit(X_train, y_train)
print("✅ Model training completed.")

# ----------------------------
# Evaluate Model
# ----------------------------
score = model.score(X_test, y_test)
print(f"📊 Test set accuracy (multi-label): {score:.4f}")

# ----------------------------
# Save Model
# ----------------------------
joblib.dump(model, "loan_lender_model.pkl")
print("💾 Model saved to loan_lender_model.pkl")
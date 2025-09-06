import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import os

MODEL_PATH = "models/expense_model.pkl"

# Train a model on past expenses
def train_model(data_path="data/expenses.csv"):
    df = pd.read_csv(data_path)

    if df.empty:
        return None

    # Convert date to month number (e.g., 2025-09-05 → 9)
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month

    # Group by month → total spend
    monthly = df.groupby("month")["amount"].sum().reset_index()

    X = monthly[["month"]]
    y = monthly["amount"]

    model = LinearRegression()
    model.fit(X, y)

    # Save the model
    if not os.path.exists("models"):
        os.makedirs("models")
    joblib.dump(model, MODEL_PATH)

    return model


# Predict next month's expense
def predict_next_month(data_path="data/expenses.csv"):
    df = pd.read_csv(data_path)

    if df.empty or not os.path.exists(MODEL_PATH):
        return None

    model = joblib.load(MODEL_PATH)

    # Predict for next month
    last_date = pd.to_datetime(df["date"]).max()
    next_month = (last_date.month % 12) + 1
    prediction = model.predict(np.array([[next_month]]))

    return float(prediction[0])

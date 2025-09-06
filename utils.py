import pandas as pd
import os

DATA_PATH = "data/expenses.csv"

# Ensure the data folder and file exist
def init_data():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(DATA_PATH):
        df = pd.DataFrame(columns=["date", "category", "amount"])
        df.to_csv(DATA_PATH, index=False)

# Add a new expense
def add_expense(date, category, amount):
    init_data()
    df = pd.read_csv(DATA_PATH)
    new_expense = {"date": date, "category": category, "amount": amount}
    df = pd.concat([df, pd.DataFrame([new_expense])], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)

# Load all expenses
def load_expenses():
    init_data()
    return pd.read_csv(DATA_PATH)

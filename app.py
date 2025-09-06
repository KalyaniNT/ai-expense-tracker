import streamlit as st
from utils import add_expense, load_expenses
import pandas as pd
import matplotlib.pyplot as plt
from model import train_model, predict_next_month

# --- Page Config ---
st.set_page_config(page_title="AI Expense Tracker", layout="wide")

# --- Custom CSS for styling ---
st.markdown("""
    <style>
    body {background-color: #f0f8ff;}
    .css-1d391kg h1 {color: #ff6600; text-align: center; font-size: 3rem; animation: fadeIn 2s ease-in-out;}
    h2 {font-family: 'Arial', sans-serif; margin-top: 10px;}
    div.stButton > button {background-color: #4CAF50; color: white; font-weight: bold; border-radius: 12px; padding: 10px 24px; transition: all 0.3s ease;}
    div.stButton > button:hover {background-color: #45a049; transform: scale(1.05);}
    .stDataFrame table {border-collapse: collapse; width: 100%;}
    .stDataFrame th {background-color: #ffcc99; color: black; font-weight: bold;}
    .stDataFrame td {background-color: #fff2e6;}
    @keyframes fadeIn {0% {opacity: 0;} 100% {opacity: 1;}}
    .card {background-color: #e6f7ff; padding: 20px; border-radius: 15px; box-shadow: 2px 2px 10px #aaa; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

st.title("💰 AI-Powered Expense Tracker")

# --- Total Monthly Budget ---
if "total_budget" not in st.session_state:
    st.session_state.total_budget = 15000  # default budget

st.markdown("<div class='card'><h2 style='color:#ff6600;'>💰 Set Total Monthly Budget</h2></div>", unsafe_allow_html=True)
st.session_state.total_budget = st.number_input(
    "Enter your total budget for this month (₹):",
    min_value=0,
    value=st.session_state.total_budget,
    step=500
)

# --- Add Expense Form ---
st.markdown("<div class='card'><h2 style='color:#333399;'>➕ Add New Expense</h2></div>", unsafe_allow_html=True)
with st.form("expense_form", clear_on_submit=True):
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"])
    amount_str = st.text_input("Amount (₹)", "")
    amount = None
    if amount_str:
        try:
            amount = float(amount_str)
        except ValueError:
            st.warning("⚠️ Please enter a valid number for Amount.")
    submitted = st.form_submit_button("Add Expense")
    if submitted:
        if amount is not None:
            add_expense(date, category, amount)
            st.success(f"Expense added: {category} - ₹{amount:.2f} on {date}")
        else:
            st.warning("⚠️ Enter a valid Amount before submitting.")

# --- Clear All Expenses ---
st.markdown("<div class='card'><h2 style='color:#ff3333;'>🗑️ Clear All Expenses</h2></div>", unsafe_allow_html=True)
if st.checkbox("I confirm I want to delete all expenses"):
    if st.button("Clear All Expenses"):
        empty_df = pd.DataFrame(columns=["date", "category", "amount"])
        empty_df.to_csv("data/expenses.csv", index=False)
        st.success("✅ All expenses have been cleared!")

# --- Show Expenses ---
st.markdown("<div class='card'><h2 style='color:#0099cc;'>📊 All Expenses</h2></div>", unsafe_allow_html=True)
df = load_expenses()
st.dataframe(df)

# --- Total Spend vs Budget ---
st.markdown("<div class='card'><h2 style='color:#ff6600;'>📊 Monthly Budget Status</h2></div>", unsafe_allow_html=True)
total_spent = df["amount"].sum() if not df.empty else 0
st.metric("Total Spend", f"₹{total_spent:.2f}")
st.metric("Monthly Budget", f"₹{st.session_state.total_budget:.2f}")
progress = min(total_spent / st.session_state.total_budget, 1.0)
st.progress(progress)
if total_spent > st.session_state.total_budget:
    st.warning("⚠️ You have exceeded your monthly budget!")
else:
    st.success(f"✅ Within budget. Remaining: ₹{st.session_state.total_budget - total_spent:.2f}")

# --- Analytics ---
st.markdown("<div class='card'><h2 style='color:#ff6600;'>📈 Expense Analytics</h2></div>", unsafe_allow_html=True)
if not df.empty:
    category_summary = df.groupby("category")["amount"].sum()

    # Bar Chart
    fig, ax = plt.subplots(figsize=(6, 4))
    category_summary.plot(kind="bar", ax=ax, color='coral')
    ax.set_ylabel("Amount (₹)")
    ax.set_title("Spending by Category")
    st.pyplot(fig, use_container_width=True)

    # Pie Chart
    fig2, ax2 = plt.subplots(figsize=(5, 5))
    category_summary.plot.pie(
        autopct='%1.1f%%',
        startangle=90,
        ax=ax2,
        colors=plt.cm.Paired.colors
    )
    ax2.set_ylabel("")
    ax2.set_title("Category-wise Expenses")
    st.pyplot(fig2, use_container_width=True)

# --- AI Prediction ---
st.markdown("<div class='card'><h2 style='color:#9933ff;'>🤖 AI Prediction</h2></div>", unsafe_allow_html=True)
if st.button("Train Model"):
    model = train_model()
    if model:
        st.success("✅ Model trained successfully!")
    else:
        st.warning("⚠️ Not enough data to train the model.")

if st.button("Predict Next Month’s Expense"):
    prediction = predict_next_month()
    if prediction:
        st.info(f"📌 Predicted expense for next month: ₹{prediction:.2f}")
    else:
        st.warning("⚠️ Train the model first or add more data.")

import streamlit as st
import pandas as pd
import json
import os
from datetime import date
import matplotlib.pyplot as plt
import io


# --- Page Config ---
st.set_page_config(page_title="💸 Expense Tracker", layout="centered")
try:
    st.image("expense-track.png")
except FileNotFoundError:
    st.warning("Header image (expenses.png) not found. Please ensure the file is uploaded to the repository.")

st.title("💸 Expense Tracker")
st.markdown("Track your spending, analyze habits, and stay financially fit! 🧾")

st.markdown("""
    <style>
        .stApp {
            background-color: #1e1e1e;
            color: white;
        }
        .css-1d391kg, .css-hxt7ib, .css-1v3fvcr {
            background-color: #2e2e2e !important;
            color: white !important;
        }
        .css-ffhzg2 {
            color: white !important;
        }
        .css-1cpxqw2, .css-1x8cf1d {
            color: white !important;
        }
        input, textarea {
            background-color: #333333 !important;
            color: white !important;
        }
        .stButton > button {
            background-color: #04AA6D;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# --- Load Existing Data ---
data_file = "expenses.json"

if not os.path.exists(data_file):
    with open(data_file, "w") as f:
        json.dump([], f)

with open(data_file, "r") as f:
    expenses = json.load(f)

# --- Add New Expense ---
st.subheader("➕ Add New Expense")
with st.form("expense_form"):
    title = st.text_input("Title (e.g., Groceries, Internet Bill)")
    amount = st.number_input("Amount (PKR)", min_value=0.0, step=0.5)
    category = st.selectbox("Category", ["Food", "Transport", "Bills", "Shopping", "Entertainment", "Other"])
    expense_date = st.date_input("Date", value=date.today())
    submitted = st.form_submit_button("💾 Save Expense")

if submitted:
    if title and amount > 0:
        new_expense = {
            "date": str(expense_date),
            "title": title,
            "amount": amount,
            "category": category
        }
        expenses.append(new_expense)
        with open(data_file, "w") as f:
            json.dump(expenses, f, indent=2)
        st.success("✅ Expense Added Successfully!")
    else:
        st.warning("Please fill all fields correctly.")

# --- Convert to DataFrame ---
df = pd.DataFrame(expenses)

# Define filtered_df with a default empty DataFrame
filtered_df = pd.DataFrame()

if not df.empty:
    df["date"] = pd.to_datetime(df["date"])

    # --- Filter by Date Range ---
    st.subheader("📅 Filter by Date")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=df["date"].min().date())
    with col2:
        end_date = st.date_input("End Date", value=df["date"].max().date())

    filtered_df = df[(df["date"] >= pd.to_datetime(start_date)) & (df["date"] <= pd.to_datetime(end_date))]

    # --- Show Expenses ---
    st.subheader("📋 Expense Records")
    st.dataframe(filtered_df.sort_values("date", ascending=False), use_container_width=True)

    # --- Total Spend ---
    total = filtered_df["amount"].sum()
    st.success(f"💰 Total Spent: PKR {total:,.2f}")

    # --- Category Summary ---
    st.subheader("📊 Expenses by Category")
    cat_summary = filtered_df.groupby("category")["amount"].sum().reset_index()
    st.dataframe(cat_summary)

    # --- Pie Chart ---
    if not cat_summary.empty:
        fig, ax = plt.subplots()
        ax.pie(cat_summary["amount"], labels=cat_summary["category"], autopct='%1.1f%%')
        ax.axis("equal")
        st.subheader("🥧 Expense Distribution")
        st.pyplot(fig)

    # --- Monthly Summary ---
    st.subheader("📆 Monthly Summary")
    filtered_df["month"] = filtered_df["date"].dt.to_period("M").astype(str)
    monthly_summary = filtered_df.groupby("month")["amount"].sum().reset_index()
    st.dataframe(monthly_summary)

    # --- Export Buttons ---
    st.subheader("📤 Export Your Data")

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", csv_data, "expenses.csv", "text/csv")

    # Excel Export
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    filtered_df.to_excel(writer, index=False, sheet_name="Expenses")
    writer.close()
    excel_data = output.getvalue()
    st.download_button("⬇️ Download Excel", excel_data, "expenses.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

else:
    st.info("No expenses recorded yet. Add your first one above! 🚀")

# --- Sidebar Motivation ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2736/2736690.png", width=100)
try:
    st.sidebar.image("expenses.png")
except FileNotFoundError:
    st.sidebar.warning("Sidebar image (expenses.png) not found. Please ensure the file is uploaded.")

st.sidebar.markdown("## 💡 Money Tip")
st.sidebar.info("Track every rupee, and your wallet will thank you! 💰")

# --- Sidebar Category Summary ---
st.sidebar.subheader("📊 Expenses by Category")
if not filtered_df.empty:
    cat_summary = filtered_df.groupby("category")["amount"].sum().reset_index()
    st.sidebar.dataframe(cat_summary)
else:
    st.sidebar.info("No expenses to summarize yet.")

if st.sidebar.button("🧹 Clear All Data"):
    with open("expenses.json", "w") as f:
        json.dump([], f)
    st.sidebar.success("All expense data cleared!")

st.sidebar.markdown("---")
# 📬 Contact Section
st.sidebar.markdown("### 📬 Contact")
st.sidebar.write("📧 [Email Us](mailto:ismailahmedshahpk@gmail.com)")
st.sidebar.write("🔗 [Connect on LinkedIn](https://www.linkedin.com/in/ismail-ahmed-shah-2455b01ba/)")
st.sidebar.write("💬 [Chat on WhatsApp](https://wa.me/923322241405)")
st.sidebar.markdown("---")
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135716.png", width=90, use_container_width=True)
st.sidebar.markdown("---")
st.sidebar.markdown("<p style='text-align: center; color: grey;'>Build with ❤️ By Ismail Ahmed Shah</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")
import os
import streamlit as st
import requests
from datetime import date


API_URL = os.getenv("API_URL", "http://localhost:8000")

st.write("Streamlit app is running")


st.title("💰 AI Expense Tracker")
st.header("Add new Expense")

category = st.text_input("Category")
amount = st.number_input("Amount")
expense_date = st.date_input("Date", value=date.today())
description = st.text_input("Description")


def fetch_expenses():
    try:
        response = requests.get(f"{API_URL}/expenses", timeout=5)
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return []

    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            st.error("Invalid JSON received from API")
            return []
    else:
        st.error(f"Error fetching expenses: {response.status_code} {response.text}")
        return []


if st.button("Add Expense"):
    payload = {
        "category": category,
        "amount": amount,
        "date": str(expense_date),
        "description": description,
    }

    try:
        response = requests.post(f"{API_URL}/add-expense", json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
    else:
        if response.status_code == 200:
            st.success("Expense added successfully!")
        else:
            st.error(f"Error adding expense: {response.status_code} {response.text}")


# st.header("All expenses")

# if st.button("Refresh Expenses"):
#     expenses = fetch_expenses()
#     if expenses:
#         st.table(expenses)

# # show expenses on load
# expenses = fetch_expenses()
# if expenses:
#     st.table(expenses)
# else:
#     st.info("No expenses found.")
st.header("All expenses")

if st.button("Show All Expeses"):
    expenses = fetch_expenses()

    if expenses:
        # remove 'id' column before displaying to the user
        display_expenses = [{k: v for k, v in exp.items() if k != "id"} for exp in expenses]
        st.table(display_expenses)

        # total = sum(exp["amount"] for exp in expenses)
        # st.subheader(f"💰 Total Expense: ₹ {total}")
    else:
        st.info("No expenses found.")



st.header("📊 Expense Summary")

try:
    response = requests.get(f"{API_URL}/expense-summary", timeout=5)

    if response.status_code == 200:
        data = response.json()

        st.write("💰 Total:", data["total"])
        st.bar_chart(data["category_summary"])
    else:
        st.error(f"Error fetching summary: {response.status_code} {response.text}")

except requests.exceptions.RequestException as e:
    st.error(f"Connection error: {e}")




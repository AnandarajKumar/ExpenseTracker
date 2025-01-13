import streamlit as st
import mysql.connector
import pandas as pd
from mysql.connector import Error
import matplotlib.pyplot as plt


def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',        # or your MySQL server IP
            user='root',    # your MySQL username
            password='04051996',  # your MySQL password
            database='expensedb1'  # your database name
        )
        if connection.is_connected():
            st.success("Connected to MySQL server")
    except Error as e:
        st.error(f"Error while connecting to MySQL: {e}")
    return connection


def fetch_data(query):
    connection = create_connection()
    if connection:
        df = pd.read_sql(query, connection)
        connection.close()
        return df
    return None


st.title("Expense Tracker")


if st.button("Show All Expenses"):
    query = "SELECT * FROM expenses"
    data = fetch_data(query)
    if data is not None:
        st.write(data)


st.subheader("Filter by Date Range")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

if st.button("Filter Expenses"):
    filter_query = f"""
    SELECT * FROM expenses
    WHERE Date BETWEEN '{start_date}' AND '{end_date}'
    """
    filtered_data = fetch_data(filter_query)
    if filtered_data is not None and not filtered_data.empty:
        st.write(filtered_data)
    else:
        st.warning("No records found for the selected date range.")


st.subheader("Expense Analysis Queries")


if st.button("Total Expenses"):
    query = "SELECT SUM(Amount) AS Total_Expenses FROM expenses"
    total_expenses = fetch_data(query)
    st.write(total_expenses)


if st.button("Expenses by Category"):
    query = "SELECT Category, SUM(Amount) AS Total_Amount FROM expenses GROUP BY Category"
    category_data = fetch_data(query)
    if category_data is not None:
        st.bar_chart(category_data.set_index('Category'))


if st.button("Average Expense Amount"):
    query = "SELECT AVG(Amount) AS Average_Expense FROM expenses"
    avg_expense = fetch_data(query)
    st.write(avg_expense)


if st.button("Count of Expenses"):
    query = "SELECT COUNT(*) AS Total_Records FROM expenses"
    total_records = fetch_data(query)
    st.write(total_records)


if st.button("Maximum Expense"):
    query = "SELECT MAX(Amount) AS Max_Expense FROM expenses"
    max_expense = fetch_data(query)
    st.write(max_expense)


if st.button("Minimum Expense"):
    query = "SELECT MIN(Amount) AS Min_Expense FROM expenses"
    min_expense = fetch_data(query)
    st.write(min_expense)


if st.button("Expenses by Payment Mode"):
    query = "SELECT Payment_Mode, SUM(Amount) AS Total_Amount FROM expenses GROUP BY Payment_Mode"
    payment_data = fetch_data(query)
    if payment_data is not None:
        st.bar_chart(payment_data.set_index('Payment_Mode'))


if st.button("Monthly Expense Summary"):
    query = "SELECT DATE_FORMAT(Date, '%Y-%m') AS Month, SUM(Amount) AS Total_Amount FROM expenses GROUP BY Month ORDER BY Month"
    monthly_data = fetch_data(query)
    if monthly_data is not None:
        st.line_chart(monthly_data.set_index('Month'))


if st.button("Top 5 Expenses"):
    query = "SELECT * FROM expenses ORDER BY Amount DESC LIMIT 5"
    top_expenses = fetch_data(query)
    st.write(top_expenses)


if st.button("Expenses Over 500"):
    query = "SELECT * FROM expenses WHERE Amount > 500"
    high_expenses = fetch_data(query)
    st.write(high_expenses)


if st.button("Count of Expenses by Category"):
    query = "SELECT Category, COUNT(*) AS Count FROM expenses GROUP BY Category"
    count_data = fetch_data(query)
   
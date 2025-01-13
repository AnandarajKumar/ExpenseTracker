import streamlit as st
import mysql.connector
import pandas as pd
from mysql.connector import Error
import matplotlib.pyplot as plt

# Function to create a connection to the database
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

# Function to fetch data from the database
def fetch_data(query):
    connection = create_connection()
    if connection:
        df = pd.read_sql(query, connection)
        connection.close()
        return df
    return None

# Streamlit app layout
st.title("Expense Tracker")

# 1. Total amount spent in each category
if st.button("Total Amount Spent in Each Category"):
    query = "SELECT Category, SUM(Amount) AS Total_Amount FROM expenses GROUP BY Category"
    category_data = fetch_data(query)
    if category_data is not None:
        st.bar_chart(category_data.set_index('Category'))

# 2. Total amount spent using each payment mode
if st.button("Total Amount Spent by Payment Mode"):
    query = "SELECT Payment_Mode, SUM(Amount) AS Total_Amount FROM expenses GROUP BY Payment_Mode"
    payment_data = fetch_data(query)
    if payment_data is not None:
        st.bar_chart(payment_data.set_index('Payment_Mode'))

# 3. Total cashback received across all transactions
if st.button("Total Cashback Received"):
    query = "SELECT SUM(Cash_back) AS Total_Cash_Back FROM expenses"
    cashback_data = fetch_data(query)
    st.write(cashback_data)

# 4. Top 5 most expensive categories
if st.button("Top 5 Most Expensive Categories"):
    query = "SELECT Category, SUM(Amount) AS Total_Amount FROM expenses GROUP BY Category ORDER BY Total_Amount DESC LIMIT 5"
    top_categories = fetch_data(query)
    st.write(top_categories)

# 5. Spending on transportation using different payment modes
if st.button("Transportation Spending by Payment Mode"):
    query = "SELECT Payment_Mode, SUM(Amount) AS Total_Amount FROM expenses WHERE Category = 'Transport' GROUP BY Payment_Mode"
    transport_data = fetch_data(query)
    if transport_data is not None:
        st.bar_chart(transport_data.set_index('Payment_Mode'))

# 6. Transactions that resulted in cashback
if st.button("Transactions with Cashback"):
    query = "SELECT * FROM expenses WHERE Cash_back > 0"
    cashback_transactions = fetch_data(query)
    st.write(cashback_transactions)

# 7. Total spending in each month of the year
if st.button("Total Spending by Month"):
    query = "SELECT DATE_FORMAT(Date, '%Y-%m') AS Month, SUM(Amount) AS Total_Amount FROM expenses GROUP BY Month ORDER BY Month"
    monthly_spending = fetch_data(query)
    if monthly_spending is not None:
        st.line_chart(monthly_spending.set_index('Month'))

# 8. Months with highest spending in specific categories
if st.button("Highest Spending in Travel, Entertainment, Gifts"):
    query = """
    SELECT DATE_FORMAT(Date, '%Y-%m') AS Month, Category, SUM(Amount) AS Total_Amount 
    FROM expenses 
    WHERE Category IN ('Travel', 'Entertainment', 'Gifts') 
    GROUP BY Month, Category 
    ORDER BY Month, Total_Amount DESC
    """
    specific_category_data = fetch_data(query)
    st.write(specific_category_data)

# 9. Recurring expenses during specific months
if st.button("Recurring Expenses by Month"):
    query = """
    SELECT Category, COUNT(*) AS Count, MONTH(Date) AS Month 
    FROM expenses 
    GROUP BY Category, Month 
    HAVING Count > 1
    """
    recurring_expenses = fetch_data(query)
    st.write(recurring_expenses)
# 10. Cashback or rewards earned in each month
if st.button("Cashback Earned by Month"):
    query = "SELECT DATE_FORMAT(Date, '%Y-%m') AS Month, SUM(Cash_back) AS Total_Cash_Back FROM expenses GROUP BY Month ORDER BY Month"
    cashback_by_month = fetch_data(query)
    if cashback_by_month is not None:
        st.line_chart(cashback_by_month.set_index('Month'))

# 11. Overall spending trend over time
if st.button("Overall Spending Trend"):
    query = "SELECT DATE_FORMAT(Date, '%Y-%m') AS Month, SUM(Amount) AS Total_Amount FROM expenses GROUP BY Month ORDER BY Month"
    spending_trend = fetch_data(query)
    if spending_trend is not None:
        st.line_chart(spending_trend.set_index('Month'))

# 12. Typical costs associated with different types of travel
if st.button("Typical Travel Costs"):
    query = "SELECT Category, AVG(Amount) AS Average_Cost FROM expenses WHERE Category LIKE '%Travel%' GROUP BY Category"
    travel_costs = fetch_data(query)
    if travel_costs is not None:
        st.bar_chart(travel_costs.set_index('Category'))

# 13. Patterns in grocery spending
if st.button("Grocery Spending Patterns"):
    query = """
    SELECT DAYOFWEEK(Date) AS Day, SUM(Amount) AS Total_Amount 
    FROM expenses 
    WHERE Category = 'Food' 
    GROUP BY Day 
    ORDER BY Day
    """
    grocery_patterns = fetch_data(query)
    if grocery_patterns is not None:
        st.bar_chart(grocery_patterns.set_index('Day'))

# 14. Define High and Low Priority Categories
if st.button("High and Low Priority Categories"):
    query = """
    SELECT Category, SUM(Amount) AS Total_Amount 
    FROM expenses 
    GROUP BY Category 
    HAVING Total_Amount > (SELECT AVG(SUM(Amount)) FROM expenses GROUP BY Category) 
    ORDER BY Total_Amount DESC
    """
    high_priority = fetch_data(query)
    st.write("High Priority Categories:")
    st.write(high_priority)

    low_priority_query = """
    SELECT Category, SUM(Amount) AS Total_Amount 
    FROM expenses 
    GROUP BY Category 
    HAVING Total_Amount <= (SELECT AVG(SUM(Amount)) FROM expenses GROUP BY Category) 
    ORDER BY Total_Amount ASC
    """
    low_priority = fetch_data(low_priority_query)
    st.write("Low Priority Categories:")
    st.write(low_priority)

# 15. Category contributing the highest percentage of total spending
if st.button("Category Contributing Highest Percentage"):
    query = """
    SELECT Category, SUM(Amount) AS Total_Amount 
    FROM expenses 
    GROUP BY Category 
    ORDER BY Total_Amount DESC 
    LIMIT 1
    """
    highest_percentage_category = fetch_data(query)
    total_spending_query = "SELECT SUM(Amount) AS Total_Spending FROM expenses"
    total_spending = fetch_data(total_spending_query)
    if highest_percentage_category is not None and total_spending is not None:
        highest_amount = highest_percentage_category['Total_Amount'].values[0]
        total_amount = total_spending['Total_Spending'].values[0]
        percentage = (highest_amount / total_amount) * 100
        st.write(f"Category: {highest_percentage_category['Category'].values[0]} contributes {percentage:.2f}% of total spending.")

# Custom SQL Query Execution
st.subheader("Run Custom SQL Query")
custom_query = st.text_area("Enter your SQL query here:")
if st.button("Execute Query"):
    result = fetch_data(custom_query)
    if result is not None:
        st.write(result)
    else:
        st.error("Failed to execute query.")
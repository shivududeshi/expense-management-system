import streamlit as st
from datetime import datetime
import requests
import pandas as pd

APP_URL="http://localhost:8000"

def analytics_months_tab():
    selected_input_date=st.date_input("Enter Date:",datetime(2024,8,12),label_visibility="collapsed")
    selected_year = selected_input_date.year
    response=requests.get(f"{APP_URL}/expenses/monthwise/{selected_year}")
    if response.status_code==200:
        monthwise_expenses=response.json()
    else:
        st.error("Failed to retrieve expenses")
        monthwise_expenses=[]
    data={
        "Total":[month_expense.get("total_expense") for month_expense in monthwise_expenses],
        "month":[month_expense.get("month") for month_expense in monthwise_expenses]
    }

    df=pd.DataFrame(data)
    df_sorted=df.sort_values(by="month")

    st.title("Expense Breakdown by Months")
    st.bar_chart(data=df_sorted.set_index("month")["Total"],width=0,height=0,use_container_width=5)
    st.table(df_sorted)
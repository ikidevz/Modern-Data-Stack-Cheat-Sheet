import streamlit as st

from components import sidebar
from components.data_cleaning_sql_1 import DataCleaningSQL as sql_1
from components.data_cleaning_sql_2 import DataCleaningSQL as sql_2
from components.data_cleaning_sql_3 import DataCleaningFinanceSQL as sql_3

st.set_page_config(
    page_title="Data Cleaning (SQL)",
    page_icon="🧹",
    layout="wide"
)
sidebar()

st.markdown("""
<style>
    .main { padding: 1rem 2rem; }
    .sql-tip {
        background: transparent;
        border-left: 4px solid #1976d2;
        padding: 0.75rem 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    .best-practice {
        background: transparent;
        border-left: 4px solid #388e3c;
        padding: 0.75rem 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    .warning-box {
        background: transparent;
        border-left: 4px solid #f57c00;
        padding: 0.75rem 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
            

</style>
""", unsafe_allow_html=True)
st.title("🧹 Data Cleaning (SQL) Cheat Sheet Universal Data")
st.markdown("### Universal Data Cleaning Guide - Real Customer Orders Dataset")
st.markdown("*Step-by-step SQL queries with live result visualization*")
st.markdown("---")


pages = {
    'Shipments': sql_1,
    'Customer Orders': sql_2,
    'Transactions': sql_3
}

sql_dataset_page = st.selectbox("Datasets:", list(pages.keys()))

sql_page = pages[sql_dataset_page]()
sql_page.output()

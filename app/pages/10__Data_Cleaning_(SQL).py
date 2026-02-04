import streamlit as st
from components.data_cleaning_sql import DataCleaningSQL

st.set_page_config(
    page_title="Data Cleaning (SQL)",
    page_icon="🧹",
    layout="wide"
)

st.title("🧹 Data Cleaning (SQL) Cheat Sheet Universal Data")
st.markdown("### Universal Data Cleaning Guide - Real Customer Orders Dataset")
st.markdown("*Step-by-step SQL queries with live result visualization*")
st.markdown("---")

data_cleaning_sql = DataCleaningSQL()
data_cleaning_sql.output()

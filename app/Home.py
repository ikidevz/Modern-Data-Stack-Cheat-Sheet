import streamlit as st

from components import sidebar
from utility.seo import inject_seo

st.set_page_config(
    page_title="The Modern Data Stack Cheat Sheet",
    page_icon="📊🧱⚙️",
    layout="wide"
)
inject_seo("/")

st.markdown('<img src="https://tdhghaslnufgtzjybhhf.supabase.co/storage/v1/object/public/resume/moden_data_stack_cheat_sheer_banner.png" alt="main-banner" style="width:100%; object-fit: cover;"/>', unsafe_allow_html=True)
st.title("📊🧱⚙️  The Modern Data Stack Cheat Sheet")
st.caption("Analytics • Engineering • Data System Patterns")

sidebar()

st.divider()

# --------------------------------------------------
# Intro Section
# --------------------------------------------------
st.markdown(
    """
    **The Modern Data Stack Cheat Sheet** is a practical, engineering-first reference
    for **Data Analysts, Analytics Engineers, and Data Engineers**.

    This is not a tutorial.  
    It is a **working knowledge base** of patterns, syntax, and system-level thinking
    across the modern data stack.
    """
)

# --------------------------------------------------
# What You'll Find
# --------------------------------------------------
st.subheader("🧠 What You'll Find Here")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        **📊 Data Analysis & Math**
        - 📈 Data Analysis — EDA, aggregations, and analytical workflows
        - 🔢 Math & Statistics — core statistical concepts and mathematical foundations
        - 🧮 Data Structure & Algorithm — essential structures and algorithmic thinking

        **🐍 Python & DataFrames**
        - 🐼 Pandas — local analytics and data wrangling
        - 🔍 EDA — exploratory data analysis patterns and techniques
        - 🧹 Data Cleaning (Pandas) — cleaning and transforming data in Python

        **🗄️ SQL & Databases**
        - 🧹 Data Cleaning (SQL) — cleaning at the database layer
        - 🐘 PostgreSQL — advanced SQL and relational patterns
        - 🐬 MySQL — queries, joins, and DB management
        """
    )

with col2:
    st.markdown(
        """
        **⚡ Big Data & Processing**
        - 🌀 Polars — columnar, high-performance data processing
        - 🔥 PySpark — distributed big data processing
        - 🧱 Databricks & Delta — Delta Lake patterns and Databricks workflows

        **⚙️ Data Engineering**
        - 🌊 Kafka — event streaming and message queues
        - 🔄 ETL Types — batch, streaming, and hybrid ETL patterns
        - 🛠️ Feature Engineering — feature creation and transformation
        - 🏗️ Data Engineering Patterns — pipeline architecture and best practices
        - 🧩 Design Patterns — software and system design patterns for data

        **🎨 Visualization**
        - 🎨 Data Visualization — charts, plots, and storytelling with data
        """
    )

# --------------------------------------------------
# How to Use This Cheat Sheet
# --------------------------------------------------
st.subheader("🧭 How to Use This Cheat Sheet")

st.markdown(
    """
    - Use the **sidebar** to jump between tools and layers  
    - Treat each page as a **quick reference**, not a walkthrough  
    - Focus on **patterns**, not memorization  
    - Apply what you see directly to **real pipelines and data apps**
    """
)

# --------------------------------------------------
# Footer Note
# --------------------------------------------------
st.divider()

st.caption(
    "Built as a living reference for real-world data systems — not just syntax."
)

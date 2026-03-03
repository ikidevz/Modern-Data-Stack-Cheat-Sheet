import streamlit as st

from components import sidebar

st.set_page_config(
    page_title="The Modern Data Stack Cheat Sheet",
    page_icon="📊🧱⚙️",
    layout="wide"
)

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
        **📊 Data Analysis & Visualization**
        - 📈 Data Analysis — EDA, aggregations, and analytical workflows
        - 🎨 Data Visualization — charts, plots, and storytelling with data

        **🧹 Data Cleaning**
        - 🐼 Data Cleaning (Pandas) — cleaning in Python
        - 🗄️ Data Cleaning (SQL) — cleaning at the database layer

        **🐍 DataFrame & Processing**
        - 🐼 Pandas — local analytics and data wrangling
        - ⚡ Polars — columnar, high-performance processing
        - 🔥 PySpark — distributed big data processing
        """
    )

with col2:
    st.markdown(
        """
        **🗄️ SQL & Databases**
        - 🐘 PostgreSQL — advanced SQL and relational patterns
        - 🐬 MySQL — queries, joins, and DB management

        **⚙️ Data Engineering**
        - 🌊 Kafka — event streaming and message queues
        - 🧱 Design Patterns — architecture and pipeline design patterns
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

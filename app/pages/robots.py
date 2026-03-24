import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Robots.txt", layout="wide")

st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="stToolbar"] {display: none;}
        footer {display: none;}
    </style>
""", unsafe_allow_html=True)

robots_txt = """User-agent: *
Allow: /

# Sitemap location (note: Streamlit-hosted page, not a static file)
Sitemap: https://modern-data-stack-cheat-sheet-ikigami.streamlit.app/sitemap
"""

components.html(f"""
    <pre style="font-family: monospace; font-size: 14px;">{robots_txt}</pre>
""", height=200)

st.subheader("📋 Your robots.txt content")
st.code(robots_txt, language="text")

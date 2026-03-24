import streamlit as st
import streamlit.components.v1 as components

# Hide this page from sidebar
st.set_page_config(page_title="Sitemap", layout="wide")

# Hide sidebar + streamlit UI chrome
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="stToolbar"] {display: none;}
        footer {display: none;}
        .block-container {padding: 0;}
    </style>
""", unsafe_allow_html=True)

BASE = "https://modern-data-stack-cheat-sheet-ikigami.streamlit.app"

PAGES = [
    ("", "1.0", "weekly"),
    ("Data_Analysis", "0.9", "weekly"),
    ("PostgreSQL", "0.9", "weekly"),
    ("MySQL", "0.9", "weekly"),
    ("Pandas", "0.9", "weekly"),
    ("Polaris", "0.8", "weekly"),
    ("PySpark", "0.9", "weekly"),
    ("Kafka", "0.9", "weekly"),
    ("Data_Visualization", "0.8", "weekly"),
    ("Data_Cleaning_(Pandas)", "0.8", "weekly"),
    ("Data_Cleaning_(SQL)", "0.8", "weekly"),
    ("Design_Patterns", "0.8", "weekly"),
    ("ETL_Types", "0.8", "weekly"),
    ("Feature_Engineering", "0.8", "weekly"),
    ("Data_Engineering_Patterns", "0.9", "weekly"),
]

urls = "\n".join([
    f"""  <url>
    <loc>{BASE}/{slug}</loc>
    <priority>{priority}</priority>
    <changefreq>{freq}</changefreq>
  </url>"""
    for slug, priority, freq in PAGES
])

xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>"""

# Render as plain XML in browser
components.html(f"""
    <pre style="font-family: monospace; font-size: 13px; white-space: pre-wrap;">{xml}</pre>
    <script>
        // Tell parent this is XML content
        try {{
            parent.document.contentType = 'application/xml';
        }} catch(e) {{}}
    </script>
""", height=800, scrolling=True)

# Also show copyable version
st.subheader("📋 Your Sitemap XML")
st.caption("Copy this and submit manually to Google Search Console")
st.code(xml, language="xml")

import streamlit as st
import streamlit.components.v1 as components

PAGE_META = {
    "/": {
        "title": "Modern Data Stack Cheat Sheet | SQL, Pandas, PySpark & More",
        "description": "Your all-in-one reference for the modern data stack: SQL, Python, Kafka, ETL, and more.",
    },
    "Data_Analysis": {
        "title": "Data Analysis Cheat Sheet — Pandas, SQL & Python",
        "description": "Quick reference for data analysis techniques using Pandas, SQL, and Python.",
    },
    "PostgreSQL": {
        "title": "PostgreSQL Cheat Sheet — Queries, Functions & Tips",
        "description": "Master PostgreSQL with this concise cheat sheet covering queries, joins, indexes, and functions.",
    },
    "MySQL": {
        "title": "MySQL Cheat Sheet — Commands & Best Practices",
        "description": "Essential MySQL commands, syntax, and best practices for data engineers and developers.",
    },
    "Pandas": {
        "title": "Pandas Cheat Sheet — DataFrames, GroupBy & More",
        "description": "Complete Pandas reference for data manipulation, filtering, merging, and aggregation.",
    },
    "Polaris": {
        "title": "Polars Cheat Sheet — Fast DataFrame Operations",
        "description": "Learn Polars, the blazing-fast DataFrame library for data engineering in Python.",
    },
    "PySpark": {
        "title": "PySpark Cheat Sheet — Big Data with Apache Spark",
        "description": "PySpark quick reference for distributed data processing, transformations, and actions.",
    },
    "Kafka": {
        "title": "Apache Kafka Cheat Sheet — Topics, Producers & Consumers",
        "description": "Essential Kafka concepts, commands, and patterns for data streaming pipelines.",
    },
    "Data_Visualization": {
        "title": "Data Visualization Cheat Sheet — Charts & Graphs",
        "description": "Handy reference for building effective data visualizations with Python and SQL.",
    },
    "Data_Cleaning_(Pandas)": {
        "title": "Data Cleaning with Pandas — Handle Nulls, Duplicates & More",
        "description": "Clean messy data efficiently using Pandas: nulls, duplicates, type casting, and more.",
    },
    "Data_Cleaning_(SQL)": {
        "title": "Data Cleaning with SQL — Queries & Techniques",
        "description": "SQL techniques for cleaning and transforming raw data in relational databases.",
    },
    "Design_Patterns": {
        "title": "Data Engineering Design Patterns — Best Practices",
        "description": "Common design patterns for scalable, maintainable data pipelines and architectures.",
    },
    "ETL_Types": {
        "title": "ETL Types Cheat Sheet — Batch, Streaming & Micro-batch",
        "description": "Understand the different ETL types: batch, streaming, micro-batch, and ELT approaches.",
    },
    "Feature_Engineering": {
        "title": "Feature Engineering Cheat Sheet — ML & Data Science",
        "description": "Feature engineering techniques for machine learning: encoding, scaling, binning, and more.",
    },
    "Data_Engineering_Patterns": {
        "title": "Data Engineering Patterns — Lake, Mesh & Pipeline Designs",
        "description": "Architectural patterns for data engineers: data lake, lakehouse, mesh, and pipeline design.",
    },
    "Databricks": {
        "title": "Delta Lake Cheat Sheet - Best Practices",
        "description": "Building a professional Streamlit cheat sheet app ",
    },
}

BASE_URL = "https://modern-data-stack-cheat-sheet-ikigami.streamlit.app"
# replace with real image URL
OG_IMAGE = "https://tdhghaslnufgtzjybhhf.supabase.co/storage/v1/object/public/resume/moden_data_stack_cheat_sheer_banner.png"


def inject_seo(page_key: str = "/"):
    meta = PAGE_META.get(page_key, PAGE_META["/"])
    title = meta["title"]
    description = meta["description"]
    url = BASE_URL if page_key == "/" else f"{BASE_URL}/{page_key}"

    components.html(f"""
        <script>
            // Inject into parent document (Streamlit iframe workaround)
            try {{

                const setMeta = (name, content, attr="name") => {{
                    let el = parent.document.querySelector(`meta[${{attr}}="${{name}}"]`);
                    if (!el) {{
                        el = parent.document.createElement("meta");
                        el.setAttribute(attr, name);
                        parent.document.head.appendChild(el);
                    }}
                    el.setAttribute("content", content);
                }};

                // Standard
                setMeta("description", "{description}");
                setMeta("keywords", "data engineering, SQL cheat sheet, pandas, pyspark, kafka, ETL, polars, feature engineering, data stack");
                setMeta("robots", "index, follow");

                // Open Graph
                setMeta("og:title", "{title} - Modern Data Stack Cheat Sheet", "property");
                setMeta("og:description", "{description}", "property");
                setMeta("og:url", "{url}", "property");
                setMeta("og:image", "{OG_IMAGE}", "property");
                setMeta("og:type", "website", "property");
                setMeta("og:site_name", "Modern Data Stack Cheat Sheet", "property");

                // Twitter
                setMeta("twitter:card", "summary_large_image");
                setMeta("twitter:title", "{title} - Modern Data Stack Cheat Sheet");
                setMeta("twitter:description", "{description}");
                setMeta("twitter:image", "{OG_IMAGE}");

                // Canonical
                let canonical = parent.document.querySelector('link[rel="canonical"]');
                if (!canonical) {{
                    canonical = parent.document.createElement("link");
                    canonical.setAttribute("rel", "canonical");
                    parent.document.head.appendChild(canonical);
                }}
                canonical.setAttribute("href", "{url}");

            }} catch(e) {{
                console.warn("SEO injection skipped:", e);
            }}
        </script>
    """, height=0)

import streamlit as st
import datetime
from components import sidebar
from utility.seo import inject_seo

st.set_page_config(page_title="Data Model", page_icon="📐", layout="wide")
inject_seo('Data Model')
sidebar()
st.title("📐 Data Model")
st.caption("A reference guide to data modeling concepts, patterns, and examples.")

st.divider()

tab1, tab2 = st.tabs(["📖 Concepts & Theory", "🧩 Examples"])

# ─── TAB 1: Concepts & Theory ───────────────────────────────────────────────
with tab1:

    # ── What is a Data Model ──────────────────────────────────────────────────
    st.subheader("What is a Data Model?")
    st.write(
        """
        A **data model** is an abstract representation that organizes data elements and 
        standardizes how they relate to one another and to the properties of real-world entities. 
        It defines the structure, storage, and retrieval of data in a system.
        """
    )

    st.divider()

    # ── Why It Matters ────────────────────────────────────────────────────────
    st.subheader("Why Data Modeling Matters")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**🎯 Clarity**")
        st.write(
            "Aligns business stakeholders and engineers on what data means and how it flows.")
    with col2:
        st.markdown("**⚡ Performance**")
        st.write(
            "Well-structured models reduce query complexity and improve warehouse efficiency.")
    with col3:
        st.markdown("**🔄 Maintainability**")
        st.write("Clean models are easier to debug, extend, and document over time.")

    st.divider()

    # ── Core Modeling Approaches ──────────────────────────────────────────────
    st.subheader("Core Modeling Approaches")

    with st.expander("🏛️ Kimball (Dimensional Modeling)", expanded=True):
        st.write(
            """
            Developed by Ralph Kimball, this bottom-up approach organizes data into 
            **fact tables** and **dimension tables** designed for fast analytical queries.
            
            - **Fact tables** store measurable events (sales, clicks, transactions)
            - **Dimension tables** store descriptive context (customer, product, date)
            - Data marts are built first, enterprise warehouse emerges from integration
            - Optimized for **end-user readability** and BI tool compatibility
            """
        )
        st.info(
            "Best for: BI-heavy organizations, self-service analytics, fast time-to-value")

    with st.expander("🏗️ Inmon (Corporate Information Factory)"):
        st.write(
            """
            Bill Inmon's top-down approach builds a **normalized enterprise data warehouse (EDW)** 
            first, then feeds department-specific data marts from it.
            
            - Follows 3NF (Third Normal Form) — no redundancy
            - Single source of truth before any analytics layer
            - Longer initial build time but highly consistent
            """
        )
        st.info(
            "Best for: Large enterprises, strict governance, complex regulatory environments")

    with st.expander("🥇 Data Vault"):
        st.write(
            """
            A hybrid methodology that focuses on **auditability, scalability, and flexibility**.
            Uses three entity types:
            
            - **Hubs** — unique business keys (e.g., customer ID)
            - **Links** — relationships between hubs
            - **Satellites** — descriptive attributes with full history
            """
        )
        st.info("Best for: Highly regulated industries, frequent source system changes")

    with st.expander("🧱 One Big Table (OBT) / Wide Table"):
        st.write(
            """
            A denormalized single table that pre-joins all relevant dimensions and facts. 
            Common in modern lakehouses and tools like dbt.
            
            - Simple for end users — no joins needed
            - High storage cost due to duplication
            - Works well with columnar formats (Parquet, Iceberg)
            """
        )
        st.info("Best for: Flat schemas, fast exploration, ML feature stores")

    st.divider()

    # ── NEW: Modeling Layers ──────────────────────────────────────────────────
    st.subheader("🗂️ Modeling Layers: Raw → Staging → Mart")
    st.write(
        """
        Modern data stacks (especially dbt-based pipelines) organize transformations into 
        distinct layers. Each layer has a clear responsibility — mixing concerns across layers 
        is one of the most common causes of unmaintainable warehouse code.
        """
    )

    col_r, col_s, col_m = st.columns(3)
    with col_r:
        st.markdown("**🟤 Raw / Source**")
        st.write(
            """
            Exact copy of source data — no transformations. 
            Preserves the original payload for debugging and re-processing.
            
            - One table per source object
            - No renaming, casting, or filtering
            - Append-only or full-replace load
            - Named: `raw_<source>.<table>`
            """
        )
    with col_s:
        st.markdown("**🔵 Staging**")
        st.write(
            """
            Light cleaning and standardization. One model per source table. 
            No joins, no business logic — only renaming and casting.
            
            - Rename fields to snake_case
            - Cast data types (strings → dates, floats)
            - Filter soft-deleted rows
            - Named: `stg_<source>__<table>`
            """
        )
    with col_m:
        st.markdown("**🟢 Mart / Serving**")
        st.write(
            """
            Final business-facing models. Kimball star schemas, OBTs, 
            or aggregated metrics tables ready for BI tools.
            
            - Joins, business logic, aggregations
            - Fact and dimension tables
            - Exposed to Tableau, Looker, Power BI
            - Named: `fct_<entity>`, `dim_<entity>`
            """
        )

    st.info(
        "💡 **Intermediate layer** (optional): sits between staging and mart for complex "
        "business logic like MRR classification, CLV calculations, or multi-source joins. "
        "Named: `int_<description>`"
    )

    st.divider()

    # ── NEW: Normalization Forms ───────────────────────────────────────────────
    st.subheader("📐 Normalization Forms (1NF → 2NF → 3NF)")
    st.write(
        """
        Normalization is the process of structuring a relational database to reduce redundancy 
        and improve data integrity. Each normal form builds on the previous one.
        """
    )

    with st.expander("1️⃣ First Normal Form (1NF)", expanded=True):
        st.write(
            """
            **Rule:** Every column must contain atomic (indivisible) values. No repeating groups or arrays.
            """
        )
        col_bad, col_good = st.columns(2)
        with col_bad:
            st.markdown("❌ **Violates 1NF**")
            st.code(
                """
orders
─────────────────────────────────
order_id │ products
─────────┼──────────────────────
1001     │ 'shirt, pants, shoes'
1002     │ 'hat'
                """,
                language="text",
            )
        with col_good:
            st.markdown("✅ **Satisfies 1NF**")
            st.code(
                """
order_lines
─────────────────────────
order_id │ product_name
─────────┼───────────────
1001     │ shirt
1001     │ pants
1001     │ shoes
1002     │ hat
                """,
                language="text",
            )

    with st.expander("2️⃣ Second Normal Form (2NF)"):
        st.write(
            """
            **Rule:** Must be in 1NF, and every non-key column must depend on the **entire** primary key 
            (no partial dependencies). Applies only when the primary key is composite.
            """
        )
        col_bad2, col_good2 = st.columns(2)
        with col_bad2:
            st.markdown("❌ **Violates 2NF**")
            st.code(
                """
order_lines (PK = order_id + product_id)
─────────────────────────────────────────
order_id │ product_id │ product_name
─────────┼────────────┼─────────────
1001     │ P01        │ Shirt
-- product_name depends only on product_id,
-- not the full composite key → partial dependency
                """,
                language="text",
            )
        with col_good2:
            st.markdown("✅ **Satisfies 2NF**")
            st.code(
                """
order_lines            products
──────────────────     ──────────────────
order_id │ product_id  product_id │ name
─────────┼──────────   ───────────┼──────
1001     │ P01         P01        │ Shirt
 
-- product_name moved to its own table
                """,
                language="text",
            )

    with st.expander("3️⃣ Third Normal Form (3NF)"):
        st.write(
            """
            **Rule:** Must be in 2NF, and no non-key column should depend on another non-key column 
            (no transitive dependencies). This is the standard for Inmon-style EDWs.
            """
        )
        col_bad3, col_good3 = st.columns(2)
        with col_bad3:
            st.markdown("❌ **Violates 3NF**")
            st.code(
                """
employees
──────────────────────────────────────
emp_id │ dept_id │ dept_name
───────┼─────────┼──────────
E01    │ D10     │ Finance
-- dept_name depends on dept_id,
-- not emp_id → transitive dependency
                """,
                language="text",
            )
        with col_good3:
            st.markdown("✅ **Satisfies 3NF**")
            st.code(
                """
employees           departments
────────────────    ─────────────────
emp_id │ dept_id    dept_id │ name
───────┼─────────   ────────┼────────
E01    │ D10        D10     │ Finance
 
-- dept_name moved to its own table
                """,
                language="text",
            )

    st.info(
        "📌 **When to normalize:** Use 3NF in transactional systems (OLTP) and Inmon EDWs. "
        "Intentionally **denormalize** for analytical marts (OLAP) to reduce join complexity."
    )

    st.divider()

    # ── NEW: Star vs Snowflake ─────────────────────────────────────────────────
    st.subheader("⭐ Star Schema vs ❄️ Snowflake Schema")
    st.write(
        """
        Both are Kimball dimensional designs. The difference is whether dimension tables 
        are further normalized into sub-dimensions.
        """
    )

    col_star, col_snow = st.columns(2)
    with col_star:
        st.markdown("#### ⭐ Star Schema")
        st.code(
            """
fact_orders
    ↓ FK
dim_customer   (flat, denormalized)
  customer_key
  full_name
  city
  country       ← stored directly
  region        ← stored directly
            """,
            language="text",
        )
        st.write(
            """
            - Dimensions are **flat** — all attributes in one table
            - Fewer joins → faster queries
            - Some redundancy (e.g. country repeated per customer)
            - Easier to understand for BI users
            - **Most common in practice**
            """
        )

    with col_snow:
        st.markdown("#### ❄️ Snowflake Schema")
        st.code(
            """
fact_orders
    ↓ FK
dim_customer
  customer_key
  full_name
  city_key      → dim_city
                    city_key
                    city_name
                    country_key → dim_country
                                    country_key
                                    region
            """,
            language="text",
        )
        st.write(
            """
            - Dimensions are **normalized** into sub-dimensions
            - More joins → slower queries
            - Less storage redundancy
            - Harder to query without good BI tooling
            - Useful when dimension tables are very large
            """
        )

    comparison_data = {
        "Attribute": [
            "Join complexity",
            "Query performance",
            "Storage efficiency",
            "Ease of use for analysts",
            "Redundancy",
            "Typical use case",
        ],
        "⭐ Star Schema": [
            "Low (1 join per dim)",
            "Faster",
            "Lower (some duplication)",
            "High",
            "Some",
            "Most BI/analytics workloads",
        ],
        "❄️ Snowflake Schema": [
            "High (multi-level joins)",
            "Slower",
            "Higher (normalized)",
            "Lower",
            "Minimal",
            "Very large, slowly changing dims",
        ],
    }

    import pandas as pd
    st.dataframe(pd.DataFrame(comparison_data),
                 width='stretch', hide_index=True)

    st.divider()

    # ── NEW: Anti-Patterns ────────────────────────────────────────────────────
    st.subheader("🚫 Data Modeling Anti-Patterns")
    st.write(
        "Knowing what **not** to do is as important as knowing the patterns. "
        "These are the most common mistakes teams make when designing data models."
    )

    anti_patterns = [
        {
            "icon": "🕳️",
            "name": "Undefined grain",
            "problem": "Building a fact table without defining what one row represents. "
                       "Results in accidental fan-out and double-counting in aggregations.",
            "fix": "Always write the grain statement first: "
                   "'One row per X per Y.' Validate row counts against source before publishing.",
        },
        {
            "icon": "🍝",
            "name": "Logic in the mart layer",
            "problem": "Embedding complex business rules (MRR classification, cohort logic, "
                       "CLV formulas) directly in fact or dimension models. "
                       "Makes models hard to test and reuse.",
            "fix": "Move all business logic to the intermediate layer. "
                   "Marts should only join and select — no CASE/WHEN chains.",
        },
        {
            "icon": "🔑",
            "name": "Using natural keys as surrogate keys",
            "problem": "Relying on source system IDs (email, order number) as primary keys. "
                       "Source keys can change, be reused, or conflict across systems.",
            "fix": "Generate surrogate keys (integer sequences or hash keys) in your warehouse. "
                   "Keep the natural key as a separate business key column.",
        },
        {
            "icon": "📦",
            "name": "One giant staging model",
            "problem": "Joining multiple source tables in the staging layer 'to save time.' "
                       "Breaks the 1:1 source-to-model contract and makes lineage invisible.",
            "fix": "One staging model per source table. All joins belong in intermediate models.",
        },
        {
            "icon": "📅",
            "name": "Summing semi-additive facts across time",
            "problem": "Applying SUM() to balance or inventory columns across date ranges. "
                       "Returns inflated, meaningless totals (e.g. summing daily account balances).",
            "fix": "Use snapshot-based queries for semi-additive facts. "
                   "Document additive vs semi-additive measures in your data catalog.",
        },
        {
            "icon": "🌀",
            "name": "Overusing SCD Type 2 everywhere",
            "problem": "Applying SCD Type 2 to every dimension by default adds row explosion, "
                       "complex point-in-time joins, and maintenance overhead where it's not needed.",
            "fix": "Use Type 1 for corrections, Type 2 only when historical accuracy is "
                   "required for analysis. Document the SCD type on every dimension.",
        },
        {
            "icon": "🏚️",
            "name": "No documentation or data catalog",
            "problem": "Models with no descriptions, column definitions, or grain statements. "
                       "Creates institutional knowledge silos and slows onboarding.",
            "fix": "Enforce descriptions in schema.yml (dbt) or your catalog tool. "
                   "At minimum: table grain, owner, and additive/semi-additive labels.",
        },
        {
            "icon": "🔗",
            "name": "Many-to-many joins without a bridge table",
            "problem": "Directly joining a fact table to a dimension with a many-to-many "
                       "relationship causes row multiplication and incorrect aggregations.",
            "fix": "Use a bridge table with an optional weighting column to resolve "
                   "many-to-many relationships before joining to facts.",
        },
    ]

    for ap in anti_patterns:
        with st.expander(f"{ap['icon']} {ap['name']}"):
            col_p, col_f = st.columns(2)
            with col_p:
                st.markdown("**❌ Problem**")
                st.write(ap["problem"])
            with col_f:
                st.markdown("**✅ Fix**")
                st.write(ap["fix"])

    st.divider()

    # ── Key Concepts Glossary ──────────────────────────────────────────────────
    st.subheader("Key Concepts Glossary")

    glossary = {
        "Grain": "The level of detail each row in a fact table represents. Must be defined before building.",
        "Slowly Changing Dimension (SCD)": "Technique for tracking historical changes in dimension attributes (Type 1, 2, 3).",
        "Surrogate Key": "A system-generated key (usually integer or UUID) used as primary key instead of natural keys.",
        "Conformed Dimension": "A dimension shared across multiple fact tables/data marts for consistent reporting.",
        "Bridge Table": "Resolves many-to-many relationships between fact and dimension tables.",
        "Junk Dimension": "Groups low-cardinality flags and indicators into a single dimension to reduce fact table clutter.",
        "Degenerate Dimension": "A dimension attribute stored directly in the fact table (e.g., order number).",
        "Snapshot Fact Table": "Records the state of a process at regular intervals (daily, monthly).",
        "Accumulating Snapshot": "Tracks the lifecycle of a process through multiple pipeline stages.",
        "Transitive Dependency": "When a non-key column depends on another non-key column rather than the primary key (violates 3NF).",
        "Partial Dependency": "When a non-key column depends only on part of a composite primary key (violates 2NF).",
        "Semi-Additive Fact": "A measure that can be summed across some dimensions (e.g. accounts) but not across time (e.g. balances).",
        "Fan-out": "Unintended row multiplication caused by joining tables with a many-to-many relationship without a bridge table.",
    }

    for term, definition in glossary.items():
        st.markdown(f"**{term}**")
        st.caption(definition)


# ─── TAB 2: Examples ─────────────────────────────────────────────────────────
with tab2:

    st.subheader("Data Model Examples")
    st.write("20 fully worked reference implementations covering Kimball, Data Vault, Inmon, OBT, and modern patterns.")
    st.divider()

    # ── Example 01 ────────────────────────────────────────────────────────────
    with st.expander("✅ Example 01 — Kimball: E-Commerce Star Schema", expanded=True):
        st.markdown("#### Overview")
        st.write("A classic star schema for an e-commerce platform. The central fact table records individual order line items; four dimensions provide context.")
        st.markdown("#### Grain")
        st.info("One row per order line item (one product within one order).")
        st.markdown("#### Schema Diagram")
        st.code("""
                ┌─────────────────┐
                │  dim_customer   │
                │─────────────────│
                │ customer_key PK │
                │ customer_id     │
                │ full_name       │
                │ city / country  │
                │ segment         │
                └────────┬────────┘
                         │
┌──────────────┐  ┌──────▼────────────────────────┐   ┌─────────────────┐
│  dim_product │  │      fact_order_lines         │   │   dim_date      │
│──────────────│  │───────────────────────────────│   │─────────────────│
│ product_key  ├─►│ order_line_key  PK            │◄─ ┤ date_key PK     │
│ product_name │  │ customer_key  FK              │   │ full_date       │
│ category     │  │ product_key   FK              │   │ month / quarter │
│ brand        │  │ date_key      FK              │   │ year            │
│ unit_cost    │  │ channel_key   FK              │   └─────────────────┘
└──────────────┘  │ quantity_ordered              │
                  │ unit_price / gross_revenue    │  ┌─────────────────┐
                  │ discount / net_revenue        │  │  dim_channel    │
                  │ cogs / gross_margin           │◄─┤ channel_key PK  │
                  └───────────────────────────────┘  │ channel_name    │
                                                     │ channel_type    │
                                                     └─────────────────┘
        """, language="text")
        st.markdown("#### DDL")
        st.code("""
CREATE TABLE fact_order_lines (
    order_line_key     BIGINT PRIMARY KEY,
    order_key          BIGINT NOT NULL,
    customer_key       INT    NOT NULL REFERENCES dim_customer(customer_key),
    product_key        INT    NOT NULL REFERENCES dim_product(product_key),
    date_key           INT    NOT NULL REFERENCES dim_date(date_key),
    channel_key        INT    NOT NULL REFERENCES dim_channel(channel_key),
    quantity_ordered   INT,
    unit_price         NUMERIC(12,2),
    gross_revenue      NUMERIC(14,2),
    discount_amount    NUMERIC(14,2),
    net_revenue        NUMERIC(14,2),
    cost_of_goods_sold NUMERIC(14,2),
    gross_margin       NUMERIC(14,2)
);

CREATE TABLE dim_customer (
    customer_key   INT PRIMARY KEY,
    customer_id    VARCHAR(50),
    full_name      VARCHAR(200),
    email          VARCHAR(200),
    city           VARCHAR(100),
    country        VARCHAR(100),
    segment        VARCHAR(50),
    effective_date DATE NOT NULL,
    expiry_date    DATE,
    is_current     BOOLEAN DEFAULT TRUE   -- SCD Type 2
);
        """, language="sql")
        st.markdown("#### Sample Query — Monthly Revenue by Category")
        st.code("""
SELECT d.year, d.month, p.category,
       SUM(f.net_revenue)   AS total_net_revenue,
       SUM(f.gross_margin)  AS total_gross_margin,
       ROUND(SUM(f.gross_margin)/NULLIF(SUM(f.net_revenue),0)*100,2) AS margin_pct
FROM   fact_order_lines f
JOIN   dim_date    d ON f.date_key    = d.date_key
JOIN   dim_product p ON f.product_key = p.product_key
WHERE  d.year = 2024
GROUP  BY d.year, d.month, p.category
ORDER  BY d.month, total_net_revenue DESC;
        """, language="sql")
        st.markdown("#### Design Decisions")
        st.write("""
- SCD Type 2 on `dim_customer` to track segment changes over time
- `order_key` is a degenerate dimension — no separate dim_order needed
- `dim_date` is conformed and shared across all fact tables
- Pre-calculated `gross_margin` stored for query speed
        """)

    # ── Example 02 ────────────────────────────────────────────────────────────
    with st.expander("✅ Example 02 — Kimball: SaaS Subscription Metrics (MRR, Churn, ARR)",  expanded=True):
        st.markdown("#### Overview")
        st.write("Tracks subscription-based revenue metrics for a SaaS business: Monthly Recurring Revenue, churn, expansions, and Annual Run Rate.")
        st.markdown("#### Grain")
        st.info("One row per customer per month (monthly subscription snapshot).")
        st.markdown("#### Schema Diagram")
        st.code("""
┌──────────────────┐   ┌──────────────────────────────┐   ┌─────────────────┐
│  dim_customer    │   │  fact_subscription_monthly   │   │   dim_date      │
│──────────────────│   │──────────────────────────────│   │─────────────────│
│ customer_key  PK ├──►│ sub_snapshot_key  PK         │◄──┤ date_key PK     │
│ company_name     │   │ customer_key  FK             │   │ month_start_date│
│ industry         │   │ plan_key      FK             │   │ month / year    │
│ region           │   │ date_key      FK             │   └─────────────────┘
│ contract_type    │   │ mrr                          │
│ csm_owner        │   │ arr                          │   ┌─────────────────┐
└──────────────────┘   │ seats_licensed               │   │   dim_plan      │
                       │ seats_used                   │◄──┤ plan_key PK     │
                       │ expansion_mrr                │   │ plan_name       │
                       │ contraction_mrr              │   │ tier            │
                       │ churned_mrr                  │   │ billing_cycle   │
                       │ new_mrr                      │   │ base_price      │
                       │ net_revenue_retention        │   └─────────────────┘
                       └──────────────────────────────┘
        """, language="text")
        st.markdown("#### DDL")
        st.code("""
CREATE TABLE fact_subscription_monthly (
    sub_snapshot_key      BIGINT PRIMARY KEY,
    customer_key          INT    NOT NULL REFERENCES dim_customer(customer_key),
    plan_key              INT    NOT NULL REFERENCES dim_plan(plan_key),
    date_key              INT    NOT NULL REFERENCES dim_date(date_key),
    mrr                   NUMERIC(14,2),
    arr                   NUMERIC(14,2),
    seats_licensed        INT,
    seats_used            INT,
    new_mrr               NUMERIC(14,2),   -- from new customers
    expansion_mrr         NUMERIC(14,2),   -- upgrades / seat adds
    contraction_mrr       NUMERIC(14,2),   -- downgrades
    churned_mrr           NUMERIC(14,2),   -- cancellations
    net_revenue_retention NUMERIC(6,4)     -- e.g. 1.12 = 112% NRR
);
        """, language="sql")
        st.markdown("#### Sample Query — MRR Waterfall by Month")
        st.code("""
SELECT
    d.year, d.month,
    SUM(new_mrr)         AS new_mrr,
    SUM(expansion_mrr)   AS expansion_mrr,
    SUM(contraction_mrr) AS contraction_mrr,
    SUM(churned_mrr)     AS churned_mrr,
    SUM(mrr)             AS ending_mrr
FROM   fact_subscription_monthly f
JOIN   dim_date d ON f.date_key = d.date_key
GROUP  BY d.year, d.month
ORDER  BY d.year, d.month;
        """, language="sql")
        st.markdown("#### Design Decisions")
        st.write("""
- Periodic snapshot grain (monthly) — ideal for time-series MRR analysis
- MRR components (new/expansion/churn) stored separately for waterfall charts
- NRR stored as pre-computed decimal to avoid repeated division
- `dim_plan` captures product tier for cohort-level analysis
        """)

    # ── Example 03 ────────────────────────────────────────────────────────────
    with st.expander("✅ Example 03 — Kimball: Marketing Attribution — Multi-Touch",  expanded=True):
        st.markdown("#### Overview")
        st.write("Models marketing touchpoints across the customer journey to attribute revenue credit to channels and campaigns using multi-touch attribution.")
        st.markdown("#### Grain")
        st.info(
            "One row per touchpoint per customer journey (one marketing interaction).")
        st.markdown("#### Schema Diagram")
        st.code("""
┌─────────────────┐   ┌────────────────────────────────┐   ┌──────────────────┐
│  dim_customer   │   │  fact_marketing_touchpoints    │   │  dim_campaign    │
│─────────────────│   │────────────────────────────────│   │──────────────────│
│ customer_key PK ├──►│ touchpoint_key  PK             │◄──┤ campaign_key  PK │
│ full_name       │   │ customer_key    FK             │   │ campaign_name    │
│ email           │   │ campaign_key    FK             │   │ channel          │
│ acquisition_src │   │ channel_key     FK             │   │ start_date       │
└─────────────────┘   │ date_key        FK             │   │ budget           │
                      │ touchpoint_position            │   └──────────────────┘
┌─────────────────┐   │ total_touches_in_journey       │
│  dim_channel    │   │ days_to_convert                │   ┌─────────────────┐
│─────────────────│   │ attributed_revenue_linear      │   │   dim_date      │
│ channel_key  PK ├──►│ attributed_revenue_first_touch │◄──┤ date_key PK     │
│ channel_name    │   │ attributed_revenue_last_touch  │   │ full_date       │
│ channel_type    │   │ attributed_revenue_time_decay  │   └─────────────────┘
│ paid_flag       │   │ converted_flag                 │
└─────────────────┘   └────────────────────────────────┘
        """, language="text")
        st.markdown("#### DDL")
        st.code("""
CREATE TABLE fact_marketing_touchpoints (
    touchpoint_key              BIGINT PRIMARY KEY,
    customer_key                INT  NOT NULL REFERENCES dim_customer(customer_key),
    campaign_key                INT  NOT NULL REFERENCES dim_campaign(campaign_key),
    channel_key                 INT  NOT NULL REFERENCES dim_channel(channel_key),
    date_key                    INT  NOT NULL REFERENCES dim_date(date_key),
    touchpoint_position         INT,
    total_touches_in_journey    INT,
    days_to_convert             INT,
    converted_flag              BOOLEAN,
    attributed_revenue_linear   NUMERIC(14,2),
    attributed_revenue_first    NUMERIC(14,2),
    attributed_revenue_last     NUMERIC(14,2),
    attributed_revenue_decay    NUMERIC(14,2)
);
        """, language="sql")
        st.markdown("#### Sample Query — Channel Revenue by Attribution Model")
        st.code("""
SELECT
    ch.channel_name,
    SUM(attributed_revenue_linear) AS linear_revenue,
    SUM(attributed_revenue_first)  AS first_touch_revenue,
    SUM(attributed_revenue_last)   AS last_touch_revenue,
    SUM(attributed_revenue_decay)  AS time_decay_revenue
FROM   fact_marketing_touchpoints f
JOIN   dim_channel ch ON f.channel_key = ch.channel_key
WHERE  converted_flag = TRUE
GROUP  BY ch.channel_name
ORDER  BY linear_revenue DESC;
        """, language="sql")
        st.markdown("#### Design Decisions")
        st.write("""
- Multiple attribution models stored as separate columns — avoids repeated recomputation
- `touchpoint_position` enables first/last-touch filtering without subqueries
- `days_to_convert` supports funnel velocity analysis
- One row per touchpoint, not per conversion — preserves full journey detail
        """)

    # ── Example 04 ────────────────────────────────────────────────────────────
    with st.expander("✅ Example 04 — Kimball: HR Headcount & Attrition",  expanded=True):
        st.markdown("#### Overview")
        st.write(
            "Tracks workforce headcount, hires, terminations, and attrition by department, role, and time period.")
        st.markdown("#### Grain")
        st.info("One row per employee per month (monthly headcount snapshot).")
        st.markdown("#### Schema Diagram")
        st.code("""
┌──────────────────┐   ┌──────────────────────────────┐   ┌──────────────────┐
│  dim_employee    │   │    fact_headcount_monthly     │   │  dim_department  │
│──────────────────│   │──────────────────────────────│   │──────────────────│
│ employee_key  PK ├──►│ headcount_key  PK            │◄──┤ dept_key  PK     │
│ employee_id      │   │ employee_key   FK            │   │ dept_name        │
│ full_name        │   │ dept_key       FK            │   │ cost_center      │
│ hire_date        │   │ role_key       FK            │   │ vp_owner         │
│ employment_type  │   │ date_key       FK            │   └──────────────────┘
│ gender           │   │ is_active                    │
│ location         │   │ is_new_hire                  │   ┌──────────────────┐
└──────────────────┘   │ is_terminated                │   │   dim_role       │
                       │ termination_type             │◄──┤ role_key  PK     │
                       │ tenure_months                │   │ role_title       │
                       │ salary_band                  │   │ level            │
                       └──────────────────────────────┘   │ function         │
                                                          └──────────────────┘
        """, language="text")
        st.markdown("#### DDL")
        st.code("""
CREATE TABLE fact_headcount_monthly (
    headcount_key    BIGINT PRIMARY KEY,
    employee_key     INT  NOT NULL REFERENCES dim_employee(employee_key),
    dept_key         INT  NOT NULL REFERENCES dim_department(dept_key),
    role_key         INT  NOT NULL REFERENCES dim_role(role_key),
    date_key         INT  NOT NULL REFERENCES dim_date(date_key),
    is_active        BOOLEAN,
    is_new_hire      BOOLEAN,
    is_terminated    BOOLEAN,
    termination_type VARCHAR(50),   -- 'voluntary', 'involuntary', 'retirement'
    tenure_months    INT,
    salary_band      VARCHAR(20)
);
        """, language="sql")
        st.markdown("#### Sample Query — Monthly Attrition Rate by Department")
        st.code("""
SELECT
    d.year, d.month, dp.dept_name,
    COUNT(*)                                        AS total_headcount,
    SUM(CASE WHEN is_terminated THEN 1 ELSE 0 END) AS terminations,
    ROUND(
      SUM(CASE WHEN is_terminated THEN 1 ELSE 0 END)::NUMERIC
      / NULLIF(COUNT(*),0) * 100, 2
    )                                               AS attrition_rate_pct
FROM   fact_headcount_monthly f
JOIN   dim_date       d  ON f.date_key  = d.date_key
JOIN   dim_department dp ON f.dept_key  = dp.dept_key
GROUP  BY d.year, d.month, dp.dept_name
ORDER  BY d.year, d.month;
        """, language="sql")
        st.markdown("#### Design Decisions")
        st.write("""
- Monthly snapshot grain enables trend analysis without event-level complexity
- `termination_type` stored in fact to avoid extra dimension for low-cardinality flag
- `dim_employee` uses SCD Type 2 to track role/department transfers
- `salary_band` banded (not raw) to protect PII
        """)

    # ── Example 05 ────────────────────────────────────────────────────────────
    with st.expander("✅ Example 05 — Kimball: Inventory & Supply Chain",  expanded=True):
        st.markdown("#### Overview")
        st.write(
            "Models inventory levels, stock movements (receipts, shipments, adjustments), and supplier performance.")
        st.markdown("#### Grain")
        st.info("One row per SKU per warehouse per day (daily inventory snapshot).")
        st.markdown("#### Schema Diagram")
        st.code("""
┌──────────────────┐   ┌────────────────────────────────┐   ┌──────────────────┐
│  dim_product     │   │    fact_inventory_daily         │   │  dim_warehouse   │
│──────────────────│   │────────────────────────────────│   │──────────────────│
│ product_key   PK ├──►│ inventory_key  PK              │◄──┤ warehouse_key PK │
│ sku              │   │ product_key    FK              │   │ warehouse_name   │
│ product_name     │   │ warehouse_key  FK              │   │ city / region    │
│ category         │   │ supplier_key   FK              │   │ capacity_units   │
│ unit_of_measure  │   │ date_key       FK              │   └──────────────────┘
│ reorder_point    │   │ opening_stock                  │
└──────────────────┘   │ closing_stock                  │   ┌──────────────────┐
                       │ units_received                 │   │  dim_supplier    │
                       │ units_shipped                  │◄──┤ supplier_key  PK │
                       │ units_adjusted                 │   │ supplier_name    │
                       │ days_of_supply                 │   │ lead_time_days   │
                       │ stockout_flag                  │   │ country          │
                       └────────────────────────────────┘   └──────────────────┘
        """, language="text")
        st.markdown("#### DDL")
        st.code("""
CREATE TABLE fact_inventory_daily (
    inventory_key   BIGINT PRIMARY KEY,
    product_key     INT  NOT NULL REFERENCES dim_product(product_key),
    warehouse_key   INT  NOT NULL REFERENCES dim_warehouse(warehouse_key),
    supplier_key    INT  NOT NULL REFERENCES dim_supplier(supplier_key),
    date_key        INT  NOT NULL REFERENCES dim_date(date_key),
    opening_stock   INT,
    closing_stock   INT,
    units_received  INT,
    units_shipped   INT,
    units_adjusted  INT,   -- shrinkage, write-offs
    days_of_supply  NUMERIC(8,2),
    stockout_flag   BOOLEAN
);
        """, language="sql")
        st.markdown("#### Sample Query — Stockout Risk by SKU")
        st.code("""
SELECT
    p.sku, p.product_name, p.reorder_point,
    f.closing_stock, f.days_of_supply, w.warehouse_name
FROM   fact_inventory_daily f
JOIN   dim_product   p ON f.product_key   = p.product_key
JOIN   dim_warehouse w ON f.warehouse_key = w.warehouse_key
JOIN   dim_date      d ON f.date_key      = d.date_key
WHERE  d.full_date = CURRENT_DATE - 1
  AND  f.closing_stock <= p.reorder_point
ORDER  BY f.days_of_supply ASC;
        """, language="sql")
        st.markdown("#### Design Decisions")
        st.write("""
- `days_of_supply` pre-computed (closing_stock / avg daily shipments) for operational dashboards
- `stockout_flag` allows simple boolean filter without threshold logic in BI tools
- Semi-additive measures: `opening_stock` and `closing_stock` cannot be summed across dates
- Supplier linked at SKU×warehouse level to support multi-supplier scenarios
        """)

    # ── Example 06 ────────────────────────────────────────────────────────────
    with st.expander("✅ Example 06 — Data Vault: Customer Hub + CRM Satellite",  expanded=True):
        st.markdown("#### Overview")
        st.write("A Data Vault 2.0 implementation for customer data integrated from a CRM source. Separates identity (Hub), relationships (Link), and descriptive attributes (Satellite).")
        st.markdown("#### Grain")
        st.info("Hub: one row per unique customer business key. Satellite: one row per customer per load batch (full history).")
        st.markdown("#### Schema Diagram")
        st.code("""
┌──────────────────────┐       ┌──────────────────────────────┐
│     hub_customer     │       │   sat_customer_crm           │
│──────────────────────│       │──────────────────────────────│
│ customer_hk  PK      │──────►│ customer_hk  FK              │
│ customer_bk          │       │ load_dts     PK (with hk)    │
│ load_dts             │       │ record_source                │
│ record_source        │       │ hash_diff                    │
└──────────┬───────────┘       │ full_name                    │
           │                   │ email / phone                │
┌──────────▼────────────────┐  │ city / country               │
│  lnk_customer_account     │  │ customer_segment             │
│───────────────────────────│  │ account_status               │
│ link_hk      PK           │  └──────────────────────────────┘
│ customer_hk  FK           │
│ account_hk   FK           │  ┌──────────────────────────────┐
│ load_dts                  │  │   hub_account                │
│ record_source             │  │──────────────────────────────│
└───────────────────────────┘  │ account_hk   PK              │
                               │ account_bk / load_dts        │
                               └──────────────────────────────┘
        """, language="text")
        st.markdown("#### DDL")
        st.code("""
CREATE TABLE hub_customer (
    customer_hk    CHAR(32) PRIMARY KEY,  -- MD5 hash of business key
    customer_bk    VARCHAR(100) NOT NULL,
    load_dts       TIMESTAMP NOT NULL,
    record_source  VARCHAR(100) NOT NULL
);

CREATE TABLE sat_customer_crm (
    customer_hk      CHAR(32)     NOT NULL REFERENCES hub_customer(customer_hk),
    load_dts         TIMESTAMP    NOT NULL,
    record_source    VARCHAR(100) NOT NULL,
    hash_diff        CHAR(32)     NOT NULL,
    full_name        VARCHAR(200),
    email            VARCHAR(200),
    phone            VARCHAR(50),
    city             VARCHAR(100),
    country          VARCHAR(100),
    customer_segment VARCHAR(50),
    account_status   VARCHAR(50),
    PRIMARY KEY (customer_hk, load_dts)
);

CREATE TABLE lnk_customer_account (
    link_hk       CHAR(32) PRIMARY KEY,
    customer_hk   CHAR(32) NOT NULL REFERENCES hub_customer(customer_hk),
    account_hk    CHAR(32) NOT NULL REFERENCES hub_account(account_hk),
    load_dts      TIMESTAMP NOT NULL,
    record_source VARCHAR(100) NOT NULL
);
        """, language="sql")
        st.markdown(
            "#### Sample Query — Current Customer Profile (Point-in-Time)")
        st.code("""
SELECT h.customer_bk, s.full_name, s.email, s.customer_segment, s.account_status
FROM   hub_customer h
JOIN   sat_customer_crm s ON h.customer_hk = s.customer_hk
WHERE  s.load_dts = (
    SELECT MAX(s2.load_dts)
    FROM   sat_customer_crm s2
    WHERE  s2.customer_hk = h.customer_hk
    AND    s2.load_dts   <= '2024-12-31'
);
        """, language="sql")
        st.markdown("#### Design Decisions")
        st.write("""
- Hash keys derived from business keys — source-system agnostic
- `hash_diff` on satellite detects attribute changes without full-row comparison
- Satellites are insert-only — full audit trail by design
- Links decouple relationships from hub definitions for max flexibility
        """)

    # ── Example 07 ────────────────────────────────────────────────────────────
    with st.expander("✅ Example 07 — Data Vault: Financial Transactions", expanded=True):
        st.markdown("#### Overview")
        st.write("Data Vault model for financial transaction data ingested from banking/ERP systems. Designed for auditability and regulatory compliance.")
        st.markdown("#### Grain")
        st.info("Hub: one row per unique transaction business key. Satellite: one row per transaction per load batch.")
        st.markdown("#### Schema Diagram")
        st.code("""
┌────────────────────────┐    ┌──────────────────────────────┐
│   hub_transaction      │    │   sat_transaction_detail     │
│────────────────────────│    │──────────────────────────────│
│ transaction_hk  PK     ├───►│ transaction_hk  FK           │
│ transaction_bk         │    │ load_dts  PK (with hk)       │
│ load_dts               │    │ hash_diff / record_source    │
│ record_source          │    │ amount / currency            │
└───────────┬────────────┘    │ transaction_type / status    │
            │                 │ description                  │
┌───────────▼────────────────────────────┐  └──────────────────┘
│      lnk_transaction_account           │
│────────────────────────────────────────│  ┌──────────────────┐
│ link_hk           PK                   │  │   hub_account    │
│ transaction_hk    FK                   │  │──────────────────│
│ debit_account_hk  FK                   │  │ account_hk PK    │
│ credit_account_hk FK                   │  │ account_bk       │
│ load_dts / record_source               │  └──────────────────┘
└────────────────────────────────────────┘
        """, language="text")
        st.markdown("#### DDL")
        st.code("""
CREATE TABLE hub_transaction (
    transaction_hk  CHAR(32) PRIMARY KEY,
    transaction_bk  VARCHAR(100) NOT NULL,
    load_dts        TIMESTAMP NOT NULL,
    record_source   VARCHAR(100) NOT NULL
);

CREATE TABLE sat_transaction_detail (
    transaction_hk    CHAR(32)      NOT NULL REFERENCES hub_transaction(transaction_hk),
    load_dts          TIMESTAMP     NOT NULL,
    hash_diff         CHAR(32)      NOT NULL,
    record_source     VARCHAR(100)  NOT NULL,
    amount            NUMERIC(18,4) NOT NULL,
    currency          CHAR(3)       NOT NULL,
    transaction_type  VARCHAR(50),
    status            VARCHAR(50),
    description       VARCHAR(500),
    PRIMARY KEY (transaction_hk, load_dts)
);

CREATE TABLE lnk_transaction_account (
    link_hk            CHAR(32) PRIMARY KEY,
    transaction_hk     CHAR(32) NOT NULL REFERENCES hub_transaction(transaction_hk),
    debit_account_hk   CHAR(32) NOT NULL REFERENCES hub_account(account_hk),
    credit_account_hk  CHAR(32) NOT NULL REFERENCES hub_account(account_hk),
    load_dts           TIMESTAMP NOT NULL,
    record_source      VARCHAR(100) NOT NULL
);
        """, language="sql")
        st.markdown("#### Sample Query — Daily Transaction Volume by Type")
        st.code("""
SELECT
    DATE(s.load_dts) AS txn_date,
    s.transaction_type, s.currency,
    COUNT(*)         AS txn_count,
    SUM(s.amount)    AS total_amount
FROM   hub_transaction h
JOIN   sat_transaction_detail s ON h.transaction_hk = s.transaction_hk
WHERE  s.load_dts = (
    SELECT MAX(s2.load_dts) FROM sat_transaction_detail s2
    WHERE  s2.transaction_hk = s.transaction_hk
)
GROUP  BY DATE(s.load_dts), s.transaction_type, s.currency
ORDER  BY txn_date DESC;
        """, language="sql")
        st.markdown("#### Design Decisions")
        st.write("""
- Insert-only satellites satisfy SOX and PCI audit trail requirements
- Dual account FK on link (debit + credit) models double-entry bookkeeping
- `hash_diff` detects status changes (pending → cleared) without row comparison
- Currency stored on satellite — same transaction can settle in different currencies
        """)

    # ── Example 08 ────────────────────────────────────────────────────────────
    with st.expander("✅ Example 08 — Inmon 3NF: Enterprise Customer Master", expanded=True):
        st.markdown("#### Overview")
        st.write("A fully normalized 3NF customer master entity for an enterprise data warehouse following Inmon's Corporate Information Factory. No redundancy; data is stored once and referenced everywhere.")
        st.markdown("#### Grain")
        st.info(
            "One row per entity at each normalized level (customer, address, contact, segment).")
        st.markdown("#### Schema Diagram")
        st.code("""
┌──────────────────┐
│     customer     │
│──────────────────│
│ customer_id   PK │
│ created_at       │
│ source_system    │
└────────┬─────────┘
         │ 1:N
┌────────▼──────────────┐       ┌──────────────────────┐
│   customer_profile    │       │   customer_address   │
│───────────────────────│       │──────────────────────│
│ profile_id    PK      │       │ address_id    PK     │
│ customer_id   FK      │       │ customer_id   FK     │
│ full_name             │       │ address_type         │
│ email                 │       │ street / city        │
│ date_of_birth         │       │ state / country      │
│ valid_from / valid_to │       │ postal_code          │
└───────────────────────┘       │ is_primary           │
                                └──────────────────────┘
┌───────────────────────┐       ┌──────────────────────┐
│  customer_segment     │       │  customer_contact    │
│───────────────────────│       │──────────────────────│
│ segment_id    PK      │       │ contact_id    PK     │
│ customer_id   FK      │       │ customer_id   FK     │
│ segment_code          │       │ contact_type         │
│ segment_name          │       │ contact_value        │
│ assigned_date         │       │ is_primary           │
└───────────────────────┘       │ opt_in_flag          │
                                └──────────────────────┘
        """, language="text")
        st.markdown("#### DDL")
        st.code("""
CREATE TABLE customer (
    customer_id   SERIAL PRIMARY KEY,
    created_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    source_system VARCHAR(100) NOT NULL
);

CREATE TABLE customer_profile (
    profile_id    SERIAL PRIMARY KEY,
    customer_id   INT NOT NULL REFERENCES customer(customer_id),
    full_name     VARCHAR(200),
    email         VARCHAR(200),
    date_of_birth DATE,
    gender        VARCHAR(20),
    valid_from    DATE NOT NULL,
    valid_to      DATE
);

CREATE TABLE customer_address (
    address_id    SERIAL PRIMARY KEY,
    customer_id   INT NOT NULL REFERENCES customer(customer_id),
    address_type  VARCHAR(50),
    street_line_1 VARCHAR(255),
    city          VARCHAR(100),
    state         VARCHAR(100),
    country       VARCHAR(100),
    postal_code   VARCHAR(20),
    is_primary    BOOLEAN DEFAULT FALSE
);

CREATE TABLE customer_segment (
    segment_id    SERIAL PRIMARY KEY,
    customer_id   INT NOT NULL REFERENCES customer(customer_id),
    segment_code  VARCHAR(50),
    segment_name  VARCHAR(100),
    assigned_date DATE
);
        """, language="sql")
        st.markdown("#### Sample Query — Active Customers with Primary Address")
        st.code("""
SELECT c.customer_id, cp.full_name, cp.email, ca.city, ca.country, cs.segment_name
FROM   customer c
JOIN   customer_profile cp ON c.customer_id = cp.customer_id AND cp.valid_to IS NULL
JOIN   customer_address ca ON c.customer_id = ca.customer_id AND ca.is_primary = TRUE
LEFT   JOIN customer_segment cs ON c.customer_id = cs.customer_id
ORDER  BY cp.full_name;
        """, language="sql")
        st.markdown("#### Design Decisions")
        st.write("""
- 3NF eliminates redundancy — email stored once, not repeated across fact tables
- `valid_from/valid_to` on profile handles historization without full SCD infrastructure
- Separate `customer_contact` table allows multiple phone/email entries with opt-in flags
- This normalized layer feeds denormalized data marts downstream
        """)

    # ── Example 09 ────────────────────────────────────────────────────────────
    with st.expander("✅ Example 09 — One Big Table: Product Analytics Event Stream", expanded=True):
        st.markdown("#### Overview")
        st.write("A denormalized wide table for product analytics — all user event data pre-joined with user, session, and product context. Common output of dbt Intermediate → Mart layer.")
        st.markdown("#### Grain")
        st.info("One row per user event (page view, click, feature interaction).")
        st.markdown("#### Schema Diagram")
        st.code("""
┌────────────────────────────────────────────────────────────────┐
│                   obt_product_events                           │
│────────────────────────────────────────────────────────────────│
│  event_id              VARCHAR    PK                           │
│  event_timestamp       TIMESTAMP                               │
│  event_type            VARCHAR    -- 'page_view','click'       │
│  event_name            VARCHAR                                 │
│                                                                │
│  -- User context (denormalized)                                │
│  user_id / user_email  VARCHAR                                 │
│  user_plan             VARCHAR                                 │
│  user_country          VARCHAR                                 │
│  user_signup_date      DATE                                    │
│  user_cohort_month     CHAR(7)    -- 'YYYY-MM'                 │
│                                                                │
│  -- Session context                                            │
│  session_id            VARCHAR                                 │
│  session_start_ts      TIMESTAMP                               │
│  session_channel       VARCHAR                                 │
│  session_referrer      VARCHAR                                 │
│                                                                │
│  -- Page / Feature context                                     │
│  page_url / page_section  VARCHAR                              │
│  feature_name / feature_area VARCHAR                           │
│                                                                │
│  -- Device context                                             │
│  device_type / browser / os  VARCHAR                           │
└────────────────────────────────────────────────────────────────┘
        """, language="text")
        st.markdown("#### DDL")
        st.code("""
CREATE TABLE obt_product_events (
    event_id           VARCHAR(100) PRIMARY KEY,
    event_timestamp    TIMESTAMP    NOT NULL,
    event_type         VARCHAR(50),
    event_name         VARCHAR(200),
    user_id            VARCHAR(100),
    user_email         VARCHAR(200),
    user_plan          VARCHAR(50),
    user_country       VARCHAR(100),
    user_signup_date   DATE,
    user_cohort_month  CHAR(7),
    session_id         VARCHAR(100),
    session_start_ts   TIMESTAMP,
    session_channel    VARCHAR(100),
    session_referrer   VARCHAR(500),
    page_url           VARCHAR(500),
    page_section       VARCHAR(100),
    feature_name       VARCHAR(100),
    feature_area       VARCHAR(100),
    device_type        VARCHAR(50),
    browser            VARCHAR(100),
    os                 VARCHAR(100)
);
        """, language="sql")
        st.markdown("#### Sample Query — Feature Adoption by Plan")
        st.code("""
SELECT
    user_plan, feature_name,
    COUNT(DISTINCT user_id) AS unique_users,
    COUNT(*)                AS total_events
FROM   obt_product_events
WHERE  event_type = 'feature_interaction'
  AND  event_timestamp >= CURRENT_DATE - 30
GROUP  BY user_plan, feature_name
ORDER  BY unique_users DESC;
        """, language="sql")
        st.markdown("#### Design Decisions")
        st.write("""
- No joins required — ideal for product analysts and data scientists
- `user_cohort_month` pre-computed to simplify retention/cohort queries
- Trade-off: high storage cost due to repeated user/session attributes per event
- Works best with columnar storage (Parquet, BigQuery, Snowflake)
        """)

    # ── Example 10 ────────────────────────────────────────────────────────────
    with st.expander("✅ Example 10 — One Big Table: Ad Spend + Performance", expanded=True):
        st.markdown("#### Overview")
        st.write("A wide denormalized table for marketing performance reporting — ad spend, impressions, clicks, conversions, and cost metrics across platforms in one table.")
        st.markdown("#### Grain")
        st.info("One row per ad × platform × date.")
        st.markdown("#### Schema Diagram")
        st.code("""
┌────────────────────────────────────────────────────────────────┐
│                   obt_ad_performance                           │
│────────────────────────────────────────────────────────────────│
│  row_id             VARCHAR    PK                              │
│  report_date        DATE                                       │
│  platform           VARCHAR    -- 'google','meta','tiktok'     │
│  platform_account   VARCHAR                                    │
│  campaign_id / campaign_name    VARCHAR                        │
│  campaign_objective VARCHAR    -- 'awareness','conversion'     │
│  ad_set_id / ad_id / ad_name   VARCHAR                        │
│  target_country / age_range / gender  VARCHAR                 │
│  impressions        BIGINT                                     │
│  clicks             BIGINT                                     │
│  spend              NUMERIC(14,4)                              │
│  conversions        INT                                        │
│  revenue_attributed NUMERIC(14,2)                              │
│  ctr  NUMERIC   -- click-through rate                         │
│  cpc  NUMERIC   -- cost per click                             │
│  cpa  NUMERIC   -- cost per acquisition                       │
│  roas NUMERIC   -- return on ad spend                         │
└────────────────────────────────────────────────────────────────┘
        """, language="text")
        st.markdown("#### DDL")
        st.code("""
CREATE TABLE obt_ad_performance (
    row_id               VARCHAR(200) PRIMARY KEY,
    report_date          DATE         NOT NULL,
    platform             VARCHAR(50)  NOT NULL,
    platform_account     VARCHAR(200),
    campaign_id          VARCHAR(200),
    campaign_name        VARCHAR(500),
    campaign_objective   VARCHAR(100),
    ad_set_id            VARCHAR(200),
    ad_id                VARCHAR(200),
    ad_name              VARCHAR(500),
    target_country       VARCHAR(100),
    target_age_range     VARCHAR(50),
    target_gender        VARCHAR(20),
    impressions          BIGINT,
    clicks               BIGINT,
    spend                NUMERIC(14,4),
    conversions          INT,
    revenue_attributed   NUMERIC(14,2),
    ctr                  NUMERIC(8,6),
    cpc                  NUMERIC(10,4),
    cpa                  NUMERIC(10,4),
    roas                 NUMERIC(8,4)
);
        """, language="sql")
        st.markdown("#### Sample Query — ROAS by Platform and Objective")
        st.code("""
SELECT
    platform, campaign_objective,
    SUM(spend)              AS total_spend,
    SUM(revenue_attributed) AS total_revenue,
    ROUND(SUM(revenue_attributed)/NULLIF(SUM(spend),0),2) AS blended_roas,
    ROUND(SUM(spend)/NULLIF(SUM(conversions),0),2)        AS avg_cpa
FROM   obt_ad_performance
WHERE  report_date BETWEEN '2024-01-01' AND '2024-12-31'
GROUP  BY platform, campaign_objective
ORDER  BY total_spend DESC;
        """, language="sql")
        st.markdown("#### Design Decisions")
        st.write("""
- Derived metrics (CTR, CPC, CPA, ROAS) stored pre-computed to avoid BI-layer inconsistencies
- `row_id` composed of platform+campaign+ad+date for natural uniqueness
- Single table spans multiple platforms — no cross-platform join needed
- Updated daily via full-replace or incremental upsert by report_date
        """)

    # ── Example 11 ────────────────────────────────────────────────────────────
    with st.expander("✅ Example 11 — Snapshot Fact: Daily Active Users", expanded=True):
        st.markdown("#### Overview")
        st.write("A periodic snapshot fact table that captures daily user activity metrics — DAU, session counts, and engagement scores — for trend and cohort analysis.")
        st.markdown("#### Grain")
        st.info("One row per user per day (only for days the user was active).")
        st.markdown("#### Schema Diagram")
        st.code("""
┌──────────────────┐   ┌────────────────────────────────┐   ┌─────────────────┐
│   dim_user       │   │   fact_daily_active_users      │   │   dim_date      │
│──────────────────│   │────────────────────────────────│   │─────────────────│
│ user_key      PK ├──►│ dau_key           PK           │◄──┤ date_key PK     │
│ user_id          │   │ user_key          FK           │   │ full_date       │
│ plan             │   │ date_key          FK           │   │ is_weekend      │
│ country          │   │ platform_key      FK           │   │ week_number     │
│ signup_date      │   │ session_count                  │   └─────────────────┘
│ cohort_month     │   │ total_time_spent_sec           │
└──────────────────┘   │ pages_viewed                   │   ┌─────────────────┐
                       │ features_used_count            │   │  dim_platform   │
                       │ events_fired                   │◄──┤ platform_key PK │
                       │ engagement_score               │   │ platform_name   │
                       └────────────────────────────────┘   │ device_type     │
                                                            └─────────────────┘
        """, language="text")
        st.markdown("#### DDL")
        st.code("""
CREATE TABLE fact_daily_active_users (
    dau_key               BIGINT PRIMARY KEY,
    user_key              INT  NOT NULL REFERENCES dim_user(user_key),
    date_key              INT  NOT NULL REFERENCES dim_date(date_key),
    platform_key          INT  NOT NULL REFERENCES dim_platform(platform_key),
    session_count         INT,
    total_time_spent_sec  INT,
    pages_viewed          INT,
    features_used_count   INT,
    events_fired          INT,
    engagement_score      NUMERIC(6,2)
);
        """, language="sql")
        st.markdown("#### Sample Query — 30-Day Rolling DAU by Plan")
        st.code("""
SELECT
    d.full_date, u.plan,
    COUNT(DISTINCT f.user_key)       AS dau,
    AVG(f.total_time_spent_sec)/60.0 AS avg_session_min,
    AVG(f.engagement_score)          AS avg_engagement
FROM   fact_daily_active_users f
JOIN   dim_user u ON f.user_key = u.user_key
JOIN   dim_date d ON f.date_key = d.date_key
WHERE  d.full_date >= CURRENT_DATE - 30
GROUP  BY d.full_date, u.plan
ORDER  BY d.full_date DESC, dau DESC;
        """, language="sql")
        st.markdown("#### Design Decisions")
        st.write("""
- Only active days are inserted — reduces table size vs. storing zeros for inactive users
- `engagement_score` is a composite metric computed in dbt before load
- `dim_platform` separates mobile/web/desktop for cross-platform DAU analysis
- Use `COUNT(DISTINCT user_key)` — not COUNT(*) — when aggregating DAU across platforms
        """)

    # ── Example 12 ────────────────────────────────────────────────────────────
    with st.expander("✅ Example 12 — Accumulating Snapshot: Lead-to-Close Pipeline", expanded=True):
        st.markdown("#### Overview")
        st.write("An accumulating snapshot fact table tracking a sales lead through each pipeline stage. One row per lead — updated in-place as the lead progresses.")
        st.markdown("#### Grain")
        st.info("One row per sales lead (updated at each stage milestone).")
        st.markdown("#### Schema Diagram")
        st.code("""
┌──────────────────┐   ┌────────────────────────────────────────┐
│   dim_lead       │   │      fact_lead_pipeline                │
│──────────────────│   │────────────────────────────────────────│
│ lead_key      PK ├──►│ lead_pipeline_key   PK                 │
│ lead_id          │   │ lead_key            FK                 │
│ company_name     │   │ rep_key             FK                 │
│ lead_source      │   │                                        │
│ industry         │   │ -- one date FK per stage milestone     │
└──────────────────┘   │ created_date_key                       │
                       │ qualified_date_key                     │
┌──────────────────┐   │ demo_date_key                          │
│   dim_rep        │   │ proposal_date_key                      │
│──────────────────│   │ negotiation_date_key                   │
│ rep_key       PK ├──►│ closed_date_key                        │
│ rep_name         │   │                                        │
│ region / team    │   │ days_created_to_qualified              │
└──────────────────┘   │ days_qualified_to_demo                 │
                       │ days_demo_to_proposal                  │
                       │ days_proposal_to_close                 │
                       │ total_days_to_close                    │
                       │ deal_value                             │
                       │ pipeline_stage / outcome               │
                       └────────────────────────────────────────┘
        """, language="text")
        st.markdown("#### DDL")
        st.code("""
CREATE TABLE fact_lead_pipeline (
    lead_pipeline_key          BIGINT PRIMARY KEY,
    lead_key                   INT NOT NULL REFERENCES dim_lead(lead_key),
    rep_key                    INT NOT NULL REFERENCES dim_rep(rep_key),
    created_date_key           INT REFERENCES dim_date(date_key),
    qualified_date_key         INT REFERENCES dim_date(date_key),
    demo_date_key              INT REFERENCES dim_date(date_key),
    proposal_date_key          INT REFERENCES dim_date(date_key),
    negotiation_date_key       INT REFERENCES dim_date(date_key),
    closed_date_key            INT REFERENCES dim_date(date_key),
    days_created_to_qualified  INT,
    days_qualified_to_demo     INT,
    days_demo_to_proposal      INT,
    days_proposal_to_close     INT,
    total_days_to_close        INT,
    deal_value                 NUMERIC(14,2),
    pipeline_stage             VARCHAR(50),
    outcome                    VARCHAR(20)   -- 'won', 'lost', NULL = open
);
        """, language="sql")
        st.markdown("#### Sample Query — Average Days per Stage for Won Deals")
        st.code("""
SELECT
    r.region,
    ROUND(AVG(days_created_to_qualified),1) AS avg_days_to_qualified,
    ROUND(AVG(days_qualified_to_demo),1)    AS avg_days_to_demo,
    ROUND(AVG(days_demo_to_proposal),1)     AS avg_days_to_proposal,
    ROUND(AVG(days_proposal_to_close),1)    AS avg_days_to_close,
    ROUND(AVG(total_days_to_close),1)       AS avg_total_cycle
FROM   fact_lead_pipeline f
JOIN   dim_rep r ON f.rep_key = r.rep_key
WHERE  outcome = 'won'
GROUP  BY r.region
ORDER  BY avg_total_cycle;
        """, language="sql")
        st.markdown("#### Design Decisions")
        st.write("""
- One row per lead updated in-place — unlike transaction facts which are insert-only
- Multiple date FKs for each stage enable time-intelligence per milestone
- NULL date keys indicate a stage not yet reached
- Lag metrics pre-computed on each update to avoid repeated date arithmetic in BI tools
        """)

    # ── Example 13 ────────────────────────────────────────────────────────────
    with st.expander("✅ Example 13 — Bridge Table: Product Tags Many-to-Many", expanded=True):
        st.markdown("#### Overview")
        st.write("A bridge table resolves the many-to-many relationship between products and tags. Enables tag-based filtering and revenue attribution without multi-valued columns.")
        st.markdown("#### Grain")
        st.info("One row per product–tag combination.")
        st.markdown("#### Schema Diagram")
        st.code("""
┌──────────────────┐   ┌──────────────────────────────┐   ┌──────────────────┐
│   dim_product    │   │   bridge_product_tag         │   │    dim_tag       │
│──────────────────│   │──────────────────────────────│   │──────────────────│
│ product_key   PK ├──►│ product_key    FK            │◄──┤ tag_key       PK │
│ product_name     │   │ tag_key        FK            │   │ tag_name         │
│ category         │   │ tag_weight     NUMERIC       │   │ tag_category     │
│ sku              │   │ assigned_date  DATE          │   │ is_active        │
└──────────────────┘   │ assigned_by    VARCHAR       │   └──────────────────┘
                       │ PK (product_key, tag_key)    │
                       └──────────────────────────────┘

Join pattern: fact_order_lines → dim_product → bridge_product_tag → dim_tag
        """, language="text")
        st.markdown("#### DDL")
        st.code("""
CREATE TABLE dim_tag (
    tag_key       INT PRIMARY KEY,
    tag_name      VARCHAR(100) NOT NULL,
    tag_category  VARCHAR(100),
    is_active     BOOLEAN DEFAULT TRUE
);

CREATE TABLE bridge_product_tag (
    product_key   INT  NOT NULL REFERENCES dim_product(product_key),
    tag_key       INT  NOT NULL REFERENCES dim_tag(tag_key),
    tag_weight    NUMERIC(5,4) DEFAULT 1.0,
    assigned_date DATE,
    assigned_by   VARCHAR(100),
    PRIMARY KEY (product_key, tag_key)
);
        """, language="sql")
        st.markdown("#### Sample Query — Revenue by Tag")
        st.code("""
SELECT
    t.tag_name, t.tag_category,
    COUNT(DISTINCT f.order_line_key) AS line_items,
    SUM(f.net_revenue)               AS total_revenue
FROM   fact_order_lines    f
JOIN   dim_product         p  ON f.product_key = p.product_key
JOIN   bridge_product_tag  bt ON p.product_key = bt.product_key
JOIN   dim_tag             t  ON bt.tag_key    = t.tag_key
WHERE  t.is_active = TRUE
GROUP  BY t.tag_name, t.tag_category
ORDER  BY total_revenue DESC;
        """, language="sql")
        st.markdown("#### Design Decisions")
        st.write("""
- Bridge table avoids multi-value columns (comma-separated tags) in the dimension
- `tag_weight` supports partial attribution when a product has multiple tags
- Join through bridge explodes rows — always filter/aggregate with this in mind
- A product with N tags produces N rows when joined — wrap in CTE if counting distinct products
        """)

    # ── Example 14 ────────────────────────────────────────────────────────────
    with st.expander("✅ Example 14 — Junk Dimension: Web Session Flags", expanded=True):
        st.markdown("#### Overview")
        st.write("A junk dimension groups several low-cardinality boolean flag columns from web session data into a single dimension, reducing fact table width without creating many small dimension tables.")
        st.markdown("#### Grain")
        st.info(
            "One row per unique combination of flag values (not per session). Max 2^N rows.")
        st.markdown("#### Schema Diagram")
        st.code("""
┌───────────────────────────────┐   ┌──────────────────────────────────┐
│       dim_session_flags       │   │      fact_web_sessions           │
│───────────────────────────────│   │──────────────────────────────────│
│ session_flag_key  PK          │◄──┤ session_key         PK           │
│ is_authenticated              │   │ user_key            FK           │
│ is_mobile                     │   │ date_key            FK           │
│ is_returning_user             │   │ session_flag_key    FK  ◄── junk │
│ has_bounced                   │   │ pageviews                        │
│ is_organic_traffic            │   │ time_on_site_sec                 │
│ has_converted                 │   │ revenue                          │
│ is_bot                        │   └──────────────────────────────────┘
└───────────────────────────────┘
7 flags → max 128 rows in junk dimension
        """, language="text")
        st.markdown("#### DDL")
        st.code("""
CREATE TABLE dim_session_flags (
    session_flag_key   INT PRIMARY KEY,
    is_authenticated   BOOLEAN,
    is_mobile          BOOLEAN,
    is_returning_user  BOOLEAN,
    has_bounced        BOOLEAN,
    is_organic_traffic BOOLEAN,
    has_converted      BOOLEAN,
    is_bot             BOOLEAN
);

-- Populate all 2^7 = 128 combinations
INSERT INTO dim_session_flags (session_flag_key, is_authenticated, is_mobile,
    is_returning_user, has_bounced, is_organic_traffic, has_converted, is_bot)
SELECT ROW_NUMBER() OVER () AS session_flag_key, a.v, b.v, c.v, d.v, e.v, f.v, g.v
FROM (VALUES (TRUE),(FALSE)) a(v), (VALUES (TRUE),(FALSE)) b(v),
     (VALUES (TRUE),(FALSE)) c(v), (VALUES (TRUE),(FALSE)) d(v),
     (VALUES (TRUE),(FALSE)) e(v), (VALUES (TRUE),(FALSE)) f(v),
     (VALUES (TRUE),(FALSE)) g(v);

CREATE TABLE fact_web_sessions (
    session_key       BIGINT PRIMARY KEY,
    user_key          INT NOT NULL REFERENCES dim_user(user_key),
    date_key          INT NOT NULL REFERENCES dim_date(date_key),
    session_flag_key  INT NOT NULL REFERENCES dim_session_flags(session_flag_key),
    pageviews         INT,
    time_on_site_sec  INT,
    revenue           NUMERIC(12,2)
);
        """, language="sql")
        st.markdown("#### Sample Query — Conversion Rate by Traffic Type")
        st.code("""
SELECT
    sf.is_mobile, sf.is_organic_traffic,
    COUNT(*)                                         AS total_sessions,
    SUM(CASE WHEN sf.has_converted THEN 1 END)       AS conversions,
    ROUND(
      SUM(CASE WHEN sf.has_converted THEN 1 END)::NUMERIC / COUNT(*) * 100, 2
    )                                                AS conversion_rate_pct
FROM   fact_web_sessions f
JOIN   dim_session_flags sf ON f.session_flag_key = sf.session_flag_key
WHERE  sf.is_bot = FALSE
GROUP  BY sf.is_mobile, sf.is_organic_traffic;
        """, language="sql")
        st.markdown("#### Design Decisions")
        st.write("""
- 7 flags × 128 combinations — tiny dimension, massive fact table savings
- Filter `is_bot = FALSE` at join layer, not in a WHERE subquery
- Junk dim lookup happens at ETL time — no runtime flag-to-key resolution needed
- Avoid adding high-cardinality fields (e.g., country) to junk dim — use a separate dimension
        """)

    # ── Example 15 ────────────────────────────────────────────────────────────
    with st.expander("✅ Example 15 — SCD Type 2: Employee Role History", expanded=True):
        st.markdown("#### Overview")
        st.write("Demonstrates Slowly Changing Dimension Type 2 for tracking employee role and department changes over time. Each change creates a new row with effective dates.")
        st.markdown("#### Grain")
        st.info(
            "One row per employee per role period (a new row is added for each change).")
        st.markdown("#### Schema Diagram")
        st.code("""
dim_employee (SCD Type 2)
┌────────────────────────────────────────────────────────────────┐
│  employee_key     INT   PK  (surrogate — new one per change)   │
│  employee_id      VARCHAR    (natural/business key)            │
│  full_name        VARCHAR                                      │
│  role_title       VARCHAR                                      │
│  department       VARCHAR                                      │
│  manager_id       VARCHAR                                      │
│  location         VARCHAR                                      │
│  salary_band      VARCHAR                                      │
│  effective_date   DATE                                         │
│  expiry_date      DATE       (NULL = current record)           │
│  is_current       BOOLEAN                                      │
└────────────────────────────────────────────────────────────────┘

Example:
 employee_key │ employee_id │ role_title          │ effective  │ expiry     │ current
─────────────┼─────────────┼─────────────────────┼────────────┼────────────┼────────
           1 │ E001        │ Data Analyst         │ 2021-03-01 │ 2023-06-30 │ FALSE
           2 │ E001        │ Senior Data Analyst  │ 2023-07-01 │ 2024-11-30 │ FALSE
           3 │ E001        │ Analytics Manager    │ 2024-12-01 │ NULL       │ TRUE
        """, language="text")
        st.markdown("#### DDL")
        st.code("""
CREATE TABLE dim_employee (
    employee_key    SERIAL PRIMARY KEY,
    employee_id     VARCHAR(50)  NOT NULL,
    full_name       VARCHAR(200) NOT NULL,
    role_title      VARCHAR(200),
    department      VARCHAR(100),
    manager_id      VARCHAR(50),
    location        VARCHAR(100),
    salary_band     VARCHAR(20),
    effective_date  DATE NOT NULL,
    expiry_date     DATE,
    is_current      BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE UNIQUE INDEX idx_employee_current
    ON dim_employee (employee_id) WHERE is_current = TRUE;
        """, language="sql")
        st.markdown("#### SCD Type 2 Update Logic")
        st.code("""
-- Step 1: Expire old record
UPDATE dim_employee
SET    expiry_date = :new_effective_date - INTERVAL '1 day',
       is_current  = FALSE
WHERE  employee_id = :employee_id AND is_current = TRUE;

-- Step 2: Insert new version
INSERT INTO dim_employee (
    employee_id, full_name, role_title, department,
    manager_id, location, salary_band, effective_date, expiry_date, is_current
) VALUES (
    :employee_id, :full_name, :new_role, :new_dept,
    :manager_id, :location, :salary_band, :new_effective_date, NULL, TRUE
);
        """, language="sql")
        st.markdown("#### Sample Query — Headcount by Role at a Point in Time")
        st.code("""
SELECT role_title, department, COUNT(*) AS headcount
FROM   dim_employee
WHERE  effective_date <= '2023-12-31'
  AND  (expiry_date > '2023-12-31' OR expiry_date IS NULL)
GROUP  BY role_title, department
ORDER  BY headcount DESC;
        """, language="sql")
        st.markdown("#### Design Decisions")
        st.write("""
- New surrogate key per version — fact rows pointing to old key preserve historical role
- `is_current` flag enables fast lookup without date arithmetic
- Partial unique index ensures only one current row per `employee_id`
- Point-in-time pattern: `effective_date <= :dt AND (expiry_date > :dt OR expiry_date IS NULL)`
        """)

    # ── Example 16 ────────────────────────────────────────────────────────────
    with st.expander("✅ Example 16 — SCD Type 3: Customer Tier Changes", expanded=True):
        st.markdown("#### Overview")
        st.write("SCD Type 3 tracks a limited change history by adding 'previous value' columns alongside the current value. Used when you need to compare current vs. prior state without full history.")
        st.markdown("#### Grain")
        st.info(
            "One row per customer (updated in-place — only retains prior and current tier).")
        st.markdown("#### Schema Diagram")
        st.code("""
dim_customer (SCD Type 3)
┌────────────────────────────────────────────────────────────────┐
│  customer_key         INT    PK                                │
│  customer_id          VARCHAR                                  │
│  full_name            VARCHAR                                  │
│  email / country      VARCHAR    ← Type 1: overwrite           │
│                                                                │
│  current_tier         VARCHAR    ← Type 3: current value       │
│  tier_change_date     DATE                                     │
│                                                                │
│  previous_tier        VARCHAR    ← Type 3: one prior state     │
│  previous_tier_date   DATE                                     │
└────────────────────────────────────────────────────────────────┘

Limitation: only ONE prior state. For full history → use Type 2.
        """, language="text")
        st.markdown("#### DDL")
        st.code("""
CREATE TABLE dim_customer (
    customer_key       INT PRIMARY KEY,
    customer_id        VARCHAR(50) NOT NULL UNIQUE,
    full_name          VARCHAR(200),
    email              VARCHAR(200),
    country            VARCHAR(100),
    current_tier       VARCHAR(50),
    tier_change_date   DATE,
    previous_tier      VARCHAR(50),
    previous_tier_date DATE
);
        """, language="sql")
        st.markdown("#### Type 3 Update Logic")
        st.code("""
UPDATE dim_customer
SET    previous_tier      = current_tier,
       previous_tier_date = tier_change_date,
       current_tier       = :new_tier,
       tier_change_date   = :change_date,
       email              = :email         -- Type 1 overwrite
WHERE  customer_id = :customer_id;
        """, language="sql")
        st.markdown("#### Sample Query — Tier Upgrade/Downgrade Analysis")
        st.code("""
SELECT
    previous_tier, current_tier,
    COUNT(*) AS customer_count,
    CASE
        WHEN current_tier IN ('Gold','Platinum') AND previous_tier IN ('Bronze','Silver')
        THEN 'Upgrade'
        WHEN current_tier IN ('Bronze','Silver') AND previous_tier IN ('Gold','Platinum')
        THEN 'Downgrade'
        ELSE 'Lateral'
    END AS movement_type
FROM   dim_customer
WHERE  previous_tier IS NOT NULL
GROUP  BY previous_tier, current_tier
ORDER  BY customer_count DESC;
        """, language="sql")
        st.markdown("#### Design Decisions")
        st.write("""
- Type 3 is simpler than Type 2 but limited to one prior state
- Good fit when the question is 'what tier were they before?' not a full timeline
- `email` and `country` use Type 1 (overwrite) — no history needed
- If more than two historical states are needed, migrate to Type 2
        """)

    # ── Example 17 ────────────────────────────────────────────────────────────
    with st.expander("✅ Example 17 — SCD Type Comparison (Type 1 / 2 / 3)", expanded=True):
        st.markdown("#### Overview")
        st.write("A side-by-side reference comparing the three main Slowly Changing Dimension strategies — when to use each, trade-offs, and implementation patterns.")
        st.markdown("#### Comparison")
        st.code("""
┌──────────────┬──────────────────────────┬──────────────────────────────┬──────────────────────────────┐
│              │ Type 1 — Overwrite       │ Type 2 — New Row             │ Type 3 — New Column          │
├──────────────┼──────────────────────────┼──────────────────────────────┼──────────────────────────────┤
│ Strategy     │ Update in place          │ Insert new record            │ Add 'previous_value' column  │
│ History kept │ None                     │ Full history (all versions)  │ One prior state only         │
│ Row count    │ 1 per entity             │ N per entity (1 per version) │ 1 per entity                 │
│ Surrogate key│ Reused                   │ New key per version          │ Reused                       │
│ Complexity   │ Low                      │ High                         │ Medium                       │
│ Storage      │ Lowest                   │ Highest                      │ Medium                       │
│ Best for     │ Corrections, typos       │ Tracking changes over time   │ Compare current vs. prior    │
│ Example      │ Fixing a misspelled name │ Customer address history     │ Customer tier upgrades       │
└──────────────┴──────────────────────────┴──────────────────────────────┴──────────────────────────────┘
        """, language="text")
        st.markdown("#### Type 1 — Overwrite")
        st.code("""
UPDATE dim_customer SET email = 'new@email.com' WHERE customer_id = 'C001';
        """, language="sql")
        st.markdown("#### Type 2 — New Row")
        st.code("""
-- Expire old
UPDATE dim_customer SET expiry_date = CURRENT_DATE - 1, is_current = FALSE
WHERE  customer_id = 'C001' AND is_current = TRUE;
-- Insert new version
INSERT INTO dim_customer (customer_id, email, city, effective_date, expiry_date, is_current)
VALUES ('C001', 'new@email.com', 'Manila', CURRENT_DATE, NULL, TRUE);
        """, language="sql")
        st.markdown("#### Type 3 — New Column")
        st.code("""
UPDATE dim_customer
SET    prev_email    = email,
       email         = 'new@email.com',
       email_changed = CURRENT_DATE
WHERE  customer_id = 'C001';
        """, language="sql")
        st.markdown("#### Decision Guide")
        st.write("""
- **Type 1**: No history needed. Corrections, name fixes. Simple.
- **Type 2**: Full history required. Regulatory, audit, time-series analysis. Most common.
- **Type 3**: Only need to compare 'before vs. after'. Simple reporting. Limited.
- **Type 4 (mini-dimension)**: High-change attributes split into a separate small dimension.
- **Type 6 (hybrid)**: Combines Type 1+2+3 — current attribute + historical rows + prior column.
        """)

    # ── Example 18 ────────────────────────────────────────────────────────────
    with st.expander("✅ Example 18 — Semi-Additive Facts: Account Balances", expanded=True):
        st.markdown("#### Overview")
        st.write("Semi-additive facts can be summed across some dimensions (accounts) but NOT across time. Account balances are the canonical example — you sum across accounts but average (or pick a snapshot) across time.")
        st.markdown("#### Grain")
        st.info("One row per account per day (daily balance snapshot).")
        st.markdown("#### Schema Diagram")
        st.code("""
┌──────────────────┐   ┌────────────────────────────────┐   ┌─────────────────┐
│   dim_account    │   │   fact_account_balance_daily   │   │   dim_date      │
│──────────────────│   │────────────────────────────────│   │─────────────────│
│ account_key   PK ├──►│ balance_key     PK             │◄──┤ date_key PK     │
│ account_id       │   │ account_key     FK             │   │ full_date       │
│ account_type     │   │ date_key        FK             │   │ month / year    │
│ currency         │   │ customer_key    FK             │   │ end_of_month    │
│ open_date        │   │ opening_balance NUMERIC        │   └─────────────────┘
│ status           │   │ closing_balance NUMERIC        │
└──────────────────┘   │ deposits        NUMERIC        │
                       │ withdrawals     NUMERIC        │
                       │ interest_earned NUMERIC        │
                       └────────────────────────────────┘

opening_balance / closing_balance  = SEMI-ADDITIVE (sum across accounts ✓, sum across time ✗)
deposits / withdrawals / interest  = FULLY ADDITIVE (sum across all dimensions ✓)
        """, language="text")
        st.markdown("#### DDL")
        st.code("""
CREATE TABLE fact_account_balance_daily (
    balance_key       BIGINT  PRIMARY KEY,
    account_key       INT     NOT NULL REFERENCES dim_account(account_key),
    customer_key      INT     NOT NULL REFERENCES dim_customer(customer_key),
    date_key          INT     NOT NULL REFERENCES dim_date(date_key),
    opening_balance   NUMERIC(18,4),   -- semi-additive
    closing_balance   NUMERIC(18,4),   -- semi-additive
    deposits          NUMERIC(18,4),   -- fully additive
    withdrawals       NUMERIC(18,4),   -- fully additive
    interest_earned   NUMERIC(18,4)    -- fully additive
);
        """, language="sql")
        st.markdown("#### Sample Queries — Correct vs Incorrect Aggregation")
        st.code("""
-- ✅ CORRECT: Total balance across all accounts on a specific date
SELECT d.full_date, SUM(f.closing_balance) AS total_aum
FROM   fact_account_balance_daily f
JOIN   dim_date d ON f.date_key = d.date_key
WHERE  d.full_date = '2024-12-31'
GROUP  BY d.full_date;

-- ✅ CORRECT: Month-end balance using end_of_month flag
SELECT d.full_date, a.account_type, SUM(f.closing_balance) AS balance
FROM   fact_account_balance_daily f
JOIN   dim_date    d ON f.date_key    = d.date_key
JOIN   dim_account a ON f.account_key = a.account_key
WHERE  d.end_of_month = TRUE
GROUP  BY d.full_date, a.account_type;

-- ❌ WRONG: SUMing closing_balance across all dates → inflated totals
-- SELECT SUM(closing_balance) FROM fact_account_balance_daily
-- WHERE date_key BETWEEN x AND y;  ← DO NOT do this
        """, language="sql")
        st.markdown("#### Design Decisions")
        st.write("""
- `closing_balance` is semi-additive — document this clearly in your data catalog
- `deposits` and `withdrawals` are fully additive — safe to SUM across any dimension
- `end_of_month` flag on `dim_date` simplifies month-end balance extraction
- For monthly summaries, use last-day-of-month snapshot, not SUM of daily balances
        """)

    # ── Example 19 ────────────────────────────────────────────────────────────
    with st.expander("✅ Example 19 — Factless Fact Table: Course Enrollment", expanded=True):
        st.markdown("#### Overview")
        st.write("A factless fact table records events or coverage relationships with no natural numeric measure. This example tracks student course enrollments — the existence of the row IS the fact.")
        st.markdown("#### Grain")
        st.info("One row per student–course enrollment event.")
        st.markdown("#### Schema Diagram")
        st.code("""
┌──────────────────┐   ┌──────────────────────────────────┐   ┌──────────────────┐
│   dim_student    │   │   fact_enrollment (factless)     │   │   dim_course     │
│──────────────────│   │──────────────────────────────────│   │──────────────────│
│ student_key   PK ├──►│ enrollment_key    PK             │◄──┤ course_key    PK │
│ student_id       │   │ student_key       FK             │   │ course_code      │
│ full_name        │   │ course_key        FK             │   │ course_name      │
│ major            │   │ instructor_key    FK             │   │ department       │
│ year_level       │   │ date_key          FK             │   │ credits          │
│ gpa              │   │ enrollment_type   VARCHAR        │   │ format           │
└──────────────────┘   │ -- no numeric measures --        │   └──────────────────┘
                       └──────────────────────────────────┘
                                  │
                     ┌────────────▼────────┐
                     │   dim_instructor    │
                     │─────────────────────│
                     │ instructor_key   PK │
                     │ instructor_name     │
                     │ department          │
                     └─────────────────────┘
        """, language="text")
        st.markdown("#### DDL")
        st.code("""
CREATE TABLE fact_enrollment (
    enrollment_key   BIGINT PRIMARY KEY,
    student_key      INT NOT NULL REFERENCES dim_student(student_key),
    course_key       INT NOT NULL REFERENCES dim_course(course_key),
    instructor_key   INT NOT NULL REFERENCES dim_instructor(instructor_key),
    date_key         INT NOT NULL REFERENCES dim_date(date_key),
    enrollment_type  VARCHAR(50)   -- 'regular', 'waitlist', 'audit'
    -- No numeric measures — COUNT(*) IS the measure
);
        """, language="sql")
        st.markdown("#### Sample Queries")
        st.code("""
-- Enrollments per course
SELECT c.course_name, c.department, COUNT(*) AS enrolled_students
FROM   fact_enrollment f
JOIN   dim_course c ON f.course_key = c.course_key
GROUP  BY c.course_name, c.department
ORDER  BY enrolled_students DESC;

-- Students taking more than 5 courses this semester
SELECT s.full_name, s.year_level, COUNT(*) AS courses_enrolled
FROM   fact_enrollment f
JOIN   dim_student s ON f.student_key = s.student_key
JOIN   dim_date    d ON f.date_key    = d.date_key
WHERE  d.year = 2024 AND d.semester = 'Fall'
GROUP  BY s.full_name, s.year_level
HAVING COUNT(*) > 5;

-- Coverage gap: courses with ZERO enrollments (LEFT JOIN anti-pattern)
SELECT c.course_name
FROM   dim_course c
LEFT   JOIN fact_enrollment f ON c.course_key = f.course_key
WHERE  f.course_key IS NULL;
        """, language="sql")
        st.markdown("#### Design Decisions")
        st.write("""
- No numeric measures — `COUNT(*)` is the only meaningful aggregation
- `enrollment_type` is low-cardinality — kept in fact to avoid junk dimension overhead
- Coverage queries (zero enrollments) use LEFT JOIN anti-pattern
- A second factless fact can track course completions separately for pass/fail analysis
        """)

    # ── Example 20 ────────────────────────────────────────────────────────────
    with st.expander("✅ Example 20 — dbt Project Layout: Staging → Intermediate → Mart", expanded=True):
        st.markdown("#### Overview")
        st.write("A dbt project architecture pattern organizing SQL models into three layers: Staging (raw source cleaning), Intermediate (business logic), and Mart (final Kimball-style tables for BI).")
        st.markdown("#### Folder Structure")
        st.code("""
models/
├── staging/                        ← Layer 1: One-to-one with source tables
│   ├── salesforce/
│   │   ├── _salesforce__sources.yml
│   │   ├── stg_salesforce__leads.sql
│   │   ├── stg_salesforce__opportunities.sql
│   │   └── stg_salesforce__accounts.sql
│   ├── stripe/
│   │   ├── stg_stripe__charges.sql
│   │   └── stg_stripe__subscriptions.sql
│   └── postgres_app/
│       ├── stg_app__users.sql
│       └── stg_app__events.sql
│
├── intermediate/                   ← Layer 2: Business logic & joins
│   ├── int_orders_enriched.sql
│   ├── int_customer_lifetime_value.sql
│   └── int_mrr_movements.sql
│
└── marts/                          ← Layer 3: Kimball star schema for BI
    ├── core/
    │   ├── dim_customer.sql
    │   ├── dim_product.sql
    │   ├── dim_date.sql
    │   └── fct_orders.sql
    ├── marketing/
    │   ├── dim_campaign.sql
    │   └── fct_ad_performance.sql
    └── finance/
        ├── fct_subscription_monthly.sql
        └── fct_account_balances.sql
        """, language="text")
        st.markdown("#### Layer 1 — Staging (`stg_salesforce__leads.sql`)")
        st.code("""
-- Purpose: rename and cast raw Salesforce fields. No joins. No business logic.
WITH source AS (
    SELECT * FROM {{ source('salesforce', 'leads') }}
),
renamed AS (
    SELECT
        id               AS lead_id,
        name             AS full_name,
        email            AS email,
        company          AS company_name,
        status           AS lead_status,
        leadsource       AS lead_source,
        isconverted      AS is_converted,
        converteddate    AS converted_date,
        createddate      AS created_at,
        lastmodifieddate AS updated_at
    FROM source
    WHERE isdeleted = FALSE
)
SELECT * FROM renamed
        """, language="sql")
        st.markdown("#### Layer 2 — Intermediate (`int_mrr_movements.sql`)")
        st.code("""
-- Purpose: classify MRR movements from subscription events.
WITH subscriptions AS (
    SELECT * FROM {{ ref('stg_stripe__subscriptions') }}
),
lagged AS (
    SELECT
        customer_id, subscription_id, mrr, status, event_date,
        LAG(mrr)    OVER (PARTITION BY customer_id ORDER BY event_date) AS prev_mrr,
        LAG(status) OVER (PARTITION BY customer_id ORDER BY event_date) AS prev_status
    FROM subscriptions
),
classified AS (
    SELECT *,
        CASE
            WHEN prev_status IS NULL  THEN 'new'
            WHEN status = 'canceled'  THEN 'churned'
            WHEN mrr > prev_mrr       THEN 'expansion'
            WHEN mrr < prev_mrr       THEN 'contraction'
            ELSE                           'retained'
        END AS mrr_movement_type,
        mrr - COALESCE(prev_mrr, 0) AS mrr_delta
    FROM lagged
)
SELECT * FROM classified
        """, language="sql")
        st.markdown("#### Layer 3 — Mart (`fct_orders.sql`)")
        st.code("""
-- Purpose: final fact table — assembly only, minimal transformation.
WITH orders    AS (SELECT * FROM {{ ref('stg_app__orders') }}),
     customers AS (SELECT * FROM {{ ref('dim_customer') }}),
     products  AS (SELECT * FROM {{ ref('dim_product') }}),
     dates     AS (SELECT * FROM {{ ref('dim_date') }})

SELECT
    {{ dbt_utils.generate_surrogate_key(['o.order_id', 'o.line_item_id']) }} AS order_line_key,
    c.customer_key,
    p.product_key,
    d.date_key,
    o.order_id,
    o.quantity,
    o.unit_price,
    o.quantity * o.unit_price             AS gross_revenue,
    o.discount_amount,
    o.quantity * o.unit_price
      - o.discount_amount                 AS net_revenue
FROM   orders    o
JOIN   customers c ON o.customer_id = c.customer_id AND c.is_current = TRUE
JOIN   products  p ON o.product_id  = p.product_id
JOIN   dates     d ON o.order_date  = d.full_date
        """, language="sql")
        st.markdown("#### schema.yml — Tests & Documentation")
        st.code("""
version: 2
models:
  - name: fct_orders
    description: "One row per order line item. Grain: order_id + line_item_id."
    columns:
      - name: order_line_key
        tests: [unique, not_null]
      - name: customer_key
        tests: [not_null, relationships: {to: ref('dim_customer'), field: customer_key}]
      - name: net_revenue
        description: "Gross revenue minus discount. Additive across all dimensions."
        tests: [not_null]
        """, language="yaml")
        st.markdown("#### Design Decisions")
        st.write("""
- **Staging**: rename only, no joins, no business logic — one model per source table
- **Intermediate**: business logic lives here — MRR classification, CLV, enrichments
- **Mart**: final star schema optimized for BI — minimal transformations, only assembly
- `{{ ref() }}` in dbt auto-builds the DAG — no manual dependency tracking
- `schema.yml` tests (`unique`, `not_null`, `relationships`) catch data quality issues in CI
        """)

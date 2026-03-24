import streamlit as st
import pandas as pd
import io
import re


class DataCleaningSQL:
    def __init__(self):
        self.data = [
            [1001, "John Smith",         "john.smith@gmail.com", "2023-11-02",
                "Apple Watch",       1,    399.99,  "usa",           "Delivered",  "-"],
            [1002, "john smith",         "john.smith@gmail.com", "11/02/2023",  "apple watch",
                1,    399.99,  "USA",           "delivered",  "Duplicate name?"],
            [1003, "SARAH THOMPSON",     "sarah.t@gmail.com",    "2023/10/30",  "Samsung Galaxy S22",
                "two", 799.00, "United States", "shipped",    "customer requested refund"],
            [1004, "Tom O'Brien",        None,                   "2023-11-05",
                "Google Pixel",      1,    599.00,  "UK",            "Delivered",  "NULL"],
            [1005, "Mary Johnson",       "mary.j@gmail.com",     "2023-11-06",  "Samsung Galaxy S22",
                2,    800.00,  "United Kingdom", "returned",   "Return due to defect"],
            [1006, "Ankit Patel",        "ankit@@patel.com",     "2023-11-07",  "NULL",
                1,    0.00,    "india",         "pending",    "no stock"],
            [1007, "John Smith",         "john.smith@gmail.com", "2023-11-02",
                "Apple Watch",       1,    399.99,  "usa",           "delivered",  "Duplicate?"],
            [1008, "Carlos Hernández",   "carlos@hernandez.com", "2023-11-08",
                "Iphone 14",         1,    1099.00, "spain",         "DELIVERED",  "-"],
            [1009, "NULL",               "jessica@abc.com",      "2023-11-09",  "Macbook Pro",
                1,    1299.99, "canada",        "returned",   "Missing name"],
            [1010, "Aisha Khan",         "aisha.khan@outlook",   "2023-11-10",  "MacBook Pro",
                1,    1299.99, "CANADA",        "Returned",   "check eligibility"],
            [1011, "Sarah Thompson",     "sarah.t@gmail.com",    "2023-10-30",  "Samsung Galaxy S22",
                2,    799.00,  "US",            "refunded",   "updated payment method"],
            [1012, "tom o'brien",        "tom.obrien@gmail.com", "2023-11-05",
                "Google pixel",      1,    599.00,  "uk",            "Delivered",  "no comment"],
            [1013, "Mary Johnson",       "mary.j@gmail.com",     "2023-11-06",
                "SAMSUNG GALAXY S22", 2,    800.00,  "UK",            "Returned",   None],
            [1014, "Ankit Patel",        "ankit@patel.com",      "2023-11-07",
                "Samsung Galaxy S22", 1,    None,    "India",         "Pending",    "missing price"],
            [1015, "Carlos Hernández",   "carlos@hernandez.com", "2023-11-08",  "iPhone 14",
                1,    1099.00, "Spain",         "delivered",  "duplicate product format"],
        ]
        self.columns = [
            "order_id", "customer_name", "email", "order_date",
            "product_name", "quantity", "price", "country",
            "order_status", "notes"
        ]
        self.df = pd.DataFrame(self.data, columns=self.columns)

    # ─────────────────────────────────────────────
    # STEP 1 – Inspect
    # ─────────────────────────────────────────────
    def step_1_inspect_data(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1976d2;margin:0.3rem 0;'>🔍 Step 1 – Initial Data Inspection</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "Examine structure, quality, and basic statistics before touching anything")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- View table structure (PostgreSQL)
SELECT
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'customer_orders'
ORDER BY ordinal_position;

-- Preview data
SELECT * FROM customer_orders LIMIT 10;

-- Row count & duplicate check
SELECT
    COUNT(*)                      AS total_rows,
    COUNT(DISTINCT order_id)      AS unique_orders,
    COUNT(*) - COUNT(DISTINCT order_id) AS duplicates
FROM customer_orders;

-- Basic statistics
SELECT
    COUNT(*)                        AS total_records,
    COUNT(DISTINCT order_id)        AS unique_orders,
    COUNT(DISTINCT customer_name)   AS unique_customers,
    COUNT(DISTINCT product_name)    AS unique_products,
    MIN(order_date)                 AS earliest_order,
    MAX(order_date)                 AS latest_order,
    ROUND(AVG(price)::NUMERIC, 2)   AS avg_price,
    COUNT(DISTINCT country)         AS countries
FROM customer_orders;

-- Quick data quality scan
SELECT 'Missing email'        AS issue, COUNT(*) AS count
FROM customer_orders WHERE email IS NULL OR email = ''
UNION ALL
SELECT 'String NULL name',    COUNT(*)
FROM customer_orders WHERE UPPER(TRIM(customer_name)) = 'NULL'
UNION ALL
SELECT 'String NULL product', COUNT(*)
FROM customer_orders WHERE UPPER(TRIM(product_name))  = 'NULL'
UNION ALL
SELECT 'Zero/NULL price',     COUNT(*)
FROM customer_orders WHERE price IS NULL OR price = 0
UNION ALL
SELECT 'Invalid email',       COUNT(*)
FROM customer_orders
WHERE email NOT LIKE '%@%.%'
   OR email LIKE '%@@%';""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 SQL Tip:</strong><br>
                    Inspect raw data before writing any cleaning logic.
                    Look for mixed casing, string "NULL" values, invalid
                    email formats, and inconsistent product/status names.
                </div>""", unsafe_allow_html=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ Best Practice:</strong><br>
                    • Document original schema before any changes<br>
                    • Check both true NULLs and string "NULL" literals<br>
                    • Identify duplicate key combinations early<br>
                    • Note columns with mixed formats (dates, prices)
                </div>""", unsafe_allow_html=True)

            with col_result:
                st.markdown("**Table Structure**")
                structure_data = {
                    "Column":   self.df.columns.tolist(),
                    "Type":     [str(d) for d in self.df.dtypes],
                    "Nullable": ["YES" if self.df[c].isnull().any() else "NO"
                                 for c in self.df.columns],
                }
                st.dataframe(pd.DataFrame(structure_data),
                             hide_index=True, width='stretch')

                st.markdown("**Data Preview (LIMIT 5)**")
                st.dataframe(self.df.head(5), width='stretch')

                st.markdown("**Basic Statistics**")
                c1, c2 = st.columns(2)
                c1.metric("Total Records",    len(self.df))
                c2.metric("Unique Orders",    self.df["order_id"].nunique())
                c1.metric("Unique Customers",
                          self.df["customer_name"].nunique())
                c2.metric(
                    "Unique Products",  self.df["product_name"].str.upper().str.strip().nunique())
                c1.metric("Missing Email",    int(
                    self.df["email"].isnull().sum()))
                c2.metric("Countries",
                          self.df["country"].str.strip().str.upper().nunique())

        st.divider()

    # ─────────────────────────────────────────────
    # STEP 2 – Standardize order_status (Query 1)
    # ─────────────────────────────────────────────
    def step_2_order_status(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1976d2;margin:0.3rem 0;'>📦 Step 2 – Standardize order_status</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "Use LIKE pattern matching to collapse messy status variants into canonical values")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- PostgreSQL: standardise order_status with LIKE
SELECT
    order_id,
    order_status AS raw_status,
    CASE
        WHEN LOWER(order_status) LIKE '%deliver%' THEN 'Delivered'
        WHEN LOWER(order_status) LIKE '%return%'  THEN 'Returned'
        WHEN LOWER(order_status) LIKE '%refund%'  THEN 'Refunded'
        WHEN LOWER(order_status) LIKE '%pend%'    THEN 'Pending'
        WHEN LOWER(order_status) LIKE '%ship%'    THEN 'Shipped'
        ELSE 'Other'
    END AS cleaned_order_status
FROM customer_orders;

-- Apply update in place
UPDATE customer_orders
SET order_status = CASE
    WHEN LOWER(order_status) LIKE '%deliver%' THEN 'Delivered'
    WHEN LOWER(order_status) LIKE '%return%'  THEN 'Returned'
    WHEN LOWER(order_status) LIKE '%refund%'  THEN 'Refunded'
    WHEN LOWER(order_status) LIKE '%pend%'    THEN 'Pending'
    WHEN LOWER(order_status) LIKE '%ship%'    THEN 'Shipped'
    ELSE 'Other'
END;

-- Verify distinct values after cleaning
SELECT order_status, COUNT(*) AS count
FROM customer_orders
GROUP BY order_status
ORDER BY count DESC;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 BigQuery → PostgreSQL:</strong><br>
                    Both use single quotes for string literals.
                    BigQuery allows double quotes; PostgreSQL does not —
                    always use <code>'Delivered'</code> not
                    <code>"Delivered"</code> in PostgreSQL.
                </div>""", unsafe_allow_html=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ Best Practice:</strong><br>
                    • Always <code>LOWER()</code> before LIKE matching<br>
                    • Use partial patterns (%deliver%) to catch variants<br>
                    • Map to a fixed enum list to prevent future drift<br>
                    • Add a CHECK constraint after standardising
                </div>""", unsafe_allow_html=True)

            with col_result:
                st.markdown("**Raw order_status variants**")
                raw_counts = self.df["order_status"].value_counts(
                ).reset_index()
                raw_counts.columns = ["order_status", "count"]
                st.dataframe(raw_counts, hide_index=True,
                             width='stretch')

                # apply
                def clean_status(s):
                    if pd.isna(s):
                        return "Other"
                    s = str(s).lower()
                    if "deliver" in s:
                        return "Delivered"
                    if "return" in s:
                        return "Returned"
                    if "refund" in s:
                        return "Refunded"
                    if "pend" in s:
                        return "Pending"
                    if "ship" in s:
                        return "Shipped"
                    return "Other"

                before = self.df[["order_id", "order_status"]].copy()
                self.df["order_status"] = self.df["order_status"].apply(
                    clean_status)

                st.markdown("**Before → After (sample)**")
                compare = before.copy()
                compare["cleaned"] = self.df["order_status"]
                st.dataframe(compare, hide_index=True,
                             width='stretch')

                st.markdown("**Distinct values after cleaning:**")
                clean_counts = self.df["order_status"].value_counts(
                ).reset_index()
                clean_counts.columns = ["order_status", "count"]
                st.dataframe(clean_counts, hide_index=True,
                             width='stretch')
                st.success("✅ order_status standardised to 5 canonical values")

        st.divider()

    # ─────────────────────────────────────────────
    # STEP 3 – Standardize product_name (Query 2)
    # ─────────────────────────────────────────────
    def step_3_product_name(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1976d2;margin:0.3rem 0;'>📱 Step 3 – Standardize product_name</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "Collapse all product name variants into exact canonical brand names")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- PostgreSQL: normalise product names
SELECT
    order_id,
    product_name AS raw_product,
    CASE
        WHEN LOWER(product_name) LIKE '%apple watch%'       THEN 'Apple Watch'
        WHEN LOWER(product_name) LIKE '%samsung galaxy s22%' THEN 'Samsung Galaxy S22'
        WHEN LOWER(product_name) LIKE '%google pixel%'      THEN 'Google Pixel'
        WHEN LOWER(product_name) LIKE '%macbook pro%'       THEN 'MacBook Pro'
        WHEN LOWER(product_name) LIKE '%iphone 14%'         THEN 'iPhone 14'
        ELSE 'Other'
    END AS clean_product_name
FROM customer_orders;

-- Apply update
UPDATE customer_orders
SET product_name = CASE
    WHEN LOWER(product_name) LIKE '%apple watch%'        THEN 'Apple Watch'
    WHEN LOWER(product_name) LIKE '%samsung galaxy s22%' THEN 'Samsung Galaxy S22'
    WHEN LOWER(product_name) LIKE '%google pixel%'       THEN 'Google Pixel'
    WHEN LOWER(product_name) LIKE '%macbook pro%'        THEN 'MacBook Pro'
    WHEN LOWER(product_name) LIKE '%iphone 14%'          THEN 'iPhone 14'
    ELSE NULL  -- NULL out unrecognised products for review
END
WHERE UPPER(TRIM(product_name)) != 'NULL'
   OR product_name IS NOT NULL;

-- NULL out string 'NULL' product rows
UPDATE customer_orders
SET product_name = NULL
WHERE UPPER(TRIM(product_name)) = 'NULL';

-- Verify
SELECT product_name, COUNT(*) AS count
FROM customer_orders
GROUP BY product_name
ORDER BY count DESC;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 SQL Tip:</strong><br>
                    The original queries had mismatched quotes
                    (<code>"Google Pixel"</code>, unclosed
                    <code>'MacBook Pro</code>). In PostgreSQL, all
                    string literals must use single quotes and be
                    properly closed.
                </div>""", unsafe_allow_html=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ Best Practice:</strong><br>
                    • Use LOWER() + LIKE for fuzzy matching<br>
                    • Map to exact canonical brand casing (iPhone not Iphone)<br>
                    • NULL unrecognised products — don't silently label 'Other'<br>
                    • Maintain a product reference table for large catalogues
                </div>""", unsafe_allow_html=True)

            with col_result:
                st.markdown("**Raw product_name variants**")
                raw = self.df["product_name"].value_counts().reset_index()
                raw.columns = ["product_name", "count"]
                st.dataframe(raw, hide_index=True, width='stretch')

                def clean_product(p):
                    if pd.isna(p) or str(p).upper().strip() == "NULL":
                        return None
                    p = str(p).lower()
                    if "apple watch" in p:
                        return "Apple Watch"
                    if "samsung galaxy s22" in p:
                        return "Samsung Galaxy S22"
                    if "google pixel" in p:
                        return "Google Pixel"
                    if "macbook pro" in p:
                        return "MacBook Pro"
                    if "iphone 14" in p:
                        return "iPhone 14"
                    return None

                before = self.df[["order_id", "product_name"]].copy()
                self.df["product_name"] = self.df["product_name"].apply(
                    clean_product)

                st.markdown("**Before → After (sample)**")
                compare = before.copy()
                compare["cleaned"] = self.df["product_name"]
                st.dataframe(compare, hide_index=True,
                             width='stretch')

                clean = self.df["product_name"].value_counts(
                    dropna=False).reset_index()
                clean.columns = ["product_name", "count"]
                st.markdown("**After standardisation:**")
                st.dataframe(clean, hide_index=True, width='stretch')
                st.success("✅ Product names mapped to 5 canonical brands")

        st.divider()

    # ─────────────────────────────────────────────
    # STEP 4 – Clean quantity field (Query 3)
    # ─────────────────────────────────────────────
    def step_4_quantity(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1976d2;margin:0.3rem 0;'>🔢 Step 4 – Clean quantity Field</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "Convert text numbers ('two') to integers and cast the whole column to INTEGER")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- PostgreSQL: convert text words to integers
SELECT
    order_id,
    quantity AS raw_quantity,
    CASE
        WHEN LOWER(quantity::TEXT) = 'one'   THEN 1
        WHEN LOWER(quantity::TEXT) = 'two'   THEN 2
        WHEN LOWER(quantity::TEXT) = 'three' THEN 3
        WHEN LOWER(quantity::TEXT) = 'four'  THEN 4
        WHEN LOWER(quantity::TEXT) = 'five'  THEN 5
        ELSE quantity::INTEGER
    END AS clean_quantity
FROM customer_orders;

-- Step 1: Update text words to numeric strings
UPDATE customer_orders
SET quantity = CASE
    WHEN LOWER(quantity::TEXT) = 'one'   THEN '1'
    WHEN LOWER(quantity::TEXT) = 'two'   THEN '2'
    WHEN LOWER(quantity::TEXT) = 'three' THEN '3'
    WHEN LOWER(quantity::TEXT) = 'four'  THEN '4'
    WHEN LOWER(quantity::TEXT) = 'five'  THEN '5'
    ELSE quantity::TEXT
END;

-- Step 2: Cast column to INTEGER
ALTER TABLE customer_orders
ALTER COLUMN quantity TYPE INTEGER
    USING quantity::INTEGER;

-- Verify
SELECT
    MIN(quantity) AS min_qty,
    MAX(quantity) AS max_qty,
    AVG(quantity) AS avg_qty,
    COUNT(*) FILTER (WHERE quantity IS NULL) AS null_count
FROM customer_orders;

-- Note: BigQuery uses CAST(quantity AS INT64)
-- PostgreSQL equivalent is quantity::INTEGER
-- or CAST(quantity AS INTEGER)""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 BigQuery → PostgreSQL:</strong><br>
                    BigQuery uses <code>CAST(col AS INT64)</code>.
                    PostgreSQL uses <code>col::INTEGER</code> or
                    <code>CAST(col AS INTEGER)</code>.
                    There is no INT64 type in PostgreSQL — use
                    <code>INTEGER</code> (32-bit) or <code>BIGINT</code>
                    (64-bit).
                </div>""", unsafe_allow_html=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ Best Practice:</strong><br>
                    • Handle all written-out numbers before casting<br>
                    • NULL out values that cannot be converted<br>
                    • Add a CHECK constraint: quantity &gt;= 1<br>
                    • Validate range after conversion
                </div>""", unsafe_allow_html=True)

            with col_result:
                st.markdown("**Raw quantity values**")
                raw = self.df["quantity"].value_counts(
                    dropna=False).reset_index()
                raw.columns = ["quantity", "count"]
                st.dataframe(raw, hide_index=True, width='stretch')

                text_map = {"one": 1, "two": 2,
                            "three": 3, "four": 4, "five": 5}

                before = self.df[["order_id", "quantity"]].copy()
                self.df["quantity"] = self.df["quantity"].apply(
                    lambda x: text_map.get(
                        str(x).lower().strip(), x) if pd.notna(x) else x
                )
                self.df["quantity"] = pd.to_numeric(
                    self.df["quantity"], errors="coerce").astype("Int64")

                st.markdown("**Before → After (all rows)**")
                compare = before.copy()
                compare["cleaned"] = self.df["quantity"]
                st.dataframe(compare, hide_index=True,
                             width='stretch')

                c1, c2 = st.columns(2)
                c1.metric("Min Qty", int(self.df["quantity"].min()))
                c2.metric("Max Qty", int(self.df["quantity"].max()))
                c1.metric("Avg Qty", f'{self.df["quantity"].mean():.2f}')
                c2.metric("NULL count", int(
                    self.df["quantity"].isnull().sum()))
                st.success("✅ quantity cast to INTEGER; 'two' → 2")

        st.divider()

    # ─────────────────────────────────────────────
    # STEP 5 – Clean customer_name (Query 4)
    # ─────────────────────────────────────────────
    def step_5_customer_name(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1976d2;margin:0.3rem 0;'>👤 Step 5 – Clean customer_name Field</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "Apply INITCAP for proper Title Case and replace string 'NULL' with true NULL")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- PostgreSQL: INITCAP + handle string NULLs
SELECT
    order_id,
    customer_name AS raw_name,
    INITCAP(TRIM(customer_name)) AS clean_customer_name
FROM customer_orders
WHERE customer_name IS NOT NULL
  AND UPPER(TRIM(customer_name)) != 'NULL';

-- Step 1: replace string 'NULL' with true NULL
UPDATE customer_orders
SET customer_name = NULL
WHERE UPPER(TRIM(customer_name)) = 'NULL';

-- Step 2: apply INITCAP and TRIM
UPDATE customer_orders
SET customer_name = INITCAP(TRIM(customer_name))
WHERE customer_name IS NOT NULL;

-- Verify: check for remaining casing issues
SELECT DISTINCT customer_name
FROM customer_orders
ORDER BY customer_name;

-- Optional: flag rows with missing names
ALTER TABLE customer_orders
ADD COLUMN name_missing BOOLEAN
    GENERATED ALWAYS AS (customer_name IS NULL) STORED;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 SQL Tip:</strong><br>
                    <code>INITCAP()</code> works well for most names but
                    may mis-capitalise names like <em>O'Brien</em>
                    → <em>O'brien</em>. For production, consider a
                    curated name lookup or application-layer formatting.
                </div>""", unsafe_allow_html=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ Best Practice:</strong><br>
                    • Always replace string 'NULL' before INITCAP<br>
                    • TRIM before INITCAP to avoid leading-space bugs<br>
                    • Do NOT drop rows with NULL names — flag them<br>
                    • Validate with DISTINCT after update
                </div>""", unsafe_allow_html=True)

            with col_result:
                st.markdown("**Raw customer_name values**")
                raw = self.df[["order_id", "customer_name"]].copy()
                st.dataframe(raw, hide_index=True, width='stretch')

                # replace string NULL
                self.df["customer_name"] = self.df["customer_name"].apply(
                    lambda x: None if pd.isna(x) or str(
                        x).upper().strip() == "NULL" else x
                )
                # INITCAP
                self.df["customer_name"] = self.df["customer_name"].apply(
                    lambda x: x.strip().title() if pd.notna(x) else x
                )

                st.markdown("**After INITCAP + NULL fix:**")
                after = self.df[["order_id", "customer_name"]]
                st.dataframe(after, hide_index=True, width='stretch')

                null_names = int(self.df["customer_name"].isnull().sum())
                c1, c2 = st.columns(2)
                c1.metric("Unique Names", self.df["customer_name"].nunique())
                c2.metric("NULL Names",   null_names)
                st.success("✅ customer_name cleaned and title-cased")

        st.divider()

    # ─────────────────────────────────────────────
    # STEP 6 – Remove Duplicate Orders (Query 5)
    # ─────────────────────────────────────────────
    def step_6_duplicates(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1976d2;margin:0.3rem 0;'>🔁 Step 6 – Remove Duplicate Orders</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "Partition by email + product to find semantic duplicates and keep the earliest order")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- PostgreSQL: ROW_NUMBER() deduplication
-- Partition by lowercase email + product name
SELECT *
FROM (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY
                LOWER(email),
                LOWER(product_name)
            ORDER BY order_id
        ) AS rn
    FROM customer_orders
) sub
WHERE rn = 1;

-- Alternative: DELETE duplicates directly
DELETE FROM customer_orders
WHERE order_id NOT IN (
    SELECT MIN(order_id)
    FROM customer_orders
    GROUP BY
        LOWER(email),
        LOWER(product_name)
);

-- How many duplicates exist?
SELECT
    LOWER(email)        AS email_lower,
    LOWER(product_name) AS product_lower,
    COUNT(*)            AS occurrence_count,
    STRING_AGG(order_id::TEXT, ', ' ORDER BY order_id) AS order_ids
FROM customer_orders
GROUP BY LOWER(email), LOWER(product_name)
HAVING COUNT(*) > 1;

-- Create deduplicated view
CREATE VIEW customer_orders_deduped AS
SELECT * FROM (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY LOWER(email), LOWER(product_name)
            ORDER BY order_id
        ) AS rn
    FROM customer_orders
) sub
WHERE rn = 1;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 BigQuery → PostgreSQL:</strong><br>
                    BigQuery uses <code>SELECT * EXCEPT(rn)</code> to
                    drop the row-number column. PostgreSQL has no
                    <code>EXCEPT</code> column syntax — wrap in a
                    subquery and alias, or list columns explicitly.
                    <code>ROW_NUMBER()</code> syntax is identical.
                </div>""", unsafe_allow_html=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ Deduplication Strategy:</strong><br>
                    • Partition by email + product (semantic duplicate)<br>
                    • Keep lowest order_id (earliest order)<br>
                    • Use LOWER() so casing doesn't hide duplicates<br>
                    • Always preview before DELETE
                </div>""", unsafe_allow_html=True)

            with col_result:
                st.markdown("**Duplicate Analysis**")
                total_before = len(self.df)

                # find duplicates
                key = ["email_lower", "product_lower"]
                self.df["email_lower"] = self.df["email"].fillna(
                    "").str.lower()
                self.df["product_lower"] = self.df["product_name"].fillna(
                    "").str.lower()
                self.df["rn"] = self.df.groupby(
                    key)["order_id"].rank(method="first").astype(int)

                dup_rows = self.df[self.df["rn"] > 1]
                dup_groups = self.df.groupby(key).filter(lambda x: len(x) > 1)

                c1, c2 = st.columns(2)
                c1.metric("Total Before", total_before)
                c2.metric("Duplicate Rows", len(dup_rows))

                if not dup_rows.empty:
                    st.warning(f"⚠️ {len(dup_rows)} duplicate row(s) found")
                    st.markdown("**Duplicate records (rn > 1):**")
                    st.dataframe(
                        dup_groups.sort_values(
                            ["email_lower", "product_lower", "order_id"])
                        [["order_id", "customer_name", "email",
                            "product_name", "order_status"]],
                        hide_index=True, width='stretch'
                    )

                # keep rn == 1
                self.df = self.df[self.df["rn"] == 1].drop(
                    columns=["email_lower", "product_lower", "rn"])

                c1.metric("Rows After Dedup", len(self.df))
                c2.metric("Removed", total_before - len(self.df))
                st.success(
                    f"✅ Removed {total_before - len(self.df)} duplicate(s) → {len(self.df)} rows remain")

        st.divider()

    # ─────────────────────────────────────────────
    # STEP 7 – Final CTE: Full Pipeline (Final Query)
    # ─────────────────────────────────────────────
    def step_7_final_cte(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1976d2;margin:0.3rem 0;'>🔗 Step 7 – Final CTE: Full Cleaning Pipeline</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "Combine all steps into a single readable CTE chain — the production-ready query")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- PostgreSQL: full cleaning pipeline as CTEs
WITH cleaned_data AS (
    SELECT
        order_id,
        -- Name: INITCAP + NULL guard
        CASE
            WHEN UPPER(TRIM(customer_name)) = 'NULL' THEN NULL
            ELSE INITCAP(TRIM(customer_name))
        END AS customer_name,
        LOWER(TRIM(email)) AS email,

        -- order_status: LIKE-based standardisation
        CASE
            WHEN LOWER(order_status) LIKE '%deliver%' THEN 'Delivered'
            WHEN LOWER(order_status) LIKE '%return%'  THEN 'Returned'
            WHEN LOWER(order_status) LIKE '%refund%'  THEN 'Refunded'
            WHEN LOWER(order_status) LIKE '%pend%'    THEN 'Pending'
            WHEN LOWER(order_status) LIKE '%ship%'    THEN 'Shipped'
            ELSE 'Other'
        END AS order_status,

        -- product_name: canonical brand names
        CASE
            WHEN LOWER(product_name) LIKE '%apple watch%'        THEN 'Apple Watch'
            WHEN LOWER(product_name) LIKE '%samsung galaxy s22%' THEN 'Samsung Galaxy S22'
            WHEN LOWER(product_name) LIKE '%google pixel%'       THEN 'Google Pixel'
            WHEN LOWER(product_name) LIKE '%macbook pro%'        THEN 'MacBook Pro'
            WHEN LOWER(product_name) LIKE '%iphone 14%'          THEN 'iPhone 14'
            ELSE NULL
        END AS product_name,

        -- quantity: text-to-integer conversion
        CASE
            WHEN LOWER(quantity::TEXT) = 'one'   THEN 1
            WHEN LOWER(quantity::TEXT) = 'two'   THEN 2
            WHEN LOWER(quantity::TEXT) = 'three' THEN 3
            ELSE quantity::INTEGER
        END AS quantity,

        -- price: strip $ and cast
        NULLIF(
            REGEXP_REPLACE(price::TEXT, '[^0-9.]', '', 'g'),
            ''
        )::NUMERIC(10,2) AS price,

        -- order_date: parse multiple formats → DATE
        COALESCE(
            TO_DATE(order_date::TEXT, 'YYYY-MM-DD'),
            TO_DATE(order_date::TEXT, 'MM/DD/YYYY'),
            TO_DATE(order_date::TEXT, 'YYYY/MM/DD')
        ) AS order_date,

        INITCAP(TRIM(country)) AS country,
        COALESCE(NULLIF(TRIM(notes), '-'), NULL) AS notes

    FROM customer_orders
    WHERE customer_name IS NOT NULL
      AND UPPER(TRIM(customer_name)) != 'NULL'
),

deduplicated_data AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY LOWER(email), LOWER(product_name)
            ORDER BY order_id
        ) AS rn
    FROM cleaned_data
)

SELECT
    order_id,
    customer_name,
    email,
    order_date,
    product_name,
    quantity,
    price,
    quantity * price AS total_amount,
    country,
    order_status,
    notes
FROM deduplicated_data
WHERE rn = 1
  AND product_name IS NOT NULL
  AND price IS NOT NULL
  AND price > 0
ORDER BY order_id;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 BigQuery → PostgreSQL fixes applied:</strong><br>
                    • <code>SAFE.PARSE_DATE()</code> → <code>TO_DATE()</code> wrapped in <code>COALESCE</code><br>
                    • <code>CAST(x AS INT64)</code> → <code>x::INTEGER</code><br>
                    • Double-quote strings → single-quote strings<br>
                    • <code>SELECT * EXCEPT(rn)</code> → explicit column list<br>
                    • <code>ROW NUMBER()</code> (with space) → <code>ROW_NUMBER()</code>
                </div>""", unsafe_allow_html=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ CTE Pipeline Best Practices:</strong><br>
                    • One CTE per concern (clean → dedup → filter)<br>
                    • Filter NULLs in the final SELECT, not early CTEs<br>
                    • Compute derived columns (total_amount) at the end<br>
                    • Add ORDER BY only in the final output
                </div>""", unsafe_allow_html=True)

            with col_result:
                st.markdown("**Final Clean Dataset**")

                # simulate full pipeline on fresh copy
                raw = pd.DataFrame([
                    [1001, "John Smith", "john.smith@gmail.com", "2023-11-02",
                        "Apple Watch", 1, 399.99, "usa", "Delivered", "-"],
                    [1002, "john smith", "john.smith@gmail.com", "11/02/2023",
                        "apple watch", 1, 399.99, "USA", "delivered", "Duplicate name?"],
                    [1003, "SARAH THOMPSON", "sarah.t@gmail.com", "2023/10/30", "Samsung Galaxy S22",
                        "two", 799.0, "United States", "shipped", "customer requested refund"],
                    [1004, "Tom O'Brien", None, "2023-11-05",
                        "Google Pixel", 1, 599.0, "UK", "Delivered", "NULL"],
                    [1005, "Mary Johnson", "mary.j@gmail.com", "2023-11-06", "Samsung Galaxy S22",
                        2, 800.0, "United Kingdom", "returned", "Return due to defect"],
                    [1006, "Ankit Patel", "ankit@@patel.com", "2023-11-07",
                        "NULL", 1, 0.0, "india", "pending", "no stock"],
                    [1007, "John Smith", "john.smith@gmail.com", "2023-11-02",
                        "Apple Watch", 1, 399.99, "usa", "delivered", "Duplicate?"],
                    [1008, "Carlos Hernández", "carlos@hernandez.com", "2023-11-08",
                        "Iphone 14", 1, 1099.0, "spain", "DELIVERED", "-"],
                    [1009, "NULL", "jessica@abc.com", "2023-11-09", "Macbook Pro",
                        1, 1299.99, "canada", "returned", "Missing name"],
                    [1010, "Aisha Khan", "aisha.khan@outlook", "2023-11-10", "MacBook Pro",
                        1, 1299.99, "CANADA", "Returned", "check eligibility"],
                    [1011, "Sarah Thompson", "sarah.t@gmail.com", "2023-10-30",
                        "Samsung Galaxy S22", 2, 799.0, "US", "refunded", "updated payment method"],
                    [1012, "tom o'brien", "tom.obrien@gmail.com", "2023-11-05",
                        "Google pixel", 1, 599.0, "uk", "Delivered", "no comment"],
                    [1013, "Mary Johnson", "mary.j@gmail.com", "2023-11-06",
                        "SAMSUNG GALAXY S22", 2, 800.0, "UK", "Returned", None],
                    [1014, "Ankit Patel", "ankit@patel.com", "2023-11-07",
                        "Samsung Galaxy S22", 1, None, "India", "Pending", "missing price"],
                    [1015, "Carlos Hernández", "carlos@hernandez.com", "2023-11-08",
                        "iPhone 14", 1, 1099.0, "Spain", "delivered", "duplicate product format"],
                ], columns=["order_id", "customer_name", "email", "order_date", "product_name", "quantity", "price", "country", "order_status", "notes"])

                def full_pipeline(df):
                    d = df.copy()
                    # null guard
                    d["customer_name"] = d["customer_name"].apply(
                        lambda x: None if pd.isna(x) or str(x).upper().strip() == "NULL" else x.strip().title())
                    d["product_name"] = d["product_name"].apply(
                        lambda x: None if pd.isna(x) or str(x).upper().strip() == "NULL" else x)
                    d = d[d["customer_name"].notna()]

                    def cs(s):
                        s = str(s).lower()
                        if "deliver" in s:
                            return "Delivered"
                        if "return" in s:
                            return "Returned"
                        if "refund" in s:
                            return "Refunded"
                        if "pend" in s:
                            return "Pending"
                        if "ship" in s:
                            return "Shipped"
                        return "Other"
                    d["order_status"] = d["order_status"].apply(cs)

                    def cp(p):
                        if pd.isna(p):
                            return None
                        pl = str(p).lower()
                        if "apple watch" in pl:
                            return "Apple Watch"
                        if "samsung galaxy s22" in pl:
                            return "Samsung Galaxy S22"
                        if "google pixel" in pl:
                            return "Google Pixel"
                        if "macbook pro" in pl:
                            return "MacBook Pro"
                        if "iphone 14" in pl:
                            return "iPhone 14"
                        return None
                    d["product_name"] = d["product_name"].apply(cp)

                    tm = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
                    d["quantity"] = d["quantity"].apply(lambda x: tm.get(
                        str(x).lower().strip(), x) if pd.notna(x) else x)
                    d["quantity"] = pd.to_numeric(
                        d["quantity"], errors="coerce").astype("Int64")

                    d["price"] = pd.to_numeric(d["price"], errors="coerce")
                    d["email"] = d["email"].fillna("").str.lower().str.strip()

                    def pd_date(v):
                        for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d"):
                            try:
                                return pd.to_datetime(str(v).strip(), format=fmt)
                            except:
                                pass
                        return pd.NaT
                    d["order_date"] = d["order_date"].apply(pd_date)

                    d["country"] = d["country"].apply(
                        lambda x: x.strip().title() if pd.notna(x) else x)
                    d["notes"] = d["notes"].apply(lambda x: None if pd.isna(
                        x) or str(x).strip() in ["-", "NULL", ""] else x)

                    # dedup
                    d["_ek"] = d["email"].str.lower()
                    d["_pk"] = d["product_name"].str.lower().fillna("")
                    d["rn"] = d.groupby(["_ek", "_pk"])["order_id"].rank(
                        method="first").astype(int)
                    d = d[d["rn"] == 1].drop(columns=["_ek", "_pk", "rn"])

                    # filter
                    d = d[d["product_name"].notna() & d["price"].notna()
                          & (d["price"] > 0)]
                    d["total_amount"] = (d["quantity"] * d["price"]).round(2)
                    return d.sort_values("order_id").reset_index(drop=True)

                final = full_pipeline(raw)

                st.dataframe(
                    final[["order_id", "customer_name", "email", "order_date", "product_name",
                           "quantity", "price", "total_amount", "country", "order_status", "notes"]],
                    width='stretch'
                )

                c1, c2 = st.columns(2)
                c1.metric("Final Rows",      len(final))
                c2.metric("Unique Customers", final["customer_name"].nunique())
                total_rev = final["total_amount"].sum()
                avg_order = final["total_amount"].mean()
                c1.metric("Total Revenue",   f"${total_rev:,.2f}")
                c2.metric("Avg Order Value", f"${avg_order:,.2f}")
                c1.metric("Products",        final["product_name"].nunique())
                c2.metric("Countries",       final["country"].nunique())

                csv_buf = io.StringIO()
                final.to_csv(csv_buf, index=False)
                st.download_button(
                    label="📥 Download Final Clean Orders CSV",
                    data=csv_buf.getvalue(),
                    file_name="customer_orders_clean.csv",
                    mime="text/csv",
                    width='stretch'
                )
                st.success(
                    "✅ Full CTE pipeline complete — data ready for production!")

        st.divider()

    def output(self):
        self.step_1_inspect_data()
        self.step_2_order_status()
        self.step_3_product_name()
        self.step_4_quantity()
        self.step_5_customer_name()
        self.step_6_duplicates()
        self.step_7_final_cte()

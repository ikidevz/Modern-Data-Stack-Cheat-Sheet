import streamlit as st
import pandas as pd
import io
import re


class DataCleaningSQL:
    def __init__(self):
        self.data = [
            ["SHP-1001", "Warehouse A",    "Dallas",          "TX", "FastFreight",
                "2024-01-10",  "2024-01-14",  120.5,  450.00, "Delivered",  48,   "No"],
            ["SHP-1002", "warehouse b",    "  Los Angeles  ", "CA", "SPEEDYHAUL",
                "2024-01-12",  "2024-01-11",  85.3,   320.00, "delivered",  30,   "no"],
            ["SHP-1003", "Warehouse A",    "Dallas",          "TX", "FastFreight",
                "2024-01-10",  "2024-01-14",  120.5,  450.00, "Delivered",  48,   "No"],
            ["SHP-1004", "Warehouse C",    "Chicago",         "il", "FastFreight",
                "01/15/2024",  "01/19/2024",  200.0,  610.00, "In Transit", 75,   None],
            ["SHP-1005", "warehouse a",    "Houston",         "TX", "QuickShip",
                None,          "2024-01-20",  -45.2,  280.00, "Delivered",  20,   "Yes"],
            ["SHP-1006", "Warehouse B",    "Phoenix",         "AZ", "SpeedyHaul",
                "2024-01-18",  "2024-01-23",  95.0,   None,   "Delivered",  0,    "No"],
            ["SHP-1007", "  Warehouse D  ", "Seattle",         "WA", "quickship",
                "2024-01-20",  "2024-01-25",  310.8,  980.00, "delivered",  110,  "yes"],
            ["SHP-1008", "Warehouse C",    "Denver",          "CO", "FastFreight",
                "2024/01/22",  "2024/01/27",  150.0,  520.00, "Pending",    55,   "No"],
            ["SHP-1009", "Warehouse B",    "Miami",           "FL", "SpeedyHaul",
                "2024-01-25",  "2024-02-01",  88.7,   345.00, "Delivered",  33,   None],
            ["SHP-1010", "WAREHOUSE A",    "  dallas  ",      "tx", "FASTFREIGHT",
                "2024-02-01",  "2024-02-05",  175.3,  590.00, "DELIVERED",  65,   "NO"],
            ["SHP-1011", "Warehouse D",    "Portland",        "OR", "QuickShip",
                "2024-02-03",  "2024-02-08",  60.0,   210.00, "Cancelled",  -15,  "No"],
            ["SHP-1012", "Warehouse B",    "Los Angeles",     "CA", "SpeedyHaul",
                "2024-02-05",  "2024-02-10",  85.3,   320.00, "Delivered",  30,   "No"],
            ["SHP-1013", "Warehouse C",    None,              "IL", "FastFreight",
                "2024-02-08",  "2024-02-12",  225.0,  670.00, "Delivered",  80,   "Yes"],
            ["SHP-1014", "warehouse d",    "San Francisco",   "CA", "QuickShip",
                "Feb 10 2024", "Feb 15 2024", 140.6,  485.00, "In transit", 52,   "No"],
            ["SHP-1015", "Warehouse A",    "Houston",         "TX", "FastFreight",
                "2024-02-12",  "2024-02-16",  98.4,   370.00, "Delivered",  40,   "No"],
            ["SHP-1016", "Warehouse B",    "Phoenix",         "AZ", "SpeedyHaul",
                "2024-02-14",  "2024-02-19",  95.0,   15000.0, "Delivered",  35,   "Yes"],
            ["SHP-1017", "  warehouse c  ", "Denver",          "CO", "QUICKSHIP",
                "2024-02-18",  "2024-02-23",  0.0,    0.00,   "Pending",    0,    None],
            ["SHP-1018", "Warehouse D",    "Seattle",         "WA", "QuickShip",
                "2024-02-20",  "2024-02-25",  310.8,  980.00, "Delivered",  110,  "No"],
            ["SHP-1019", "Warehouse A",    "Atlanta",         "GA", "FastFreight",
                "2024-02-22",  None,          165.0,  540.00, "In Transit", 60,   "No"],
            ["SHP-1020", "Warehouse B",    "Miami",           "FL", "speedyhaul",
                "2024-02-25",  "2024-03-02",  72.1,   265.00, "Delivered",  28,   "no"],
            ["SHP-1021", "Warehouse C",    "Chicago",         "IL", "FastFreight",
                "2024-03-01",  "2024-03-05",  190.0,  600.00, "Delivered",  70,   "No"],
            ["SHP-1022", "WAREHOUSE D",    "  Portland  ",    "or", "QUICKSHIP",
                "2024-03-03",  "2024-03-08",  55.4,   195.00, "CANCELLED",  22,   "NO"],
            ["SHP-1023", "Warehouse A",    "Dallas",          "TX", "FastFreight",
                "2024-03-05",  "2024-03-09",  120.5,  450.00, "Delivered",  48,   "Yes"],
            ["SHP-1024", "Warehouse B",    "Los Angeles",     "CA", "SpeedyHaul",
                "March 7 2024", "March 12 2024", 130.2, 460.00, "Delivered",  50,   "No"],
            ["SHP-1025", "Warehouse C",    "San Francisco",   "CA", "QuickShip",
                "2024-03-10",  "2024-03-15",  145.9,  500.00, "Delivered",  54,   "No"],
        ]
        self.columns = [
            "shipment_id", "origin_warehouse", "destination_city",
            "destination_state", "carrier", "ship_date", "delivery_date",
            "weight_kg", "freight_cost", "shipment_status", "items_count",
            "damage_reported"
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
                "Examine the structure, quality, and basic statistics of your dataset")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- View table structure (PostgreSQL)
SELECT
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'shipments'
ORDER BY ordinal_position;
 
-- Preview data
SELECT * FROM shipments
LIMIT 10;
 
-- Row count & duplicate check
SELECT
    COUNT(*)                        AS total_rows,
    COUNT(DISTINCT shipment_id)     AS unique_shipments,
    COUNT(*) - COUNT(DISTINCT shipment_id) AS duplicates
FROM shipments;
 
-- Basic statistics
SELECT
    COUNT(*)                         AS total_records,
    COUNT(DISTINCT shipment_id)      AS unique_shipments,
    COUNT(DISTINCT origin_warehouse) AS unique_warehouses,
    COUNT(DISTINCT carrier)          AS unique_carriers,
    MIN(ship_date)                   AS earliest_ship,
    MAX(ship_date)                   AS latest_ship,
    ROUND(AVG(weight_kg)::NUMERIC, 2) AS avg_weight_kg,
    MIN(freight_cost)                AS min_cost,
    MAX(freight_cost)                AS max_cost,
    COUNT(DISTINCT destination_state) AS states_served
FROM shipments;
 
-- Data quality issues
SELECT 'Missing destination_city'  AS issue, COUNT(*) AS count
FROM shipments WHERE destination_city IS NULL OR destination_city = ''
UNION ALL
SELECT 'Missing ship_date',        COUNT(*)
FROM shipments WHERE ship_date IS NULL
UNION ALL
SELECT 'Missing freight_cost',     COUNT(*)
FROM shipments WHERE freight_cost IS NULL
UNION ALL
SELECT 'Negative weight_kg',       COUNT(*)
FROM shipments WHERE weight_kg < 0
UNION ALL
SELECT 'Negative items_count',     COUNT(*)
FROM shipments WHERE items_count < 0;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 SQL Tip:</strong><br>
                    Always inspect raw data first. Look for type mismatches,
                    inconsistent casing, NULLs, and obvious outliers before
                    writing any cleaning logic.
                </div>""", unsafe_allow_html=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ Best Practice:</strong><br>
                    • Document original schema before changes<br>
                    • Identify primary keys and NOT NULL expectations<br>
                    • Note mixed date formats early<br>
                    • Flag columns with suspicious ranges
                </div>""", unsafe_allow_html=True)

            with col_result:
                st.markdown("**Table Structure**")
                structure_data = {
                    "Column": self.df.columns.tolist(),
                    "Type": [str(d) for d in self.df.dtypes],
                    "Nullable": ["YES" if self.df[c].isnull().any() else "NO" for c in self.df.columns],
                }
                st.dataframe(pd.DataFrame(structure_data),
                             hide_index=True, width='stretch')

                st.markdown("**Data Preview (LIMIT 5)**")
                st.dataframe(self.df.head(5), width='stretch')

                st.markdown("**Basic Statistics**")
                c1, c2 = st.columns(2)
                c1.metric("Total Records",     len(self.df))
                c2.metric("Unique Shipments",
                          self.df["shipment_id"].nunique())
                c1.metric("Unique Warehouses", self.df["origin_warehouse"].str.strip(
                ).str.upper().nunique())
                c2.metric("Unique Carriers",
                          self.df["carrier"].str.strip().str.upper().nunique())
                c1.metric("Missing Cols",      int(
                    self.df.isnull().any(axis=1).sum()))
                c2.metric("States Served",     self.df["destination_state"].str.strip(
                ).str.upper().nunique())

        st.divider()

    # ─────────────────────────────────────────────
    # STEP 2 – Trim Whitespace (Query 1)
    # ─────────────────────────────────────────────
    def step_2_trim_whitespace(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1976d2;margin:0.3rem 0;'>✂️ Step 2 – Remove Leading / Trailing Whitespace</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "TRIM() removes invisible spaces that break GROUP BY, JOINs, and comparisons")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- PostgreSQL: TRIM all key text columns
SELECT
    shipment_id,
    TRIM(origin_warehouse)   AS origin_warehouse,
    TRIM(destination_city)   AS destination_city,
    TRIM(destination_state)  AS destination_state,
    TRIM(carrier)            AS carrier
FROM shipments;
 
-- Update in place
UPDATE shipments
SET
    origin_warehouse  = TRIM(origin_warehouse),
    destination_city  = TRIM(destination_city),
    destination_state = TRIM(destination_state),
    carrier           = TRIM(carrier),
    shipment_status   = TRIM(shipment_status),
    damage_reported   = TRIM(damage_reported);
 
-- Verify no more leading/trailing spaces remain
SELECT shipment_id, origin_warehouse
FROM shipments
WHERE origin_warehouse <> TRIM(origin_warehouse);""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 SQL Tip:</strong><br>
                    In PostgreSQL, <code>TRIM(col)</code> removes spaces from
                    both ends. Use <code>LTRIM</code> / <code>RTRIM</code> for
                    one side only. Always TRIM before any case-standardisation.
                </div>""", unsafe_allow_html=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ Best Practice:</strong><br>
                    • TRIM every free-text column on ingest<br>
                    • Run TRIM before INITCAP / LOWER / UPPER<br>
                    • Verify with a WHERE col &lt;&gt; TRIM(col) check
                </div>""", unsafe_allow_html=True)

            with col_result:
                st.markdown("**Before (raw values with spaces)**")
                before = self.df[["shipment_id", "origin_warehouse",
                                  "destination_city", "carrier"]].head(8).copy()
                st.dataframe(before, width='stretch')

                # apply
                for col in ["origin_warehouse", "destination_city", "destination_state", "carrier", "shipment_status", "damage_reported"]:
                    self.df[col] = self.df[col].astype(
                        str).str.strip().replace("None", "")
                    self.df[col] = self.df[col].where(
                        self.df[col] != "", other=None)

                st.markdown("**After TRIM()**")
                after = self.df[["shipment_id", "origin_warehouse",
                                 "destination_city", "carrier"]].head(8)
                st.dataframe(after, width='stretch')

                had_spaces = before["origin_warehouse"].apply(
                    lambda x: x != x.strip()).sum()
                st.success(
                    f"✅ Fixed {had_spaces} cells with leading/trailing spaces")

        st.divider()

    # ─────────────────────────────────────────────
    # STEP 3 – Standardize Casing (Query 2)
    # ─────────────────────────────────────────────
    def step_3_standardize_casing(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1976d2;margin:0.3rem 0;'>🔡 Step 3 – Standardize Text Casing</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "Uniform casing prevents duplicate groups and broken joins")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- PostgreSQL: INITCAP for names, UPPER for codes
SELECT
    shipment_id,
    INITCAP(TRIM(origin_warehouse))   AS origin_warehouse,
    INITCAP(TRIM(destination_city))   AS destination_city,
    UPPER(TRIM(destination_state))    AS destination_state,
    INITCAP(TRIM(carrier))            AS carrier,
    INITCAP(TRIM(shipment_status))    AS shipment_status
FROM shipments;
 
-- Update in place
UPDATE shipments
SET
    origin_warehouse  = INITCAP(TRIM(origin_warehouse)),
    destination_city  = INITCAP(TRIM(destination_city)),
    destination_state = UPPER(TRIM(destination_state)),
    carrier           = INITCAP(TRIM(carrier)),
    shipment_status   = INITCAP(TRIM(shipment_status));
 
-- Verify distinct values after standardisation
SELECT DISTINCT carrier FROM shipments ORDER BY 1;
SELECT DISTINCT shipment_status FROM shipments ORDER BY 1;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 SQL Tip:</strong><br>
                    • <code>INITCAP()</code> – Title Case (names, cities)<br>
                    • <code>UPPER()</code> – ALL CAPS (state codes, IDs)<br>
                    • <code>LOWER()</code> – lowercase (emails, slugs)
                </div>""", unsafe_allow_html=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ Best Practice:</strong><br>
                    • Choose one canonical form per column<br>
                    • State codes → UPPER (TX, CA, IL)<br>
                    • Carrier/warehouse names → INITCAP<br>
                    • Status fields → INITCAP for display
                </div>""", unsafe_allow_html=True)

            with col_result:
                st.markdown("**Before (mixed case)**")
                cols = ["shipment_id", "origin_warehouse", "destination_city",
                        "destination_state", "carrier", "shipment_status"]
                before = self.df[cols].head(8).copy()
                st.dataframe(before, width='stretch')

                # apply
                self.df["origin_warehouse"] = self.df["origin_warehouse"].apply(
                    lambda x: x.strip().title() if pd.notna(x) else x)
                self.df["destination_city"] = self.df["destination_city"].apply(
                    lambda x: x.strip().title() if pd.notna(x) else x)
                self.df["destination_state"] = self.df["destination_state"].apply(
                    lambda x: x.strip().upper() if pd.notna(x) else x)
                self.df["carrier"] = self.df["carrier"].apply(
                    lambda x: x.strip().title() if pd.notna(x) else x)
                self.df["shipment_status"] = self.df["shipment_status"].apply(
                    lambda x: x.strip().title() if pd.notna(x) else x)

                st.markdown("**After Casing**")
                st.dataframe(self.df[cols].head(8), width='stretch')

                st.markdown("**Distinct carriers after fix:**")
                st.write(sorted(self.df["carrier"].dropna().unique().tolist()))
                st.success("✅ Casing standardised")

        st.divider()

    # ─────────────────────────────────────────────
    # STEP 4 – Replace String "NULL" & Handle True NULLs (Query 3)
    # ─────────────────────────────────────────────
    def step_4_nulls(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1976d2;margin:0.3rem 0;'>❓ Step 4 – Replace String \"NULL\" & Handle True NULLs</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "String 'NULL' is not a real NULL — it must be handled separately")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- Replace literal 'NULL' string with proper NULL
UPDATE shipments
SET damage_reported = NULL
WHERE UPPER(TRIM(damage_reported)) = 'NULL';
 
-- Use COALESCE to fill true NULLs with defaults
SELECT
    shipment_id,
    CASE
        WHEN UPPER(TRIM(damage_reported)) = 'NULL' THEN NULL
        ELSE INITCAP(TRIM(damage_reported))
    END                                               AS damage_reported,
    COALESCE(destination_city, 'Unknown')             AS destination_city,
    COALESCE(delivery_date::TEXT, 'Not Yet Delivered') AS delivery_date
FROM shipments;
 
-- Count NULLs per critical column
SELECT
    COUNT(*) - COUNT(ship_date)       AS missing_ship_date,
    COUNT(*) - COUNT(delivery_date)   AS missing_delivery_date,
    COUNT(*) - COUNT(freight_cost)    AS missing_freight_cost,
    COUNT(*) - COUNT(destination_city) AS missing_dest_city,
    COUNT(*) - COUNT(damage_reported) AS missing_damage_info
FROM shipments;
 
-- Strategy: fill missing freight_cost with average per carrier
UPDATE shipments s
SET freight_cost = (
    SELECT ROUND(AVG(freight_cost)::NUMERIC, 2)
    FROM shipments s2
    WHERE s2.carrier = s.carrier
      AND s2.freight_cost IS NOT NULL
)
WHERE s.freight_cost IS NULL;
 
-- Mark records with any critical NULL
ALTER TABLE shipments ADD COLUMN data_quality VARCHAR(20);
UPDATE shipments
SET data_quality = CASE
    WHEN destination_city IS NULL OR freight_cost IS NULL THEN 'Incomplete'
    WHEN ship_date IS NULL                                THEN 'Missing Date'
    ELSE 'Complete'
END;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 SQL Tip:</strong><br>
                    Databases store the text <em>"NULL"</em> as a six-character
                    string. Always check for both <code>IS NULL</code> and
                    <code>UPPER(col) = 'NULL'</code> when cleaning source data.
                </div>""", unsafe_allow_html=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ NULL Handling Strategies:</strong><br>
                    • Delete rows with NULLs in primary key fields<br>
                    • Default text for optional columns (e.g. 'Unknown')<br>
                    • Infer numeric NULLs from peer rows (avg per carrier)<br>
                    • Flag incomplete rows with a data_quality column
                </div>""", unsafe_allow_html=True)

            with col_result:
                st.markdown("**Missing Values Before**")
                # show raw missing counts
                raw_null = self.df.isnull().sum()
                # also count string "NULL"
                string_null = self.df.apply(lambda col: col.astype(
                    str).str.upper().str.strip().eq("NULL").sum())
                missing_df = pd.DataFrame({
                    "Column": raw_null.index,
                    "True NULLs": raw_null.values,
                    "String 'NULL'": string_null.values
                })
                missing_df = missing_df[(missing_df["True NULLs"] > 0) | (
                    missing_df["String 'NULL'"] > 0)]
                st.dataframe(missing_df, hide_index=True,
                             width='stretch')

                # apply cleaning
                for col in self.df.columns:
                    mask = self.df[col].astype(
                        str).str.upper().str.strip() == "NULL"
                    self.df.loc[mask, col] = None

                # fill destination_city
                self.df["destination_city"] = self.df["destination_city"].fillna(
                    "Unknown")

                # fill freight_cost with carrier avg
                self.df["freight_cost"] = pd.to_numeric(
                    self.df["freight_cost"], errors="coerce")
                for carrier in self.df["carrier"].unique():
                    mask = (self.df["carrier"] ==
                            carrier) & self.df["freight_cost"].isnull()
                    avg = self.df[self.df["carrier"] ==
                                  carrier]["freight_cost"].mean()
                    self.df.loc[mask, "freight_cost"] = round(
                        avg, 2) if pd.notna(avg) else 0

                st.markdown("**After NULL Handling**")
                st.metric("Remaining True NULLs (freight_cost)",
                          int(self.df["freight_cost"].isnull().sum()))
                st.dataframe(
                    self.df[["shipment_id", "destination_city",
                             "freight_cost", "damage_reported"]].head(10),
                    width='stretch'
                )
                st.success(
                    "✅ String NULLs replaced; missing costs filled by carrier average")

        st.divider()

    # ─────────────────────────────────────────────
    # STEP 5 – Remove Exact Duplicates (Query 4)
    # ─────────────────────────────────────────────
    def step_5_duplicates(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1976d2;margin:0.3rem 0;'>🔁 Step 5 – Remove Exact Duplicate Rows</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "Use ROW_NUMBER() to rank duplicates and keep only the first occurrence")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- Detect exact duplicates using ROW_NUMBER()
WITH ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY
                origin_warehouse,
                destination_city,
                carrier,
                ship_date,
                CAST(weight_kg    AS TEXT),
                CAST(freight_cost AS TEXT)
            ORDER BY shipment_id
        ) AS row_num
    FROM shipments
)
SELECT * EXCEPT (row_num)          -- BigQuery syntax
FROM ranked
WHERE row_num = 1;
 
-- PostgreSQL equivalent (no EXCEPT, use subquery)
DELETE FROM shipments
WHERE shipment_id NOT IN (
    SELECT MIN(shipment_id)
    FROM shipments
    GROUP BY
        origin_warehouse,
        destination_city,
        carrier,
        ship_date,
        weight_kg,
        freight_cost
);
 
-- How many exact duplicates exist?
SELECT
    origin_warehouse, destination_city, carrier,
    ship_date, weight_kg, freight_cost,
    COUNT(*) AS occurrence_count
FROM shipments
GROUP BY
    origin_warehouse, destination_city, carrier,
    ship_date, weight_kg, freight_cost
HAVING COUNT(*) > 1;
 
-- Create clean table keeping one per group
CREATE TABLE shipments_clean AS
WITH ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY origin_warehouse, destination_city,
                         carrier, ship_date, weight_kg, freight_cost
            ORDER BY shipment_id
        ) AS rn
    FROM shipments
)
SELECT shipment_id, origin_warehouse, destination_city,
       destination_state, carrier, ship_date, delivery_date,
       weight_kg, freight_cost, shipment_status,
       items_count, damage_reported
FROM ranked WHERE rn = 1;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ Deduplication Strategy:</strong><br>
                    • <b>Exact dups:</b> identical in ALL columns<br>
                    • <b>Semantic dups:</b> same route + date + carrier<br>
                    • Keep lowest shipment_id as canonical row<br>
                    • Always back up before deleting
                </div>""", unsafe_allow_html=True)

            with col_result:
                st.markdown("**Duplicate Analysis**")
                total = len(self.df)
                key_cols = ["origin_warehouse", "destination_city",
                            "carrier", "ship_date", "weight_kg", "freight_cost"]
                dup_groups = self.df.groupby(key_cols).size()
                semantic_dups = int((dup_groups > 1).sum())

                c1, c2 = st.columns(2)
                c1.metric("Total Rows", total)
                c2.metric("Duplicate Groups", semantic_dups)

                if semantic_dups:
                    dup_rows = self.df[self.df.duplicated(
                        subset=key_cols, keep=False)]
                    st.warning(
                        f"⚠️ Found {len(dup_rows)} rows forming {semantic_dups} duplicate group(s)")
                    st.dataframe(
                        dup_rows[["shipment_id", "origin_warehouse", "destination_city",
                                  "carrier", "ship_date"]].sort_values("shipment_id"),
                        width='stretch'
                    )
                    self.df = self.df.drop_duplicates(
                        subset=key_cols, keep="first")
                    st.success(
                        f"✅ Removed duplicates → {len(self.df)} rows remaining")
                else:
                    st.success("✅ No exact duplicates found")

                c1.metric("After Dedup", len(self.df))

        st.divider()

    # ─────────────────────────────────────────────
    # STEP 6 – Fix Negative & Suspicious Numeric Values (Query 5)
    # ─────────────────────────────────────────────
    def step_6_numeric_fix(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1976d2;margin:0.3rem 0;'>🔢 Step 6 – Fix Negative & Suspicious Numeric Values</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "Negative weight or item counts are data-entry errors — fix with ABS() or NULL them out")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- Inspect suspicious numeric values
SELECT
    shipment_id,
    weight_kg,
    items_count,
    freight_cost
FROM shipments
WHERE weight_kg   < 0
   OR weight_kg   = 0
   OR items_count < 0
   OR freight_cost < 0;
 
-- Fix weight_kg
SELECT
    shipment_id,
    CASE
        WHEN weight_kg < 0 THEN ABS(weight_kg)  -- flip sign
        WHEN weight_kg = 0 THEN NULL             -- zero = unknown
        ELSE weight_kg
    END AS weight_kg_cleaned
FROM shipments;
 
-- Fix items_count
SELECT
    shipment_id,
    CASE
        WHEN items_count < 0 THEN ABS(items_count)
        WHEN items_count = 0 THEN NULL
        ELSE items_count
    END AS items_count_cleaned
FROM shipments;
 
-- Apply updates
UPDATE shipments
SET weight_kg = CASE
    WHEN weight_kg < 0 THEN ABS(weight_kg)
    WHEN weight_kg = 0 THEN NULL
    ELSE weight_kg
END;
 
UPDATE shipments
SET items_count = CASE
    WHEN items_count < 0 THEN ABS(items_count)
    WHEN items_count = 0 THEN NULL
    ELSE items_count
END;
 
-- Also NULL out zero freight_cost (likely missing)
UPDATE shipments
SET freight_cost = NULL
WHERE freight_cost = 0;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='warning-box'>
                    <strong>⚠️ Decision point:</strong><br>
                    • Negative weight → probably a sign flip → use ABS()<br>
                    • Zero weight → truly unknown → NULL<br>
                    • Zero items → entry error → NULL<br>
                    • Zero freight cost → missing data → NULL or avg-fill
                </div>""", unsafe_allow_html=True)

            with col_result:
                st.markdown("**Suspicious Values Found**")
                self.df["weight_kg"] = pd.to_numeric(
                    self.df["weight_kg"],    errors="coerce")
                self.df["items_count"] = pd.to_numeric(
                    self.df["items_count"],  errors="coerce")
                self.df["freight_cost"] = pd.to_numeric(
                    self.df["freight_cost"], errors="coerce")

                neg_weight = int((self.df["weight_kg"] < 0).sum())
                zero_weight = int((self.df["weight_kg"] == 0).sum())
                neg_items = int((self.df["items_count"] < 0).sum())
                zero_items = int((self.df["items_count"] == 0).sum())

                issue_df = pd.DataFrame({
                    "Issue":  ["Negative weight_kg", "Zero weight_kg", "Negative items_count", "Zero items_count"],
                    "Count":  [neg_weight, zero_weight, neg_items, zero_items]
                })
                st.dataframe(issue_df, hide_index=True,
                             width='stretch')

                bad = self.df[(self.df["weight_kg"] < 0) | (self.df["weight_kg"] == 0) |
                              (self.df["items_count"] < 0) | (self.df["items_count"] == 0)]
                if not bad.empty:
                    st.markdown("**Records before fix:**")
                    st.dataframe(
                        bad[["shipment_id", "weight_kg", "items_count", "freight_cost"]], width='stretch')

                # apply fix
                self.df["weight_kg"] = self.df["weight_kg"].apply(lambda x: abs(
                    x) if pd.notna(x) and x < 0 else (None if pd.notna(x) and x == 0 else x))
                self.df["items_count"] = self.df["items_count"].apply(lambda x: abs(
                    x) if pd.notna(x) and x < 0 else (None if pd.notna(x) and x == 0 else x))
                self.df["freight_cost"] = self.df["freight_cost"].apply(
                    lambda x: None if pd.notna(x) and x == 0 else x)

                st.markdown("**After fix:**")
                st.dataframe(
                    self.df[["shipment_id", "weight_kg",
                             "items_count", "freight_cost"]].head(10),
                    width='stretch'
                )
                st.success("✅ Negative values corrected; zeros nulled")

        st.divider()

    # ─────────────────────────────────────────────
    # STEP 7 – Validate Date Logic (Query 6)
    # ─────────────────────────────────────────────
    def step_7_date_validation(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1976d2;margin:0.3rem 0;'>📅 Step 7 – Validate Date Logic (Delivery After Ship Date)</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "Parse multiple date formats and flag impossible delivery-before-ship-date records")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- PostgreSQL: parse mixed date formats safely
-- Step 1: normalise text dates to YYYY-MM-DD
UPDATE shipments
SET ship_date = TO_DATE(ship_date, 'MM/DD/YYYY')
WHERE ship_date ~ '^\\d{2}/\\d{2}/\\d{4}$';
 
UPDATE shipments
SET ship_date = TO_DATE(ship_date, 'YYYY/MM/DD')
WHERE ship_date ~ '^\\d{4}/\\d{2}/\\d{2}$';
 
UPDATE shipments
SET ship_date = TO_DATE(ship_date, 'Month DD YYYY')
WHERE ship_date ~ '^[A-Za-z]+ \\d{1,2} \\d{4}$';
 
-- Step 2: cast to DATE
ALTER TABLE shipments
    ALTER COLUMN ship_date    TYPE DATE USING ship_date::DATE,
    ALTER COLUMN delivery_date TYPE DATE USING delivery_date::DATE;
 
-- Step 3: calculate transit days & flag bad dates
SELECT
    shipment_id,
    ship_date,
    delivery_date,
    delivery_date - ship_date                         AS transit_days,
    CASE
        WHEN delivery_date < ship_date THEN 'INVALID'
        WHEN delivery_date = ship_date THEN 'SAME DAY DELIVERY'
        ELSE 'VALID'
    END                                               AS date_quality_flag
FROM shipments;
 
-- Step 4: fix invalid (swap dates)
UPDATE shipments
SET ship_date     = delivery_date,
    delivery_date = ship_date
WHERE delivery_date < ship_date;
 
-- Step 5: remove future ship dates
DELETE FROM shipments
WHERE ship_date > CURRENT_DATE;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 SQL Tip:</strong><br>
                    PostgreSQL's <code>TO_DATE()</code> is strict — the format
                    mask must match exactly. Use regex guards
                    (<code>~</code>) so only matching rows are updated.
                    <code>SAFE.PARSE_DATE</code> is BigQuery-specific.
                </div>""", unsafe_allow_html=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ Date Cleaning Checklist:</strong><br>
                    • Parse all format variants (MM/DD/YYYY, YYYY/MM/DD, Month D YYYY)<br>
                    • Cast to DATE after normalising<br>
                    • Flag delivery_date &lt; ship_date as INVALID<br>
                    • Null out missing delivery_date (shipment in transit)<br>
                    • Compute transit_days for sanity checks
                </div>""", unsafe_allow_html=True)

            with col_result:
                st.markdown("**Date Parsing & Validation**")

                def parse_date(val):
                    if pd.isna(val) or str(val).strip() == "":
                        return pd.NaT
                    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d", "%B %d %Y", "%B %Y"):
                        try:
                            return pd.to_datetime(val.strip(), format=fmt)
                        except Exception:
                            pass
                    try:
                        return pd.to_datetime(val.strip(), infer_datetime_format=True)
                    except Exception:
                        return pd.NaT

                self.df["ship_date"] = self.df["ship_date"].astype(
                    str).apply(parse_date)
                self.df["delivery_date"] = self.df["delivery_date"].astype(
                    str).apply(parse_date)

                self.df["transit_days"] = (
                    self.df["delivery_date"] - self.df["ship_date"]).dt.days

                def date_flag(row):
                    if pd.isna(row["delivery_date"]):
                        return "In Transit"
                    if row["delivery_date"] < row["ship_date"]:
                        return "⛔ INVALID"
                    if row["delivery_date"] == row["ship_date"]:
                        return "⚡ Same Day"
                    return "✅ VALID"

                self.df["date_quality_flag"] = self.df.apply(date_flag, axis=1)

                invalid_dates = (
                    self.df["date_quality_flag"] == "⛔ INVALID").sum()
                in_transit = (self.df["date_quality_flag"]
                              == "In Transit").sum()

                c1, c2 = st.columns(2)
                c1.metric("Invalid Dates",   int(invalid_dates))
                c2.metric("In Transit (no delivery)", int(in_transit))

                st.dataframe(
                    self.df[["shipment_id", "ship_date", "delivery_date",
                             "transit_days", "date_quality_flag"]],
                    width='stretch'
                )

                # fix invalid
                mask = self.df["date_quality_flag"] == "⛔ INVALID"
                self.df.loc[mask, ["ship_date", "delivery_date"]] = \
                    self.df.loc[mask, ["delivery_date", "ship_date"]].values
                self.df["transit_days"] = (
                    self.df["delivery_date"] - self.df["ship_date"]).dt.days

                if invalid_dates:
                    st.success(
                        f"✅ Swapped ship/delivery dates for {invalid_dates} invalid record(s)")

        st.divider()

    # ─────────────────────────────────────────────
    # STEP 8 – Detect & Cap Outliers (Query 7)
    # ─────────────────────────────────────────────
    def step_8_outliers(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1976d2;margin:0.3rem 0;'>📊 Step 8 – Detect & Cap Outliers Using IQR</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "Use the IQR method to flag and cap extreme freight_cost values")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- PostgreSQL: IQR outlier detection on freight_cost
WITH stats AS (
    SELECT
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY freight_cost) AS q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY freight_cost) AS q3
    FROM shipments
    WHERE freight_cost > 0           -- exclude zero/NULL
),
bounds AS (
    SELECT
        q1,
        q3,
        q3 - q1                      AS iqr,
        q1 - 1.5 * (q3 - q1)        AS lower_bound,
        q3 + 1.5 * (q3 - q1)        AS upper_bound
    FROM stats
)
SELECT
    s.shipment_id,
    s.freight_cost                   AS original_cost,
    CASE
        WHEN s.freight_cost > b.upper_bound THEN b.upper_bound
        WHEN s.freight_cost < b.lower_bound THEN b.lower_bound
        ELSE s.freight_cost
    END                              AS cleaned_cost,
    CASE
        WHEN s.freight_cost > b.upper_bound
          OR s.freight_cost < b.lower_bound THEN TRUE
        ELSE FALSE
    END                              AS was_outlier
FROM shipments s
CROSS JOIN bounds b;
 
-- Apply cap update
WITH stats AS (
    SELECT
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY freight_cost) AS q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY freight_cost) AS q3
    FROM shipments WHERE freight_cost > 0
),
bounds AS (
    SELECT q1 - 1.5*(q3-q1) AS lb, q3 + 1.5*(q3-q1) AS ub FROM stats
)
UPDATE shipments
SET freight_cost = CASE
    WHEN freight_cost > (SELECT ub FROM bounds) THEN (SELECT ub FROM bounds)
    WHEN freight_cost < (SELECT lb FROM bounds) THEN (SELECT lb FROM bounds)
    ELSE freight_cost
END;
 
-- Z-score alternative
WITH stats AS (
    SELECT AVG(freight_cost) AS mean, STDDEV(freight_cost) AS std
    FROM shipments WHERE freight_cost > 0
)
SELECT shipment_id, freight_cost,
    (freight_cost - mean) / std AS z_score
FROM shipments, stats
WHERE ABS((freight_cost - mean) / std) > 3;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 PostgreSQL vs BigQuery:</strong><br>
                    BigQuery uses <code>APPROX_QUANTILES(col, 100)[OFFSET(25)]</code>.
                    PostgreSQL uses the exact <code>PERCENTILE_CONT(0.25)
                    WITHIN GROUP (ORDER BY col)</code> — more accurate but
                    slower on very large tables.
                </div>""", unsafe_allow_html=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ Outlier Options:</strong><br>
                    • <b>Cap (Winsorize):</b> replace with boundary value<br>
                    • <b>Remove:</b> delete row if clearly erroneous<br>
                    • <b>Flag:</b> keep but mark <code>was_outlier = TRUE</code><br>
                    • <b>Z-score:</b> flag |z| > 3 as extreme
                </div>""", unsafe_allow_html=True)

            with col_result:
                st.markdown("**Outlier Analysis – freight_cost**")

                clean_fc = self.df["freight_cost"].dropna()
                clean_fc = clean_fc[clean_fc > 0]

                Q1 = clean_fc.quantile(0.25)
                Q3 = clean_fc.quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - 1.5 * IQR
                upper = Q3 + 1.5 * IQR

                c1, c2 = st.columns(2)
                c1.metric("Q1",  f"${Q1:,.2f}")
                c2.metric("Q3",  f"${Q3:,.2f}")
                c1.metric("IQR", f"${IQR:,.2f}")
                c2.metric("Lower Bound", f"${lower:,.2f}")
                c1.metric("Upper Bound", f"${upper:,.2f}")

                outliers = self.df[(self.df["freight_cost"] > upper) | (
                    self.df["freight_cost"] < lower)]
                c2.metric("Outliers Found", len(outliers))

                if not outliers.empty:
                    st.markdown("**Outlier Records:**")
                    st.dataframe(
                        outliers[["shipment_id", "carrier", "freight_cost"]],
                        width='stretch'
                    )

                # cap outliers
                self.df["original_cost"] = self.df["freight_cost"]
                self.df["freight_cost"] = self.df["freight_cost"].clip(
                    lower=lower, upper=upper)
                self.df["was_outlier"] = self.df["original_cost"].apply(
                    lambda x: True if pd.notna(x) and (
                        x > upper or x < lower) else False
                )

                st.markdown(f"**Valid range:** ${lower:,.2f} – ${upper:,.2f}")
                st.dataframe(
                    self.df[["shipment_id", "original_cost",
                             "freight_cost", "was_outlier"]].head(10),
                    width='stretch'
                )
                st.success(
                    f"✅ Capped {len(outliers)} outlier(s) to IQR bounds")

        st.divider()

    # ─────────────────────────────────────────────
    # STEP 9 – Export Clean Table
    # ─────────────────────────────────────────────
    def step_9_export(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1976d2;margin:0.3rem 0;'>💾 Step 9 – Create Clean Table & Export</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "Final production-ready schema with constraints, indexes, and computed columns")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- Create clean production table (PostgreSQL)
CREATE TABLE shipments_clean (
    shipment_id       VARCHAR(20)     PRIMARY KEY,
    origin_warehouse  VARCHAR(100)    NOT NULL,
    destination_city  VARCHAR(100)    NOT NULL DEFAULT 'Unknown',
    destination_state CHAR(2)         NOT NULL,
    carrier           VARCHAR(100)    NOT NULL,
    ship_date         DATE            NOT NULL,
    delivery_date     DATE,
    weight_kg         NUMERIC(8,2)    CHECK (weight_kg > 0),
    freight_cost      NUMERIC(10,2)   CHECK (freight_cost > 0),
    shipment_status   VARCHAR(50),
    items_count       INTEGER         CHECK (items_count > 0),
    damage_reported   VARCHAR(20),
    transit_days      INTEGER
        GENERATED ALWAYS AS (delivery_date - ship_date) STORED,
    is_delivered      BOOLEAN
        GENERATED ALWAYS AS (shipment_status = 'Delivered') STORED,
    was_outlier       BOOLEAN         DEFAULT FALSE,
    created_at        TIMESTAMPTZ     DEFAULT NOW()
);
 
-- Insert from cleaned staging table
INSERT INTO shipments_clean
    (shipment_id, origin_warehouse, destination_city,
     destination_state, carrier, ship_date, delivery_date,
     weight_kg, freight_cost, shipment_status, items_count,
     damage_reported, was_outlier)
SELECT
    shipment_id,
    INITCAP(TRIM(origin_warehouse)),
    COALESCE(INITCAP(TRIM(destination_city)), 'Unknown'),
    UPPER(TRIM(destination_state)),
    INITCAP(TRIM(carrier)),
    ship_date::DATE,
    delivery_date::DATE,
    CASE WHEN weight_kg  <= 0 THEN NULL ELSE ABS(weight_kg)  END,
    CASE WHEN freight_cost <= 0 THEN NULL ELSE freight_cost END,
    INITCAP(TRIM(shipment_status)),
    CASE WHEN items_count  <= 0 THEN NULL ELSE ABS(items_count) END,
    CASE WHEN UPPER(TRIM(damage_reported)) = 'NULL' THEN NULL
         ELSE INITCAP(TRIM(damage_reported)) END,
    was_outlier
FROM shipments_staging
WHERE ship_date IS NOT NULL
  AND delivery_date >= ship_date;
 
-- Indexes for analytics performance
CREATE INDEX idx_carrier       ON shipments_clean(carrier);
CREATE INDEX idx_ship_date     ON shipments_clean(ship_date);
CREATE INDEX idx_dest_state    ON shipments_clean(destination_state);
CREATE INDEX idx_status        ON shipments_clean(shipment_status);
 
-- Analytics views
CREATE VIEW carrier_performance AS
SELECT
    carrier,
    COUNT(*)                           AS total_shipments,
    ROUND(AVG(transit_days), 1)        AS avg_transit_days,
    ROUND(AVG(freight_cost)::NUMERIC, 2) AS avg_freight_cost,
    SUM(CASE WHEN is_delivered THEN 1 ELSE 0 END) AS delivered_count
FROM shipments_clean
GROUP BY carrier;
 
-- Export to CSV (psql)
COPY shipments_clean TO '/tmp/shipments_clean.csv'
WITH (FORMAT CSV, HEADER TRUE);""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 Production Best Practices:</strong><br>
                    • Never overwrite source data — write to a _clean table<br>
                    • Add GENERATED columns for derived metrics<br>
                    • Index columns used in WHERE / JOIN / GROUP BY<br>
                    • Create views for common analytics queries<br>
                    • Schedule weekly data-quality checks
                </div>""", unsafe_allow_html=True)

            with col_result:
                st.markdown("**Final Clean Dataset Preview**")

                export_cols = [
                    "shipment_id", "origin_warehouse", "destination_city",
                    "destination_state", "carrier", "ship_date", "delivery_date",
                    "weight_kg", "freight_cost", "shipment_status",
                    "items_count", "damage_reported", "transit_days", "was_outlier"
                ]
                export_df = self.df[[
                    c for c in export_cols if c in self.df.columns]].copy()

                st.dataframe(export_df.head(10), width='stretch')

                st.markdown("**Summary Metrics**")
                c1, c2 = st.columns(2)
                c1.metric("Clean Rows",       len(export_df))
                c2.metric("Unique Carriers",  export_df["carrier"].nunique())
                c1.metric(
                    "Avg Freight Cost", f"${export_df['freight_cost'].mean():,.2f}" if "freight_cost" in export_df else "N/A")
                c2.metric("Outliers Capped",  int(
                    export_df["was_outlier"].sum()) if "was_outlier" in export_df else 0)

                if "transit_days" in export_df.columns:
                    avg_transit = export_df["transit_days"].dropna().mean()
                    c1.metric("Avg Transit Days", f"{avg_transit:.1f}" if pd.notna(
                        avg_transit) else "N/A")

                c2.metric("States Served",
                          export_df["destination_state"].nunique())

                # Download
                csv_buf = io.StringIO()
                export_df.to_csv(csv_buf, index=False)

                st.download_button(
                    label="📥 Download Clean Shipments CSV",
                    data=csv_buf.getvalue(),
                    file_name="shipments_clean.csv",
                    mime="text/csv",
                    width='stretch'
                )
                st.success("✅ Clean dataset ready for production!")

        st.divider()

    def output(self):
        self.step_1_inspect_data()
        self.step_2_trim_whitespace()
        self.step_3_standardize_casing()
        self.step_4_nulls()
        self.step_5_duplicates()
        self.step_6_numeric_fix()
        self.step_7_date_validation()
        self.step_8_outliers()
        self.step_9_export()

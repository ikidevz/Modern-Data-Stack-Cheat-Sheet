import streamlit as st
import pandas as pd
import io


class DataCleaningFinanceSQL:
    def __init__(self):
        self.data = [
            ["TXN-1001", "Investment Portfolio", "Apple Inc.",        "AAPL",  "Equities",
                "2024-01-10", "2024-01-12", 152.50, 10, 1525.00,  "Settled",   "Buy",  "No"],
            ["TXN-1002", "retirement fund",      "  Tesla Inc.  ",    "tsla",  "EQUITIES",
                "2024-01-12", "2024-01-11", 238.10, 5,  1190.50,  "settled",   "buy",  "no"],
            ["TXN-1003", "Investment Portfolio", "Apple Inc.",        "AAPL",  "Equities",
                "2024-01-10", "2024-01-12", 152.50, 10, 1525.00,  "Settled",   "Buy",  "No"],
            ["TXN-1004", "Hedge Fund",           "Microsoft Corp.",   "MSFT",  "equities",
                "01/15/2024", "01/17/2024", 375.20, 8,  3001.60,  "Pending",   "Sell", None],
            ["TXN-1005", "investment portfolio", "Nvidia Corp.",      "NVDA",  "Equities",
                None,         "2024-01-20", -88.40, 3,  -265.20,  "Settled",   "Buy",  "Yes"],
            ["TXN-1006", "Hedge Fund",           "Amazon.com Inc.",   "AMZN",  "Equities",
                "2024-01-18", "2024-01-22", 178.30, 12, None,     "Settled",   "Sell", "No"],
            ["TXN-1007", "  Mutual Fund A  ",    "Alphabet Inc.",     "GOOGL", "equities",
                "2024-01-20", "2024-01-24", 140.50, 20, 2810.00,  "settled",   "Buy",  "yes"],
            ["TXN-1008", "Hedge Fund",           "Meta Platforms",    "META",  "Equities",
                "2024/01/22", "2024/01/26", 505.00, 4,  2020.00,  "Pending",   "Buy",  "No"],
            ["TXN-1009", "Retirement Fund",      "Berkshire Hathaway", "BRK.B", "Equities",
                "2024-01-25", "2024-01-29", 361.80, 7,  2532.60,  "Settled",   "Buy",  None],
            ["TXN-1010", "INVESTMENT PORTFOLIO", "  apple inc.  ",    "aapl",  "EQUITIES",
                "2024-02-01", "2024-02-05", 185.20, 6,  1111.20,  "SETTLED",   "SELL", "NO"],
            ["TXN-1011", "Mutual Fund A",        "Shopify Inc.",      "SHOP",  "Equities",
                "2024-02-03", "2024-02-07", 72.40,  15, 1086.00,  "Cancelled", "Buy",  "No"],
            ["TXN-1012", "Hedge Fund",           "Tesla Inc.",        "TSLA",  "Equities",
                "2024-02-05", "2024-02-09", 238.10, 5,  1190.50,  "Settled",   "Sell", "No"],
            ["TXN-1013", "Retirement Fund",      None,                "MSFT",  "Equities",
                "2024-02-08", "2024-02-12", 415.60, 9,  3740.40,  "Settled",   "Buy",  "Yes"],
            ["TXN-1014", "mutual fund a",        "Palantir Tech.",    "PLTR",  "Equities",
                "Feb 10 2024", "Feb 14 2024", 23.80,  50, 1190.00,  "In Review", "Buy",  "No"],
            ["TXN-1015", "Investment Portfolio", "Nvidia Corp.",      "NVDA",  "Equities",
                "2024-02-12", "2024-02-16", 612.30, 2,  1224.60,  "Settled",   "Buy",  "No"],
            ["TXN-1016", "Hedge Fund",           "Amazon.com Inc.",   "AMZN",  "Equities",
                "2024-02-14", "2024-02-18", 178.30, 3,  98000.00, "Settled",   "Sell", "Yes"],
            ["TXN-1017", "  retirement fund  ",  "Coinbase Global",   "COIN",  "CRYPTO",
                "2024-02-18", "2024-02-22", 0.0,    0,  0.00,     "Pending",   "Buy",  None],
            ["TXN-1018", "Mutual Fund A",        "Alphabet Inc.",     "GOOGL", "Equities",
                "2024-02-20", "2024-02-26", 140.50, 20, 2810.00,  "Settled",   "Sell", "No"],
            ["TXN-1019", "Investment Portfolio", "Salesforce Inc.",   "CRM",   "Equities",
                "2024-02-22", None,          273.90, 11, 3012.90,  "In Transit", "Buy",  "No"],
            ["TXN-1020", "Hedge Fund",           "Netflix Inc.",      "NFLX",  "equities",
                "2024-02-25", "2024-03-01", 591.20, 4,  2364.80,  "Settled",   "sell", "no"],
            ["TXN-1021", "Retirement Fund",      "Microsoft Corp.",   "MSFT",  "Equities",
                "2024-03-01", "2024-03-05", 415.60, 7,  2909.20,  "Settled",   "Buy",  "No"],
            ["TXN-1022", "MUTUAL FUND A",        "  Shopify Inc.  ",  "shop",  "EQUITIES",
                "2024-03-03", "2024-03-07", 72.40,  30, 2172.00,  "CANCELLED", "Sell", "NO"],
            ["TXN-1023", "Investment Portfolio", "Apple Inc.",        "AAPL",  "Equities",
                "2024-03-05", "2024-03-09", 185.20, 5,  926.00,   "Settled",   "Buy",  "Yes"],
            ["TXN-1024", "Hedge Fund",           "Tesla Inc.",        "TSLA",  "Equities",
                "March 7 2024", "March 11 2024", 238.10, 8, 1904.80,  "Settled",   "Buy",  "No"],
            ["TXN-1025", "Retirement Fund",      "Nvidia Corp.",      "NVDA",  "Equities",
                "2024-03-10", "2024-03-14", 875.40, 3,  2626.20,  "Settled",   "Buy",  "No"],
        ]
        self.columns = [
            "transaction_id", "fund_name", "company_name",
            "ticker_symbol", "asset_class", "trade_date", "settlement_date",
            "unit_price", "quantity", "total_value", "transaction_status",
            "trade_direction", "flag_review"
        ]
        self.df = pd.DataFrame(self.data, columns=self.columns)

    # ─────────────────────────────────────────────
    # STEP 1 – Inspect
    # ─────────────────────────────────────────────
    def step_1_inspect_data(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1565c0;margin:0.3rem 0;'>🔍 Step 1 – Initial Data Inspection</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "Examine the structure, quality, and basic statistics of your financial transaction dataset")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- View table structure (PostgreSQL)
SELECT
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'transactions'
ORDER BY ordinal_position;
 
-- Preview data
SELECT * FROM transactions
LIMIT 10;
 
-- Row count & duplicate check
SELECT
    COUNT(*)                          AS total_rows,
    COUNT(DISTINCT transaction_id)    AS unique_transactions,
    COUNT(*) - COUNT(DISTINCT transaction_id) AS duplicates
FROM transactions;
 
-- Basic statistics
SELECT
    COUNT(*)                           AS total_records,
    COUNT(DISTINCT transaction_id)     AS unique_transactions,
    COUNT(DISTINCT fund_name)          AS unique_funds,
    COUNT(DISTINCT ticker_symbol)      AS unique_tickers,
    MIN(trade_date)                    AS earliest_trade,
    MAX(trade_date)                    AS latest_trade,
    ROUND(AVG(unit_price)::NUMERIC, 2) AS avg_unit_price,
    MIN(total_value)                   AS min_total_value,
    MAX(total_value)                   AS max_total_value,
    COUNT(DISTINCT asset_class)        AS asset_classes
FROM transactions;
 
-- Data quality issues
SELECT 'Missing company_name'    AS issue, COUNT(*) AS count
FROM transactions WHERE company_name IS NULL OR company_name = ''
UNION ALL
SELECT 'Missing trade_date',     COUNT(*)
FROM transactions WHERE trade_date IS NULL
UNION ALL
SELECT 'Missing total_value',    COUNT(*)
FROM transactions WHERE total_value IS NULL
UNION ALL
SELECT 'Negative unit_price',    COUNT(*)
FROM transactions WHERE unit_price < 0
UNION ALL
SELECT 'Negative quantity',      COUNT(*)
FROM transactions WHERE quantity < 0;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 SQL Tip:</strong><br>
                    Always inspect raw financial data first. Look for type
                    mismatches, inconsistent casing, NULLs, and impossible
                    values (e.g. negative prices) before writing any cleaning
                    logic. Regulatory audits require clean audit trails.
                </div>""", unsafe_allow_html=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ Best Practice:</strong><br>
                    • Document original schema before changes<br>
                    • Identify primary keys and NOT NULL expectations<br>
                    • Note mixed date formats early (trade vs settlement)<br>
                    • Flag columns with suspicious numeric ranges
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
                c1.metric("Total Records",    len(self.df))
                c2.metric("Unique Transactions",
                          self.df["transaction_id"].nunique())
                c1.metric("Unique Funds",
                          self.df["fund_name"].str.strip().str.upper().nunique())
                c2.metric(
                    "Unique Tickers",   self.df["ticker_symbol"].str.strip().str.upper().nunique())
                c1.metric("Missing Cols",     int(
                    self.df.isnull().any(axis=1).sum()))
                c2.metric(
                    "Asset Classes",    self.df["asset_class"].str.strip().str.upper().nunique())

        st.divider()

    # ─────────────────────────────────────────────
    # STEP 2 – Trim Whitespace
    # ─────────────────────────────────────────────
    def step_2_trim_whitespace(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1565c0;margin:0.3rem 0;'>✂️ Step 2 – Remove Leading / Trailing Whitespace</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "TRIM() removes invisible spaces that break GROUP BY, JOINs, and ticker lookups")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- PostgreSQL: TRIM all key text columns
SELECT
    transaction_id,
    TRIM(fund_name)          AS fund_name,
    TRIM(company_name)       AS company_name,
    TRIM(ticker_symbol)      AS ticker_symbol,
    TRIM(asset_class)        AS asset_class
FROM transactions;
 
-- Update in place
UPDATE transactions
SET
    fund_name           = TRIM(fund_name),
    company_name        = TRIM(company_name),
    ticker_symbol       = TRIM(ticker_symbol),
    asset_class         = TRIM(asset_class),
    transaction_status  = TRIM(transaction_status),
    trade_direction     = TRIM(trade_direction),
    flag_review         = TRIM(flag_review);
 
-- Verify no more leading/trailing spaces remain
SELECT transaction_id, fund_name
FROM transactions
WHERE fund_name <> TRIM(fund_name);""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 SQL Tip:</strong><br>
                    In PostgreSQL, <code>TRIM(col)</code> removes spaces from
                    both ends. For financial ticker symbols, a stray space
                    like <code>'AAPL '</code> will silently fail any market
                    data API lookup. Always TRIM before case-standardisation.
                </div>""", unsafe_allow_html=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ Best Practice:</strong><br>
                    • TRIM every text column on ingest<br>
                    • Run TRIM before UPPER / INITCAP<br>
                    • Verify with WHERE col &lt;&gt; TRIM(col)<br>
                    • Pay special attention to ticker symbols — API calls are exact-match
                </div>""", unsafe_allow_html=True)

            with col_result:
                st.markdown("**Before (raw values with spaces)**")
                before = self.df[["transaction_id", "fund_name",
                                  "company_name", "ticker_symbol"]].head(8).copy()
                st.dataframe(before, width='stretch')

                for col in ["fund_name", "company_name", "ticker_symbol",
                            "asset_class", "transaction_status",
                            "trade_direction", "flag_review"]:
                    self.df[col] = self.df[col].astype(
                        str).str.strip().replace("None", "")
                    self.df[col] = self.df[col].where(
                        self.df[col] != "", other=None)

                st.markdown("**After TRIM()**")
                after = self.df[["transaction_id", "fund_name",
                                 "company_name", "ticker_symbol"]].head(8)
                st.dataframe(after, width='stretch')

                had_spaces = before["fund_name"].apply(
                    lambda x: x != x.strip()).sum()
                st.success(
                    f"✅ Fixed {had_spaces} cells with leading/trailing spaces")

        st.divider()

    # ─────────────────────────────────────────────
    # STEP 3 – Standardize Casing
    # ─────────────────────────────────────────────
    def step_3_standardize_casing(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1565c0;margin:0.3rem 0;'>🔡 Step 3 – Standardize Text Casing</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "Uniform casing prevents duplicate groups, broken joins, and mismatched ticker lookups")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- PostgreSQL: UPPER for codes, INITCAP for names
SELECT
    transaction_id,
    INITCAP(TRIM(fund_name))          AS fund_name,
    INITCAP(TRIM(company_name))       AS company_name,
    UPPER(TRIM(ticker_symbol))        AS ticker_symbol,
    UPPER(TRIM(asset_class))          AS asset_class,
    INITCAP(TRIM(transaction_status)) AS transaction_status,
    UPPER(TRIM(trade_direction))      AS trade_direction
FROM transactions;
 
-- Update in place
UPDATE transactions
SET
    fund_name          = INITCAP(TRIM(fund_name)),
    company_name       = INITCAP(TRIM(company_name)),
    ticker_symbol      = UPPER(TRIM(ticker_symbol)),
    asset_class        = UPPER(TRIM(asset_class)),
    transaction_status = INITCAP(TRIM(transaction_status)),
    trade_direction    = UPPER(TRIM(trade_direction));
 
-- Verify distinct values after standardisation
SELECT DISTINCT ticker_symbol FROM transactions ORDER BY 1;
SELECT DISTINCT transaction_status FROM transactions ORDER BY 1;
SELECT DISTINCT trade_direction FROM transactions ORDER BY 1;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 SQL Tip:</strong><br>
                    • <code>UPPER()</code> – ticker symbols, asset classes, BUY/SELL<br>
                    • <code>INITCAP()</code> – fund names, company names, statuses<br>
                    • Never mix cases — GROUP BY is case-sensitive in SQL
                </div>""", unsafe_allow_html=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ Best Practice:</strong><br>
                    • Ticker symbols → UPPER (AAPL, TSLA, NVDA)<br>
                    • Trade direction → UPPER (BUY, SELL)<br>
                    • Fund/company names → INITCAP<br>
                    • Asset class → UPPER (EQUITIES, CRYPTO)
                </div>""", unsafe_allow_html=True)

            with col_result:
                st.markdown("**Before (mixed case)**")
                cols = ["transaction_id", "fund_name", "ticker_symbol",
                        "asset_class", "transaction_status", "trade_direction"]
                before = self.df[cols].head(8).copy()
                st.dataframe(before, width='stretch')

                self.df["fund_name"] = self.df["fund_name"].apply(
                    lambda x: x.strip().title() if pd.notna(x) else x)
                self.df["company_name"] = self.df["company_name"].apply(
                    lambda x: x.strip().title() if pd.notna(x) else x)
                self.df["ticker_symbol"] = self.df["ticker_symbol"].apply(
                    lambda x: x.strip().upper() if pd.notna(x) else x)
                self.df["asset_class"] = self.df["asset_class"].apply(
                    lambda x: x.strip().upper() if pd.notna(x) else x)
                self.df["transaction_status"] = self.df["transaction_status"].apply(
                    lambda x: x.strip().title() if pd.notna(x) else x)
                self.df["trade_direction"] = self.df["trade_direction"].apply(
                    lambda x: x.strip().upper() if pd.notna(x) else x)

                st.markdown("**After Casing**")
                st.dataframe(self.df[cols].head(8), width='stretch')

                st.markdown("**Distinct tickers after fix:**")
                st.write(
                    sorted(self.df["ticker_symbol"].dropna().unique().tolist()))
                st.success("✅ Casing standardised")

        st.divider()

    # ─────────────────────────────────────────────
    # STEP 4 – Replace String "NULL" & Handle True NULLs
    # ─────────────────────────────────────────────
    def step_4_nulls(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1565c0;margin:0.3rem 0;'>❓ Step 4 – Replace String \"NULL\" & Handle True NULLs</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "String 'NULL' is not a real NULL — critical for financial integrity checks")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- Replace literal 'NULL' string with proper NULL
UPDATE transactions
SET flag_review = NULL
WHERE UPPER(TRIM(flag_review)) = 'NULL';
 
-- Use COALESCE to fill true NULLs with defaults
SELECT
    transaction_id,
    CASE
        WHEN UPPER(TRIM(flag_review)) = 'NULL' THEN NULL
        ELSE INITCAP(TRIM(flag_review))
    END                                                AS flag_review,
    COALESCE(company_name, 'Unknown Company')          AS company_name,
    COALESCE(settlement_date::TEXT, 'Pending Settlement') AS settlement_date
FROM transactions;
 
-- Count NULLs per critical column
SELECT
    COUNT(*) - COUNT(trade_date)       AS missing_trade_date,
    COUNT(*) - COUNT(settlement_date)  AS missing_settlement_date,
    COUNT(*) - COUNT(total_value)      AS missing_total_value,
    COUNT(*) - COUNT(company_name)     AS missing_company,
    COUNT(*) - COUNT(flag_review)      AS missing_flag_review
FROM transactions;
 
-- Strategy: fill missing total_value from unit_price * quantity
UPDATE transactions
SET total_value = ROUND(unit_price * quantity, 2)
WHERE total_value IS NULL
  AND unit_price IS NOT NULL
  AND quantity   IS NOT NULL;
 
-- Mark records with any critical NULL
ALTER TABLE transactions ADD COLUMN data_quality VARCHAR(20);
UPDATE transactions
SET data_quality = CASE
    WHEN company_name IS NULL OR total_value IS NULL THEN 'Incomplete'
    WHEN trade_date IS NULL                          THEN 'Missing Date'
    ELSE 'Complete'
END;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 SQL Tip:</strong><br>
                    In financial data, a missing <code>total_value</code> can
                    often be reconstructed from <code>unit_price × quantity</code>.
                    Always prefer derivation over imputation with averages for
                    monetary columns — averages introduce reporting inaccuracies.
                </div>""", unsafe_allow_html=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ NULL Handling Strategies:</strong><br>
                    • Derive total_value from unit_price × quantity<br>
                    • Default text for optional columns ('Unknown Company')<br>
                    • Flag incomplete rows with a data_quality column<br>
                    • Never impute monetary values with statistical averages
                </div>""", unsafe_allow_html=True)

            with col_result:
                st.markdown("**Missing Values Before**")
                raw_null = self.df.isnull().sum()
                string_null = self.df.apply(lambda col: col.astype(
                    str).str.upper().str.strip().eq("NULL").sum())
                missing_df = pd.DataFrame({
                    "Column": raw_null.index,
                    "True NULLs": raw_null.values,
                    "String 'NULL'": string_null.values
                })
                missing_df = missing_df[(missing_df["True NULLs"] > 0) | (
                    missing_df["String 'NULL'"] > 0)]
                st.dataframe(missing_df, hide_index=True, width='stretch')

                for col in self.df.columns:
                    mask = self.df[col].astype(
                        str).str.upper().str.strip() == "NULL"
                    self.df.loc[mask, col] = None

                self.df["company_name"] = self.df["company_name"].fillna(
                    "Unknown Company")

                self.df["total_value"] = pd.to_numeric(
                    self.df["total_value"], errors="coerce")
                self.df["unit_price"] = pd.to_numeric(
                    self.df["unit_price"],  errors="coerce")
                self.df["quantity"] = pd.to_numeric(
                    self.df["quantity"],     errors="coerce")

                mask_missing = self.df["total_value"].isnull() & \
                    self.df["unit_price"].notna() & \
                    self.df["quantity"].notna()
                self.df.loc[mask_missing, "total_value"] = (
                    self.df.loc[mask_missing, "unit_price"] *
                    self.df.loc[mask_missing, "quantity"]
                ).round(2)

                st.markdown("**After NULL Handling**")
                st.metric("Remaining True NULLs (total_value)",
                          int(self.df["total_value"].isnull().sum()))
                st.dataframe(
                    self.df[["transaction_id", "company_name",
                             "total_value", "flag_review"]].head(10),
                    width='stretch'
                )
                st.success(
                    "✅ String NULLs replaced; missing total_value derived from unit_price × quantity")

        st.divider()

    # ─────────────────────────────────────────────
    # STEP 5 – Remove Exact Duplicates
    # ─────────────────────────────────────────────
    def step_5_duplicates(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1565c0;margin:0.3rem 0;'>🔁 Step 5 – Remove Exact Duplicate Rows</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "Use ROW_NUMBER() to rank duplicates — duplicate trades overstate portfolio value and volume")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- Detect exact duplicates using ROW_NUMBER()
WITH ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY
                fund_name,
                ticker_symbol,
                trade_direction,
                trade_date,
                CAST(unit_price AS TEXT),
                CAST(quantity   AS TEXT)
            ORDER BY transaction_id
        ) AS row_num
    FROM transactions
)
SELECT * EXCEPT (row_num)          -- BigQuery syntax
FROM ranked
WHERE row_num = 1;
 
-- PostgreSQL equivalent (no EXCEPT, use subquery)
DELETE FROM transactions
WHERE transaction_id NOT IN (
    SELECT MIN(transaction_id)
    FROM transactions
    GROUP BY
        fund_name,
        ticker_symbol,
        trade_direction,
        trade_date,
        unit_price,
        quantity
);
 
-- How many exact duplicates exist?
SELECT
    fund_name, ticker_symbol, trade_direction,
    trade_date, unit_price, quantity,
    COUNT(*) AS occurrence_count
FROM transactions
GROUP BY
    fund_name, ticker_symbol, trade_direction,
    trade_date, unit_price, quantity
HAVING COUNT(*) > 1;
 
-- Create clean table keeping one per group
CREATE TABLE transactions_clean AS
WITH ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY fund_name, ticker_symbol, trade_direction,
                         trade_date, unit_price, quantity
            ORDER BY transaction_id
        ) AS rn
    FROM transactions
)
SELECT transaction_id, fund_name, company_name,
       ticker_symbol, asset_class, trade_date, settlement_date,
       unit_price, quantity, total_value, transaction_status,
       trade_direction, flag_review
FROM ranked WHERE rn = 1;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ Deduplication Strategy:</strong><br>
                    • <b>Exact dups:</b> identical in ALL columns<br>
                    • <b>Semantic dups:</b> same fund + ticker + date + direction<br>
                    • Keep lowest transaction_id as canonical row<br>
                    • Duplicate trades inflate AUM — always back up before deleting
                </div>""", unsafe_allow_html=True)

            with col_result:
                st.markdown("**Duplicate Analysis**")
                total = len(self.df)
                key_cols = ["fund_name", "ticker_symbol", "trade_direction",
                            "trade_date", "unit_price", "quantity"]
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
                        dup_rows[["transaction_id", "fund_name", "ticker_symbol",
                                  "trade_direction", "trade_date"]].sort_values("transaction_id"),
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
    # STEP 6 – Fix Negative & Suspicious Numeric Values
    # ─────────────────────────────────────────────
    def step_6_numeric_fix(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1565c0;margin:0.3rem 0;'>🔢 Step 6 – Fix Negative & Suspicious Numeric Values</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "Negative unit prices or quantities are data-entry errors — fix with ABS() or context-based logic")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- Inspect suspicious numeric values
SELECT
    transaction_id,
    unit_price,
    quantity,
    total_value
FROM transactions
WHERE unit_price  < 0
   OR unit_price  = 0
   OR quantity    < 0
   OR total_value < 0;
 
-- Fix unit_price
SELECT
    transaction_id,
    CASE
        WHEN unit_price < 0 THEN ABS(unit_price)  -- likely sign error
        WHEN unit_price = 0 THEN NULL              -- zero = unknown price
        ELSE unit_price
    END AS unit_price_cleaned
FROM transactions;
 
-- Fix quantity
SELECT
    transaction_id,
    CASE
        WHEN quantity < 0 THEN ABS(quantity)
        WHEN quantity = 0 THEN NULL
        ELSE quantity
    END AS quantity_cleaned
FROM transactions;
 
-- Apply updates
UPDATE transactions
SET unit_price = CASE
    WHEN unit_price < 0 THEN ABS(unit_price)
    WHEN unit_price = 0 THEN NULL
    ELSE unit_price
END;
 
UPDATE transactions
SET quantity = CASE
    WHEN quantity < 0 THEN ABS(quantity)
    WHEN quantity = 0 THEN NULL
    ELSE quantity
END;
 
-- Also NULL out zero total_value (likely missing, not zero-dollar)
UPDATE transactions
SET total_value = NULL
WHERE total_value = 0;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='warning-box'>
                    <strong>⚠️ Decision point:</strong><br>
                    • Negative unit_price → sign flip error → use ABS()<br>
                    • Zero unit_price → unknown → NULL<br>
                    • Zero quantity → entry error → NULL<br>
                    • Negative total_value → may indicate a SELL short — verify against trade_direction first
                </div>""", unsafe_allow_html=True)

            with col_result:
                st.markdown("**Suspicious Values Found**")
                self.df["unit_price"] = pd.to_numeric(
                    self.df["unit_price"],  errors="coerce")
                self.df["quantity"] = pd.to_numeric(
                    self.df["quantity"],     errors="coerce")
                self.df["total_value"] = pd.to_numeric(
                    self.df["total_value"],  errors="coerce")

                neg_price = int((self.df["unit_price"] < 0).sum())
                zero_price = int((self.df["unit_price"] == 0).sum())
                neg_qty = int((self.df["quantity"] < 0).sum())
                zero_qty = int((self.df["quantity"] == 0).sum())

                issue_df = pd.DataFrame({
                    "Issue":  ["Negative unit_price", "Zero unit_price",
                               "Negative quantity",   "Zero quantity"],
                    "Count":  [neg_price, zero_price, neg_qty, zero_qty]
                })
                st.dataframe(issue_df, hide_index=True, width='stretch')

                bad = self.df[
                    (self.df["unit_price"] < 0) | (self.df["unit_price"] == 0) |
                    (self.df["quantity"] < 0) | (self.df["quantity"] == 0)
                ]
                if not bad.empty:
                    st.markdown("**Records before fix:**")
                    st.dataframe(
                        bad[["transaction_id", "unit_price",
                            "quantity", "total_value"]],
                        width='stretch'
                    )

                self.df["unit_price"] = self.df["unit_price"].apply(
                    lambda x: abs(x) if pd.notna(x) and x < 0
                    else (None if pd.notna(x) and x == 0 else x))
                self.df["quantity"] = self.df["quantity"].apply(
                    lambda x: abs(x) if pd.notna(x) and x < 0
                    else (None if pd.notna(x) and x == 0 else x))
                self.df["total_value"] = self.df["total_value"].apply(
                    lambda x: None if pd.notna(x) and x == 0 else x)

                st.markdown("**After fix:**")
                st.dataframe(
                    self.df[["transaction_id", "unit_price",
                             "quantity", "total_value"]].head(10),
                    width='stretch'
                )
                st.success("✅ Negative values corrected; zeros nulled")

        st.divider()

    # ─────────────────────────────────────────────
    # STEP 7 – Validate Date Logic (Trade Before Settlement)
    # ─────────────────────────────────────────────
    def step_7_date_validation(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1565c0;margin:0.3rem 0;'>📅 Step 7 – Validate Date Logic (Settlement After Trade Date)</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "Parse multiple date formats and flag impossible settlement-before-trade-date records (T+2 standard)")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- PostgreSQL: parse mixed date formats safely
-- Step 1: normalise text dates to YYYY-MM-DD
UPDATE transactions
SET trade_date = TO_DATE(trade_date, 'MM/DD/YYYY')
WHERE trade_date ~ '^\\d{2}/\\d{2}/\\d{4}$';
 
UPDATE transactions
SET trade_date = TO_DATE(trade_date, 'YYYY/MM/DD')
WHERE trade_date ~ '^\\d{4}/\\d{2}/\\d{2}$';
 
UPDATE transactions
SET trade_date = TO_DATE(trade_date, 'Month DD YYYY')
WHERE trade_date ~ '^[A-Za-z]+ \\d{1,2} \\d{4}$';
 
-- Step 2: cast to DATE
ALTER TABLE transactions
    ALTER COLUMN trade_date      TYPE DATE USING trade_date::DATE,
    ALTER COLUMN settlement_date TYPE DATE USING settlement_date::DATE;
 
-- Step 3: calculate settlement lag & flag bad dates
SELECT
    transaction_id,
    trade_date,
    settlement_date,
    settlement_date - trade_date                       AS settlement_days,
    CASE
        WHEN settlement_date < trade_date  THEN 'INVALID'
        WHEN settlement_date = trade_date  THEN 'SAME DAY T+0'
        WHEN settlement_date - trade_date = 2 THEN 'STANDARD T+2'
        ELSE 'NON-STANDARD'
    END                                                AS settlement_flag
FROM transactions;
 
-- Step 4: fix invalid (swap dates)
UPDATE transactions
SET trade_date      = settlement_date,
    settlement_date = trade_date
WHERE settlement_date < trade_date;
 
-- Step 5: remove future trade dates
DELETE FROM transactions
WHERE trade_date > CURRENT_DATE;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 SQL Tip:</strong><br>
                    Equity trades typically settle T+2 (two business days
                    after the trade date). Use <code>settlement_date -
                    trade_date</code> to flag non-standard settlement windows
                    for compliance review alongside format errors.
                </div>""", unsafe_allow_html=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ Date Cleaning Checklist:</strong><br>
                    • Parse all format variants (MM/DD/YYYY, YYYY/MM/DD, Month D YYYY)<br>
                    • Cast to DATE after normalising<br>
                    • Flag settlement_date &lt; trade_date as INVALID<br>
                    • Flag non-T+2 settlements for compliance review<br>
                    • Null out missing settlement_date (trade pending settlement)
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

                self.df["trade_date"] = self.df["trade_date"].astype(
                    str).apply(parse_date)
                self.df["settlement_date"] = self.df["settlement_date"].astype(
                    str).apply(parse_date)
                self.df["settlement_days"] = (
                    self.df["settlement_date"] - self.df["trade_date"]).dt.days

                def date_flag(row):
                    if pd.isna(row["settlement_date"]):
                        return "⏳ Pending"
                    if row["settlement_date"] < row["trade_date"]:
                        return "⛔ INVALID"
                    if row["settlement_days"] == 0:
                        return "⚡ T+0"
                    if row["settlement_days"] == 2:
                        return "✅ T+2"
                    return f"⚠️ T+{row['settlement_days']}"

                self.df["settlement_flag"] = self.df.apply(date_flag, axis=1)

                invalid_dates = (
                    self.df["settlement_flag"] == "⛔ INVALID").sum()
                pending = (self.df["settlement_flag"] == "⏳ Pending").sum()

                c1, c2 = st.columns(2)
                c1.metric("Invalid Dates",           int(invalid_dates))
                c2.metric("Pending Settlement",      int(pending))

                st.dataframe(
                    self.df[["transaction_id", "trade_date", "settlement_date",
                             "settlement_days", "settlement_flag"]],
                    width='stretch'
                )

                mask = self.df["settlement_flag"] == "⛔ INVALID"
                self.df.loc[mask, ["trade_date", "settlement_date"]] = \
                    self.df.loc[mask, ["settlement_date", "trade_date"]].values
                self.df["settlement_days"] = (
                    self.df["settlement_date"] - self.df["trade_date"]).dt.days

                if invalid_dates:
                    st.success(
                        f"✅ Swapped trade/settlement dates for {invalid_dates} invalid record(s)")

        st.divider()

    # ─────────────────────────────────────────────
    # STEP 8 – Detect & Cap Outliers Using IQR
    # ─────────────────────────────────────────────
    def step_8_outliers(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1565c0;margin:0.3rem 0;'>📊 Step 8 – Detect & Cap Outliers Using IQR</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "Use the IQR method to flag and cap extreme total_value transaction amounts")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- PostgreSQL: IQR outlier detection on total_value
WITH stats AS (
    SELECT
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY total_value) AS q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY total_value) AS q3
    FROM transactions
    WHERE total_value > 0           -- exclude zero/NULL
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
    t.transaction_id,
    t.total_value                    AS original_value,
    CASE
        WHEN t.total_value > b.upper_bound THEN b.upper_bound
        WHEN t.total_value < b.lower_bound THEN b.lower_bound
        ELSE t.total_value
    END                              AS cleaned_value,
    CASE
        WHEN t.total_value > b.upper_bound
          OR t.total_value < b.lower_bound THEN TRUE
        ELSE FALSE
    END                              AS was_outlier
FROM transactions t
CROSS JOIN bounds b;
 
-- Apply cap update
WITH stats AS (
    SELECT
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY total_value) AS q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY total_value) AS q3
    FROM transactions WHERE total_value > 0
),
bounds AS (
    SELECT q1 - 1.5*(q3-q1) AS lb, q3 + 1.5*(q3-q1) AS ub FROM stats
)
UPDATE transactions
SET total_value = CASE
    WHEN total_value > (SELECT ub FROM bounds) THEN (SELECT ub FROM bounds)
    WHEN total_value < (SELECT lb FROM bounds) THEN (SELECT lb FROM bounds)
    ELSE total_value
END;
 
-- Z-score alternative for regulatory flagging
WITH stats AS (
    SELECT AVG(total_value) AS mean, STDDEV(total_value) AS std
    FROM transactions WHERE total_value > 0
)
SELECT transaction_id, total_value,
    (total_value - mean) / std AS z_score
FROM transactions, stats
WHERE ABS((total_value - mean) / std) > 3;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 PostgreSQL vs BigQuery:</strong><br>
                    BigQuery uses <code>APPROX_QUANTILES(col, 100)[OFFSET(25)]</code>.
                    PostgreSQL uses the exact <code>PERCENTILE_CONT(0.25)
                    WITHIN GROUP (ORDER BY col)</code>. For AML compliance,
                    prefer exact percentiles over approximations.
                </div>""", unsafe_allow_html=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ Outlier Options:</strong><br>
                    • <b>Cap (Winsorize):</b> replace with boundary value<br>
                    • <b>Flag:</b> keep but mark <code>was_outlier = TRUE</code> for compliance<br>
                    • <b>Escalate:</b> route to AML review if |z| > 3<br>
                    • <b>Never silently delete</b> financial records — audit trail required
                </div>""", unsafe_allow_html=True)

            with col_result:
                st.markdown("**Outlier Analysis – total_value**")

                clean_tv = self.df["total_value"].dropna()
                clean_tv = clean_tv[clean_tv > 0]

                Q1 = clean_tv.quantile(0.25)
                Q3 = clean_tv.quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - 1.5 * IQR
                upper = Q3 + 1.5 * IQR

                c1, c2 = st.columns(2)
                c1.metric("Q1",          f"${Q1:,.2f}")
                c2.metric("Q3",          f"${Q3:,.2f}")
                c1.metric("IQR",         f"${IQR:,.2f}")
                c2.metric("Lower Bound", f"${lower:,.2f}")
                c1.metric("Upper Bound", f"${upper:,.2f}")

                outliers = self.df[
                    (self.df["total_value"] > upper) |
                    (self.df["total_value"] < lower)
                ]
                c2.metric("Outliers Found", len(outliers))

                if not outliers.empty:
                    st.markdown("**Outlier Records:**")
                    st.dataframe(
                        outliers[["transaction_id", "ticker_symbol",
                                  "trade_direction", "total_value"]],
                        width='stretch'
                    )

                self.df["original_value"] = self.df["total_value"]
                self.df["total_value"] = self.df["total_value"].clip(
                    lower=lower, upper=upper)
                self.df["was_outlier"] = self.df["original_value"].apply(
                    lambda x: True if pd.notna(x) and (
                        x > upper or x < lower) else False
                )

                st.markdown(f"**Valid range:** ${lower:,.2f} – ${upper:,.2f}")
                st.dataframe(
                    self.df[["transaction_id", "original_value",
                             "total_value", "was_outlier"]].head(10),
                    width='stretch'
                )
                st.success(
                    f"✅ Flagged & capped {len(outliers)} outlier(s) to IQR bounds")

        st.divider()

    # ─────────────────────────────────────────────
    # STEP 9 – Export Clean Table
    # ─────────────────────────────────────────────
    def step_9_export(self):
        with st.container():
            st.markdown(
                "<h3 style='color:#1565c0;margin:0.3rem 0;'>💾 Step 9 – Create Clean Table & Export</h3>",
                unsafe_allow_html=True
            )
            st.caption(
                "Final production-ready schema with constraints, indexes, computed columns, and compliance views")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- Create clean production table (PostgreSQL)
CREATE TABLE transactions_clean (
    transaction_id      VARCHAR(20)     PRIMARY KEY,
    fund_name           VARCHAR(100)    NOT NULL,
    company_name        VARCHAR(150)    NOT NULL DEFAULT 'Unknown Company',
    ticker_symbol       VARCHAR(10)     NOT NULL,
    asset_class         VARCHAR(50)     NOT NULL,
    trade_date          DATE            NOT NULL,
    settlement_date     DATE,
    unit_price          NUMERIC(12,4)   CHECK (unit_price > 0),
    quantity            INTEGER         CHECK (quantity > 0),
    total_value         NUMERIC(15,2)   CHECK (total_value > 0),
    transaction_status  VARCHAR(50),
    trade_direction     VARCHAR(10)     CHECK (trade_direction IN ('BUY','SELL')),
    flag_review         VARCHAR(20),
    settlement_days     INTEGER
        GENERATED ALWAYS AS (settlement_date - trade_date) STORED,
    is_settled          BOOLEAN
        GENERATED ALWAYS AS (transaction_status = 'Settled') STORED,
    was_outlier         BOOLEAN         DEFAULT FALSE,
    created_at          TIMESTAMPTZ     DEFAULT NOW()
);
 
-- Insert from cleaned staging table
INSERT INTO transactions_clean
    (transaction_id, fund_name, company_name,
     ticker_symbol, asset_class, trade_date, settlement_date,
     unit_price, quantity, total_value, transaction_status,
     trade_direction, flag_review, was_outlier)
SELECT
    transaction_id,
    INITCAP(TRIM(fund_name)),
    COALESCE(INITCAP(TRIM(company_name)), 'Unknown Company'),
    UPPER(TRIM(ticker_symbol)),
    UPPER(TRIM(asset_class)),
    trade_date::DATE,
    settlement_date::DATE,
    CASE WHEN unit_price  <= 0 THEN NULL ELSE ABS(unit_price) END,
    CASE WHEN quantity    <= 0 THEN NULL ELSE ABS(quantity)   END,
    CASE WHEN total_value <= 0 THEN NULL ELSE total_value     END,
    INITCAP(TRIM(transaction_status)),
    UPPER(TRIM(trade_direction)),
    CASE WHEN UPPER(TRIM(flag_review)) = 'NULL' THEN NULL
         ELSE INITCAP(TRIM(flag_review)) END,
    was_outlier
FROM transactions_staging
WHERE trade_date IS NOT NULL
  AND (settlement_date IS NULL OR settlement_date >= trade_date);
 
-- Indexes for analytics & compliance performance
CREATE INDEX idx_ticker      ON transactions_clean(ticker_symbol);
CREATE INDEX idx_trade_date  ON transactions_clean(trade_date);
CREATE INDEX idx_fund        ON transactions_clean(fund_name);
CREATE INDEX idx_status      ON transactions_clean(transaction_status);
CREATE INDEX idx_direction   ON transactions_clean(trade_direction);
 
-- Analytics views
CREATE VIEW fund_performance AS
SELECT
    fund_name,
    COUNT(*)                              AS total_transactions,
    ROUND(AVG(settlement_days), 1)        AS avg_settlement_days,
    ROUND(AVG(total_value)::NUMERIC, 2)   AS avg_trade_value,
    SUM(CASE WHEN is_settled THEN 1 ELSE 0 END) AS settled_count,
    SUM(CASE WHEN trade_direction = 'BUY'  THEN total_value ELSE 0 END) AS total_bought,
    SUM(CASE WHEN trade_direction = 'SELL' THEN total_value ELSE 0 END) AS total_sold
FROM transactions_clean
GROUP BY fund_name;
 
-- Export to CSV (psql)
COPY transactions_clean TO '/tmp/transactions_clean.csv'
WITH (FORMAT CSV, HEADER TRUE);""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 Production Best Practices:</strong><br>
                    • Never overwrite source data — write to a _clean table<br>
                    • Add GENERATED columns for settlement_days and is_settled<br>
                    • Index ticker, fund, trade_date for fast query performance<br>
                    • Create compliance views separating BUY vs SELL exposure<br>
                    • Schedule nightly data-quality checks for regulatory audit
                </div>""", unsafe_allow_html=True)

            with col_result:
                st.markdown("**Final Clean Dataset Preview**")

                export_cols = [
                    "transaction_id", "fund_name", "company_name",
                    "ticker_symbol", "asset_class", "trade_date", "settlement_date",
                    "unit_price", "quantity", "total_value", "transaction_status",
                    "trade_direction", "flag_review", "settlement_days", "was_outlier"
                ]
                export_df = self.df[[
                    c for c in export_cols if c in self.df.columns]].copy()

                st.dataframe(export_df.head(10), width='stretch')

                st.markdown("**Summary Metrics**")
                c1, c2 = st.columns(2)
                c1.metric("Clean Rows",        len(export_df))
                c2.metric("Unique Tickers",
                          export_df["ticker_symbol"].nunique())
                c1.metric(
                    "Avg Trade Value",
                    f"${export_df['total_value'].mean():,.2f}"
                    if "total_value" in export_df else "N/A")
                c2.metric("Outliers Flagged",  int(
                    export_df["was_outlier"].sum()) if "was_outlier" in export_df else 0)

                if "settlement_days" in export_df.columns:
                    avg_settle = export_df["settlement_days"].dropna().mean()
                    c1.metric("Avg Settlement Days",
                              f"{avg_settle:.1f}" if pd.notna(avg_settle) else "N/A")

                c2.metric("Unique Funds",
                          export_df["fund_name"].nunique())

                csv_buf = io.StringIO()
                export_df.to_csv(csv_buf, index=False)

                st.download_button(
                    label="📥 Download Clean Transactions CSV",
                    data=csv_buf.getvalue(),
                    file_name="transactions_clean.csv",
                    mime="text/csv",
                    width='stretch'
                )
                st.success("✅ Clean financial dataset ready for production!")

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

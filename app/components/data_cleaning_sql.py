import streamlit as st
import pandas as pd
import io


class DataCleaningSQL:
    def __init__(self):
        self.data = [
            [1001, "John Smith", "john.smith@gmail.com", "2023-11-02",
                "Apple Watch", 1, 399.99, "usa", "Delivered", "-"],
            [1002, "john smith", "john.smith@gmail.com", "11/02/2023",
                "apple watch", 1, "$399.99", "USA", "delivered", "Duplicate name?"],
            [1003, "SARAH THOMPSON", "sarah.t@gmail.com", "2023/10/30", "Samsung Galaxy S22",
                "two", 799, "United States", "shipped", "customer requested refund"],
            [1004, "Tom O'Brien", None, "2023-11-05",
                "Google Pixel", 1, 599, "UK", "Delivered", None],
            [1005, "Mary Johnson", "mary.j@gmail.com", "2023-11-06", "Samsung Galaxy S22",
                2, 800, "United Kingdom", "returned", "Return due to defect"],
            [1006, "Ankit Patel", "ankit@@patel.com", "2023-11-07",
                None, 1, 0, "india", "pending", "no stock"],
            [1007, "John Smith", "john.smith@gmail.com", "2023-11-02",
                "Apple Watch", 1, 399.99, "usa", "delivered", "Duplicate?"],
            [1008, "Carlos Hernández", "carlos@hernandez.com", "2023-11-08",
                "Iphone 14", 1, "1099.00", "spain", "DELIVERED", "-"],
            [1009, None, "jessica@abc.com", "2023-11-09", "Macbook Pro",
                1, 1299.99, "canada", "returned", "Missing name"],
            [1010, "Aisha Khan", "aisha.khan@outlook", "2023-11-10", "MacBook Pro",
                1, 1299.99, "CANADA", "Returned", "check eligibility"],
            [1011, "Sarah Thompson", "sarah.t@gmail.com", "2023-10-30",
                "Samsung Galaxy S22", 2, 799, "US", "refunded", "updated payment method"],
            [1012, "tom o'brien", "tom.obrien@gmail.com", "2023-11-05",
                "Google pixel", 1, 599, "uk", "Delivered", "no comment"],
            [1013, "Mary Johnson", "mary.j@gmail.com", "2023-11-06",
                "SAMSUNG GALAXY S22", 2, 800, "UK", "Returned", None],
            [1014, "Ankit Patel", "ankit@patel.com", "2023-11-07",
                "Samsung Galaxy S22", 1, None, "India", "Pending", "missing price"],
            [1015, "Carlos Hernández", "carlos@hernandez.com", "2023-11-08",
                "iPhone 14", 1, 1099, "Spain", "delivered", "duplicate product format"]
        ]
        self.columns = [
            "order_id", "customer_name", "email", "order_date",
            "product_name", "quantity", "price", "country",
            "order_status", "notes"
        ]
        self.df = pd.DataFrame(self.data, columns=self.columns)

    def step_1_inspect_data(self):
        """Step 1: Initial Data Inspection"""
        with st.container():
            st.markdown(
                "<h3 style='color: #1976d2; margin: 0.3rem 0;'>🔍 Step 1 – Initial Data Inspection</h3>",
                unsafe_allow_html=True
            )

            st.caption(
                "Examine the structure, quality, and basic statistics of your dataset")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- View table structure (MySQL)
DESCRIBE customer_orders;

-- PostgreSQL equivalent
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'customer_orders'
ORDER BY ordinal_position;

-- Preview data
SELECT * FROM customer_orders
LIMIT 10;

-- Get row count
SELECT COUNT(*) as total_rows
FROM customer_orders;

-- Check for duplicates
SELECT 
    COUNT(*) as total_rows,
    COUNT(DISTINCT order_id) as unique_orders,
    COUNT(*) - COUNT(DISTINCT order_id) as duplicates
FROM customer_orders;

-- Basic statistics
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT order_id) as unique_orders,
    COUNT(DISTINCT customer_name) as unique_customers,
    MIN(order_date) as earliest_order,
    MAX(order_date) as latest_order,
    ROUND(AVG(quantity), 2) as avg_quantity,
    MIN(price) as min_price,
    MAX(price) as max_price,
    COUNT(DISTINCT country) as countries
FROM customer_orders;

-- Check data quality issues
SELECT 
    'Missing Emails' as issue,
    COUNT(*) as count
FROM customer_orders
WHERE email IS NULL OR email = ''
UNION ALL
SELECT 
    'Invalid Emails',
    COUNT(*)
FROM customer_orders
WHERE email NOT LIKE '%@%.%'
UNION ALL
SELECT 
    'Missing Product Names',
    COUNT(*)
FROM customer_orders
WHERE product_name IS NULL;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 SQL Tip:</strong><br>
                    Always start with data inspection before cleaning. Understanding your data structure, 
                    data types, and basic statistics helps you identify what needs to be cleaned.
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ Best Practice:</strong><br>
                    • Document original data structure<br>
                    • Identify primary and foreign keys<br>
                    • Check for data type mismatches<br>
                    • Note which columns allow NULLs<br>
                    • Look for obvious quality issues
                </div>
                """, unsafe_allow_html=True)

            with col_result:
                st.markdown("**Table Structure**")

                # Simulate DESCRIBE output
                structure_data = {
                    'Column': self.df.columns.tolist(),
                    'Type': [str(dtype) for dtype in self.df.dtypes],
                    'Null': ['YES' if self.df[col].isnull().any() else 'NO' for col in self.df.columns]
                }
                structure_df = pd.DataFrame(structure_data)
                st.dataframe(structure_df, hide_index=True,
                             width='stretch')

                st.markdown("**Data Preview (LIMIT 5)**")
                st.dataframe(self.df.head(5), width='stretch')

                st.markdown("**Basic Statistics**")
                col1, col2 = st.columns(2)
                col1.metric("Total Records", len(self.df))
                col2.metric("Total Columns", len(self.df.columns))
                col1.metric("Unique Orders", self.df['order_id'].nunique())
                col2.metric("Duplicates", self.df.duplicated(
                    subset=['order_id']).sum())
                col1.metric("Unique Customers",
                            self.df['customer_name'].nunique())
                col2.metric("Countries", self.df['country'].nunique())

        st.divider()

    def step_2_duplicates(self):
        """Step 2: Handle Duplicates"""
        with st.container():
            st.markdown(
                "<h3 style='color: #1976d2; margin: 0.3rem 0;'>🔍 Step 2 – Identify and Remove Duplicates</h3>",
                unsafe_allow_html=True
            )

            st.caption(
                "Find and eliminate duplicate records to maintain data integrity")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- Check for complete duplicate rows
SELECT 
    order_id, customer_name, product_name, order_date,
    COUNT(*) as occurrence_count
FROM customer_orders
GROUP BY order_id, customer_name, product_name, order_date
HAVING COUNT(*) > 1;

-- Find duplicates based on order_id
SELECT order_id, COUNT(*) as count
FROM customer_orders
GROUP BY order_id
HAVING COUNT(*) > 1;

-- Find semantic duplicates (same customer, product, date)
SELECT 
    customer_name,
    product_name,
    order_date,
    COUNT(*) as duplicate_count,
    STRING_AGG(order_id::TEXT, ', ') as order_ids
FROM customer_orders
GROUP BY customer_name, product_name, order_date
HAVING COUNT(*) > 1;

-- Remove duplicates using ROW_NUMBER (PostgreSQL)
WITH ranked_orders AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY order_id 
            ORDER BY 
                CASE WHEN email IS NOT NULL THEN 0 ELSE 1 END,
                order_date DESC
        ) as row_num
    FROM customer_orders
)
DELETE FROM customer_orders
WHERE order_id IN (
    SELECT order_id 
    FROM ranked_orders 
    WHERE row_num > 1
);

-- Alternative: Create clean table keeping most recent
CREATE TABLE customer_orders_clean AS
WITH ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY customer_name, product_name, order_date 
            ORDER BY 
                CASE WHEN email IS NOT NULL THEN 0 ELSE 1 END,
                order_id
        ) as rn
    FROM customer_orders
)
SELECT 
    order_id, customer_name, email, order_date,
    product_name, quantity, price, country, 
    order_status, notes
FROM ranked WHERE rn = 1;

-- MySQL approach
CREATE TEMPORARY TABLE temp_orders AS
SELECT DISTINCT * FROM customer_orders;

DELETE FROM customer_orders;
INSERT INTO customer_orders 
SELECT * FROM temp_orders;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ Deduplication Strategy:</strong><br>
                    • <b>Exact Duplicates:</b> Identical in all columns<br>
                    • <b>Semantic Duplicates:</b> Same customer, product, date<br>
                    • <b>Keep Most Complete:</b> Prioritize rows with non-null email<br>
                    • Always backup data before deleting duplicates
                </div>
                """, unsafe_allow_html=True)

            with col_result:
                st.markdown("**Duplicate Analysis**")

                total_rows = len(self.df)

                # Check for exact duplicates on order_id
                exact_duplicates = self.df.duplicated(
                    subset=['order_id']).sum()

                # Check for semantic duplicates
                semantic_dup = self.df.groupby(
                    ['customer_name', 'product_name', 'order_date']).size()
                semantic_duplicates = (semantic_dup > 1).sum()

                col1, col2 = st.columns(2)
                col1.metric("Total Rows", total_rows)
                col2.metric("Exact Duplicates (order_id)", exact_duplicates)
                col1.metric("Semantic Duplicates", semantic_duplicates)

                if semantic_duplicates > 0:
                    st.warning(
                        f"⚠️ Found {semantic_duplicates} groups with duplicate orders")

                    # Show duplicate rows
                    dup_groups = self.df.groupby(
                        ['customer_name', 'product_name', 'order_date']).filter(lambda x: len(x) > 1)
                    dup_groups_display = dup_groups.sort_values(
                        ['customer_name', 'product_name', 'order_date'])

                    st.markdown("**Duplicate Records:**")
                    st.dataframe(dup_groups_display[['order_id', 'customer_name', 'product_name', 'order_date', 'email']],
                                 width='stretch')

                    # Simulate removal - keep first occurrence with email preference
                    self.df = self.df.sort_values('email', na_position='last')
                    self.df = self.df.drop_duplicates(
                        subset=['customer_name', 'product_name', 'order_date'], keep='first')

                    st.success(
                        f"✅ After removal: {len(self.df)} rows remaining")
                else:
                    st.success("✅ No semantic duplicates found")

                col2.metric("Final Row Count", len(self.df))

        st.divider()

    def step_3_missing_values(self):
        """Step 3: Handle Missing Values"""
        with st.container():
            st.markdown(
                "<h3 style='color: #1976d2; margin: 0.3rem 0;'>❓ Step 3 – Handle Missing (NULL) Values</h3>",
                unsafe_allow_html=True
            )

            st.caption(
                "Identify and handle NULL values with appropriate strategies")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- Count NULL values per column
SELECT 
    COUNT(*) - COUNT(customer_name) as missing_customer,
    COUNT(*) - COUNT(email) as missing_email,
    COUNT(*) - COUNT(order_date) as missing_order_date,
    COUNT(*) - COUNT(product_name) as missing_product,
    COUNT(*) - COUNT(quantity) as missing_quantity,
    COUNT(*) - COUNT(price) as missing_price,
    COUNT(*) - COUNT(country) as missing_country
FROM customer_orders;

-- Find rows with any NULL values in critical fields
SELECT * FROM customer_orders
WHERE customer_name IS NULL
   OR email IS NULL
   OR product_name IS NULL
   OR price IS NULL;

-- Strategy 1: Delete rows with NULLs in critical fields
DELETE FROM customer_orders
WHERE email IS NULL 
   OR order_id IS NULL
   OR product_name IS NULL;

-- Strategy 2: Fill with default values
UPDATE customer_orders 
SET notes = 'No notes' 
WHERE notes IS NULL;

UPDATE customer_orders
SET customer_name = 'Unknown Customer'
WHERE customer_name IS NULL;

-- Strategy 3: Fill quantity with 1 (reasonable default)
UPDATE customer_orders
SET quantity = 1
WHERE quantity IS NULL;

-- Strategy 4: Use COALESCE for inline replacement
SELECT 
    order_id,
    COALESCE(customer_name, 'Unknown') as customer_name,
    COALESCE(email, 'noemail@example.com') as email,
    COALESCE(quantity, 1) as quantity,
    COALESCE(price, 0) as price,
    COALESCE(notes, 'No notes') as notes
FROM customer_orders;

-- Strategy 5: Fill missing price from same product
UPDATE customer_orders o1
SET price = (
    SELECT AVG(price)
    FROM customer_orders o2
    WHERE o2.product_name = o1.product_name
      AND o2.price IS NOT NULL
)
WHERE o1.price IS NULL;

-- Strategy 6: Mark incomplete records
ALTER TABLE customer_orders 
ADD COLUMN data_quality VARCHAR(20);

UPDATE customer_orders
SET data_quality = CASE
    WHEN email IS NULL OR product_name IS NULL THEN 'Incomplete'
    WHEN price IS NULL OR quantity IS NULL THEN 'Missing Values'
    ELSE 'Complete'
END;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 NULL Handling Strategies:</strong><br>
                    • <b>Delete:</b> For critical fields (email, product, price)<br>
                    • <b>Default Value:</b> For optional fields (notes)<br>
                    • <b>Infer from Data:</b> Average price for same product<br>
                    • <b>Flag Incomplete:</b> Add data_quality column<br>
                    • <b>Leave NULL:</b> When absence is meaningful
                </div>
                """, unsafe_allow_html=True)

            with col_result:
                st.markdown("**Missing Values Analysis**")

                missing_counts = self.df.isnull().sum()
                missing_pct = (missing_counts / len(self.df) * 100).round(2)

                missing_df = pd.DataFrame({
                    'Column': missing_counts.index,
                    'Missing': missing_counts.values,
                    'Percentage': missing_pct.values
                })
                missing_df = missing_df[missing_df['Missing'] > 0].sort_values(
                    'Missing', ascending=False)

                if not missing_df.empty:
                    st.dataframe(missing_df, hide_index=True,
                                 width='stretch')

                    # Apply cleaning
                    st.markdown("**Cleaning Strategy Applied:**")

                    # Fill quantity with 1
                    if 'quantity' in self.df.columns and self.df['quantity'].isnull().any():
                        self.df['quantity'].fillna(1, inplace=True)
                        st.info("• quantity: Filled with default (1)")

                    # Fill price with average for same product
                    if 'price' in self.df.columns:
                        # Convert price to numeric, coerce errors to NaN
                        self.df['price'] = pd.to_numeric(
                            self.df['price'], errors='coerce')

                        if self.df['price'].isnull().any():
                            for product in self.df['product_name'].unique():
                                if pd.notna(product):
                                    avg_price = self.df[self.df['product_name'] == product]['price'].mean(
                                    )
                                    self.df.loc[(self.df['product_name'] == product) &
                                                (self.df['price'].isnull()), 'price'] = avg_price
                            st.info("• price: Filled with product average")

                    # Fill categorical with defaults
                    if 'customer_name' in self.df.columns and self.df['customer_name'].isnull().any():
                        self.df['customer_name'].fillna(
                            'Unknown Customer', inplace=True)
                        st.info("• customer_name: Filled with 'Unknown Customer'")

                    if 'notes' in self.df.columns and self.df['notes'].isnull().any():
                        self.df['notes'].fillna('No notes', inplace=True)
                        st.info("• notes: Filled with 'No notes'")

                    st.success("✅ Missing values handled")
                else:
                    st.success("✅ No missing values found")

        st.divider()

    def step_4_text_cleaning(self):
        """Step 4: Text Data Standardization"""
        with st.container():
            st.markdown(
                "<h3 style='color: #1976d2; margin: 0.3rem 0;'>✏️ Step 4 – Text Data Standardization</h3>",
                unsafe_allow_html=True
            )

            st.caption("Clean and standardize text fields for consistency")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- Remove leading/trailing whitespace
UPDATE customer_orders
SET customer_name = TRIM(customer_name),
    product_name = TRIM(product_name),
    country = TRIM(country),
    order_status = TRIM(order_status);

-- Standardize customer names (Title Case)
UPDATE customer_orders
SET customer_name = INITCAP(TRIM(customer_name));

-- Standardize product names (Title Case)
UPDATE customer_orders
SET product_name = INITCAP(TRIM(product_name));

-- Convert email to lowercase
UPDATE customer_orders
SET email = LOWER(TRIM(email));

-- Standardize country names
UPDATE customer_orders
SET country = CASE
    WHEN UPPER(country) IN ('USA', 'US', 'UNITED STATES') 
        THEN 'United States'
    WHEN UPPER(country) = 'UK' 
        THEN 'United Kingdom'
    WHEN UPPER(country) = 'INDIA' 
        THEN 'India'
    WHEN UPPER(country) = 'CANADA' 
        THEN 'Canada'
    WHEN UPPER(country) = 'SPAIN' 
        THEN 'Spain'
    ELSE INITCAP(TRIM(country))
END;

-- Standardize order status (Capitalize first letter)
UPDATE customer_orders
SET order_status = CASE
    WHEN LOWER(order_status) = 'delivered' THEN 'Delivered'
    WHEN LOWER(order_status) = 'shipped' THEN 'Shipped'
    WHEN LOWER(order_status) = 'pending' THEN 'Pending'
    WHEN LOWER(order_status) = 'returned' THEN 'Returned'
    WHEN LOWER(order_status) = 'refunded' THEN 'Refunded'
    ELSE INITCAP(order_status)
END;

-- Fix common typos in product names
UPDATE customer_orders
SET product_name = REPLACE(product_name, 'Iphone', 'iPhone');

UPDATE customer_orders
SET product_name = REPLACE(product_name, 'Macbook', 'MacBook');

-- Remove extra internal spaces (PostgreSQL)
UPDATE customer_orders
SET customer_name = REGEXP_REPLACE(
    TRIM(customer_name), 
    '\\s+', 
    ' ', 
    'g'
);

-- Clean email addresses (remove invalid characters)
UPDATE customer_orders
SET email = LOWER(REGEXP_REPLACE(email, '[^a-zA-Z0-9@._-]', '', 'g'))
WHERE email IS NOT NULL;

-- Standardize quantity text to numbers
UPDATE customer_orders
SET quantity = CASE
    WHEN LOWER(quantity::TEXT) = 'one' THEN 1
    WHEN LOWER(quantity::TEXT) = 'two' THEN 2
    WHEN LOWER(quantity::TEXT) = 'three' THEN 3
    ELSE quantity
END;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ Text Cleaning Best Practices:</strong><br>
                    • Use INITCAP() for names (proper case)<br>
                    • Use LOWER() for emails/usernames<br>
                    • Use CASE for standardizing categories<br>
                    • Always TRIM() before other operations<br>
                    • Create lookup tables for standard values
                </div>
                """, unsafe_allow_html=True)

            with col_result:
                st.markdown("**Text Cleaning Examples**")

                # Show before/after
                before_df = self.df[[
                    'customer_name', 'product_name', 'country', 'order_status']].head(5).copy()
                st.markdown("**Before:**")
                st.dataframe(before_df, width='stretch')

                # Apply cleaning (simulate SQL operations)
                self.df['customer_name'] = self.df['customer_name'].astype(
                    str).str.strip().str.title()
                self.df['product_name'] = self.df['product_name'].astype(
                    str).str.strip().str.title()
                self.df['product_name'] = self.df['product_name'].str.replace(
                    'Iphone', 'iPhone', case=False)
                self.df['product_name'] = self.df['product_name'].str.replace(
                    'Macbook', 'MacBook', case=False)

                self.df['email'] = self.df['email'].astype(
                    str).str.lower().str.strip()

                # Standardize country
                country_map = {
                    'USA': 'United States',
                    'US': 'United States',
                    'UK': 'United Kingdom',
                    'INDIA': 'India',
                    'CANADA': 'Canada',
                    'SPAIN': 'Spain'
                }
                self.df['country'] = self.df['country'].str.upper().map(
                    lambda x: country_map.get(x, x.title() if isinstance(x, str) else x))

                # Standardize status
                self.df['order_status'] = self.df['order_status'].str.strip(
                ).str.capitalize()

                # Convert text numbers to integers
                text_to_num = {'one': 1, 'two': 2,
                               'three': 3, 'four': 4, 'five': 5}
                self.df['quantity'] = self.df['quantity'].apply(
                    lambda x: text_to_num.get(
                        str(x).lower(), x) if pd.notna(x) else x
                )

                after_df = self.df[[
                    'customer_name', 'product_name', 'country', 'order_status']].head(5)
                st.markdown("**After:**")
                st.dataframe(after_df, width='stretch')

                st.success("✅ Text standardization complete")

        st.divider()

    def step_5_data_types(self):
        """Step 5: Data Type Conversion"""
        with st.container():
            st.markdown(
                "<h3 style='color: #1976d2; margin: 0.3rem 0;'>🔄 Step 5 – Data Type Conversion & Formatting</h3>",
                unsafe_allow_html=True
            )

            st.caption(
                "Convert columns to appropriate data types and clean formatting")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- Check current data types
SELECT 
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'customer_orders';

-- Convert quantity to integer
ALTER TABLE customer_orders
ALTER COLUMN quantity TYPE INTEGER 
    USING quantity::INTEGER;

-- Clean and convert price (remove $ and , )
UPDATE customer_orders
SET price = REPLACE(REPLACE(price::TEXT, '$', ''), ',', '');

ALTER TABLE customer_orders
ALTER COLUMN price TYPE DECIMAL(10,2)
    USING price::DECIMAL(10,2);

-- Convert order_date to proper DATE type
-- Handle multiple date formats
UPDATE customer_orders
SET order_date = CASE
    -- Format: YYYY-MM-DD
    WHEN order_date LIKE '____-__-__' 
        THEN TO_DATE(order_date, 'YYYY-MM-DD')
    -- Format: MM/DD/YYYY
    WHEN order_date LIKE '__/__/____' 
        THEN TO_DATE(order_date, 'MM/DD/YYYY')
    -- Format: YYYY/MM/DD
    WHEN order_date LIKE '____/__/__' 
        THEN TO_DATE(order_date, 'YYYY/MM/DD')
    ELSE NULL
END::TEXT;

ALTER TABLE customer_orders
ALTER COLUMN order_date TYPE DATE
    USING order_date::DATE;

-- MySQL approach for date conversion
ALTER TABLE customer_orders
MODIFY COLUMN quantity INT,
MODIFY COLUMN price DECIMAL(10,2),
MODIFY COLUMN order_date DATE;

-- Create computed columns
ALTER TABLE customer_orders
ADD COLUMN total_amount DECIMAL(10,2);

UPDATE customer_orders
SET total_amount = quantity * price;

-- Extract year and month for analysis
ALTER TABLE customer_orders
ADD COLUMN order_year INTEGER,
ADD COLUMN order_month INTEGER;

UPDATE customer_orders
SET order_year = EXTRACT(YEAR FROM order_date),
    order_month = EXTRACT(MONTH FROM order_date);

-- Create boolean columns
ALTER TABLE customer_orders
ADD COLUMN is_delivered BOOLEAN,
ADD COLUMN is_returned BOOLEAN;

UPDATE customer_orders
SET is_delivered = (order_status = 'Delivered'),
    is_returned = (order_status IN ('Returned', 'Refunded'));""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='warning-box'>
                    <strong>⚠️ Important:</strong><br>
                    • Clean data before type conversion (remove $, commas)<br>
                    • Handle multiple date formats carefully<br>
                    • Failed conversions may result in NULL values<br>
                    • Always test on a subset first
                </div>
                """, unsafe_allow_html=True)

            with col_result:
                st.markdown("**Data Type Conversion**")

                st.markdown("**Before:**")
                types_before = pd.DataFrame({
                    'Column': ['quantity', 'price', 'order_date'],
                    'Type': ['object', 'object', 'object']
                })
                st.dataframe(types_before, hide_index=True,
                             width='stretch')

                # Simulate conversion
                # Clean and convert quantity
                self.df['quantity'] = pd.to_numeric(
                    self.df['quantity'], errors='coerce').fillna(1).astype(int)

                # Clean and convert price
                if self.df['price'].dtype == 'object':
                    self.df['price'] = self.df['price'].astype(
                        str).str.replace('$', '').str.replace(',', '')
                self.df['price'] = pd.to_numeric(
                    self.df['price'], errors='coerce')

                # Convert date
                self.df['order_date'] = pd.to_datetime(
                    self.df['order_date'], errors='coerce')

                # Create computed columns
                self.df['total_amount'] = self.df['quantity'] * \
                    self.df['price']
                self.df['order_year'] = self.df['order_date'].dt.year
                self.df['order_month'] = self.df['order_date'].dt.month

                st.markdown("**After:**")
                types_after = pd.DataFrame({
                    'Column': ['quantity', 'price', 'order_date', 'total_amount'],
                    'Type': [str(self.df['quantity'].dtype), str(self.df['price'].dtype),
                             str(self.df['order_date'].dtype), str(self.df['total_amount'].dtype)]
                })
                st.dataframe(types_after, hide_index=True,
                             width='stretch')

                st.markdown("**Sample Values:**")
                sample_df = self.df[['quantity', 'price',
                                     'total_amount', 'order_date']].head(3)
                st.dataframe(sample_df, width='stretch')

                st.success("✅ Data types converted and formatted")

        st.divider()
        """Step 5: Data Type Conversion"""
        with st.container():
            st.markdown(
                "<h3 style='color: #1976d2; margin: 0.3rem 0;'>🔄 Step 5 – Data Type Conversion & Validation</h3>",
                unsafe_allow_html=True
            )

            st.caption(
                "Convert columns to appropriate data types and validate formats")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- Check current data types
SELECT 
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'customers';

-- Convert to appropriate types (PostgreSQL)
ALTER TABLE customers
ALTER COLUMN age TYPE INTEGER 
    USING age::INTEGER;

ALTER TABLE customers
ALTER COLUMN annual_salary TYPE DECIMAL(10,2)
    USING annual_salary::DECIMAL(10,2);

ALTER TABLE customers
ALTER COLUMN join_date TYPE DATE
    USING join_date::DATE;

-- MySQL approach
ALTER TABLE customers
MODIFY COLUMN age INT,
MODIFY COLUMN annual_salary DECIMAL(10,2),
MODIFY COLUMN join_date DATE;

-- Safe conversion with error handling (PostgreSQL)
ALTER TABLE customers
ALTER COLUMN age TYPE INTEGER
    USING CASE 
        WHEN age ~ '^[0-9]+$' THEN age::INTEGER
        ELSE NULL
    END;

-- Convert text to date with multiple formats
UPDATE customers
SET join_date = CASE
    WHEN join_date LIKE '____-__-__' 
        THEN TO_DATE(join_date, 'YYYY-MM-DD')
    WHEN join_date LIKE '__/__/____' 
        THEN TO_DATE(join_date, 'DD/MM/YYYY')
    WHEN join_date LIKE '____/__/__' 
        THEN TO_DATE(join_date, 'YYYY/MM/DD')
    ELSE NULL
END;

-- Create computed boolean column
ALTER TABLE customers
ADD COLUMN is_active BOOLEAN;

UPDATE customers
SET is_active = CASE
    WHEN LOWER(status) = 'active' THEN TRUE
    ELSE FALSE
END;

-- Extract year from date
ALTER TABLE customers
ADD COLUMN join_year INTEGER;

UPDATE customers
SET join_year = EXTRACT(YEAR FROM join_date);""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='warning-box'>
                    <strong>⚠️ Warning:</strong><br>
                    Always backup data before type conversion. Failed conversions 
                    may result in NULL values or errors. Test on a small subset first.
                </div>
                """, unsafe_allow_html=True)

            with col_result:
                st.markdown("**Data Type Conversion**")

                st.markdown("**Before:**")
                types_before = pd.DataFrame({
                    'Column': ['age', 'annual_salary', 'join_date'],
                    'Type': ['object', 'int64', 'object']
                })
                st.dataframe(types_before, hide_index=True, width='stretch')

                # Simulate conversion
                if 'age' in self.df.columns:
                    self.df['age'] = pd.to_numeric(
                        self.df['age'], errors='coerce').astype('Int64')

                if 'annual_salary' in self.df.columns:
                    self.df['annual_salary'] = pd.to_numeric(
                        self.df['annual_salary'], errors='coerce')

                if 'join_date' in self.df.columns:
                    self.df['join_date'] = pd.to_datetime(
                        self.df['join_date'], errors='coerce')

                st.markdown("**After:**")
                columns = []
                types = []

                for col in ['age', 'annual_salary', 'join_date']:
                    if col in self.df.columns:
                        columns.append(col)
                        types.append(str(self.df[col].dtype))

                types_after = pd.DataFrame({
                    'Column': columns,
                    'Type': types
                })
                st.dataframe(types_after, hide_index=True,
                             width='stretch')

                st.success("✅ Data types converted successfully")

        st.divider()

    def step_6_outliers(self):
        """Step 6: Outlier Detection and Handling"""
        with st.container():
            st.markdown(
                "<h3 style='color: #1976d2; margin: 0.3rem 0;'>📊 Step 6 – Outlier Detection & Handling</h3>",
                unsafe_allow_html=True
            )

            st.caption(
                "Identify and handle outliers in price and quantity using statistical methods")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- Calculate IQR and identify price outliers
WITH stats AS (
    SELECT 
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price) as q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) as q3
    FROM customer_orders
),
bounds AS (
    SELECT 
        q1,
        q3,
        q3 - q1 as iqr,
        q1 - 1.5 * (q3 - q1) as lower_bound,
        q3 + 1.5 * (q3 - q1) as upper_bound
    FROM stats
)
SELECT 
    o.*,
    b.lower_bound,
    b.upper_bound,
    CASE 
        WHEN o.price < b.lower_bound OR o.price > b.upper_bound 
        THEN 'Outlier'
        ELSE 'Normal'
    END as outlier_flag
FROM customer_orders o
CROSS JOIN bounds b;

-- Remove price outliers using IQR
DELETE FROM customer_orders
WHERE price NOT BETWEEN 
    (SELECT PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price) 
     - 1.5 * (PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) 
            - PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price))
     FROM customer_orders)
AND
    (SELECT PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) 
     + 1.5 * (PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) 
            - PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price))
     FROM customer_orders);

-- Business rule approach (domain knowledge)
DELETE FROM customer_orders
WHERE price < 0 OR price > 10000;

DELETE FROM customer_orders
WHERE quantity < 1 OR quantity > 100;

-- Cap outliers instead of removing
UPDATE customer_orders
SET price = CASE
    WHEN price < 10 THEN 10
    WHEN price > 5000 THEN 5000
    ELSE price
END;

UPDATE customer_orders
SET quantity = CASE
    WHEN quantity < 1 THEN 1
    WHEN quantity > 50 THEN 50
    ELSE quantity
END;

-- Z-score approach for price
WITH stats AS (
    SELECT 
        AVG(price) as mean_price,
        STDDEV(price) as std_price
    FROM customer_orders
)
SELECT 
    order_id,
    price,
    (price - (SELECT mean_price FROM stats)) 
        / (SELECT std_price FROM stats) as z_score
FROM customer_orders
WHERE ABS((price - (SELECT mean_price FROM stats)) 
        / (SELECT std_price FROM stats)) > 3;

-- Flag outliers without removing
ALTER TABLE customer_orders
ADD COLUMN is_outlier BOOLEAN;

UPDATE customer_orders
SET is_outlier = (price < 0 OR price > 5000 OR quantity > 50);""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 Outlier Detection Methods:</strong><br>
                    • <b>IQR Method:</b> Q1 - 1.5×IQR to Q3 + 1.5×IQR<br>
                    • <b>Z-Score:</b> Remove values with |z| > 3<br>
                    • <b>Business Rules:</b> Price > 0 and < 10000<br>
                    • <b>Percentile:</b> Remove top/bottom X%
                </div>
                """, unsafe_allow_html=True)

            with col_result:
                st.markdown("**Outlier Analysis - Price**")

                if 'price' in self.df.columns:
                    Q1 = self.df['price'].quantile(0.25)
                    Q3 = self.df['price'].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR

                    col1, col2 = st.columns(2)
                    col1.metric("Q1", f"${Q1:.2f}")
                    col2.metric("Q3", f"${Q3:.2f}")
                    col1.metric("IQR", f"${IQR:.2f}")

                    outliers = self.df[(self.df['price'] < lower_bound) | (
                        self.df['price'] > upper_bound)]
                    col2.metric("Outliers", len(outliers))

                    st.markdown(
                        f"**Valid Range:** ${lower_bound:.2f} to ${upper_bound:.2f}")

                    # Show outliers
                    if not outliers.empty:
                        st.markdown("**Outlier Records:**")
                        st.dataframe(outliers[['order_id', 'customer_name', 'product_name', 'price', 'quantity']],
                                     width='stretch')

                        # Business rule: remove negative prices and unreasonable values
                        self.df = self.df[(self.df['price'] >= 0) & (
                            self.df['price'] <= 5000)]
                        self.df = self.df[(self.df['quantity'] >= 1) & (
                            self.df['quantity'] <= 50)]

                        st.success(
                            f"✅ Removed {len(outliers)} outliers using business rules")
                    else:
                        st.success("✅ No outliers detected")

        st.divider()
        """Step 6: Outlier Detection and Handling"""
        with st.container():
            st.markdown(
                "<h3 style='color: #1976d2; margin: 0.3rem 0;'>📊 Step 6 – Outlier Detection & Handling</h3>",
                unsafe_allow_html=True
            )

            st.caption(
                "Identify and handle outliers using statistical methods and business rules")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- Calculate IQR and identify outliers
WITH stats AS (
    SELECT 
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY age) as q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY age) as q3
    FROM customers
),
bounds AS (
    SELECT 
        q1,
        q3,
        q3 - q1 as iqr,
        q1 - 1.5 * (q3 - q1) as lower_bound,
        q3 + 1.5 * (q3 - q1) as upper_bound
    FROM stats
)
SELECT 
    c.*,
    b.lower_bound,
    b.upper_bound,
    CASE 
        WHEN c.age < b.lower_bound OR c.age > b.upper_bound 
        THEN 'Outlier'
        ELSE 'Normal'
    END as outlier_flag
FROM customers c
CROSS JOIN bounds b;

-- Remove outliers using IQR
DELETE FROM customers
WHERE age NOT BETWEEN 
    (SELECT PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY age) 
     - 1.5 * (PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY age) 
            - PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY age))
     FROM customers)
AND
    (SELECT PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY age) 
     + 1.5 * (PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY age) 
            - PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY age))
     FROM customers);

-- Business rule approach (domain knowledge)
DELETE FROM customers
WHERE age < 18 OR age > 100;

DELETE FROM customers
WHERE annual_salary < 0 OR annual_salary > 1000000;

-- Cap outliers instead of removing
UPDATE customers
SET age = CASE
    WHEN age < 18 THEN 18
    WHEN age > 65 THEN 65
    ELSE age
END;

UPDATE customers
SET annual_salary = CASE
    WHEN annual_salary < 20000 THEN 20000
    WHEN annual_salary > 500000 THEN 500000
    ELSE annual_salary
END;

-- Z-score approach (requires standard deviation)
WITH stats AS (
    SELECT 
        AVG(age) as mean_age,
        STDDEV(age) as std_age
    FROM customers
)
DELETE FROM customers
WHERE ABS((age - (SELECT mean_age FROM stats)) 
        / (SELECT std_age FROM stats)) > 3;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 Outlier Detection Methods:</strong><br>
                    • <b>IQR Method:</b> Q1 - 1.5×IQR to Q3 + 1.5×IQR<br>
                    • <b>Z-Score:</b> Remove values with |z| > 3<br>
                    • <b>Business Rules:</b> Domain-specific constraints<br>
                    • <b>Percentile:</b> Remove top/bottom X%
                </div>
                """, unsafe_allow_html=True)

            with col_result:
                st.markdown("**Outlier Analysis - Age**")

                if 'age' in self.df.columns:
                    Q1 = self.df['age'].quantile(0.25)
                    Q3 = self.df['age'].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR

                    col1, col2 = st.columns(2)
                    col1.metric("Q1", f"{Q1:.0f}")
                    col2.metric("Q3", f"{Q3:.0f}")
                    col1.metric("IQR", f"{IQR:.0f}")
                    col2.metric("Outliers", len(self.df[(self.df['age'] < lower_bound) |
                                                        (self.df['age'] > upper_bound)]))

                    st.markdown(
                        "**Range:** {:.0f} to {:.0f}".format(lower_bound, upper_bound))

                    # Show outliers
                    outliers = self.df[(self.df['age'] < lower_bound) | (
                        self.df['age'] > upper_bound)]
                    if not outliers.empty:
                        st.markdown("**Outlier Records:**")
                        st.dataframe(outliers[['customer_id', 'first_name', 'age']],
                                     width='stretch')

                        # Remove outliers
                        self.df = self.df[(self.df['age'] >= lower_bound) &
                                          (self.df['age'] <= upper_bound)]
                        st.success(f"✅ Removed {len(outliers)} outliers")
                    else:
                        st.success("✅ No outliers detected")

        st.divider()

    def step_7_validation(self):
        """Step 7: Data Validation with Constraints"""
        with st.container():
            st.markdown(
                "<h3 style='color: #1976d2; margin: 0.3rem 0;'>✅ Step 7 – Data Validation & Constraints</h3>",
                unsafe_allow_html=True
            )

            st.caption(
                "Validate data against business rules and add database constraints")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- Email validation (PostgreSQL regex)
SELECT 
    order_id,
    email,
    CASE 
        WHEN email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'
        THEN 'Valid'
        ELSE 'Invalid'
    END as email_status
FROM customer_orders
WHERE email IS NOT NULL;

-- Price validation
SELECT 
    order_id,
    price,
    CASE 
        WHEN price > 0 AND price < 10000 THEN 'Valid'
        ELSE 'Invalid'
    END as price_status
FROM customer_orders;

-- Quantity validation
SELECT 
    order_id,
    quantity,
    CASE 
        WHEN quantity >= 1 AND quantity <= 100 THEN 'Valid'
        ELSE 'Invalid'
    END as quantity_status
FROM customer_orders;

-- Date validation (not in future)
SELECT 
    order_id,
    order_date,
    CASE 
        WHEN order_date <= CURRENT_DATE THEN 'Valid'
        ELSE 'Invalid (Future Date)'
    END as date_status
FROM customer_orders;

-- Product name validation
SELECT 
    order_id,
    product_name,
    CASE 
        WHEN product_name IS NOT NULL 
        AND LENGTH(product_name) > 0 
        THEN 'Valid'
        ELSE 'Invalid'
    END as product_status
FROM customer_orders;

-- Add CHECK constraints
ALTER TABLE customer_orders
ADD CONSTRAINT check_price 
    CHECK (price > 0 AND price < 10000);

ALTER TABLE customer_orders
ADD CONSTRAINT check_quantity 
    CHECK (quantity >= 1 AND quantity <= 100);

ALTER TABLE customer_orders
ADD CONSTRAINT check_email 
    CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$');

ALTER TABLE customer_orders
ADD CONSTRAINT check_order_date 
    CHECK (order_date <= CURRENT_DATE);

ALTER TABLE customer_orders
ADD CONSTRAINT check_total_amount
    CHECK (total_amount > 0);

-- Add NOT NULL constraints
ALTER TABLE customer_orders
ALTER COLUMN order_id SET NOT NULL,
ALTER COLUMN customer_name SET NOT NULL,
ALTER COLUMN email SET NOT NULL,
ALTER COLUMN product_name SET NOT NULL;

-- Add UNIQUE constraint
ALTER TABLE customer_orders
ADD CONSTRAINT unique_order_id 
    UNIQUE (order_id);

-- Add PRIMARY KEY
ALTER TABLE customer_orders
ADD PRIMARY KEY (order_id);

-- Validation summary report
SELECT 
    'Email Validation' as check_type,
    COUNT(*) as total,
    SUM(CASE WHEN email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$' 
        THEN 1 ELSE 0 END) as valid,
    SUM(CASE WHEN email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$' 
        OR email IS NULL THEN 1 ELSE 0 END) as invalid
FROM customer_orders
UNION ALL
SELECT 
    'Price Validation',
    COUNT(*),
    SUM(CASE WHEN price > 0 AND price < 10000 THEN 1 ELSE 0 END),
    SUM(CASE WHEN price <= 0 OR price >= 10000 OR price IS NULL 
        THEN 1 ELSE 0 END)
FROM customer_orders
UNION ALL
SELECT 
    'Quantity Validation',
    COUNT(*),
    SUM(CASE WHEN quantity >= 1 AND quantity <= 100 THEN 1 ELSE 0 END),
    SUM(CASE WHEN quantity < 1 OR quantity > 100 OR quantity IS NULL 
        THEN 1 ELSE 0 END)
FROM customer_orders;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ Constraint Best Practices:</strong><br>
                    • Add constraints AFTER cleaning data<br>
                    • Use NOT NULL for required fields<br>
                    • Use CHECK for business rules<br>
                    • Use UNIQUE for unique identifiers<br>
                    • Document all validation rules
                </div>
                """, unsafe_allow_html=True)

            with col_result:
                st.markdown("**Validation Report**")

                # Email validation
                import re
                email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
                valid_emails = self.df['email'].astype(str).apply(
                    lambda x: bool(re.match(email_pattern, x)
                                   ) if x != 'nan' else False
                ).sum()

                # Price validation
                valid_prices = ((self.df['price'] > 0) & (
                    self.df['price'] < 10000)).sum()

                # Quantity validation
                valid_quantities = ((self.df['quantity'] >= 1) & (
                    self.df['quantity'] <= 100)).sum()

                # Date validation
                today = pd.Timestamp.now()
                valid_dates = (self.df['order_date'] <= today).sum()

                validation_df = pd.DataFrame({
                    'Validation': ['Email Format', 'Price Range (0-10000)', 'Quantity (1-100)', 'Date Not Future'],
                    'Valid': [valid_emails, valid_prices, valid_quantities, valid_dates],
                    'Invalid': [
                        len(self.df) - valid_emails,
                        len(self.df) - valid_prices,
                        len(self.df) - valid_quantities,
                        len(self.df) - valid_dates
                    ]
                })

                st.dataframe(validation_df, hide_index=True,
                             width='stretch')

                # Overall validation
                all_valid = (
                    (valid_emails == len(self.df)) and
                    (valid_prices == len(self.df)) and
                    (valid_quantities == len(self.df)) and
                    (valid_dates == len(self.df))
                )

                if all_valid:
                    st.success("✅ All records passed validation!")
                else:
                    total_invalid = (len(self.df) - valid_emails + len(self.df) - valid_prices +
                                     len(self.df) - valid_quantities + len(self.df) - valid_dates)
                    st.warning(
                        f"⚠️ Found validation issues - review data quality")

        st.divider()
        """Step 7: Data Validation with Constraints"""
        with st.container():
            st.markdown(
                "<h3 style='color: #1976d2; margin: 0.3rem 0;'>✅ Step 7 – Data Validation & Constraints</h3>",
                unsafe_allow_html=True
            )

            st.caption(
                "Validate data against business rules and add database constraints")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- Email validation (PostgreSQL regex)
SELECT 
    customer_id,
    email_address,
    CASE 
        WHEN email_address ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'
        THEN 'Valid'
        ELSE 'Invalid'
    END as email_status
FROM customers;

-- Phone validation (exactly 10 digits)
SELECT 
    customer_id,
    phone_number,
    CASE 
        WHEN LENGTH(phone_number) = 10 
        AND phone_number ~ '^[0-9]+$'
        THEN 'Valid'
        ELSE 'Invalid'
    END as phone_status
FROM customers;

-- Age validation
SELECT 
    customer_id,
    age,
    CASE 
        WHEN age BETWEEN 18 AND 100 THEN 'Valid'
        ELSE 'Invalid'
    END as age_status
FROM customers;

-- Date validation (not in future)
SELECT 
    customer_id,
    join_date,
    CASE 
        WHEN join_date <= CURRENT_DATE THEN 'Valid'
        ELSE 'Invalid'
    END as date_status
FROM customers;

-- Add CHECK constraints
ALTER TABLE customers
ADD CONSTRAINT check_age 
    CHECK (age BETWEEN 18 AND 100);

ALTER TABLE customers
ADD CONSTRAINT check_salary 
    CHECK (annual_salary > 0);

ALTER TABLE customers
ADD CONSTRAINT check_email 
    CHECK (email_address ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$');

ALTER TABLE customers
ADD CONSTRAINT check_join_date 
    CHECK (join_date <= CURRENT_DATE);

-- Add NOT NULL constraints
ALTER TABLE customers
ALTER COLUMN customer_id SET NOT NULL,
ALTER COLUMN email_address SET NOT NULL;

-- Add UNIQUE constraint
ALTER TABLE customers
ADD CONSTRAINT unique_email 
    UNIQUE (email_address);

-- Add PRIMARY KEY
ALTER TABLE customers
ADD PRIMARY KEY (customer_id);

-- Create validation report
SELECT 
    'Email' as validation_type,
    COUNT(*) as total,
    SUM(CASE WHEN email_address ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$' 
        THEN 1 ELSE 0 END) as valid_count,
    SUM(CASE WHEN email_address !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$' 
        THEN 1 ELSE 0 END) as invalid_count
FROM customers
UNION ALL
SELECT 
    'Age',
    COUNT(*),
    SUM(CASE WHEN age BETWEEN 18 AND 100 THEN 1 ELSE 0 END),
    SUM(CASE WHEN age NOT BETWEEN 18 AND 100 THEN 1 ELSE 0 END)
FROM customers;""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='best-practice'>
                    <strong>✅ Constraint Best Practices:</strong><br>
                    • Add constraints AFTER cleaning data<br>
                    • Use NOT NULL for required fields<br>
                    • Use CHECK for business rules<br>
                    • Use UNIQUE for unique identifiers<br>
                    • Document all constraints
                </div>
                """, unsafe_allow_html=True)

            with col_result:
                st.markdown("**Validation Report**")

                # Email validation
                import re
                email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

                # Email validation
                if 'email_address' in self.df.columns:
                    valid_emails = self.df['email_address'].astype(str).apply(
                        lambda x: bool(re.match(email_pattern, x))).sum()
                else:
                    valid_emails = 0

                # Age validation
                if 'age' in self.df.columns:
                    valid_ages = self.df['age'].between(18, 100).sum()
                else:
                    valid_ages = 0

                # Salary validation
                if 'annual_salary' in self.df.columns:
                    valid_salaries = (self.df['annual_salary'] > 0).sum()
                else:
                    valid_salaries = 0

                validation_df = pd.DataFrame({
                    'Validation': ['Email Format', 'Age Range (18-100)', 'Salary > 0'],
                    'Valid': [valid_emails, valid_ages, valid_salaries],
                    'Invalid': [
                        len(self.df) - valid_emails,
                        len(self.df) - valid_ages,
                        len(self.df) - valid_salaries
                    ]
                })

                st.dataframe(validation_df, hide_index=True, width='stretch')

                # Overall validation
                all_valid = (
                    (valid_emails == len(self.df)) and
                    (valid_ages == len(self.df)) and
                    (valid_salaries == len(self.df))
                )

                if all_valid:
                    st.success("✅ All records passed validation!")
                else:
                    st.warning("⚠️ Some records failed validation")

        st.divider()

    def step_8_export(self):
        """Step 8: Create Clean Table & Export"""
        with st.container():
            st.markdown(
                "<h3 style='color: #1976d2; margin: 0.3rem 0;'>💾 Step 8 – Create Clean Table & Export</h3>",
                unsafe_allow_html=True
            )

            st.caption(
                "Create production-ready clean table with proper structure")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- Create clean table with proper schema
CREATE TABLE customer_orders_clean (
    order_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(200) NOT NULL,
    email VARCHAR(255) NOT NULL 
        CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'),
    order_date DATE NOT NULL 
        CHECK (order_date <= CURRENT_DATE),
    product_name VARCHAR(200) NOT NULL,
    quantity INTEGER NOT NULL 
        CHECK (quantity >= 1 AND quantity <= 100),
    price DECIMAL(10,2) NOT NULL 
        CHECK (price > 0 AND price < 10000),
    country VARCHAR(100),
    order_status VARCHAR(50),
    notes TEXT,
    total_amount DECIMAL(10,2),
    order_year INTEGER,
    order_month INTEGER,
    is_delivered BOOLEAN,
    is_returned BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert cleaned data
INSERT INTO customer_orders_clean 
    (order_id, customer_name, email, order_date, 
     product_name, quantity, price, country, 
     order_status, notes, total_amount, order_year, 
     order_month, is_delivered, is_returned)
SELECT 
    order_id,
    INITCAP(TRIM(customer_name)),
    LOWER(TRIM(email)),
    order_date::DATE,
    INITCAP(TRIM(product_name)),
    quantity,
    price,
    INITCAP(TRIM(country)),
    INITCAP(TRIM(order_status)),
    COALESCE(notes, 'No notes'),
    quantity * price as total_amount,
    EXTRACT(YEAR FROM order_date),
    EXTRACT(MONTH FROM order_date),
    (order_status = 'Delivered') as is_delivered,
    (order_status IN ('Returned', 'Refunded')) as is_returned
FROM customer_orders
WHERE email IS NOT NULL
  AND product_name IS NOT NULL
  AND price > 0 AND price < 10000
  AND quantity >= 1;

-- Create indexes for performance
CREATE INDEX idx_customer_email 
    ON customer_orders_clean(email);
CREATE INDEX idx_order_date 
    ON customer_orders_clean(order_date);
CREATE INDEX idx_product_name 
    ON customer_orders_clean(product_name);
CREATE INDEX idx_order_status 
    ON customer_orders_clean(order_status);
CREATE INDEX idx_country 
    ON customer_orders_clean(country);

-- Export to CSV (PostgreSQL)
COPY customer_orders_clean 
TO '/tmp/customer_orders_clean.csv' 
WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',');

-- Create analytics views
CREATE VIEW monthly_sales AS
SELECT 
    order_year,
    order_month,
    COUNT(*) as total_orders,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_order_value
FROM customer_orders_clean
GROUP BY order_year, order_month
ORDER BY order_year, order_month;

CREATE VIEW product_performance AS
SELECT 
    product_name,
    COUNT(*) as total_orders,
    SUM(quantity) as total_quantity_sold,
    SUM(total_amount) as total_revenue,
    AVG(price) as avg_price
FROM customer_orders_clean
GROUP BY product_name
ORDER BY total_revenue DESC;

-- Create data quality report
CREATE VIEW data_quality_summary AS
SELECT 
    'Total Orders' as metric,
    COUNT(*)::TEXT as value
FROM customer_orders_clean
UNION ALL
SELECT 
    'Unique Customers',
    COUNT(DISTINCT customer_name)::TEXT
FROM customer_orders_clean
UNION ALL
SELECT 
    'Total Revenue',
    '$' || ROUND(SUM(total_amount), 2)::TEXT
FROM customer_orders_clean
UNION ALL
SELECT 
    'Avg Order Value',
    '$' || ROUND(AVG(total_amount), 2)::TEXT
FROM customer_orders_clean;

-- Add table documentation
COMMENT ON TABLE customer_orders_clean IS 
    'Cleaned customer orders data - validated and standardized';
COMMENT ON COLUMN customer_orders_clean.order_id IS 
    'Unique order identifier - Primary Key';
COMMENT ON COLUMN customer_orders_clean.email IS 
    'Customer email - validated format';
COMMENT ON COLUMN customer_orders_clean.total_amount IS 
    'Computed as quantity * price';""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 Production Best Practices:</strong><br>
                    • Create separate clean table (don't overwrite source)<br>
                    • Add appropriate indexes for query performance<br>
                    • Create analytical views for common queries<br>
                    • Document with table/column comments<br>
                    • Schedule regular data quality checks
                </div>
                """, unsafe_allow_html=True)

            with col_result:
                st.markdown("**Final Clean Dataset**")

                # Show final data sample
                st.dataframe(self.df.head(10), width='stretch')

                st.markdown("**Data Summary**")
                col1, col2 = st.columns(2)
                col1.metric("Total Orders", len(self.df))
                col2.metric("Unique Customers",
                            self.df['customer_name'].nunique())

                if 'total_amount' in self.df.columns:
                    total_revenue = self.df['total_amount'].sum()
                    avg_order = self.df['total_amount'].mean()
                    col1.metric("Total Revenue", f"${total_revenue:,.2f}")
                    col2.metric("Avg Order Value", f"${avg_order:.2f}")

                col1.metric("Products", self.df['product_name'].nunique())
                col2.metric("Countries", self.df['country'].nunique())

                # Download button
                csv_buffer = io.StringIO()
                self.df.to_csv(csv_buffer, index=False)
                csv_data = csv_buffer.getvalue()

                st.download_button(
                    label="📥 Download Clean Data (CSV)",
                    data=csv_data,
                    file_name="customer_orders_clean.csv",
                    mime="text/csv",
                    width='stretch'
                )

                st.success("✅ Clean dataset ready for production!")

        st.divider()
        """Step 8: Create Clean Table & Export"""
        with st.container():
            st.markdown(
                "<h3 style='color: #1976d2; margin: 0.3rem 0;'>💾 Step 8 – Create Clean Table & Export</h3>",
                unsafe_allow_html=True
            )

            st.caption(
                "Create production-ready clean table with proper structure")

            col_code, col_result = st.columns([5, 4], gap="medium")

            with col_code:
                st.code("""-- Create clean table with proper schema
CREATE TABLE customers_clean (
    customer_id INTEGER PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email_address VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(10),
    age INTEGER CHECK (age BETWEEN 18 AND 100),
    annual_salary DECIMAL(10,2) CHECK (annual_salary > 0),
    join_date DATE CHECK (join_date <= CURRENT_DATE),
    department VARCHAR(100),
    status VARCHAR(20),
    is_active BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert cleaned data
INSERT INTO customers_clean 
    (customer_id, first_name, last_name, email_address, 
     phone_number, age, annual_salary, join_date, 
     department, status, is_active)
SELECT 
    customer_id,
    INITCAP(TRIM(first_name)),
    INITCAP(TRIM(last_name)),
    LOWER(TRIM(email_address)),
    REGEXP_REPLACE(phone_number, '[^0-9]', '', 'g'),
    age,
    annual_salary,
    join_date::DATE,
    INITCAP(TRIM(department)),
    CASE WHEN LOWER(status) = 'active' THEN 'Active' ELSE 'Inactive' END,
    CASE WHEN LOWER(status) = 'active' THEN TRUE ELSE FALSE END
FROM customers
WHERE email_address IS NOT NULL
  AND age BETWEEN 18 AND 100
  AND annual_salary > 0;

-- Create indexes for performance
CREATE INDEX idx_email ON customers_clean(email_address);
CREATE INDEX idx_department ON customers_clean(department);
CREATE INDEX idx_join_date ON customers_clean(join_date);

-- Export to CSV (PostgreSQL)
COPY customers_clean 
TO '/tmp/customers_clean.csv' 
WITH (FORMAT CSV, HEADER TRUE);

-- Create data quality report
CREATE VIEW data_quality_report AS
SELECT 
    'Total Records' as metric,
    COUNT(*)::TEXT as value
FROM customers_clean
UNION ALL
SELECT 
    'Unique Customers',
    COUNT(DISTINCT customer_id)::TEXT
FROM customers_clean
UNION ALL
SELECT 
    'Avg Age',
    ROUND(AVG(age), 2)::TEXT
FROM customers_clean
UNION ALL
SELECT 
    'Avg Salary',
    ROUND(AVG(annual_salary), 2)::TEXT
FROM customers_clean;

-- Add table comments for documentation
COMMENT ON TABLE customers_clean IS 
    'Cleaned customer data - validated and standardized';
COMMENT ON COLUMN customers_clean.customer_id IS 
    'Unique customer identifier';
COMMENT ON COLUMN customers_clean.email_address IS 
    'Validated email address - required field';""", language="sql", line_numbers=True)

                st.markdown("""
                <div class='sql-tip'>
                    <strong>💡 Production Best Practices:</strong><br>
                    • Create separate clean table<br>
                    • Add appropriate indexes<br>
                    • Document with comments<br>
                    • Create data quality views<br>
                    • Schedule regular cleaning jobs
                </div>
                """, unsafe_allow_html=True)

            with col_result:
                st.markdown("**Final Clean Dataset**")

                # Show final data sample
                st.dataframe(self.df.head(10), width='stretch')

                st.markdown("**Data Summary**")
                col1, col2 = st.columns(2)
                col1.metric("Total Records", len(self.df))
                col2.metric("Total Columns", len(self.df.columns))
                col1.metric(
                    "Memory Usage", f"{self.df.memory_usage(deep=True).sum() / 1024:.2f} KB")
                col2.metric("Data Quality", "100%")

                # Download button
                csv_buffer = io.StringIO()
                self.df.to_csv(csv_buffer, index=False)
                csv_data = csv_buffer.getvalue()

                st.download_button(
                    label="📥 Download Clean Data (CSV)",
                    data=csv_data,
                    file_name="customers_clean.csv",
                    mime="text/csv",
                    width='stretch'
                )

                st.success("✅ Clean dataset ready for production!")

        st.divider()

    def output(self):
        self.step_1_inspect_data()
        self.step_2_duplicates()
        self.step_3_missing_values()
        self.step_4_text_cleaning()
        self.step_5_data_types()
        self.step_6_outliers()
        self.step_7_validation()
        self.step_8_export()

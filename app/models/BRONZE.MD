# 🏅 Medallion Architecture — Bronze Layer (Ingestion)

> **Layer:** Bronze (Raw Ingestion)  
> **Purpose:** Store raw, unvalidated data exactly as received from source systems. No transformations. Full audit trail.  
> **Conventions:**
>
> - All tables prefixed with `brz_`
> - `_ingested_at` — timestamp when the row landed in the lake
> - `_source_system` — origin system name
> - `_batch_id` — batch/pipeline run identifier
> - `_is_deleted` — soft delete flag for CDC support
> - Primary keys are surrogate (`BIGSERIAL` / `BIGINT`) at ingestion; source IDs preserved as-is

---

## 📂 Sector 1 — Finance

### brz_fin_accounts

```sql
CREATE TABLE brz_fin_accounts (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    account_id        VARCHAR(100),
    account_number    VARCHAR(50),
    account_name      VARCHAR(255),
    account_type      VARCHAR(50),       -- savings, checking, credit, loan
    currency_code     VARCHAR(10),
    status            VARCHAR(50),
    customer_id       VARCHAR(100),
    branch_id         VARCHAR(100),
    opened_date       DATE,
    closed_date       DATE,
    raw_payload       TEXT               -- original JSON/XML from source
);
```

### brz_fin_transactions

```sql
CREATE TABLE brz_fin_transactions (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    transaction_id    VARCHAR(100),
    account_id        VARCHAR(100),
    transaction_date  TIMESTAMP,
    value_date        DATE,
    amount            NUMERIC(20, 4),
    currency_code     VARCHAR(10),
    transaction_type  VARCHAR(50),       -- debit, credit, transfer
    description       TEXT,
    reference_no      VARCHAR(100),
    channel           VARCHAR(50),       -- ATM, online, branch, mobile
    merchant_id       VARCHAR(100),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_fin_customers

```sql
CREATE TABLE brz_fin_customers (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    customer_id       VARCHAR(100),
    first_name        VARCHAR(100),
    last_name         VARCHAR(100),
    date_of_birth     DATE,
    national_id       VARCHAR(100),
    email             VARCHAR(255),
    phone             VARCHAR(50),
    address_line1     TEXT,
    address_line2     TEXT,
    city              VARCHAR(100),
    country           VARCHAR(100),
    kyc_status        VARCHAR(50),
    risk_rating       VARCHAR(50),
    segment           VARCHAR(50),       -- retail, corporate, premium
    created_at        TIMESTAMP,
    raw_payload       TEXT
);
```

### brz_fin_loans

```sql
CREATE TABLE brz_fin_loans (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    loan_id           VARCHAR(100),
    customer_id       VARCHAR(100),
    loan_type         VARCHAR(50),       -- personal, mortgage, auto, business
    principal_amount  NUMERIC(20, 4),
    currency_code     VARCHAR(10),
    interest_rate     NUMERIC(8, 4),
    term_months       INTEGER,
    disbursement_date DATE,
    maturity_date     DATE,
    status            VARCHAR(50),
    outstanding_balance NUMERIC(20, 4),
    raw_payload       TEXT
);
```

### brz_fin_market_prices

```sql
CREATE TABLE brz_fin_market_prices (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    ticker_symbol     VARCHAR(20),
    exchange          VARCHAR(50),
    price_date        DATE,
    open_price        NUMERIC(20, 6),
    close_price       NUMERIC(20, 6),
    high_price        NUMERIC(20, 6),
    low_price         NUMERIC(20, 6),
    volume            BIGINT,
    adjusted_close    NUMERIC(20, 6),
    currency_code     VARCHAR(10),
    raw_payload       TEXT
);
```

### brz_fin_ledger_entries

```sql
CREATE TABLE brz_fin_ledger_entries (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    entry_id          VARCHAR(100),
    journal_id        VARCHAR(100),
    entry_date        DATE,
    account_code      VARCHAR(50),
    debit_amount      NUMERIC(20, 4),
    credit_amount     NUMERIC(20, 4),
    currency_code     VARCHAR(10),
    description       TEXT,
    cost_center       VARCHAR(100),
    posted_by         VARCHAR(100),
    raw_payload       TEXT
);
```

### brz_fin_cards

```sql
CREATE TABLE brz_fin_cards (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    card_id           VARCHAR(100),
    account_id        VARCHAR(100),
    customer_id       VARCHAR(100),
    card_type         VARCHAR(50),       -- debit, credit, prepaid
    card_network      VARCHAR(50),       -- visa, mastercard, amex
    card_number_masked VARCHAR(20),
    expiry_date       DATE,
    issued_date       DATE,
    status            VARCHAR(50),
    credit_limit      NUMERIC(20,4),
    raw_payload       TEXT
);
```

### brz_fin_fraud_alerts

```sql
CREATE TABLE brz_fin_fraud_alerts (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    alert_id          VARCHAR(100),
    transaction_id    VARCHAR(100),
    account_id        VARCHAR(100),
    customer_id       VARCHAR(100),
    alert_type        VARCHAR(50),
    severity          VARCHAR(20),
    rule_triggered    VARCHAR(100),
    score             NUMERIC(8,4),
    detected_at       TIMESTAMP,
    resolved_at       TIMESTAMP,
    resolution        VARCHAR(50),       -- confirmed_fraud, false_positive, pending
    raw_payload       TEXT
);
```

### brz_fin_fx_rates

```sql
CREATE TABLE brz_fin_fx_rates (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    rate_id           VARCHAR(100),
    base_currency     CHAR(3),
    quote_currency    CHAR(3),
    rate_date         DATE,
    bid_rate          NUMERIC(20,8),
    ask_rate          NUMERIC(20,8),
    mid_rate          NUMERIC(20,8),
    source            VARCHAR(100),
    raw_payload       TEXT
);
```

### brz_fin_budgets

```sql
CREATE TABLE brz_fin_budgets (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    budget_id         VARCHAR(100),
    cost_center       VARCHAR(100),
    department_id     VARCHAR(100),
    fiscal_year       INTEGER,
    fiscal_period     INTEGER,
    account_code      VARCHAR(50),
    budget_amount     NUMERIC(20,4),
    currency_code     VARCHAR(10),
    budget_type       VARCHAR(50),       -- opex, capex, revenue
    approved_by       VARCHAR(100),
    raw_payload       TEXT
);
```

### brz_fin_invoices

```sql
CREATE TABLE brz_fin_invoices (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    invoice_id        VARCHAR(100),
    invoice_number    VARCHAR(50),
    customer_id       VARCHAR(100),
    invoice_date      DATE,
    due_date          DATE,
    subtotal          NUMERIC(20,4),
    tax_amount        NUMERIC(20,4),
    total_amount      NUMERIC(20,4),
    currency_code     VARCHAR(10),
    status            VARCHAR(50),       -- draft, sent, paid, overdue, cancelled
    payment_terms     VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_fin_audit_logs

```sql
CREATE TABLE brz_fin_audit_logs (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    log_id            VARCHAR(100),
    user_id           VARCHAR(100),
    action            VARCHAR(100),
    entity_type       VARCHAR(100),
    entity_id         VARCHAR(100),
    old_values        TEXT,
    new_values        TEXT,
    ip_address        VARCHAR(50),
    action_timestamp  TIMESTAMP,
    raw_payload       TEXT
);
```

---

## 📂 Sector 2 — Marketing

### brz_mkt_campaigns

```sql
CREATE TABLE brz_mkt_campaigns (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    campaign_id       VARCHAR(100),
    campaign_name     VARCHAR(255),
    campaign_type     VARCHAR(50),       -- email, social, paid, sms, push
    channel           VARCHAR(50),
    status            VARCHAR(50),
    start_date        DATE,
    end_date          DATE,
    budget            NUMERIC(20, 4),
    currency_code     VARCHAR(10),
    target_segment    VARCHAR(100),
    owner_id          VARCHAR(100),
    raw_payload       TEXT
);
```

### brz_mkt_campaign_performance

```sql
CREATE TABLE brz_mkt_campaign_performance (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    performance_id    VARCHAR(100),
    campaign_id       VARCHAR(100),
    report_date       DATE,
    impressions       BIGINT,
    clicks            BIGINT,
    conversions       BIGINT,
    spend             NUMERIC(20, 4),
    revenue           NUMERIC(20, 4),
    reach             BIGINT,
    engagement_rate   NUMERIC(10, 6),
    raw_payload       TEXT
);
```

### brz_mkt_leads

```sql
CREATE TABLE brz_mkt_leads (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    lead_id           VARCHAR(100),
    campaign_id       VARCHAR(100),
    first_name        VARCHAR(100),
    last_name         VARCHAR(100),
    email             VARCHAR(255),
    phone             VARCHAR(50),
    company           VARCHAR(255),
    lead_source       VARCHAR(100),
    lead_status       VARCHAR(50),
    score             INTEGER,
    assigned_to       VARCHAR(100),
    created_at        TIMESTAMP,
    raw_payload       TEXT
);
```

### brz_mkt_email_events

```sql
CREATE TABLE brz_mkt_email_events (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    event_id          VARCHAR(100),
    campaign_id       VARCHAR(100),
    recipient_email   VARCHAR(255),
    event_type        VARCHAR(50),       -- sent, opened, clicked, bounced, unsubscribed
    event_timestamp   TIMESTAMP,
    ip_address        VARCHAR(50),
    user_agent        TEXT,
    link_url          TEXT,
    raw_payload       TEXT
);
```

### brz_mkt_social_metrics

```sql
CREATE TABLE brz_mkt_social_metrics (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    metric_id         VARCHAR(100),
    platform          VARCHAR(50),       -- facebook, instagram, twitter, linkedin, tiktok
    post_id           VARCHAR(100),
    post_date         DATE,
    likes             BIGINT,
    shares            BIGINT,
    comments          BIGINT,
    impressions       BIGINT,
    reach             BIGINT,
    video_views       BIGINT,
    raw_payload       TEXT
);
```

### brz_mkt_customers_segments

```sql
CREATE TABLE brz_mkt_customers_segments (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    segment_id        VARCHAR(100),
    segment_name      VARCHAR(255),
    segment_type      VARCHAR(50),       -- demographic, behavioral, geographic, psychographic
    criteria          TEXT,
    customer_count    BIGINT,
    created_by        VARCHAR(100),
    created_at        TIMESTAMP,
    raw_payload       TEXT
);
```

### brz_mkt_ab_tests

```sql
CREATE TABLE brz_mkt_ab_tests (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    test_id           VARCHAR(100),
    test_name         VARCHAR(255),
    campaign_id       VARCHAR(100),
    variant           VARCHAR(10),       -- A, B, C
    start_date        DATE,
    end_date          DATE,
    sample_size       BIGINT,
    conversions       BIGINT,
    revenue           NUMERIC(20,4),
    status            VARCHAR(50),
    winner            VARCHAR(10),
    raw_payload       TEXT
);
```

### brz_mkt_content_assets

```sql
CREATE TABLE brz_mkt_content_assets (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    asset_id          VARCHAR(100),
    asset_name        VARCHAR(255),
    asset_type        VARCHAR(50),       -- image, video, blog, whitepaper, infographic
    campaign_id       VARCHAR(100),
    channel           VARCHAR(50),
    publish_date      DATE,
    views             BIGINT,
    downloads         BIGINT,
    shares            BIGINT,
    created_by        VARCHAR(100),
    raw_payload       TEXT
);
```

### brz_mkt_website_traffic

```sql
CREATE TABLE brz_mkt_website_traffic (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    traffic_id        VARCHAR(100),
    page_url          TEXT,
    traffic_date      DATE,
    sessions          BIGINT,
    users             BIGINT,
    new_users         BIGINT,
    pageviews         BIGINT,
    bounce_rate       NUMERIC(8,4),
    avg_session_sec   NUMERIC(10,2),
    source            VARCHAR(100),
    medium            VARCHAR(100),
    raw_payload       TEXT
);
```

### brz_mkt_customer_journeys

```sql
CREATE TABLE brz_mkt_customer_journeys (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    journey_id        VARCHAR(100),
    customer_id       VARCHAR(100),
    touchpoint_seq    INTEGER,
    channel           VARCHAR(50),
    event_type        VARCHAR(50),
    campaign_id       VARCHAR(100),
    event_timestamp   TIMESTAMP,
    is_conversion     BOOLEAN,
    raw_payload       TEXT
);
```

### brz_mkt_surveys

```sql
CREATE TABLE brz_mkt_surveys (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    response_id       VARCHAR(100),
    survey_id         VARCHAR(100),
    customer_id       VARCHAR(100),
    submitted_at      TIMESTAMP,
    nps_score         INTEGER,
    csat_score        NUMERIC(4,2),
    ces_score         NUMERIC(4,2),
    comments          TEXT,
    channel           VARCHAR(50),
    raw_payload       TEXT
);
```

---

## 📂 Sector 3 — Healthcare

### brz_hlt_patients

```sql
CREATE TABLE brz_hlt_patients (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    patient_id        VARCHAR(100),
    mrn               VARCHAR(100),      -- medical record number
    first_name        VARCHAR(100),
    last_name         VARCHAR(100),
    date_of_birth     DATE,
    gender            VARCHAR(20),
    blood_type        VARCHAR(10),
    phone             VARCHAR(50),
    email             VARCHAR(255),
    address_line1     TEXT,
    city              VARCHAR(100),
    country           VARCHAR(100),
    insurance_id      VARCHAR(100),
    registration_date DATE,
    raw_payload       TEXT
);
```

### brz_hlt_appointments

```sql
CREATE TABLE brz_hlt_appointments (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    appointment_id    VARCHAR(100),
    patient_id        VARCHAR(100),
    provider_id       VARCHAR(100),
    facility_id       VARCHAR(100),
    appointment_date  TIMESTAMP,
    appointment_type  VARCHAR(100),
    status            VARCHAR(50),       -- scheduled, completed, cancelled, no-show
    reason            TEXT,
    duration_minutes  INTEGER,
    notes             TEXT,
    raw_payload       TEXT
);
```

### brz_hlt_diagnoses

```sql
CREATE TABLE brz_hlt_diagnoses (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    diagnosis_id      VARCHAR(100),
    patient_id        VARCHAR(100),
    encounter_id      VARCHAR(100),
    icd_code          VARCHAR(20),
    icd_version       VARCHAR(10),
    description       TEXT,
    diagnosis_type    VARCHAR(50),       -- primary, secondary, admitting
    diagnosed_at      TIMESTAMP,
    provider_id       VARCHAR(100),
    raw_payload       TEXT
);
```

### brz_hlt_prescriptions

```sql
CREATE TABLE brz_hlt_prescriptions (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    prescription_id   VARCHAR(100),
    patient_id        VARCHAR(100),
    provider_id       VARCHAR(100),
    drug_code         VARCHAR(50),
    drug_name         VARCHAR(255),
    dosage            VARCHAR(100),
    frequency         VARCHAR(100),
    quantity          NUMERIC(10, 2),
    unit              VARCHAR(50),
    prescribed_at     TIMESTAMP,
    start_date        DATE,
    end_date          DATE,
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_hlt_lab_results

```sql
CREATE TABLE brz_hlt_lab_results (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    result_id         VARCHAR(100),
    patient_id        VARCHAR(100),
    order_id          VARCHAR(100),
    test_code         VARCHAR(50),
    test_name         VARCHAR(255),
    result_value      VARCHAR(255),
    unit              VARCHAR(50),
    reference_range   VARCHAR(100),
    abnormal_flag     VARCHAR(10),
    collected_at      TIMESTAMP,
    resulted_at       TIMESTAMP,
    raw_payload       TEXT
);
```

### brz_hlt_providers

```sql
CREATE TABLE brz_hlt_providers (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    provider_id       VARCHAR(100),
    npi               VARCHAR(20),       -- national provider identifier
    first_name        VARCHAR(100),
    last_name         VARCHAR(100),
    specialty         VARCHAR(100),
    license_number    VARCHAR(100),
    facility_id       VARCHAR(100),
    phone             VARCHAR(50),
    email             VARCHAR(255),
    active            BOOLEAN,
    raw_payload       TEXT
);
```

### brz_hlt_encounters

```sql
CREATE TABLE brz_hlt_encounters (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    encounter_id      VARCHAR(100),
    patient_id        VARCHAR(100),
    provider_id       VARCHAR(100),
    facility_id       VARCHAR(100),
    encounter_type    VARCHAR(50),       -- inpatient, outpatient, emergency, telehealth
    admit_date        TIMESTAMP,
    discharge_date    TIMESTAMP,
    discharge_disposition VARCHAR(50),
    drg_code          VARCHAR(20),
    primary_dx_code   VARCHAR(20),
    raw_payload       TEXT
);
```

### brz_hlt_procedures

```sql
CREATE TABLE brz_hlt_procedures (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    procedure_id      VARCHAR(100),
    encounter_id      VARCHAR(100),
    patient_id        VARCHAR(100),
    provider_id       VARCHAR(100),
    cpt_code          VARCHAR(20),
    procedure_name    VARCHAR(255),
    procedure_date    TIMESTAMP,
    quantity          INTEGER,
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_hlt_vitals

```sql
CREATE TABLE brz_hlt_vitals (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    vital_id          VARCHAR(100),
    patient_id        VARCHAR(100),
    encounter_id      VARCHAR(100),
    recorded_at       TIMESTAMP,
    height_cm         NUMERIC(6,2),
    weight_kg         NUMERIC(6,2),
    bmi               NUMERIC(6,2),
    blood_pressure_sys INTEGER,
    blood_pressure_dia INTEGER,
    heart_rate        INTEGER,
    temperature_c     NUMERIC(5,2),
    oxygen_sat_pct    NUMERIC(5,2),
    raw_payload       TEXT
);
```

### brz_hlt_insurance_claims

```sql
CREATE TABLE brz_hlt_insurance_claims (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    claim_id          VARCHAR(100),
    encounter_id      VARCHAR(100),
    patient_id        VARCHAR(100),
    payer_id          VARCHAR(100),
    submission_date   DATE,
    service_date      DATE,
    billed_amount     NUMERIC(20,4),
    allowed_amount    NUMERIC(20,4),
    paid_amount       NUMERIC(20,4),
    denial_reason     VARCHAR(100),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_hlt_facilities

```sql
CREATE TABLE brz_hlt_facilities (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    facility_id       VARCHAR(100),
    facility_name     VARCHAR(255),
    facility_type     VARCHAR(50),       -- hospital, clinic, lab, pharmacy
    address_line1     TEXT,
    city              VARCHAR(100),
    country           VARCHAR(100),
    bed_count         INTEGER,
    accreditation     VARCHAR(100),
    is_active         BOOLEAN,
    raw_payload       TEXT
);
```

### brz_hlt_allergies

```sql
CREATE TABLE brz_hlt_allergies (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    allergy_id        VARCHAR(100),
    patient_id        VARCHAR(100),
    allergen          VARCHAR(255),
    allergy_type      VARCHAR(50),       -- drug, food, environmental
    reaction          VARCHAR(255),
    severity          VARCHAR(20),
    onset_date        DATE,
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

---

## 📂 Sector 4 — Retail

### brz_ret_products

```sql
CREATE TABLE brz_ret_products (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    product_id        VARCHAR(100),
    sku               VARCHAR(100),
    barcode           VARCHAR(100),
    product_name      VARCHAR(255),
    brand             VARCHAR(100),
    category          VARCHAR(100),
    subcategory       VARCHAR(100),
    unit_cost         NUMERIC(20, 4),
    unit_price        NUMERIC(20, 4),
    currency_code     VARCHAR(10),
    uom               VARCHAR(50),       -- unit of measure
    is_active         BOOLEAN,
    raw_payload       TEXT
);
```

### brz_ret_sales_transactions

```sql
CREATE TABLE brz_ret_sales_transactions (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    transaction_id    VARCHAR(100),
    store_id          VARCHAR(100),
    pos_terminal_id   VARCHAR(100),
    customer_id       VARCHAR(100),
    transaction_date  TIMESTAMP,
    total_amount      NUMERIC(20, 4),
    discount_amount   NUMERIC(20, 4),
    tax_amount        NUMERIC(20, 4),
    payment_method    VARCHAR(50),
    cashier_id        VARCHAR(100),
    currency_code     VARCHAR(10),
    raw_payload       TEXT
);
```

### brz_ret_sales_items

```sql
CREATE TABLE brz_ret_sales_items (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    line_id           VARCHAR(100),
    transaction_id    VARCHAR(100),
    product_id        VARCHAR(100),
    sku               VARCHAR(100),
    quantity          NUMERIC(10, 3),
    unit_price        NUMERIC(20, 4),
    discount          NUMERIC(20, 4),
    line_total        NUMERIC(20, 4),
    raw_payload       TEXT
);
```

### brz_ret_stores

```sql
CREATE TABLE brz_ret_stores (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    store_id          VARCHAR(100),
    store_code        VARCHAR(50),
    store_name        VARCHAR(255),
    store_type        VARCHAR(50),       -- flagship, outlet, kiosk, franchise
    address_line1     TEXT,
    city              VARCHAR(100),
    region            VARCHAR(100),
    country           VARCHAR(100),
    manager_id        VARCHAR(100),
    open_date         DATE,
    is_active         BOOLEAN,
    raw_payload       TEXT
);
```

### brz_ret_inventory

```sql
CREATE TABLE brz_ret_inventory (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    inventory_id      VARCHAR(100),
    store_id          VARCHAR(100),
    product_id        VARCHAR(100),
    sku               VARCHAR(100),
    quantity_on_hand  NUMERIC(10, 3),
    quantity_reserved NUMERIC(10, 3),
    reorder_point     NUMERIC(10, 3),
    last_count_date   DATE,
    raw_payload       TEXT
);
```

### brz_ret_customers

```sql
CREATE TABLE brz_ret_customers (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    customer_id       VARCHAR(100),
    first_name        VARCHAR(100),
    last_name         VARCHAR(100),
    email             VARCHAR(255),
    phone             VARCHAR(50),
    loyalty_card_no   VARCHAR(100),
    loyalty_points    BIGINT,
    tier              VARCHAR(50),
    registered_at     TIMESTAMP,
    date_of_birth     DATE,
    gender            VARCHAR(20),
    raw_payload       TEXT
);
```

### brz_ret_promotions

```sql
CREATE TABLE brz_ret_promotions (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    promotion_id      VARCHAR(100),
    promo_name        VARCHAR(255),
    promo_type        VARCHAR(50),       -- percent_off, buy_x_get_y, fixed_amount, bundle
    start_date        DATE,
    end_date          DATE,
    discount_value    NUMERIC(10,4),
    min_purchase      NUMERIC(20,4),
    applicable_skus   TEXT,
    store_ids         TEXT,
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_ret_returns

```sql
CREATE TABLE brz_ret_returns (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    return_id         VARCHAR(100),
    transaction_id    VARCHAR(100),
    store_id          VARCHAR(100),
    customer_id       VARCHAR(100),
    return_date       TIMESTAMP,
    reason_code       VARCHAR(50),
    product_id        VARCHAR(100),
    quantity          NUMERIC(10,3),
    refund_amount     NUMERIC(20,4),
    return_method     VARCHAR(50),       -- in_store, mail, pickup
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_ret_suppliers

```sql
CREATE TABLE brz_ret_suppliers (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    supplier_id       VARCHAR(100),
    supplier_name     VARCHAR(255),
    contact_name      VARCHAR(100),
    email             VARCHAR(255),
    phone             VARCHAR(50),
    country           VARCHAR(100),
    payment_terms     VARCHAR(50),
    lead_time_days    INTEGER,
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_ret_purchase_orders

```sql
CREATE TABLE brz_ret_purchase_orders (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    po_id             VARCHAR(100),
    po_number         VARCHAR(50),
    supplier_id       VARCHAR(100),
    store_id          VARCHAR(100),
    order_date        DATE,
    expected_date     DATE,
    total_amount      NUMERIC(20,4),
    currency_code     VARCHAR(10),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_ret_shrinkage

```sql
CREATE TABLE brz_ret_shrinkage (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    shrinkage_id      VARCHAR(100),
    store_id          VARCHAR(100),
    product_id        VARCHAR(100),
    event_date        DATE,
    quantity_lost     NUMERIC(10,3),
    unit_cost         NUMERIC(20,4),
    total_loss_value  NUMERIC(20,4),
    reason_code       VARCHAR(50),       -- theft, damage, expiry, admin_error
    raw_payload       TEXT
);
```

### brz_ret_price_changes

```sql
CREATE TABLE brz_ret_price_changes (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    change_id         VARCHAR(100),
    product_id        VARCHAR(100),
    store_id          VARCHAR(100),
    old_price         NUMERIC(20,4),
    new_price         NUMERIC(20,4),
    effective_date    DATE,
    reason            VARCHAR(100),
    approved_by       VARCHAR(100),
    raw_payload       TEXT
);
```

---

## 📂 Sector 5 — Manufacturing

### brz_mfg_work_orders

```sql
CREATE TABLE brz_mfg_work_orders (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    work_order_id     VARCHAR(100),
    product_id        VARCHAR(100),
    bom_id            VARCHAR(100),      -- bill of materials
    plant_id          VARCHAR(100),
    quantity_planned  NUMERIC(15, 3),
    quantity_produced NUMERIC(15, 3),
    start_date        DATE,
    end_date          DATE,
    status            VARCHAR(50),
    priority          VARCHAR(20),
    raw_payload       TEXT
);
```

### brz_mfg_machines

```sql
CREATE TABLE brz_mfg_machines (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    machine_id        VARCHAR(100),
    machine_code      VARCHAR(50),
    machine_name      VARCHAR(255),
    machine_type      VARCHAR(100),
    plant_id          VARCHAR(100),
    line_id           VARCHAR(100),
    manufacturer      VARCHAR(100),
    model             VARCHAR(100),
    serial_number     VARCHAR(100),
    install_date      DATE,
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_mfg_machine_telemetry

```sql
CREATE TABLE brz_mfg_machine_telemetry (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    telemetry_id      VARCHAR(100),
    machine_id        VARCHAR(100),
    recorded_at       TIMESTAMP,
    temperature       NUMERIC(10, 4),
    pressure          NUMERIC(10, 4),
    vibration         NUMERIC(10, 4),
    rpm               NUMERIC(10, 2),
    power_consumption NUMERIC(10, 4),
    status_code       VARCHAR(20),
    raw_payload       TEXT
);
```

### brz_mfg_quality_inspections

```sql
CREATE TABLE brz_mfg_quality_inspections (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    inspection_id     VARCHAR(100),
    work_order_id     VARCHAR(100),
    batch_number      VARCHAR(100),
    product_id        VARCHAR(100),
    inspector_id      VARCHAR(100),
    inspection_date   TIMESTAMP,
    quantity_inspected NUMERIC(15, 3),
    quantity_passed   NUMERIC(15, 3),
    quantity_rejected NUMERIC(15, 3),
    defect_code       VARCHAR(50),
    result            VARCHAR(50),       -- pass, fail, conditional
    raw_payload       TEXT
);
```

### brz_mfg_bill_of_materials

```sql
CREATE TABLE brz_mfg_bill_of_materials (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    bom_id            VARCHAR(100),
    bom_version       VARCHAR(20),
    product_id        VARCHAR(100),
    component_id      VARCHAR(100),
    quantity_required NUMERIC(15, 6),
    uom               VARCHAR(50),
    scrap_factor      NUMERIC(8, 4),
    effective_date    DATE,
    expiry_date       DATE,
    raw_payload       TEXT
);
```

### brz_mfg_maintenance_orders

```sql
CREATE TABLE brz_mfg_maintenance_orders (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    order_id          VARCHAR(100),
    machine_id        VARCHAR(100),
    plant_id          VARCHAR(100),
    order_type        VARCHAR(50),       -- preventive, corrective, predictive
    priority          VARCHAR(20),
    scheduled_date    DATE,
    completed_date    DATE,
    technician_id     VARCHAR(100),
    downtime_minutes  INTEGER,
    cost              NUMERIC(20,4),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_mfg_production_schedules

```sql
CREATE TABLE brz_mfg_production_schedules (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    schedule_id       VARCHAR(100),
    plant_id          VARCHAR(100),
    line_id           VARCHAR(100),
    product_id        VARCHAR(100),
    scheduled_date    DATE,
    shift             VARCHAR(20),
    planned_qty       NUMERIC(15,3),
    actual_qty        NUMERIC(15,3),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_mfg_raw_materials

```sql
CREATE TABLE brz_mfg_raw_materials (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    material_id       VARCHAR(100),
    material_code     VARCHAR(50),
    material_name     VARCHAR(255),
    material_type     VARCHAR(50),
    uom               VARCHAR(50),
    stock_qty         NUMERIC(15,3),
    reorder_level     NUMERIC(15,3),
    supplier_id       VARCHAR(100),
    unit_cost         NUMERIC(20,4),
    storage_location  VARCHAR(100),
    raw_payload       TEXT
);
```

### brz_mfg_shift_logs

```sql
CREATE TABLE brz_mfg_shift_logs (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    log_id            VARCHAR(100),
    plant_id          VARCHAR(100),
    line_id           VARCHAR(100),
    shift_date        DATE,
    shift             VARCHAR(20),       -- morning, evening, night
    supervisor_id     VARCHAR(100),
    operators_count   INTEGER,
    production_qty    NUMERIC(15,3),
    downtime_minutes  INTEGER,
    incidents         INTEGER,
    notes             TEXT,
    raw_payload       TEXT
);
```

### brz_mfg_energy_consumption

```sql
CREATE TABLE brz_mfg_energy_consumption (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    consumption_id    VARCHAR(100),
    plant_id          VARCHAR(100),
    machine_id        VARCHAR(100),
    reading_date      DATE,
    electricity_kwh   NUMERIC(15,4),
    gas_m3            NUMERIC(15,4),
    water_liters      NUMERIC(15,4),
    cost              NUMERIC(20,4),
    raw_payload       TEXT
);
```

### brz_mfg_scrap_records

```sql
CREATE TABLE brz_mfg_scrap_records (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    scrap_id          VARCHAR(100),
    work_order_id     VARCHAR(100),
    product_id        VARCHAR(100),
    plant_id          VARCHAR(100),
    scrap_date        DATE,
    quantity          NUMERIC(15,3),
    uom               VARCHAR(50),
    reason_code       VARCHAR(50),
    disposal_method   VARCHAR(50),
    cost              NUMERIC(20,4),
    raw_payload       TEXT
);
```

---

## 📂 Sector 6 — E-Commerce

### brz_ecom_orders

```sql
CREATE TABLE brz_ecom_orders (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    order_id          VARCHAR(100),
    customer_id       VARCHAR(100),
    order_date        TIMESTAMP,
    status            VARCHAR(50),
    subtotal          NUMERIC(20, 4),
    discount          NUMERIC(20, 4),
    tax               NUMERIC(20, 4),
    shipping_fee      NUMERIC(20, 4),
    total_amount      NUMERIC(20, 4),
    currency_code     VARCHAR(10),
    payment_status    VARCHAR(50),
    channel           VARCHAR(50),       -- web, mobile_app, marketplace
    raw_payload       TEXT
);
```

### brz_ecom_order_items

```sql
CREATE TABLE brz_ecom_order_items (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    line_id           VARCHAR(100),
    order_id          VARCHAR(100),
    product_id        VARCHAR(100),
    sku               VARCHAR(100),
    product_name      VARCHAR(255),
    quantity          NUMERIC(10, 2),
    unit_price        NUMERIC(20, 4),
    discount          NUMERIC(20, 4),
    line_total        NUMERIC(20, 4),
    raw_payload       TEXT
);
```

### brz_ecom_customers

```sql
CREATE TABLE brz_ecom_customers (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    customer_id       VARCHAR(100),
    email             VARCHAR(255),
    first_name        VARCHAR(100),
    last_name         VARCHAR(100),
    phone             VARCHAR(50),
    registered_at     TIMESTAMP,
    last_login        TIMESTAMP,
    is_guest          BOOLEAN,
    marketing_opt_in  BOOLEAN,
    raw_payload       TEXT
);
```

### brz_ecom_product_catalog

```sql
CREATE TABLE brz_ecom_product_catalog (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    product_id        VARCHAR(100),
    sku               VARCHAR(100),
    product_name      VARCHAR(255),
    description       TEXT,
    category          VARCHAR(100),
    subcategory       VARCHAR(100),
    brand             VARCHAR(100),
    price             NUMERIC(20, 4),
    sale_price        NUMERIC(20, 4),
    currency_code     VARCHAR(10),
    stock_quantity    INTEGER,
    is_active         BOOLEAN,
    raw_payload       TEXT
);
```

### brz_ecom_web_sessions

```sql
CREATE TABLE brz_ecom_web_sessions (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    session_id        VARCHAR(100),
    customer_id       VARCHAR(100),
    session_start     TIMESTAMP,
    session_end       TIMESTAMP,
    device_type       VARCHAR(50),
    browser           VARCHAR(100),
    os                VARCHAR(100),
    ip_address        VARCHAR(50),
    referral_source   VARCHAR(255),
    pages_viewed      INTEGER,
    cart_adds         INTEGER,
    converted         BOOLEAN,
    raw_payload       TEXT
);
```

### brz_ecom_returns

```sql
CREATE TABLE brz_ecom_returns (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    return_id         VARCHAR(100),
    order_id          VARCHAR(100),
    customer_id       VARCHAR(100),
    return_date       TIMESTAMP,
    reason_code       VARCHAR(50),
    reason_text       TEXT,
    status            VARCHAR(50),
    refund_amount     NUMERIC(20, 4),
    raw_payload       TEXT
);
```

### brz_ecom_reviews

```sql
CREATE TABLE brz_ecom_reviews (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    review_id         VARCHAR(100),
    product_id        VARCHAR(100),
    customer_id       VARCHAR(100),
    order_id          VARCHAR(100),
    rating            SMALLINT,
    title             VARCHAR(255),
    body              TEXT,
    is_verified       BOOLEAN,
    helpful_votes     INTEGER,
    submitted_at      TIMESTAMP,
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_ecom_cart_events

```sql
CREATE TABLE brz_ecom_cart_events (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    event_id          VARCHAR(100),
    session_id        VARCHAR(100),
    customer_id       VARCHAR(100),
    product_id        VARCHAR(100),
    event_type        VARCHAR(50),       -- add, remove, view, wishlist
    quantity          NUMERIC(10,2),
    price_at_event    NUMERIC(20,4),
    event_timestamp   TIMESTAMP,
    raw_payload       TEXT
);
```

### brz_ecom_promotions

```sql
CREATE TABLE brz_ecom_promotions (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    promo_id          VARCHAR(100),
    promo_code        VARCHAR(50),
    promo_type        VARCHAR(50),
    discount_value    NUMERIC(10,4),
    min_order_amount  NUMERIC(20,4),
    usage_limit       INTEGER,
    times_used        INTEGER,
    start_date        DATE,
    end_date          DATE,
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_ecom_payments

```sql
CREATE TABLE brz_ecom_payments (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    payment_id        VARCHAR(100),
    order_id          VARCHAR(100),
    payment_method    VARCHAR(50),
    payment_gateway   VARCHAR(100),
    amount            NUMERIC(20,4),
    currency_code     VARCHAR(10),
    status            VARCHAR(50),
    gateway_ref       VARCHAR(100),
    paid_at           TIMESTAMP,
    raw_payload       TEXT
);
```

### brz_ecom_wishlists

```sql
CREATE TABLE brz_ecom_wishlists (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    wishlist_id       VARCHAR(100),
    customer_id       VARCHAR(100),
    product_id        VARCHAR(100),
    added_at          TIMESTAMP,
    moved_to_cart     BOOLEAN,
    purchased         BOOLEAN,
    raw_payload       TEXT
);
```

### brz_ecom_sellers

```sql
CREATE TABLE brz_ecom_sellers (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    seller_id         VARCHAR(100),
    seller_name       VARCHAR(255),
    email             VARCHAR(255),
    phone             VARCHAR(50),
    country           VARCHAR(100),
    category          VARCHAR(100),
    rating            NUMERIC(4,2),
    total_products    INTEGER,
    joined_date       DATE,
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

---

## 📂 Sector 7 — Logistics

### brz_log_shipments

```sql
CREATE TABLE brz_log_shipments (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    shipment_id       VARCHAR(100),
    tracking_number   VARCHAR(100),
    carrier_id        VARCHAR(100),
    origin_id         VARCHAR(100),
    destination_id    VARCHAR(100),
    shipper_id        VARCHAR(100),
    consignee_id      VARCHAR(100),
    ship_date         TIMESTAMP,
    estimated_delivery DATE,
    actual_delivery   TIMESTAMP,
    status            VARCHAR(50),
    weight_kg         NUMERIC(10, 3),
    volume_m3         NUMERIC(10, 4),
    raw_payload       TEXT
);
```

### brz_log_shipment_events

```sql
CREATE TABLE brz_log_shipment_events (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    event_id          VARCHAR(100),
    shipment_id       VARCHAR(100),
    event_type        VARCHAR(50),       -- picked_up, in_transit, out_for_delivery, delivered, exception
    event_timestamp   TIMESTAMP,
    location_code     VARCHAR(100),
    location_name     VARCHAR(255),
    latitude          NUMERIC(10, 7),
    longitude         NUMERIC(10, 7),
    notes             TEXT,
    raw_payload       TEXT
);
```

### brz_log_warehouses

```sql
CREATE TABLE brz_log_warehouses (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    warehouse_id      VARCHAR(100),
    warehouse_code    VARCHAR(50),
    warehouse_name    VARCHAR(255),
    warehouse_type    VARCHAR(50),       -- fulfillment, distribution, cold storage
    address_line1     TEXT,
    city              VARCHAR(100),
    country           VARCHAR(100),
    capacity_m3       NUMERIC(15, 2),
    is_active         BOOLEAN,
    raw_payload       TEXT
);
```

### brz_log_vehicles

```sql
CREATE TABLE brz_log_vehicles (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    vehicle_id        VARCHAR(100),
    plate_number      VARCHAR(50),
    vehicle_type      VARCHAR(50),       -- truck, van, motorcycle, container
    capacity_kg       NUMERIC(10, 2),
    capacity_m3       NUMERIC(10, 4),
    driver_id         VARCHAR(100),
    carrier_id        VARCHAR(100),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_log_routes

```sql
CREATE TABLE brz_log_routes (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    route_id          VARCHAR(100),
    route_name        VARCHAR(255),
    origin_id         VARCHAR(100),
    destination_id    VARCHAR(100),
    distance_km       NUMERIC(10,2),
    transit_days      INTEGER,
    mode              VARCHAR(50),       -- road, rail, air, sea
    carrier_id        VARCHAR(100),
    is_active         BOOLEAN,
    raw_payload       TEXT
);
```

### brz_log_delivery_attempts

```sql
CREATE TABLE brz_log_delivery_attempts (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    attempt_id        VARCHAR(100),
    shipment_id       VARCHAR(100),
    attempt_number    INTEGER,
    attempt_date      TIMESTAMP,
    driver_id         VARCHAR(100),
    status            VARCHAR(50),       -- delivered, failed, rescheduled
    failure_reason    VARCHAR(100),
    next_attempt_date DATE,
    raw_payload       TEXT
);
```

### brz_log_customs

```sql
CREATE TABLE brz_log_customs (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    customs_id        VARCHAR(100),
    shipment_id       VARCHAR(100),
    declaration_no    VARCHAR(100),
    entry_port        VARCHAR(100),
    country_of_origin VARCHAR(100),
    destination_country VARCHAR(100),
    hs_code           VARCHAR(20),
    declared_value    NUMERIC(20,4),
    duties_amount     NUMERIC(20,4),
    status            VARCHAR(50),
    clearance_date    DATE,
    raw_payload       TEXT
);
```

### brz_log_fleet_maintenance

```sql
CREATE TABLE brz_log_fleet_maintenance (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    maintenance_id    VARCHAR(100),
    vehicle_id        VARCHAR(100),
    maintenance_type  VARCHAR(50),
    service_date      DATE,
    odometer_km       NUMERIC(12,2),
    technician_id     VARCHAR(100),
    cost              NUMERIC(20,4),
    next_service_date DATE,
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_log_packaging

```sql
CREATE TABLE brz_log_packaging (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    package_id        VARCHAR(100),
    shipment_id       VARCHAR(100),
    package_type      VARCHAR(50),
    length_cm         NUMERIC(8,2),
    width_cm          NUMERIC(8,2),
    height_cm         NUMERIC(8,2),
    weight_kg         NUMERIC(10,3),
    fragile           BOOLEAN,
    hazmat            BOOLEAN,
    raw_payload       TEXT
);
```

---

## 📂 Sector 8 — Supply Chain

### brz_sc_suppliers

```sql
CREATE TABLE brz_sc_suppliers (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    supplier_id       VARCHAR(100),
    supplier_code     VARCHAR(50),
    supplier_name     VARCHAR(255),
    contact_name      VARCHAR(100),
    email             VARCHAR(255),
    phone             VARCHAR(50),
    country           VARCHAR(100),
    payment_terms     VARCHAR(50),
    lead_time_days    INTEGER,
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_sc_purchase_orders

```sql
CREATE TABLE brz_sc_purchase_orders (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    po_id             VARCHAR(100),
    po_number         VARCHAR(50),
    supplier_id       VARCHAR(100),
    buyer_id          VARCHAR(100),
    order_date        DATE,
    expected_date     DATE,
    status            VARCHAR(50),
    total_amount      NUMERIC(20, 4),
    currency_code     VARCHAR(10),
    raw_payload       TEXT
);
```

### brz_sc_purchase_order_lines

```sql
CREATE TABLE brz_sc_purchase_order_lines (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    line_id           VARCHAR(100),
    po_id             VARCHAR(100),
    item_id           VARCHAR(100),
    description       TEXT,
    quantity_ordered  NUMERIC(15, 3),
    quantity_received NUMERIC(15, 3),
    unit_price        NUMERIC(20, 4),
    uom               VARCHAR(50),
    line_total        NUMERIC(20, 4),
    raw_payload       TEXT
);
```

### brz_sc_goods_receipts

```sql
CREATE TABLE brz_sc_goods_receipts (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    receipt_id        VARCHAR(100),
    po_id             VARCHAR(100),
    warehouse_id      VARCHAR(100),
    received_date     TIMESTAMP,
    received_by       VARCHAR(100),
    status            VARCHAR(50),
    notes             TEXT,
    raw_payload       TEXT
);
```

### brz_sc_inventory_movements

```sql
CREATE TABLE brz_sc_inventory_movements (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    movement_id       VARCHAR(100),
    item_id           VARCHAR(100),
    warehouse_id      VARCHAR(100),
    movement_type     VARCHAR(50),       -- receipt, issue, transfer, adjustment
    quantity          NUMERIC(15, 3),
    uom               VARCHAR(50),
    reference_doc     VARCHAR(100),
    movement_date     TIMESTAMP,
    raw_payload       TEXT
);
```

### brz_sc_contracts

```sql
CREATE TABLE brz_sc_contracts (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    contract_id       VARCHAR(100),
    contract_number   VARCHAR(50),
    supplier_id       VARCHAR(100),
    contract_type     VARCHAR(50),
    start_date        DATE,
    end_date          DATE,
    total_value       NUMERIC(20,4),
    currency_code     VARCHAR(10),
    payment_terms     VARCHAR(50),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_sc_demand_forecasts

```sql
CREATE TABLE brz_sc_demand_forecasts (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    forecast_id       VARCHAR(100),
    item_id           VARCHAR(100),
    warehouse_id      VARCHAR(100),
    forecast_date     DATE,
    forecast_period   VARCHAR(20),       -- weekly, monthly
    forecasted_qty    NUMERIC(15,3),
    actual_qty        NUMERIC(15,3),
    model_version     VARCHAR(50),
    confidence_pct    NUMERIC(6,2),
    raw_payload       TEXT
);
```

### brz_sc_returns_to_supplier

```sql
CREATE TABLE brz_sc_returns_to_supplier (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    return_id         VARCHAR(100),
    po_id             VARCHAR(100),
    supplier_id       VARCHAR(100),
    item_id           VARCHAR(100),
    return_date       DATE,
    quantity          NUMERIC(15,3),
    reason_code       VARCHAR(50),
    credit_note_no    VARCHAR(100),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_sc_warehouse_locations

```sql
CREATE TABLE brz_sc_warehouse_locations (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    location_id       VARCHAR(100),
    warehouse_id      VARCHAR(100),
    zone              VARCHAR(20),
    aisle             VARCHAR(10),
    rack              VARCHAR(10),
    bin               VARCHAR(10),
    capacity_units    INTEGER,
    current_units     INTEGER,
    is_active         BOOLEAN,
    raw_payload       TEXT
);
```

### brz_sc_quality_holds

```sql
CREATE TABLE brz_sc_quality_holds (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    hold_id           VARCHAR(100),
    item_id           VARCHAR(100),
    warehouse_id      VARCHAR(100),
    quantity_held     NUMERIC(15,3),
    reason            TEXT,
    hold_date         DATE,
    release_date      DATE,
    disposition       VARCHAR(50),       -- return, destroy, use_as_is, rework
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

---

## 📂 Sector 9 — Telecommunications

### brz_tel_subscribers

```sql
CREATE TABLE brz_tel_subscribers (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    subscriber_id     VARCHAR(100),
    msisdn            VARCHAR(20),       -- mobile number
    sim_iccid         VARCHAR(50),
    plan_id           VARCHAR(100),
    activation_date   DATE,
    status            VARCHAR(50),
    customer_id       VARCHAR(100),
    network_type      VARCHAR(20),       -- 4G, 5G, LTE
    raw_payload       TEXT
);
```

### brz_tel_call_detail_records

```sql
CREATE TABLE brz_tel_call_detail_records (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    cdr_id            VARCHAR(100),
    caller_msisdn     VARCHAR(20),
    callee_msisdn     VARCHAR(20),
    call_start        TIMESTAMP,
    call_end          TIMESTAMP,
    duration_seconds  INTEGER,
    call_type         VARCHAR(20),       -- voice, video, data
    direction         VARCHAR(10),       -- inbound, outbound
    cell_id           VARCHAR(50),
    roaming           BOOLEAN,
    charge_amount     NUMERIC(20, 6),
    raw_payload       TEXT
);
```

### brz_tel_data_usage

```sql
CREATE TABLE brz_tel_data_usage (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    usage_id          VARCHAR(100),
    subscriber_id     VARCHAR(100),
    session_start     TIMESTAMP,
    session_end       TIMESTAMP,
    bytes_uploaded    BIGINT,
    bytes_downloaded  BIGINT,
    apn               VARCHAR(100),
    cell_id           VARCHAR(50),
    roaming           BOOLEAN,
    raw_payload       TEXT
);
```

### brz_tel_network_events

```sql
CREATE TABLE brz_tel_network_events (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    event_id          VARCHAR(100),
    node_id           VARCHAR(100),
    event_type        VARCHAR(50),       -- outage, degradation, maintenance
    severity          VARCHAR(20),
    event_start       TIMESTAMP,
    event_end         TIMESTAMP,
    affected_cells    TEXT,
    description       TEXT,
    raw_payload       TEXT
);
```

### brz_tel_plans

```sql
CREATE TABLE brz_tel_plans (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    plan_id           VARCHAR(100),
    plan_name         VARCHAR(255),
    plan_type         VARCHAR(50),       -- prepaid, postpaid, enterprise
    monthly_fee       NUMERIC(20,4),
    data_quota_gb     NUMERIC(10,2),
    voice_minutes     INTEGER,
    sms_count         INTEGER,
    network_type      VARCHAR(20),
    is_active         BOOLEAN,
    raw_payload       TEXT
);
```

### brz_tel_billing

```sql
CREATE TABLE brz_tel_billing (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    bill_id           VARCHAR(100),
    subscriber_id     VARCHAR(100),
    billing_period    VARCHAR(20),
    bill_date         DATE,
    due_date          DATE,
    base_charge       NUMERIC(20,4),
    usage_charge      NUMERIC(20,4),
    roaming_charge    NUMERIC(20,4),
    tax               NUMERIC(20,4),
    total_amount      NUMERIC(20,4),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_tel_tower_inventory

```sql
CREATE TABLE brz_tel_tower_inventory (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    tower_id          VARCHAR(100),
    cell_id           VARCHAR(50),
    tower_type        VARCHAR(50),
    latitude          NUMERIC(10,7),
    longitude         NUMERIC(10,7),
    region            VARCHAR(100),
    network_type      VARCHAR(20),
    status            VARCHAR(50),
    install_date      DATE,
    operator_id       VARCHAR(100),
    raw_payload       TEXT
);
```

### brz_tel_complaints

```sql
CREATE TABLE brz_tel_complaints (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    complaint_id      VARCHAR(100),
    subscriber_id     VARCHAR(100),
    complaint_type    VARCHAR(100),
    channel           VARCHAR(50),       -- call_center, app, web, store
    submitted_at      TIMESTAMP,
    resolved_at       TIMESTAMP,
    resolution        TEXT,
    satisfaction_score INTEGER,
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_tel_roaming_agreements

```sql
CREATE TABLE brz_tel_roaming_agreements (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    agreement_id      VARCHAR(100),
    partner_operator  VARCHAR(255),
    country_code      CHAR(3),
    voice_rate        NUMERIC(10,6),
    data_rate_per_mb  NUMERIC(10,6),
    sms_rate          NUMERIC(10,6),
    effective_date    DATE,
    expiry_date       DATE,
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

---

## 📂 Sector 10 — Energy & Utilities

### brz_ene_meters

```sql
CREATE TABLE brz_ene_meters (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    meter_id          VARCHAR(100),
    meter_serial      VARCHAR(100),
    meter_type        VARCHAR(50),       -- electricity, gas, water
    customer_id       VARCHAR(100),
    service_point_id  VARCHAR(100),
    install_date      DATE,
    status            VARCHAR(50),
    latitude          NUMERIC(10, 7),
    longitude         NUMERIC(10, 7),
    raw_payload       TEXT
);
```

### brz_ene_meter_readings

```sql
CREATE TABLE brz_ene_meter_readings (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    reading_id        VARCHAR(100),
    meter_id          VARCHAR(100),
    reading_date      TIMESTAMP,
    reading_value     NUMERIC(15, 4),
    reading_unit      VARCHAR(20),       -- kWh, m3, liters
    reading_type      VARCHAR(20),       -- actual, estimated, customer
    quality_flag      VARCHAR(20),
    raw_payload       TEXT
);
```

### brz_ene_grid_events

```sql
CREATE TABLE brz_ene_grid_events (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    event_id          VARCHAR(100),
    substation_id     VARCHAR(100),
    event_type        VARCHAR(50),       -- outage, fault, overload, maintenance
    severity          VARCHAR(20),
    event_start       TIMESTAMP,
    event_end         TIMESTAMP,
    affected_customers INTEGER,
    cause_code        VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_ene_generation_assets

```sql
CREATE TABLE brz_ene_generation_assets (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    asset_id          VARCHAR(100),
    asset_name        VARCHAR(255),
    asset_type        VARCHAR(50),       -- solar, wind, hydro, gas, nuclear
    capacity_mw       NUMERIC(10, 3),
    location          VARCHAR(255),
    commission_date   DATE,
    status            VARCHAR(50),
    operator_id       VARCHAR(100),
    raw_payload       TEXT
);
```

### brz_ene_tariffs

```sql
CREATE TABLE brz_ene_tariffs (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    tariff_id         VARCHAR(100),
    tariff_name       VARCHAR(255),
    utility_type      VARCHAR(50),
    customer_class    VARCHAR(50),       -- residential, commercial, industrial
    effective_date    DATE,
    expiry_date       DATE,
    rate_per_unit     NUMERIC(15,6),
    unit              VARCHAR(20),
    fixed_charge      NUMERIC(20,4),
    is_tou            BOOLEAN,           -- time-of-use
    raw_payload       TEXT
);
```

### brz_ene_work_orders

```sql
CREATE TABLE brz_ene_work_orders (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    work_order_id     VARCHAR(100),
    order_type        VARCHAR(50),       -- installation, repair, inspection, upgrade
    asset_id          VARCHAR(100),
    priority          VARCHAR(20),
    assigned_to       VARCHAR(100),
    scheduled_date    DATE,
    completed_date    DATE,
    cost              NUMERIC(20,4),
    status            VARCHAR(50),
    notes             TEXT,
    raw_payload       TEXT
);
```

### brz_ene_renewable_output

```sql
CREATE TABLE brz_ene_renewable_output (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    output_id         VARCHAR(100),
    asset_id          VARCHAR(100),
    reading_timestamp TIMESTAMP,
    output_mwh        NUMERIC(15,6),
    capacity_factor   NUMERIC(8,4),
    weather_condition VARCHAR(50),
    irradiance        NUMERIC(10,4),     -- for solar (W/m2)
    wind_speed_ms     NUMERIC(8,2),      -- for wind
    raw_payload       TEXT
);
```

### brz_ene_customer_accounts

```sql
CREATE TABLE brz_ene_customer_accounts (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    account_id        VARCHAR(100),
    customer_id       VARCHAR(100),
    tariff_id         VARCHAR(100),
    service_type      VARCHAR(50),
    address_line1     TEXT,
    city              VARCHAR(100),
    country           VARCHAR(100),
    start_date        DATE,
    end_date          DATE,
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_ene_bills

```sql
CREATE TABLE brz_ene_bills (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    bill_id           VARCHAR(100),
    account_id        VARCHAR(100),
    bill_date         DATE,
    due_date          DATE,
    consumption_units NUMERIC(15,4),
    unit_rate         NUMERIC(15,6),
    energy_charge     NUMERIC(20,4),
    fixed_charge      NUMERIC(20,4),
    tax               NUMERIC(20,4),
    total_amount      NUMERIC(20,4),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

---

## 📂 Sector 11 — Agriculture

### brz_agr_farms

```sql
CREATE TABLE brz_agr_farms (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    farm_id           VARCHAR(100),
    farm_name         VARCHAR(255),
    owner_id          VARCHAR(100),
    total_area_ha     NUMERIC(15, 4),
    address           TEXT,
    region            VARCHAR(100),
    country           VARCHAR(100),
    latitude          NUMERIC(10, 7),
    longitude         NUMERIC(10, 7),
    primary_crop      VARCHAR(100),
    certification     VARCHAR(100),      -- organic, GAP, etc.
    raw_payload       TEXT
);
```

### brz_agr_crop_cycles

```sql
CREATE TABLE brz_agr_crop_cycles (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    cycle_id          VARCHAR(100),
    farm_id           VARCHAR(100),
    field_id          VARCHAR(100),
    crop_id           VARCHAR(100),
    crop_variety      VARCHAR(100),
    planting_date     DATE,
    harvest_date      DATE,
    area_planted_ha   NUMERIC(15, 4),
    yield_kg          NUMERIC(15, 3),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_agr_field_sensors

```sql
CREATE TABLE brz_agr_field_sensors (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    sensor_id         VARCHAR(100),
    farm_id           VARCHAR(100),
    field_id          VARCHAR(100),
    sensor_type       VARCHAR(50),       -- soil_moisture, temperature, humidity, ph
    recorded_at       TIMESTAMP,
    value             NUMERIC(15, 6),
    unit              VARCHAR(20),
    battery_level     NUMERIC(5, 2),
    raw_payload       TEXT
);
```

### brz_agr_inputs_applied

```sql
CREATE TABLE brz_agr_inputs_applied (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    application_id    VARCHAR(100),
    cycle_id          VARCHAR(100),
    field_id          VARCHAR(100),
    input_type        VARCHAR(50),       -- fertilizer, pesticide, herbicide, water
    product_name      VARCHAR(255),
    quantity_applied  NUMERIC(15, 4),
    uom               VARCHAR(20),
    application_date  DATE,
    applicator_id     VARCHAR(100),
    raw_payload       TEXT
);
```

### brz_agr_livestock

```sql
CREATE TABLE brz_agr_livestock (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    animal_id         VARCHAR(100),
    farm_id           VARCHAR(100),
    species           VARCHAR(50),
    breed             VARCHAR(100),
    date_of_birth     DATE,
    gender            VARCHAR(10),
    weight_kg         NUMERIC(8,2),
    health_status     VARCHAR(50),
    tag_number        VARCHAR(50),
    acquired_date     DATE,
    raw_payload       TEXT
);
```

### brz_agr_weather_observations

```sql
CREATE TABLE brz_agr_weather_observations (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    observation_id    VARCHAR(100),
    farm_id           VARCHAR(100),
    station_id        VARCHAR(100),
    observed_at       TIMESTAMP,
    temp_max_c        NUMERIC(6,2),
    temp_min_c        NUMERIC(6,2),
    rainfall_mm       NUMERIC(8,2),
    humidity_pct      NUMERIC(6,2),
    wind_speed_ms     NUMERIC(8,2),
    solar_rad         NUMERIC(10,4),
    raw_payload       TEXT
);
```

### brz_agr_pest_disease_reports

```sql
CREATE TABLE brz_agr_pest_disease_reports (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    report_id         VARCHAR(100),
    farm_id           VARCHAR(100),
    field_id          VARCHAR(100),
    report_date       DATE,
    pest_disease_name VARCHAR(255),
    category          VARCHAR(50),       -- pest, disease, weed
    severity          VARCHAR(20),
    affected_area_ha  NUMERIC(10,4),
    treatment_applied TEXT,
    raw_payload       TEXT
);
```

### brz_agr_equipment

```sql
CREATE TABLE brz_agr_equipment (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    equipment_id      VARCHAR(100),
    farm_id           VARCHAR(100),
    equipment_type    VARCHAR(50),       -- tractor, harvester, irrigator, sprayer
    brand             VARCHAR(100),
    model             VARCHAR(100),
    year              INTEGER,
    status            VARCHAR(50),
    last_service_date DATE,
    raw_payload       TEXT
);
```

### brz_agr_market_prices

```sql
CREATE TABLE brz_agr_market_prices (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    price_id          VARCHAR(100),
    crop_id           VARCHAR(100),
    market_name       VARCHAR(100),
    price_date        DATE,
    price_per_kg      NUMERIC(15,4),
    currency_code     VARCHAR(10),
    price_type        VARCHAR(30),       -- farm_gate, wholesale, retail
    raw_payload       TEXT
);
```

---

## 📂 Sector 12 — Transportation

### brz_trn_routes

```sql
CREATE TABLE brz_trn_routes (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    route_id          VARCHAR(100),
    route_code        VARCHAR(50),
    route_name        VARCHAR(255),
    transport_mode    VARCHAR(50),       -- bus, rail, air, sea, metro
    origin_code       VARCHAR(50),
    destination_code  VARCHAR(50),
    distance_km       NUMERIC(10, 2),
    estimated_minutes INTEGER,
    is_active         BOOLEAN,
    raw_payload       TEXT
);
```

### brz_trn_trips

```sql
CREATE TABLE brz_trn_trips (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    trip_id           VARCHAR(100),
    route_id          VARCHAR(100),
    vehicle_id        VARCHAR(100),
    driver_id         VARCHAR(100),
    scheduled_departure TIMESTAMP,
    actual_departure  TIMESTAMP,
    scheduled_arrival TIMESTAMP,
    actual_arrival    TIMESTAMP,
    status            VARCHAR(50),
    passengers_count  INTEGER,
    raw_payload       TEXT
);
```

### brz_trn_tickets

```sql
CREATE TABLE brz_trn_tickets (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    ticket_id         VARCHAR(100),
    trip_id           VARCHAR(100),
    passenger_id      VARCHAR(100),
    ticket_class      VARCHAR(50),
    seat_number       VARCHAR(20),
    fare_amount       NUMERIC(20, 4),
    currency_code     VARCHAR(10),
    booking_date      TIMESTAMP,
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_trn_vehicle_gps

```sql
CREATE TABLE brz_trn_vehicle_gps (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    gps_id            VARCHAR(100),
    vehicle_id        VARCHAR(100),
    trip_id           VARCHAR(100),
    recorded_at       TIMESTAMP,
    latitude          NUMERIC(10, 7),
    longitude         NUMERIC(10, 7),
    speed_kmh         NUMERIC(8, 2),
    heading_degrees   NUMERIC(6, 2),
    raw_payload       TEXT
);
```

### brz_trn_drivers

```sql
CREATE TABLE brz_trn_drivers (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    driver_id         VARCHAR(100),
    first_name        VARCHAR(100),
    last_name         VARCHAR(100),
    license_number    VARCHAR(100),
    license_class     VARCHAR(20),
    license_expiry    DATE,
    date_of_birth     DATE,
    hire_date         DATE,
    status            VARCHAR(50),
    carrier_id        VARCHAR(100),
    raw_payload       TEXT
);
```

### brz_trn_incidents

```sql
CREATE TABLE brz_trn_incidents (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    incident_id       VARCHAR(100),
    trip_id           VARCHAR(100),
    vehicle_id        VARCHAR(100),
    driver_id         VARCHAR(100),
    incident_type     VARCHAR(50),       -- accident, breakdown, delay, infraction
    incident_date     TIMESTAMP,
    latitude          NUMERIC(10,7),
    longitude         NUMERIC(10,7),
    severity          VARCHAR(20),
    description       TEXT,
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_trn_stops

```sql
CREATE TABLE brz_trn_stops (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    stop_id           VARCHAR(100),
    stop_name         VARCHAR(255),
    stop_type         VARCHAR(50),       -- origin, intermediate, terminal
    route_id          VARCHAR(100),
    sequence_no       INTEGER,
    latitude          NUMERIC(10,7),
    longitude         NUMERIC(10,7),
    scheduled_time    TIME,
    is_active         BOOLEAN,
    raw_payload       TEXT
);
```

### brz_trn_fuel_logs

```sql
CREATE TABLE brz_trn_fuel_logs (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    log_id            VARCHAR(100),
    vehicle_id        VARCHAR(100),
    trip_id           VARCHAR(100),
    fill_date         DATE,
    liters_filled     NUMERIC(10,3),
    cost_per_liter    NUMERIC(10,4),
    total_cost        NUMERIC(20,4),
    odometer_km       NUMERIC(12,2),
    station_id        VARCHAR(100),
    raw_payload       TEXT
);
```

### brz_trn_passenger_feedback

```sql
CREATE TABLE brz_trn_passenger_feedback (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    feedback_id       VARCHAR(100),
    trip_id           VARCHAR(100),
    passenger_id      VARCHAR(100),
    submitted_at      TIMESTAMP,
    rating            SMALLINT,
    punctuality_score SMALLINT,
    cleanliness_score SMALLINT,
    staff_score       SMALLINT,
    comments          TEXT,
    raw_payload       TEXT
);
```

---

## 📂 Sector 13 — Real Estate

### brz_re_properties

```sql
CREATE TABLE brz_re_properties (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    property_id       VARCHAR(100),
    property_code     VARCHAR(50),
    property_type     VARCHAR(50),       -- residential, commercial, industrial, land
    address_line1     TEXT,
    city              VARCHAR(100),
    region            VARCHAR(100),
    country           VARCHAR(100),
    latitude          NUMERIC(10, 7),
    longitude         NUMERIC(10, 7),
    land_area_sqm     NUMERIC(15, 4),
    floor_area_sqm    NUMERIC(15, 4),
    year_built        INTEGER,
    status            VARCHAR(50),
    owner_id          VARCHAR(100),
    raw_payload       TEXT
);
```

### brz_re_listings

```sql
CREATE TABLE brz_re_listings (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    listing_id        VARCHAR(100),
    property_id       VARCHAR(100),
    listing_type      VARCHAR(20),       -- sale, rent
    asking_price      NUMERIC(20, 4),
    currency_code     VARCHAR(10),
    listing_date      DATE,
    expiry_date       DATE,
    status            VARCHAR(50),
    agent_id          VARCHAR(100),
    description       TEXT,
    raw_payload       TEXT
);
```

### brz_re_transactions

```sql
CREATE TABLE brz_re_transactions (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    transaction_id    VARCHAR(100),
    property_id       VARCHAR(100),
    listing_id        VARCHAR(100),
    transaction_type  VARCHAR(20),       -- sale, lease
    buyer_id          VARCHAR(100),
    seller_id         VARCHAR(100),
    transaction_date  DATE,
    sale_price        NUMERIC(20, 4),
    currency_code     VARCHAR(10),
    agent_id          VARCHAR(100),
    raw_payload       TEXT
);
```

### brz_re_leases

```sql
CREATE TABLE brz_re_leases (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    lease_id          VARCHAR(100),
    property_id       VARCHAR(100),
    tenant_id         VARCHAR(100),
    landlord_id       VARCHAR(100),
    lease_start       DATE,
    lease_end         DATE,
    monthly_rent      NUMERIC(20, 4),
    currency_code     VARCHAR(10),
    deposit_amount    NUMERIC(20, 4),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_re_agents

```sql
CREATE TABLE brz_re_agents (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    agent_id          VARCHAR(100),
    first_name        VARCHAR(100),
    last_name         VARCHAR(100),
    license_number    VARCHAR(100),
    agency_id         VARCHAR(100),
    email             VARCHAR(255),
    phone             VARCHAR(50),
    specialization    VARCHAR(100),
    active_since      DATE,
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_re_valuations

```sql
CREATE TABLE brz_re_valuations (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    valuation_id      VARCHAR(100),
    property_id       VARCHAR(100),
    valuation_date    DATE,
    valuation_method  VARCHAR(50),       -- market, income, cost
    appraised_value   NUMERIC(20,4),
    currency_code     VARCHAR(10),
    appraiser_id      VARCHAR(100),
    purpose           VARCHAR(50),       -- sale, refinance, insurance, tax
    raw_payload       TEXT
);
```

### brz_re_maintenance_requests

```sql
CREATE TABLE brz_re_maintenance_requests (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    request_id        VARCHAR(100),
    property_id       VARCHAR(100),
    tenant_id         VARCHAR(100),
    category          VARCHAR(50),       -- plumbing, electrical, structural, hvac
    description       TEXT,
    priority          VARCHAR(20),
    submitted_at      TIMESTAMP,
    resolved_at       TIMESTAMP,
    cost              NUMERIC(20,4),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_re_inspections

```sql
CREATE TABLE brz_re_inspections (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    inspection_id     VARCHAR(100),
    property_id       VARCHAR(100),
    inspection_type   VARCHAR(50),       -- pre_sale, pre_lease, routine, final
    inspector_id      VARCHAR(100),
    inspection_date   DATE,
    overall_condition VARCHAR(20),
    notes             TEXT,
    report_url        TEXT,
    raw_payload       TEXT
);
```

### brz_re_mortgages

```sql
CREATE TABLE brz_re_mortgages (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    mortgage_id       VARCHAR(100),
    property_id       VARCHAR(100),
    borrower_id       VARCHAR(100),
    lender_id         VARCHAR(100),
    principal         NUMERIC(20,4),
    interest_rate     NUMERIC(8,4),
    term_years        INTEGER,
    start_date        DATE,
    maturity_date     DATE,
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

---

## 📂 Sector 14 — Human Resources

### brz_hr_employees

```sql
CREATE TABLE brz_hr_employees (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    employee_id       VARCHAR(100),
    employee_number   VARCHAR(50),
    first_name        VARCHAR(100),
    last_name         VARCHAR(100),
    date_of_birth     DATE,
    gender            VARCHAR(20),
    national_id       VARCHAR(100),
    email             VARCHAR(255),
    phone             VARCHAR(50),
    hire_date         DATE,
    termination_date  DATE,
    department_id     VARCHAR(100),
    job_id            VARCHAR(100),
    manager_id        VARCHAR(100),
    employment_type   VARCHAR(50),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_hr_payroll

```sql
CREATE TABLE brz_hr_payroll (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    payroll_id        VARCHAR(100),
    employee_id       VARCHAR(100),
    pay_period_start  DATE,
    pay_period_end    DATE,
    basic_salary      NUMERIC(20, 4),
    allowances        NUMERIC(20, 4),
    overtime          NUMERIC(20, 4),
    gross_pay         NUMERIC(20, 4),
    deductions        NUMERIC(20, 4),
    net_pay           NUMERIC(20, 4),
    currency_code     VARCHAR(10),
    payment_date      DATE,
    raw_payload       TEXT
);
```

### brz_hr_attendance

```sql
CREATE TABLE brz_hr_attendance (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    attendance_id     VARCHAR(100),
    employee_id       VARCHAR(100),
    work_date         DATE,
    time_in           TIMESTAMP,
    time_out          TIMESTAMP,
    hours_worked      NUMERIC(6, 2),
    overtime_hours    NUMERIC(6, 2),
    status            VARCHAR(50),       -- present, absent, leave, holiday
    raw_payload       TEXT
);
```

### brz_hr_performance_reviews

```sql
CREATE TABLE brz_hr_performance_reviews (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    review_id         VARCHAR(100),
    employee_id       VARCHAR(100),
    reviewer_id       VARCHAR(100),
    review_period     VARCHAR(50),
    review_date       DATE,
    overall_rating    NUMERIC(4, 2),
    goals_rating      NUMERIC(4, 2),
    competency_rating NUMERIC(4, 2),
    comments          TEXT,
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_hr_job_postings

```sql
CREATE TABLE brz_hr_job_postings (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    posting_id        VARCHAR(100),
    job_title         VARCHAR(255),
    department_id     VARCHAR(100),
    location          VARCHAR(255),
    employment_type   VARCHAR(50),
    salary_min        NUMERIC(20, 4),
    salary_max        NUMERIC(20, 4),
    currency_code     VARCHAR(10),
    posted_date       DATE,
    closing_date      DATE,
    status            VARCHAR(50),
    description       TEXT,
    raw_payload       TEXT
);
```

### brz_hr_training

```sql
CREATE TABLE brz_hr_training (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    training_id       VARCHAR(100),
    employee_id       VARCHAR(100),
    course_name       VARCHAR(255),
    training_type     VARCHAR(50),       -- onboarding, compliance, skills, leadership
    provider          VARCHAR(100),
    start_date        DATE,
    end_date          DATE,
    duration_hours    NUMERIC(6,2),
    status            VARCHAR(50),
    score             NUMERIC(6,2),
    certified         BOOLEAN,
    raw_payload       TEXT
);
```

### brz_hr_benefits

```sql
CREATE TABLE brz_hr_benefits (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    enrollment_id     VARCHAR(100),
    employee_id       VARCHAR(100),
    benefit_type      VARCHAR(50),       -- health, dental, life, pension, stock
    plan_name         VARCHAR(255),
    start_date        DATE,
    end_date          DATE,
    employee_contrib  NUMERIC(20,4),
    employer_contrib  NUMERIC(20,4),
    currency_code     VARCHAR(10),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_hr_disciplinary

```sql
CREATE TABLE brz_hr_disciplinary (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    case_id           VARCHAR(100),
    employee_id       VARCHAR(100),
    incident_date     DATE,
    incident_type     VARCHAR(100),
    severity          VARCHAR(20),
    action_taken      VARCHAR(100),
    issued_by         VARCHAR(100),
    issued_date       DATE,
    appeal_status     VARCHAR(50),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_hr_offboarding

```sql
CREATE TABLE brz_hr_offboarding (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    offboarding_id    VARCHAR(100),
    employee_id       VARCHAR(100),
    notice_date       DATE,
    last_day          DATE,
    exit_reason       VARCHAR(100),      -- voluntary, involuntary, retirement, contract_end
    exit_interview    BOOLEAN,
    rehire_eligible   BOOLEAN,
    clearance_status  VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_hr_org_structure

```sql
CREATE TABLE brz_hr_org_structure (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    node_id           VARCHAR(100),
    node_type         VARCHAR(50),       -- company, division, department, team
    node_name         VARCHAR(255),
    parent_node_id    VARCHAR(100),
    level             INTEGER,
    cost_center       VARCHAR(100),
    head_employee_id  VARCHAR(100),
    effective_date    DATE,
    raw_payload       TEXT
);
```

---

## 📂 Sector 15 — Insurance

### brz_ins_policies

```sql
CREATE TABLE brz_ins_policies (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    policy_id         VARCHAR(100),
    policy_number     VARCHAR(50),
    policyholder_id   VARCHAR(100),
    product_id        VARCHAR(100),
    policy_type       VARCHAR(50),       -- life, health, auto, property, liability
    status            VARCHAR(50),
    start_date        DATE,
    end_date          DATE,
    premium_amount    NUMERIC(20, 4),
    sum_assured       NUMERIC(20, 4),
    currency_code     VARCHAR(10),
    agent_id          VARCHAR(100),
    raw_payload       TEXT
);
```

### brz_ins_claims

```sql
CREATE TABLE brz_ins_claims (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    claim_id          VARCHAR(100),
    claim_number      VARCHAR(50),
    policy_id         VARCHAR(100),
    claimant_id       VARCHAR(100),
    incident_date     DATE,
    reported_date     DATE,
    claim_type        VARCHAR(50),
    claimed_amount    NUMERIC(20, 4),
    approved_amount   NUMERIC(20, 4),
    status            VARCHAR(50),
    adjuster_id       VARCHAR(100),
    currency_code     VARCHAR(10),
    raw_payload       TEXT
);
```

### brz_ins_premium_payments

```sql
CREATE TABLE brz_ins_premium_payments (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    payment_id        VARCHAR(100),
    policy_id         VARCHAR(100),
    due_date          DATE,
    payment_date      DATE,
    amount_due        NUMERIC(20, 4),
    amount_paid       NUMERIC(20, 4),
    payment_method    VARCHAR(50),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_ins_underwriting

```sql
CREATE TABLE brz_ins_underwriting (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    underwriting_id   VARCHAR(100),
    application_id    VARCHAR(100),
    applicant_id      VARCHAR(100),
    product_id        VARCHAR(100),
    risk_score        NUMERIC(8, 4),
    decision          VARCHAR(20),       -- approved, declined, referred
    decision_date     DATE,
    underwriter_id    VARCHAR(100),
    notes             TEXT,
    raw_payload       TEXT
);
```

### brz_ins_reinsurance

```sql
CREATE TABLE brz_ins_reinsurance (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    treaty_id         VARCHAR(100),
    reinsurer_name    VARCHAR(255),
    treaty_type       VARCHAR(50),       -- quota_share, excess_of_loss, proportional
    line_of_business  VARCHAR(100),
    start_date        DATE,
    end_date          DATE,
    cession_pct       NUMERIC(8,4),
    max_liability     NUMERIC(20,4),
    currency_code     VARCHAR(10),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_ins_agents

```sql
CREATE TABLE brz_ins_agents (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    agent_id          VARCHAR(100),
    first_name        VARCHAR(100),
    last_name         VARCHAR(100),
    license_number    VARCHAR(100),
    license_expiry    DATE,
    agency_id         VARCHAR(100),
    channel           VARCHAR(50),       -- tied, broker, bancassurance, direct
    email             VARCHAR(255),
    phone             VARCHAR(50),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_ins_commission

```sql
CREATE TABLE brz_ins_commission (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    commission_id     VARCHAR(100),
    agent_id          VARCHAR(100),
    policy_id         VARCHAR(100),
    commission_type   VARCHAR(50),       -- new_business, renewal, override
    commission_rate   NUMERIC(8,4),
    premium_amount    NUMERIC(20,4),
    commission_amount NUMERIC(20,4),
    period_start      DATE,
    period_end        DATE,
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_ins_risk_assessments

```sql
CREATE TABLE brz_ins_risk_assessments (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    assessment_id     VARCHAR(100),
    policy_id         VARCHAR(100),
    risk_type         VARCHAR(50),
    assessed_by       VARCHAR(100),
    assessed_at       TIMESTAMP,
    risk_score        NUMERIC(8,4),
    risk_category     VARCHAR(20),       -- low, medium, high, very_high
    factors           TEXT,
    notes             TEXT,
    raw_payload       TEXT
);
```

### brz_ins_beneficiaries

```sql
CREATE TABLE brz_ins_beneficiaries (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    beneficiary_id    VARCHAR(100),
    policy_id         VARCHAR(100),
    first_name        VARCHAR(100),
    last_name         VARCHAR(100),
    relationship      VARCHAR(50),
    allocation_pct    NUMERIC(6,2),
    date_of_birth     DATE,
    national_id       VARCHAR(100),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

---

## 📂 Sector 16 — Cybersecurity

### brz_sec_security_events

```sql
CREATE TABLE brz_sec_security_events (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    event_id          VARCHAR(100),
    event_type        VARCHAR(100),      -- login_failure, port_scan, malware_detected
    severity          VARCHAR(20),       -- low, medium, high, critical
    source_ip         VARCHAR(50),
    destination_ip    VARCHAR(50),
    source_port       INTEGER,
    destination_port  INTEGER,
    protocol          VARCHAR(20),
    user_id           VARCHAR(100),
    host_id           VARCHAR(100),
    event_timestamp   TIMESTAMP,
    raw_log           TEXT,
    raw_payload       TEXT
);
```

### brz_sec_vulnerabilities

```sql
CREATE TABLE brz_sec_vulnerabilities (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    vuln_id           VARCHAR(100),
    cve_id            VARCHAR(50),
    asset_id          VARCHAR(100),
    severity          VARCHAR(20),
    cvss_score        NUMERIC(4, 1),
    description       TEXT,
    discovered_date   DATE,
    remediated_date   DATE,
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_sec_assets

```sql
CREATE TABLE brz_sec_assets (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    asset_id          VARCHAR(100),
    hostname          VARCHAR(255),
    ip_address        VARCHAR(50),
    mac_address       VARCHAR(50),
    asset_type        VARCHAR(50),       -- server, endpoint, network_device, cloud
    os                VARCHAR(100),
    os_version        VARCHAR(100),
    owner_id          VARCHAR(100),
    criticality       VARCHAR(20),
    last_seen         TIMESTAMP,
    raw_payload       TEXT
);
```

### brz_sec_access_logs

```sql
CREATE TABLE brz_sec_access_logs (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    log_id            VARCHAR(100),
    user_id           VARCHAR(100),
    resource_id       VARCHAR(100),
    action            VARCHAR(50),       -- read, write, delete, execute
    result            VARCHAR(20),       -- success, failure
    ip_address        VARCHAR(50),
    user_agent        TEXT,
    access_timestamp  TIMESTAMP,
    session_id        VARCHAR(100),
    raw_payload       TEXT
);
```

### brz_sec_incidents

```sql
CREATE TABLE brz_sec_incidents (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    incident_id       VARCHAR(100),
    title             VARCHAR(255),
    incident_type     VARCHAR(100),
    severity          VARCHAR(20),
    status            VARCHAR(50),
    detected_at       TIMESTAMP,
    resolved_at       TIMESTAMP,
    affected_assets   TEXT,
    assigned_to       VARCHAR(100),
    description       TEXT,
    raw_payload       TEXT
);
```

### brz_sec_threat_intelligence

```sql
CREATE TABLE brz_sec_threat_intelligence (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    intel_id          VARCHAR(100),
    indicator_type    VARCHAR(50),       -- ip, domain, hash, url, email
    indicator_value   TEXT,
    threat_category   VARCHAR(100),
    confidence_score  NUMERIC(5,2),
    severity          VARCHAR(20),
    source_feed       VARCHAR(100),
    first_seen        TIMESTAMP,
    last_seen         TIMESTAMP,
    is_active         BOOLEAN,
    raw_payload       TEXT
);
```

### brz_sec_patch_management

```sql
CREATE TABLE brz_sec_patch_management (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    patch_id          VARCHAR(100),
    asset_id          VARCHAR(100),
    patch_name        VARCHAR(255),
    cve_id            VARCHAR(50),
    severity          VARCHAR(20),
    released_date     DATE,
    applied_date      DATE,
    applied_by        VARCHAR(100),
    status            VARCHAR(50),       -- pending, applied, failed, waived
    raw_payload       TEXT
);
```

### brz_sec_user_accounts

```sql
CREATE TABLE brz_sec_user_accounts (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    account_id        VARCHAR(100),
    username          VARCHAR(100),
    email             VARCHAR(255),
    department_id     VARCHAR(100),
    role              VARCHAR(100),
    privilege_level   VARCHAR(20),
    mfa_enabled       BOOLEAN,
    last_login        TIMESTAMP,
    password_last_set DATE,
    is_locked         BOOLEAN,
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_sec_network_flows

```sql
CREATE TABLE brz_sec_network_flows (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    flow_id           VARCHAR(100),
    src_ip            VARCHAR(50),
    dst_ip            VARCHAR(50),
    src_port          INTEGER,
    dst_port          INTEGER,
    protocol          VARCHAR(20),
    start_time        TIMESTAMP,
    end_time          TIMESTAMP,
    bytes_sent        BIGINT,
    bytes_received    BIGINT,
    packets_sent      BIGINT,
    action            VARCHAR(20),       -- allow, deny, drop
    raw_payload       TEXT
);
```

### brz_sec_compliance_checks

```sql
CREATE TABLE brz_sec_compliance_checks (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    check_id          VARCHAR(100),
    asset_id          VARCHAR(100),
    framework         VARCHAR(50),       -- ISO27001, PCI-DSS, HIPAA, SOC2, NIST
    control_id        VARCHAR(50),
    control_name      VARCHAR(255),
    check_date        DATE,
    result            VARCHAR(20),       -- pass, fail, na
    evidence          TEXT,
    reviewed_by       VARCHAR(100),
    raw_payload       TEXT
);
```

---

## 📂 Sector 17 — Education

### brz_edu_students

```sql
CREATE TABLE brz_edu_students (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    student_id        VARCHAR(100),
    student_number    VARCHAR(50),
    first_name        VARCHAR(100),
    last_name         VARCHAR(100),
    date_of_birth     DATE,
    gender            VARCHAR(20),
    email             VARCHAR(255),
    phone             VARCHAR(50),
    enrolled_date     DATE,
    graduation_date   DATE,
    program_id        VARCHAR(100),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_edu_courses

```sql
CREATE TABLE brz_edu_courses (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    course_id         VARCHAR(100),
    course_code       VARCHAR(50),
    course_name       VARCHAR(255),
    department_id     VARCHAR(100),
    credit_hours      NUMERIC(4, 1),
    level             VARCHAR(50),       -- undergraduate, graduate, certificate
    description       TEXT,
    is_active         BOOLEAN,
    raw_payload       TEXT
);
```

### brz_edu_enrollments

```sql
CREATE TABLE brz_edu_enrollments (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    enrollment_id     VARCHAR(100),
    student_id        VARCHAR(100),
    course_id         VARCHAR(100),
    section_id        VARCHAR(100),
    term_id           VARCHAR(100),
    enrollment_date   DATE,
    status            VARCHAR(50),       -- active, dropped, completed
    raw_payload       TEXT
);
```

### brz_edu_grades

```sql
CREATE TABLE brz_edu_grades (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    grade_id          VARCHAR(100),
    enrollment_id     VARCHAR(100),
    student_id        VARCHAR(100),
    course_id         VARCHAR(100),
    term_id           VARCHAR(100),
    assessment_type   VARCHAR(50),       -- exam, quiz, assignment, project
    score             NUMERIC(6, 2),
    max_score         NUMERIC(6, 2),
    letter_grade      VARCHAR(5),
    graded_at         TIMESTAMP,
    raw_payload       TEXT
);
```

### brz_edu_instructors

```sql
CREATE TABLE brz_edu_instructors (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    instructor_id     VARCHAR(100),
    employee_id       VARCHAR(100),
    first_name        VARCHAR(100),
    last_name         VARCHAR(100),
    email             VARCHAR(255),
    department_id     VARCHAR(100),
    rank              VARCHAR(100),      -- professor, associate, assistant, lecturer
    hire_date         DATE,
    tenure_status     VARCHAR(50),
    is_active         BOOLEAN,
    raw_payload       TEXT
);
```

### brz_edu_attendance

```sql
CREATE TABLE brz_edu_attendance (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    attendance_id     VARCHAR(100),
    enrollment_id     VARCHAR(100),
    student_id        VARCHAR(100),
    section_id        VARCHAR(100),
    class_date        DATE,
    status            VARCHAR(20),       -- present, absent, late, excused
    raw_payload       TEXT
);
```

### brz_edu_programs

```sql
CREATE TABLE brz_edu_programs (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    program_id        VARCHAR(100),
    program_name      VARCHAR(255),
    program_code      VARCHAR(50),
    degree_type       VARCHAR(50),       -- bachelor, master, doctorate, certificate
    department_id     VARCHAR(100),
    duration_years    NUMERIC(4,1),
    credit_hours      INTEGER,
    is_active         BOOLEAN,
    accreditation     VARCHAR(100),
    raw_payload       TEXT
);
```

### brz_edu_scholarships

```sql
CREATE TABLE brz_edu_scholarships (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    scholarship_id    VARCHAR(100),
    student_id        VARCHAR(100),
    scholarship_name  VARCHAR(255),
    scholarship_type  VARCHAR(50),       -- merit, need_based, athletic, grant
    amount            NUMERIC(20,4),
    currency_code     VARCHAR(10),
    academic_year     INTEGER,
    term_id           VARCHAR(100),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_edu_fees

```sql
CREATE TABLE brz_edu_fees (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    fee_id            VARCHAR(100),
    student_id        VARCHAR(100),
    fee_type          VARCHAR(50),       -- tuition, lab, library, accommodation
    term_id           VARCHAR(100),
    amount            NUMERIC(20,4),
    currency_code     VARCHAR(10),
    due_date          DATE,
    paid_date         DATE,
    paid_amount       NUMERIC(20,4),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_edu_library

```sql
CREATE TABLE brz_edu_library (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    transaction_id    VARCHAR(100),
    student_id        VARCHAR(100),
    item_id           VARCHAR(100),
    item_type         VARCHAR(50),       -- book, journal, digital, equipment
    borrow_date       DATE,
    due_date          DATE,
    return_date       DATE,
    fine_amount       NUMERIC(10,4),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

### brz_edu_departments

```sql
CREATE TABLE brz_edu_departments (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    department_id     VARCHAR(100),
    department_name   VARCHAR(255),
    faculty           VARCHAR(100),
    head_instructor   VARCHAR(100),
    budget            NUMERIC(20,4),
    established_year  INTEGER,
    is_active         BOOLEAN,
    raw_payload       TEXT
);
```

### brz_edu_extracurricular

```sql
CREATE TABLE brz_edu_extracurricular (
    _row_id           BIGSERIAL PRIMARY KEY,
    _ingested_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    _source_system    VARCHAR(100),
    _batch_id         VARCHAR(100),
    _is_deleted       BOOLEAN DEFAULT FALSE,

    record_id         VARCHAR(100),
    student_id        VARCHAR(100),
    activity_name     VARCHAR(255),
    activity_type     VARCHAR(50),       -- sport, club, volunteer, arts
    academic_year     INTEGER,
    role              VARCHAR(100),
    hours_per_week    NUMERIC(5,2),
    status            VARCHAR(50),
    raw_payload       TEXT
);
```

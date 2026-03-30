# 🥈 Medallion Architecture — Silver Layer (Cleaned & Validated)

> **Layer:** Silver (Conformed)
> **Purpose:** Cleaned, deduplicated, type-cast, null-handled, and validated data ready for business use.
> **Conventions:**
>
> - All tables prefixed with `slv_`
> - `_source_row_id` — FK back to Bronze `_row_id`
> - `_dedup_key` — business natural key used for deduplication
> - `_is_valid` — row passed all validation rules
> - `_validation_errors` — pipe-delimited list of failed rules
> - `_valid_from` / `_valid_to` — SCD Type 2 support
> - `_processed_at` — when Silver pipeline ran
> - All amounts are `NUMERIC(20,4)`, dates are `DATE`, timestamps are `TIMESTAMP`
> - NULLs replaced with sensible defaults where appropriate

---

## 📂 Sector 1 — Finance

### slv_fin_accounts

```sql
CREATE TABLE slv_fin_accounts (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- account_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    account_id            VARCHAR(100) NOT NULL,
    account_number        VARCHAR(50) NOT NULL,
    account_name          VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    account_type          VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    customer_id           VARCHAR(100),
    branch_id             VARCHAR(100),
    opened_date           DATE,
    closed_date           DATE
);
```

### slv_fin_transactions

```sql
CREATE TABLE slv_fin_transactions (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- transaction_id + account_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    transaction_id        VARCHAR(100) NOT NULL,
    account_id            VARCHAR(100) NOT NULL,
    transaction_date      TIMESTAMP NOT NULL,
    value_date            DATE,
    amount                NUMERIC(20,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    transaction_type      VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    description           TEXT NOT NULL DEFAULT '',
    reference_no          VARCHAR(100),
    channel               VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    merchant_id           VARCHAR(100),
    status                VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN'
);
```

### slv_fin_customers

```sql
CREATE TABLE slv_fin_customers (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- customer_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    customer_id           VARCHAR(100) NOT NULL,
    first_name            VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    last_name             VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    date_of_birth         DATE,
    national_id           VARCHAR(100),
    email                 VARCHAR(255),
    phone                 VARCHAR(50),
    city                  VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    country               CHAR(2) NOT NULL DEFAULT 'XX',
    kyc_status            VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    risk_rating           VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    segment               VARCHAR(50) NOT NULL DEFAULT 'RETAIL',
    created_at            TIMESTAMP
);
```

### slv_fin_loans

```sql
CREATE TABLE slv_fin_loans (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    loan_id               VARCHAR(100) NOT NULL,
    customer_id           VARCHAR(100) NOT NULL,
    loan_type             VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    principal_amount      NUMERIC(20,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    interest_rate         NUMERIC(8,4) NOT NULL DEFAULT 0,
    term_months           INTEGER NOT NULL DEFAULT 0,
    disbursement_date     DATE,
    maturity_date         DATE,
    status                VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    outstanding_balance   NUMERIC(20,4) NOT NULL DEFAULT 0
);
```

### slv_fin_market_prices

```sql
CREATE TABLE slv_fin_market_prices (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- ticker_symbol + price_date
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    ticker_symbol         VARCHAR(20) NOT NULL,
    exchange              VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    price_date            DATE NOT NULL,
    open_price            NUMERIC(20,6) NOT NULL DEFAULT 0,
    close_price           NUMERIC(20,6) NOT NULL DEFAULT 0,
    high_price            NUMERIC(20,6) NOT NULL DEFAULT 0,
    low_price             NUMERIC(20,6) NOT NULL DEFAULT 0,
    volume                BIGINT NOT NULL DEFAULT 0,
    adjusted_close        NUMERIC(20,6) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD'
);
```

### slv_fin_ledger_entries

```sql
CREATE TABLE slv_fin_ledger_entries (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- entry_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    entry_id              VARCHAR(100) NOT NULL,
    journal_id            VARCHAR(100) NOT NULL,
    entry_date            DATE NOT NULL,
    account_code          VARCHAR(50) NOT NULL,
    debit_amount          NUMERIC(20,4) NOT NULL DEFAULT 0,
    credit_amount         NUMERIC(20,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    description           TEXT NOT NULL DEFAULT '',
    cost_center           VARCHAR(100),
    posted_by             VARCHAR(100)
);
```

### slv_fin_cards

```sql
CREATE TABLE slv_fin_cards (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- card_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    card_id               VARCHAR(100) NOT NULL,
    account_id            VARCHAR(100) NOT NULL,
    customer_id           VARCHAR(100) NOT NULL,
    card_type             VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    card_network          VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    card_number_masked    VARCHAR(20),
    expiry_date           DATE,
    issued_date           DATE,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    credit_limit          NUMERIC(20,4) NOT NULL DEFAULT 0,
    is_expired            BOOLEAN GENERATED ALWAYS AS (expiry_date < CURRENT_DATE) STORED
);
```

### slv_fin_fraud_alerts

```sql
CREATE TABLE slv_fin_fraud_alerts (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- alert_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    alert_id              VARCHAR(100) NOT NULL,
    transaction_id        VARCHAR(100) NOT NULL,
    account_id            VARCHAR(100) NOT NULL,
    customer_id           VARCHAR(100),
    alert_type            VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    severity              VARCHAR(20) NOT NULL DEFAULT 'LOW',
    rule_triggered        VARCHAR(100),
    score                 NUMERIC(8,4) NOT NULL DEFAULT 0,
    detected_at           TIMESTAMP NOT NULL,
    resolved_at           TIMESTAMP,
    resolution_hours      NUMERIC(10,2) GENERATED ALWAYS AS (
                            CASE WHEN resolved_at IS NOT NULL
                            THEN EXTRACT(EPOCH FROM (resolved_at - detected_at)) / 3600 ELSE NULL END
                          ) STORED,
    resolution            VARCHAR(50) NOT NULL DEFAULT 'PENDING'
);
```

### slv_fin_fx_rates

```sql
CREATE TABLE slv_fin_fx_rates (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- base_currency + quote_currency + rate_date
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    rate_id               VARCHAR(100) NOT NULL,
    base_currency         CHAR(3) NOT NULL,
    quote_currency        CHAR(3) NOT NULL,
    rate_date             DATE NOT NULL,
    bid_rate              NUMERIC(20,8) NOT NULL DEFAULT 0,
    ask_rate              NUMERIC(20,8) NOT NULL DEFAULT 0,
    mid_rate              NUMERIC(20,8) NOT NULL DEFAULT 0,
    spread                NUMERIC(20,8) GENERATED ALWAYS AS (ask_rate - bid_rate) STORED,
    source                VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN'
);
```

### slv_fin_budgets

```sql
CREATE TABLE slv_fin_budgets (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- cost_center + account_code + fiscal_year + fiscal_period
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    budget_id             VARCHAR(100) NOT NULL,
    cost_center           VARCHAR(100) NOT NULL,
    department_id         VARCHAR(100),
    fiscal_year           INTEGER NOT NULL,
    fiscal_period         INTEGER NOT NULL,
    account_code          VARCHAR(50) NOT NULL,
    budget_amount         NUMERIC(20,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    budget_type           VARCHAR(50) NOT NULL DEFAULT 'OPEX',
    approved_by           VARCHAR(100)
);
```

### slv_fin_invoices

```sql
CREATE TABLE slv_fin_invoices (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- invoice_number
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    invoice_id            VARCHAR(100) NOT NULL,
    invoice_number        VARCHAR(50) NOT NULL,
    customer_id           VARCHAR(100) NOT NULL,
    invoice_date          DATE NOT NULL,
    due_date              DATE,
    subtotal              NUMERIC(20,4) NOT NULL DEFAULT 0,
    tax_amount            NUMERIC(20,4) NOT NULL DEFAULT 0,
    total_amount          NUMERIC(20,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    status                VARCHAR(50) NOT NULL DEFAULT 'DRAFT',
    days_overdue          INTEGER GENERATED ALWAYS AS (
                            CASE WHEN due_date < CURRENT_DATE AND status NOT IN ('PAID','CANCELLED')
                            THEN CURRENT_DATE - due_date ELSE 0 END
                          ) STORED
);
```

### slv_fin_audit_logs

```sql
CREATE TABLE slv_fin_audit_logs (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- log_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    log_id                VARCHAR(100) NOT NULL,
    user_id               VARCHAR(100) NOT NULL,
    action                VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    entity_type           VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    entity_id             VARCHAR(100),
    old_values            TEXT,
    new_values            TEXT,
    ip_address            VARCHAR(50),
    action_timestamp      TIMESTAMP NOT NULL
);
```

---

## 📂 Sector 2 — Marketing

### slv_mkt_campaigns

```sql
CREATE TABLE slv_mkt_campaigns (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    campaign_id           VARCHAR(100) NOT NULL,
    campaign_name         VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    campaign_type         VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    channel               VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    status                VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    start_date            DATE,
    end_date              DATE,
    budget                NUMERIC(20,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    target_segment        VARCHAR(100),
    owner_id              VARCHAR(100)
);
```

### slv_mkt_campaign_performance

```sql
CREATE TABLE slv_mkt_campaign_performance (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- campaign_id + report_date
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    performance_id        VARCHAR(100) NOT NULL,
    campaign_id           VARCHAR(100) NOT NULL,
    report_date           DATE NOT NULL,
    impressions           BIGINT NOT NULL DEFAULT 0,
    clicks                BIGINT NOT NULL DEFAULT 0,
    conversions           BIGINT NOT NULL DEFAULT 0,
    spend                 NUMERIC(20,4) NOT NULL DEFAULT 0,
    revenue               NUMERIC(20,4) NOT NULL DEFAULT 0,
    reach                 BIGINT NOT NULL DEFAULT 0,
    engagement_rate       NUMERIC(10,6) NOT NULL DEFAULT 0,
    click_through_rate    NUMERIC(10,6) GENERATED ALWAYS AS (
                            CASE WHEN impressions > 0
                            THEN clicks::NUMERIC / impressions ELSE 0 END
                          ) STORED,
    cost_per_conversion   NUMERIC(20,4) GENERATED ALWAYS AS (
                            CASE WHEN conversions > 0
                            THEN spend / conversions ELSE 0 END
                          ) STORED
);
```

### slv_mkt_leads

```sql
CREATE TABLE slv_mkt_leads (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- email + campaign_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    lead_id               VARCHAR(100) NOT NULL,
    campaign_id           VARCHAR(100),
    first_name            VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    last_name             VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    email                 VARCHAR(255),
    phone                 VARCHAR(50),
    company               VARCHAR(255),
    lead_source           VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    lead_status           VARCHAR(50) NOT NULL DEFAULT 'NEW',
    score                 INTEGER NOT NULL DEFAULT 0,
    assigned_to           VARCHAR(100),
    created_at            TIMESTAMP
);
```

### slv_mkt_email_events

```sql
CREATE TABLE slv_mkt_email_events (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- event_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    event_id              VARCHAR(100) NOT NULL,
    campaign_id           VARCHAR(100) NOT NULL,
    recipient_email       VARCHAR(255) NOT NULL,
    event_type            VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    event_timestamp       TIMESTAMP NOT NULL,
    ip_address            VARCHAR(50),
    link_url              TEXT
);
```

### slv_mkt_social_metrics

```sql
CREATE TABLE slv_mkt_social_metrics (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- platform + post_id + post_date
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    metric_id             VARCHAR(100) NOT NULL,
    platform              VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    post_id               VARCHAR(100) NOT NULL,
    post_date             DATE NOT NULL,
    likes                 BIGINT NOT NULL DEFAULT 0,
    shares                BIGINT NOT NULL DEFAULT 0,
    comments              BIGINT NOT NULL DEFAULT 0,
    impressions           BIGINT NOT NULL DEFAULT 0,
    reach                 BIGINT NOT NULL DEFAULT 0,
    video_views           BIGINT NOT NULL DEFAULT 0,
    total_engagements     BIGINT GENERATED ALWAYS AS (likes + shares + comments) STORED
);

```

### slv_mkt_customer_segments

```sql
CREATE TABLE slv_mkt_customer_segments (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- segment_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    segment_id            VARCHAR(100) NOT NULL,
    segment_name          VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    segment_type          VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    criteria              TEXT,
    customer_count        BIGINT NOT NULL DEFAULT 0,
    created_by            VARCHAR(100),
    created_at            TIMESTAMP
);
```

### slv_mkt_ab_tests

```sql
CREATE TABLE slv_mkt_ab_tests (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- test_id + variant
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    test_id               VARCHAR(100) NOT NULL,
    test_name             VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    campaign_id           VARCHAR(100),
    variant               VARCHAR(10) NOT NULL DEFAULT 'A',
    start_date            DATE NOT NULL,
    end_date              DATE,
    sample_size           BIGINT NOT NULL DEFAULT 0,
    conversions           BIGINT NOT NULL DEFAULT 0,
    conversion_rate       NUMERIC(10,6) GENERATED ALWAYS AS (
                            CASE WHEN sample_size > 0
                            THEN conversions::NUMERIC / sample_size ELSE 0 END
                          ) STORED,
    revenue               NUMERIC(20,4) NOT NULL DEFAULT 0,
    status                VARCHAR(50) NOT NULL DEFAULT 'RUNNING',
    winner                VARCHAR(10)
);
```

### slv_mkt_content_assets

```sql
CREATE TABLE slv_mkt_content_assets (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- asset_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    asset_id              VARCHAR(100) NOT NULL,
    asset_name            VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    asset_type            VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    campaign_id           VARCHAR(100),
    channel               VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    publish_date          DATE,
    views                 BIGINT NOT NULL DEFAULT 0,
    downloads             BIGINT NOT NULL DEFAULT 0,
    shares                BIGINT NOT NULL DEFAULT 0,
    total_interactions    BIGINT GENERATED ALWAYS AS (views + downloads + shares) STORED,
    created_by            VARCHAR(100)
);
```

### slv_mkt_website_traffic

```sql
CREATE TABLE slv_mkt_website_traffic (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- page_url + traffic_date + source + medium
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    traffic_id            VARCHAR(100) NOT NULL,
    page_url              TEXT NOT NULL,
    traffic_date          DATE NOT NULL,
    sessions              BIGINT NOT NULL DEFAULT 0,
    users                 BIGINT NOT NULL DEFAULT 0,
    new_users             BIGINT NOT NULL DEFAULT 0,
    pageviews             BIGINT NOT NULL DEFAULT 0,
    bounce_rate           NUMERIC(8,4) NOT NULL DEFAULT 0,
    avg_session_sec       NUMERIC(10,2) NOT NULL DEFAULT 0,
    new_user_rate         NUMERIC(8,4) GENERATED ALWAYS AS (
                            CASE WHEN users > 0
                            THEN new_users::NUMERIC / users ELSE 0 END
                          ) STORED,
    source                VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    medium                VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN'
);
```

### slv_mkt_customer_journeys

```sql
CREATE TABLE slv_mkt_customer_journeys (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- journey_id + touchpoint_seq
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    journey_id            VARCHAR(100) NOT NULL,
    customer_id           VARCHAR(100) NOT NULL,
    touchpoint_seq        INTEGER NOT NULL DEFAULT 0,
    channel               VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    event_type            VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    campaign_id           VARCHAR(100),
    event_timestamp       TIMESTAMP NOT NULL,
    is_conversion         BOOLEAN NOT NULL DEFAULT FALSE
);
```

### slv_mkt_surveys

```sql
CREATE TABLE slv_mkt_surveys (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- response_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    response_id           VARCHAR(100) NOT NULL,
    survey_id             VARCHAR(100) NOT NULL,
    customer_id           VARCHAR(100),
    submitted_at          TIMESTAMP NOT NULL,
    nps_score             INTEGER,
    csat_score            NUMERIC(4,2),
    ces_score             NUMERIC(4,2),
    nps_category          VARCHAR(20) GENERATED ALWAYS AS (
                            CASE
                              WHEN nps_score >= 9 THEN 'PROMOTER'
                              WHEN nps_score >= 7 THEN 'PASSIVE'
                              WHEN nps_score IS NOT NULL THEN 'DETRACTOR'
                              ELSE NULL END
                          ) STORED,
    comments              TEXT,
    channel               VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN'
);
```

---

## 📂 Sector 3 — Healthcare

### slv_hlt_patients

```sql
CREATE TABLE slv_hlt_patients (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- mrn
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    patient_id            VARCHAR(100) NOT NULL,
    mrn                   VARCHAR(100) NOT NULL,
    first_name            VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    last_name             VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    date_of_birth         DATE,
    gender                VARCHAR(20) NOT NULL DEFAULT 'UNKNOWN',
    blood_type            VARCHAR(10),
    phone                 VARCHAR(50),
    email                 VARCHAR(255),
    city                  VARCHAR(100),
    country               CHAR(2),
    insurance_id          VARCHAR(100),
    registration_date     DATE
);
```

### slv_hlt_appointments

```sql
CREATE TABLE slv_hlt_appointments (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- appointment_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    appointment_id        VARCHAR(100) NOT NULL,
    patient_id            VARCHAR(100) NOT NULL,
    provider_id           VARCHAR(100) NOT NULL,
    facility_id           VARCHAR(100),
    appointment_date      TIMESTAMP NOT NULL,
    appointment_type      VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    status                VARCHAR(50) NOT NULL DEFAULT 'SCHEDULED',
    reason                TEXT NOT NULL DEFAULT '',
    duration_minutes      INTEGER NOT NULL DEFAULT 0
);
```

### slv_hlt_diagnoses

```sql
CREATE TABLE slv_hlt_diagnoses (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- diagnosis_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    diagnosis_id          VARCHAR(100) NOT NULL,
    patient_id            VARCHAR(100) NOT NULL,
    encounter_id          VARCHAR(100),
    icd_code              VARCHAR(20) NOT NULL,
    icd_version           VARCHAR(10) NOT NULL DEFAULT 'ICD-10',
    description           TEXT NOT NULL DEFAULT '',
    diagnosis_type        VARCHAR(50) NOT NULL DEFAULT 'PRIMARY',
    diagnosed_at          TIMESTAMP NOT NULL,
    provider_id           VARCHAR(100)
);
```

### slv_hlt_prescriptions

```sql
CREATE TABLE slv_hlt_prescriptions (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    prescription_id       VARCHAR(100) NOT NULL,
    patient_id            VARCHAR(100) NOT NULL,
    provider_id           VARCHAR(100),
    drug_code             VARCHAR(50) NOT NULL,
    drug_name             VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    dosage                VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    frequency             VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    quantity              NUMERIC(10,2) NOT NULL DEFAULT 0,
    unit                  VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    prescribed_at         TIMESTAMP NOT NULL,
    start_date            DATE,
    end_date              DATE,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE'
);
```

### slv_hlt_lab_results

```sql
CREATE TABLE slv_hlt_lab_results (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- result_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    result_id             VARCHAR(100) NOT NULL,
    patient_id            VARCHAR(100) NOT NULL,
    order_id              VARCHAR(100),
    test_code             VARCHAR(50) NOT NULL,
    test_name             VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    result_value          VARCHAR(255),
    unit                  VARCHAR(50),
    reference_range       VARCHAR(100),
    abnormal_flag         VARCHAR(10) NOT NULL DEFAULT 'N',
    collected_at          TIMESTAMP,
    resulted_at           TIMESTAMP
);
```

### slv_hlt_providers

```sql
CREATE TABLE slv_hlt_providers (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- npi
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    provider_id           VARCHAR(100) NOT NULL,
    npi                   VARCHAR(20),
    first_name            VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    last_name             VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    specialty             VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    license_number        VARCHAR(100),
    facility_id           VARCHAR(100),
    phone                 VARCHAR(50),
    email                 VARCHAR(255),
    active                BOOLEAN NOT NULL DEFAULT TRUE
);
```

### slv_hlt_encounters

```sql
CREATE TABLE slv_hlt_encounters (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- encounter_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    encounter_id          VARCHAR(100) NOT NULL,
    patient_id            VARCHAR(100) NOT NULL,
    provider_id           VARCHAR(100) NOT NULL,
    facility_id           VARCHAR(100),
    encounter_type        VARCHAR(50) NOT NULL DEFAULT 'OUTPATIENT',
    admit_date            TIMESTAMP NOT NULL,
    discharge_date        TIMESTAMP,
    length_of_stay_days   INTEGER GENERATED ALWAYS AS (
                            CASE WHEN discharge_date IS NOT NULL
                            THEN (discharge_date::DATE - admit_date::DATE) ELSE NULL END
                          ) STORED,
    drg_code              VARCHAR(20),
    primary_dx_code       VARCHAR(20)
);
```

### slv_hlt_procedures

```sql
CREATE TABLE slv_hlt_procedures (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- procedure_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    procedure_id          VARCHAR(100) NOT NULL,
    encounter_id          VARCHAR(100) NOT NULL,
    patient_id            VARCHAR(100) NOT NULL,
    provider_id           VARCHAR(100),
    cpt_code              VARCHAR(20) NOT NULL,
    procedure_name        VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    procedure_date        TIMESTAMP NOT NULL,
    quantity              INTEGER NOT NULL DEFAULT 1,
    status                VARCHAR(50) NOT NULL DEFAULT 'COMPLETED'
);
```

### slv_hlt_vitals

```sql
CREATE TABLE slv_hlt_vitals (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- patient_id + recorded_at
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    vital_id              VARCHAR(100) NOT NULL,
    patient_id            VARCHAR(100) NOT NULL,
    encounter_id          VARCHAR(100),
    recorded_at           TIMESTAMP NOT NULL,
    height_cm             NUMERIC(6,2),
    weight_kg             NUMERIC(6,2),
    bmi                   NUMERIC(6,2),
    bmi_category          VARCHAR(20) GENERATED ALWAYS AS (
                            CASE
                              WHEN bmi < 18.5 THEN 'UNDERWEIGHT'
                              WHEN bmi < 25   THEN 'NORMAL'
                              WHEN bmi < 30   THEN 'OVERWEIGHT'
                              WHEN bmi IS NOT NULL THEN 'OBESE'
                              ELSE NULL END
                          ) STORED,
    blood_pressure_sys    INTEGER,
    blood_pressure_dia    INTEGER,
    heart_rate            INTEGER,
    temperature_c         NUMERIC(5,2),
    oxygen_sat_pct        NUMERIC(5,2)
);
```

### slv_hlt_insurance_claims

```sql
CREATE TABLE slv_hlt_insurance_claims (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- claim_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    claim_id              VARCHAR(100) NOT NULL,
    encounter_id          VARCHAR(100) NOT NULL,
    patient_id            VARCHAR(100) NOT NULL,
    payer_id              VARCHAR(100) NOT NULL,
    submission_date       DATE NOT NULL,
    service_date          DATE NOT NULL,
    billed_amount         NUMERIC(20,4) NOT NULL DEFAULT 0,
    allowed_amount        NUMERIC(20,4) NOT NULL DEFAULT 0,
    paid_amount           NUMERIC(20,4) NOT NULL DEFAULT 0,
    patient_responsibility NUMERIC(20,4) GENERATED ALWAYS AS (allowed_amount - paid_amount) STORED,
    denial_reason         VARCHAR(100),
    status                VARCHAR(50) NOT NULL DEFAULT 'PENDING'
);
```

### slv_hlt_facilities

```sql
CREATE TABLE slv_hlt_facilities (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- facility_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    facility_id           VARCHAR(100) NOT NULL,
    facility_name         VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    facility_type         VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    city                  VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    country               CHAR(2) NOT NULL DEFAULT 'XX',
    bed_count             INTEGER NOT NULL DEFAULT 0,
    accreditation         VARCHAR(100),
    is_active             BOOLEAN NOT NULL DEFAULT TRUE
);
```

### slv_hlt_allergies

```sql
CREATE TABLE slv_hlt_allergies (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- patient_id + allergen
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    allergy_id            VARCHAR(100) NOT NULL,
    patient_id            VARCHAR(100) NOT NULL,
    allergen              VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    allergy_type          VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    reaction              VARCHAR(255),
    severity              VARCHAR(20) NOT NULL DEFAULT 'UNKNOWN',
    onset_date            DATE,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE'
);
```

---

## 📂 Sector 4 — Retail

### slv_ret_products

```sql
CREATE TABLE slv_ret_products (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- sku
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    product_id            VARCHAR(100) NOT NULL,
    sku                   VARCHAR(100) NOT NULL,
    barcode               VARCHAR(100),
    product_name          VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    brand                 VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    category              VARCHAR(100) NOT NULL DEFAULT 'UNCATEGORIZED',
    subcategory           VARCHAR(100),
    unit_cost             NUMERIC(20,4) NOT NULL DEFAULT 0,
    unit_price            NUMERIC(20,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    uom                   VARCHAR(50) NOT NULL DEFAULT 'EA',
    is_active             BOOLEAN NOT NULL DEFAULT TRUE,
    margin_pct            NUMERIC(8,4) GENERATED ALWAYS AS (
                            CASE WHEN unit_price > 0
                            THEN (unit_price - unit_cost) / unit_price * 100 ELSE 0 END
                          ) STORED
);
```

### slv_ret_sales_transactions

```sql
CREATE TABLE slv_ret_sales_transactions (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- transaction_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    transaction_id        VARCHAR(100) NOT NULL,
    store_id              VARCHAR(100) NOT NULL,
    pos_terminal_id       VARCHAR(100),
    customer_id           VARCHAR(100),
    transaction_date      TIMESTAMP NOT NULL,
    total_amount          NUMERIC(20,4) NOT NULL DEFAULT 0,
    discount_amount       NUMERIC(20,4) NOT NULL DEFAULT 0,
    tax_amount            NUMERIC(20,4) NOT NULL DEFAULT 0,
    net_amount            NUMERIC(20,4) GENERATED ALWAYS AS (total_amount - discount_amount) STORED,
    payment_method        VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    cashier_id            VARCHAR(100),
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD'
);
```

### slv_ret_sales_items

```sql
CREATE TABLE slv_ret_sales_items (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- line_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    line_id               VARCHAR(100) NOT NULL,
    transaction_id        VARCHAR(100) NOT NULL,
    product_id            VARCHAR(100) NOT NULL,
    sku                   VARCHAR(100) NOT NULL,
    quantity              NUMERIC(10,3) NOT NULL DEFAULT 0,
    unit_price            NUMERIC(20,4) NOT NULL DEFAULT 0,
    discount              NUMERIC(20,4) NOT NULL DEFAULT 0,
    line_total            NUMERIC(20,4) NOT NULL DEFAULT 0
);
```

### slv_ret_stores

```sql
CREATE TABLE slv_ret_stores (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    store_id              VARCHAR(100) NOT NULL,
    store_code            VARCHAR(50) NOT NULL,
    store_name            VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    store_type            VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    city                  VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    region                VARCHAR(100),
    country               CHAR(2) NOT NULL DEFAULT 'XX',
    manager_id            VARCHAR(100),
    open_date             DATE,
    is_active             BOOLEAN NOT NULL DEFAULT TRUE
);
```

### slv_ret_inventory

```sql
CREATE TABLE slv_ret_inventory (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- store_id + sku
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    inventory_id          VARCHAR(100) NOT NULL,
    store_id              VARCHAR(100) NOT NULL,
    product_id            VARCHAR(100) NOT NULL,
    sku                   VARCHAR(100) NOT NULL,
    quantity_on_hand      NUMERIC(10,3) NOT NULL DEFAULT 0,
    quantity_reserved     NUMERIC(10,3) NOT NULL DEFAULT 0,
    quantity_available    NUMERIC(10,3) GENERATED ALWAYS AS (quantity_on_hand - quantity_reserved) STORED,
    reorder_point         NUMERIC(10,3) NOT NULL DEFAULT 0,
    is_below_reorder      BOOLEAN GENERATED ALWAYS AS (quantity_on_hand <= reorder_point) STORED,
    last_count_date       DATE
);
```

### slv_ret_customers

```sql
CREATE TABLE slv_ret_customers (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- email
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    customer_id           VARCHAR(100) NOT NULL,
    first_name            VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    last_name             VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    email                 VARCHAR(255),
    phone                 VARCHAR(50),
    loyalty_card_no       VARCHAR(100),
    loyalty_points        BIGINT NOT NULL DEFAULT 0,
    tier                  VARCHAR(50) NOT NULL DEFAULT 'STANDARD',
    registered_at         TIMESTAMP,
    date_of_birth         DATE,
    gender                VARCHAR(20) NOT NULL DEFAULT 'UNKNOWN'
);
```

### slv_ret_promotions

```sql
CREATE TABLE slv_ret_promotions (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- promotion_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    promotion_id          VARCHAR(100) NOT NULL,
    promo_name            VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    promo_type            VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    start_date            DATE NOT NULL,
    end_date              DATE,
    discount_value        NUMERIC(10,4) NOT NULL DEFAULT 0,
    min_purchase          NUMERIC(20,4) NOT NULL DEFAULT 0,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    is_expired            BOOLEAN GENERATED ALWAYS AS (end_date < CURRENT_DATE) STORED
);
```

### slv_ret_returns

```sql
CREATE TABLE slv_ret_returns (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- return_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    return_id             VARCHAR(100) NOT NULL,
    transaction_id        VARCHAR(100) NOT NULL,
    store_id              VARCHAR(100) NOT NULL,
    customer_id           VARCHAR(100),
    return_date           TIMESTAMP NOT NULL,
    reason_code           VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    product_id            VARCHAR(100) NOT NULL,
    quantity              NUMERIC(10,3) NOT NULL DEFAULT 0,
    refund_amount         NUMERIC(20,4) NOT NULL DEFAULT 0,
    return_method         VARCHAR(50) NOT NULL DEFAULT 'IN_STORE',
    status                VARCHAR(50) NOT NULL DEFAULT 'PENDING'
);
```

### slv_ret_suppliers

```sql
CREATE TABLE slv_ret_suppliers (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- supplier_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    supplier_id           VARCHAR(100) NOT NULL,
    supplier_name         VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    email                 VARCHAR(255),
    country               CHAR(2) NOT NULL DEFAULT 'XX',
    payment_terms         VARCHAR(50) NOT NULL DEFAULT 'NET30',
    lead_time_days        INTEGER NOT NULL DEFAULT 0,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE'
);
```

### slv_ret_purchase_orders

```sql
CREATE TABLE slv_ret_purchase_orders (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- po_number
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    po_id                 VARCHAR(100) NOT NULL,
    po_number             VARCHAR(50) NOT NULL,
    supplier_id           VARCHAR(100) NOT NULL,
    store_id              VARCHAR(100),
    order_date            DATE NOT NULL,
    expected_date         DATE,
    total_amount          NUMERIC(20,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    status                VARCHAR(50) NOT NULL DEFAULT 'PENDING'
);
```

### slv_ret_shrinkage

```sql
CREATE TABLE slv_ret_shrinkage (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- shrinkage_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    shrinkage_id          VARCHAR(100) NOT NULL,
    store_id              VARCHAR(100) NOT NULL,
    product_id            VARCHAR(100) NOT NULL,
    event_date            DATE NOT NULL,
    quantity_lost         NUMERIC(10,3) NOT NULL DEFAULT 0,
    unit_cost             NUMERIC(20,4) NOT NULL DEFAULT 0,
    total_loss_value      NUMERIC(20,4) NOT NULL DEFAULT 0,
    reason_code           VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN'
);
```

### slv_ret_price_changes

```sql
CREATE TABLE slv_ret_price_changes (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- change_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    change_id             VARCHAR(100) NOT NULL,
    product_id            VARCHAR(100) NOT NULL,
    store_id              VARCHAR(100),
    old_price             NUMERIC(20,4) NOT NULL DEFAULT 0,
    new_price             NUMERIC(20,4) NOT NULL DEFAULT 0,
    price_change_pct      NUMERIC(10,4) GENERATED ALWAYS AS (
                            CASE WHEN old_price > 0
                            THEN (new_price - old_price) / old_price * 100 ELSE 0 END
                          ) STORED,
    is_increase           BOOLEAN GENERATED ALWAYS AS (new_price > old_price) STORED,
    effective_date        DATE NOT NULL,
    reason                VARCHAR(100),
    approved_by           VARCHAR(100)
);
```

---

## 📂 Sector 5 — Manufacturing

### slv_mfg_work_orders

```sql
CREATE TABLE slv_mfg_work_orders (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    work_order_id         VARCHAR(100) NOT NULL,
    product_id            VARCHAR(100) NOT NULL,
    bom_id                VARCHAR(100),
    plant_id              VARCHAR(100) NOT NULL,
    quantity_planned      NUMERIC(15,3) NOT NULL DEFAULT 0,
    quantity_produced     NUMERIC(15,3) NOT NULL DEFAULT 0,
    yield_pct             NUMERIC(8,4) GENERATED ALWAYS AS (
                            CASE WHEN quantity_planned > 0
                            THEN quantity_produced / quantity_planned * 100 ELSE 0 END
                          ) STORED,
    start_date            DATE,
    end_date              DATE,
    status                VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    priority              VARCHAR(20) NOT NULL DEFAULT 'NORMAL'
);
```

### slv_mfg_machines

```sql
CREATE TABLE slv_mfg_machines (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- machine_code
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    machine_id            VARCHAR(100) NOT NULL,
    machine_code          VARCHAR(50) NOT NULL,
    machine_name          VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    machine_type          VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    plant_id              VARCHAR(100) NOT NULL,
    line_id               VARCHAR(100),
    manufacturer          VARCHAR(100),
    model                 VARCHAR(100),
    serial_number         VARCHAR(100),
    install_date          DATE,
    status                VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN'
);
```

### slv_mfg_machine_telemetry

```sql
CREATE TABLE slv_mfg_machine_telemetry (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- machine_id + recorded_at
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    telemetry_id          VARCHAR(100) NOT NULL,
    machine_id            VARCHAR(100) NOT NULL,
    recorded_at           TIMESTAMP NOT NULL,
    temperature           NUMERIC(10,4) NOT NULL DEFAULT 0,
    pressure              NUMERIC(10,4) NOT NULL DEFAULT 0,
    vibration             NUMERIC(10,4) NOT NULL DEFAULT 0,
    rpm                   NUMERIC(10,2) NOT NULL DEFAULT 0,
    power_consumption     NUMERIC(10,4) NOT NULL DEFAULT 0,
    status_code           VARCHAR(20) NOT NULL DEFAULT 'OK'
);
```

### slv_mfg_quality_inspections

```sql
CREATE TABLE slv_mfg_quality_inspections (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    inspection_id         VARCHAR(100) NOT NULL,
    work_order_id         VARCHAR(100) NOT NULL,
    batch_number          VARCHAR(100),
    product_id            VARCHAR(100) NOT NULL,
    inspector_id          VARCHAR(100),
    inspection_date       TIMESTAMP NOT NULL,
    quantity_inspected    NUMERIC(15,3) NOT NULL DEFAULT 0,
    quantity_passed       NUMERIC(15,3) NOT NULL DEFAULT 0,
    quantity_rejected     NUMERIC(15,3) NOT NULL DEFAULT 0,
    defect_rate_pct       NUMERIC(8,4) GENERATED ALWAYS AS (
                            CASE WHEN quantity_inspected > 0
                            THEN quantity_rejected / quantity_inspected * 100 ELSE 0 END
                          ) STORED,
    defect_code           VARCHAR(50),
    result                VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN'
);
```

### slv_mfg_bill_of_materials

```sql
CREATE TABLE slv_mfg_bill_of_materials (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- bom_id + component_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    bom_id                VARCHAR(100) NOT NULL,
    bom_version           VARCHAR(20) NOT NULL DEFAULT '1.0',
    product_id            VARCHAR(100) NOT NULL,
    component_id          VARCHAR(100) NOT NULL,
    quantity_required     NUMERIC(15,6) NOT NULL DEFAULT 0,
    uom                   VARCHAR(50) NOT NULL DEFAULT 'EA',
    scrap_factor          NUMERIC(8,4) NOT NULL DEFAULT 0,
    effective_date        DATE,
    expiry_date           DATE
);
```

### slv_mfg_maintenance_orders

```sql
CREATE TABLE slv_mfg_maintenance_orders (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- order_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    order_id              VARCHAR(100) NOT NULL,
    machine_id            VARCHAR(100) NOT NULL,
    plant_id              VARCHAR(100) NOT NULL,
    order_type            VARCHAR(50) NOT NULL DEFAULT 'CORRECTIVE',
    priority              VARCHAR(20) NOT NULL DEFAULT 'NORMAL',
    scheduled_date        DATE,
    completed_date        DATE,
    technician_id         VARCHAR(100),
    downtime_minutes      INTEGER NOT NULL DEFAULT 0,
    cost                  NUMERIC(20,4) NOT NULL DEFAULT 0,
    status                VARCHAR(50) NOT NULL DEFAULT 'OPEN'
);
```

### slv_mfg_production_schedules

```sql
CREATE TABLE slv_mfg_production_schedules (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- schedule_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    schedule_id           VARCHAR(100) NOT NULL,
    plant_id              VARCHAR(100) NOT NULL,
    line_id               VARCHAR(100),
    product_id            VARCHAR(100) NOT NULL,
    scheduled_date        DATE NOT NULL,
    shift                 VARCHAR(20) NOT NULL DEFAULT 'MORNING',
    planned_qty           NUMERIC(15,3) NOT NULL DEFAULT 0,
    actual_qty            NUMERIC(15,3) NOT NULL DEFAULT 0,
    attainment_pct        NUMERIC(8,4) GENERATED ALWAYS AS (
                            CASE WHEN planned_qty > 0
                            THEN actual_qty / planned_qty * 100 ELSE 0 END
                          ) STORED,
    status                VARCHAR(50) NOT NULL DEFAULT 'PLANNED'
);
```

### slv_mfg_raw_materials

```sql
CREATE TABLE slv_mfg_raw_materials (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- material_code
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    material_id           VARCHAR(100) NOT NULL,
    material_code         VARCHAR(50) NOT NULL,
    material_name         VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    material_type         VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    uom                   VARCHAR(50) NOT NULL DEFAULT 'EA',
    stock_qty             NUMERIC(15,3) NOT NULL DEFAULT 0,
    reorder_level         NUMERIC(15,3) NOT NULL DEFAULT 0,
    is_below_reorder      BOOLEAN GENERATED ALWAYS AS (stock_qty <= reorder_level) STORED,
    supplier_id           VARCHAR(100),
    unit_cost             NUMERIC(20,4) NOT NULL DEFAULT 0
);
```

### slv_mfg_shift_logs

```sql
CREATE TABLE slv_mfg_shift_logs (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- plant_id + line_id + shift_date + shift
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    log_id                VARCHAR(100) NOT NULL,
    plant_id              VARCHAR(100) NOT NULL,
    line_id               VARCHAR(100),
    shift_date            DATE NOT NULL,
    shift                 VARCHAR(20) NOT NULL DEFAULT 'MORNING',
    supervisor_id         VARCHAR(100),
    operators_count       INTEGER NOT NULL DEFAULT 0,
    production_qty        NUMERIC(15,3) NOT NULL DEFAULT 0,
    downtime_minutes      INTEGER NOT NULL DEFAULT 0,
    incidents             INTEGER NOT NULL DEFAULT 0,
    uptime_pct            NUMERIC(8,4) GENERATED ALWAYS AS (
                            CASE WHEN 480 > 0
                            THEN (480 - downtime_minutes)::NUMERIC / 480 * 100 ELSE 0 END
                          ) STORED,
    notes                 TEXT
);
```

### slv_mfg_energy_consumption

```sql
CREATE TABLE slv_mfg_energy_consumption (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- plant_id + machine_id + reading_date
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    consumption_id        VARCHAR(100) NOT NULL,
    plant_id              VARCHAR(100) NOT NULL,
    machine_id            VARCHAR(100),
    reading_date          DATE NOT NULL,
    electricity_kwh       NUMERIC(15,4) NOT NULL DEFAULT 0,
    gas_m3                NUMERIC(15,4) NOT NULL DEFAULT 0,
    water_liters          NUMERIC(15,4) NOT NULL DEFAULT 0,
    cost                  NUMERIC(20,4) NOT NULL DEFAULT 0
);
```

### slv_mfg_scrap_records

```sql
CREATE TABLE slv_mfg_scrap_records (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- scrap_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    scrap_id              VARCHAR(100) NOT NULL,
    work_order_id         VARCHAR(100) NOT NULL,
    product_id            VARCHAR(100) NOT NULL,
    plant_id              VARCHAR(100) NOT NULL,
    scrap_date            DATE NOT NULL,
    quantity              NUMERIC(15,3) NOT NULL DEFAULT 0,
    uom                   VARCHAR(50) NOT NULL DEFAULT 'EA',
    reason_code           VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    disposal_method       VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    cost                  NUMERIC(20,4) NOT NULL DEFAULT 0
);
```

---

## 📂 Sector 6 — E-Commerce

### slv_ecom_orders

```sql
CREATE TABLE slv_ecom_orders (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    order_id              VARCHAR(100) NOT NULL,
    customer_id           VARCHAR(100),
    order_date            TIMESTAMP NOT NULL,
    status                VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    subtotal              NUMERIC(20,4) NOT NULL DEFAULT 0,
    discount              NUMERIC(20,4) NOT NULL DEFAULT 0,
    tax                   NUMERIC(20,4) NOT NULL DEFAULT 0,
    shipping_fee          NUMERIC(20,4) NOT NULL DEFAULT 0,
    total_amount          NUMERIC(20,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    payment_status        VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    channel               VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN'
);
```

### slv_ecom_order_items

```sql
CREATE TABLE slv_ecom_order_items (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    line_id               VARCHAR(100) NOT NULL,
    order_id              VARCHAR(100) NOT NULL,
    product_id            VARCHAR(100) NOT NULL,
    sku                   VARCHAR(100) NOT NULL,
    product_name          VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    quantity              NUMERIC(10,2) NOT NULL DEFAULT 0,
    unit_price            NUMERIC(20,4) NOT NULL DEFAULT 0,
    discount              NUMERIC(20,4) NOT NULL DEFAULT 0,
    line_total            NUMERIC(20,4) NOT NULL DEFAULT 0
);
```

### slv_ecom_customers

```sql
CREATE TABLE slv_ecom_customers (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- email
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    customer_id           VARCHAR(100) NOT NULL,
    email                 VARCHAR(255),
    first_name            VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    last_name             VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    phone                 VARCHAR(50),
    registered_at         TIMESTAMP,
    last_login            TIMESTAMP,
    is_guest              BOOLEAN NOT NULL DEFAULT FALSE,
    marketing_opt_in      BOOLEAN NOT NULL DEFAULT FALSE
);
```

### slv_ecom_product_catalog

```sql
CREATE TABLE slv_ecom_product_catalog (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- sku
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    product_id            VARCHAR(100) NOT NULL,
    sku                   VARCHAR(100) NOT NULL,
    product_name          VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    description           TEXT NOT NULL DEFAULT '',
    category              VARCHAR(100) NOT NULL DEFAULT 'UNCATEGORIZED',
    subcategory           VARCHAR(100),
    brand                 VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    price                 NUMERIC(20,4) NOT NULL DEFAULT 0,
    sale_price            NUMERIC(20,4),
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    stock_quantity        INTEGER NOT NULL DEFAULT 0,
    is_active             BOOLEAN NOT NULL DEFAULT TRUE,
    discount_pct          NUMERIC(8,4) GENERATED ALWAYS AS (
                            CASE WHEN price > 0 AND sale_price IS NOT NULL
                            THEN (price - sale_price) / price * 100 ELSE 0 END
                          ) STORED
);
```

### slv_ecom_web_sessions

```sql
CREATE TABLE slv_ecom_web_sessions (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- session_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    session_id            VARCHAR(100) NOT NULL,
    customer_id           VARCHAR(100),
    session_start         TIMESTAMP NOT NULL,
    session_end           TIMESTAMP,
    duration_seconds      INTEGER GENERATED ALWAYS AS (
                            CASE WHEN session_end IS NOT NULL
                            THEN EXTRACT(EPOCH FROM (session_end - session_start))::INTEGER ELSE NULL END
                          ) STORED,
    device_type           VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    browser               VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    os                    VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    referral_source       VARCHAR(255),
    pages_viewed          INTEGER NOT NULL DEFAULT 0,
    cart_adds             INTEGER NOT NULL DEFAULT 0,
    converted             BOOLEAN NOT NULL DEFAULT FALSE
);
```

### slv_ecom_returns

```sql
CREATE TABLE slv_ecom_returns (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    return_id             VARCHAR(100) NOT NULL,
    order_id              VARCHAR(100) NOT NULL,
    customer_id           VARCHAR(100),
    return_date           TIMESTAMP NOT NULL,
    reason_code           VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    reason_text           TEXT,
    status                VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    refund_amount         NUMERIC(20,4) NOT NULL DEFAULT 0
);
```

### slv_ecom_reviews

```sql
CREATE TABLE slv_ecom_reviews (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- review_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    review_id             VARCHAR(100) NOT NULL,
    product_id            VARCHAR(100) NOT NULL,
    customer_id           VARCHAR(100),
    order_id              VARCHAR(100),
    rating                SMALLINT NOT NULL DEFAULT 3,
    sentiment             VARCHAR(20) GENERATED ALWAYS AS (
                            CASE
                              WHEN rating >= 4 THEN 'POSITIVE'
                              WHEN rating = 3  THEN 'NEUTRAL'
                              ELSE 'NEGATIVE' END
                          ) STORED,
    title                 VARCHAR(255),
    body                  TEXT,
    is_verified           BOOLEAN NOT NULL DEFAULT FALSE,
    helpful_votes         INTEGER NOT NULL DEFAULT 0,
    submitted_at          TIMESTAMP NOT NULL,
    status                VARCHAR(50) NOT NULL DEFAULT 'PENDING'
);
```

### slv_ecom_cart_events

```sql
CREATE TABLE slv_ecom_cart_events (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- event_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    event_id              VARCHAR(100) NOT NULL,
    session_id            VARCHAR(100) NOT NULL,
    customer_id           VARCHAR(100),
    product_id            VARCHAR(100) NOT NULL,
    event_type            VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    quantity              NUMERIC(10,2) NOT NULL DEFAULT 0,
    price_at_event        NUMERIC(20,4) NOT NULL DEFAULT 0,
    event_timestamp       TIMESTAMP NOT NULL
);
```

### slv_ecom_promotions

```sql
CREATE TABLE slv_ecom_promotions (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- promo_code
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    promo_id              VARCHAR(100) NOT NULL,
    promo_code            VARCHAR(50) NOT NULL,
    promo_type            VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    discount_value        NUMERIC(10,4) NOT NULL DEFAULT 0,
    min_order_amount      NUMERIC(20,4) NOT NULL DEFAULT 0,
    usage_limit           INTEGER NOT NULL DEFAULT 0,
    times_used            INTEGER NOT NULL DEFAULT 0,
    utilization_pct       NUMERIC(8,4) GENERATED ALWAYS AS (
                            CASE WHEN usage_limit > 0
                            THEN times_used::NUMERIC / usage_limit * 100 ELSE 0 END
                          ) STORED,
    start_date            DATE NOT NULL,
    end_date              DATE,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE'
);
```

### slv_ecom_payments

```sql
CREATE TABLE slv_ecom_payments (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- payment_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    payment_id            VARCHAR(100) NOT NULL,
    order_id              VARCHAR(100) NOT NULL,
    payment_method        VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    payment_gateway       VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    amount                NUMERIC(20,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    status                VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    gateway_ref           VARCHAR(100),
    paid_at               TIMESTAMP
);
```

### slv_ecom_wishlists

```sql
CREATE TABLE slv_ecom_wishlists (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- customer_id + product_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    wishlist_id           VARCHAR(100) NOT NULL,
    customer_id           VARCHAR(100) NOT NULL,
    product_id            VARCHAR(100) NOT NULL,
    added_at              TIMESTAMP NOT NULL,
    moved_to_cart         BOOLEAN NOT NULL DEFAULT FALSE,
    purchased             BOOLEAN NOT NULL DEFAULT FALSE
);
```

### slv_ecom_sellers

```sql
CREATE TABLE slv_ecom_sellers (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- seller_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    seller_id             VARCHAR(100) NOT NULL,
    seller_name           VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    email                 VARCHAR(255),
    country               CHAR(2) NOT NULL DEFAULT 'XX',
    category              VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    rating                NUMERIC(4,2) NOT NULL DEFAULT 0,
    total_products        INTEGER NOT NULL DEFAULT 0,
    joined_date           DATE,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE'
);
```

---

## 📂 Sector 7 — Logistics

### slv_log_shipments

```sql
CREATE TABLE slv_log_shipments (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- tracking_number
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    shipment_id           VARCHAR(100) NOT NULL,
    tracking_number       VARCHAR(100) NOT NULL,
    carrier_id            VARCHAR(100) NOT NULL,
    origin_id             VARCHAR(100) NOT NULL,
    destination_id        VARCHAR(100) NOT NULL,
    shipper_id            VARCHAR(100),
    consignee_id          VARCHAR(100),
    ship_date             TIMESTAMP NOT NULL,
    estimated_delivery    DATE,
    actual_delivery       TIMESTAMP,
    days_to_deliver       INTEGER GENERATED ALWAYS AS (
                            CASE WHEN actual_delivery IS NOT NULL
                            THEN (actual_delivery::DATE - ship_date::DATE) ELSE NULL END
                          ) STORED,
    status                VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    weight_kg             NUMERIC(10,3) NOT NULL DEFAULT 0,
    volume_m3             NUMERIC(10,4) NOT NULL DEFAULT 0
);
```

### slv_log_shipment_events

```sql
CREATE TABLE slv_log_shipment_events (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- event_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    event_id              VARCHAR(100) NOT NULL,
    shipment_id           VARCHAR(100) NOT NULL,
    event_type            VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    event_timestamp       TIMESTAMP NOT NULL,
    location_code         VARCHAR(100),
    location_name         VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    latitude              NUMERIC(10,7),
    longitude             NUMERIC(10,7),
    notes                 TEXT
);
```

### slv_log_warehouses

```sql
CREATE TABLE slv_log_warehouses (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    warehouse_id          VARCHAR(100) NOT NULL,
    warehouse_code        VARCHAR(50) NOT NULL,
    warehouse_name        VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    warehouse_type        VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    city                  VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    country               CHAR(2) NOT NULL DEFAULT 'XX',
    capacity_m3           NUMERIC(15,2) NOT NULL DEFAULT 0,
    is_active             BOOLEAN NOT NULL DEFAULT TRUE
);
```

### slv_log_vehicles

```sql
CREATE TABLE slv_log_vehicles (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- plate_number
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    vehicle_id            VARCHAR(100) NOT NULL,
    plate_number          VARCHAR(50) NOT NULL,
    vehicle_type          VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    capacity_kg           NUMERIC(10,2) NOT NULL DEFAULT 0,
    capacity_m3           NUMERIC(10,4) NOT NULL DEFAULT 0,
    driver_id             VARCHAR(100),
    carrier_id            VARCHAR(100),
    status                VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN'
);
```

### slv_log_routes

```sql
CREATE TABLE slv_log_routes (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    route_id              VARCHAR(100) NOT NULL,
    route_name            VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    origin_id             VARCHAR(100) NOT NULL,
    destination_id        VARCHAR(100) NOT NULL,
    distance_km           NUMERIC(10,2) NOT NULL DEFAULT 0,
    transit_days          INTEGER NOT NULL DEFAULT 0,
    mode                  VARCHAR(50) NOT NULL DEFAULT 'ROAD',
    carrier_id            VARCHAR(100),
    is_active             BOOLEAN NOT NULL DEFAULT TRUE
);
```

### slv_log_delivery_attempts

```sql
CREATE TABLE slv_log_delivery_attempts (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- attempt_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    attempt_id            VARCHAR(100) NOT NULL,
    shipment_id           VARCHAR(100) NOT NULL,
    attempt_number        INTEGER NOT NULL DEFAULT 1,
    attempt_date          TIMESTAMP NOT NULL,
    driver_id             VARCHAR(100),
    status                VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    failure_reason        VARCHAR(100),
    next_attempt_date     DATE,
    is_successful         BOOLEAN GENERATED ALWAYS AS (status = 'DELIVERED') STORED
);
```

### slv_log_customs

```sql
CREATE TABLE slv_log_customs (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- declaration_no
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    customs_id            VARCHAR(100) NOT NULL,
    shipment_id           VARCHAR(100) NOT NULL,
    declaration_no        VARCHAR(100) NOT NULL,
    entry_port            VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    country_of_origin     CHAR(2) NOT NULL DEFAULT 'XX',
    destination_country   CHAR(2) NOT NULL DEFAULT 'XX',
    hs_code               VARCHAR(20),
    declared_value        NUMERIC(20,4) NOT NULL DEFAULT 0,
    duties_amount         NUMERIC(20,4) NOT NULL DEFAULT 0,
    effective_duty_rate   NUMERIC(8,4) GENERATED ALWAYS AS (
                            CASE WHEN declared_value > 0
                            THEN duties_amount / declared_value * 100 ELSE 0 END
                          ) STORED,
    status                VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    clearance_date        DATE
);
```

### slv_log_fleet_maintenance

```sql
CREATE TABLE slv_log_fleet_maintenance (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- maintenance_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    maintenance_id        VARCHAR(100) NOT NULL,
    vehicle_id            VARCHAR(100) NOT NULL,
    maintenance_type      VARCHAR(50) NOT NULL DEFAULT 'ROUTINE',
    service_date          DATE NOT NULL,
    odometer_km           NUMERIC(12,2) NOT NULL DEFAULT 0,
    technician_id         VARCHAR(100),
    cost                  NUMERIC(20,4) NOT NULL DEFAULT 0,
    next_service_date     DATE,
    status                VARCHAR(50) NOT NULL DEFAULT 'COMPLETED'
);
```

### slv_log_packaging

```sql
CREATE TABLE slv_log_packaging (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- package_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    package_id            VARCHAR(100) NOT NULL,
    shipment_id           VARCHAR(100) NOT NULL,
    package_type          VARCHAR(50) NOT NULL DEFAULT 'BOX',
    length_cm             NUMERIC(8,2) NOT NULL DEFAULT 0,
    width_cm              NUMERIC(8,2) NOT NULL DEFAULT 0,
    height_cm             NUMERIC(8,2) NOT NULL DEFAULT 0,
    volume_cm3            NUMERIC(15,4) GENERATED ALWAYS AS (length_cm * width_cm * height_cm) STORED,
    weight_kg             NUMERIC(10,3) NOT NULL DEFAULT 0,
    fragile               BOOLEAN NOT NULL DEFAULT FALSE,
    hazmat                BOOLEAN NOT NULL DEFAULT FALSE
);
```

---

## 📂 Sector 8 — Supply Chain

### slv_sc_suppliers

```sql
CREATE TABLE slv_sc_suppliers (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- supplier_code
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    supplier_id           VARCHAR(100) NOT NULL,
    supplier_code         VARCHAR(50) NOT NULL,
    supplier_name         VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    contact_name          VARCHAR(100),
    email                 VARCHAR(255),
    phone                 VARCHAR(50),
    country               CHAR(2) NOT NULL DEFAULT 'XX',
    payment_terms         VARCHAR(50) NOT NULL DEFAULT 'NET30',
    lead_time_days        INTEGER NOT NULL DEFAULT 0,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE'
);
```

### slv_sc_purchase_orders

```sql
CREATE TABLE slv_sc_purchase_orders (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- po_number
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    po_id                 VARCHAR(100) NOT NULL,
    po_number             VARCHAR(50) NOT NULL,
    supplier_id           VARCHAR(100) NOT NULL,
    buyer_id              VARCHAR(100),
    order_date            DATE NOT NULL,
    expected_date         DATE,
    status                VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    total_amount          NUMERIC(20,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD'
);
```

### slv_sc_purchase_order_lines

```sql
CREATE TABLE slv_sc_purchase_order_lines (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    line_id               VARCHAR(100) NOT NULL,
    po_id                 VARCHAR(100) NOT NULL,
    item_id               VARCHAR(100) NOT NULL,
    description           TEXT NOT NULL DEFAULT '',
    quantity_ordered      NUMERIC(15,3) NOT NULL DEFAULT 0,
    quantity_received     NUMERIC(15,3) NOT NULL DEFAULT 0,
    quantity_pending      NUMERIC(15,3) GENERATED ALWAYS AS (quantity_ordered - quantity_received) STORED,
    unit_price            NUMERIC(20,4) NOT NULL DEFAULT 0,
    uom                   VARCHAR(50) NOT NULL DEFAULT 'EA',
    line_total            NUMERIC(20,4) NOT NULL DEFAULT 0
);
```

### slv_sc_goods_receipts

```sql
CREATE TABLE slv_sc_goods_receipts (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    receipt_id            VARCHAR(100) NOT NULL,
    po_id                 VARCHAR(100) NOT NULL,
    warehouse_id          VARCHAR(100) NOT NULL,
    received_date         TIMESTAMP NOT NULL,
    received_by           VARCHAR(100),
    status                VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    notes                 TEXT
);
```

### slv_sc_inventory_movements

```sql
CREATE TABLE slv_sc_inventory_movements (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- movement_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    movement_id           VARCHAR(100) NOT NULL,
    item_id               VARCHAR(100) NOT NULL,
    warehouse_id          VARCHAR(100) NOT NULL,
    movement_type         VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    quantity              NUMERIC(15,3) NOT NULL DEFAULT 0,
    uom                   VARCHAR(50) NOT NULL DEFAULT 'EA',
    reference_doc         VARCHAR(100),
    movement_date         TIMESTAMP NOT NULL
);
```

### slv_sc_contracts

```sql
CREATE TABLE slv_sc_contracts (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- contract_number
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    contract_id           VARCHAR(100) NOT NULL,
    contract_number       VARCHAR(50) NOT NULL,
    supplier_id           VARCHAR(100) NOT NULL,
    contract_type         VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    start_date            DATE NOT NULL,
    end_date              DATE,
    total_value           NUMERIC(20,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    payment_terms         VARCHAR(50) NOT NULL DEFAULT 'NET30',
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    is_expired            BOOLEAN GENERATED ALWAYS AS (end_date < CURRENT_DATE) STORED
);
```

### slv_sc_demand_forecasts

```sql
CREATE TABLE slv_sc_demand_forecasts (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- item_id + warehouse_id + forecast_date
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    forecast_id           VARCHAR(100) NOT NULL,
    item_id               VARCHAR(100) NOT NULL,
    warehouse_id          VARCHAR(100) NOT NULL,
    forecast_date         DATE NOT NULL,
    forecast_period       VARCHAR(20) NOT NULL DEFAULT 'MONTHLY',
    forecasted_qty        NUMERIC(15,3) NOT NULL DEFAULT 0,
    actual_qty            NUMERIC(15,3) NOT NULL DEFAULT 0,
    forecast_accuracy_pct NUMERIC(8,4) GENERATED ALWAYS AS (
                            CASE WHEN forecasted_qty > 0
                            THEN (1 - ABS(actual_qty - forecasted_qty) / forecasted_qty) * 100
                            ELSE 0 END
                          ) STORED,
    model_version         VARCHAR(50),
    confidence_pct        NUMERIC(6,2) NOT NULL DEFAULT 0
);
```

### slv_sc_returns_to_supplier

```sql
CREATE TABLE slv_sc_returns_to_supplier (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- return_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    return_id             VARCHAR(100) NOT NULL,
    po_id                 VARCHAR(100) NOT NULL,
    supplier_id           VARCHAR(100) NOT NULL,
    item_id               VARCHAR(100) NOT NULL,
    return_date           DATE NOT NULL,
    quantity              NUMERIC(15,3) NOT NULL DEFAULT 0,
    reason_code           VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    credit_note_no        VARCHAR(100),
    status                VARCHAR(50) NOT NULL DEFAULT 'PENDING'
);
```

### slv_sc_warehouse_locations

```sql
CREATE TABLE slv_sc_warehouse_locations (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- warehouse_id + zone + aisle + rack + bin
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    location_id           VARCHAR(100) NOT NULL,
    warehouse_id          VARCHAR(100) NOT NULL,
    zone                  VARCHAR(20) NOT NULL DEFAULT 'A',
    aisle                 VARCHAR(10) NOT NULL DEFAULT '01',
    rack                  VARCHAR(10) NOT NULL DEFAULT '01',
    bin                   VARCHAR(10) NOT NULL DEFAULT '01',
    capacity_units        INTEGER NOT NULL DEFAULT 0,
    current_units         INTEGER NOT NULL DEFAULT 0,
    utilization_pct       NUMERIC(8,4) GENERATED ALWAYS AS (
                            CASE WHEN capacity_units > 0
                            THEN current_units::NUMERIC / capacity_units * 100 ELSE 0 END
                          ) STORED,
    is_active             BOOLEAN NOT NULL DEFAULT TRUE
);
```

### slv_sc_quality_holds

```sql
CREATE TABLE slv_sc_quality_holds (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- hold_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    hold_id               VARCHAR(100) NOT NULL,
    item_id               VARCHAR(100) NOT NULL,
    warehouse_id          VARCHAR(100) NOT NULL,
    quantity_held         NUMERIC(15,3) NOT NULL DEFAULT 0,
    reason                TEXT NOT NULL DEFAULT '',
    hold_date             DATE NOT NULL,
    release_date          DATE,
    days_on_hold          INTEGER GENERATED ALWAYS AS (
                            COALESCE(release_date, CURRENT_DATE) - hold_date
                          ) STORED,
    disposition           VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    status                VARCHAR(50) NOT NULL DEFAULT 'OPEN'
);
```

---

## 📂 Sector 9 — Telecommunications

### slv_tel_subscribers

```sql
CREATE TABLE slv_tel_subscribers (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- msisdn
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    subscriber_id         VARCHAR(100) NOT NULL,
    msisdn                VARCHAR(20) NOT NULL,
    sim_iccid             VARCHAR(50),
    plan_id               VARCHAR(100) NOT NULL,
    activation_date       DATE,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    customer_id           VARCHAR(100),
    network_type          VARCHAR(20) NOT NULL DEFAULT 'UNKNOWN'
);
```

### slv_tel_call_detail_records

```sql
CREATE TABLE slv_tel_call_detail_records (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- cdr_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    cdr_id                VARCHAR(100) NOT NULL,
    caller_msisdn         VARCHAR(20) NOT NULL,
    callee_msisdn         VARCHAR(20) NOT NULL,
    call_start            TIMESTAMP NOT NULL,
    call_end              TIMESTAMP,
    duration_seconds      INTEGER NOT NULL DEFAULT 0,
    call_type             VARCHAR(20) NOT NULL DEFAULT 'VOICE',
    direction             VARCHAR(10) NOT NULL DEFAULT 'UNKNOWN',
    cell_id               VARCHAR(50),
    roaming               BOOLEAN NOT NULL DEFAULT FALSE,
    charge_amount         NUMERIC(20,6) NOT NULL DEFAULT 0
);
```

### slv_tel_data_usage

```sql
CREATE TABLE slv_tel_data_usage (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- usage_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    usage_id              VARCHAR(100) NOT NULL,
    subscriber_id         VARCHAR(100) NOT NULL,
    session_start         TIMESTAMP NOT NULL,
    session_end           TIMESTAMP,
    bytes_uploaded        BIGINT NOT NULL DEFAULT 0,
    bytes_downloaded      BIGINT NOT NULL DEFAULT 0,
    total_bytes           BIGINT GENERATED ALWAYS AS (bytes_uploaded + bytes_downloaded) STORED,
    apn                   VARCHAR(100),
    cell_id               VARCHAR(50),
    roaming               BOOLEAN NOT NULL DEFAULT FALSE
);
```

### slv_tel_network_events

```sql
CREATE TABLE slv_tel_network_events (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    event_id              VARCHAR(100) NOT NULL,
    node_id               VARCHAR(100) NOT NULL,
    event_type            VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    severity              VARCHAR(20) NOT NULL DEFAULT 'LOW',
    event_start           TIMESTAMP NOT NULL,
    event_end             TIMESTAMP,
    duration_minutes      INTEGER GENERATED ALWAYS AS (
                            CASE WHEN event_end IS NOT NULL
                            THEN EXTRACT(EPOCH FROM (event_end - event_start))::INTEGER / 60 ELSE NULL END
                          ) STORED,
    description           TEXT
);
```

### slv_tel_plans

```sql
CREATE TABLE slv_tel_plans (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- plan_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    plan_id               VARCHAR(100) NOT NULL,
    plan_name             VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    plan_type             VARCHAR(50) NOT NULL DEFAULT 'PREPAID',
    monthly_fee           NUMERIC(20,4) NOT NULL DEFAULT 0,
    data_quota_gb         NUMERIC(10,2) NOT NULL DEFAULT 0,
    voice_minutes         INTEGER NOT NULL DEFAULT 0,
    sms_count             INTEGER NOT NULL DEFAULT 0,
    network_type          VARCHAR(20) NOT NULL DEFAULT 'UNKNOWN',
    is_active             BOOLEAN NOT NULL DEFAULT TRUE
);
```

### slv_tel_billing

```sql
CREATE TABLE slv_tel_billing (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- bill_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    bill_id               VARCHAR(100) NOT NULL,
    subscriber_id         VARCHAR(100) NOT NULL,
    billing_period        VARCHAR(20) NOT NULL DEFAULT 'UNKNOWN',
    bill_date             DATE NOT NULL,
    due_date              DATE NOT NULL,
    base_charge           NUMERIC(20,4) NOT NULL DEFAULT 0,
    usage_charge          NUMERIC(20,4) NOT NULL DEFAULT 0,
    roaming_charge        NUMERIC(20,4) NOT NULL DEFAULT 0,
    tax                   NUMERIC(20,4) NOT NULL DEFAULT 0,
    total_amount          NUMERIC(20,4) NOT NULL DEFAULT 0,
    days_overdue          INTEGER GENERATED ALWAYS AS (
                            CASE WHEN due_date < CURRENT_DATE AND status NOT IN ('PAID','CANCELLED')
                            THEN CURRENT_DATE - due_date ELSE 0 END
                          ) STORED,
    status                VARCHAR(50) NOT NULL DEFAULT 'PENDING'
);
```

### slv_tel_tower_inventory

```sql
CREATE TABLE slv_tel_tower_inventory (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- cell_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    tower_id              VARCHAR(100) NOT NULL,
    cell_id               VARCHAR(50) NOT NULL,
    tower_type            VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    latitude              NUMERIC(10,7),
    longitude             NUMERIC(10,7),
    region                VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    network_type          VARCHAR(20) NOT NULL DEFAULT 'UNKNOWN',
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    install_date          DATE,
    operator_id           VARCHAR(100)
);
```

### slv_tel_complaints

```sql
CREATE TABLE slv_tel_complaints (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- complaint_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    complaint_id          VARCHAR(100) NOT NULL,
    subscriber_id         VARCHAR(100) NOT NULL,
    complaint_type        VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    channel               VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    submitted_at          TIMESTAMP NOT NULL,
    resolved_at           TIMESTAMP,
    resolution_hours      NUMERIC(10,2) GENERATED ALWAYS AS (
                            CASE WHEN resolved_at IS NOT NULL
                            THEN EXTRACT(EPOCH FROM (resolved_at - submitted_at)) / 3600 ELSE NULL END
                          ) STORED,
    resolution            TEXT,
    satisfaction_score    INTEGER,
    status                VARCHAR(50) NOT NULL DEFAULT 'OPEN'
);
```

### slv_tel_roaming_agreements

```sql
CREATE TABLE slv_tel_roaming_agreements (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- agreement_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    agreement_id          VARCHAR(100) NOT NULL,
    partner_operator      VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    country_code          CHAR(3) NOT NULL,
    voice_rate            NUMERIC(10,6) NOT NULL DEFAULT 0,
    data_rate_per_mb      NUMERIC(10,6) NOT NULL DEFAULT 0,
    sms_rate              NUMERIC(10,6) NOT NULL DEFAULT 0,
    effective_date        DATE NOT NULL,
    expiry_date           DATE,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    is_expired            BOOLEAN GENERATED ALWAYS AS (expiry_date < CURRENT_DATE) STORED
);
```

---

## 📂 Sector 10 — Energy & Utilities

### slv_ene_meters

```sql
CREATE TABLE slv_ene_meters (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- meter_serial
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    meter_id              VARCHAR(100) NOT NULL,
    meter_serial          VARCHAR(100) NOT NULL,
    meter_type            VARCHAR(50) NOT NULL DEFAULT 'ELECTRICITY',
    customer_id           VARCHAR(100),
    service_point_id      VARCHAR(100),
    install_date          DATE,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    latitude              NUMERIC(10,7),
    longitude             NUMERIC(10,7)
);
```

### slv_ene_meter_readings

```sql
CREATE TABLE slv_ene_meter_readings (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- meter_id + reading_date
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    reading_id            VARCHAR(100) NOT NULL,
    meter_id              VARCHAR(100) NOT NULL,
    reading_date          TIMESTAMP NOT NULL,
    reading_value         NUMERIC(15,4) NOT NULL DEFAULT 0,
    reading_unit          VARCHAR(20) NOT NULL DEFAULT 'kWh',
    reading_type          VARCHAR(20) NOT NULL DEFAULT 'ACTUAL',
    quality_flag          VARCHAR(20) NOT NULL DEFAULT 'OK'
);
```

### slv_ene_grid_events

```sql
CREATE TABLE slv_ene_grid_events (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    event_id              VARCHAR(100) NOT NULL,
    substation_id         VARCHAR(100) NOT NULL,
    event_type            VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    severity              VARCHAR(20) NOT NULL DEFAULT 'LOW',
    event_start           TIMESTAMP NOT NULL,
    event_end             TIMESTAMP,
    outage_duration_min   INTEGER GENERATED ALWAYS AS (
                            CASE WHEN event_end IS NOT NULL
                            THEN EXTRACT(EPOCH FROM (event_end - event_start))::INTEGER / 60 ELSE NULL END
                          ) STORED,
    affected_customers    INTEGER NOT NULL DEFAULT 0,
    cause_code            VARCHAR(50)
);
```

### slv_ene_generation_assets

```sql
CREATE TABLE slv_ene_generation_assets (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    asset_id              VARCHAR(100) NOT NULL,
    asset_name            VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    asset_type            VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    capacity_mw           NUMERIC(10,3) NOT NULL DEFAULT 0,
    location              VARCHAR(255),
    commission_date       DATE,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    operator_id           VARCHAR(100)
);
```

### slv_ene_tariffs

```sql
CREATE TABLE slv_ene_tariffs (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- tariff_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    tariff_id             VARCHAR(100) NOT NULL,
    tariff_name           VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    utility_type          VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    customer_class        VARCHAR(50) NOT NULL DEFAULT 'RESIDENTIAL',
    effective_date        DATE NOT NULL,
    expiry_date           DATE,
    rate_per_unit         NUMERIC(15,6) NOT NULL DEFAULT 0,
    unit                  VARCHAR(20) NOT NULL DEFAULT 'kWh',
    fixed_charge          NUMERIC(20,4) NOT NULL DEFAULT 0,
    is_tou                BOOLEAN NOT NULL DEFAULT FALSE,
    is_active             BOOLEAN GENERATED ALWAYS AS (
                            expiry_date IS NULL OR expiry_date >= CURRENT_DATE
                          ) STORED
);
```

### slv_ene_work_orders

```sql
CREATE TABLE slv_ene_work_orders (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- work_order_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    work_order_id         VARCHAR(100) NOT NULL,
    order_type            VARCHAR(50) NOT NULL DEFAULT 'REPAIR',
    asset_id              VARCHAR(100) NOT NULL,
    priority              VARCHAR(20) NOT NULL DEFAULT 'NORMAL',
    assigned_to           VARCHAR(100),
    scheduled_date        DATE,
    completed_date        DATE,
    cost                  NUMERIC(20,4) NOT NULL DEFAULT 0,
    status                VARCHAR(50) NOT NULL DEFAULT 'OPEN',
    notes                 TEXT,
    days_to_complete      INTEGER GENERATED ALWAYS AS (
                            CASE WHEN completed_date IS NOT NULL AND scheduled_date IS NOT NULL
                            THEN completed_date - scheduled_date ELSE NULL END
                          ) STORED
);
```

### slv_ene_renewable_output

```sql
CREATE TABLE slv_ene_renewable_output (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- asset_id + reading_timestamp
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    output_id             VARCHAR(100) NOT NULL,
    asset_id              VARCHAR(100) NOT NULL,
    reading_timestamp     TIMESTAMP NOT NULL,
    output_mwh            NUMERIC(15,6) NOT NULL DEFAULT 0,
    capacity_factor       NUMERIC(8,4) NOT NULL DEFAULT 0,
    weather_condition     VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    irradiance            NUMERIC(10,4),
    wind_speed_ms         NUMERIC(8,2)
);
```

### slv_ene_customer_accounts

```sql
CREATE TABLE slv_ene_customer_accounts (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- account_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    account_id            VARCHAR(100) NOT NULL,
    customer_id           VARCHAR(100) NOT NULL,
    tariff_id             VARCHAR(100) NOT NULL,
    service_type          VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    city                  VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    country               CHAR(2) NOT NULL DEFAULT 'XX',
    start_date            DATE NOT NULL,
    end_date              DATE,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE'
);
```

### slv_ene_bills

```sql
CREATE TABLE slv_ene_bills (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- bill_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    bill_id               VARCHAR(100) NOT NULL,
    account_id            VARCHAR(100) NOT NULL,
    bill_date             DATE NOT NULL,
    due_date              DATE NOT NULL,
    consumption_units     NUMERIC(15,4) NOT NULL DEFAULT 0,
    unit_rate             NUMERIC(15,6) NOT NULL DEFAULT 0,
    energy_charge         NUMERIC(20,4) NOT NULL DEFAULT 0,
    fixed_charge          NUMERIC(20,4) NOT NULL DEFAULT 0,
    tax                   NUMERIC(20,4) NOT NULL DEFAULT 0,
    total_amount          NUMERIC(20,4) NOT NULL DEFAULT 0,
    days_overdue          INTEGER GENERATED ALWAYS AS (
                            CASE WHEN due_date < CURRENT_DATE AND status NOT IN ('PAID','CANCELLED')
                            THEN CURRENT_DATE - due_date ELSE 0 END
                          ) STORED,
    status                VARCHAR(50) NOT NULL DEFAULT 'PENDING'
);
```

---

## 📂 Sector 11 — Agriculture

### slv_agr_farms

```sql
CREATE TABLE slv_agr_farms (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    farm_id               VARCHAR(100) NOT NULL,
    farm_name             VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    owner_id              VARCHAR(100) NOT NULL,
    total_area_ha         NUMERIC(15,4) NOT NULL DEFAULT 0,
    region                VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    country               CHAR(2) NOT NULL DEFAULT 'XX',
    latitude              NUMERIC(10,7),
    longitude             NUMERIC(10,7),
    primary_crop          VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    certification         VARCHAR(100)
);
```

### slv_agr_crop_cycles

```sql
CREATE TABLE slv_agr_crop_cycles (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    cycle_id              VARCHAR(100) NOT NULL,
    farm_id               VARCHAR(100) NOT NULL,
    field_id              VARCHAR(100),
    crop_id               VARCHAR(100) NOT NULL,
    crop_variety          VARCHAR(100),
    planting_date         DATE NOT NULL,
    harvest_date          DATE,
    area_planted_ha       NUMERIC(15,4) NOT NULL DEFAULT 0,
    yield_kg              NUMERIC(15,3) NOT NULL DEFAULT 0,
    yield_per_ha          NUMERIC(15,4) GENERATED ALWAYS AS (
                            CASE WHEN area_planted_ha > 0
                            THEN yield_kg / area_planted_ha ELSE 0 END
                          ) STORED,
    status                VARCHAR(50) NOT NULL DEFAULT 'PLANTED'
);
```

### slv_agr_field_sensors

```sql
CREATE TABLE slv_agr_field_sensors (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- sensor_id + recorded_at
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    sensor_id             VARCHAR(100) NOT NULL,
    farm_id               VARCHAR(100) NOT NULL,
    field_id              VARCHAR(100),
    sensor_type           VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    recorded_at           TIMESTAMP NOT NULL,
    value                 NUMERIC(15,6) NOT NULL DEFAULT 0,
    unit                  VARCHAR(20) NOT NULL DEFAULT 'UNKNOWN',
    battery_level         NUMERIC(5,2) NOT NULL DEFAULT 100
);
```

### slv_agr_inputs_applied

```sql
CREATE TABLE slv_agr_inputs_applied (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    application_id        VARCHAR(100) NOT NULL,
    cycle_id              VARCHAR(100) NOT NULL,
    field_id              VARCHAR(100),
    input_type            VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    product_name          VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    quantity_applied      NUMERIC(15,4) NOT NULL DEFAULT 0,
    uom                   VARCHAR(20) NOT NULL DEFAULT 'KG',
    application_date      DATE NOT NULL,
    applicator_id         VARCHAR(100)
);
```

### slv_agr_livestock

```sql
CREATE TABLE slv_agr_livestock (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- tag_number
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    animal_id             VARCHAR(100) NOT NULL,
    farm_id               VARCHAR(100) NOT NULL,
    species               VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    breed                 VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    date_of_birth         DATE,
    gender                VARCHAR(10) NOT NULL DEFAULT 'UNKNOWN',
    weight_kg             NUMERIC(8,2) NOT NULL DEFAULT 0,
    health_status         VARCHAR(50) NOT NULL DEFAULT 'HEALTHY',
    tag_number            VARCHAR(50) NOT NULL,
    acquired_date         DATE
);
```

### slv_agr_weather_observations

```sql
CREATE TABLE slv_agr_weather_observations (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- farm_id + station_id + observed_at
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    observation_id        VARCHAR(100) NOT NULL,
    farm_id               VARCHAR(100) NOT NULL,
    station_id            VARCHAR(100) NOT NULL,
    observed_at           TIMESTAMP NOT NULL,
    temp_max_c            NUMERIC(6,2),
    temp_min_c            NUMERIC(6,2),
    temp_range_c          NUMERIC(6,2) GENERATED ALWAYS AS (temp_max_c - temp_min_c) STORED,
    rainfall_mm           NUMERIC(8,2) NOT NULL DEFAULT 0,
    humidity_pct          NUMERIC(6,2) NOT NULL DEFAULT 0,
    wind_speed_ms         NUMERIC(8,2) NOT NULL DEFAULT 0,
    solar_rad             NUMERIC(10,4)
);
```

### slv_agr_pest_disease_reports

```sql
CREATE TABLE slv_agr_pest_disease_reports (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- report_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    report_id             VARCHAR(100) NOT NULL,
    farm_id               VARCHAR(100) NOT NULL,
    field_id              VARCHAR(100),
    report_date           DATE NOT NULL,
    pest_disease_name     VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    category              VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    severity              VARCHAR(20) NOT NULL DEFAULT 'LOW',
    affected_area_ha      NUMERIC(10,4) NOT NULL DEFAULT 0,
    treatment_applied     TEXT
);
```

### slv_agr_equipment

```sql
CREATE TABLE slv_agr_equipment (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- equipment_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    equipment_id          VARCHAR(100) NOT NULL,
    farm_id               VARCHAR(100) NOT NULL,
    equipment_type        VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    brand                 VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    model                 VARCHAR(100),
    year                  INTEGER,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    last_service_date     DATE
);
```

### slv_agr_market_prices

```sql
CREATE TABLE slv_agr_market_prices (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- crop_id + market_name + price_date + price_type
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    price_id              VARCHAR(100) NOT NULL,
    crop_id               VARCHAR(100) NOT NULL,
    market_name           VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    price_date            DATE NOT NULL,
    price_per_kg          NUMERIC(15,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    price_type            VARCHAR(30) NOT NULL DEFAULT 'FARM_GATE'
);
```

---

## 📂 Sector 12 — Transportation

### slv_trn_routes

```sql
CREATE TABLE slv_trn_routes (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- route_code
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    route_id              VARCHAR(100) NOT NULL,
    route_code            VARCHAR(50) NOT NULL,
    route_name            VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    transport_mode        VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    origin_code           VARCHAR(50) NOT NULL,
    destination_code      VARCHAR(50) NOT NULL,
    distance_km           NUMERIC(10,2) NOT NULL DEFAULT 0,
    estimated_minutes     INTEGER NOT NULL DEFAULT 0,
    is_active             BOOLEAN NOT NULL DEFAULT TRUE
);
```

### slv_trn_trips

```sql
CREATE TABLE slv_trn_trips (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- trip_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    trip_id               VARCHAR(100) NOT NULL,
    route_id              VARCHAR(100) NOT NULL,
    vehicle_id            VARCHAR(100) NOT NULL,
    driver_id             VARCHAR(100),
    scheduled_departure   TIMESTAMP NOT NULL,
    actual_departure      TIMESTAMP,
    scheduled_arrival     TIMESTAMP,
    actual_arrival        TIMESTAMP,
    delay_minutes         INTEGER GENERATED ALWAYS AS (
                            CASE WHEN actual_arrival IS NOT NULL AND scheduled_arrival IS NOT NULL
                            THEN EXTRACT(EPOCH FROM (actual_arrival - scheduled_arrival))::INTEGER / 60 ELSE NULL END
                          ) STORED,
    status                VARCHAR(50) NOT NULL DEFAULT 'SCHEDULED',
    passengers_count      INTEGER NOT NULL DEFAULT 0
);
```

### slv_trn_tickets

```sql
CREATE TABLE slv_trn_tickets (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- ticket_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    ticket_id             VARCHAR(100) NOT NULL,
    trip_id               VARCHAR(100) NOT NULL,
    passenger_id          VARCHAR(100),
    ticket_class          VARCHAR(50) NOT NULL DEFAULT 'ECONOMY',
    seat_number           VARCHAR(20),
    fare_amount           NUMERIC(20,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    booking_date          TIMESTAMP NOT NULL,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE'
);
```

### slv_trn_vehicle_gps

```sql
CREATE TABLE slv_trn_vehicle_gps (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- vehicle_id + recorded_at
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    gps_id                VARCHAR(100) NOT NULL,
    vehicle_id            VARCHAR(100) NOT NULL,
    trip_id               VARCHAR(100),
    recorded_at           TIMESTAMP NOT NULL,
    latitude              NUMERIC(10,7) NOT NULL,
    longitude             NUMERIC(10,7) NOT NULL,
    speed_kmh             NUMERIC(8,2) NOT NULL DEFAULT 0,
    heading_degrees       NUMERIC(6,2) NOT NULL DEFAULT 0
);
```

### slv_trn_drivers

```sql
CREATE TABLE slv_trn_drivers (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- license_number
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    driver_id             VARCHAR(100) NOT NULL,
    first_name            VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    last_name             VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    license_number        VARCHAR(100) NOT NULL,
    license_class         VARCHAR(20) NOT NULL DEFAULT 'UNKNOWN',
    license_expiry        DATE,
    date_of_birth         DATE,
    hire_date             DATE,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    carrier_id            VARCHAR(100),
    is_license_valid      BOOLEAN GENERATED ALWAYS AS (
                            license_expiry IS NULL OR license_expiry >= CURRENT_DATE
                          ) STORED
);
```

### slv_trn_incidents

```sql
CREATE TABLE slv_trn_incidents (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- incident_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    incident_id           VARCHAR(100) NOT NULL,
    trip_id               VARCHAR(100),
    vehicle_id            VARCHAR(100) NOT NULL,
    driver_id             VARCHAR(100),
    incident_type         VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    incident_date         TIMESTAMP NOT NULL,
    latitude              NUMERIC(10,7),
    longitude             NUMERIC(10,7),
    severity              VARCHAR(20) NOT NULL DEFAULT 'LOW',
    description           TEXT,
    status                VARCHAR(50) NOT NULL DEFAULT 'OPEN'
);
```

### slv_trn_stops

```sql
CREATE TABLE slv_trn_stops (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- stop_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    stop_id               VARCHAR(100) NOT NULL,
    stop_name             VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    stop_type             VARCHAR(50) NOT NULL DEFAULT 'INTERMEDIATE',
    route_id              VARCHAR(100) NOT NULL,
    sequence_no           INTEGER NOT NULL DEFAULT 0,
    latitude              NUMERIC(10,7),
    longitude             NUMERIC(10,7),
    scheduled_time        TIME,
    is_active             BOOLEAN NOT NULL DEFAULT TRUE
);
```

### slv_trn_fuel_logs

```sql
CREATE TABLE slv_trn_fuel_logs (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- log_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    log_id                VARCHAR(100) NOT NULL,
    vehicle_id            VARCHAR(100) NOT NULL,
    trip_id               VARCHAR(100),
    fill_date             DATE NOT NULL,
    liters_filled         NUMERIC(10,3) NOT NULL DEFAULT 0,
    cost_per_liter        NUMERIC(10,4) NOT NULL DEFAULT 0,
    total_cost            NUMERIC(20,4) NOT NULL DEFAULT 0,
    odometer_km           NUMERIC(12,2) NOT NULL DEFAULT 0,
    station_id            VARCHAR(100)
);
```

### slv_trn_passenger_feedback

```sql
CREATE TABLE slv_trn_passenger_feedback (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- feedback_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    feedback_id           VARCHAR(100) NOT NULL,
    trip_id               VARCHAR(100) NOT NULL,
    passenger_id          VARCHAR(100),
    submitted_at          TIMESTAMP NOT NULL,
    rating                SMALLINT NOT NULL DEFAULT 3,
    punctuality_score     SMALLINT NOT NULL DEFAULT 3,
    cleanliness_score     SMALLINT NOT NULL DEFAULT 3,
    staff_score           SMALLINT NOT NULL DEFAULT 3,
    avg_score             NUMERIC(4,2) GENERATED ALWAYS AS (
                            (rating + punctuality_score + cleanliness_score + staff_score)::NUMERIC / 4
                          ) STORED,
    comments              TEXT
);
```

---

## 📂 Sector 13 — Real Estate

### slv_re_properties

```sql
CREATE TABLE slv_re_properties (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- property_code
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    property_id           VARCHAR(100) NOT NULL,
    property_code         VARCHAR(50) NOT NULL,
    property_type         VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    city                  VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    region                VARCHAR(100),
    country               CHAR(2) NOT NULL DEFAULT 'XX',
    latitude              NUMERIC(10,7),
    longitude             NUMERIC(10,7),
    land_area_sqm         NUMERIC(15,4) NOT NULL DEFAULT 0,
    floor_area_sqm        NUMERIC(15,4) NOT NULL DEFAULT 0,
    year_built            INTEGER,
    status                VARCHAR(50) NOT NULL DEFAULT 'AVAILABLE',
    owner_id              VARCHAR(100)
);
```

### slv_re_listings

```sql
CREATE TABLE slv_re_listings (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- listing_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    listing_id            VARCHAR(100) NOT NULL,
    property_id           VARCHAR(100) NOT NULL,
    listing_type          VARCHAR(20) NOT NULL DEFAULT 'SALE',
    asking_price          NUMERIC(20,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    listing_date          DATE NOT NULL,
    expiry_date           DATE,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    agent_id              VARCHAR(100)
);
```

### slv_re_transactions

```sql
CREATE TABLE slv_re_transactions (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    transaction_id        VARCHAR(100) NOT NULL,
    property_id           VARCHAR(100) NOT NULL,
    listing_id            VARCHAR(100),
    transaction_type      VARCHAR(20) NOT NULL DEFAULT 'SALE',
    buyer_id              VARCHAR(100),
    seller_id             VARCHAR(100),
    transaction_date      DATE NOT NULL,
    sale_price            NUMERIC(20,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    agent_id              VARCHAR(100)
);
```

### slv_re_leases

```sql
CREATE TABLE slv_re_leases (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- lease_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    lease_id              VARCHAR(100) NOT NULL,
    property_id           VARCHAR(100) NOT NULL,
    tenant_id             VARCHAR(100) NOT NULL,
    landlord_id           VARCHAR(100),
    lease_start           DATE NOT NULL,
    lease_end             DATE,
    lease_term_months     INTEGER GENERATED ALWAYS AS (
                            CASE WHEN lease_end IS NOT NULL
                            THEN (EXTRACT(YEAR FROM lease_end) - EXTRACT(YEAR FROM lease_start)) * 12
                                 + (EXTRACT(MONTH FROM lease_end) - EXTRACT(MONTH FROM lease_start))
                            ELSE NULL END
                          ) STORED,
    monthly_rent          NUMERIC(20,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    deposit_amount        NUMERIC(20,4) NOT NULL DEFAULT 0,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE'
);
```

### slv_re_agents

```sql
CREATE TABLE slv_re_agents (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- license_number
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    agent_id              VARCHAR(100) NOT NULL,
    first_name            VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    last_name             VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    license_number        VARCHAR(100) NOT NULL,
    agency_id             VARCHAR(100),
    email                 VARCHAR(255),
    phone                 VARCHAR(50),
    specialization        VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    active_since          DATE,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE'
);
```

### slv_re_valuations

```sql
CREATE TABLE slv_re_valuations (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- valuation_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    valuation_id          VARCHAR(100) NOT NULL,
    property_id           VARCHAR(100) NOT NULL,
    valuation_date        DATE NOT NULL,
    valuation_method      VARCHAR(50) NOT NULL DEFAULT 'MARKET',
    appraised_value       NUMERIC(20,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    appraiser_id          VARCHAR(100),
    purpose               VARCHAR(50) NOT NULL DEFAULT 'SALE'
);
```

### slv_re_maintenance_requests

```sql
CREATE TABLE slv_re_maintenance_requests (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- request_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    request_id            VARCHAR(100) NOT NULL,
    property_id           VARCHAR(100) NOT NULL,
    tenant_id             VARCHAR(100),
    category              VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    description           TEXT NOT NULL DEFAULT '',
    priority              VARCHAR(20) NOT NULL DEFAULT 'NORMAL',
    submitted_at          TIMESTAMP NOT NULL,
    resolved_at           TIMESTAMP,
    resolution_hours      NUMERIC(10,2) GENERATED ALWAYS AS (
                            CASE WHEN resolved_at IS NOT NULL
                            THEN EXTRACT(EPOCH FROM (resolved_at - submitted_at)) / 3600 ELSE NULL END
                          ) STORED,
    cost                  NUMERIC(20,4) NOT NULL DEFAULT 0,
    status                VARCHAR(50) NOT NULL DEFAULT 'OPEN'
);
```

### slv_re_inspections

```sql
CREATE TABLE slv_re_inspections (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- inspection_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    inspection_id         VARCHAR(100) NOT NULL,
    property_id           VARCHAR(100) NOT NULL,
    inspection_type       VARCHAR(50) NOT NULL DEFAULT 'ROUTINE',
    inspector_id          VARCHAR(100),
    inspection_date       DATE NOT NULL,
    overall_condition     VARCHAR(20) NOT NULL DEFAULT 'UNKNOWN',
    notes                 TEXT,
    report_url            TEXT
);
```

### slv_re_mortgages

```sql
CREATE TABLE slv_re_mortgages (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- mortgage_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    mortgage_id           VARCHAR(100) NOT NULL,
    property_id           VARCHAR(100) NOT NULL,
    borrower_id           VARCHAR(100) NOT NULL,
    lender_id             VARCHAR(100) NOT NULL,
    principal             NUMERIC(20,4) NOT NULL DEFAULT 0,
    interest_rate         NUMERIC(8,4) NOT NULL DEFAULT 0,
    term_years            INTEGER NOT NULL DEFAULT 0,
    start_date            DATE NOT NULL,
    maturity_date         DATE,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE'
);
```

---

## 📂 Sector 14 — Human Resources

### slv_hr_employees

```sql
CREATE TABLE slv_hr_employees (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- employee_number
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    employee_id           VARCHAR(100) NOT NULL,
    employee_number       VARCHAR(50) NOT NULL,
    first_name            VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    last_name             VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    date_of_birth         DATE,
    gender                VARCHAR(20) NOT NULL DEFAULT 'UNKNOWN',
    email                 VARCHAR(255),
    phone                 VARCHAR(50),
    hire_date             DATE NOT NULL,
    termination_date      DATE,
    department_id         VARCHAR(100) NOT NULL,
    job_id                VARCHAR(100) NOT NULL,
    manager_id            VARCHAR(100),
    employment_type       VARCHAR(50) NOT NULL DEFAULT 'FULL_TIME',
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    tenure_days           INTEGER GENERATED ALWAYS AS (
                            COALESCE(termination_date, CURRENT_DATE) - hire_date
                          ) STORED
);
```

### slv_hr_payroll

```sql
CREATE TABLE slv_hr_payroll (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- employee_id + pay_period_start
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    payroll_id            VARCHAR(100) NOT NULL,
    employee_id           VARCHAR(100) NOT NULL,
    pay_period_start      DATE NOT NULL,
    pay_period_end        DATE NOT NULL,
    basic_salary          NUMERIC(20,4) NOT NULL DEFAULT 0,
    allowances            NUMERIC(20,4) NOT NULL DEFAULT 0,
    overtime              NUMERIC(20,4) NOT NULL DEFAULT 0,
    gross_pay             NUMERIC(20,4) NOT NULL DEFAULT 0,
    deductions            NUMERIC(20,4) NOT NULL DEFAULT 0,
    net_pay               NUMERIC(20,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    payment_date          DATE
);
```

### slv_hr_attendance

```sql
CREATE TABLE slv_hr_attendance (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- employee_id + work_date
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    attendance_id         VARCHAR(100) NOT NULL,
    employee_id           VARCHAR(100) NOT NULL,
    work_date             DATE NOT NULL,
    time_in               TIMESTAMP,
    time_out              TIMESTAMP,
    hours_worked          NUMERIC(6,2) NOT NULL DEFAULT 0,
    overtime_hours        NUMERIC(6,2) NOT NULL DEFAULT 0,
    status                VARCHAR(50) NOT NULL DEFAULT 'PRESENT'
);
```

### slv_hr_performance_reviews

```sql
CREATE TABLE slv_hr_performance_reviews (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- review_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    review_id             VARCHAR(100) NOT NULL,
    employee_id           VARCHAR(100) NOT NULL,
    reviewer_id           VARCHAR(100) NOT NULL,
    review_period         VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    review_date           DATE NOT NULL,
    overall_rating        NUMERIC(4,2) NOT NULL DEFAULT 0,
    goals_rating          NUMERIC(4,2) NOT NULL DEFAULT 0,
    competency_rating     NUMERIC(4,2) NOT NULL DEFAULT 0,
    comments              TEXT,
    status                VARCHAR(50) NOT NULL DEFAULT 'DRAFT'
);
```

### slv_hr_job_postings

```sql
CREATE TABLE slv_hr_job_postings (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- posting_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    posting_id            VARCHAR(100) NOT NULL,
    job_title             VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    department_id         VARCHAR(100) NOT NULL,
    location              VARCHAR(255),
    employment_type       VARCHAR(50) NOT NULL DEFAULT 'FULL_TIME',
    salary_min            NUMERIC(20,4) NOT NULL DEFAULT 0,
    salary_max            NUMERIC(20,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    posted_date           DATE NOT NULL,
    closing_date          DATE,
    status                VARCHAR(50) NOT NULL DEFAULT 'OPEN'
);
```

### slv_hr_training

```sql
CREATE TABLE slv_hr_training (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- training_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    training_id           VARCHAR(100) NOT NULL,
    employee_id           VARCHAR(100) NOT NULL,
    course_name           VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    training_type         VARCHAR(50) NOT NULL DEFAULT 'SKILLS',
    provider              VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    start_date            DATE NOT NULL,
    end_date              DATE,
    duration_hours        NUMERIC(6,2) NOT NULL DEFAULT 0,
    status                VARCHAR(50) NOT NULL DEFAULT 'ENROLLED',
    score                 NUMERIC(6,2),
    certified             BOOLEAN NOT NULL DEFAULT FALSE
);
```

### slv_hr_benefits

```sql
CREATE TABLE slv_hr_benefits (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- enrollment_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    enrollment_id         VARCHAR(100) NOT NULL,
    employee_id           VARCHAR(100) NOT NULL,
    benefit_type          VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    plan_name             VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    start_date            DATE NOT NULL,
    end_date              DATE,
    employee_contrib      NUMERIC(20,4) NOT NULL DEFAULT 0,
    employer_contrib      NUMERIC(20,4) NOT NULL DEFAULT 0,
    total_contrib         NUMERIC(20,4) GENERATED ALWAYS AS (employee_contrib + employer_contrib) STORED,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE'
);
```

### slv_hr_disciplinary

```sql
CREATE TABLE slv_hr_disciplinary (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- case_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    case_id               VARCHAR(100) NOT NULL,
    employee_id           VARCHAR(100) NOT NULL,
    incident_date         DATE NOT NULL,
    incident_type         VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    severity              VARCHAR(20) NOT NULL DEFAULT 'LOW',
    action_taken          VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    issued_by             VARCHAR(100),
    issued_date           DATE,
    appeal_status         VARCHAR(50) NOT NULL DEFAULT 'NOT_APPEALED',
    status                VARCHAR(50) NOT NULL DEFAULT 'OPEN'
);
```

### slv_hr_offboarding

```sql
CREATE TABLE slv_hr_offboarding (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- employee_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    offboarding_id        VARCHAR(100) NOT NULL,
    employee_id           VARCHAR(100) NOT NULL,
    notice_date           DATE,
    last_day              DATE,
    tenure_days           INTEGER GENERATED ALWAYS AS (
                            CASE WHEN notice_date IS NOT NULL AND last_day IS NOT NULL
                            THEN last_day - notice_date ELSE NULL END
                          ) STORED,
    exit_reason           VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    exit_interview        BOOLEAN NOT NULL DEFAULT FALSE,
    rehire_eligible       BOOLEAN NOT NULL DEFAULT FALSE,
    clearance_status      VARCHAR(50) NOT NULL DEFAULT 'PENDING'
);
```

### slv_hr_org_structure

```sql
CREATE TABLE slv_hr_org_structure (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- node_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    node_id               VARCHAR(100) NOT NULL,
    node_type             VARCHAR(50) NOT NULL DEFAULT 'DEPARTMENT',
    node_name             VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    parent_node_id        VARCHAR(100),
    level                 INTEGER NOT NULL DEFAULT 0,
    cost_center           VARCHAR(100),
    head_employee_id      VARCHAR(100),
    effective_date        DATE NOT NULL,
    is_root               BOOLEAN GENERATED ALWAYS AS (parent_node_id IS NULL) STORED
);
```

---

## 📂 Sector 15 — Insurance

### slv_ins_policies

```sql
CREATE TABLE slv_ins_policies (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- policy_number
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    policy_id             VARCHAR(100) NOT NULL,
    policy_number         VARCHAR(50) NOT NULL,
    policyholder_id       VARCHAR(100) NOT NULL,
    product_id            VARCHAR(100) NOT NULL,
    policy_type           VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    start_date            DATE NOT NULL,
    end_date              DATE,
    premium_amount        NUMERIC(20,4) NOT NULL DEFAULT 0,
    sum_assured           NUMERIC(20,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    agent_id              VARCHAR(100)
);
```

### slv_ins_claims

```sql
CREATE TABLE slv_ins_claims (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- claim_number
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    claim_id              VARCHAR(100) NOT NULL,
    claim_number          VARCHAR(50) NOT NULL,
    policy_id             VARCHAR(100) NOT NULL,
    claimant_id           VARCHAR(100) NOT NULL,
    incident_date         DATE NOT NULL,
    reported_date         DATE NOT NULL,
    claim_type            VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    claimed_amount        NUMERIC(20,4) NOT NULL DEFAULT 0,
    approved_amount       NUMERIC(20,4) NOT NULL DEFAULT 0,
    approval_rate_pct     NUMERIC(8,4) GENERATED ALWAYS AS (
                            CASE WHEN claimed_amount > 0
                            THEN approved_amount / claimed_amount * 100 ELSE 0 END
                          ) STORED,
    status                VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    adjuster_id           VARCHAR(100),
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD'
);
```

### slv_ins_premium_payments

```sql
CREATE TABLE slv_ins_premium_payments (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    payment_id            VARCHAR(100) NOT NULL,
    policy_id             VARCHAR(100) NOT NULL,
    due_date              DATE NOT NULL,
    payment_date          DATE,
    amount_due            NUMERIC(20,4) NOT NULL DEFAULT 0,
    amount_paid           NUMERIC(20,4) NOT NULL DEFAULT 0,
    balance               NUMERIC(20,4) GENERATED ALWAYS AS (amount_due - amount_paid) STORED,
    payment_method        VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    status                VARCHAR(50) NOT NULL DEFAULT 'PENDING'
);
```

### slv_ins_underwriting

```sql
CREATE TABLE slv_ins_underwriting (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- application_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    underwriting_id       VARCHAR(100) NOT NULL,
    application_id        VARCHAR(100) NOT NULL,
    applicant_id          VARCHAR(100) NOT NULL,
    product_id            VARCHAR(100) NOT NULL,
    risk_score            NUMERIC(8,4) NOT NULL DEFAULT 0,
    decision              VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    decision_date         DATE,
    underwriter_id        VARCHAR(100),
    notes                 TEXT
);
```

### slv_ins_reinsurance

```sql
CREATE TABLE slv_ins_reinsurance (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- treaty_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    treaty_id             VARCHAR(100) NOT NULL,
    reinsurer_name        VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    treaty_type           VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    line_of_business      VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    start_date            DATE NOT NULL,
    end_date              DATE,
    cession_pct           NUMERIC(8,4) NOT NULL DEFAULT 0,
    max_liability         NUMERIC(20,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    is_expired            BOOLEAN GENERATED ALWAYS AS (end_date < CURRENT_DATE) STORED
);
```

### slv_ins_agents

```sql
CREATE TABLE slv_ins_agents (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- license_number
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    agent_id              VARCHAR(100) NOT NULL,
    first_name            VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    last_name             VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    license_number        VARCHAR(100) NOT NULL,
    license_expiry        DATE,
    agency_id             VARCHAR(100),
    channel               VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    email                 VARCHAR(255),
    phone                 VARCHAR(50),
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    is_license_valid      BOOLEAN GENERATED ALWAYS AS (
                            license_expiry IS NULL OR license_expiry >= CURRENT_DATE
                          ) STORED
);
```

### slv_ins_commission

```sql
CREATE TABLE slv_ins_commission (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- commission_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    commission_id         VARCHAR(100) NOT NULL,
    agent_id              VARCHAR(100) NOT NULL,
    policy_id             VARCHAR(100) NOT NULL,
    commission_type       VARCHAR(50) NOT NULL DEFAULT 'NEW_BUSINESS',
    commission_rate       NUMERIC(8,4) NOT NULL DEFAULT 0,
    premium_amount        NUMERIC(20,4) NOT NULL DEFAULT 0,
    commission_amount     NUMERIC(20,4) NOT NULL DEFAULT 0,
    period_start          DATE NOT NULL,
    period_end            DATE NOT NULL,
    status                VARCHAR(50) NOT NULL DEFAULT 'PENDING'
);
```

### slv_ins_risk_assessments

```sql
CREATE TABLE slv_ins_risk_assessments (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- assessment_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    assessment_id         VARCHAR(100) NOT NULL,
    policy_id             VARCHAR(100) NOT NULL,
    risk_type             VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    assessed_by           VARCHAR(100),
    assessed_at           TIMESTAMP NOT NULL,
    risk_score            NUMERIC(8,4) NOT NULL DEFAULT 0,
    risk_category         VARCHAR(20) NOT NULL DEFAULT 'LOW',
    factors               TEXT,
    notes                 TEXT
);
```

### slv_ins_beneficiaries

```sql
CREATE TABLE slv_ins_beneficiaries (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- beneficiary_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    beneficiary_id        VARCHAR(100) NOT NULL,
    policy_id             VARCHAR(100) NOT NULL,
    first_name            VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    last_name             VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    relationship          VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    allocation_pct        NUMERIC(6,2) NOT NULL DEFAULT 0,
    date_of_birth         DATE,
    national_id           VARCHAR(100),
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE'
);
```

---

## 📂 Sector 16 — Cybersecurity

### slv_sec_security_events

```sql
CREATE TABLE slv_sec_security_events (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- event_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    event_id              VARCHAR(100) NOT NULL,
    event_type            VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    severity              VARCHAR(20) NOT NULL DEFAULT 'LOW',
    source_ip             VARCHAR(45),
    destination_ip        VARCHAR(45),
    source_port           INTEGER,
    destination_port      INTEGER,
    protocol              VARCHAR(20),
    user_id               VARCHAR(100),
    host_id               VARCHAR(100),
    event_timestamp       TIMESTAMP NOT NULL
);
```

### slv_sec_vulnerabilities

```sql
CREATE TABLE slv_sec_vulnerabilities (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- cve_id + asset_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    vuln_id               VARCHAR(100) NOT NULL,
    cve_id                VARCHAR(50),
    asset_id              VARCHAR(100) NOT NULL,
    severity              VARCHAR(20) NOT NULL DEFAULT 'UNKNOWN',
    cvss_score            NUMERIC(4,1) NOT NULL DEFAULT 0,
    description           TEXT,
    discovered_date       DATE NOT NULL,
    remediated_date       DATE,
    days_open             INTEGER GENERATED ALWAYS AS (
                            COALESCE(remediated_date, CURRENT_DATE) - discovered_date
                          ) STORED,
    status                VARCHAR(50) NOT NULL DEFAULT 'OPEN'
);
```

### slv_sec_assets

```sql
CREATE TABLE slv_sec_assets (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- hostname
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    asset_id              VARCHAR(100) NOT NULL,
    hostname              VARCHAR(255) NOT NULL,
    ip_address            VARCHAR(45),
    mac_address           VARCHAR(50),
    asset_type            VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    os                    VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    os_version            VARCHAR(100),
    owner_id              VARCHAR(100),
    criticality           VARCHAR(20) NOT NULL DEFAULT 'LOW',
    last_seen             TIMESTAMP
);
```

### slv_sec_access_logs

```sql
CREATE TABLE slv_sec_access_logs (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- log_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    log_id                VARCHAR(100) NOT NULL,
    user_id               VARCHAR(100) NOT NULL,
    resource_id           VARCHAR(100) NOT NULL,
    action                VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    result                VARCHAR(20) NOT NULL DEFAULT 'UNKNOWN',
    ip_address            VARCHAR(45),
    access_timestamp      TIMESTAMP NOT NULL,
    session_id            VARCHAR(100)
);
```

### slv_sec_incidents

```sql
CREATE TABLE slv_sec_incidents (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- incident_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    incident_id           VARCHAR(100) NOT NULL,
    title                 VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    incident_type         VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    severity              VARCHAR(20) NOT NULL DEFAULT 'LOW',
    status                VARCHAR(50) NOT NULL DEFAULT 'OPEN',
    detected_at           TIMESTAMP NOT NULL,
    resolved_at           TIMESTAMP,
    resolution_hours      NUMERIC(10,2) GENERATED ALWAYS AS (
                            CASE WHEN resolved_at IS NOT NULL
                            THEN EXTRACT(EPOCH FROM (resolved_at - detected_at)) / 3600 ELSE NULL END
                          ) STORED,
    assigned_to           VARCHAR(100),
    description           TEXT
);
```

### slv_sec_threat_intelligence

```sql
CREATE TABLE slv_sec_threat_intelligence (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- indicator_type + indicator_value
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    intel_id              VARCHAR(100) NOT NULL,
    indicator_type        VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    indicator_value       TEXT NOT NULL,
    threat_category       VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    confidence_score      NUMERIC(5,2) NOT NULL DEFAULT 0,
    severity              VARCHAR(20) NOT NULL DEFAULT 'LOW',
    source_feed           VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    first_seen            TIMESTAMP NOT NULL,
    last_seen             TIMESTAMP,
    days_active           INTEGER GENERATED ALWAYS AS (
                            COALESCE(last_seen::DATE, CURRENT_DATE) - first_seen::DATE
                          ) STORED,
    is_active             BOOLEAN NOT NULL DEFAULT TRUE
);
```

### slv_sec_patch_management

```sql
CREATE TABLE slv_sec_patch_management (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- patch_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    patch_id              VARCHAR(100) NOT NULL,
    asset_id              VARCHAR(100) NOT NULL,
    patch_name            VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    cve_id                VARCHAR(50),
    severity              VARCHAR(20) NOT NULL DEFAULT 'UNKNOWN',
    released_date         DATE NOT NULL,
    applied_date          DATE,
    days_to_patch         INTEGER GENERATED ALWAYS AS (
                            CASE WHEN applied_date IS NOT NULL
                            THEN applied_date - released_date ELSE NULL END
                          ) STORED,
    applied_by            VARCHAR(100),
    status                VARCHAR(50) NOT NULL DEFAULT 'PENDING'
);
```

### slv_sec_user_accounts

```sql
CREATE TABLE slv_sec_user_accounts (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- username
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    account_id            VARCHAR(100) NOT NULL,
    username              VARCHAR(100) NOT NULL,
    email                 VARCHAR(255),
    department_id         VARCHAR(100),
    role                  VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    privilege_level       VARCHAR(20) NOT NULL DEFAULT 'STANDARD',
    mfa_enabled           BOOLEAN NOT NULL DEFAULT FALSE,
    last_login            TIMESTAMP,
    password_last_set     DATE,
    is_locked             BOOLEAN NOT NULL DEFAULT FALSE,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    days_since_login      INTEGER GENERATED ALWAYS AS (
                            CASE WHEN last_login IS NOT NULL
                            THEN CURRENT_DATE - last_login::DATE ELSE NULL END
                          ) STORED
);
```

### slv_sec_network_flows

```sql
CREATE TABLE slv_sec_network_flows (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- flow_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    flow_id               VARCHAR(100) NOT NULL,
    src_ip                VARCHAR(45) NOT NULL,
    dst_ip                VARCHAR(45) NOT NULL,
    src_port              INTEGER,
    dst_port              INTEGER,
    protocol              VARCHAR(20) NOT NULL DEFAULT 'UNKNOWN',
    start_time            TIMESTAMP NOT NULL,
    end_time              TIMESTAMP,
    duration_seconds      INTEGER GENERATED ALWAYS AS (
                            CASE WHEN end_time IS NOT NULL
                            THEN EXTRACT(EPOCH FROM (end_time - start_time))::INTEGER ELSE NULL END
                          ) STORED,
    bytes_sent            BIGINT NOT NULL DEFAULT 0,
    bytes_received        BIGINT NOT NULL DEFAULT 0,
    total_bytes           BIGINT GENERATED ALWAYS AS (bytes_sent + bytes_received) STORED,
    packets_sent          BIGINT NOT NULL DEFAULT 0,
    action                VARCHAR(20) NOT NULL DEFAULT 'ALLOW'
);
```

### slv_sec_compliance_checks

```sql
CREATE TABLE slv_sec_compliance_checks (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- check_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    check_id              VARCHAR(100) NOT NULL,
    asset_id              VARCHAR(100) NOT NULL,
    framework             VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    control_id            VARCHAR(50) NOT NULL,
    control_name          VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    check_date            DATE NOT NULL,
    result                VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    evidence              TEXT,
    reviewed_by           VARCHAR(100),
    is_passing            BOOLEAN GENERATED ALWAYS AS (result = 'PASS') STORED
);
```

---

## 📂 Sector 17 — Education

### slv_edu_students

```sql
CREATE TABLE slv_edu_students (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- student_number
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    student_id            VARCHAR(100) NOT NULL,
    student_number        VARCHAR(50) NOT NULL,
    first_name            VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    last_name             VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    date_of_birth         DATE,
    gender                VARCHAR(20) NOT NULL DEFAULT 'UNKNOWN',
    email                 VARCHAR(255),
    enrolled_date         DATE,
    graduation_date       DATE,
    program_id            VARCHAR(100) NOT NULL,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE'
);
```

### slv_edu_courses

```sql
CREATE TABLE slv_edu_courses (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- course_code
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    course_id             VARCHAR(100) NOT NULL,
    course_code           VARCHAR(50) NOT NULL,
    course_name           VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    department_id         VARCHAR(100) NOT NULL,
    credit_hours          NUMERIC(4,1) NOT NULL DEFAULT 0,
    level                 VARCHAR(50) NOT NULL DEFAULT 'UNDERGRADUATE',
    description           TEXT,
    is_active             BOOLEAN NOT NULL DEFAULT TRUE
);
```

### slv_edu_enrollments

```sql
CREATE TABLE slv_edu_enrollments (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- student_id + course_id + term_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    enrollment_id         VARCHAR(100) NOT NULL,
    student_id            VARCHAR(100) NOT NULL,
    course_id             VARCHAR(100) NOT NULL,
    section_id            VARCHAR(100),
    term_id               VARCHAR(100) NOT NULL,
    enrollment_date       DATE NOT NULL,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE'
);
```

### slv_edu_grades

```sql
CREATE TABLE slv_edu_grades (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- grade_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    grade_id              VARCHAR(100) NOT NULL,
    enrollment_id         VARCHAR(100) NOT NULL,
    student_id            VARCHAR(100) NOT NULL,
    course_id             VARCHAR(100) NOT NULL,
    term_id               VARCHAR(100) NOT NULL,
    assessment_type       VARCHAR(50) NOT NULL DEFAULT 'EXAM',
    score                 NUMERIC(6,2) NOT NULL DEFAULT 0,
    max_score             NUMERIC(6,2) NOT NULL DEFAULT 100,
    score_pct             NUMERIC(8,4) GENERATED ALWAYS AS (
                            CASE WHEN max_score > 0
                            THEN score / max_score * 100 ELSE 0 END
                          ) STORED,
    letter_grade          VARCHAR(5),
    graded_at             TIMESTAMP NOT NULL
);
```

### slv_edu_instructors

```sql
CREATE TABLE slv_edu_instructors (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- employee_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    instructor_id         VARCHAR(100) NOT NULL,
    employee_id           VARCHAR(100),
    first_name            VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    last_name             VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    email                 VARCHAR(255),
    department_id         VARCHAR(100) NOT NULL,
    rank                  VARCHAR(100) NOT NULL DEFAULT 'LECTURER',
    hire_date             DATE,
    tenure_status         VARCHAR(50) NOT NULL DEFAULT 'NON_TENURE',
    is_active             BOOLEAN NOT NULL DEFAULT TRUE
);
```

### slv_edu_attendance

```sql
CREATE TABLE slv_edu_attendance (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- enrollment_id + class_date
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    attendance_id         VARCHAR(100) NOT NULL,
    enrollment_id         VARCHAR(100) NOT NULL,
    student_id            VARCHAR(100) NOT NULL,
    section_id            VARCHAR(100),
    class_date            DATE NOT NULL,
    status                VARCHAR(20) NOT NULL DEFAULT 'PRESENT'
);
```

### slv_edu_programs

```sql
CREATE TABLE slv_edu_programs (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- program_code
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    program_id            VARCHAR(100) NOT NULL,
    program_name          VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    program_code          VARCHAR(50) NOT NULL,
    degree_type           VARCHAR(50) NOT NULL DEFAULT 'BACHELOR',
    department_id         VARCHAR(100) NOT NULL,
    duration_years        NUMERIC(4,1) NOT NULL DEFAULT 4,
    credit_hours          INTEGER NOT NULL DEFAULT 0,
    is_active             BOOLEAN NOT NULL DEFAULT TRUE,
    accreditation         VARCHAR(100)
);
```

### slv_edu_scholarships

```sql
CREATE TABLE slv_edu_scholarships (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- scholarship_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    scholarship_id        VARCHAR(100) NOT NULL,
    student_id            VARCHAR(100) NOT NULL,
    scholarship_name      VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    scholarship_type      VARCHAR(50) NOT NULL DEFAULT 'MERIT',
    amount                NUMERIC(20,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    academic_year         INTEGER NOT NULL,
    term_id               VARCHAR(100),
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE'
);
```

### slv_edu_fees

```sql
CREATE TABLE slv_edu_fees (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- fee_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    fee_id                VARCHAR(100) NOT NULL,
    student_id            VARCHAR(100) NOT NULL,
    fee_type              VARCHAR(50) NOT NULL DEFAULT 'TUITION',
    term_id               VARCHAR(100) NOT NULL,
    amount                NUMERIC(20,4) NOT NULL DEFAULT 0,
    currency_code         CHAR(3) NOT NULL DEFAULT 'USD',
    due_date              DATE NOT NULL,
    paid_date             DATE,
    paid_amount           NUMERIC(20,4) NOT NULL DEFAULT 0,
    outstanding_amount    NUMERIC(20,4) GENERATED ALWAYS AS (amount - paid_amount) STORED,
    days_overdue          INTEGER GENERATED ALWAYS AS (
                            CASE WHEN due_date < CURRENT_DATE AND status NOT IN ('PAID','WAIVED')
                            THEN CURRENT_DATE - due_date ELSE 0 END
                          ) STORED,
    status                VARCHAR(50) NOT NULL DEFAULT 'UNPAID'
);
```

### slv_edu_library

```sql
CREATE TABLE slv_edu_library (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- transaction_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    transaction_id        VARCHAR(100) NOT NULL,
    student_id            VARCHAR(100) NOT NULL,
    item_id               VARCHAR(100) NOT NULL,
    item_type             VARCHAR(50) NOT NULL DEFAULT 'BOOK',
    borrow_date           DATE NOT NULL,
    due_date              DATE NOT NULL,
    return_date           DATE,
    days_overdue          INTEGER GENERATED ALWAYS AS (
                            CASE WHEN return_date IS NOT NULL AND return_date > due_date
                            THEN return_date - due_date
                            WHEN return_date IS NULL AND CURRENT_DATE > due_date
                            THEN CURRENT_DATE - due_date
                            ELSE 0 END
                          ) STORED,
    fine_amount           NUMERIC(10,4) NOT NULL DEFAULT 0,
    status                VARCHAR(50) NOT NULL DEFAULT 'BORROWED'
);
```

### slv_edu_departments

```sql
CREATE TABLE slv_edu_departments (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- department_id
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,
    _valid_from           TIMESTAMP,
    _valid_to             TIMESTAMP,
    _is_current           BOOLEAN DEFAULT TRUE,

    department_id         VARCHAR(100) NOT NULL,
    department_name       VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    faculty               VARCHAR(100) NOT NULL DEFAULT 'UNKNOWN',
    head_instructor       VARCHAR(100),
    budget                NUMERIC(20,4) NOT NULL DEFAULT 0,
    established_year      INTEGER,
    is_active             BOOLEAN NOT NULL DEFAULT TRUE
);
```

### slv_edu_extracurricular

```sql
CREATE TABLE slv_edu_extracurricular (
    _row_id               BIGSERIAL PRIMARY KEY,
    _source_row_id        BIGINT,
    _processed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    _dedup_key            VARCHAR(255),        -- student_id + activity_name + academic_year
    _is_valid             BOOLEAN DEFAULT TRUE,
    _validation_errors    TEXT,

    record_id             VARCHAR(100) NOT NULL,
    student_id            VARCHAR(100) NOT NULL,
    activity_name         VARCHAR(255) NOT NULL DEFAULT 'UNKNOWN',
    activity_type         VARCHAR(50) NOT NULL DEFAULT 'UNKNOWN',
    academic_year         INTEGER NOT NULL,
    role                  VARCHAR(100) NOT NULL DEFAULT 'MEMBER',
    hours_per_week        NUMERIC(5,2) NOT NULL DEFAULT 0,
    status                VARCHAR(50) NOT NULL DEFAULT 'ACTIVE'
);
```

---

## 📊 Silver Layer Summary

| #   | Sector             | Tables        | Key Silver Features                               |
| --- | ------------------ | ------------- | ------------------------------------------------- |
| 1   | Finance            | 6             | SCD2 on accounts/customers, generated net amounts |
| 2   | Marketing          | 5             | CTR & CPC computed columns, engagement totals     |
| 3   | Healthcare         | 6             | SCD2 on patients/providers, ICD defaults          |
| 4   | Retail             | 6             | Margin %, available qty, below-reorder flag       |
| 5   | Manufacturing      | 5             | Yield %, defect rate %, SCD2 on machines          |
| 6   | E-Commerce         | 6             | Session duration, discount %, SCD2 on orders      |
| 7   | Logistics          | 4             | Days-to-deliver computed, SCD2 on shipments       |
| 8   | Supply Chain       | 5             | Pending quantity, SCD2 on POs/suppliers           |
| 9   | Telecommunications | 4             | Total bytes, outage duration, SCD2 on subscribers |
| 10  | Energy & Utilities | 4             | Outage duration, SCD2 on meters/assets            |
| 11  | Agriculture        | 4             | Yield per hectare, SCD2 on farms/cycles           |
| 12  | Transportation     | 4             | Delay minutes, tenure days, SCD2 on trips         |
| 13  | Real Estate        | 4             | Lease term months, SCD2 on listings               |
| 14  | Human Resources    | 5             | Tenure days, SCD2 on employees                    |
| 15  | Insurance          | 4             | Approval rate %, balance, SCD2 on policies        |
| 16  | Cybersecurity      | 5             | Days open, resolution hours, SCD2 on assets       |
| 17  | Education          | 6             | Score %, SCD2 on students/enrollments             |
|     | **TOTAL**          | **83 tables** |                                                   |

---

## 🔜 Next: Gold Layer

Gold layer builds **Fact + Dimension + Aggregate** tables in star schema per sector using Silver as source.

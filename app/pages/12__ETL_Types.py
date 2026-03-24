import streamlit as st

from components import sidebar
from utils.seo import inject_seo

st.set_page_config(
    page_title="ETL Load Patterns",
    page_icon="⚡",
    layout="wide",
)

sidebar()
inject_seo('ETL_Types')

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
.main { background-color: #0d0f14; }

.hero {
    background: linear-gradient(135deg, #0d0f14 0%, #111827 50%, #0d0f14 100%);
    border: 1px solid #1f2937;
    border-radius: 16px;
    padding: 3rem 2.5rem 2.5rem;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title { font-size: 2.6rem; font-weight: 800; color: #f9fafb; margin: 0 0 0.4rem; letter-spacing: -0.5px; }
.hero-title span { color: #818cf8; }
.hero-sub { color: #6b7280; font-size: 1rem; margin: 0; }

.card {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 14px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.4rem;
    transition: border-color 0.2s;
}
.card:hover { border-color: #4f46e5; }

.card-header { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem; }
.badge {
    background: #1e1b4b; color: #818cf8;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem; font-weight: 700;
    padding: 3px 10px; border-radius: 999px;
    border: 1px solid #312e81; white-space: nowrap;
}
.card-title { font-size: 1.15rem; font-weight: 700; color: #f3f4f6; margin: 0; }

.tags { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 0.9rem; }
.tag {
    background: #1f2937; color: #9ca3af;
    font-size: 0.72rem; padding: 2px 9px;
    border-radius: 6px; border: 1px solid #374151;
}

.info-grid {
    display: grid; grid-template-columns: 110px 1fr;
    gap: 0.4rem 0.8rem; margin-bottom: 0.9rem;
}
.info-label { color: #6b7280; font-size: 0.78rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; padding-top: 2px; }
.info-value  { color: #d1d5db; font-size: 0.88rem; line-height: 1.55; }

.flow-box {
    background: #0d0f14;
    border: 1px solid #1f2937;
    border-left: 3px solid #4f46e5;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem; color: #a5b4fc;
    margin-bottom: 0.9rem;
    white-space: pre-wrap; line-height: 1.7;
}

.scenario-box {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-left: 3px solid #10b981;
    border-radius: 8px;
    padding: 0.7rem 1rem; margin-bottom: 0.5rem;
}
.scenario-title { color: #34d399; font-size: 0.8rem; font-weight: 700; margin-bottom: 0.3rem; }
.scenario-body  { color: #94a3b8; font-size: 0.84rem; line-height: 1.55; }

.section-label {
    color: #6b7280; font-size: 0.73rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1px; margin: 1rem 0 0.45rem;
}
hr.subtle { border-color: #1f2937; margin: 0.5rem 0 1.2rem; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.title("⚡ ETL Load Patterns Cheat Sheet")
st.caption(
    "Types of ETL Load Patterns — Definitions, Usage, Scenarios & Python Examples")


patterns = [
    # 1 ── Initial Load ────────────────────────────────────────────────────────
    {
        "num": "01",
        "title": "Initial Load",
        "tags": ["Migration", "Onboarding", "One-Time"],
        "definition": "First-time bulk ingestion of all historical data into a brand-new target system. Runs once during project kick-off or a system migration.",
        "usage": "System migrations, greenfield data warehouse setup, historical backfill before switching to incremental pipelines.",
        "flow": "Source (Historical Data)  ->  Bulk Transfer  ->  Target (New System)",
        "scenarios": [
            {"title": "🏦 Banking CRM Migration",
                "body": "A bank migrates 10 years of customer transactions from a legacy Oracle DB to Snowflake. All rows are copied once; afterwards incremental loads take over."},
            {"title": "🛒 E-commerce Warehouse Launch",
                "body": "A retailer seeds a new data warehouse with 5 years of order history before daily delta loads begin."},
            {"title": "🏥 Healthcare Records Transfer",
                "body": "A hospital system moves patient records from an on-prem SQL Server to a cloud data lake during a digital transformation project."},
            {"title": "🎓 University LMS Migration",
                "body": "A university migrates all student grades, enrollment history, and course data from a legacy LMS to a modern analytics platform."},
            {"title": "🏭 ERP System Replacement",
                "body": "A manufacturer replaces its on-prem ERP with a cloud solution, performing a one-time initial load of 8 years of production and inventory records."},
        ],
        "examples": [
            {
                "title": "pandas + SQLAlchemy",
                "code": '''import pandas as pd
import sqlalchemy

src = sqlalchemy.create_engine("postgresql://user:pw@source/legacy_db")
tgt = sqlalchemy.create_engine("postgresql://user:pw@target/dwh")

# Read ALL historical rows from source
df = pd.read_sql("SELECT * FROM orders", src)
print(f"Rows to migrate: {len(df):,}")

# Write to target in chunks (avoids OOM on large tables)
df.to_sql(
    name="orders",
    con=tgt,
    if_exists="replace",   # replace = create + overwrite
    index=False,
    chunksize=10_000,
    method="multi",
)
print("Initial load complete ✓")
''',
            },
            {
                "title": "psycopg2 COPY (fast bulk)",
                "code": '''import psycopg2, io

src_conn = psycopg2.connect("host=source dbname=legacy_db user=etl password=pw")
tgt_conn = psycopg2.connect("host=target dbname=dwh     user=etl password=pw")

# 1. Dump source table to an in-memory CSV buffer
buf = io.StringIO()
with src_conn.cursor() as cur:
    cur.copy_expert("COPY orders TO STDOUT WITH CSV HEADER", buf)
buf.seek(0)

# 2. Bulk-load into target using PostgreSQL COPY (fastest path)
with tgt_conn.cursor() as cur:
    cur.execute("TRUNCATE TABLE orders")       # clean slate
    cur.copy_expert("COPY orders FROM STDIN WITH CSV HEADER", buf)
tgt_conn.commit()

print("Bulk COPY initial load complete ✓")
src_conn.close(); tgt_conn.close()
''',
            },
            {
                "title": "PySpark (large-scale)",
                "code": '''from pyspark.sql import SparkSession

spark = (SparkSession.builder
         .appName("InitialLoad")
         .getOrCreate())

# Read from JDBC source (parallel partitioned reads)
df = (spark.read
      .format("jdbc")
      .option("url",      "jdbc:postgresql://source/legacy_db")
      .option("dbtable",  "orders")
      .option("user",     "etl")
      .option("password", "pw")
      .option("numPartitions", 20)
      .load())

print(f"Loaded {df.count():,} rows via Spark")

# Write to Parquet data lake
(df.write
   .mode("overwrite")
   .parquet("s3://my-data-lake/warehouse/orders/"))

print("Spark initial load to S3 complete ✓")
spark.stop()
''',
            },
        ],
    },

    # 2 ── Full Load ───────────────────────────────────────────────────────────
    {
        "num": "02",
        "title": "Full Load",
        "tags": ["Simple", "Small Dataset", "Idempotent"],
        "definition": "Reloads the entire dataset on every pipeline run — no state, no bookmarks. Simple and reliable for small tables.",
        "usage": "Small reference tables (country codes, product categories), configuration data, or any table where simplicity beats efficiency.",
        "flow": "Source (Complete Dataset)  ->  Truncate Table  ->  Complete Reload  ->  Target",
        "scenarios": [
            {"title": "🗺️ Currency Exchange Rates",
                "body": "A finance app pulls the full exchange-rate table (~200 rows) from an API every hour and replaces the target table."},
            {"title": "📦 Product Catalogue",
                "body": "A small SaaS refreshes its 500-SKU product table nightly; full load ensures deleted products disappear too."},
            {"title": "🌍 Country & Region Codes",
                "body": "A logistics platform reloads its ISO country/region reference table every Sunday since records rarely change but must always be complete."},
            {"title": "🏷️ Promotion & Discount Rules",
                "body": "A retail app refreshes its promotions config table before peak hours — a full reload guarantees expired deals are never served."},
            {"title": "👥 HR Department Roster",
                "body": "An HR system rebuilds its department-to-employee mapping table nightly from the source HRIS, covering org changes and departures."},
        ],
        "examples": [
            {
                "title": "pandas + SQLAlchemy",
                "code": '''import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine("postgresql://user:pw@host/db")

# Pull complete dataset
df = pd.read_sql("SELECT * FROM currency_rates_source", engine)

# Atomic: truncate then reload in a single transaction
with engine.begin() as conn:
    conn.execute(sqlalchemy.text("TRUNCATE TABLE currency_rates"))
    df.to_sql("currency_rates", con=conn, if_exists="append",
              index=False, method="multi")

print(f"Full load: {len(df)} rows replaced ✓")
''',
            },
            {
                "title": "Requests API → SQLite",
                "code": '''import requests, sqlite3, pandas as pd

# 1. Fetch fresh data from an external API
resp  = requests.get("https://api.exchangerate.host/latest?base=USD")
rates = resp.json()["rates"]
df    = pd.DataFrame(rates.items(), columns=["currency", "rate"])

# 2. Full-replace in SQLite (tiny reference tables)
con = sqlite3.connect("finance.db")
df.to_sql("exchange_rates", con, if_exists="replace", index=False)
con.close()

print(f"Full load: {len(df)} currencies refreshed ✓")
''',
            },
            {
                "title": "dbt seed (declarative)",
                "code": '''# In a dbt project, full-load reference tables are handled as "seeds"
# Place your CSV in seeds/currency_rates.csv, then run: dbt seed

# seeds/currency_rates.csv  <- commit this file to git
# currency,rate
# EUR,0.91
# GBP,0.78
# JPY,149.50

# dbt seed drops and reloads the table on every run = pure full load.
# Trigger programmatically from Python:

import subprocess

result = subprocess.run(
    ["dbt", "seed", "--select", "currency_rates", "--full-refresh"],
    capture_output=True, text=True
)
print(result.stdout)
print("dbt seed full load complete ✓")
''',
            },
        ],
    },

    # 3 ── Incremental Load ────────────────────────────────────────────────────
    {
        "num": "03",
        "title": "Incremental Load",
        "tags": ["Efficient", "Timestamp", "Append-Only"],
        "definition": "Loads only records added since the last successful run, tracked via a high-watermark (timestamp or auto-increment ID).",
        "usage": "Event logs, transaction tables, sensor readings — any append-only source that grows continuously.",
        "flow": "Source (Timestamp / ID)  ->  Incremental Batch  ->  Target (Appended Data)",
        "scenarios": [
            {"title": "📊 Daily Sales Sync",
                "body": "An analytics pipeline runs at midnight and appends only the last 24 hours of sales records to the data warehouse."},
            {"title": "🖥️ Server Log Aggregation",
                "body": "Log entries generated since the previous run are appended to a central analytics table every 15 minutes."},
            {"title": "📱 Mobile App Event Tracking",
                "body": "A gaming app appends only new player events (clicks, purchases, sessions) recorded since the last hourly pipeline run."},
            {"title": "🚚 Shipment Status Updates",
                "body": "A logistics platform pulls only shipment records with a status_updated_at newer than the last watermark, avoiding re-processing millions of closed orders."},
            {"title": "💬 Support Ticket Ingestion",
                "body": "A customer success team syncs only newly created Zendesk tickets since the last run into their BI warehouse for SLA tracking."},
        ],
        "examples": [
            {
                "title": "Watermark via MAX(timestamp)",
                "code": '''import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine("postgresql://user:pw@host/db")

# 1. Read last watermark from target
wm = engine.execute(
    "SELECT COALESCE(MAX(created_at), '1970-01-01') FROM sales_target"
).scalar()
print(f"Last watermark: {wm}")

# 2. Fetch only rows newer than the watermark
df_new = pd.read_sql(
    f"SELECT * FROM sales_source WHERE created_at > '{wm}' ORDER BY created_at",
    engine,
)
print(f"New rows: {len(df_new)}")

# 3. Append to target
if not df_new.empty:
    df_new.to_sql("sales_target", engine,
                  if_exists="append", index=False, method="multi")
    print("Incremental append complete ✓")
else:
    print("No new data — nothing to load.")
''',
            },
            {
                "title": "Watermark via MAX(id)",
                "code": '''import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine("postgresql://user:pw@host/db")

# Auto-increment ID as watermark (faster than timestamp index scans)
last_id = engine.execute(
    "SELECT COALESCE(MAX(order_id), 0) FROM orders_target"
).scalar()
print(f"Last loaded order_id: {last_id}")

df_new = pd.read_sql(
    f"SELECT * FROM orders_source WHERE order_id > {last_id} ORDER BY order_id",
    engine,
)

if not df_new.empty:
    df_new.to_sql("orders_target", engine, if_exists="append",
                  index=False, chunksize=5_000, method="multi")
    print(f"Appended {len(df_new):,} rows "
          f"(up to id={df_new['order_id'].max()}) ✓")
else:
    print("No new orders.")
''',
            },
            {
                "title": "Airflow DAG with Variable watermark",
                "code": '''from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime, timedelta
import pandas as pd, sqlalchemy

engine = sqlalchemy.create_engine("postgresql://user:pw@host/db")

def incremental_load(**ctx):
    last_ts = Variable.get("sales_last_watermark",
                           default_var="1970-01-01 00:00:00")

    df = pd.read_sql(
        f"SELECT * FROM sales WHERE created_at > '{last_ts}'", engine
    )
    if not df.empty:
        df.to_sql("sales_dwh", engine, if_exists="append", index=False)
        new_wm = str(df["created_at"].max())
        Variable.set("sales_last_watermark", new_wm)
        print(f"Loaded {len(df)} rows | new watermark: {new_wm} ✓")
    else:
        print("No new rows.")

with DAG("incremental_sales",
         start_date=datetime(2024, 1, 1),
         schedule_interval=timedelta(hours=1),
         catchup=False) as dag:

    PythonOperator(task_id="load", python_callable=incremental_load)
''',
            },
        ],
    },

    # 4 ── Delta / CDC ─────────────────────────────────────────────────────────
    {
        "num": "04",
        "title": "Delta Load (CDC)",
        "tags": ["Real-Time", "Inserts + Updates + Deletes", "Log-Based"],
        "definition": "Change Data Capture reads the database transaction log to detect inserts, updates, AND deletes, replaying them on the target with minimal latency.",
        "usage": "Near-real-time replication, audit trails, microservice event sourcing, keeping a replica in sync.",
        "flow": "Source (Transaction Log)  ->  CDC Engine  ->  Change Stream  ->  Target (Synchronized)",
        "scenarios": [
            {"title": "🛍️ Inventory Sync",
                "body": "Product stock levels updated in PostgreSQL are streamed via Debezium to Kafka and applied to a read-replica within seconds."},
            {"title": "🔍 Audit Log",
                "body": "Every insert/update/delete on a GDPR-sensitive customers table is captured and written to an immutable audit store."},
            {"title": "💳 Payment Status Replication",
                "body": "Payment records transition through states (pending → processing → settled). CDC captures every status change and propagates it to a reporting replica instantly."},
            {"title": "🏦 Core Banking Sync",
                "body": "Account balance changes in a core banking system are streamed in real time to a fraud detection service that needs up-to-the-second accuracy."},
            {"title": "🛡️ GDPR Right-to-Erasure",
                "body": "When a DELETE fires on the customers table in the source DB, CDC immediately propagates the deletion to all downstream replicas to meet compliance SLAs."},
        ],
        "examples": [
            {
                "title": "CDC change-log table (I/U/D replay)",
                "code": '''import pandas as pd, sqlalchemy

engine = sqlalchemy.create_engine("postgresql://user:pw@host/db")

# Change log has columns: log_id, op (I/U/D), id, name, email, processed
cdc_df = pd.read_sql(
    "SELECT * FROM cdc_log WHERE processed = FALSE ORDER BY log_ts",
    engine,
)
print(f"CDC events to process: {len(cdc_df)}")

with engine.begin() as conn:
    for _, row in cdc_df.iterrows():
        if row["op"] == "I":
            conn.execute(sqlalchemy.text(
                "INSERT INTO customers_target (id, name, email) "
                "VALUES (:id, :name, :email)"
            ), row[["id","name","email"]].to_dict())

        elif row["op"] == "U":
            conn.execute(sqlalchemy.text(
                "UPDATE customers_target SET name=:name, email=:email WHERE id=:id"
            ), row[["id","name","email"]].to_dict())

        elif row["op"] == "D":
            conn.execute(sqlalchemy.text(
                "DELETE FROM customers_target WHERE id=:id"
            ), {"id": row["id"]})

    ids = cdc_df["log_id"].tolist()
    conn.execute(sqlalchemy.text(
        "UPDATE cdc_log SET processed=TRUE WHERE log_id = ANY(:ids)"
    ), {"ids": ids})

print("CDC delta applied ✓")
''',
            },
            {
                "title": "Debezium + Kafka consumer",
                "code": '''from kafka import KafkaConsumer
import json, psycopg2

# Debezium publishes changes to Kafka topic: "dbserver1.public.customers"
consumer = KafkaConsumer(
    "dbserver1.public.customers",
    bootstrap_servers=["kafka:9092"],
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    group_id="cdc-consumer",
)

conn = psycopg2.connect("host=target dbname=dwh user=etl password=pw")
cur  = conn.cursor()

for msg in consumer:
    payload = msg.value["payload"]
    op      = payload["op"]   # "c"=create, "u"=update, "d"=delete

    if op in ("c", "u"):
        after = payload["after"]
        cur.execute("""
            INSERT INTO customers_replica (id, name, email)
            VALUES (%(id)s, %(name)s, %(email)s)
            ON CONFLICT (id) DO UPDATE
              SET name=EXCLUDED.name, email=EXCLUDED.email
        """, after)

    elif op == "d":
        before = payload["before"]
        cur.execute(
            "DELETE FROM customers_replica WHERE id=%s", (before["id"],)
        )

    conn.commit()
    print(f"op={op} applied ✓")
''',
            },
            {
                "title": "Delta Lake MERGE (PySpark)",
                "code": '''from pyspark.sql import SparkSession
from delta.tables import DeltaTable

spark = SparkSession.builder.appName("CDCMerge").getOrCreate()

# CDC dataframe: column "op" = insert | update | delete
cdc_df = spark.read.parquet("s3://lake/cdc/customers/")

deletes = cdc_df.filter("op = 'delete'")
upserts = cdc_df.filter("op != 'delete'")

target = DeltaTable.forPath(spark, "s3://lake/delta/customers/")

# Apply deletes
(target.alias("t")
       .merge(deletes.alias("s"), "t.id = s.id")
       .whenMatchedDelete()
       .execute())

# Apply inserts + updates
(target.alias("t")
       .merge(upserts.alias("s"), "t.id = s.id")
       .whenMatchedUpdateAll()
       .whenNotMatchedInsertAll()
       .execute())

print("Delta Lake CDC merge complete ✓")
spark.stop()
''',
            },
        ],
    },

    # 5 ── Batch Load ─────────────────────────────────────────────────────────
    {
        "num": "05",
        "title": "Batch Load",
        "tags": ["Scheduled", "High Volume", "Cost-Efficient"],
        "definition": "Accumulates data over a period and processes it in a single scheduled job (hourly, nightly, weekly). Optimises throughput over latency.",
        "usage": "End-of-day financial reconciliation, weekly reporting aggregates, large-volume ETL where real-time is not required.",
        "flow": "Source (Accumulated Data)  ->  Scheduled Batch Job  ->  Target (Warehouse / Data Lake)",
        "scenarios": [
            {"title": "💳 Nightly Card Reconciliation",
                "body": "A payment processor batches all card authorizations from the day and loads them into the data warehouse at 02:00 UTC."},
            {"title": "📁 S3 Log Aggregation",
                "body": "Hourly application logs accumulate in S3, then a scheduled Glue job consolidates and loads them into Redshift."},
            {"title": "📈 Weekly KPI Reporting",
                "body": "Every Monday at 06:00 a batch job aggregates the prior week's sales, returns, and margins and loads summary rows into the executive dashboard tables."},
            {"title": "🏥 Insurance Claims Processing",
                "body": "A health insurer collects claims submitted during the day and processes them in a nightly batch, applying eligibility rules before loading to the adjudication DB."},
            {"title": "🎬 Streaming Platform Royalties",
                "body": "A music streaming service tallies play counts per artist overnight and loads the results into the royalty calculation system once per day."},
        ],
        "examples": [
            {
                "title": "boto3 S3 batch collector",
                "code": '''import boto3, pandas as pd
from io import StringIO
from datetime import date

s3     = boto3.client("s3")
BUCKET = "my-data-lake"
PREFIX = f"logs/{date.today()}/"

objects = s3.list_objects_v2(Bucket=BUCKET, Prefix=PREFIX).get("Contents", [])
print(f"Batch files found: {len(objects)}")

frames = []
for obj in objects:
    body = s3.get_object(Bucket=BUCKET, Key=obj["Key"])["Body"].read().decode()
    frames.append(pd.read_csv(StringIO(body)))

if frames:
    batch_df = pd.concat(frames, ignore_index=True)
    out_key  = f"processed/{date.today()}/batch.csv"
    s3.put_object(Bucket=BUCKET, Key=out_key,
                  Body=batch_df.to_csv(index=False))
    print(f"Batch {len(batch_df):,} rows -> s3://{BUCKET}/{out_key} ✓")
else:
    print("No files in batch window.")
''',
            },
            {
                "title": "Airflow nightly batch DAG",
                "code": '''from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd, sqlalchemy

engine = sqlalchemy.create_engine("postgresql://user:pw@host/db")

def nightly_batch(**ctx):
    run_date = ctx["ds"]   # Airflow execution date e.g. "2024-06-15"

    df = pd.read_sql(f"""
        SELECT * FROM transactions_source
        WHERE DATE(created_at) = '{run_date}'
    """, engine)

    print(f"[{run_date}] Batch rows: {len(df):,}")
    df.to_sql("transactions_dwh", engine,
              if_exists="append", index=False, chunksize=5_000)
    print(f"[{run_date}] Batch load complete ✓")

with DAG("nightly_batch_load",
         start_date=datetime(2024, 1, 1),
         schedule_interval="0 2 * * *",   # 02:00 UTC daily
         catchup=True) as dag:

    PythonOperator(task_id="batch_load", python_callable=nightly_batch)
''',
            },
            {
                "title": "PySpark batch to Parquet lake",
                "code": '''from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date
from datetime import date

spark = SparkSession.builder.appName("NightlyBatch").getOrCreate()

run_date = str(date.today())

df = (spark.read
      .format("jdbc")
      .option("url",      "jdbc:postgresql://source/db")
      .option("dbtable",  "transactions")
      .option("user",     "etl")
      .option("password", "pw")
      .load()
      .filter(to_date(col("created_at")) == run_date))

print(f"Batch rows for {run_date}: {df.count():,}")

(df.write
   .mode("append")
   .partitionBy("created_date")
   .parquet("s3://lake/transactions/"))

print("Batch written to Parquet lake ✓")
spark.stop()
''',
            },
        ],
    },

    # 6 ── Streaming / Real-Time ───────────────────────────────────────────────
    {
        "num": "06",
        "title": "Streaming / Real-Time Load",
        "tags": ["Kafka", "Event-Driven", "Low Latency"],
        "definition": "Continuously ingests data events as they occur with sub-second latency. Data is never at rest — it flows straight to the target.",
        "usage": "Fraud detection, live dashboards, IoT telemetry, clickstream analytics, alerting systems.",
        "flow": "Event Sources  ->  Kafka / Kinesis  ->  Stream Processor  ->  Target (Dashboards / Analytics)",
        "scenarios": [
            {"title": "🚨 Real-Time Fraud Detection",
                "body": "Payment events flow from Kafka into a stream processor that scores each transaction for fraud within milliseconds."},
            {"title": "📡 IoT Temperature Alerts",
                "body": "Sensor readings arrive via Kafka and trigger alerts when temperature exceeds safety thresholds."},
            {"title": "🛒 Live Cart Abandonment",
                "body": "Clickstream events from a retail site are streamed into a real-time engine that detects cart abandonment and fires a discount email within 60 seconds."},
            {"title": "📊 Live Sports Leaderboard",
                "body": "Score events from thousands of concurrent matches are ingested via Kinesis and aggregated in real time to update a global leaderboard dashboard."},
            {"title": "🚗 Ride-Hailing GPS Tracking",
                "body": "Driver GPS pings arrive every 2 seconds via Kafka, are processed by a Flink job, and update the rider-facing map with sub-second latency."},
        ],
        "examples": [
            {
                "title": "Kafka -> ClickHouse (buffered)",
                "code": '''from kafka import KafkaConsumer
import json, clickhouse_connect

consumer = KafkaConsumer(
    "payment_events",
    bootstrap_servers=["kafka:9092"],
    value_deserializer=lambda m: json.loads(m.decode()),
    group_id="etl-streaming",
)
client = clickhouse_connect.get_client(host="clickhouse", port=8123)

BUFFER, FLUSH_AT = [], 500

for msg in consumer:
    e = msg.value
    BUFFER.append([e["event_id"], e["user_id"],
                   e["amount"],   e["currency"], e["ts"]])

    if len(BUFFER) >= FLUSH_AT:
        client.insert("payment_events", BUFFER,
                      column_names=["event_id","user_id","amount","currency","ts"])
        print(f"Flushed {len(BUFFER)} events to ClickHouse ✓")
        BUFFER.clear()
''',
            },
            {
                "title": "AWS Kinesis -> DynamoDB",
                "code": '''import boto3, json, base64, time

kinesis  = boto3.client("kinesis",   region_name="us-east-1")
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table    = dynamodb.Table("SensorReadings")

shard_it = kinesis.get_shard_iterator(
    StreamName="iot-sensors",
    ShardId="shardId-000000000000",
    ShardIteratorType="LATEST",
)["ShardIterator"]

print("Listening for Kinesis records...")
while True:
    resp    = kinesis.get_records(ShardIterator=shard_it, Limit=100)
    records = resp["Records"]

    if records:
        with table.batch_writer() as batch:
            for rec in records:
                payload = json.loads(base64.b64decode(rec["Data"]))
                batch.put_item(Item={
                    "sensor_id": payload["sensor_id"],
                    "ts":        payload["timestamp"],
                    "temp_c":    str(payload["temperature"]),
                    "humidity":  str(payload["humidity"]),
                })
        print(f"Wrote {len(records)} readings to DynamoDB ✓")

    shard_it = resp["NextShardIterator"]
    time.sleep(1)
''',
            },
            {
                "title": "PySpark Structured Streaming",
                "code": '''from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import (StructType, StringType,
                                DoubleType, TimestampType)

spark = SparkSession.builder.appName("StreamLoad").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

schema = (StructType()
          .add("event_id", StringType())
          .add("user_id",  StringType())
          .add("amount",   DoubleType())
          .add("ts",       TimestampType()))

stream_df = (spark.readStream
             .format("kafka")
             .option("kafka.bootstrap.servers", "kafka:9092")
             .option("subscribe", "payment_events")
             .load()
             .select(from_json(col("value").cast("string"), schema).alias("d"))
             .select("d.*"))

query = (stream_df.writeStream
         .format("delta")
         .option("checkpointLocation", "s3://lake/checkpoints/payments/")
         .outputMode("append")
         .start("s3://lake/delta/payments/"))

query.awaitTermination()
''',
            },
        ],
    },

    # 7 ── Upsert / Merge ─────────────────────────────────────────────────────
    {
        "num": "07",
        "title": "Upsert / Merge Load",
        "tags": ["MERGE", "SCD", "Idempotent"],
        "definition": "Checks whether each incoming record already exists in the target: updates it if found, inserts it if not. Keeps target in sync without duplicates.",
        "usage": "SCD Type 1 dimensions, CRM sync, any table that must reflect the latest state without a full truncate.",
        "flow": "Source (Staging)  ->  MERGE INTO  ->  Match? -> UPDATE : INSERT  ->  Target",
        "scenarios": [
            {"title": "👤 Customer Profile Sync",
                "body": "CRM records are upserted into the warehouse daily — existing customers get updated fields, new ones are inserted."},
            {"title": "📋 SCD Type 1 Dimension",
                "body": "A product dimension table is refreshed hourly — price changes update existing rows, new products are inserted."},
            {"title": "🏨 Hotel Room Availability",
                "body": "A booking platform upserts room availability records from channel managers — updates reflect real-time cancellations, inserts cover newly listed rooms."},
            {"title": "📦 Supplier Inventory Feed",
                "body": "A wholesaler receives daily inventory CSV files from 50 suppliers. Each file is upserted: known SKUs update stock counts, new SKUs are inserted."},
            {"title": "🎓 Student Enrollment Records",
                "body": "A university syncs enrollment data from its SIS nightly — students who change courses trigger updates, newly enrolled students trigger inserts."},
        ],
        "examples": [
            {
                "title": "PostgreSQL ON CONFLICT",
                "code": '''import pandas as pd, sqlalchemy

engine = sqlalchemy.create_engine("postgresql://user:pw@host/db")

incoming = pd.DataFrame([
    {"customer_id": 1, "name": "Alice",   "email": "alice@new.com"},
    {"customer_id": 2, "name": "Bob",     "email": "bob@example.com"},
    {"customer_id": 3, "name": "Charlie", "email": "charlie@example.com"},
])
incoming.to_sql("staging_customers", engine,
                if_exists="replace", index=False)

upsert_sql = """
    INSERT INTO customers (customer_id, name, email)
    SELECT customer_id, name, email FROM staging_customers
    ON CONFLICT (customer_id) DO UPDATE
        SET name       = EXCLUDED.name,
            email      = EXCLUDED.email,
            updated_at = NOW();
"""
with engine.begin() as conn:
    conn.execute(sqlalchemy.text(upsert_sql))

print(f"Upserted {len(incoming)} rows ✓")
''',
            },
            {
                "title": "SQLite ON CONFLICT DO UPDATE",
                "code": '''import sqlite3, pandas as pd

con = sqlite3.connect("products.db")
con.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        name TEXT, price REAL, updated_at TEXT
    )
""")

incoming = pd.DataFrame([
    {"product_id": 101, "name": "Widget A", "price": 9.99,  "updated_at": "2024-06-01"},
    {"product_id": 102, "name": "Widget B", "price": 14.99, "updated_at": "2024-06-01"},
    {"product_id": 103, "name": "Widget C", "price": 4.49,  "updated_at": "2024-06-01"},
])

for _, row in incoming.iterrows():
    con.execute("""
        INSERT INTO products (product_id, name, price, updated_at)
        VALUES (?,?,?,?)
        ON CONFLICT(product_id) DO UPDATE
          SET name=excluded.name,
              price=excluded.price,
              updated_at=excluded.updated_at
    """, tuple(row))

con.commit(); con.close()
print("SQLite upsert complete ✓")
''',
            },
            {
                "title": "Snowflake MERGE INTO",
                "code": '''import snowflake.connector, pandas as pd

conn = snowflake.connector.connect(
    user="ETL_USER", password="pw",
    account="myorg-myaccount",
    warehouse="LOAD_WH", database="DWH", schema="PUBLIC",
)
cur = conn.cursor()

incoming = pd.DataFrame([
    {"customer_id": 1, "name": "Alice Updated", "email": "alice@v2.com"},
    {"customer_id": 5, "name": "Eve",            "email": "eve@example.com"},
])

cur.execute("CREATE OR REPLACE TEMP TABLE staging_customers LIKE customers")
for _, row in incoming.iterrows():
    cur.execute(
        "INSERT INTO staging_customers VALUES (%s,%s,%s)",
        (row.customer_id, row.name, row.email)
    )

cur.execute("""
    MERGE INTO customers t
    USING staging_customers s ON t.customer_id = s.customer_id
    WHEN MATCHED THEN
        UPDATE SET t.name=s.name, t.email=s.email,
                   t.updated_at=CURRENT_TIMESTAMP
    WHEN NOT MATCHED THEN
        INSERT (customer_id, name, email)
        VALUES (s.customer_id, s.name, s.email)
""")
conn.commit()
print(f"Snowflake MERGE: {cur.rowcount} rows affected ✓")
cur.close(); conn.close()
''',
            },
        ],
    },

    # 8 ── Truncate & Load ─────────────────────────────────────────────────────
    {
        "num": "08",
        "title": "Truncate & Load",
        "tags": ["Snapshot", "Dimension Tables", "Simple"],
        "definition": "Deletes every row in the target table and reloads it from scratch. Guarantees the target is a perfect mirror of the source snapshot.",
        "usage": "Daily dimension snapshots, reference data tables, reporting aggregates where deleted source rows must also disappear.",
        "flow": "Source (Fresh Snapshot)  ->  TRUNCATE Target  ->  Bulk Load  ->  Target (Snapshot Table)",
        "scenarios": [
            {"title": "📅 Daily Summary Snapshot",
                "body": "A pre-aggregated daily_summary table is truncated and reloaded every morning so dashboards always show fresh numbers."},
            {"title": "🗂️ Reference / Lookup Tables",
                "body": "Country codes, postal codes, and tax-rate tables are refreshed weekly — truncate ensures stale rows never linger."},
            {"title": "🏪 Store Performance Scorecard",
                "body": "A retail chain reloads its store_scorecard table nightly with freshly computed KPIs; truncating first guarantees closed stores don't appear."},
            {"title": "📉 Risk Exposure Report",
                "body": "A trading desk reloads its intraday risk_exposure snapshot table every 30 minutes — truncating ensures no stale positions survive a market reset."},
            {"title": "🧾 Tax Jurisdiction Rates",
                "body": "A tax engine reloads its jurisdiction-to-rate mapping table on the 1st of every month, replacing the entire table to reflect legislative changes."},
        ],
        "examples": [
            {
                "title": "pandas + SQLAlchemy (atomic)",
                "code": '''import pandas as pd, sqlalchemy

engine = sqlalchemy.create_engine("postgresql://user:pw@host/db")

snapshot_df = pd.read_sql("""
    SELECT region,
           SUM(revenue) AS total_revenue,
           COUNT(*)      AS order_count,
           CURRENT_DATE  AS snapshot_date
    FROM orders GROUP BY region
""", engine)

# Both statements share one transaction — all-or-nothing
with engine.begin() as conn:
    conn.execute(sqlalchemy.text("TRUNCATE TABLE daily_regional_summary"))
    snapshot_df.to_sql("daily_regional_summary", con=conn,
                       if_exists="append", index=False, method="multi")

print(f"Truncate & Load: {len(snapshot_df)} rows ✓")
''',
            },
            {
                "title": "psycopg2 with rollback safety",
                "code": '''import psycopg2, pandas as pd

conn = psycopg2.connect("host=host dbname=db user=etl password=pw")
cur  = conn.cursor()

df = pd.read_sql("SELECT * FROM product_dim_source",
                 "postgresql://user:pw@host/db")

try:
    cur.execute("BEGIN")
    cur.execute("TRUNCATE TABLE product_dim")

    rows = [tuple(r) for r in df.itertuples(index=False)]
    cur.executemany(
        "INSERT INTO product_dim VALUES (%s,%s,%s,%s)", rows
    )
    conn.commit()
    print(f"Truncate & Load: {len(rows)} rows committed ✓")

except Exception as e:
    conn.rollback()
    print(f"Error — rolled back: {e}")

finally:
    cur.close(); conn.close()
''',
            },
            {
                "title": "dbt full-refresh model",
                "code": '''-- models/daily_regional_summary.sql
-- materialized='table' + --full-refresh = truncate & load on every run

{{
  config(
    materialized = 'table',
    full_refresh  = true
  )
}}

SELECT
    region,
    SUM(revenue) AS total_revenue,
    COUNT(*)      AS order_count,
    CURRENT_DATE  AS snapshot_date
FROM {{ ref('orders') }}
GROUP BY region

-- Trigger from Python:
-- import subprocess
-- subprocess.run(["dbt", "run",
--                 "--select", "daily_regional_summary",
--                 "--full-refresh"])
--
-- dbt will DROP + CREATE the target table on every run.
''',
            },
        ],
    },
]


for p in patterns:
    tags_html = "".join(f'<span class="tag">{t}</span>' for t in p["tags"])

    st.markdown(f"""
    <div class="card">
      <div class="card-header">
        <span class="badge">{p['num']}</span>
        <p class="card-title">{p['title']}</p>
      </div>
      <div class="tags">{tags_html}</div>

      <div class="info-grid">
        <span class="info-label">Definition</span>
        <span class="info-value">{p['definition']}</span>
        <span class="info-label">Usage</span>
        <span class="info-value">{p['usage']}</span>
      </div>

      <p class="section-label">Flow</p>
      <div class="flow-box">{p['flow']}</div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-label">Real-World Scenarios</p>',
                unsafe_allow_html=True)
    for sc in p["scenarios"]:
        st.markdown(f"""
        <div class="scenario-box">
          <div class="scenario-title">{sc['title']}</div>
          <div class="scenario-body">{sc['body']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<p class="section-label">Python Examples</p>',
                unsafe_allow_html=True)
    tabs = st.tabs([ex["title"] for ex in p["examples"]])
    for tab, ex in zip(tabs, p["examples"]):
        with tab:
            st.code(ex["code"], language="python")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<hr class='subtle'>", unsafe_allow_html=True)

import streamlit as st

from components import sidebar
from utils.seo import inject_seo


st.set_page_config(
    page_title="Data Engineering Patterns",
    page_icon="⚙️",
    layout="wide"
)
inject_seo('Data_Engineering_Patterns')
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Syne:wght@400;600;700;800&display=swap');
 
.stApp {
    background-color: #0a0a0f;
    color: #e8e8f0;
    font-family: 'Syne', sans-serif;
}
 
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
}
 
.main-title {
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -1px;
    color: #ffffff;
    margin-bottom: 0.2rem;
}
 
.main-subtitle {
    font-size: 1rem;
    color: #6b6b8a;
    font-weight: 400;
    margin-bottom: 2rem;
    letter-spacing: 2px;
    text-transform: uppercase;
}
 
.pattern-card {
    background: #12121e;
    border: 1px solid #1e1e35;
    border-radius: 12px;
    padding: 1.6rem;
    margin-bottom: 1.2rem;
    transition: border-color 0.2s ease;
}
 
.pattern-card:hover {
    border-color: #3d3d6b;
}
 
.pattern-number {
    font-size: 0.72rem;
    font-weight: 600;
    color: #4a4a7a;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
    font-family: 'JetBrains Mono', monospace;
}
 
.pattern-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #c8c8f0;
    margin-bottom: 0.5rem;
}
 
.tag {
    display: inline-block;
    background: #1a1a2e;
    border: 1px solid #2e2e50;
    border-radius: 4px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace;
    color: #6a6aaa;
    margin-right: 6px;
    margin-bottom: 6px;
    letter-spacing: 1px;
    text-transform: uppercase;
}
 
.definition-box {
    background: #0e0e1a;
    border-left: 3px solid #3535a0;
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    font-size: 0.95rem;
    color: #b0b0d0;
    line-height: 1.7;
}
 
.use-case-box {
    background: #0d1a0d;
    border-left: 3px solid #2a7a2a;
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    font-size: 0.9rem;
    color: #90c090;
    line-height: 1.7;
}
 
.pros-cons {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin: 1rem 0;
}
 
.stSelectbox > div > div {
    background: #12121e !important;
    border: 1px solid #2a2a45 !important;
    color: #c8c8f0 !important;
    font-family: 'Syne', sans-serif !important;
    border-radius: 8px !important;
}
 
.stExpander {
    background: #12121e !important;
    border: 1px solid #1e1e35 !important;
    border-radius: 10px !important;
}
 
div[data-testid="stExpander"] {
    background: #12121e !important;
    border: 1px solid #2a2a45 !important;
    border-radius: 10px !important;
}
 
div[data-testid="stExpander"] summary {
    color: #c8c8f0 !important;
}
 
code {
    font-family: 'JetBrains Mono', monospace !important;
}
 
.stCode {
    border-radius: 8px !important;
}
 
.divider {
    border: none;
    border-top: 1px solid #1a1a2e;
    margin: 2rem 0;
}
 
.label-pill {
    background: #1a1a30;
    color: #7070c0;
    font-size: 0.68rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid #2a2a50;
    display: inline-block;
    margin-bottom: 0.8rem;
}
 
.section-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #4a4a7a;
    margin-bottom: 0.5rem;
    font-family: 'JetBrains Mono', monospace;
}
</style>
""", unsafe_allow_html=True)
sidebar()
# ── Data ────────────────────────────────────────────────────────────────────

PATTERNS = [
    {
        "num": "01",
        "title": "ETL Pattern",
        "tags": ["Batch", "Transform", "Warehouse"],
        "definition": "ETL (Extract, Transform, Load) extracts data from source systems, applies business-rule transformations on a dedicated processing server, then loads the cleaned, structured result into a target data warehouse.",
        "when_to_use": "Use ETL when your target system has strict schema requirements, when transformations are complex and compute-intensive, or when data quality must be guaranteed before it ever touches the warehouse.",
        "pros": ["Schema enforced before load", "Easier compliance/auditing", "Mature tooling ecosystem"],
        "cons": ["Slower time-to-insight", "Processing server is a bottleneck", "Schema changes are painful"],
        "examples": {
            "Pure Python": """\
import csv, sqlite3, datetime
 
# EXTRACT
def extract(filepath):
    with open(filepath, newline="") as f:
        return list(csv.DictReader(f))
 
# TRANSFORM
def transform(rows):
    cleaned = []
    for r in rows:
        try:
            cleaned.append({
                "user_id":    int(r["user_id"]),
                "revenue":    float(r["revenue"]),
                "event_date": datetime.date.fromisoformat(r["event_date"].strip()),
                "country":    r["country"].strip().upper(),
            })
        except (ValueError, KeyError):
            pass  # skip malformed rows
    return cleaned
 
# LOAD
def load(rows, db_path="warehouse.db"):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute(\"\"\"
        CREATE TABLE IF NOT EXISTS sales (
            user_id INTEGER, revenue REAL,
            event_date TEXT,  country TEXT
        )
    \"\"\")
    cur.executemany(
        "INSERT INTO sales VALUES (:user_id,:revenue,:event_date,:country)",
        rows,
    )
    con.commit(); con.close()
 
if __name__ == "__main__":
    raw  = extract("raw_sales.csv")
    data = transform(raw)
    load(data)
    print(f"Loaded {len(data)} rows.")
""",
            "Apache Airflow": """\
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
 
default_args = {"owner": "de-team", "retries": 2,
                "retry_delay": timedelta(minutes=5)}
 
def extract(**ctx):
    df = pd.read_csv("/data/raw_sales.csv")
    df.to_parquet("/tmp/raw.parquet", index=False)
    ctx["ti"].xcom_push(key="row_count", value=len(df))
 
def transform(**ctx):
    df = pd.read_parquet("/tmp/raw.parquet")
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    df = df.dropna(subset=["revenue"])
    df["country"] = df["country"].str.upper().str.strip()
    df.to_parquet("/tmp/transformed.parquet", index=False)
 
def load(**ctx):
    import sqlalchemy as sa
    engine = sa.create_engine("postgresql://user:pass@localhost/warehouse")
    pd.read_parquet("/tmp/transformed.parquet").to_sql(
        "sales", engine, if_exists="append", index=False
    )
 
with DAG("etl_sales", start_date=datetime(2024,1,1),
         schedule="@daily", default_args=default_args,
         catchup=False) as dag:
 
    t_extract   = PythonOperator(task_id="extract",   python_callable=extract)
    t_transform = PythonOperator(task_id="transform", python_callable=transform)
    t_load      = PythonOperator(task_id="load",      python_callable=load)
 
    t_extract >> t_transform >> t_load
""",
        },
    },
    {
        "num": "02",
        "title": "ELT Pattern",
        "tags": ["Cloud", "Raw Load", "Data Lake"],
        "definition": "ELT (Extract, Load, Transform) loads raw data directly into a cloud data lake or warehouse, deferring transformations until query time. The warehouse's compute engine handles transformation.",
        "when_to_use": "Ideal for cloud-native stacks (Snowflake, BigQuery, Redshift) where cheap storage and powerful SQL engines make in-place transformation more efficient than pre-processing.",
        "pros": ["Raw data always preserved", "Transformations are flexible/repeatable", "Fast initial load"],
        "cons": ["Requires powerful warehouse compute", "Raw PII may land in warehouse", "Query costs can spike"],
        "examples": {
            "Pure Python": """\
import boto3, json, datetime, pathlib
 
s3 = boto3.client("s3")
BUCKET = "my-data-lake"
 
# EXTRACT + LOAD raw to S3 (no transform yet)
def extract_and_load(api_response: list[dict]):
    key = f"raw/events/{datetime.date.today()}/batch.json"
    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps(api_response).encode(),
        ContentType="application/json",
    )
    print(f"Loaded {len(api_response)} records → s3://{BUCKET}/{key}")
 
# TRANSFORM happens later via SQL (shown as Python string here)
TRANSFORM_SQL = \"\"\"
CREATE OR REPLACE TABLE analytics.clean_events AS
SELECT
    CAST(user_id AS INT64)                          AS user_id,
    SAFE_CAST(revenue AS FLOAT64)                   AS revenue,
    UPPER(TRIM(country))                            AS country,
    DATE(PARSE_TIMESTAMP('%Y-%m-%d', event_date))   AS event_date
FROM raw.events
WHERE revenue IS NOT NULL;
\"\"\"
 
if __name__ == "__main__":
    sample = [{"user_id": "1", "revenue": "99.9",
               "country": "ph", "event_date": "2024-06-01"}]
    extract_and_load(sample)
    print("SQL to run in warehouse:", TRANSFORM_SQL[:80], "...")
""",
            "boto3 (AWS S3)": """\
import boto3, json, datetime, io
import pandas as pd
 
s3 = boto3.client("s3")
BUCKET = "my-elt-lake"
PREFIX = f"raw/orders/{datetime.date.today()}/"
 
def load_raw_to_s3(records: list[dict]):
    \"\"\"Step 1 – dump raw JSON to S3 with no transformation.\"\"\"
    body = "\\n".join(json.dumps(r) for r in records)   # newline-delimited JSON
    key  = PREFIX + "orders.ndjson"
    s3.put_object(Bucket=BUCKET, Key=key,
                  Body=body.encode(), ContentType="application/x-ndjson")
    print(f"Raw load complete → s3://{BUCKET}/{key}")
 
def read_and_transform_from_s3():
    \"\"\"Step 2 – read raw, apply transform (normally done in Athena/BigQuery).\"\"\"
    obj  = s3.get_object(Bucket=BUCKET,
                         Key=PREFIX + "orders.ndjson")
    lines = obj["Body"].read().decode().splitlines()
    df = pd.DataFrame([json.loads(l) for l in lines])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])
    return df
 
if __name__ == "__main__":
    raw = [{"order_id": "A1", "amount": "120.5", "status": "shipped"},
           {"order_id": "A2", "amount": "bad",   "status": "pending"}]
    load_raw_to_s3(raw)
    clean = read_and_transform_from_s3()
    print(clean)
""",
        },
    },
    {
        "num": "03",
        "title": "Change Data Capture",
        "tags": ["CDC", "Real-time", "Replication"],
        "definition": "CDC (Change Data Capture) monitors source databases for INSERT, UPDATE, and DELETE operations and streams those changes to downstream systems in near real-time — without polling the entire table.",
        "when_to_use": "Use CDC when you need to sync databases with low latency, build event-driven microservices, maintain audit logs, or keep a data warehouse in sync with an OLTP database.",
        "pros": ["Near real-time replication", "Minimal source DB load", "Full audit history"],
        "cons": ["Complex setup (log access)", "Schema changes need care", "Ordering guarantees vary"],
        "examples": {
            "Pure Python": """\
import sqlite3, time, json, hashlib
 
# Simulate CDC via row-hash polling (lightweight, no log access needed)
con = sqlite3.connect("source.db")
con.execute(\"\"\"CREATE TABLE IF NOT EXISTS orders
               (id INTEGER PRIMARY KEY, status TEXT, amount REAL)\"\"\")
con.commit()
 
def get_snapshot(cur):
    cur.execute("SELECT id, status, amount FROM orders")
    return {row[0]: row for row in cur.fetchall()}
 
def detect_changes(old: dict, new: dict):
    for pk, row in new.items():
        if pk not in old:
            yield {"op": "INSERT", "pk": pk, "row": row}
        elif old[pk] != row:
            yield {"op": "UPDATE", "pk": pk, "before": old[pk], "after": row}
    for pk in old:
        if pk not in new:
            yield {"op": "DELETE", "pk": pk}
 
prev = {}
print("CDC watcher started. CTRL-C to stop.")
try:
    while True:
        cur  = con.cursor()
        curr = get_snapshot(cur)
        for event in detect_changes(prev, curr):
            print(json.dumps(event))
        prev = curr
        time.sleep(2)
except KeyboardInterrupt:
    con.close()
""",
            "Apache Kafka": """\
# Producer – publishes DB change events to Kafka
from kafka import KafkaProducer
import json, time, random
 
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode(),
)
 
TOPIC = "cdc.orders"
 
def publish_change(op: str, pk: int, payload: dict):
    event = {"op": op, "pk": pk, "payload": payload,
             "ts": int(time.time() * 1000)}
    producer.send(TOPIC, key=str(pk).encode(), value=event)
    print(f"Published → {op} pk={pk}")
 
# Simulated change stream
ops = ["INSERT", "UPDATE", "DELETE"]
for i in range(10):
    publish_change(
        op=random.choice(ops),
        pk=random.randint(1, 100),
        payload={"status": random.choice(["pending","shipped","done"]),
                 "amount": round(random.uniform(10, 500), 2)},
    )
    time.sleep(0.5)
 
producer.flush()
producer.close()
 
# ── Consumer ──────────────────────────────────────────────────────────────
from kafka import KafkaConsumer
 
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode()),
    auto_offset_reset="earliest",
    group_id="cdc-processor",
)
 
for msg in consumer:
    evt = msg.value
    print(f"[{evt['op']}] pk={evt['pk']} → {evt['payload']}")
""",
        },
    },
    {
        "num": "04",
        "title": "Data Lakehouse",
        "tags": ["Delta Lake", "ACID", "Unified"],
        "definition": "The Lakehouse architecture sits a transactional metadata and indexing layer (like Delta Lake or Apache Iceberg) on top of cheap object storage, giving you ACID transactions, schema enforcement, and BI-grade query performance — without separate data warehouse infrastructure.",
        "when_to_use": "Use when you want a single storage tier that supports both ML workloads (raw files) and BI workloads (fast SQL), eliminating the lake→warehouse ETL hop.",
        "pros": ["One copy of data", "ACID on object storage", "Time-travel / versioning"],
        "cons": ["Newer tooling, steeper learning curve", "Compaction overhead", "Cloud lock-in risk"],
        "examples": {
            "Pure Python": """\
# Simulating Lakehouse concepts with plain Python + Parquet versioning
import os, json, datetime, pathlib
import pandas as pd
 
LAKE_ROOT = pathlib.Path("lakehouse/sales")
LAKE_ROOT.mkdir(parents=True, exist_ok=True)
 
def write_version(df: pd.DataFrame) -> str:
    \"\"\"Append-only versioned write (mimics Delta log).\"\"\"
    version = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    path = LAKE_ROOT / f"v_{version}.parquet"
    df.to_parquet(path, index=False)
    log_entry = {"version": version, "rows": len(df), "path": str(path)}
    with open(LAKE_ROOT / "_delta_log.ndjson", "a") as f:
        f.write(json.dumps(log_entry) + "\\n")
    return version
 
def read_latest() -> pd.DataFrame:
    \"\"\"Read all parquet files – union = current table state.\"\"\"
    files = sorted(LAKE_ROOT.glob("v_*.parquet"))
    if not files:
        return pd.DataFrame()
    return pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
 
def time_travel(before_version: str) -> pd.DataFrame:
    files = [f for f in sorted(LAKE_ROOT.glob("v_*.parquet"))
             if f.stem <= f"v_{before_version}"]
    return pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
 
# Demo
df1 = pd.DataFrame({"id": [1, 2], "amount": [100, 200]})
df2 = pd.DataFrame({"id": [3],    "amount": [300]})
v1 = write_version(df1);  print("Wrote v1:", v1)
v2 = write_version(df2);  print("Wrote v2:", v2)
print(read_latest())
""",
            "boto3 (AWS S3)": """\
import boto3, io, json, datetime
import pandas as pd
 
s3      = boto3.client("s3")
BUCKET  = "my-lakehouse"
PREFIX  = "tables/sales/"
 
def write_parquet_to_s3(df: pd.DataFrame, label: str):
    buf = io.BytesIO()
    df.to_parquet(buf, index=False)
    ts  = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    key = PREFIX + f"{label}_{ts}.parquet"
    s3.put_object(Bucket=BUCKET, Key=key, Body=buf.getvalue())
    print(f"Written: s3://{BUCKET}/{key}")
    return key
 
def read_full_table() -> pd.DataFrame:
    resp = s3.list_objects_v2(Bucket=BUCKET, Prefix=PREFIX)
    frames = []
    for obj in resp.get("Contents", []):
        body = s3.get_object(Bucket=BUCKET, Key=obj["Key"])["Body"].read()
        frames.append(pd.read_parquet(io.BytesIO(body)))
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
 
df = pd.DataFrame({"user_id": [1, 2], "spend": [50.0, 75.0]})
write_parquet_to_s3(df, "batch")
print(read_full_table())
""",
        },
    },
    {
        "num": "05",
        "title": "Real-time Streaming",
        "tags": ["Kafka", "Stream", "Low-latency"],
        "definition": "Real-time streaming continuously ingests, processes, and acts on data as it is generated — milliseconds to seconds after events occur — using message brokers and stream processors.",
        "when_to_use": "Fraud detection, live dashboards, IoT telemetry, recommendation engines, or any use-case where stale data means lost value.",
        "pros": ["Immediate insights", "Event-driven architecture", "Scales horizontally"],
        "cons": ["Complex state management", "Exactly-once semantics hard", "Higher operational cost"],
        "examples": {
            "Pure Python": """\
import threading, queue, time, random, json
 
event_queue: queue.Queue = queue.Queue(maxsize=1000)
 
def producer(n=20):
    \"\"\"Simulate sensor emitting events.\"\"\"
    for i in range(n):
        event = {"sensor_id": f"S{random.randint(1,5)}",
                 "temp_c": round(random.uniform(20, 80), 1),
                 "ts": time.time()}
        event_queue.put(event)
        time.sleep(0.1)
    event_queue.put(None)  # sentinel
 
def consumer():
    \"\"\"Process events as they arrive.\"\"\"
    while True:
        event = event_queue.get()
        if event is None:
            break
        if event["temp_c"] > 70:
            print(f"⚠ ALERT: {event['sensor_id']} = {event['temp_c']}°C")
        else:
            print(f"  OK:    {event['sensor_id']} = {event['temp_c']}°C")
        event_queue.task_done()
 
t_prod = threading.Thread(target=producer)
t_cons = threading.Thread(target=consumer)
t_cons.start(); t_prod.start()
t_prod.join();  t_cons.join()
print("Stream complete.")
""",
            "Apache Kafka": """\
# ── Producer ──────────────────────────────────────────────────────────────
from kafka import KafkaProducer
import json, time, random
 
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode(),
)
 
for _ in range(50):
    msg = {"user_id": random.randint(1, 1000),
           "event":   random.choice(["click","view","purchase"]),
           "ts":      int(time.time() * 1000)}
    producer.send("user-events", value=msg)
    time.sleep(0.05)
 
producer.flush(); producer.close()
print("Events published.")
 
# ── Consumer with windowed aggregation ────────────────────────────────────
from kafka import KafkaConsumer
from collections import defaultdict
 
consumer = KafkaConsumer(
    "user-events",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode()),
    auto_offset_reset="latest",
    group_id="stream-agg",
)
 
window: dict[str, int] = defaultdict(int)
WINDOW_SIZE = 10  # events before printing
 
for i, msg in enumerate(consumer, 1):
    evt = msg.value
    window[evt["event"]] += 1
    if i % WINDOW_SIZE == 0:
        print(f"Window stats: {dict(window)}")
        window.clear()
""",
        },
    },
    {
        "num": "06",
        "title": "Batch Processing",
        "tags": ["Scheduled", "High-volume", "Hadoop/Spark"],
        "definition": "Batch processing accumulates data over a period (hours, days) and processes it all at once in a scheduled run. The workload is high-throughput, latency-tolerant, and usually cheaper than streaming.",
        "when_to_use": "End-of-day financial reconciliation, nightly ML retraining, weekly business reports, or any job where processing all data together is more efficient than continuous processing.",
        "pros": ["Simple to reason about", "Cost-effective for large volumes", "Failure recovery is straightforward"],
        "cons": ["Data is stale between runs", "Long job failures are costly", "Poor fit for real-time needs"],
        "examples": {
            "Pure Python": """\
import csv, pathlib, datetime
from collections import defaultdict
 
INPUT_DIR  = pathlib.Path("data/raw")
OUTPUT_DIR = pathlib.Path("data/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
 
def run_batch(date: datetime.date):
    print(f"Batch run: {date}")
    revenue_by_country: dict[str, float] = defaultdict(float)
    rows_processed = 0
 
    for filepath in INPUT_DIR.glob("*.csv"):
        with open(filepath) as f:
            for row in csv.DictReader(f):
                try:
                    if datetime.date.fromisoformat(row["date"]) == date:
                        revenue_by_country[row["country"]] += float(row["revenue"])
                        rows_processed += 1
                except (ValueError, KeyError):
                    continue
 
    out = OUTPUT_DIR / f"daily_revenue_{date}.csv"
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["country", "revenue"])
        for country, rev in sorted(revenue_by_country.items()):
            w.writerow([country, round(rev, 2)])
 
    print(f"Processed {rows_processed} rows → {out}")
 
run_batch(datetime.date.today())
""",
            "Apache Airflow": """\
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import pandas as pd
 
def aggregate_daily(**ctx):
    ds   = ctx["ds"]          # YYYY-MM-DD of the run
    df   = pd.read_parquet(f"/data/raw/{ds}.parquet")
    agg  = (df.groupby("country")["revenue"]
              .sum().reset_index().rename(columns={"revenue": "total_revenue"}))
    agg["run_date"] = ds
    agg.to_parquet(f"/data/agg/{ds}.parquet", index=False)
    print(f"Aggregated {len(df)} rows for {ds}")
 
def load_to_dw(**ctx):
    import sqlalchemy as sa
    ds  = ctx["ds"]
    df  = pd.read_parquet(f"/data/agg/{ds}.parquet")
    eng = sa.create_engine("postgresql://user:pass@localhost/dw")
    df.to_sql("daily_revenue", eng, if_exists="append", index=False)
    print(f"Loaded {len(df)} aggregated rows.")
 
with DAG("batch_daily_revenue",
         start_date=datetime(2024,1,1),
         schedule="0 2 * * *",    # 2 AM every day
         catchup=True,
         default_args={"retries": 1, "retry_delay": timedelta(minutes=10)}) as dag:
 
    extract  = BashOperator(task_id="extract",
                            bash_command="python /scripts/extract.py {{ ds }}")
    agg      = PythonOperator(task_id="aggregate", python_callable=aggregate_daily)
    load     = PythonOperator(task_id="load",      python_callable=load_to_dw)
 
    extract >> agg >> load
""",
        },
    },
    {
        "num": "07",
        "title": "Data Cataloging Pattern",
        "tags": ["Metadata", "Discovery", "Governance"],
        "definition": "A Data Catalog is a centralized inventory of data assets — tables, columns, owners, lineage, and quality metrics — that enables teams to discover, understand, and trust data across the organization.",
        "when_to_use": "When your organization has many data sources, teams spend time hunting for datasets, or compliance requires knowing where sensitive data lives.",
        "pros": ["Improves data discoverability", "Enables governance/compliance", "Reduces duplicate datasets"],
        "cons": ["High initial setup cost", "Requires cultural adoption", "Metadata staleness risk"],
        "examples": {
            "Pure Python": """\
import json, datetime, pathlib
 
CATALOG_FILE = pathlib.Path("catalog.json")
 
def load_catalog() -> dict:
    if CATALOG_FILE.exists():
        return json.loads(CATALOG_FILE.read_text())
    return {}
 
def save_catalog(catalog: dict):
    CATALOG_FILE.write_text(json.dumps(catalog, indent=2, default=str))
 
def register_dataset(name: str, location: str, owner: str,
                     columns: list[str], tags: list[str] = []):
    cat = load_catalog()
    cat[name] = {
        "location":   location,
        "owner":      owner,
        "columns":    columns,
        "tags":       tags,
        "registered": datetime.datetime.utcnow().isoformat(),
    }
    save_catalog(cat)
    print(f"Registered: {name}")
 
def search(keyword: str):
    cat = load_catalog()
    results = {k: v for k, v in cat.items()
               if keyword.lower() in k.lower()
               or any(keyword.lower() in t.lower() for t in v.get("tags", []))}
    return results
 
# Demo
register_dataset("sales_daily",   "s3://datalake/sales/",   "alice@co",
                 ["date","country","revenue"], tags=["finance","pii"])
register_dataset("user_profiles", "postgres://db/users",    "bob@co",
                 ["user_id","email","signup_date"], tags=["pii","marketing"])
 
print(json.dumps(search("pii"), indent=2))
""",
            "boto3 (AWS Glue)": """\
import boto3
 
glue   = boto3.client("glue", region_name="us-east-1")
DB     = "my_catalog_db"
 
# Ensure database exists
try:
    glue.create_database(DatabaseInput={"Name": DB})
    print(f"Created database: {DB}")
except glue.exceptions.AlreadyExistsException:
    pass
 
# Register a table in the Glue Data Catalog
glue.create_table(
    DatabaseName=DB,
    TableInput={
        "Name": "sales_daily",
        "Description": "Daily aggregated sales by country",
        "TableType": "EXTERNAL_TABLE",
        "Parameters": {"classification": "parquet",
                       "owner": "alice@company.com",
                       "tags": "finance,aggregated"},
        "StorageDescriptor": {
            "Columns": [
                {"Name": "event_date", "Type": "date"},
                {"Name": "country",    "Type": "string"},
                {"Name": "revenue",    "Type": "double"},
            ],
            "Location":      "s3://my-datalake/sales/daily/",
            "InputFormat":   "org.apache.hadoop.mapred.TextInputFormat",
            "OutputFormat":  "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
            "SerdeInfo":     {"SerializationLibrary":
                              "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"},
        },
    },
)
 
# Search catalog
resp   = glue.search_tables(SearchText="sales", MaxResults=10)
for t in resp["TableList"]:
    print(t["Name"], "–", t.get("Description", ""))
""",
        },
    },
    {
        "num": "08",
        "title": "Data Mesh Pattern",
        "tags": ["Decentralized", "Domain", "Self-serve"],
        "definition": "Data Mesh decentralizes data ownership to domain teams (e.g., Orders, Users, Payments), each treating their data as a product with clear contracts, discoverability, and SLAs — governed by a federated computational governance layer.",
        "when_to_use": "When a central data team becomes a bottleneck for a large organization, or when data quality and context are best understood by the owning domain team.",
        "pros": ["Scales with org growth", "Domain expertise improves quality", "Reduces central bottleneck"],
        "cons": ["Requires strong culture/discipline", "Duplication risk between domains", "Governance complexity"],
        "examples": {
            "Pure Python": """\
# Each domain exposes a DataProduct with a defined contract
import dataclasses, datetime, pandas as pd
from abc import ABC, abstractmethod
 
@dataclasses.dataclass
class DataProductContract:
    name:        str
    owner:       str
    sla_freshness_hours: int
    output_schema: dict[str, str]   # column → dtype
 
class DataProduct(ABC):
    def __init__(self, contract: DataProductContract):
        self.contract = contract
 
    @abstractmethod
    def get_data(self) -> pd.DataFrame: ...
 
    def validate(self, df: pd.DataFrame) -> bool:
        for col, dtype in self.contract.output_schema.items():
            if col not in df.columns:
                raise ValueError(f"Missing column: {col}")
        return True
 
# ── Orders domain ──────────────────────────────────────────────────────────
class OrdersProduct(DataProduct):
    def get_data(self) -> pd.DataFrame:
        df = pd.DataFrame({
            "order_id": [1, 2, 3],
            "amount":   [100.0, 250.0, 75.0],
            "status":   ["shipped", "pending", "done"],
        })
        self.validate(df)
        return df
 
orders_product = OrdersProduct(DataProductContract(
    name="orders",
    owner="orders-team@company.com",
    sla_freshness_hours=4,
    output_schema={"order_id": "int", "amount": "float", "status": "str"},
))
 
print(orders_product.contract)
print(orders_product.get_data())
""",
            "Apache Airflow": """\
# Each domain team owns their own DAG (Data Product pipeline)
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd, sqlalchemy as sa
 
ENGINE = sa.create_engine("postgresql://user:pass@localhost/mesh")
 
# ── Orders Domain DAG ──────────────────────────────────────────────────────
def publish_orders_product():
    df = pd.read_sql("SELECT * FROM raw.orders", ENGINE)
    df = df[df["status"].notna()]
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df.to_sql("domain.orders_product", ENGINE,
              if_exists="replace", index=False)
    print(f"Published orders product: {len(df)} rows")
 
with DAG("domain_orders_product",
         start_date=datetime(2024,1,1),
         schedule="@hourly", catchup=False) as dag:
    PythonOperator(task_id="publish", python_callable=publish_orders_product)
 
# ── Downstream: cross-domain join (Consumer) ───────────────────────────────
def cross_domain_report():
    orders = pd.read_sql("SELECT * FROM domain.orders_product", ENGINE)
    users  = pd.read_sql("SELECT * FROM domain.users_product",  ENGINE)
    report = orders.merge(users, on="user_id", how="left")
    report.to_sql("reports.order_summary", ENGINE,
                  if_exists="replace", index=False)
 
with DAG("cross_domain_report",
         start_date=datetime(2024,1,1),
         schedule="@daily", catchup=False) as dag2:
    PythonOperator(task_id="report", python_callable=cross_domain_report)
""",
        },
    },
    {
        "num": "09",
        "title": "Lambda Architecture",
        "tags": ["Hybrid", "Batch+Stream", "Views"],
        "definition": "Lambda Architecture handles massive data by combining a Batch Layer (complete, accurate processing of historical data), a Speed Layer (low-latency processing of recent data), and a Serving Layer that merges both views for queries.",
        "when_to_use": "When you need both historical accuracy and real-time freshness — e.g., analytics dashboards that show historical trends alongside live data.",
        "pros": ["Fault tolerant via batch recompute", "Handles late-arriving data", "Proven at scale"],
        "cons": ["Two codebases to maintain", "Complex serving layer merge", "Kappa is often simpler"],
        "examples": {
            "Pure Python": """\
import time, threading, queue, datetime, collections
 
# ─── Batch Layer ─────────────────────────────────────────────────────────
historical = [
    {"user": "alice", "spend": 400, "date": "2024-05-01"},
    {"user": "bob",   "spend": 200, "date": "2024-05-01"},
]
 
def batch_view(records: list[dict]) -> dict[str, float]:
    totals: dict[str, float] = collections.defaultdict(float)
    for r in records:
        totals[r["user"]] += r["spend"]
    return dict(totals)
 
batch_result = batch_view(historical)
print("Batch view:", batch_result)
 
# ─── Speed Layer (real-time stream) ──────────────────────────────────────
stream: queue.Queue = queue.Queue()
speed_view: dict[str, float] = collections.defaultdict(float)
lock = threading.Lock()
 
def stream_processor():
    while True:
        event = stream.get()
        if event is None: break
        with lock:
            speed_view[event["user"]] += event["spend"]
        stream.task_done()
 
# ─── Serving Layer: merge batch + speed ──────────────────────────────────
def serving_layer() -> dict[str, float]:
    with lock:
        merged = dict(batch_result)
        for user, spend in speed_view.items():
            merged[user] = merged.get(user, 0) + spend
    return merged
 
t = threading.Thread(target=stream_processor, daemon=True)
t.start()
stream.put({"user": "alice", "spend": 50})
stream.put({"user": "carol", "spend": 120})
time.sleep(0.1)
print("Serving view:", serving_layer())
stream.put(None)
""",
            "Apache Kafka": """\
# Lambda: Kafka as Speed Layer, Parquet files as Batch Layer
from kafka import KafkaProducer, KafkaConsumer
import json, time, random, collections
 
TOPIC = "lambda-events"
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode(),
)
 
# Publish real-time events (Speed Layer input)
for _ in range(20):
    producer.send(TOPIC, {"user": f"u{random.randint(1,5)}",
                          "spend": random.uniform(5, 100)})
    time.sleep(0.05)
producer.flush(); producer.close()
 
# Speed Layer consumer – in-memory real-time view
speed_view: dict[str, float] = collections.defaultdict(float)
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode()),
    auto_offset_reset="earliest",
    group_id="lambda-speed",
    consumer_timeout_ms=3000,
)
for msg in consumer:
    evt = msg.value
    speed_view[evt["user"]] += evt["spend"]
 
# Batch Layer – precomputed totals (from nightly job)
batch_view = {"u1": 500.0, "u2": 300.0}
 
# Serving Layer – merge
final = {**batch_view}
for k, v in speed_view.items():
    final[k] = final.get(k, 0) + v
print("Final merged view:", dict(sorted(final.items())))
""",
        },
    },
    {
        "num": "10",
        "title": "Kappa Architecture",
        "tags": ["Unified Stream", "Simplified", "Reprocessing"],
        "definition": "Kappa Architecture processes everything — historical and real-time data — through a single streaming pipeline, eliminating the separate batch layer. Historical reprocessing is done by replaying the event log from the beginning.",
        "when_to_use": "When Lambda's dual codebase is too costly to maintain, your event store can hold full history (e.g., Kafka with long retention), and stream processing is mature enough to handle reprocessing.",
        "pros": ["One codebase", "Simpler operations", "Kafka log is single source of truth"],
        "cons": ["Reprocessing is slow for huge history", "Requires append-only event model", "State management is harder"],
        "examples": {
            "Pure Python": """\
import queue, threading, collections, time
 
# All data — past and present — flows through one pipeline
EVENT_LOG: list[dict] = [
    # Historical events (would be replayed from Kafka on reprocess)
    {"user": "alice", "spend": 100, "ts": 1},
    {"user": "bob",   "spend": 50,  "ts": 2},
]
 
stream: queue.Queue = queue.Queue()
state: dict[str, float] = collections.defaultdict(float)
 
def pipeline(event: dict):
    \"\"\"Single processing function handles ALL events.\"\"\"
    state[event["user"]] += event["spend"]
 
def worker():
    while True:
        evt = stream.get()
        if evt is None: break
        pipeline(evt)
        stream.task_done()
 
t = threading.Thread(target=worker, daemon=True)
t.start()
 
# Replay history (re-process from beginning)
print("Replaying historical log...")
for evt in EVENT_LOG:
    stream.put(evt)
 
# Continue with new real-time events
print("Processing real-time events...")
stream.put({"user": "alice", "spend": 75, "ts": time.time()})
stream.put({"user": "carol", "spend": 200, "ts": time.time()})
 
stream.join()
stream.put(None)
print("Kappa state:", dict(state))
""",
            "Apache Kafka": """\
# Kappa: replay from offset 0 = full historical reprocessing
from kafka import KafkaConsumer, KafkaProducer
import json, collections, time
 
TOPIC   = "kappa-events"
BROKERS = "localhost:9092"
 
# ── Produce some events (historical + new) ─────────────────────────────────
producer = KafkaProducer(bootstrap_servers=BROKERS,
                         value_serializer=lambda v: json.dumps(v).encode())
events = [{"user": "alice", "spend": 80},
          {"user": "bob",   "spend": 40},
          {"user": "alice", "spend": 60}]
for e in events:
    producer.send(TOPIC, e)
producer.flush(); producer.close()
 
# ── Single pipeline: replay from beginning for reprocessing ────────────────
def run_kappa(from_beginning=True):
    offset = "earliest" if from_beginning else "latest"
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BROKERS,
        value_deserializer=lambda m: json.loads(m.decode()),
        auto_offset_reset=offset,
        group_id=f"kappa-{'replay' if from_beginning else 'live'}",
        consumer_timeout_ms=2000,
    )
    state: dict[str, float] = collections.defaultdict(float)
    for msg in consumer:
        evt = msg.value
        state[evt["user"]] += evt["spend"]   # same logic for history & live
    return dict(state)
 
print("Full reprocess result:", run_kappa(from_beginning=True))
""",
        },
    },
    {
        "num": "11",
        "title": "Data Lineage Tracking",
        "tags": ["Provenance", "Audit", "DAG"],
        "definition": "Data Lineage tracks the complete journey of data — from its origin through every transformation and join to its final destination — creating an auditable, visual graph of data provenance.",
        "when_to_use": "Regulatory compliance (GDPR, HIPAA), debugging incorrect metrics, understanding the blast radius of upstream schema changes, or building trust in data assets.",
        "pros": ["Enables impact analysis", "Regulatory compliance", "Faster root-cause debugging"],
        "cons": ["Instrumentation overhead", "Graph can become huge", "Often requires tooling buy-in"],
        "examples": {
            "Pure Python": """\
import dataclasses, datetime, json
from typing import Optional
 
@dataclasses.dataclass
class LineageNode:
    name:        str
    node_type:   str          # "source" | "transform" | "sink"
    location:    str
    description: str = ""
 
@dataclasses.dataclass
class LineageEdge:
    source:      str
    destination: str
    operation:   str
    timestamp:   str = dataclasses.field(
        default_factory=lambda: datetime.datetime.utcnow().isoformat()
    )
 
class LineageGraph:
    def __init__(self):
        self.nodes: dict[str, LineageNode] = {}
        self.edges: list[LineageEdge]      = []
 
    def add_node(self, node: LineageNode):
        self.nodes[node.name] = node
 
    def add_edge(self, src: str, dst: str, op: str):
        self.edges.append(LineageEdge(src, dst, op))
        print(f"Lineage: {src} —[{op}]→ {dst}")
 
    def upstream_of(self, name: str) -> list[str]:
        return [e.source for e in self.edges if e.destination == name]
 
    def to_json(self) -> str:
        return json.dumps({
            "nodes": [dataclasses.asdict(n) for n in self.nodes.values()],
            "edges": [dataclasses.asdict(e) for e in self.edges],
        }, indent=2)
 
g = LineageGraph()
g.add_node(LineageNode("raw_orders",       "source",    "s3://raw/"))
g.add_node(LineageNode("clean_orders",     "transform", "s3://clean/"))
g.add_node(LineageNode("revenue_by_country","sink",     "postgres/dw"))
 
g.add_edge("raw_orders",   "clean_orders",      "null_drop + type_cast")
g.add_edge("clean_orders", "revenue_by_country","GROUP BY country")
 
print("Upstream of revenue_by_country:", g.upstream_of("revenue_by_country"))
print(g.to_json())
""",
            "Apache Airflow": """\
# Airflow's built-in Lineage via inlets/outlets
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.lineage.entities import File
from datetime import datetime
import pandas as pd
 
RAW_FILE   = File(url="s3://datalake/raw/orders.parquet")
CLEAN_FILE = File(url="s3://datalake/clean/orders.parquet")
REPORT_FILE= File(url="s3://datalake/reports/revenue.parquet")
 
def clean_orders(**ctx):
    # In real use, read from RAW_FILE.url
    df = pd.DataFrame({"order_id":[1,2], "amount":["100","bad"], "country":["PH","SG"]})
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])
    # df.to_parquet(CLEAN_FILE.url)
    print(f"Cleaned: {len(df)} rows")
 
def build_report(**ctx):
    # df = pd.read_parquet(CLEAN_FILE.url)
    df = pd.DataFrame({"amount":[100.0], "country":["PH"]})
    report = df.groupby("country")["amount"].sum().reset_index()
    print(report)
 
with DAG("lineage_example", start_date=datetime(2024,1,1),
         schedule="@daily", catchup=False) as dag:
 
    t1 = PythonOperator(
        task_id="clean_orders",
        python_callable=clean_orders,
        inlets=[RAW_FILE],        # Airflow records: reads from RAW_FILE
        outlets=[CLEAN_FILE],     # Airflow records: writes to CLEAN_FILE
    )
    t2 = PythonOperator(
        task_id="build_report",
        python_callable=build_report,
        inlets=[CLEAN_FILE],
        outlets=[REPORT_FILE],
    )
    t1 >> t2
# Lineage graph now visible in Airflow UI under Graph → Lineage
""",
        },
    },
    {
        "num": "12",
        "title": "Orchestration Pattern",
        "tags": ["Workflow", "Scheduling", "DAG"],
        "definition": "Data Orchestration manages, schedules, and monitors complex dependent pipelines — ensuring tasks run in the right order, retrying on failure, and providing observability over the entire workflow.",
        "when_to_use": "Any multi-step data pipeline where tasks depend on each other, where you need retry logic, alerting, backfill support, or a centralized view of pipeline health.",
        "pros": ["Centralized visibility", "Automatic retry/alerting", "Backfill support"],
        "cons": ["Learning curve (Airflow can be heavy)", "Single point of orchestration failure", "Scheduler lag for micro-batches"],
        "examples": {
            "Pure Python": """\
import time, traceback
from typing import Callable
 
# Minimal task orchestrator with dependency resolution
class Task:
    def __init__(self, name: str, fn: Callable,
                 depends_on: list["Task"] = None, retries: int = 2):
        self.name       = name
        self.fn         = fn
        self.depends_on = depends_on or []
        self.retries    = retries
        self.status     = "pending"
 
class DAGRunner:
    def __init__(self, tasks: list[Task]):
        self.tasks = {t.name: t for t in tasks}
 
    def run(self):
        completed: set[str] = set()
        queue = list(self.tasks.values())
 
        while queue:
            progress = False
            for task in list(queue):
                if all(d.name in completed for d in task.depends_on):
                    self._run_task(task)
                    completed.add(task.name)
                    queue.remove(task)
                    progress = True
            if not progress:
                raise RuntimeError("Circular dependency or stuck tasks")
 
    def _run_task(self, task: Task):
        for attempt in range(1, task.retries + 2):
            try:
                print(f"▶ Running [{task.name}] (attempt {attempt})")
                task.fn()
                task.status = "success"
                print(f"✔ Done    [{task.name}]")
                return
            except Exception as e:
                print(f"✘ Failed  [{task.name}]: {e}")
                if attempt > task.retries:
                    task.status = "failed"
                    raise
 
extract  = Task("extract",   lambda: print("  Extracting data..."))
transform= Task("transform", lambda: print("  Transforming..."),  depends_on=[extract])
load     = Task("load",      lambda: print("  Loading to DW..."), depends_on=[transform])
 
DAGRunner([extract, transform, load]).run()
""",
            "Apache Airflow": """\
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty  import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta
import random
 
def extract():
    print("Extracting from API...")
    if random.random() < 0.1:
        raise ValueError("API timeout simulated")
 
def validate(**ctx):
    row_count = random.randint(0, 1000)
    ctx["ti"].xcom_push(key="row_count", value=row_count)
    return "transform" if row_count > 0 else "skip_empty"
 
def transform(**ctx):
    n = ctx["ti"].xcom_pull(key="row_count")
    print(f"Transforming {n} rows...")
 
def notify_success():  print("✔ Pipeline succeeded – Slack/PagerDuty alert here")
def notify_failure():  print("✘ Pipeline failed  – alert sent")
 
default_args = {
    "retries":       3,
    "retry_delay":   timedelta(minutes=2),
    "on_failure_callback": lambda ctx: print("Task failed:", ctx["task_instance"]),
}
 
with DAG("orchestrated_pipeline",
         start_date=datetime(2024,1,1),
         schedule="0 6 * * *",
         catchup=False,
         default_args=default_args) as dag:
 
    t_extract   = PythonOperator(task_id="extract",     python_callable=extract)
    t_validate  = BranchPythonOperator(task_id="validate", python_callable=validate)
    t_transform = PythonOperator(task_id="transform",   python_callable=transform)
    t_skip      = EmptyOperator(task_id="skip_empty")
    t_success   = PythonOperator(task_id="notify_success", python_callable=notify_success,
                                 trigger_rule=TriggerRule.ONE_SUCCESS)
    t_failure   = PythonOperator(task_id="notify_failure", python_callable=notify_failure,
                                 trigger_rule=TriggerRule.ONE_FAILED)
 
    t_extract >> t_validate >> [t_transform, t_skip]
    t_transform >> t_success
    t_skip     >> t_success
    t_extract  >> t_failure
""",
        },
    },
]


st.markdown('<div class="main-title">Data Engineering Patterns</div>',
            unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Top 12 · Reference Guide · Code Examples</div>',
            unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

for p in PATTERNS:
    with st.expander(f"  {p['num']}  ·  {p['title']}", expanded=False):

        # Tags
        tags_html = "".join(f'<span class="tag">{t}</span>' for t in p["tags"])
        st.markdown(tags_html, unsafe_allow_html=True)

        # Tabs: Learn / Code
        tab_learn, tab_code = st.tabs(["📖  Learn", "💻  Code"])

        with tab_learn:
            st.markdown('<div class="section-label">Definition</div>',
                        unsafe_allow_html=True)
            st.markdown(
                f'<div class="definition-box">{p["definition"]}</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-label">When to Use</div>',
                        unsafe_allow_html=True)
            st.markdown(
                f'<div class="use-case-box">{p["when_to_use"]}</div>', unsafe_allow_html=True)

            col_pros, col_cons = st.columns(2)
            with col_pros:
                st.markdown("**✅ Pros**")
                for item in p["pros"]:
                    st.markdown(f"- {item}")
            with col_cons:
                st.markdown("**⚠️ Cons**")
                for item in p["cons"]:
                    st.markdown(f"- {item}")

        with tab_code:
            options = list(p["examples"].keys())
            selected = st.selectbox(
                "Example stack",
                options,
                key=f"select_{p['num']}",
                label_visibility="collapsed",
            )
            lang = "python"
            st.code(p["examples"][selected], language=lang)

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center;color:#3a3a5a;font-size:0.78rem;'
    'font-family:\'JetBrains Mono\',monospace;letter-spacing:1px;">'
    'DATA ENGINEERING PATTERNS · REFERENCE GUIDE</p>',
    unsafe_allow_html=True,
)

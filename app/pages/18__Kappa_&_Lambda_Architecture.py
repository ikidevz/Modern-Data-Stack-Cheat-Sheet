import streamlit as st
import pandas as pd

from components import sidebar
from utility.seo import inject_seo

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kappa vs Lambda Architecture",
    page_icon="⚡",
    layout="wide",
)
inject_seo('Kappa & Lambda Architecture')
# ── Minimal Light CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Clean white base */
.stApp { background: #ffffff; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #f8f9fa !important;
    border-right: 1px solid #e9ecef;
}

/* Remove default padding on metric */
[data-testid="metric-container"] {
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 12px 16px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    border-bottom: 2px solid #e9ecef;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 4px 4px 0 0;
    font-weight: 500;
    color: #6c757d;
}
.stTabs [aria-selected="true"] {
    color: #0d6efd !important;
    border-bottom: 2px solid #0d6efd !important;
}

/* Expander */
div[data-testid="stExpander"] {
    border: 1px solid #e9ecef !important;
    border-radius: 8px !important;
}

/* Callout boxes using native Streamlit info/warning/success/error */
div[data-testid="stAlert"] { border-radius: 8px; }

/* Code block */
.stCodeBlock { border-radius: 6px !important; }

/* Divider spacing */
hr { margin: 1.5rem 0; border-color: #e9ecef; }

/* Table */
.data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
}
.data-table th {
    background: #f1f3f5;
    color: #343a40;
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
    border-bottom: 2px solid #dee2e6;
}
.data-table td {
    padding: 9px 14px;
    border-bottom: 1px solid #f1f3f5;
    color: #495057;
    vertical-align: top;
}
.data-table tr:hover td { background: #f8f9fa; }

.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
}
.badge-lambda { background: #fff3cd; color: #856404; }
.badge-kappa  { background: #cfe2ff; color: #084298; }
</style>
""", unsafe_allow_html=True)
sidebar()

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ⚡ Data Arch Guide")
    st.divider()
    page = st.radio(
        "Navigate",
        ["📖 Documentation", "🐍 Python Examples",
            "📋 Cheat Sheet", "🎛️ Interactive Tools"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("Covers Lambda · Kappa · Batch · Stream · Kafka · Spark · Flink")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DOCUMENTATION
# ══════════════════════════════════════════════════════════════════════════════
if "📖 Documentation" in page:
    st.title("⚡ Kappa vs Lambda Architecture")
    st.markdown("##### A Data Engineer's Deep-Dive Reference")
    st.divider()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Lambda Layers", "3", help="Batch + Speed + Serving")
    col2.metric("Kappa Layers", "2", help="Stream + Serving")
    col3.metric("Core Tools", "6+")
    col4.metric("Architectures Covered", "2")

    st.divider()

    tab_lambda, tab_kappa, tab_compare = st.tabs([
        "🟡  Lambda Architecture",
        "🔵  Kappa Architecture",
        "⚖️  Side-by-Side Comparison",
    ])

    # ─── LAMBDA ──────────────────────────────────────────────────────────────
    with tab_lambda:
        st.subheader("🟡 Lambda Architecture")
        st.markdown(
            "Coined by **Nathan Marz (~2011)**. Handles massive data with both batch and "
            "stream processing simultaneously — robust, fault-tolerant, low-latency reads."
        )

        st.markdown("#### 🏗️ The Three Layers")
        lcol1, lcol2, lcol3 = st.columns(3)
        with lcol1:
            st.info("**📦 Batch Layer**\n\nManages the master dataset. Processes **all historical data** with high accuracy.\n\n- Immutable, append-only\n- High latency (hours–days)\n- 100% accurate\n\n*Tools: Hadoop, Apache Spark*")
        with lcol2:
            st.warning("**⚡ Speed Layer**\n\nCompensates for batch latency. Processes **real-time streams** only.\n\n- Only recent data\n- Low latency (seconds)\n- Approximate accuracy\n\n*Tools: Flink, Kafka Streams*")
        with lcol3:
            st.success("**🗄️ Serving Layer**\n\nMerges batch + speed views.\n\n- Low-latency reads\n- Random read access\n- Ad-hoc query support\n\n*Tools: Cassandra, Druid, Redis*")

        st.markdown("#### 🔄 Data Flow")
        st.code("""
Raw Data / Events
      │
      ├───────────────────────────────┐
      ▼                               ▼
 [BATCH LAYER]                  [SPEED LAYER]
  Spark / Hadoop              Flink / Kafka Streams
  All historical data          Recent data only
  High latency, accurate       Low latency, approximate
      │                               │
      ▼                               ▼
 Batch Views (S3/HDFS)       Real-time Views (Redis)
      │                               │
      └──────────────┬────────────────┘
                     ▼
              [SERVING LAYER]
               Druid / HBase
                     │
                     ▼
              Query Results ← User / App
        """, language="text")

        st.markdown("#### ✅ When to Use Lambda")
        st.success(
            "**Lambda is ideal when:**\n"
            "- You need both historical reprocessing AND real-time results\n"
            "- Batch accuracy is non-negotiable (finance, compliance, billing)\n"
            "- Teams have separate Batch and Stream engineers\n"
            "- Data volumes are enormous\n"
            "- Fault tolerance with full reprocessing capability is required"
        )
        st.error(
            "**⚠️ Lambda Challenges:**\n"
            "- Code duplication — same logic written twice (batch + stream)\n"
            "- High operational complexity — two systems to maintain\n"
            "- Debugging is harder across two separate pipelines\n"
            "- Keeping batch and speed layer semantics in sync is error-prone"
        )

        st.markdown("#### 🛠️ Lambda Tech Stack")
        st.dataframe(pd.DataFrame({
            "Layer":   ["Ingestion", "Batch",    "Speed",             "Storage",         "Serving"],
            "OSS":     ["Kafka",     "Spark",     "Flink",             "HDFS / S3",       "Druid / Cassandra"],
            "AWS":     ["Kinesis",   "EMR+Glue",  "Kinesis Analytics", "S3 + DynamoDB",   "Redshift / DynamoDB"],
            "GCP":     ["Pub/Sub",   "Dataproc",  "Dataflow",          "GCS + Bigtable",  "BigQuery"],
        }), use_container_width=True, hide_index=True)

    # ─── KAPPA ───────────────────────────────────────────────────────────────
    with tab_kappa:
        st.subheader("🔵 Kappa Architecture")
        st.markdown(
            "Proposed by **Jay Kreps (LinkedIn/Confluent, 2014)**. A simpler alternative: "
            "one stream-processing engine handles everything — real-time and historical reprocessing."
        )

        st.markdown("#### 🏗️ The Two Layers")
        kcol1, kcol2 = st.columns(2)
        with kcol1:
            st.info("**🌊 Stream Processing Layer**\n\nOne engine handles everything.\n\n- Unified processing logic (write once)\n- Reprocess by replaying Kafka from offset 0\n- Stateful stream processing\n- Event-time + watermarks\n\n*Tools: Kafka + Flink / Kafka Streams*")
        with kcol2:
            st.success("**🗄️ Serving Layer**\n\nStores & serves materialized views.\n\n- Fast random-read access\n- Fully rebuilt from stream replay\n- Time-series, aggregates, lookups\n\n*Tools: ClickHouse, Redis, Cassandra*")

        st.markdown("#### 🔄 Data Flow")
        st.code("""
Raw Data / Events
      │
      ▼
[Kafka / Event Log]  ◄─── Immutable, retained long-term
      │
      │  replay from offset 0 → reprocessing
      │  OR consume latest   → real-time
      │
      ▼
[STREAM PROCESSING LAYER]
  Flink / Kafka Streams / Spark Structured Streaming
  Single codebase handles ALL processing
      │
      ├── Windowed Aggregations
      ├── Joins & Enrichments
      ├── ML Feature Computation
      └── Event-driven Transformations
      │
      ▼
[SERVING LAYER]
  ClickHouse / Redis / Cassandra
      │
      ▼
  Query Results ← User / App / Dashboard
        """, language="text")

        st.markdown("#### ✅ When to Use Kappa")
        st.success(
            "**Kappa is ideal when:**\n"
            "- You want one codebase for both historical and real-time processing\n"
            "- Stream processing latency is acceptable as batch replacement\n"
            "- Your data volumes fit within Kafka's retention window\n"
            "- Small-to-medium team that can't maintain two separate systems\n"
            "- Building event-driven microservices or streaming pipelines"
        )
        st.error(
            "**⚠️ Kappa Challenges:**\n"
            "- Reprocessing is slower than dedicated batch at petabyte scale\n"
            "- Kafka retention costs — storing all raw events long-term is expensive\n"
            "- Complex historical joins are harder in streaming than batch SQL\n"
            "- Stateful stream processing debugging is non-trivial"
        )

        st.markdown("#### 🛠️ Kappa Tech Stack")
        st.dataframe(pd.DataFrame({
            "Component":  ["Event Log",  "Stream Processing",        "State Store",    "Serving"],
            "OSS":        ["Kafka",       "Flink / Kafka Streams",    "RocksDB",        "ClickHouse / Redis"],
            "AWS":        ["MSK/Kinesis", "Kinesis Data Analytics",   "DynamoDB",       "Redshift / ElastiCache"],
            "GCP":        ["Pub/Sub",     "Dataflow",                 "Bigtable",       "BigQuery / Memorystore"],
        }), use_container_width=True, hide_index=True)

    # ─── COMPARISON ──────────────────────────────────────────────────────────
    with tab_compare:
        st.subheader("⚖️ Architecture Comparison")
        st.dataframe(pd.DataFrame({
            "Dimension":           ["Complexity", "Code Duplication", "Latency", "Historical Accuracy",
                                    "Reprocessing", "Scalability", "Operational Cost",
                                    "Data Retention Cost", "Time to Implement", "Best For"],
            "🟡 Lambda":           ["High (2 systems)", "Yes — batch + stream logic",
                                   "Near-real-time (speed layer)", "Exact (batch recomputes)",
                                   "Batch layer re-runs", "Excellent (battle-tested)",
                                   "High (two teams/stacks)", "Low (S3/HDFS cheap)",
                                   "Weeks–Months", "Finance, compliance, large orgs"],
            "🔵 Kappa":            ["Medium (1 system)", "No — single codebase",
                                   "Real-time / seconds", "Replay-based reprocessing",
                                   "Replay Kafka from offset 0", "Good (limited by stream)",
                                   "Lower (unified)", "Higher (Kafka retention)",
                                   "Days–Weeks", "Startups, event-driven apps"],
        }), use_container_width=True, hide_index=True)

        st.markdown("#### 🧭 Decision Framework")
        st.code("""
Start Here
    │
    ├─ Need 100% historical accuracy for compliance/audit?
    │       YES ──► Lambda Architecture
    │       NO ↓
    ├─ Separate Batch + Streaming engineering teams?
    │       YES ──► Lambda Architecture
    │       NO ↓
    ├─ Can afford storing ALL raw events in Kafka long-term?
    │       NO  ──► Lambda Architecture (use cheap blob storage)
    │       YES ↓
    ├─ Is reducing codebase complexity the top priority?
    │       YES ──► Kappa Architecture
    │       ↓
    └─ Default for greenfield event-driven projects ──► Kappa
        """, language="text")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PYTHON EXAMPLES
# ══════════════════════════════════════════════════════════════════════════════
elif "🐍 Python Examples" in page:
    st.title("🐍 Python Examples")
    st.markdown(
        "##### Production-grade patterns used by professional Data Engineers")
    st.divider()

    # ── Filters ───────────────────────────────────────────────────────────────
    fc1, fc2, fc3 = st.columns([2, 2, 3])
    with fc1:
        arch_filter = st.selectbox(
            "Architecture",
            ["Both", "🟡 Lambda", "🔵 Kappa"],
        )
    with fc2:
        topic_filter = st.multiselect(
            "Topic",
            ["Batch Processing", "Stream Processing", "Serving Layer",
             "Reprocessing", "Orchestration", "Monitoring", "ML Features"],
            default=[],
            placeholder="All topics",
        )
    with fc3:
        search_term = st.text_input(
            "🔍 Search examples", placeholder="e.g. Kafka, Redis, Flink...")

    st.divider()

    # ── Example registry ──────────────────────────────────────────────────────
    # Each entry: (arch, topic, title, description, code)
    EXAMPLES = []

    # ── LAMBDA EXAMPLES ───────────────────────────────────────────────────────
    EXAMPLES.append(("Lambda", "Batch Processing",
                     "L1 — PySpark Batch Layer: Daily Aggregation Job",
                     "Batch layer job processing all historical clickstream events from S3/HDFS. Computes daily user engagement metrics and writes batch views to Parquet. Runs nightly via Airflow.",
                     '''# batch_layer/daily_user_metrics.py
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def create_spark_session(app_name: str) -> SparkSession:
    return (SparkSession.builder
        .appName(app_name)
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        .config("spark.sql.shuffle.partitions", "200")
        .getOrCreate())

def read_raw_events(spark, s3_path: str, processing_date: str):
    """Read raw immutable events — batch layer source of truth."""
    return (spark.read
        .option("mergeSchema", "true")
        .parquet(f"{s3_path}/date={processing_date}"))

def compute_batch_view(df):
    """Batch view: 100% accurate daily user engagement metrics."""
    return (df
        .groupBy("user_id", "event_date")
        .agg(
            F.count("event_id").alias("total_events"),
            F.countDistinct("session_id").alias("total_sessions"),
            F.sum("revenue_usd").alias("total_revenue"),
            F.avg("page_load_ms").alias("avg_page_load_ms"),
            F.approx_count_distinct("product_id").alias("unique_products_viewed"),
            F.max("event_timestamp").alias("last_active_ts"),
        )
        .withColumn("batch_computed_at", F.lit(datetime.utcnow().isoformat()))
        .withColumn("is_batch_view", F.lit(True))
    )

def write_batch_view(df, output_path: str):
    (df.repartition(50)
       .write
       .mode("overwrite")
       .partitionBy("event_date")
       .parquet(f"{output_path}/user_daily_metrics"))

def run_batch_job(processing_date: str):
    spark = create_spark_session("LambdaBatchLayer-UserMetrics")
    raw_df = read_raw_events(spark, "s3://my-datalake/raw/clickstream", processing_date)
    logger.info(f"Read {raw_df.count():,} raw events")
    batch_view_df = compute_batch_view(raw_df)
    write_batch_view(batch_view_df, "s3://my-datalake/batch-views")
    spark.stop()

if __name__ == "__main__":
    import sys
    date = sys.argv[1] if len(sys.argv) > 1 else (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
    run_batch_job(date)
'''))

    EXAMPLES.append(("Lambda", "Stream Processing",
                     "L2 — Speed Layer: Real-time Kafka Consumer with Redis",
                     "Speed layer consuming Kafka events, computing rolling 1-hour metrics, writing to Redis with 2-hour TTL. Compensates for batch latency until the next batch job.",
                     '''# speed_layer/realtime_consumer.py
from kafka import KafkaConsumer
import redis, json, logging, time
from datetime import datetime, timezone
from collections import defaultdict

logger = logging.getLogger(__name__)

class SpeedLayerConsumer:
    """Lambda Speed Layer — compensates for batch latency."""
    
    def __init__(self, kafka_brokers: list, redis_host: str):
        self.consumer = KafkaConsumer(
            "clickstream-events",
            bootstrap_servers=kafka_brokers,
            group_id="speed-layer-user-metrics",
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="latest",
            enable_auto_commit=True,
            max_poll_records=500,
        )
        self.redis = redis.Redis(host=redis_host, port=6379, decode_responses=True)
        self.local_buffer = defaultdict(lambda: {"event_count": 0, "revenue": 0.0, "sessions": set()})
        self.flush_interval = 5
        self.last_flush = time.time()

    def process_event(self, event: dict):
        user_id = event.get("user_id")
        if not user_id:
            return
        buf = self.local_buffer[user_id]
        buf["event_count"] += 1
        buf["revenue"] += float(event.get("revenue_usd", 0))
        buf["sessions"].add(event.get("session_id", ""))

    def flush_to_redis(self):
        """Atomic pipeline write — 2-hour TTL (batch catches up within 24h)."""
        pipe = self.redis.pipeline()
        now_hour = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H")
        for user_id, metrics in self.local_buffer.items():
            key = f"speed:user_metrics:{user_id}:{now_hour}"
            pipe.hincrbyfloat(key, "event_count", metrics["event_count"])
            pipe.hincrbyfloat(key, "revenue_usd", metrics["revenue"])
            pipe.hincrbyfloat(key, "session_count", len(metrics["sessions"]))
            pipe.expire(key, 7200)  # 2-hour TTL
        pipe.execute()
        self.local_buffer.clear()
        self.last_flush = time.time()

    def run(self):
        for msg in self.consumer:
            self.process_event(msg.value)
            if time.time() - self.last_flush >= self.flush_interval:
                self.flush_to_redis()

if __name__ == "__main__":
    SpeedLayerConsumer(["kafka-1:9092"], "redis-speed-layer").run()
'''))

    EXAMPLES.append(("Lambda", "Serving Layer",
                     "L3 — Serving Layer: Merge Batch + Speed Views (FastAPI)",
                     "FastAPI microservice that merges batch views (PostgreSQL) with speed layer (Redis). The core Lambda pattern — combine both for accuracy + recency.",
                     '''# serving_layer/query_service.py
from fastapi import FastAPI
from pydantic import BaseModel
import redis, psycopg2
from datetime import datetime, timezone, timedelta
from typing import Optional

app = FastAPI(title="Lambda Serving Layer")
redis_client = redis.Redis(host="redis-speed-layer", port=6379, decode_responses=True)

class UserMetrics(BaseModel):
    user_id: str
    total_events: int
    total_revenue: float
    total_sessions: int
    source: str
    as_of: str

def get_batch_view(user_id: str, date: str) -> Optional[dict]:
    conn = psycopg2.connect(host="postgres-serving", database="lambda_serving",
                            user="de_user", password="secret")
    cur = conn.cursor()
    cur.execute("""
        SELECT total_events, total_revenue, total_sessions
        FROM user_daily_metrics WHERE user_id = %s AND event_date = %s
    """, (user_id, date))
    row = cur.fetchone()
    cur.close(); conn.close()
    return {"events": row[0], "revenue": float(row[1]), "sessions": row[2]} if row else None

def get_speed_view(user_id: str) -> dict:
    now_hour = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H")
    data = redis_client.hgetall(f"speed:user_metrics:{user_id}:{now_hour}")
    return {
        "events":   int(float(data.get("event_count", 0))),
        "revenue":  float(data.get("revenue_usd", 0.0)),
        "sessions": int(float(data.get("session_count", 0))),
    }

@app.get("/metrics/user/{user_id}", response_model=UserMetrics)
def get_user_metrics(user_id: str):
    """Merge batch + speed views — the Lambda serving pattern."""
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
    batch = get_batch_view(user_id, yesterday)
    speed = get_speed_view(user_id)
    source = "merged" if batch else "speed_only"
    b = batch or {"events": 0, "revenue": 0.0, "sessions": 0}
    return UserMetrics(
        user_id=user_id,
        total_events=b["events"] + speed["events"],
        total_revenue=b["revenue"] + speed["revenue"],
        total_sessions=b["sessions"] + speed["sessions"],
        source=source,
        as_of=datetime.now(timezone.utc).isoformat(),
    )
'''))

    EXAMPLES.append(("Lambda", "Orchestration",
                     "L4 — Batch Pipeline Orchestration (Airflow DAG)",
                     "Airflow DAG orchestrating the Lambda batch layer nightly: validate raw data, run PySpark, load serving layer, invalidate speed cache. Supports backfills.",
                     '''# dags/lambda_batch_pipeline.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import logging, boto3, psycopg2, redis

logger = logging.getLogger(__name__)

DEFAULT_ARGS = {
    "owner": "data-engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=10),
    "email_on_failure": True,
    "email": ["de-team@company.com"],
}

with DAG(
    dag_id="lambda_batch_layer_pipeline",
    default_args=DEFAULT_ARGS,
    schedule_interval="0 3 * * *",  # 3am UTC nightly
    start_date=days_ago(1),
    catchup=True,   # Enables historical backfill
    max_active_runs=3,
    tags=["lambda", "batch-layer"],
) as dag:

    def check_raw_data(**context):
        ds = context["ds"]
        s3 = boto3.client("s3")
        r = s3.list_objects_v2(Bucket="my-datalake", Prefix=f"raw/clickstream/date={ds}/", MaxKeys=1)
        if "Contents" not in r:
            raise ValueError(f"No raw data for {ds}")

    def load_serving(**context):
        ds = context["ds"]
        conn = psycopg2.connect(host="postgres-serving", database="lambda_serving",
                                user="de_user", password="secret")
        cur = conn.cursor()
        cur.execute(f"DELETE FROM user_daily_metrics WHERE event_date = '{ds}'")
        cur.execute(f"INSERT INTO user_daily_metrics SELECT * FROM staging WHERE event_date = '{ds}'")
        conn.commit(); cur.close(); conn.close()

    def invalidate_cache(**context):
        ds = context["ds"]
        r = redis.Redis(host="redis-speed-layer", port=6379, decode_responses=True)
        keys = r.keys(f"speed:user_metrics:*:{ds}*")
        if keys:
            r.delete(*keys)
            logger.info(f"Invalidated {len(keys)} speed layer keys")

    validate = PythonOperator(task_id="validate_raw_data", python_callable=check_raw_data)

    compute = SparkSubmitOperator(
        task_id="compute_batch_views",
        application="s3://my-datalake/jobs/daily_user_metrics.py",
        conn_id="spark_emr",
        conf={"spark.executor.memory": "8g", "spark.executor.instances": "20",
              "spark.sql.adaptive.enabled": "true"},
        application_args=["--date", "{{ ds }}"],
    )

    load    = PythonOperator(task_id="load_serving_layer",  python_callable=load_serving)
    cache   = PythonOperator(task_id="invalidate_speed_cache", python_callable=invalidate_cache)

    validate >> compute >> load >> cache
'''))

    EXAMPLES.append(("Lambda", "Monitoring",
                     "L5 — Lambda Pipeline Monitor with Prometheus & Graceful Degradation",
                     "Production pipeline manager with health checks, Prometheus metrics, and graceful degradation — falls back to batch-only when the speed layer is unavailable.",
                     '''# lambda_pipeline/pipeline_manager.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import redis, psycopg2, logging, time
from dataclasses import dataclass
from typing import Optional

QUERY_COUNTER = Counter("lambda_serving_queries_total", "Total queries", ["source"])
QUERY_LATENCY = Histogram("lambda_serving_latency_seconds", "Query latency")
SPEED_LAYER_UP = Gauge("lambda_speed_layer_healthy", "Speed layer health")
BATCH_LAG_HOURS = Gauge("lambda_batch_lag_hours", "Hours since last batch run")

@dataclass
class Config:
    redis_host: str = "redis-speed-layer"
    postgres_host: str = "postgres-serving"
    batch_lag_alert_hours: int = 25

class LambdaPipelineManager:
    def __init__(self, config: Config):
        self.config = config
        self._redis: Optional[redis.Redis] = None
        self._speed_ok = True

    @property
    def redis(self):
        if self._redis is None:
            self._redis = redis.Redis(host=self.config.redis_host, port=6379,
                                      socket_connect_timeout=2, decode_responses=True)
        return self._redis

    def health_check(self) -> bool:
        try:
            self.redis.ping()
            SPEED_LAYER_UP.set(1); self._speed_ok = True
        except Exception:
            SPEED_LAYER_UP.set(0); self._speed_ok = False
        return self._speed_ok

    @QUERY_LATENCY.time()
    def query(self, user_id: str) -> dict:
        batch = self._batch(user_id)
        speed = self._speed(user_id) if self.health_check() else None
        source = ("merged" if batch and speed
                  else "batch_only_degraded" if not speed
                  else "speed_only")
        QUERY_COUNTER.labels(source=source).inc()
        b = batch or {"events": 0, "revenue": 0.0, "sessions": 0}
        s = speed or {"events": 0, "revenue": 0.0, "sessions": 0}
        return {
            "total_events":   b["events"] + s["events"],
            "total_revenue":  round(b["revenue"] + s["revenue"], 2),
            "total_sessions": b["sessions"] + s["sessions"],
            "source": source,
        }

    def _batch(self, user_id: str):
        try:
            conn = psycopg2.connect(host=self.config.postgres_host, database="lambda_serving",
                                    user="de_user", password="secret")
            cur = conn.cursor()
            cur.execute("""
                SELECT SUM(total_events), SUM(total_revenue), SUM(total_sessions)
                FROM user_daily_metrics WHERE user_id = %s
                  AND event_date >= CURRENT_DATE - INTERVAL \'30 days\'
            """, (user_id,))
            row = cur.fetchone(); cur.close(); conn.close()
            return {"events": row[0] or 0, "revenue": float(row[1] or 0), "sessions": row[2] or 0}
        except Exception:
            return None

    def _speed(self, user_id: str):
        from datetime import datetime, timezone
        key = f"speed:user_metrics:{user_id}:{datetime.now(timezone.utc).strftime(\'%Y-%m-%dT%H\')}"
        data = self.redis.hgetall(key)
        return {"events": int(float(data.get("event_count", 0))),
                "revenue": float(data.get("revenue_usd", 0.0)),
                "sessions": int(float(data.get("session_count", 0)))}

if __name__ == "__main__":
    start_http_server(8000)
    mgr = LambdaPipelineManager(Config())
    print(mgr.query("user-12345"))
'''))

    EXAMPLES.append(("Lambda", "Batch Processing",
                     "L6 — Schema Evolution & Backward-Compatible Batch Views",
                     "Handles schema evolution in the batch layer using PySpark with Delta Lake. Safely adds new columns without breaking existing consumers.",
                     '''# batch_layer/schema_evolution.py
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType
from delta import configure_spark_with_delta_pip
import logging

logger = logging.getLogger(__name__)

SCHEMA_V1 = StructType([
    StructField("user_id", StringType(), True),
    StructField("event_date", StringType(), True),
    StructField("total_events", LongType(), True),
    StructField("total_revenue", DoubleType(), True),
])

# Schema V2 adds two new nullable columns — backward compatible
SCHEMA_V2 = StructType(SCHEMA_V1.fields + [
    StructField("total_sessions", LongType(), True),
    StructField("avg_page_load_ms", DoubleType(), True),
])

def build_spark():
    builder = (SparkSession.builder
        .appName("LambdaBatch-SchemaEvolution")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog"))
    return configure_spark_with_delta_pip(builder).getOrCreate()

def compute_v2_batch_view(df):
    return (df
        .groupBy("user_id", F.to_date("event_timestamp").alias("event_date"))
        .agg(
            F.count("*").alias("total_events"),
            F.sum("revenue_usd").alias("total_revenue"),
            F.countDistinct("session_id").alias("total_sessions"),   # NEW in V2
            F.avg("page_load_ms").alias("avg_page_load_ms"),          # NEW in V2
        ))

def write_delta_with_schema_evolution(df, delta_path: str):
    """
    Delta Lake mergeSchema=true — new columns are added automatically.
    Existing consumers reading V1 columns are unaffected.
    """
    (df.write
        .format("delta")
        .mode("overwrite")
        .option("mergeSchema", "true")     # KEY: enables schema evolution
        .option("overwriteSchema", "false") # Don't drop existing columns
        .partitionBy("event_date")
        .save(delta_path))
    logger.info("Batch view written with V2 schema (backward compatible)")

def verify_schema_compatibility(spark, delta_path: str):
    """Read back and confirm V1 consumers can still access their columns."""
    df = spark.read.format("delta").load(delta_path)
    v1_cols = [f.name for f in SCHEMA_V1.fields]
    missing = [c for c in v1_cols if c not in df.columns]
    if missing:
        raise RuntimeError(f"Schema regression! Missing V1 columns: {missing}")
    logger.info(f"Schema compatibility verified. Columns: {df.columns}")

if __name__ == "__main__":
    spark = build_spark()
    raw = spark.read.parquet("s3://my-datalake/raw/clickstream/date=2024-01-15")
    view = compute_v2_batch_view(raw)
    write_delta_with_schema_evolution(view, "s3://my-datalake/batch-views/user_daily")
    verify_schema_compatibility(spark, "s3://my-datalake/batch-views/user_daily")
    spark.stop()
'''))

    # ── KAPPA EXAMPLES ────────────────────────────────────────────────────────
    EXAMPLES.append(("Kappa", "Stream Processing",
                     "K1 — Unified Kafka Stream Processor (confluent-kafka)",
                     "Single Kappa processor handling BOTH real-time and historical reprocessing. Same code, different offset. Start with REPROCESS_FROM_BEGINNING=true for historical replay.",
                     '''# kappa/stream_processor.py
from confluent_kafka import Consumer, Producer, KafkaException
import json, logging, signal, os
from datetime import datetime, timezone
from collections import defaultdict
import clickhouse_driver

logger = logging.getLogger(__name__)

class KappaStreamProcessor:
    """
    Kappa Architecture: one processor for everything.
    Real-time mode   → consume from latest offset
    Reprocessing mode → consume from offset 0 (same code!)
    """
    def __init__(self, brokers, topic, group_id, start_from_beginning=False):
        self.consumer = Consumer({
            "bootstrap.servers": brokers,
            "group.id": group_id,
            "auto.offset.reset": "earliest" if start_from_beginning else "latest",
            "enable.auto.commit": False,
            "max.poll.interval.ms": 300000,
        })
        self.topic = topic
        self.consumer.subscribe([topic])
        self.ch = clickhouse_driver.Client(host="clickhouse-serving")
        self.state = defaultdict(lambda: {"events": 0, "revenue": 0.0, "sessions": set()})
        self.running = True
        signal.signal(signal.SIGTERM, lambda *_: setattr(self, "running", False))

    def process_event(self, event: dict):
        """Core logic — identical for real-time and replay."""
        user_id = event.get("user_id")
        if not user_id:
            return None
        ts = datetime.fromisoformat(event["event_timestamp"])
        key = f"{user_id}:{ts.strftime('%Y-%m-%dT%H:00:00')}"
        s = self.state[key]
        s["events"] += 1
        s["revenue"] += float(event.get("revenue_usd", 0))
        s["sessions"].add(event.get("session_id", ""))
        return {"user_id": user_id, "hour": ts.strftime("%Y-%m-%dT%H:00:00"),
                "event_count": s["events"], "revenue_usd": round(s["revenue"], 4),
                "session_count": len(s["sessions"]),
                "processed_at": datetime.now(timezone.utc).isoformat()}

    def flush(self, records: list):
        if not records:
            return
        self.ch.execute(
            "INSERT INTO user_hourly_metrics "
            "(user_id, hour, event_count, revenue_usd, session_count, processed_at) VALUES",
            [(r["user_id"], r["hour"], r["event_count"],
              r["revenue_usd"], r["session_count"], r["processed_at"]) for r in records]
        )

    def run(self, flush_every=1000):
        buffer, count = [], 0
        while self.running:
            msg = self.consumer.poll(timeout=1.0)
            if msg is None or msg.error():
                continue
            result = self.process_event(json.loads(msg.value().decode()))
            if result:
                buffer.append(result); count += 1
            if len(buffer) >= flush_every:
                self.flush(buffer)
                self.consumer.commit(asynchronous=False)
                buffer.clear()
        if buffer:
            self.flush(buffer); self.consumer.commit(asynchronous=False)
        self.consumer.close()

if __name__ == "__main__":
    reprocess = os.getenv("REPROCESS_FROM_BEGINNING", "false").lower() == "true"
    KappaStreamProcessor(
        brokers="kafka-1:9092,kafka-2:9092",
        topic="clickstream-events",
        group_id="kappa-v2" if reprocess else "kappa-live",
        start_from_beginning=reprocess,
    ).run()
'''))

    EXAMPLES.append(("Kappa", "Stream Processing",
                     "K2 — Stateful Windowed Aggregation with Faust (Kafka Streams for Python)",
                     "Faust-based Kafka Streams app with 5-minute tumbling windows backed by RocksDB state. Core Kappa stateful processing pattern.",
                     '''# kappa/faust_windowed.py
# pip install faust-streaming
import faust
from faust import Record
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class ClickEvent(Record, serializer="json"):
    user_id: str; event_id: str; event_type: str
    revenue_usd: float = 0.0; session_id: str = ""

class WindowMetrics(Record, serializer="json"):
    user_id: str; window_start: str; event_count: int = 0
    total_revenue: float = 0.0; unique_sessions: int = 0

app = faust.App(
    "kappa-windowed-metrics",
    broker="kafka://kafka-1:9092",
    store="rocksdb://",      # Persistent, survives restarts
    topic_replication_factor=3,
)

clicks  = app.topic("clickstream-events", value_type=ClickEvent)
metrics = app.topic("user-window-metrics", value_type=WindowMetrics)

# 5-minute tumbling windows — state in RocksDB
event_counts = app.Table("event_counts", default=int).tumbling(300, expires=3600)
revenue_totals = app.Table("revenue",    default=float).tumbling(300, expires=3600)

@app.agent(clicks)
async def process(events):
    """Single agent — same code runs for real-time AND replay."""
    async for ev in events:
        event_counts[ev.user_id] += 1
        revenue_totals[ev.user_id] += ev.revenue_usd
        await metrics.send(key=ev.user_id, value=WindowMetrics(
            user_id=ev.user_id,
            window_start=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:00"),
            event_count=event_counts[ev.user_id].value(),
            total_revenue=round(revenue_totals[ev.user_id].value(), 4),
        ))

@app.timer(interval=300.0)
async def log_summary():
    logger.info("5-minute window complete — state persisted to RocksDB.")

if __name__ == "__main__":
    app.main()
    # faust -A kappa.faust_windowed worker -l info
'''))

    EXAMPLES.append(("Kappa", "Reprocessing",
                     "K3 — Historical Reprocessing Manager: Replay from Offset 0",
                     "Orchestrates a full Kappa reprocessing workflow — new consumer group, offset reset, process into a new table, atomic swap in ClickHouse. Zero downtime.",
                     '''# kappa/reprocessing_manager.py
from confluent_kafka.admin import AdminClient
from confluent_kafka import Consumer, TopicPartition
import subprocess, logging, time, uuid
import clickhouse_driver

logger = logging.getLogger(__name__)
BROKERS = "kafka-1:9092,kafka-2:9092"

class KappaReprocessingManager:
    """
    Kappa reprocessing strategy:
    1. New consumer group → start from offset 0
    2. Process into a new table version
    3. Atomic swap (zero downtime)
    4. Decommission old group
    """
    def __init__(self):
        self.ch = clickhouse_driver.Client(host="clickhouse-serving")

    def create_new_table(self, version: str):
        self.ch.execute(f"""
            CREATE TABLE IF NOT EXISTS user_hourly_metrics_v{version}
            (user_id String, hour DateTime,
             event_count UInt64, revenue_usd Float64, session_count UInt64,
             processed_at DateTime DEFAULT now())
            ENGINE = ReplacingMergeTree(processed_at)
            PARTITION BY toYYYYMM(hour)
            ORDER BY (user_id, hour)
        """)
        logger.info(f"Created table v{version}")

    def check_lag(self, group: str) -> int:
        """Parse kafka-consumer-groups output and return total lag."""
        result = subprocess.run(
            ["kafka-consumer-groups.sh", "--bootstrap-server", BROKERS,
             "--group", group, "--describe"],
            capture_output=True, text=True
        )
        total = 0
        for line in result.stdout.split("\\n"):
            parts = line.split()
            if len(parts) > 5 and parts[5].isdigit():
                total += int(parts[5])
        return total

    def wait_complete(self, group: str, poll_secs=60):
        while True:
            lag = self.check_lag(group)
            logger.info(f"Reprocessing lag: {lag:,} messages")
            if lag == 0:
                logger.info("Reprocessing complete!")
                return
            time.sleep(poll_secs)

    def atomic_swap(self, old_v: str, new_v: str):
        """Zero-downtime swap using ClickHouse EXCHANGE TABLES."""
        self.ch.execute(
            f"EXCHANGE TABLES user_hourly_metrics_v{old_v} "
            f"AND user_hourly_metrics_v{new_v}"
        )
        logger.info(f"Swapped v{old_v} → v{new_v}. All queries now hit reprocessed data.")

    def run(self, topic: str, old_v: str, new_v: str):
        logger.info("Starting Kappa historical reprocessing...")
        self.create_new_table(new_v)
        group = f"kappa-reprocess-v{new_v}"
        proc = subprocess.Popen(
            ["python", "kappa/stream_processor.py"],
            env={"REPROCESS_FROM_BEGINNING": "true",
                 "CONSUMER_GROUP": group, "OUTPUT_TABLE": f"user_hourly_metrics_v{new_v}"},
        )
        self.wait_complete(group)
        self.atomic_swap(old_v, new_v)
        proc.terminate()
        logger.info("Reprocessing done. Old table can be dropped.")

if __name__ == "__main__":
    KappaReprocessingManager().run("clickstream-events", old_v="1", new_v="2")
'''))

    EXAMPLES.append(("Kappa", "ML Features",
                     "K4 — Real-time ML Feature Pipeline (Kappa + Feature Store)",
                     "Computes ML features in real-time from Kafka and writes to Redis (online serving) and Kafka (offline training). Powers fraud detection and recommendation models.",
                     '''# kappa/ml_feature_pipeline.py
from confluent_kafka import Consumer, Producer
import redis, json, logging, numpy as np
from datetime import datetime, timezone
from collections import defaultdict, deque
from typing import Optional

logger = logging.getLogger(__name__)

class RealTimeFeatureComputer:
    """
    Kappa ML Feature Pipeline.
    Online store  → Redis (model inference)
    Offline store → Kafka topic (training data)
    """
    def __init__(self, brokers: str, feature_store_host: str):
        self.consumer = Consumer({
            "bootstrap.servers": brokers,
            "group.id": "kappa-ml-features-v3",
            "auto.offset.reset": "latest",
            "enable.auto.commit": True,
        })
        self.producer = Producer({"bootstrap.servers": brokers})
        self.fs = redis.Redis(host=feature_store_host, port=6379, decode_responses=True)
        self.event_times  = defaultdict(lambda: deque(maxlen=1000))
        self.revenues     = defaultdict(lambda: deque(maxlen=100))
        self.session_evts = defaultdict(int)
        self.last_seen    = {}
        self.devices      = defaultdict(set)

    def _rate(self, uid: str, window_s: int) -> int:
        from time import time
        cutoff = time() - window_s
        return sum(1 for t in self.event_times[uid] if t >= cutoff)

    def compute(self, event: dict) -> Optional[dict]:
        uid = event.get("user_id")
        if not uid: return None
        from time import time
        now = time()
        self.event_times[uid].append(now)
        self.revenues[uid].append(float(event.get("revenue_usd", 0)))
        self.session_evts[uid] += 1
        self.devices[uid].add(event.get("device_type", "unknown"))
        since_last = (now - self.last_seen[uid]) if uid in self.last_seen else -1
        self.last_seen[uid] = now
        revs = list(self.revenues[uid])
        return {
            "user_id": uid,
            "feature_ts": datetime.now(timezone.utc).isoformat(),
            "event_rate_1min": self._rate(uid, 60),
            "event_rate_5min": self._rate(uid, 300),
            "event_rate_1hr":  self._rate(uid, 3600),
            "revenue_last":    float(event.get("revenue_usd", 0)),
            "revenue_avg_5":   round(float(np.mean(revs[-5:])), 4) if revs else 0.0,
            "session_depth":   self.session_evts[uid],
            "time_since_last": round(since_last, 2),
            "device_diversity": len(self.devices[uid]),
            "is_rapid_fire":   1 if self._rate(uid, 10) > 10 else 0,
            "is_high_revenue": 1 if float(event.get("revenue_usd", 0)) > 500 else 0,
        }

    def write(self, features: dict):
        uid = features["user_id"]
        # Online: Redis, 24h TTL
        pipe = self.fs.pipeline()
        pipe.hset(f"features:user:{uid}:latest", mapping={k: str(v) for k, v in features.items()})
        pipe.expire(f"features:user:{uid}:latest", 86400)
        pipe.execute()
        # Offline: Kafka topic for training
        self.producer.produce("ml-features-offline", key=uid.encode(),
                              value=json.dumps(features).encode())
        self.producer.poll(0)

    def run(self):
        self.consumer.subscribe(["clickstream-events"])
        count = 0
        while True:
            msg = self.consumer.poll(1.0)
            if msg is None or msg.error(): continue
            f = self.compute(json.loads(msg.value().decode()))
            if f:
                self.write(f); count += 1
                if count % 10000 == 0:
                    logger.info(f"Computed {count:,} feature vectors")

if __name__ == "__main__":
    RealTimeFeatureComputer("kafka-1:9092,kafka-2:9092", "redis-features").run()
'''))

    EXAMPLES.append(("Kappa", "Stream Processing",
                     "K5 — PyFlink End-to-End with Event-Time Watermarks",
                     "Enterprise-grade PyFlink Kappa pipeline with event-time processing, watermarks for late-arriving events, and tumbling windows. Used at Uber/LinkedIn scale.",
                     '''# kappa/pyflink_pipeline.py
# pip install apache-flink
from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.datastream.connectors import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.datastream.window import TumblingEventTimeWindows
from pyflink.datastream.functions import ProcessWindowFunction, AggregateFunction
from pyflink.common import WatermarkStrategy, Duration
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.window import Time
import json, logging
from datetime import datetime

logger = logging.getLogger(__name__)

class EventTimeExtractor:
    def extract_timestamp(self, event: str, record_ts: int) -> int:
        try:
            ts_str = json.loads(event).get("event_timestamp", "")
            dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            return int(dt.timestamp() * 1000)
        except Exception:
            return record_ts

class UserMetricsAgg(AggregateFunction):
    def create_accumulator(self):
        return {"user_id": "", "events": 0, "revenue": 0.0, "sessions": set()}

    def add(self, value: str, acc: dict) -> dict:
        try:
            ev = json.loads(value)
            acc["user_id"] = ev.get("user_id", "")
            acc["events"] += 1
            acc["revenue"] += float(ev.get("revenue_usd", 0))
            acc["sessions"].add(ev.get("session_id", ""))
        except Exception:
            pass
        return acc

    def get_result(self, acc: dict) -> dict:
        return {**acc, "unique_sessions": len(acc["sessions"])}

    def merge(self, a, b):
        a["events"] += b["events"]; a["revenue"] += b["revenue"]
        a["sessions"].update(b["sessions"]); return a

class WindowProcess(ProcessWindowFunction):
    def process(self, key, ctx, elements, out):
        w = ctx.window()
        for el in elements:
            out.collect(json.dumps({
                **el,
                "window_start": datetime.utcfromtimestamp(w.start / 1000).isoformat(),
                "window_end":   datetime.utcfromtimestamp(w.end / 1000).isoformat(),
                "architecture": "kappa-pyflink",
            }))

def build_pipeline():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_stream_time_characteristic(TimeCharacteristic.EventTime)
    env.set_parallelism(8)
    env.enable_checkpointing(60000)  # Fault-tolerant checkpoints every 60s

    kafka_props = {"bootstrap.servers": "kafka-1:9092", "group.id": "kappa-flink-v1",
                   "auto.offset.reset": "latest"}  # Use "earliest" for reprocessing
    source = FlinkKafkaConsumer("clickstream-events", SimpleStringSchema(), kafka_props)
    sink   = FlinkKafkaProducer("user-window-metrics-flink", SimpleStringSchema(),
                                {"bootstrap.servers": "kafka-1:9092"})

    watermark_strategy = (WatermarkStrategy
        .for_bounded_out_of_orderness(Duration.of_seconds(10))  # Allow 10s late arrivals
        .with_timestamp_assigner(EventTimeExtractor()))

    (env
        .add_source(source)
        .assign_timestamps_and_watermarks(watermark_strategy)
        .filter(lambda m: bool(json.loads(m).get("user_id")))
        .key_by(lambda m: json.loads(m).get("user_id", "unknown"))
        .window(TumblingEventTimeWindows.of(Time.minutes(5)))  # 5-min event-time windows
        .aggregate(UserMetricsAgg(), WindowProcess())
        .add_sink(sink))

    logger.info("Submitting PyFlink Kappa pipeline...")
    env.execute("Kappa-UserMetrics-Flink")
    # Run: flink run -py kappa/pyflink_pipeline.py

if __name__ == "__main__":
    build_pipeline()
'''))

    EXAMPLES.append(("Kappa", "Reprocessing",
                     "K6 — Dead Letter Queue & Error Recovery in Kappa",
                     "Production error handling for Kappa pipelines — routes failed events to a DLQ, retries with exponential backoff, and tracks error rates in Prometheus.",
                     '''# kappa/error_handling.py
from confluent_kafka import Consumer, Producer
from prometheus_client import Counter, start_http_server
import json, logging, time, redis
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)

PROCESSED  = Counter("kappa_events_processed_total", "Processed events")
DLQ_EVENTS = Counter("kappa_dlq_events_total", "Dead-letter events", ["reason"])
RETRIES    = Counter("kappa_retries_total", "Retry attempts")

class KappaWithDLQ:
    """
    Kappa pipeline with Dead Letter Queue (DLQ) and retry logic.
    Failed events go to DLQ topic instead of crashing the pipeline.
    """
    MAX_RETRIES = 3
    RETRY_BACKOFF = [1, 5, 30]  # seconds

    def __init__(self, brokers: str, input_topic: str, dlq_topic: str):
        self.consumer = Consumer({
            "bootstrap.servers": brokers,
            "group.id": "kappa-with-dlq",
            "auto.offset.reset": "latest",
            "enable.auto.commit": False,
        })
        self.producer = Producer({"bootstrap.servers": brokers})
        self.dlq_topic = dlq_topic
        self.consumer.subscribe([input_topic])

    def _send_to_dlq(self, raw_msg: bytes, error: str, attempt: int):
        """Route failed events to DLQ with full context for debugging."""
        dlq_payload = json.dumps({
            "original_message": raw_msg.decode("utf-8", errors="replace"),
            "error": str(error),
            "attempt": attempt,
            "failed_at": datetime.now(timezone.utc).isoformat(),
        })
        self.producer.produce(self.dlq_topic, value=dlq_payload.encode())
        self.producer.poll(0)
        DLQ_EVENTS.labels(reason=type(error).__name__).inc()
        logger.warning(f"Sent to DLQ after {attempt} attempts: {error}")

    def process_with_retry(self, raw_msg: bytes) -> Optional[dict]:
        """Process with exponential backoff retry."""
        event = json.loads(raw_msg.decode("utf-8"))
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                # Your core Kappa processing logic here
                if not event.get("user_id"):
                    raise ValueError("Missing user_id")
                result = {
                    "user_id": event["user_id"],
                    "processed_at": datetime.now(timezone.utc).isoformat(),
                    "event_type": event.get("event_type"),
                }
                PROCESSED.inc()
                return result
            except (json.JSONDecodeError, KeyError) as e:
                # Non-retryable — go straight to DLQ
                self._send_to_dlq(raw_msg, e, attempt)
                return None
            except Exception as e:
                RETRIES.inc()
                if attempt < self.MAX_RETRIES:
                    wait = self.RETRY_BACKOFF[attempt - 1]
                    logger.warning(f"Attempt {attempt} failed, retrying in {wait}s: {e}")
                    time.sleep(wait)
                else:
                    self._send_to_dlq(raw_msg, e, attempt)
                    return None
        return None

    def run(self):
        logger.info("Kappa DLQ processor started")
        while True:
            msg = self.consumer.poll(1.0)
            if msg is None or msg.error():
                continue
            result = self.process_with_retry(msg.value())
            # Only commit offset after successful processing or DLQ routing
            self.consumer.commit(asynchronous=False)

if __name__ == "__main__":
    start_http_server(8000)  # Prometheus metrics
    KappaWithDLQ("kafka-1:9092", "clickstream-events", "clickstream-dlq").run()
'''))

    # ── Filtering logic ───────────────────────────────────────────────────────
    def show_arch(ex_arch):
        if arch_filter == "Both":
            return True
        return ex_arch in arch_filter

    def show_topic(ex_topic):
        if not topic_filter:
            return True
        return ex_topic in topic_filter

    def show_search(title, desc, code):
        if not search_term:
            return True
        q = search_term.lower()
        return q in title.lower() or q in desc.lower() or q in code.lower()

    filtered = [
        ex for ex in EXAMPLES
        if show_arch(ex[0]) and show_topic(ex[1]) and show_search(ex[2], ex[3], ex[4])
    ]

    # Count indicators
    lambda_count = sum(1 for e in filtered if e[0] == "Lambda")
    kappa_count = sum(1 for e in filtered if e[0] == "Kappa")

    ic1, ic2, ic3 = st.columns(3)
    ic1.metric("Showing", f"{len(filtered)} examples")
    ic2.metric("🟡 Lambda", lambda_count)
    ic3.metric("🔵 Kappa",  kappa_count)

    if not filtered:
        st.info(
            "No examples match your filters. Try adjusting the search or topic filter.")
    else:
        for arch, topic, title, desc, code in filtered:
            badge = "🟡" if arch == "Lambda" else "🔵"
            with st.expander(f"{badge} {title}"):
                st.caption(f"**Architecture:** {arch}  ·  **Topic:** {topic}")
                st.markdown(desc)
                st.code(code, language="python")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: CHEAT SHEET
# ══════════════════════════════════════════════════════════════════════════════
elif "📋 Cheat Sheet" in page:
    st.title("📋 Cheat Sheet")
    st.markdown(
        "##### Quick-reference for interviews, design reviews & daily engineering work")
    st.divider()

    st.subheader("⚡ Architecture at a Glance")
    st.dataframe(pd.DataFrame({
        "Property":              ["Coined by", "Core idea", "Layers", "Historical processing",
                                  "Real-time", "Code duplication", "Reprocessing trigger",
                                  "Accuracy", "Latency", "Team size"],
        "🟡 Lambda":             ["Nathan Marz (2011)", "Batch + Stream in parallel", "3",
                                 "Dedicated Spark/Hadoop job", "Speed layer (Flink/Storm)",
                                 "Yes — same logic twice", "Re-run batch + rebuild views",
                                 "Exact (batch)", "Seconds (speed) + hours (batch)", "Larger"],
        "🔵 Kappa":              ["Jay Kreps (2014)", "Everything is a stream", "2",
                                 "Replay Kafka from offset 0", "Same stream processor",
                                 "No — single codebase", "New consumer group + replay",
                                 "Exactly-once (Flink)", "Milliseconds–seconds", "Smaller"],
    }), use_container_width=True, hide_index=True)

    st.divider()
    cs1, cs2 = st.columns(2)
    with cs1:
        st.subheader("🟡 Lambda Stack")
        st.dataframe(pd.DataFrame({
            "Layer":    ["Ingest", "Batch Store", "Batch Engine", "Speed Engine", "Serving", "Orchestration"],
            "Tools":    ["Kafka/Kinesis", "HDFS/S3/GCS", "Spark/Hive/Hadoop", "Flink/Storm/Kafka Streams",
                         "Cassandra/Druid/Redis", "Airflow/Prefect"],
        }), use_container_width=True, hide_index=True)
    with cs2:
        st.subheader("🔵 Kappa Stack")
        st.dataframe(pd.DataFrame({
            "Component": ["Event Log", "Stream Engine", "State Store", "Serving", "Monitoring", "Orchestration"],
            "Tools":     ["Kafka/Redpanda/Pulsar", "Flink/Kafka Streams/Faust", "RocksDB",
                          "ClickHouse/Redis/Pinot", "Prometheus + Grafana", "Kubernetes Jobs"],
        }), use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("🎯 Interview Quick Answers")
    qa_data = {
        "Question": [
            "Why does Lambda have code duplication?",
            "How does Kappa reprocess historical data?",
            "When choose Lambda over Kappa?",
            "What is the serving layer's job?",
            "What makes Kafka central to Kappa?",
            "What is a watermark in Flink?",
            "What is exactly-once semantics?",
            "What is a Dead Letter Queue (DLQ)?",
        ],
        "Answer": [
            "Batch and speed layers implement the same logic independently — once in Spark, once in Flink. Keeping them in sync is the biggest operational pain.",
            "Create a new consumer group, reset offsets to 0, run the same processor — it replays all events into a new table, then atomically swap the serving layer.",
            "When you need 100% accurate historical recomputation at petabyte scale, or have regulatory/audit requirements, or teams are already split batch/streaming.",
            "Lambda: merge batch + speed views for low-latency reads. Kappa: serve stream-computed materialized views. Both provide fast random access.",
            "Kafka's durable replayable log IS the data store — you can re-read from any offset, enabling reprocessing without a separate data lake.",
            "A timestamp in the event stream telling Flink 'all events before X have arrived'. Enables correct event-time windowing with out-of-order events.",
            "Each event's effect is written exactly once — not lost or duplicated. Achieved via Flink distributed snapshots + transactional Kafka sinks.",
            "A queue for events that fail processing. Instead of crashing the pipeline, failed events are routed to a DLQ topic for inspection and retry.",
        ],
    }
    st.dataframe(pd.DataFrame(qa_data),
                 use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("⚠️ Common Pitfalls")
    p1, p2 = st.columns(2)
    with p1:
        st.warning(
            "**🟡 Lambda Pitfalls**\n"
            "- Logic drift between batch and speed layer\n"
            "- Forgetting to invalidate speed layer after batch\n"
            "- Not testing batch reprocessing on schema changes\n"
            "- Speed layer TTL shorter than batch window → data gaps\n"
            "- Serving layer not handling NULL from missing batch views"
        )
    with p2:
        st.warning(
            "**🔵 Kappa Pitfalls**\n"
            "- Kafka retention too short for reprocessing\n"
            "- Reusing same consumer group → wrong offsets on replay\n"
            "- State explosion — unbounded state causes OOM\n"
            "- Forgetting watermarks → windows never close\n"
            "- No atomic swap → downtime during reprocessing"
        )

    st.divider()
    st.subheader("📦 Python Library Quick Reference")
    st.dataframe(pd.DataFrame({
        "Library":           ["pyspark", "confluent-kafka", "faust-streaming", "apache-flink",
                              "kafka-python", "redis", "clickhouse-driver", "prometheus-client", "apache-airflow"],
        "Use Case":          ["Lambda batch layer", "Kafka producer/consumer", "Kafka Streams in Python",
                              "PyFlink stream processing", "Simpler Kafka client", "Speed layer / feature store",
                              "Kappa serving layer", "Pipeline monitoring", "Lambda batch orchestration"],
        "Install":           [f"pip install {p}" for p in [
                              "pyspark", "confluent-kafka", "faust-streaming", "apache-flink",
                              "kafka-python", "redis", "clickhouse-driver", "prometheus-client", "apache-airflow"]],
    }), use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: INTERACTIVE TOOLS
# ══════════════════════════════════════════════════════════════════════════════
elif "🎛️ Interactive Tools" in page:
    st.title("🎛️ Interactive Tools")
    st.markdown(
        "##### Explore architecture trade-offs with hands-on calculators")
    st.divider()

    tool = st.radio(
        "Select Tool",
        ["🏗️ Architecture Recommender", "💰 Cost Estimator", "📊 Latency Simulator",
         "🔁 Reprocessing Time Calculator"],
        horizontal=True,
    )
    st.divider()

    # ── Tool 1: Architecture Recommender ─────────────────────────────────────
    if "Recommender" in tool:
        st.subheader("🏗️ Architecture Recommender")
        st.markdown("Answer a few questions and get a recommendation.")

        t1, t2 = st.columns(2)
        with t1:
            accuracy = st.radio("Historical accuracy requirement?",
                                ["Best-effort (approximate OK)", "High (some tolerance)", "Exact (regulatory/audit)"])
            team_size = st.select_slider("Engineering team size", [
                                         "1–3", "4–10", "11–30", "30+"])
            latency = st.radio("Latency requirement?",
                               ["Sub-second real-time", "Seconds (near real-time)", "Minutes to hours OK"])
        with t2:
            data_vol = st.radio("Daily data volume?",
                                ["< 1 GB", "1 GB – 1 TB", "1 TB – 100 TB", "> 100 TB"])
            budget = st.radio("Infrastructure budget?",
                              ["Tight (minimize cost)", "Moderate", "Large (reliability first)"])
            reprocess = st.radio("Need historical reprocessing?",
                                 ["Rarely / Never", "Occasionally", "Frequently"])

        st.divider()

        # Scoring
        lambda_score, kappa_score = 0, 0

        if "Exact" in accuracy:
            lambda_score += 3
        elif "High" in accuracy:
            lambda_score += 1
            kappa_score += 1
        else:
            kappa_score += 2

        if team_size in ["30+"]:
            lambda_score += 2
        elif team_size in ["11–30"]:
            lambda_score += 1
            kappa_score += 1
        else:
            kappa_score += 2

        if "Sub-second" in latency:
            kappa_score += 2
        elif "Seconds" in latency:
            kappa_score += 1
            lambda_score += 1
        else:
            lambda_score += 1

        if "> 100 TB" in data_vol:
            lambda_score += 2
        elif "1 TB" in data_vol:
            lambda_score += 1
            kappa_score += 1
        else:
            kappa_score += 2

        if "Tight" in budget:
            kappa_score += 2
        elif "Large" in budget:
            lambda_score += 1

        if "Frequently" in reprocess:
            kappa_score += 2
        elif "Occasionally" in reprocess:
            kappa_score += 1
            lambda_score += 1
        else:
            lambda_score += 1

        total = lambda_score + kappa_score
        lp = int(lambda_score / total * 100)
        kp = 100 - lp

        rc1, rc2, rc3 = st.columns([1, 2, 1])
        with rc2:
            st.metric("🟡 Lambda Score", f"{lp}%")
            st.progress(lp / 100)
            st.metric("🔵 Kappa Score",  f"{kp}%")
            st.progress(kp / 100)

            if lp > 60:
                st.success(
                    "✅ **Recommendation: Lambda Architecture**\nYour requirements favour high accuracy, large team coordination, and large data volumes.")
            elif kp > 60:
                st.success(
                    "✅ **Recommendation: Kappa Architecture**\nYour requirements favour simplicity, lower latency, and unified codebase.")
            else:
                st.info("🤔 **Recommendation: Hybrid approach**\nYour requirements are balanced. Consider starting with Kappa and adding batch layers where needed.")

    # ── Tool 2: Cost Estimator ─────────────────────────────────────────────────
    elif "Cost" in tool:
        st.subheader("💰 Monthly Infrastructure Cost Estimator")
        st.caption("Rough estimates for AWS-based deployments")

        c1, c2 = st.columns(2)
        with c1:
            daily_events_m = st.slider("Daily events (millions)", 1, 1000, 50)
            avg_event_size_kb = st.slider("Avg event size (KB)", 1, 50, 2)
            kafka_retention_d = st.slider("Kafka retention (days)", 1, 30, 7)
            stream_workers = st.slider("Stream processing workers", 2, 50, 8)
        with c2:
            batch_cluster_hrs = st.slider(
                "Batch cluster hours/day (Lambda only)", 1, 12, 4)
            serving_reads_m = st.slider(
                "Serving layer reads/day (millions)", 1, 500, 100)
            replication = st.slider("Replication factor", 1, 5, 3)
            regions = st.slider("AWS regions", 1, 3, 1)

        daily_gb = (daily_events_m * 1_000_000 * avg_event_size_kb) / (1024**3)
        monthly_gb = daily_gb * 30

        # Kafka cost (MSK ~$0.01/GB-hour retained * replication)
        kafka_stored_gb = daily_gb * kafka_retention_d * replication
        kafka_cost = kafka_stored_gb * 0.01 * 24 * 30 / 30  # rough
        kafka_cost_month = kafka_cost * 30

        # Stream workers (~$0.05/hr per worker, r6g.xlarge equivalent)
        stream_cost = stream_workers * 0.05 * 24 * 30 * regions

        # Lambda: extra batch cluster
        batch_cost = batch_cluster_hrs * 10 * 30  # ~$10/hr for EMR cluster

        # Serving layer (ElastiCache + RDS, rough)
        serving_cost = 200 + (serving_reads_m * 0.01)

        # S3 storage for Lambda
        s3_cost_lambda = monthly_gb * replication * 0.023

        kappa_total = kafka_cost_month + stream_cost + serving_cost
        lambda_total = s3_cost_lambda + stream_cost + batch_cost + serving_cost

        st.divider()
        ec1, ec2 = st.columns(2)
        with ec1:
            st.markdown("#### 🟡 Lambda Monthly Estimate")
            st.metric("S3 Storage",       f"${s3_cost_lambda:,.0f}")
            st.metric("Stream (Flink)",    f"${stream_cost:,.0f}")
            st.metric("Batch (EMR)",       f"${batch_cost:,.0f}")
            st.metric("Serving (RDS+Cache)", f"${serving_cost:,.0f}")
            st.metric("**Total**",         f"${lambda_total:,.0f}")
        with ec2:
            st.markdown("#### 🔵 Kappa Monthly Estimate")
            st.metric("Kafka (MSK)",       f"${kafka_cost_month:,.0f}")
            st.metric("Stream (Flink)",    f"${stream_cost:,.0f}")
            st.metric("Serving (Cache)",   f"${serving_cost:,.0f}")
            st.metric("Batch (EMR)",       "—")
            st.metric("**Total**",         f"${kappa_total:,.0f}")

        diff = abs(lambda_total - kappa_total)
        cheaper = "Kappa" if kappa_total < lambda_total else "Lambda"
        st.info(f"💡 **{cheaper}** is ~${diff:,.0f}/month cheaper with these settings. "
                "Note: actual costs vary significantly by workload and reserved pricing.")
        st.caption(
            "Estimates are rough approximations. Always validate with AWS Pricing Calculator.")

    # ── Tool 3: Latency Simulator ─────────────────────────────────────────────
    elif "Latency" in tool:
        st.subheader("📊 Latency Profile Simulator")

        lc1, lc2 = st.columns(2)
        with lc1:
            st.markdown("**Lambda Settings**")
            batch_run_hrs = st.slider("Batch run interval (hours)", 1, 24, 8)
            batch_lag_mins = st.slider(
                "Batch job duration (minutes)", 10, 240, 60)
            speed_lag_s = st.slider(
                "Speed layer p99 latency (seconds)", 1, 60, 5)
        with lc2:
            st.markdown("**Kappa Settings**")
            kappa_lag_s = st.slider("Kappa p99 latency (seconds)", 1, 30, 3)
            kappa_replay_h = st.slider(
                "Kappa reprocessing time (hours, 1yr data)", 1, 48, 6)
            lambda_replay_h = st.slider(
                "Lambda batch reprocess time (hours, 1yr data)", 1, 48, 12)

        st.divider()

        # Build comparison table
        scenarios = {
            "Real-time query latency": (f"{speed_lag_s}s",         f"{kappa_lag_s}s"),
            "Fresh data max staleness": (f"Up to {batch_run_hrs}h", f"~{kappa_lag_s}s"),
            "Historical reprocessing":  (f"{lambda_replay_h}h",    f"{kappa_replay_h}h"),
            "Batch job completion":      (f"{batch_lag_mins} min",   "N/A"),
            "Post-batch data accuracy":  ("100% exact",             "Replay-complete"),
        }
        df_latency = pd.DataFrame(scenarios, index=["🟡 Lambda", "🔵 Kappa"]).T
        df_latency.index.name = "Scenario"
        st.dataframe(df_latency, use_container_width=True)

        st.caption(
            "Lambda excels at historical accuracy at the cost of data staleness. "
            "Kappa delivers lower real-time latency with faster reprocessing at smaller scale."
        )

    # ── Tool 4: Reprocessing Calculator ──────────────────────────────────────
    elif "Reprocessing" in tool:
        st.subheader("🔁 Reprocessing Time Calculator")
        st.markdown(
            "Estimate how long historical reprocessing takes for each architecture.")

        rc1, rc2 = st.columns(2)
        with rc1:
            history_months = st.slider(
                "Historical data to reprocess (months)", 1, 60, 12)
            events_per_day_m = st.slider(
                "Events per day (millions)", 1, 500, 100)
            event_size_bytes = st.slider(
                "Avg event size (bytes)", 100, 5000, 500)
        with rc2:
            spark_cores = st.slider(
                "Spark cores (Lambda batch)", 50, 1000, 200)
            kafka_partitions = st.slider(
                "Kafka partitions (Kappa replay)", 10, 500, 100)
            flink_parallelism = st.slider(
                "Flink parallelism (Kappa)", 8, 256, 32)

        # Rough calculations
        total_events_b = (events_per_day_m * 1_000_000 * history_months * 30)
        total_gb = (total_events_b * event_size_bytes) / (1024**3)

        # Lambda: Spark processes ~10GB/core/hour (rough)
        lambda_hours = total_gb / (spark_cores * 10)

        # Kappa: Kafka replay at ~50MB/partition/sec (limited by processing)
        kappa_throughput_gbh = (
            kafka_partitions * flink_parallelism * 0.05 * 3600) / 1024
        kappa_hours = total_gb / kappa_throughput_gbh

        st.divider()
        st.markdown(
            f"**Total data to reprocess: `{total_gb:,.1f} GB` ({total_events_b/1e9:.1f}B events)**")

        mc1, mc2, mc3 = st.columns(3)
        mc1.metric("🟡 Lambda Reprocess Time", f"{lambda_hours:.1f} hrs",
                   f"~{lambda_hours/24:.1f} days")
        mc2.metric("🔵 Kappa Reprocess Time",  f"{kappa_hours:.1f} hrs",
                   f"~{kappa_hours/24:.1f} days")
        mc3.metric("Speedup",
                   f"{(lambda_hours/kappa_hours):.1f}×" if kappa_hours < lambda_hours
                   else f"{(kappa_hours/lambda_hours):.1f}× slower")

        if kappa_hours < lambda_hours:
            st.success(
                f"🔵 Kappa is **{lambda_hours/kappa_hours:.1f}× faster** for reprocessing with these settings.")
        else:
            st.success(
                f"🟡 Lambda is **{kappa_hours/lambda_hours:.1f}× faster** for reprocessing with these settings.")

        st.warning(
            "⚠️ These are rough estimates. Real throughput depends on event complexity, "
            "transformation logic, state size, network I/O, and cluster configuration."
        )

    st.divider()
    st.caption(
        "⚡ Kappa vs Lambda Architecture Reference · Built for Data Engineers")

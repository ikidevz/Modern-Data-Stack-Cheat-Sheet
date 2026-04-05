import streamlit as st

from components import sidebar
from utility.seo import inject_seo

# ── PAGE CONFIG ──────────────────────────────────────────
st.set_page_config(
    page_title="Delta Lake Cheat Sheet",
    page_icon="🔺",
    layout="wide",
)

inject_seo('Databricks')

# ── CUSTOM CSS ───────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}



/* Header banner */
.delta-header {
    background: linear-gradient(135deg, #161b22 0%, #1c2330 100%);
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 24px 28px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 16px;
}
.delta-header h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #e6edf3;
    margin: 0;
}
.delta-header span { color: #e07b39; }
.delta-sub {
    font-size: 0.8rem;
    color: #8b949e;
    margin-top: 4px;
    font-family: 'JetBrains Mono', monospace;
}

/* Badges */
.badge-row { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 8px; }
.badge {
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.6px;
    font-family: 'JetBrains Mono', monospace;
    display: inline-block;
}
.badge-spark  { background:#e25d1818;color:#e25d18;border:1px solid #e25d1840; }
.badge-acid   { background:#3fb95018;color:#3fb950;border:1px solid #3fb95040; }
.badge-lake   { background:#58a6ff18;color:#58a6ff;border:1px solid #58a6ff40; }
.badge-dlt    { background:#bc8cff18;color:#bc8cff;border:1px solid #bc8cff40; }

/* Section header */
.section-head {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 8px 14px;
    border-radius: 6px 6px 0 0;
    margin-bottom: 0;
}
.head-bronze { background:#e07b3918;color:#e07b39;border:1px solid #e07b3930;border-bottom:none; }
.head-silver { background:#9db8d918;color:#9db8d9;border:1px solid #9db8d930;border-bottom:none; }
.head-gold   { background:#f0c04018;color:#f0c040;border:1px solid #f0c04030;border-bottom:none; }
.head-blue   { background:#58a6ff18;color:#58a6ff;border:1px solid #58a6ff30;border-bottom:none; }
.head-green  { background:#3fb95018;color:#3fb950;border:1px solid #3fb95030;border-bottom:none; }
.head-purple { background:#bc8cff18;color:#bc8cff;border:1px solid #bc8cff30;border-bottom:none; }
.head-teal   { background:#39c5bb18;color:#39c5bb;border:1px solid #39c5bb30;border-bottom:none; }
.head-red    { background:#f8514918;color:#f85149;border:1px solid #f8514930;border-bottom:none; }

/* Code card */
.code-card {
    background:#0d1117;
    border:1px solid #30363d;
    border-radius:0 0 8px 8px;
    overflow:hidden;
    margin-bottom:16px;
}
.code-label {
    background:#161b22;
    padding:6px 14px;
    font-size:0.65rem;
    color:#8b949e;
    font-family:'JetBrains Mono',monospace;
    border-bottom:1px solid #30363d;
    display:flex;align-items:center;gap:6px;
}
.code-label::before {
    content:'';width:6px;height:6px;border-radius:50%;background:#e07b39;flex-shrink:0;
}
.code-block {
    font-family:'JetBrains Mono',monospace;
    font-size:0.75rem;
    line-height:1.7;
    padding:14px 16px;
    overflow-x:auto;
    white-space:pre;
    color:#e6edf3;
}

/* Medallion diagram */
.medallion {
    display:flex;
    border:1px solid #30363d;
    border-radius:10px;
    overflow:hidden;
    margin-bottom:20px;
}
.medal-bronze { flex:1;background:linear-gradient(160deg,#3d1a08,#200e04);padding:20px;border-right:1px solid #30363d; }
.medal-silver { flex:1;background:linear-gradient(160deg,#1a2633,#0f1a26);padding:20px;border-right:1px solid #30363d; }
.medal-gold   { flex:1;background:linear-gradient(160deg,#2a2200,#1a1500);padding:20px; }

.medal-title { font-weight:800;font-size:1.1rem;margin-bottom:4px; }
.bronze-title { color:#cd7f32; }
.silver-title { color:#9db8d9; }
.gold-title   { color:#f0c040; }
.medal-sub    { font-size:0.68rem;color:#8b949e;margin-bottom:10px; }
.medal-desc   { font-size:0.72rem;color:#c9d1d9;margin-bottom:10px;line-height:1.5; }
.tag-row      { display:flex;flex-wrap:wrap;gap:4px; }
.tag {
    padding:2px 8px;border-radius:4px;
    font-size:0.62rem;font-family:'JetBrains Mono',monospace;font-weight:600;
}
.tag-bronze { background:#cd7f3218;color:#cd7f32;border:1px solid #cd7f3235; }
.tag-silver { background:#9db8d918;color:#9db8d9;border:1px solid #9db8d935; }
.tag-gold   { background:#f0c04018;color:#f0c040;border:1px solid #f0c04035; }

/* Info pills */
.pill-row { display:flex;gap:6px;flex-wrap:wrap;padding:8px 14px;background:#161b22;border-bottom:1px solid #21262d; }
.pill {
    padding:2px 9px;border-radius:20px;font-size:0.63rem;
    font-family:'JetBrains Mono',monospace;font-weight:600;
}
.pill-orange { background:#e07b3918;color:#e07b39;border:1px solid #e07b3935; }
.pill-blue   { background:#58a6ff18;color:#58a6ff;border:1px solid #58a6ff35; }
.pill-green  { background:#3fb95018;color:#3fb950;border:1px solid #3fb95035; }
.pill-purple { background:#bc8cff18;color:#bc8cff;border:1px solid #bc8cff35; }
.pill-teal   { background:#39c5bb18;color:#39c5bb;border:1px solid #39c5bb35; }

/* Syntax colors inside code blocks */
.kw  { color:#ff7b72; }
.fn  { color:#d2a8ff; }
.str { color:#a5d6ff; }
.num { color:#79c0ff; }
.cmt { color:#6e7681;font-style:italic; }
.var { color:#ffa657; }
.cls { color:#f0c040; }
.mth { color:#39c5bb; }

/* Section divider */
.sec-div {
    display:flex;align-items:center;gap:12px;
    margin:28px 0 18px 0;
    font-family:'Syne',sans-serif;font-weight:800;font-size:1.15rem;
}
.sec-div::after { content:'';flex:1;height:1px;background:#21262d; }

/* Tip box */
.tip-box {
    background:#161b22;border:1px solid #30363d;border-left:3px solid #e07b39;
    border-radius:6px;padding:12px 16px;margin:12px 0;
    font-size:0.78rem;line-height:1.6;
}
.tip-box strong { color:#e07b39; }

/* stCode override for streamlit code elements */
.stCodeBlock { border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)
sidebar()
# ════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🔺 Delta Lake")
    st.markdown("**Databricks + Apache Spark**")
    st.markdown("---")

    section = st.radio(
        "Navigate",
        [
            "🏅 Medallion Architecture",
            "⚡ Spark SQL Basics",
            "🐍 Python API",
            "🔀 MERGE Patterns",
            "⏱ Time Travel",
            "🌊 Streaming",
            "🚀 Performance",
            "🔧 Utility Methods",
            "🏗️ Architecture & Design",
            "🔄 Ingestion & ETL",
            "🧪 Data Quality & Governance",
            "⚙️ Jobs & Orchestration",
            "🧠 Advanced Delta Lake",
            "📊 Query Optimization",
            "🔐 Security & Access Control",
            "📦 Dev & MLOps",
            "🛠️ Monitoring & Observability",
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""
<div style='font-size:0.68rem;color:#8b949e;font-family:JetBrains Mono,monospace;line-height:1.8;'>
🔺 Delta Lake 3.x<br>
⚡ Apache Spark 3.5<br>
☁️ Databricks Runtime 14+<br>
🐍 Python 3.10+
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    search = st.text_input("🔍 Search snippets",
                           placeholder="e.g. merge, vacuum...")

# ════════════════════════════════════════════════════════
# HEADER
# ════════════════════════════════════════════════════════
st.title("🔺 Delta Lake Cheat Sheet")
st.caption("Databricks · Apache Spark · Medallion Architecture · DLT · Streaming")

# ════════════════════════════════════════════════════════
# SNIPPET DATA (for search)
# ════════════════════════════════════════════════════════
ALL_SNIPPETS = {
    "Bronze Auto Loader": {
        "tags": ["bronze", "autoloader", "cloudfiles", "streaming", "ingest"],
        "lang": "python",
        "code": '''\
from pyspark.sql.functions import current_timestamp, input_file_name

bronze_df = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "/mnt/schema/bronze")
    .option("cloudFiles.inferColumnTypes", "true")
    .load("/mnt/landing/events/")
    .withColumn("_ingest_time", current_timestamp())
    .withColumn("_source_file", input_file_name())
)

(
    bronze_df.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/mnt/checkpoints/bronze")
    .trigger(processingTime="10 minutes")
    .toTable("bronze.raw_events")
)'''
    },
    "Silver MERGE Upsert": {
        "tags": ["silver", "merge", "upsert", "deduplicate", "cleanse"],
        "lang": "python",
        "code": '''\
from delta.tables import DeltaTable
from pyspark.sql.functions import col, row_number, to_timestamp
from pyspark.sql.window import Window

bronze_df = spark.table("bronze.raw_events")

w = Window.partitionBy("event_id").orderBy(col("_ingest_time").desc())
clean_df = (
    bronze_df
    .withColumn("rn", row_number().over(w))
    .filter(col("rn") == 1).drop("rn")
    .filter(col("event_id").isNotNull())
    .withColumn("event_ts", to_timestamp(col("event_time")))
)

silver_table = DeltaTable.forName(spark, "silver.events")
(
    silver_table.alias("target")
    .merge(clean_df.alias("source"), "target.event_id = source.event_id")
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)'''
    },
    "Gold Aggregation": {
        "tags": ["gold", "aggregate", "kpi", "groupby", "revenue"],
        "lang": "python",
        "code": '''\
from pyspark.sql.functions import count, sum, avg, date_trunc

silver_df = spark.table("silver.events")

gold_df = (
    silver_df
    .filter(col("event_type") == "purchase")
    .withColumn("event_date", date_trunc("day", col("event_ts")))
    .groupBy("event_date", "product_id", "region")
    .agg(
        count("*").alias("total_orders"),
        sum("amount").alias("total_revenue"),
        avg("amount").alias("avg_order_value")
    )
)

(
    gold_df.write.format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .partitionBy("event_date")
    .saveAsTable("gold.daily_revenue")
)'''
    },
    "MERGE Upsert": {
        "tags": ["merge", "upsert", "update", "insert"],
        "lang": "python",
        "code": '''\
from delta.tables import DeltaTable

dt = DeltaTable.forName(spark, "target_table")

# Full upsert
(
    dt.alias("t")
    .merge(updates.alias("s"), "t.id = s.id")
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)

# Conditional update only
(
    dt.alias("t")
    .merge(updates.alias("s"), "t.id = s.id")
    .whenMatchedUpdate(
        condition="s.version > t.version",
        set={"name": "s.name", "version": "s.version"}
    )
    .whenNotMatchedInsertAll()
    .execute()
)

# Delete matched rows
(
    dt.alias("t")
    .merge(to_delete.alias("s"), "t.id = s.id")
    .whenMatchedDelete()
    .execute()
)'''
    },
    "OPTIMIZE Z-ORDER": {
        "tags": ["optimize", "zorder", "compact", "performance", "z-order"],
        "lang": "sql",
        "code": '''\
-- Compact small files
OPTIMIZE tableName;

-- Z-ORDER by columns used in filters
OPTIMIZE tableName ZORDER BY (colA, colB);

-- Optimize specific partition
OPTIMIZE tableName
WHERE date = '2024-01-01'
ZORDER BY (user_id);

-- Liquid Clustering (Delta 3.1+, replaces Z-Order)
ALTER TABLE tableName CLUSTER BY (event_date, user_id);
OPTIMIZE tableName;  -- incremental clustering'''
    },
    "VACUUM": {
        "tags": ["vacuum", "cleanup", "retention", "files"],
        "lang": "sql",
        "code": '''\
-- Delete unreferenced files older than 7 days (default)
VACUUM tableName;

-- Custom retention window
VACUUM tableName RETAIN 168 HOURS;

-- Dry run (preview only)
VACUUM tableName RETAIN 0 HOURS DRY RUN;

-- Python API
dt.vacuum()       # 7d default
dt.vacuum(100)    # 100h retention'''
    },
    "Time Travel SQL": {
        "tags": ["time travel", "version", "history", "restore", "rollback"],
        "lang": "sql",
        "code": '''\
-- View transaction log
DESCRIBE HISTORY tableName;

-- Query by version
SELECT * FROM tableName VERSION AS OF 5;

-- Query by timestamp
SELECT * FROM tableName TIMESTAMP AS OF '2024-01-15 12:00:00';

-- Shorthand version
SELECT * FROM tableName@v0;

-- Diff between versions
SELECT * FROM tableName VERSION AS OF 12
EXCEPT ALL
SELECT * FROM tableName VERSION AS OF 11;

-- Rollback
RESTORE TABLE tableName VERSION AS OF 3;
RESTORE TABLE tableName TIMESTAMP AS OF '2024-01-10';'''
    },
    "SCD Type 2": {
        "tags": ["scd", "slowly changing dimension", "history", "current_flag"],
        "lang": "python",
        "code": '''\
from delta.tables import DeltaTable
from pyspark.sql.functions import lit, current_timestamp, col

dim_table = DeltaTable.forName(spark, "silver.dim_customer")
updates   = spark.table("stage.customer_updates")

updates_with_key = updates.withColumn("merge_key", col("customer_id"))

# Expire changed rows + insert new ones
staged = updates_with_key.union(
    updates_with_key
    .join(dim_table.toDF(), "customer_id")
    .where("current_flag = true AND updates.email != dim_customer.email")
    .select(updates_with_key["*"])
    .withColumn("merge_key", lit(None))
)

(
    dim_table.alias("target")
    .merge(staged.alias("s"), "target.customer_id = s.merge_key")
    .whenMatchedUpdate(
        condition="target.current_flag = true AND target.email != s.email",
        set={"current_flag": lit(False), "end_date": current_timestamp()}
    )
    .whenNotMatchedInsert(values={
        "customer_id":  col("s.customer_id"),
        "email":        col("s.email"),
        "current_flag": lit(True),
        "start_date":   current_timestamp(),
        "end_date":     lit(None)
    })
    .execute()
)'''
    },
}

# ════════════════════════════════════════════════════════
# HELPER: render a code card
# ════════════════════════════════════════════════════════


def code_card(header_class, title, filename, lang, code, pills=None):
    st.markdown(
        f'<div class="section-head {header_class}">{title}</div>', unsafe_allow_html=True)
    html = '<div class="code-card">'
    if pills:
        html += '<div class="pill-row">' + "".join(
            f'<span class="pill pill-{c}">{t}</span>' for t, c in pills
        ) + "</div>"
    html += f'<div class="code-label">{filename}</div></div>'
    st.markdown(html, unsafe_allow_html=True)
    st.code(code, language=lang)


# ════════════════════════════════════════════════════════
# SEARCH MODE
# ════════════════════════════════════════════════════════
if search and search.strip():
    q = search.lower()
    st.markdown(
        f'<div class="sec-div">🔍 Search results for "{search}"</div>', unsafe_allow_html=True)
    found = 0
    for name, data in ALL_SNIPPETS.items():
        if q in name.lower() or any(q in t for t in data["tags"]):
            st.markdown(
                f'<div class="section-head head-blue">📄 {name}</div>', unsafe_allow_html=True)
            st.markdown('<div class="code-card"><div class="code-label">' +
                        name + '</div></div>', unsafe_allow_html=True)
            st.code(data["code"], language=data["lang"])
            found += 1
    if found == 0:
        st.info(
            f"No snippets matched **{search}**. Try: merge, vacuum, optimize, bronze, silver, gold, streaming…")

# ════════════════════════════════════════════════════════
# 🏅 MEDALLION ARCHITECTURE
# ════════════════════════════════════════════════════════
elif section == "🏅 Medallion Architecture":

    st.markdown("""
<div class="medallion">
  <div class="medal-bronze">
    <div class="medal-title bronze-title">🥉 Bronze</div>
    <div class="medal-sub">Raw Ingestion Layer</div>
    <div class="medal-desc">Append-only. Schema-on-read. Preserves full source fidelity. No transformations.</div>
    <div class="tag-row">
      <span class="tag tag-bronze">Raw Data</span>
      <span class="tag tag-bronze">Append Only</span>
      <span class="tag tag-bronze">Auto Loader</span>
      <span class="tag tag-bronze">Kafka</span>
      <span class="tag tag-bronze">Landing Zone</span>
    </div>
  </div>
  <div class="medal-silver">
    <div class="medal-title silver-title">🥈 Silver</div>
    <div class="medal-sub">Cleansed &amp; Conformed</div>
    <div class="medal-desc">Deduplication, validation, type casting, joins. Queryable and business-friendly.</div>
    <div class="tag-row">
      <span class="tag tag-silver">Dedup</span>
      <span class="tag tag-silver">Validated</span>
      <span class="tag tag-silver">Merged</span>
      <span class="tag tag-silver">DQ Checks</span>
      <span class="tag tag-silver">SCD Type 2</span>
    </div>
  </div>
  <div class="medal-gold">
    <div class="medal-title gold-title">🥇 Gold</div>
    <div class="medal-sub">Business Aggregations</div>
    <div class="medal-desc">Aggregated, denormalized, BI-ready. Serves dashboards, ML models, and reports.</div>
    <div class="tag-row">
      <span class="tag tag-gold">KPIs</span>
      <span class="tag tag-gold">Aggregated</span>
      <span class="tag tag-gold">ML Features</span>
      <span class="tag tag-gold">Reporting</span>
      <span class="tag tag-gold">Star Schema</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        code_card("head-bronze", "🥉 Bronze — Auto Loader Ingestion", "bronze_ingestion.py", "python",
                  '''\
from pyspark.sql.functions import current_timestamp, input_file_name

bronze_df = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "/mnt/schema/bronze")
    .option("cloudFiles.inferColumnTypes", "true")
    .load("/mnt/landing/events/")
    .withColumn("_ingest_time", current_timestamp())
    .withColumn("_source_file", input_file_name())
)

(
    bronze_df.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/mnt/checkpoints/bronze")
    .trigger(processingTime="10 minutes")
    .toTable("bronze.raw_events")
)''',
                  pills=[("cloudFiles", "orange"), ("Append Only", "orange"), ("Schema Inference", "orange")])

        code_card("head-gold", "🥇 Gold — KPI Aggregations", "gold_aggregation.py", "python",
                  '''\
from pyspark.sql.functions import count, sum, avg, date_trunc, col

silver_df = spark.table("silver.events")

gold_df = (
    silver_df
    .filter(col("event_type") == "purchase")
    .withColumn("event_date", date_trunc("day", col("event_ts")))
    .groupBy("event_date", "product_id", "region")
    .agg(
        count("*").alias("total_orders"),
        sum("amount").alias("total_revenue"),
        avg("amount").alias("avg_order_value")
    )
)

(
    gold_df.write.format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .partitionBy("event_date")
    .saveAsTable("gold.daily_revenue")
)''',
                  pills=[("Aggregated", "purple"), ("BI Ready", "purple"), ("Partitioned", "purple")])

    with col2:
        code_card("head-silver", "🥈 Silver — Cleanse, Dedup & MERGE", "silver_transform.py", "python",
                  '''\
from delta.tables import DeltaTable
from pyspark.sql.functions import col, row_number, to_timestamp
from pyspark.sql.window import Window

bronze_df = spark.table("bronze.raw_events")

# Deduplicate: keep latest per event_id
w = Window.partitionBy("event_id").orderBy(col("_ingest_time").desc())
clean_df = (
    bronze_df
    .withColumn("rn", row_number().over(w))
    .filter(col("rn") == 1).drop("rn")
    .filter(col("event_id").isNotNull())
    .withColumn("event_ts", to_timestamp(col("event_time")))
)

# MERGE into Silver
silver_table = DeltaTable.forName(spark, "silver.events")
(
    silver_table.alias("target")
    .merge(clean_df.alias("source"),
           "target.event_id = source.event_id")
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)''',
                  pills=[("MERGE INTO", "blue"), ("Dedup", "blue"), ("Data Quality", "blue")])

        code_card("head-teal", "⚡ Delta Live Tables (DLT) Pipeline", "dlt_pipeline.py", "python",
                  '''\
import dlt
from pyspark.sql.functions import col, current_timestamp

# ── Bronze Layer ──
@dlt.table(comment="Raw events from landing zone")
def bronze_events():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load("/mnt/landing/events")
        .withColumn("_loaded_at", current_timestamp())
    )

# ── Silver with Expectations (data quality rules) ──
@dlt.expect_or_drop("valid_event_id", "event_id IS NOT NULL")
@dlt.expect("positive_amount",  "amount > 0")
@dlt.table(comment="Cleansed validated events")
def silver_events():
    return dlt.read_stream("bronze_events").select(
        col("event_id").cast("string"),
        col("amount").cast("double"),
        col("event_time").cast("timestamp"),
        col("product_id"),
    )

# ── Gold Layer ──
@dlt.table(comment="Daily revenue rollup")
def gold_daily_revenue():
    from pyspark.sql.functions import sum, count, date_trunc
    return (
        dlt.read("silver_events")
        .withColumn("date", date_trunc("day", "event_time"))
        .groupBy("date", "product_id")
        .agg(sum("amount").alias("revenue"),
             count("*").alias("orders"))
    )''',
                  pills=[("@dlt.table", "green"), ("Expectations", "green"), ("Auto Lineage", "green")])

    st.markdown('<div class="sec-div">📐 SCD Type 2 Pattern</div>',
                unsafe_allow_html=True)
    code_card("head-purple", "📋 Slowly Changing Dimensions Type 2", "scd_type2.py", "python",
              '''\
from delta.tables import DeltaTable
from pyspark.sql.functions import lit, current_timestamp, col

dim_table = DeltaTable.forName(spark, "silver.dim_customer")
updates   = spark.table("stage.customer_updates")
           .withColumn("merge_key", col("customer_id"))

# Stage: keep both changed rows to expire + new versions
staged_updates = updates.union(
    updates
    .join(dim_table.toDF(), "customer_id")
    .where("current_flag = true AND updates.email != dim_customer.email")
    .select(updates["*"])
    .withColumn("merge_key", lit(None))  # force insert path
)

(
    dim_table.alias("target")
    .merge(staged_updates.alias("s"), "target.customer_id = s.merge_key")
    .whenMatchedUpdate(
        condition="target.current_flag = true AND target.email != s.email",
        set={
            "current_flag": lit(False),
            "end_date":     current_timestamp()
        }
    )
    .whenNotMatchedInsert(values={
        "customer_id":  col("s.customer_id"),
        "email":        col("s.email"),
        "current_flag": lit(True),
        "start_date":   current_timestamp(),
        "end_date":     lit(None)
    })
    .execute()
)''',
              pills=[("History Tracking", "purple"), ("MERGE Pattern", "purple"), ("current_flag", "purple")])

# ════════════════════════════════════════════════════════
# ⚡ SPARK SQL BASICS
# ════════════════════════════════════════════════════════
elif section == "⚡ Spark SQL Basics":

    col1, col2 = st.columns(2)
    with col1:
        code_card("head-bronze", "Create Database & Tables", "create.sql", "sql",
                  '''\
-- Managed database (saved in Hive metastore)
CREATE DATABASE IF NOT EXISTS dbName;
USE dbName;

-- Create Delta table with explicit DDL
CREATE TABLE IF NOT EXISTS tableName (
    id   INT NOT NULL,
    name STRING,
    dt   DATE,
    amt  FLOAT
)
USING DELTA
PARTITIONED BY (dt);

-- Create as SELECT
CREATE TABLE silver.users
USING DELTA
AS SELECT * FROM bronze.raw_users
WHERE user_id IS NOT NULL;

-- Query by name
SELECT * FROM [dbName.] tableName;

-- Query by path (backticks required)
SELECT * FROM delta.`/path/to/delta_table`;''')

        code_card("head-blue", "Insert / Update / Delete", "dml.sql", "sql",
                  '''\
-- Insert VALUES
INSERT INTO tableName VALUES
  (1, 'Alice', '2024-01-01', 99.9),
  (2, 'Bob',   '2024-01-02', 49.5);

-- Insert from SELECT
INSERT INTO tableName SELECT * FROM sourceTable;

-- Atomic overwrite
INSERT OVERWRITE tableName
SELECT * FROM sourceTable;

-- Update rows
UPDATE tableName
SET event = 'click'
WHERE event = 'clk';

-- Delete rows
DELETE FROM tableName
WHERE dt < '2023-01-01';

-- Upsert with MERGE
MERGE INTO target USING updates
ON target.id = updates.id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;''')

    with col2:
        code_card("head-green", "Convert Parquet → Delta", "convert.sql", "sql",
                  '''\
-- By table name
CONVERT TO DELTA [dbName.]tableName
[PARTITIONED BY (col1 type1, col2 type2)];

-- By path
CONVERT TO DELTA
  parquet.`/path/to/table`
[PARTITIONED BY (year INT, month INT)];

-- Verify it's a Delta table
DESCRIBE DETAIL tableName;
DESCRIBE FORMATTED tableName;''')

        code_card("head-teal", "Alter Table: Columns & Constraints", "alter.sql", "sql",
                  '''\
-- Add column
ALTER TABLE tableName
ADD COLUMNS (
    new_col STRING [FIRST|AFTER existing_col]
);

-- NOT NULL constraint
ALTER TABLE tableName
CHANGE COLUMN col_name col_name TYPE NOT NULL;

-- CHECK constraint
ALTER TABLE tableName
ADD CONSTRAINT validDate
  CHECK (dt > '1900-01-01');

-- Drop constraint
ALTER TABLE tableName
DROP CONSTRAINT validDate;

-- Rename column
ALTER TABLE tableName
RENAME COLUMN old_name TO new_name;''')

        code_card("head-purple", "COPY INTO (Idempotent)", "copy_into.sql", "sql",
                  '''\
-- COPY INTO tracks loaded files → idempotent
COPY INTO silver.events
FROM '/mnt/landing/events/'
FILEFORMAT = PARQUET
COPY_OPTIONS ('mergeSchema' = 'true');

-- CSV with transformation
COPY INTO gold.products
FROM (
  SELECT
    CAST(_c0 AS INT)    AS product_id,
    _c1                 AS name,
    CAST(_c2 AS DOUBLE) AS price
  FROM '/mnt/raw/products/'
)
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'false')
COPY_OPTIONS  ('force' = 'false');''')

# ════════════════════════════════════════════════════════
# 🐍 PYTHON API
# ════════════════════════════════════════════════════════
elif section == "🐍 Python API":

    col1, col2 = st.columns(2)
    with col1:
        code_card("head-bronze", "Read & Write DataFrames", "read_write.py", "python",
                  '''\
# Read from path
df = spark.read.format("delta").load("/path/to/table")

# Read from table name
df = spark.table("silver.events")

# Write: append
(
    df.write.format("delta")
    .mode("append")
    .partitionBy("date")
    .option("mergeSchema", "true")
    .save("/path/to/delta_table")
)

# Write: overwrite
(
    df.write.format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("silver.events")
)

# From pandas DataFrame
import pandas as pd
pdf = pd.read_csv("data.csv")
sdf = spark.createDataFrame(pdf)
sdf.write.format("delta").save("/mnt/delta/my_table")''')

        code_card("head-purple", "Schema Evolution", "schema_evolution.py", "python",
                  '''\
# Default: schema enforcement (raises error on mismatch)
df.write.format("delta").mode("append").save(path)

# Auto-merge schema (add new columns on write)
(
    df.write.format("delta")
    .mode("append")
    .option("mergeSchema", "true")
    .save(path)
)

# Enable globally via Spark config
spark.conf.set(
    "spark.databricks.delta.schema.autoMerge.enabled",
    "true"
)

# Overwrite schema completely
(
    df.write.format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .save(path)
)

# Inspect current schema
dt = DeltaTable.forName(spark, "silver.events")
dt.toDF().printSchema()''')

    with col2:
        code_card("head-blue", "DeltaTable API", "delta_table_api.py", "python",
                  '''\
from delta.tables import DeltaTable

# Reference by name or path
dt = DeltaTable.forName(spark, "silver.events")
dt = DeltaTable.forPath(spark, "/path/to/table")

# Check if path is a Delta table
DeltaTable.isDeltaTable(spark, "/path/to/table")

# Update rows
from pyspark.sql.functions import lit
dt.update(
    condition="eventType = 'clk'",
    set={"eventType": lit("click")}
)

# Delete rows
dt.delete("date < '2023-01-01'")

# View as DataFrame
df = dt.toDF()

# Get table history
dt.history().show(10, truncate=False)

# Clone table
dt.clone(
    target="/path/to/clone",
    isShallow=True,
    replace=True
)''')

        code_card("head-green", "Interop: SQL ↔ Python", "interop.py", "python",
                  '''\
# Run SQL from Python
spark.sql("SELECT * FROM silver.events").show()
spark.sql("""
    SELECT product_id, SUM(amount) AS revenue
    FROM silver.events
    WHERE event_type = 'purchase'
    GROUP BY product_id
    ORDER BY revenue DESC
""").display()

# Read Hive metastore table into DataFrame
df = spark.table("silver.events")

# Read path-based Delta into DataFrame
df = (
    spark.read.format("delta")
    .load("/path/to/delta_table")
)

# Register temp view for SQL
df.createOrReplaceTempView("events_view")
spark.sql("SELECT * FROM events_view LIMIT 10")

# Convert DataFrame to pandas
pdf = df.limit(1000).toPandas()''')

# ════════════════════════════════════════════════════════
# 🔀 MERGE PATTERNS
# ════════════════════════════════════════════════════════
elif section == "🔀 MERGE Patterns":

    col1, col2 = st.columns(2)
    with col1:
        code_card("head-bronze", "Pattern 1: Full Upsert", "merge_upsert.py", "python",
                  '''\
from delta.tables import DeltaTable

dt = DeltaTable.forName(spark, "silver.events")

(
    dt.alias("t")
    .merge(updates.alias("s"), "t.id = s.id")
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)''',
                  pills=[("Update + Insert", "blue")])

        code_card("head-blue", "Pattern 3: Insert-Only (Dedup)", "merge_dedup.py", "python",
                  '''\
from delta.tables import DeltaTable

logs = DeltaTable.forName(spark, "silver.logs")
new_logs = spark.table("stage.new_logs")

# Only insert rows that don\'t already exist
(
    logs.alias("t")
    .merge(new_logs.alias("s"),
           "t.uniqueId = s.uniqueId")
    .whenNotMatchedInsertAll()
    .execute()
)

# SQL equivalent
spark.sql("""
    MERGE INTO silver.logs AS t
    USING stage.new_logs AS s
    ON t.uniqueId = s.uniqueId
    WHEN NOT MATCHED THEN INSERT *
""")''',
                  pills=[("Dedup", "green"), ("Insert Only", "green")])

        code_card("head-red", "Pattern 4: Delete Matched", "merge_delete.py", "python",
                  '''\
# Soft-delete: mark rows as deleted
(
    dt.alias("t")
    .merge(to_delete.alias("s"), "t.id = s.id")
    .whenMatchedUpdate(set={"is_deleted": lit(True)})
    .execute()
)

# Hard-delete matched rows entirely
(
    dt.alias("t")
    .merge(to_delete.alias("s"), "t.id = s.id")
    .whenMatchedDelete()
    .execute()
)

# GDPR-compliant bulk delete by SQL
spark.sql("""
    DELETE FROM silver.events
    WHERE user_id IN (
        SELECT user_id FROM gdpr.deletion_requests
    )
""")''',
                  pills=[("GDPR Delete", "orange"), ("Hard Delete", "orange")])

    with col2:
        code_card("head-silver", "Pattern 2: Conditional Update", "merge_conditional.py", "python",
                  '''\
from delta.tables import DeltaTable

dt = DeltaTable.forName(spark, "silver.products")

(
    dt.alias("t")
    .merge(updates.alias("s"), "t.product_id = s.product_id")
    # Update only if source version is newer
    .whenMatchedUpdate(
        condition="s.version > t.version",
        set={
            "name":       "s.name",
            "price":      "s.price",
            "version":    "s.version",
            "updated_at": "s.updated_at"
        }
    )
    # Insert brand new products
    .whenNotMatchedInsertAll()
    # Delete discontinued products
    .whenMatchedDelete(
        condition="s.status = 'discontinued'"
    )
    .execute()
)''',
                  pills=[("Conditional", "blue"), ("Multi-clause", "blue")])

        code_card("head-gold", "Pattern 5: foreachBatch Streaming Upsert", "foreach_batch.py", "python",
                  '''\
from delta.tables import DeltaTable

def upsert_to_delta(batch_df, batch_id):
    path = "/mnt/silver/events"

    # Create table on first run
    if not DeltaTable.isDeltaTable(spark, path):
        batch_df.write.format("delta").save(path)
        return

    dt = DeltaTable.forPath(spark, path)
    (
        dt.alias("t")
        .merge(batch_df.alias("s"),
               "t.event_id = s.event_id")
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute()
    )

# Attach pattern to streaming query
(
    stream_df.writeStream
    .format("delta")
    .foreachBatch(upsert_to_delta)
    .option("checkpointLocation", "/mnt/chkpt/upsert")
    .trigger(processingTime="1 minute")
    .start()
)''',
                  pills=[("Streaming", "teal"), ("Micro-batch Upsert", "teal")])

# ════════════════════════════════════════════════════════
# ⏱ TIME TRAVEL
# ════════════════════════════════════════════════════════
elif section == "⏱ Time Travel":

    col1, col2 = st.columns(2)
    with col1:
        code_card("head-bronze", "Time Travel — Spark SQL", "time_travel.sql", "sql",
                  '''\
-- View full transaction log
DESCRIBE HISTORY tableName;

-- Query specific version
SELECT * FROM tableName VERSION AS OF 5;

-- Query at timestamp
SELECT * FROM tableName
TIMESTAMP AS OF '2024-01-15 12:00:00';

-- Shorthand syntax
SELECT * FROM tableName@v0;

-- Diff: what changed between versions?
SELECT * FROM tableName VERSION AS OF 12
EXCEPT ALL
SELECT * FROM tableName VERSION AS OF 11;

-- Rollback to version
RESTORE TABLE tableName VERSION AS OF 3;

-- Rollback to timestamp (requires Delta 0.7+)
RESTORE TABLE tableName
TIMESTAMP AS OF '2024-01-10';''')

    with col2:
        code_card("head-blue", "Time Travel — Python API", "time_travel.py", "python",
                  '''\
from delta.tables import DeltaTable

# Read at specific version
df_v5 = (
    spark.read.format("delta")
    .option("versionAsOf", 5)
    .load("/path/to/delta_table")
)

# Read at specific timestamp
df_ts = (
    spark.read.format("delta")
    .option("timestampAsOf", "2024-01-15")
    .load("/path/to/delta_table")
)

# Get full history DataFrame
dt = DeltaTable.forPath(spark, "/path/to/table")
history_df = dt.history()
history_df.select("version","timestamp","operation").show()

# Rollback
dt.restoreToVersion(2)
dt.restoreToTimestamp("2024-01-15 12:00:00")

# Find rows added in latest version
df_new = spark.read.format("delta").option("versionAsOf", 3).load(path)
df_old = spark.read.format("delta").option("versionAsOf", 2).load(path)
df_new.exceptAll(df_old).show()''')

    st.markdown("""
<div class="tip-box">
<strong>💡 Tip:</strong> Time travel reads previous versions from the Delta transaction log (JSON files in <code>_delta_log/</code>).
Data files are retained until <code>VACUUM</code> removes them — so always set <code>logRetentionDuration</code> to match your recovery window.
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# 🌊 STREAMING
# ════════════════════════════════════════════════════════
elif section == "🌊 Streaming":

    col1, col2 = st.columns(2)
    with col1:
        code_card("head-teal", "Read Delta as Stream Source", "stream_read.py", "python",
                  '''\
stream_df = (
    spark.readStream
    .format("delta")
    .option("ignoreDeletes",      "true")
    .option("maxFilesPerTrigger", 100)    # throttle
    .table("bronze.events")
    # or .load("/mnt/bronze/events")
)

# Windowed aggregation with late-data watermark
from pyspark.sql.functions import window, count, col

result = (
    stream_df
    .withWatermark("event_time", "10 minutes")
    .groupBy(
        window(col("event_time"), "5 minutes"),
        "user_id"
    )
    .agg(count("*").alias("event_count"))
)

# Write to Delta sink
(
    result.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/mnt/chkpt/events")
    .trigger(processingTime="30 seconds")
    .toTable("silver.event_counts")
)''')

        code_card("head-purple", "Trigger Modes", "triggers.py", "python",
                  '''\
from pyspark.sql.functions import expr

# ── Fixed interval ──
q = (df.writeStream
     .trigger(processingTime="1 minute")
     .start())

# ── Once: process all available, then stop ──
q = (df.writeStream
     .trigger(once=True)
     .start())

# ── AvailableNow: like once, but multi-batch ──
q = (df.writeStream
     .trigger(availableNow=True)
     .start())

# ── Continuous (low-latency, ~1ms) ──
q = (df.writeStream
     .trigger(continuous="1 second")
     .start())

# Monitor running stream
q.status
q.lastProgress
q.awaitTermination()
q.stop()''')

    with col2:
        code_card("head-blue", "Stream → Delta (foreachBatch Upsert)", "foreach_batch.py", "python",
                  '''\
from delta.tables import DeltaTable

def upsert_batch(batch_df, batch_id):
    path = "/mnt/silver/events"
    if not DeltaTable.isDeltaTable(spark, path):
        batch_df.write.format("delta").save(path)
        return

    dt = DeltaTable.forPath(spark, path)
    (
        dt.alias("t")
        .merge(batch_df.alias("s"),
               "t.event_id = s.event_id")
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute()
    )

(
    stream_df.writeStream
    .foreachBatch(upsert_batch)
    .option("checkpointLocation", "/mnt/chkpt/silver")
    .trigger(processingTime="1 minute")
    .start()
)''')

        code_card("head-green", "Kafka → Bronze → Silver Pipeline", "kafka_pipeline.py", "python",
                  '''\
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType

schema = (StructType()
    .add("event_id", StringType())
    .add("user_id",  StringType())
    .add("amount",   DoubleType()))

# 1. Read from Kafka
raw = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "broker:9092")
    .option("subscribe", "events-topic")
    .load()
    .select(from_json(col("value").cast("string"),
                      schema).alias("data"))
    .select("data.*")
)

# 2. Land to Bronze
(raw.writeStream.format("delta")
    .option("checkpointLocation", "/chkpt/bronze")
    .toTable("bronze.kafka_events"))

# 3. Clean → Silver (separate stream)
bronze_stream = spark.readStream.table("bronze.kafka_events")
clean = bronze_stream.filter(col("event_id").isNotNull())
(clean.writeStream.format("delta")
     .option("checkpointLocation", "/chkpt/silver")
     .toTable("silver.events"))''')

# ════════════════════════════════════════════════════════
# 🚀 PERFORMANCE
# ════════════════════════════════════════════════════════
elif section == "🚀 Performance":

    col1, col2 = st.columns(2)
    with col1:
        code_card("head-gold", "OPTIMIZE & Z-ORDER", "optimize.sql", "sql",
                  '''\
-- Compact small files (bin-packing)
OPTIMIZE tableName;

-- Z-ORDER: co-locate related data for fast skipping
-- Use columns in WHERE/JOIN predicates
OPTIMIZE tableName ZORDER BY (colA, colB);

-- Partition-scoped optimization
OPTIMIZE tableName
WHERE date = '2024-01-01'
ZORDER BY (user_id);

-- Liquid Clustering (Delta 3.1+ — replaces Z-Order)
-- Better for high-cardinality, multi-column access
ALTER TABLE tableName CLUSTER BY (event_date, user_id);
OPTIMIZE tableName;   -- incremental, safe to run often

-- Auto-optimize on this table
ALTER TABLE tableName
SET TBLPROPERTIES (
    'delta.autoOptimize.optimizeWrite' = 'true',
    'delta.autoOptimize.autoCompact'   = 'true'
);''',
                  pills=[("Z-ORDER", "orange"), ("Liquid Clustering", "orange"), ("Auto-Optimize", "orange")])

        code_card("head-teal", "Data Skipping & Statistics", "stats.sql", "sql",
                  '''\
-- Data skipping uses min/max stats stored in Delta log
-- Collected automatically on write for first 32 columns

-- Control which columns collect stats
ALTER TABLE tableName
SET TBLPROPERTIES (
    'delta.dataSkippingNumIndexedCols' = '5'
);

-- Collect stats on existing data
ANALYZE TABLE tableName
COMPUTE DELTA STATISTICS;

-- Column-level statistics (for query pushdown)
ANALYZE TABLE tableName
COMPUTE STATISTICS FOR COLUMNS
    user_id, event_date, amount;

-- Check estimated row counts
DESCRIBE EXTENDED tableName;

-- Partition pruning: always filter on partition cols
SELECT * FROM tableName
WHERE event_date = '2024-01-01'   -- partition skip
  AND user_id = 'abc123';         -- Z-Order/cluster skip''')

    with col2:
        code_card("head-teal", "VACUUM — Clean Up Old Files", "vacuum.py", "python",
                  '''\
# SQL approach
spark.sql("VACUUM tableName")                  # 7d default
spark.sql("VACUUM tableName RETAIN 168 HOURS") # 7 days explicit
spark.sql("VACUUM tableName RETAIN 0 HOURS DRY RUN")  # preview

# Python API
from delta.tables import DeltaTable
dt = DeltaTable.forName(spark, "silver.events")
dt.vacuum()       # 7d default
dt.vacuum(100)    # 100h retention window

# Set retention via table properties
spark.sql("""
    ALTER TABLE tableName
    SET TBLPROPERTIES (
        'delta.logRetentionDuration'
            = 'interval 30 days',
        'delta.deletedFileRetentionDuration'
            = 'interval 7 days'
    )
""")

# Show current properties
spark.sql("SHOW TBLPROPERTIES tableName").show()''',
                  pills=[("Cleanup", "teal"), ("Retention", "teal"), ("DRY RUN", "teal")])

        code_card("head-purple", "Delta Cache & Caching", "cache.sql", "sql",
                  '''\
-- Databricks Delta Cache: SSD-backed I/O cache
-- Enabled by default on Databricks clusters

-- Cache a full table
CACHE SELECT * FROM tableName;

-- Cache a filtered subset
CACHE SELECT colA, colB
FROM tableName
WHERE colA > 0;

-- Cache in Python
spark.sql("CACHE SELECT * FROM silver.events")

-- Uncache
spark.sql("UNCACHE TABLE silver.events")

-- Spark in-memory cache (different from Delta cache)
df = spark.table("silver.events")
df.cache()          # lazy — materializes on first action
df.persist()        # same
df.count()          # trigger materialization
df.unpersist()      # release memory

-- Check if cached
spark.catalog.isCached("silver.events")''')

    st.markdown('<div class="sec-div">⚙️ Spark & Executor Tuning</div>',
                unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        code_card("head-blue", "Executor Memory Tuning", "executor_memory.py", "python",
                  '''\
# ── Executor memory layout ──
# executor.memory        = JVM heap (default 1g)
# memoryFraction         = fraction for execution+storage (default 0.6)
# storageFraction        = fraction of above for caching (default 0.5)
# memoryOverhead         = off-heap overhead for Python/containers

# Recommended cluster config (Spark conf or cluster UI)
spark.conf.set("spark.executor.memory",          "8g")
spark.conf.set("spark.executor.memoryOverhead",  "2g")   # off-heap
spark.conf.set("spark.memory.fraction",          "0.8")  # more for exec
spark.conf.set("spark.memory.storageFraction",   "0.3")  # less for cache

# Driver memory (for collect(), large DataFrames to driver)
spark.conf.set("spark.driver.memory",            "4g")
spark.conf.set("spark.driver.maxResultSize",     "2g")

# Executor cores (2-5 is sweet spot; avoid 1 or >5)
spark.conf.set("spark.executor.cores",           "4")

# Dynamic allocation (scale executors automatically)
spark.conf.set("spark.dynamicAllocation.enabled",             "true")
spark.conf.set("spark.dynamicAllocation.minExecutors",        "2")
spark.conf.set("spark.dynamicAllocation.maxExecutors",        "20")
spark.conf.set("spark.dynamicAllocation.initialExecutors",    "4")
spark.conf.set("spark.dynamicAllocation.executorIdleTimeout", "60s")

# Check current memory usage per executor
spark.sparkContext.statusTracker().getExecutorInfos()''',
                  pills=[("Executor Memory", "blue"), ("Dynamic Alloc", "blue"), ("Memory Fraction", "blue")])

        code_card("head-teal", "Shuffle & Partition Tuning", "shuffle_tuning.py", "python",
                  '''\
# ── Shuffle partition tuning (most impactful setting!) ──
# Default: 200 partitions — too small for large data, too big for small

# Rule of thumb: target 128MB–256MB per partition
# total_data_size / target_partition_size = num_partitions

spark.conf.set("spark.sql.shuffle.partitions", "400")   # after large joins/agg

# AQE auto-coalesces shuffle partitions (Spark 3+)
spark.conf.set("spark.sql.adaptive.enabled",                          "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled",       "true")
spark.conf.set("spark.sql.adaptive.advisoryPartitionSizeInBytes",     "128MB")
spark.conf.set("spark.sql.adaptive.coalescePartitions.minPartitionNum", "1")

# Repartition vs Coalesce
df_repartitioned = df.repartition(200)              # full shuffle, balanced
df_repartitioned = df.repartition(200, "date")      # shuffle on key (good for joins)
df_coalesced     = df.coalesce(10)                  # no shuffle, just merge — for writes

# Check current partition count and sizes
print(f"Partitions: {df.rdd.getNumPartitions()}")

from pyspark.sql.functions import spark_partition_id, count
df.groupBy(spark_partition_id().alias("pid")) \
  .agg(count("*").alias("rows")) \
  .orderBy("rows", ascending=False).show(10)

# Output file size control (Delta write)
spark.conf.set("spark.databricks.delta.targetFileSize", "134217728")  # 128 MB''',
                  pills=[("shuffle.partitions", "teal"), ("Repartition", "teal"), ("Coalesce", "teal")])

    with col2:
        code_card("head-purple", "Salting — Fix Data Skew", "salting.py", "python",
                  '''\
# ── Salting: fix skewed joins / groupBy ──
# Problem: one key (e.g. NULL, "US") has 90% of rows → hot partition

from pyspark.sql.functions import col, concat_ws, lit, floor, rand, explode, array

SALT_FACTOR = 50   # tune based on skew severity

# ── Salted GroupBy ──
from pyspark.sql.functions import floor, rand
salted = df.withColumn("salt", (rand() * SALT_FACTOR).cast("int"))
partial = (salted.groupBy("skewed_key", "salt")
                 .agg(sum("amount").alias("partial_sum")))
result  = partial.groupBy("skewed_key").agg(sum("partial_sum").alias("total"))

# ── Salted Join (large skewed left + small right) ──
# Step 1: replicate small table with all salt values
salt_vals = array(*[lit(i) for i in range(SALT_FACTOR)])
small_replicated = (small_df
    .withColumn("salt_arr", explode(salt_vals))
    .withColumnRenamed("join_key", "join_key_salt"))

# Step 2: add random salt to large (skewed) table
large_salted = large_df.withColumn(
    "join_key_salt",
    concat_ws("_", col("join_key"),
              (rand() * SALT_FACTOR).cast("int"))
)

# Step 3: join on salted key
result = large_salted.join(
    small_replicated,
    large_salted.join_key_salt == small_replicated.join_key_salt
).drop("join_key_salt", "salt_arr")''',
                  pills=[("Salting", "purple"), ("Skew Fix", "purple"), ("Hot Partition", "purple")])

        code_card("head-gold", "Bucketing — Pre-Shuffle for Joins", "bucketing.py", "python",
                  '''\
# ── Bucketing: eliminate shuffle for repeated joins ──
# Write once with buckets → all future joins on that key are shuffle-free

# Write bucketed table (must use saveAsTable — not save())
(orders_df
    .write
    .format("delta")
    .mode("overwrite")
    .bucketBy(64, "customer_id")    # 64 buckets on join key
    .sortBy("customer_id")          # optional: sort within bucket
    .saveAsTable("silver.orders_bucketed"))

(customers_df
    .write
    .format("delta")
    .mode("overwrite")
    .bucketBy(64, "customer_id")    # SAME number of buckets + key!
    .sortBy("customer_id")
    .saveAsTable("silver.customers_bucketed"))

# Now join — Spark skips the shuffle entirely
result = (
    spark.table("silver.orders_bucketed")
    .join(spark.table("silver.customers_bucketed"), "customer_id")
)
result.explain()
# Look for: SortMergeJoin without Exchange nodes = no shuffle ✅

# SQL equivalent
spark.sql("""
    CREATE TABLE silver.orders_bucketed
    USING DELTA
    CLUSTERED BY (customer_id) INTO 64 BUCKETS
    AS SELECT * FROM silver.orders
""")''',
                  pills=[("Bucketing", "gold"), ("No-Shuffle Join", "gold"), ("bucketBy", "gold")])

        code_card("head-green", "Kryo Serialization & Off-Heap", "kryo_offheap.py", "python",
                  '''\
# ── Kryo serialization: faster than Java default ──
spark.conf.set("spark.serializer",
               "org.apache.spark.serializer.KryoSerializer")
spark.conf.set("spark.kryo.unsafe",          "true")  # extra speed
spark.conf.set("spark.kryo.referenceTracking", "false")

# Register custom classes for even faster Kryo
spark.conf.set("spark.kryo.classesToRegister",
               "com.mycompany.MyClass,com.mycompany.OtherClass")

# ── Off-heap memory (reduces GC pressure) ──
spark.conf.set("spark.memory.offHeap.enabled", "true")
spark.conf.set("spark.memory.offHeap.size",    "4g")

# ── GC tuning (reduce GC pauses) ──
# In cluster/spark config:
# spark.executor.extraJavaOptions = -XX:+UseG1GC
#   -XX:InitiatingHeapOccupancyPercent=35
#   -XX:ConcGCThreads=4

# ── Accumulators: distributed counters ──
bad_rows    = spark.sparkContext.longAccumulator("bad_rows")
null_events = spark.sparkContext.longAccumulator("null_events")

def process_row(row):
    if row["amount"] is None:
        bad_rows.add(1)
        return None
    if row["event_id"] is None:
        null_events.add(1)
        return None
    return row

from pyspark.sql.functions import udf
from pyspark.sql.types import BooleanType

@udf(BooleanType())
def is_valid(amount, event_id):
    if amount is None: bad_rows.add(1); return False
    if event_id is None: null_events.add(1); return False
    return True

clean_df = df.filter(is_valid(col("amount"), col("event_id")))
clean_df.count()  # trigger action
print(f"Bad rows: {bad_rows.value}, Null events: {null_events.value}")''',
                  pills=[("Kryo", "green"), ("Off-Heap", "green"), ("Accumulators", "green")])

# ════════════════════════════════════════════════════════
# 🔧 UTILITY METHODS
# ════════════════════════════════════════════════════════
elif section == "🔧 Utility Methods":

    col1, col2 = st.columns(2)
    with col1:
        code_card("head-bronze", "Describe & Inspect Tables", "describe.sql", "sql",
                  '''\
-- View table details (size, partitions, location)
DESCRIBE DETAIL tableName;
DESCRIBE FORMATTED tableName;

-- List all columns with types
DESCRIBE tableName;

-- View table properties
SHOW TBLPROPERTIES tableName;

-- View partition info
SHOW PARTITIONS tableName;

-- List all tables in database
SHOW TABLES IN dbName;

-- Check Delta transaction log
DESCRIBE HISTORY tableName;

-- Python equivalent
dt = DeltaTable.forName(spark, "silver.events")
dt.detail().show(vertical=True)
dt.history(5).show()''')

        code_card("head-blue", "Clone a Delta Table", "clone.sql", "sql",
                  '''\
-- Deep clone: full data copy (independent)
CREATE TABLE [IF NOT EXISTS] silver.events_backup
DEEP CLONE silver.events;

-- Shallow clone: only metadata + log (no data copy)
-- Points to source files — cheap, fast, read-only safe
CREATE TABLE silver.events_dev
SHALLOW CLONE silver.events
VERSION AS OF 10;

-- Clone to a path (unmanaged)
CREATE TABLE delta.`/mnt/backup/events`
DEEP CLONE silver.events;

-- Python API
dt = DeltaTable.forName(spark, "silver.events")
dt.clone(
    target="/mnt/backup/events_clone",
    isShallow=True,
    replace=True
)''')

    with col2:
        code_card("head-green", "Run SQL from Python", "sql_from_python.py", "python",
                  '''\
# Execute any SQL statement
spark.sql("OPTIMIZE silver.events ZORDER BY (user_id)")
spark.sql("VACUUM silver.events RETAIN 168 HOURS")
spark.sql("DESCRIBE HISTORY silver.events").show(5)

# Multi-line SQL
result = spark.sql("""
    SELECT
        product_id,
        SUM(amount)   AS revenue,
        COUNT(*)      AS orders,
        AVG(amount)   AS aov
    FROM silver.events
    WHERE event_type = \'purchase\'
      AND event_date >= \'2024-01-01\'
    GROUP BY product_id
    ORDER BY revenue DESC
    LIMIT 20
""")
result.display()

# Read path-based Delta table
df = (spark.read.format("delta")
      .load("/path/to/delta_table"))

# Read path-based Delta with SQL (backticks)
spark.sql("SELECT * FROM delta.`/path/to/delta_table`")''')

        code_card("head-purple", "Manage Table Properties", "tblproperties.py", "python",
                  '''\
# Set multiple properties
spark.sql("""
    ALTER TABLE silver.events
    SET TBLPROPERTIES (
        'delta.autoOptimize.optimizeWrite' = 'true',
        'delta.autoOptimize.autoCompact'   = 'true',
        'delta.logRetentionDuration'       = 'interval 30 days',
        'delta.deletedFileRetentionDuration' = 'interval 7 days',
        'delta.dataSkippingNumIndexedCols' = '10',
        'comment' = 'Cleansed events table - Silver layer'
    )
""")

# View all properties
spark.sql("SHOW TBLPROPERTIES silver.events").show(50, False)

# Unset a property
spark.sql("""
    ALTER TABLE silver.events
    UNSET TBLPROPERTIES IF EXISTS
        ('delta.autoOptimize.autoCompact')
""")''')

# ════════════════════════════════════════════════════════
# 🏗️ ARCHITECTURE & DESIGN
# ════════════════════════════════════════════════════════
elif section == "🏗️ Architecture & Design":

    st.markdown('<div class="sec-div">🏗️ Unity Catalog & Architecture Patterns</div>',
                unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        code_card("head-blue", "Unity Catalog — 3-Level Namespace", "unity_catalog.sql", "sql",
                  '''\
-- Unity Catalog: catalog.schema.table (3 levels)
-- catalog  = top-level container (e.g. prod, dev)
-- schema   = database / namespace
-- table    = Delta table or view

-- Create catalog (workspace admin required)
CREATE CATALOG IF NOT EXISTS prod;
CREATE CATALOG IF NOT EXISTS dev;

-- Create schema inside catalog
CREATE SCHEMA IF NOT EXISTS prod.silver;
CREATE SCHEMA IF NOT EXISTS prod.gold;

-- Create table with full 3-level path
CREATE TABLE prod.silver.events (
    event_id   STRING NOT NULL,
    user_id    STRING,
    event_ts   TIMESTAMP,
    amount     DOUBLE
) USING DELTA
PARTITIONED BY (DATE(event_ts));

-- Query with full namespace
SELECT * FROM prod.silver.events;

-- Set default catalog for session
USE CATALOG prod;
USE SCHEMA silver;
SELECT * FROM events;  -- resolves to prod.silver.events

-- List catalogs / schemas / tables
SHOW CATALOGS;
SHOW SCHEMAS IN prod;
SHOW TABLES IN prod.silver;''',
                  pills=[("Unity Catalog", "blue"), ("3-Level Namespace", "blue")])

        code_card("head-teal", "External Locations & Storage Credentials", "external_location.sql", "sql",
                  '''\
-- Step 1: Create storage credential (admin only)
CREATE STORAGE CREDENTIAL my_adls_cred
WITH AZURE_MANAGED_IDENTITY (
    connector_id = '/subscriptions/.../connectors/myConnector'
);

-- Step 2: Create external location pointing to storage
CREATE EXTERNAL LOCATION my_ext_loc
URL 'abfss://container@storageacct.dfs.core.windows.net/path'
WITH (STORAGE CREDENTIAL my_adls_cred);

-- Step 3: Grant access to users
GRANT READ FILES ON EXTERNAL LOCATION my_ext_loc
TO `data-engineers@company.com`;

-- Create external Delta table at that location
CREATE TABLE prod.bronze.raw_events
USING DELTA
LOCATION 'abfss://bronze@storageacct.dfs.core.windows.net/events';

-- Show all external locations
SHOW EXTERNAL LOCATIONS;
DESCRIBE EXTERNAL LOCATION my_ext_loc;''',
                  pills=[("External Location", "teal"), ("ADLS Gen2", "teal"), ("Storage Cred", "teal")])

        code_card("head-purple", "Delta Sharing — Cross-Org Data", "delta_sharing.sql", "sql",
                  '''\
-- Delta Sharing: share Delta tables without copying data

-- Step 1: Create a share
CREATE SHARE customer_share
COMMENT 'Share for external partner analytics';

-- Step 2: Add tables to the share
ALTER SHARE customer_share
ADD TABLE prod.gold.daily_revenue
  COMMENT 'Aggregated daily revenue';

ALTER SHARE customer_share
ADD TABLE prod.gold.product_catalog
  PARTITION (region = 'US');  -- filter by partition

-- Step 3: Create recipient
CREATE RECIPIENT partner_analytics
COMMENT 'External BI team'
USING ID 'databricks://sharing.cloud.databricks.com/.../share';

-- Step 4: Grant recipient access to share
GRANT SELECT ON SHARE customer_share TO RECIPIENT partner_analytics;

-- View shares & recipients
SHOW SHARES;
SHOW RECIPIENTS;
DESCRIBE SHARE customer_share;
SHOW ALL IN SHARE customer_share;''',
                  pills=[("Delta Sharing", "purple"), ("Cross-Org", "purple"), ("Zero Copy", "purple")])

    with col2:
        code_card("head-bronze", "Change Data Capture (CDC) Pattern", "cdc_pattern.py", "python",
                  '''\
# ── CDC Pattern: Bronze → Silver via APPLY CHANGES ──
# Uses DLT (Delta Live Tables) APPLY CHANGES INTO

import dlt
from pyspark.sql.functions import col

# 1. Bronze: raw CDC events from Kafka/Debezium
@dlt.table(name="bronze_cdc_events",
           comment="Raw CDC from source DB via Debezium")
def bronze_cdc():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load("/mnt/cdc/source_db/customers/")
    )

# 2. Silver: apply CDC changes with dedup
dlt.apply_changes(
    target         = "silver_customers",
    source         = "bronze_cdc_events",
    keys           = ["customer_id"],
    sequence_by    = col("_commit_timestamp"),
    apply_as_deletes = col("_op") == "DELETE",
    except_column_list = ["_op", "_db", "_table"],
    stored_as_scd_type = 1   # or 2 for full history
)

# ── Non-DLT CDC merge pattern ──
from delta.tables import DeltaTable
from pyspark.sql.functions import lit

def apply_cdc_batch(batch_df, batch_id):
    deletes = batch_df.filter(col("_op") == "DELETE")
    upserts = batch_df.filter(col("_op").isin("INSERT","UPDATE"))

    dt = DeltaTable.forName(spark, "silver.customers")
    # Apply upserts
    (dt.alias("t").merge(upserts.alias("s"), "t.id = s.id")
       .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute())
    # Apply deletes
    (dt.alias("t").merge(deletes.alias("s"), "t.id = s.id")
       .whenMatchedDelete().execute())''',
                  pills=[("CDC", "orange"), ("Debezium", "orange"), ("APPLY CHANGES", "orange")])

        code_card("head-green", "Data Contract / Schema Registry", "data_contract.py", "python",
                  '''\
# ── Enforce Data Contracts using Delta constraints ──

# 1. Define contract via table DDL constraints
spark.sql("""
    CREATE TABLE IF NOT EXISTS prod.silver.orders (
        order_id    STRING  NOT NULL,
        customer_id STRING  NOT NULL,
        amount      DOUBLE  NOT NULL,
        status      STRING  NOT NULL,
        order_date  DATE    NOT NULL
    ) USING DELTA
""")

# 2. Add CHECK constraints (contract rules)
spark.sql("""
    ALTER TABLE prod.silver.orders
    ADD CONSTRAINT positive_amount CHECK (amount > 0)
""")
spark.sql("""
    ALTER TABLE prod.silver.orders
    ADD CONSTRAINT valid_status
    CHECK (status IN ('pending','confirmed','shipped','cancelled'))
""")

# 3. Validate schema before writing
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, DateType

CONTRACT_SCHEMA = StructType([
    StructField("order_id",    StringType(), nullable=False),
    StructField("customer_id", StringType(), nullable=False),
    StructField("amount",      DoubleType(), nullable=False),
    StructField("status",      StringType(), nullable=False),
    StructField("order_date",  DateType(),   nullable=False),
])

def validate_schema(df, contract):
    missing = set(f.name for f in contract.fields) - set(df.columns)
    if missing:
        raise ValueError(f"Contract violation — missing cols: {missing}")
    return df.select([f.name for f in contract.fields])

validated_df = validate_schema(raw_df, CONTRACT_SCHEMA)
validated_df.write.format("delta").mode("append").saveAsTable("prod.silver.orders")''',
                  pills=[("Data Contract", "green"), ("Schema Enforce", "green"), ("CHECK Constraint", "green")])


# ════════════════════════════════════════════════════════
# 🔄 INGESTION & ETL
# ════════════════════════════════════════════════════════
elif section == "🔄 Ingestion & ETL":

    col1, col2 = st.columns(2)
    with col1:
        code_card("head-bronze", "Auto Loader — Advanced Options", "autoloader_advanced.py", "python",
                  '''\
# ── Auto Loader: Advanced Configuration ──

# Rescue unknown columns into _rescued_data
bronze_df = (
    spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation",  "/mnt/schema/events")
    .option("cloudFiles.inferColumnTypes", "true")
    .option("cloudFiles.schemaEvolutionMode", "rescue")   # rescue | addNewColumns | failOnNewColumns
    .option("cloudFiles.rescuedDataColumn", "_rescued")
    .option("cloudFiles.maxFilesPerTrigger", 1000)
    .option("cloudFiles.includeExistingFiles", "true")
    # File notification mode (faster than directory listing)
    .option("cloudFiles.useNotifications", "true")
    .option("cloudFiles.subscriptionId", "<azure-sub-id>")
    .option("cloudFiles.resourceGroup",  "<resource-group>")
    .option("cloudFiles.tenantId",       "<tenant-id>")
    .option("cloudFiles.clientId",       "<client-id>")
    .option("cloudFiles.clientSecret",   dbutils.secrets.get("kv","client-secret"))
    .load("abfss://landing@storageacct.dfs.core.windows.net/events/")
)

# Schema hints for known columns
spark.readStream.format("cloudFiles") \
    .option("cloudFiles.schemaHints",
            "amount DOUBLE, event_ts TIMESTAMP") \
    .load(path)''',
                  pills=[("cloudFiles", "orange"), ("Schema Evolution", "orange"), ("File Notifications", "orange")])

        code_card("head-blue", "COPY INTO — Multi-Format", "copy_into_advanced.sql", "sql",
                  '''\
-- JSON with nested field selection
COPY INTO bronze.api_events
FROM (
    SELECT
        get_json_object(jsonData, "$.event_id")   AS event_id,
        get_json_object(jsonData, "$.user.id")    AS user_id,
        get_json_object(jsonData, "$.timestamp")  AS event_ts,
        CAST(get_json_object(jsonData, "$.amount") AS DOUBLE) AS amount
    FROM "/mnt/landing/api_events/"
)
FILEFORMAT = JSON
COPY_OPTIONS ("force" = "false");

-- Avro ingestion
COPY INTO bronze.kafka_events
FROM "/mnt/kafka/events/"
FILEFORMAT = AVRO;

-- ORC ingestion with partition columns
COPY INTO bronze.hive_exports
FROM (
    SELECT *, year, month
    FROM "/mnt/hive/exports/"
)
FILEFORMAT = ORC
COPY_OPTIONS ("mergeSchema" = "true");

-- Check what was loaded
SELECT operation, operationParameters, numOutputRows
FROM (DESCRIBE HISTORY bronze.api_events)
WHERE operation = "WRITE"
ORDER BY version DESC LIMIT 5;''',
                  pills=[("JSON", "blue"), ("Avro", "blue"), ("ORC", "blue")])

        code_card("head-green", "Multi-Hop Pipeline Orchestration", "multi_hop.py", "python",
                  '''\
# ── Multi-hop ETL pipeline helper ──
from delta.tables import DeltaTable
from pyspark.sql.functions import current_timestamp, col

class MedallionPipeline:
    def __init__(self, spark, catalog="prod"):
        self.spark = spark
        self.catalog = catalog

    def bronze_to_silver(self, source_table, target_table,
                         key_cols, dedup_col="_ingest_time"):
        from pyspark.sql.window import Window
        from pyspark.sql.functions import row_number

        df = self.spark.table(f"{self.catalog}.bronze.{source_table}")

        # Dedup
        w = Window.partitionBy(key_cols).orderBy(col(dedup_col).desc())
        clean = df.withColumn("_rn", row_number().over(w)) \
                  .filter(col("_rn") == 1).drop("_rn")

        # Merge
        full_target = f"{self.catalog}.silver.{target_table}"
        if DeltaTable.isDeltaTable(self.spark, full_target):
            dt = DeltaTable.forName(self.spark, full_target)
            cond = " AND ".join([f"t.{k}=s.{k}" for k in key_cols])
            (dt.alias("t").merge(clean.alias("s"), cond)
               .whenMatchedUpdateAll()
               .whenNotMatchedInsertAll()
               .execute())
        else:
            clean.write.format("delta").saveAsTable(full_target)

    def silver_to_gold(self, query, target_table):
        gold_df = self.spark.sql(query)
        (gold_df.write.format("delta").mode("overwrite")
                .option("overwriteSchema","true")
                .saveAsTable(f"{self.catalog}.gold.{target_table}"))

# Usage
pipeline = MedallionPipeline(spark)
pipeline.bronze_to_silver("raw_orders", "orders", ["order_id"])
pipeline.silver_to_gold("""
    SELECT DATE(order_date) AS dt,
           SUM(amount) AS revenue
    FROM prod.silver.orders GROUP BY 1
""", "daily_revenue")''',
                  pills=[("Multi-hop", "green"), ("Reusable", "green"), ("Class Pattern", "green")])

    with col2:
        code_card("head-teal", "Debezium CDC Ingestion Pattern", "debezium_cdc.py", "python",
                  '''\
# ── Ingest Debezium CDC from Kafka → Bronze ──
from pyspark.sql.functions import from_json, col, get_json_object
from pyspark.sql.types import StructType, StringType, LongType

# Debezium envelope schema (simplified)
DEBEZIUM_SCHEMA = StructType() \
    .add("before", StringType()) \
    .add("after",  StringType()) \
    .add("op",     StringType()) \
    .add("ts_ms",  LongType())

# Read from Kafka
raw = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "broker:9092")
    .option("subscribe", "dbserver.public.orders")
    .option("startingOffsets", "latest")
    .load()
)

# Parse Debezium envelope
parsed = (
    raw
    .select(from_json(col("value").cast("string"),
                      DEBEZIUM_SCHEMA).alias("cdc"))
    .select(
        get_json_object(col("cdc.after"),  "$.order_id").alias("order_id"),
        get_json_object(col("cdc.after"),  "$.amount").cast("double").alias("amount"),
        get_json_object(col("cdc.after"),  "$.status").alias("status"),
        col("cdc.op").alias("_op"),
        (col("cdc.ts_ms") / 1000).cast("timestamp").alias("_cdc_ts")
    )
)

# Land to Bronze
(parsed.writeStream.format("delta")
       .option("checkpointLocation", "/mnt/chkpt/cdc_orders")
       .outputMode("append")
       .toTable("bronze.cdc_orders"))''',
                  pills=[("Debezium", "teal"), ("Kafka CDC", "teal"), ("Envelope Parse", "teal")])

        code_card("head-purple", "APPLY CHANGES INTO (DLT CDC)", "apply_changes.py", "python",
                  '''\
# ── DLT: APPLY CHANGES INTO — easiest CDC pattern ──
import dlt
from pyspark.sql.functions import col, expr

# Source: streaming CDC events
@dlt.table(name="bronze_orders_cdc")
def bronze_orders_cdc():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load("/mnt/cdc/orders/")
    )

# Target: SCD Type 1 (latest value wins)
dlt.apply_changes(
    target      = "silver_orders",
    source      = "bronze_orders_cdc",
    keys        = ["order_id"],
    sequence_by = col("_commit_version"),
    apply_as_deletes   = expr("_op = 'DELETE'"),
    apply_as_truncates = expr("_op = 'TRUNCATE'"),
    column_list        = ["order_id", "customer_id", "amount", "status"],
    stored_as_scd_type = 1
)

# SCD Type 2 (full history preserved)
dlt.apply_changes(
    target             = "silver_customers_history",
    source             = "bronze_customers_cdc",
    keys               = ["customer_id"],
    sequence_by        = col("_commit_timestamp"),
    stored_as_scd_type = 2,
    track_history_column_list = ["email", "address", "tier"]
)''',
                  pills=[("APPLY CHANGES", "purple"), ("SCD Type 1/2", "purple"), ("DLT CDC", "purple")])


# ════════════════════════════════════════════════════════
# 🧪 DATA QUALITY & GOVERNANCE
# ════════════════════════════════════════════════════════
elif section == "🧪 Data Quality & Governance":

    col1, col2 = st.columns(2)
    with col1:
        code_card("head-green", "DLT Expectations — Data Quality Rules", "dlt_expectations.py", "python",
                  '''\
import dlt
from pyspark.sql.functions import col

# ── @dlt.expect: warn but keep bad rows ──
@dlt.expect("non_negative_amount", "amount >= 0")
@dlt.expect("valid_status",
            "status IN (\'pending\',\'confirmed\',\'shipped\')")
@dlt.table
def silver_orders():
    return dlt.read_stream("bronze_orders")

# ── @dlt.expect_or_drop: silently drop bad rows ──
@dlt.expect_or_drop("not_null_order_id", "order_id IS NOT NULL")
@dlt.expect_or_drop("valid_date",        "order_date > \'2020-01-01\'")
@dlt.table
def silver_orders_clean():
    return dlt.read_stream("bronze_orders")

# ── @dlt.expect_or_fail: halt pipeline on violation ──
@dlt.expect_or_fail("no_duplicates",
    "COUNT(*) OVER (PARTITION BY order_id) = 1")
@dlt.table
def silver_orders_strict():
    return dlt.read_stream("bronze_orders")

# ── @dlt.expect_all: multiple rules at once ──
RULES = {
    "valid_order_id":  "order_id IS NOT NULL",
    "positive_amount": "amount > 0",
    "known_region":    "region IN (\'US\',\'EU\',\'APAC\')"
}

@dlt.expect_all(RULES)
@dlt.expect_all_or_drop(RULES)  # or drop bad rows
@dlt.table
def silver_orders_validated():
    return dlt.read_stream("bronze_orders")''',
                  pills=[("@dlt.expect", "green"), ("expect_or_drop", "green"), ("expect_or_fail", "green")])

        code_card("head-blue", "Row-Level Security with Dynamic Views", "rls.sql", "sql",
                  '''\
-- ── Row-Level Security via Dynamic View ──

-- Create secure view that filters by current user
CREATE OR REPLACE VIEW prod.silver.orders_secure AS
SELECT *
FROM prod.silver.orders
WHERE
  -- Admins see everything
  is_member("data-admins") = TRUE
  OR
  -- Analysts see only their region
  region = (
    SELECT region FROM prod.security.user_region_map
    WHERE email = current_user()
  );

-- Grant view access (not table directly)
GRANT SELECT ON VIEW prod.silver.orders_secure
TO `data-analysts@company.com`;

-- Verify RLS is working
SELECT current_user();
SELECT * FROM prod.silver.orders_secure LIMIT 10;

-- Column-level masking (Unity Catalog)
CREATE OR REPLACE FUNCTION prod.security.mask_pii(val STRING)
RETURNS STRING
RETURN CASE
    WHEN is_member("pii-access-group") THEN val
    ELSE CONCAT(LEFT(val, 2), "****")
END;

ALTER TABLE prod.silver.customers
ALTER COLUMN email
SET MASK prod.security.mask_pii;''',
                  pills=[("RLS", "blue"), ("Dynamic View", "blue"), ("Column Masking", "blue")])

    with col2:
        code_card("head-purple", "Great Expectations Integration", "great_expectations.py", "python",
                  '''\
# ── Great Expectations with Databricks ──
# pip install great-expectations

import great_expectations as gx
from great_expectations.dataset import SparkDFDataset

# Wrap Spark DataFrame
df = spark.table("silver.orders")
ge_df = SparkDFDataset(df)

# Define expectations
ge_df.expect_column_to_exist("order_id")
ge_df.expect_column_values_to_not_be_null("order_id")
ge_df.expect_column_values_to_not_be_null("customer_id")
ge_df.expect_column_values_to_be_between(
    "amount", min_value=0, max_value=100000
)
ge_df.expect_column_values_to_be_in_set(
    "status", ["pending", "confirmed", "shipped", "cancelled"]
)
ge_df.expect_column_values_to_match_regex(
    "email", r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)

# Run validation
results = ge_df.validate()

# Fail pipeline if expectations not met
if not results["success"]:
    failed = [r for r in results["results"] if not r["success"]]
    raise ValueError(f"DQ validation failed: {failed}")

print(f"✅ All {len(results['results'])} expectations passed")''',
                  pills=[("Great Expectations", "purple"), ("DQ Validation", "purple")])

        code_card("head-teal", "Data Lineage via Unity Catalog", "lineage.sql", "sql",
                  '''\
-- Unity Catalog auto-tracks lineage for:
-- SELECT, CREATE TABLE AS, INSERT INTO,
-- MERGE INTO, CREATE VIEW, Python DataFrames

-- View column-level lineage in UI:
-- Catalog Explorer → Table → Lineage tab

-- Query lineage programmatically via system tables
SELECT
    source_table_full_name,
    target_table_full_name,
    created_by,
    created_at
FROM system.access.table_lineage
WHERE target_table_full_name = 'prod.gold.daily_revenue'
ORDER BY created_at DESC;

-- Column-level lineage
SELECT
    source_table_full_name,
    source_column_name,
    target_table_full_name,
    target_column_name
FROM system.access.column_lineage
WHERE target_table_full_name = 'prod.gold.daily_revenue'
  AND target_column_name     = 'total_revenue';

-- Audit: who accessed what
SELECT
    user_identity.email,
    request_params.full_name_arg AS table_accessed,
    event_time
FROM system.access.audit
WHERE action_name = 'getTable'
ORDER BY event_time DESC LIMIT 20;''',
                  pills=[("Lineage", "teal"), ("system.access", "teal"), ("Audit Log", "teal")])


# ════════════════════════════════════════════════════════
# ⚙️ JOBS & ORCHESTRATION
# ════════════════════════════════════════════════════════
elif section == "⚙️ Jobs & Orchestration":

    col1, col2 = st.columns(2)
    with col1:
        code_card("head-bronze", "Databricks Workflows — Multi-Task Job", "workflow.py", "python",
                  '''\
# ── Databricks Jobs API: create multi-task workflow ──
import requests, json

TOKEN   = dbutils.secrets.get("kv", "databricks-pat")
HOST    = "https://<workspace>.azuredatabricks.net"
HEADERS = {"Authorization": f"Bearer {TOKEN}",
           "Content-Type": "application/json"}

job_config = {
    "name": "Medallion ETL Pipeline",
    "tasks": [
        {
            "task_key": "bronze_ingest",
            "description": "Ingest raw events to Bronze",
            "notebook_task": {
                "notebook_path": "/Repos/prod/pipelines/01_bronze_ingest",
                "base_parameters": {"env": "prod"}
            },
            "job_cluster_key": "etl_cluster",
            "timeout_seconds": 3600
        },
        {
            "task_key": "silver_transform",
            "depends_on": [{"task_key": "bronze_ingest"}],
            "notebook_task": {
                "notebook_path": "/Repos/prod/pipelines/02_silver_transform"
            },
            "job_cluster_key": "etl_cluster"
        },
        {
            "task_key": "gold_aggregate",
            "depends_on": [{"task_key": "silver_transform"}],
            "python_wheel_task": {
                "package_name": "etl_pipeline",
                "entry_point": "run_gold"
            },
            "job_cluster_key": "etl_cluster"
        }
    ],
    "job_clusters": [{
        "job_cluster_key": "etl_cluster",
        "new_cluster": {
            "spark_version": "14.3.x-scala2.12",
            "node_type_id": "Standard_DS3_v2",
            "num_workers": 4
        }
    }],
    "schedule": {
        "quartz_cron_expression": "0 0 6 * * ?",
        "timezone_id": "UTC"
    }
}

resp = requests.post(f"{HOST}/api/2.1/jobs/create",
                     headers=HEADERS, json=job_config)
print(f"Job ID: {resp.json()[\'job_id\']}")''',
                  pills=[("Workflows", "orange"), ("Multi-Task", "orange"), ("Depends On", "orange")])

        code_card("head-blue", "dbutils — Essential Utilities", "dbutils.py", "python",
                  '''\
# ── dbutils.fs: File System operations ──
dbutils.fs.ls("/mnt/bronze/events/")          # list files
dbutils.fs.mkdirs("/mnt/silver/new_table/")   # create dir
dbutils.fs.cp("/mnt/src/file", "/mnt/dst/")   # copy
dbutils.fs.mv("/mnt/src/file", "/mnt/dst/")   # move
dbutils.fs.rm("/mnt/old/path/", recurse=True) # delete
dbutils.fs.head("/mnt/file.json", 1024)        # preview bytes
dbutils.fs.put("/mnt/out.txt", "hello world") # write text

# ── dbutils.secrets: retrieve secrets ──
token  = dbutils.secrets.get(scope="kv",  key="api-token")
pw     = dbutils.secrets.get(scope="kv",  key="db-password")
dbutils.secrets.listScopes()
dbutils.secrets.list(scope="kv")

# ── dbutils.widgets: parameterize notebooks ──
dbutils.widgets.text("env",    "dev",  "Environment")
dbutils.widgets.text("date",   "",     "Run Date (YYYY-MM-DD)")
dbutils.widgets.dropdown("layer", "silver", ["bronze","silver","gold"])

env   = dbutils.widgets.get("env")
date  = dbutils.widgets.get("date")
layer = dbutils.widgets.get("layer")

# ── dbutils.notebook: run another notebook ──
result = dbutils.notebook.run(
    "/Repos/prod/pipelines/helper",
    timeout_seconds=600,
    arguments={"env": env, "date": date}
)

# Exit with value (for parent notebook)
dbutils.notebook.exit(json.dumps({"status": "success", "rows": 1234}))''',
                  pills=[("dbutils.fs", "blue"), ("dbutils.secrets", "blue"), ("dbutils.widgets", "blue")])

    with col2:
        code_card("head-teal", "Databricks Asset Bundles (DABs) — CI/CD", "databricks.yml", "yaml",
                  '''\
# databricks.yml — project root config
bundle:
  name: medallion_etl

variables:
  env:
    default: dev

targets:
  dev:
    mode: development
    workspace:
      host: https://dev-workspace.azuredatabricks.net
    variables:
      env: dev

  prod:
    mode: production
    workspace:
      host: https://prod-workspace.azuredatabricks.net
    variables:
      env: prod

resources:
  jobs:
    medallion_pipeline:
      name: "Medallion ETL - ${var.env}"
      schedule:
        quartz_cron_expression: "0 0 6 * * ?"
        timezone_id: UTC
      tasks:
        - task_key: bronze
          notebook_task:
            notebook_path: ./notebooks/01_bronze.py
            base_parameters:
              env: ${var.env}
          job_cluster_key: etl_cluster

        - task_key: silver
          depends_on:
            - task_key: bronze
          python_wheel_task:
            package_name: etl_pipeline
            entry_point:  run_silver

      job_clusters:
        - job_cluster_key: etl_cluster
          new_cluster:
            spark_version: "14.3.x-scala2.12"
            num_workers: 4

# CLI commands:
# databricks bundle validate
# databricks bundle deploy --target dev
# databricks bundle run medallion_pipeline --target prod''',
                  pills=[("DABs", "teal"), ("CI/CD", "teal"), ("IaC", "teal")])

        code_card("head-purple", "Databricks CLI — Common Commands", "cli.sh", "bash",
                  '''\
# ── Install & Configure Databricks CLI ──
pip install databricks-cli

# Authenticate
databricks configure --token
# or with OAuth
databricks auth login --host https://workspace.azuredatabricks.net

# ── Clusters ──
databricks clusters list
databricks clusters get --cluster-id <id>
databricks clusters start --cluster-id <id>
databricks clusters delete --cluster-id <id>

# ── Jobs ──
databricks jobs list
databricks jobs get --job-id <id>
databricks jobs run-now --job-id <id>
databricks runs list --job-id <id>
databricks runs get-output --run-id <id>

# ── DBFS / Files ──
databricks fs ls dbfs:/mnt/bronze/
databricks fs cp local_file.py dbfs:/mnt/scripts/
databricks fs rm dbfs:/mnt/old/ --recursive

# ── Repos ──
databricks repos list
databricks repos update --repo-id <id> --branch main

# ── Secrets ──
databricks secrets list-scopes
databricks secrets list --scope kv
databricks secrets put --scope kv --key api-token

# ── Asset Bundles ──
databricks bundle validate
databricks bundle deploy --target prod
databricks bundle run <job-name> --target prod''',
                  pills=[("CLI", "purple"), ("Automation", "purple"), ("DevOps", "purple")])


# ════════════════════════════════════════════════════════
# 🧠 ADVANCED DELTA LAKE
# ════════════════════════════════════════════════════════
elif section == "🧠 Advanced Delta Lake":

    col1, col2 = st.columns(2)
    with col1:
        code_card("head-bronze", "Change Data Feed (CDF)", "cdf.py", "python",
                  '''\
# ── Enable Change Data Feed on table ──
spark.sql("""
    ALTER TABLE silver.orders
    SET TBLPROPERTIES (delta.enableChangeDataFeed = true)
""")

# Enable at CREATE time
spark.sql("""
    CREATE TABLE silver.orders (...)
    USING DELTA
    TBLPROPERTIES (delta.enableChangeDataFeed = true)
""")

# ── Read CDF: batch ──
cdf_df = (
    spark.read.format("delta")
    .option("readChangeFeed", "true")
    .option("startingVersion", 5)        # from version
    # .option("startingTimestamp", "2024-01-01")
    # .option("endingVersion", 10)
    .table("silver.orders")
)

# CDF adds metadata columns:
# _change_type: insert | update_preimage | update_postimage | delete
# _commit_version: Long
# _commit_timestamp: Timestamp

cdf_df.filter(col("_change_type") == "update_postimage").show()

# ── Read CDF: streaming ──
stream_cdf = (
    spark.readStream.format("delta")
    .option("readChangeFeed", "true")
    .option("startingVersion", "latest")
    .table("silver.orders")
)

# Use CDF to propagate changes downstream
(stream_cdf
    .filter(col("_change_type").isin("insert","update_postimage"))
    .drop("_change_type","_commit_version","_commit_timestamp")
    .writeStream.format("delta")
    .option("checkpointLocation", "/mnt/chkpt/gold_orders_cdf")
    .outputMode("append")
    .toTable("gold.orders_propagated"))''',
                  pills=[("CDF", "orange"), ("readChangeFeed", "orange"), ("Incremental", "orange")])

        code_card("head-blue", "Deletion Vectors & Row Tracking", "deletion_vectors.sql", "sql",
                  '''\
-- Deletion Vectors: soft-delete rows without rewriting files
-- Dramatically speeds up DELETE/UPDATE/MERGE

-- Enable Deletion Vectors
ALTER TABLE silver.events
SET TBLPROPERTIES (
    "delta.enableDeletionVectors" = "true"
);

-- Enable at table creation
CREATE TABLE silver.events (...)
USING DELTA
TBLPROPERTIES ("delta.enableDeletionVectors" = "true");

-- Enable globally for all new tables
SET spark.databricks.delta.properties.defaults
    .enableDeletionVectors = true;

-- Row Tracking: stable row IDs across rewrites
ALTER TABLE silver.events
SET TBLPROPERTIES (
    "delta.enableRowTracking" = "true"
);

-- Access row ID and commit version
SELECT
    _metadata.row_id,
    _metadata.row_commit_version,
    *
FROM silver.events;

-- REORG: materialize deletion vectors (cleanup)
REORG TABLE silver.events APPLY (PURGE);

-- Check deletion vector stats
DESCRIBE DETAIL silver.events;''',
                  pills=[("Deletion Vectors", "blue"), ("Row Tracking", "blue"), ("Fast DML", "blue")])

    with col2:
        code_card("head-green", "Predictive Optimization & Auto Tune", "predictive_opt.sql", "sql",
                  '''\
-- Predictive Optimization (Databricks-managed)
-- Auto-runs OPTIMIZE & VACUUM based on usage patterns

-- Enable for a table
ALTER TABLE silver.events
SET TBLPROPERTIES (
    "delta.predictiveOptimization" = "enable"
);

-- Enable for an entire schema
ALTER SCHEMA prod.silver
SET DBPROPERTIES (
    "delta.predictiveOptimization" = "enable"
);

-- Enable catalog-wide (Unity Catalog admin)
ALTER CATALOG prod
SET DBPROPERTIES (
    "delta.predictiveOptimization" = "enable"
);

-- Check predictive optimization history
SELECT * FROM system.storage.predictive_optimization_operations
WHERE table_name = "silver.events"
ORDER BY timestamp DESC
LIMIT 20;

-- Manual override: disable on specific table
ALTER TABLE silver.large_static_table
SET TBLPROPERTIES (
    "delta.predictiveOptimization" = "disable"
);

-- REORG TABLE: combined OPTIMIZE + purge DVs
REORG TABLE silver.events APPLY (PURGE);''',
                  pills=[("Predictive Opt", "green"), ("Auto OPTIMIZE", "green"), ("Auto VACUUM", "green")])

        code_card("head-purple", "Delta Log & Transaction Log Deep Dive", "delta_log.py", "python",
                  '''\
# ── Inspect the Delta Transaction Log ──

# List _delta_log entries
dbutils.fs.ls("/mnt/silver/events/_delta_log/")
# → 00000000000000000000.json  (first commit)
# → 00000000000000000001.json
# → 00000000000000000010.checkpoint.parquet

# Read a commit JSON (shows what changed)
import json
log_entry = dbutils.fs.head(
    "/mnt/silver/events/_delta_log/00000000000000000005.json"
)
for line in log_entry.strip().split("\n"):
    print(json.dumps(json.loads(line), indent=2))

# Read checkpoint file (snapshot of all active files)
checkpoint_df = spark.read.parquet(
    "/mnt/silver/events/_delta_log/*.checkpoint.parquet"
)
checkpoint_df.printSchema()

# Python: get active files list
from delta.tables import DeltaTable
dt = DeltaTable.forName(spark, "silver.events")

# Detail shows numFiles, sizeInBytes, partitionColumns
dt.detail().select(
    "numFiles","sizeInBytes","partitionColumns","numOutputRows"
).show(vertical=True)

# Log compaction (prevent too many small JSON files)
spark.sql("REORG TABLE silver.events APPLY (PURGE)")

# History with full operation details
dt.history().select(
    "version","timestamp","operation",
    "operationMetrics","userMetadata"
).show(10, truncate=False)''',
                  pills=[("Delta Log", "purple"), ("Checkpoint", "purple"), ("Transaction Log", "purple")])


# ════════════════════════════════════════════════════════
# 📊 QUERY OPTIMIZATION
# ════════════════════════════════════════════════════════
elif section == "📊 Query Optimization":

    col1, col2 = st.columns(2)
    with col1:
        code_card("head-gold", "Adaptive Query Execution (AQE)", "aqe.py", "python",
                  '''\
# ── Adaptive Query Execution (AQE) — enabled by default ──
# AQE re-optimizes query plans at runtime using actual stats

# Check AQE status
spark.conf.get("spark.sql.adaptive.enabled")  # default: true

# Enable explicitly
spark.conf.set("spark.sql.adaptive.enabled", "true")

# AQE features:
# 1. Coalesce shuffle partitions (reduce small partitions)
spark.conf.set(
    "spark.sql.adaptive.coalescePartitions.enabled", "true"
)
spark.conf.set(
    "spark.sql.adaptive.advisoryPartitionSizeInBytes", "128MB"
)

# 2. Switch join strategies at runtime (skew join fix)
spark.conf.set(
    "spark.sql.adaptive.skewJoin.enabled", "true"
)
spark.conf.set(
    "spark.sql.adaptive.skewJoin.skewedPartitionFactor", "5"
)
spark.conf.set(
    "spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes",
    "256MB"
)

# 3. Optimize joins: sort-merge → broadcast if small table
spark.conf.set(
    "spark.sql.adaptive.localShuffleReader.enabled", "true"
)

# Diagnose skew: check partition sizes in Spark UI
df.rdd.getNumPartitions()
df.groupBy(spark_partition_id()).count().orderBy("count", ascending=False).show()''',
                  pills=[("AQE", "gold"), ("Skew Join", "gold"), ("Coalesce", "gold")])

        code_card("head-blue", "Broadcast Join vs Sort-Merge Join", "joins.py", "python",
                  '''\
from pyspark.sql.functions import broadcast

# ── Broadcast Join: small table fits in memory ──
# Threshold default: 10MB (spark.sql.autoBroadcastJoinThreshold)
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "50MB")

# Explicit broadcast hint
result = large_df.join(broadcast(small_df), "product_id")

# SQL broadcast hint
spark.sql("""
    SELECT /*+ BROADCAST(p) */ o.*, p.product_name
    FROM silver.orders o
    JOIN silver.products p ON o.product_id = p.product_id
""")

# ── Sort-Merge Join: both tables are large ──
# Best when both sides are partitioned on join key
spark.conf.set("spark.sql.join.preferSortMergeJoin", "true")

# Partition both tables on join key before writing
orders_df.repartition(200, "customer_id") \
         .write.format("delta").partitionBy("order_date") \
         .saveAsTable("silver.orders_partitioned")

# ── Shuffle Hash Join ──
spark.sql("""
    SELECT /*+ SHUFFLE_HASH(o) */ o.order_id, c.name
    FROM silver.orders o
    JOIN silver.customers c ON o.customer_id = c.customer_id
""")

# ── Disable broadcast to force SMJ ──
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")''',
                  pills=[("Broadcast", "blue"), ("Sort-Merge", "blue"), ("Join Hints", "blue")])

    with col2:
        code_card("head-teal", "EXPLAIN & Query Plan Reading", "explain.py", "python",
                  '''\
# ── Read Spark Query Plans ──

# Simple plan (parsed → analyzed → optimized → physical)
df.explain()

# Verbose with all 4 plan stages
df.explain(mode="extended")

# Cost-based optimizer plan
df.explain(mode="cost")

# Formatted (most readable)
df.explain(mode="formatted")

# SQL EXPLAIN
spark.sql("EXPLAIN FORMATTED SELECT * FROM silver.orders WHERE amount > 100")
spark.sql("EXPLAIN COST    SELECT * FROM silver.orders WHERE amount > 100")

# ── Interpret key plan nodes ──
# FileScan       → reading Delta files
# ColumnarToRow  → Photon optimization
# HashAggregate  → groupBy/agg
# SortMergeJoin  → large table join
# BroadcastHashJoin → small table join (good!)
# Exchange       → shuffle (expensive — minimize these!)
# Filter         → WHERE pushdown (good — happens early)

# ── Count stages in plan to spot shuffles ──
plan_str = df._jdf.queryExecution().toString()
shuffle_count = plan_str.count("Exchange")
print(f"Shuffle stages: {shuffle_count}")

# ── Cache intermediate result to avoid recompute ──
intermediate = spark.sql("SELECT ... expensive query ...")
intermediate.cache()
intermediate.count()  # materialize
# Now reuse intermediate multiple times cheaply''',
                  pills=[("EXPLAIN", "teal"), ("Query Plan", "teal"), ("Shuffle Count", "teal")])

        code_card("head-purple", "Bloom Filter Indexes & Photon", "bloom_photon.sql", "sql",
                  '''\
-- ── Bloom Filter Index: skip files on high-cardinality cols ──
-- Great for: UUIDs, emails, IDs in WHERE = ... queries

CREATE BLOOMFILTER INDEX ON TABLE silver.orders
FOR COLUMNS (order_id OPTIONS (fpp=0.1, numItems=50000000),
             customer_id OPTIONS (fpp=0.1));

-- Check if bloom filter is being used
EXPLAIN SELECT * FROM silver.orders
WHERE order_id = \'abc-123-xyz\';
-- Look for: PushedFilters in plan output

-- Drop bloom filter index
DROP BLOOMFILTER INDEX ON TABLE silver.orders;

-- ── Photon: Databricks vectorized query engine ──
-- Auto-enabled on Photon-enabled cluster types
-- Speeds up: scans, aggregations, joins, sort, Delta writes

-- Check if Photon is running (Spark UI → SQL tab)
-- Look for: ColumnarToRow, WholeStageCodegen nodes in plan

-- Photon-friendly operations (fully vectorized):
-- SELECT, WHERE, GROUP BY, ORDER BY, JOIN, WINDOW functions
-- COPY INTO, Delta MERGE, Delta OPTIMIZE

-- Operations NOT yet Photon-accelerated:
-- Python UDFs (use Pandas UDFs instead)
-- Complex nested struct operations

-- Use Pandas UDF for vectorized Python processing
from pyspark.sql.functions import pandas_udf
import pandas as pd

@pandas_udf("double")
def score_udf(amounts: pd.Series) -> pd.Series:
    return amounts * 1.15  # vectorized, Photon-compatible''',
                  pills=[("Bloom Filter", "purple"), ("Photon", "purple"), ("Pandas UDF", "purple")])

    st.markdown('<div class="sec-div">⚙️ Advanced Spark Query Tuning</div>',
                unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        code_card("head-teal", "Dynamic Partition Pruning (DPP)", "dpp.py", "python",
                  '''\
# ── Dynamic Partition Pruning (DPP) ──
# Spark 3+ auto-filters partitioned fact tables based on
# a dimension table's values — without scanning all partitions

# Enable (default: true in Spark 3+)
spark.conf.set("spark.sql.optimizer.dynamicPartitionPruning.enabled", "true")

# DPP works when:
# 1. Large fact table is partitioned on the join key
# 2. Small dimension table is joined and filtered
# 3. AQE is enabled

# Example: DPP kicks in automatically
result = (
    spark.table("gold.fact_sales")          # partitioned by region
    .join(
        spark.table("silver.dim_region")
             .filter(col("country") == "US"),  # dimension filter
        "region"
    )
)
# Spark pushes "country = US" filter onto fact_sales scan
# Only US partitions are read → massive I/O savings

result.explain()
# Look for: PartitionFilters: [dynamicpruningexpression(...)]

# Verify DPP is used (Spark UI → SQL tab → look for
# "DynamicPruning" in the query plan graph)

# Force disable for testing
spark.conf.set(
    "spark.sql.optimizer.dynamicPartitionPruning.enabled", "false"
)

# DPP + Delta data skipping = best combo for partitioned tables
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set(
    "spark.sql.optimizer.dynamicPartitionPruning.reuseBroadcastOnly",
    "false"   # allow DPP even without broadcast join
)''',
                  pills=[("DPP", "teal"), ("Partition Pruning", "teal"), ("Auto Filter", "teal")])

        code_card("head-gold", "Delta File Size & Write Tuning", "file_size_tuning.py", "python",
                  '''\
# ── Delta target file size tuning ──
# Default target: 104857600 (100 MB)
# Too small = too many files, slow reads
# Too large = slow writes, poor skipping granularity

# Set globally
spark.conf.set(
    "spark.databricks.delta.targetFileSize",
    str(128 * 1024 * 1024)   # 128 MB
)

# Set per-table via TBLPROPERTIES
spark.sql("""
    ALTER TABLE silver.events
    SET TBLPROPERTIES (
        'delta.targetFileSize' = '134217728'
    )
""")

# Tune max records per file (alternative)
spark.conf.set(
    "spark.databricks.delta.properties.defaults.dataSkippingNumIndexedCols",
    "32"
)

# Optimized writes: auto-coalesce small files before write
spark.conf.set(
    "spark.databricks.delta.optimizeWrite.enabled", "true"
)
spark.conf.set(
    "spark.databricks.delta.optimizeWrite.binSize",
    str(512 * 1024 * 1024)   # 512 MB bin size for coalescing
)

# Check current file sizes on a table
spark.sql("""
    SELECT
        COUNT(*)               AS num_files,
        SUM(size) / 1e9        AS total_gb,
        AVG(size) / 1e6        AS avg_file_mb,
        MIN(size) / 1e6        AS min_file_mb,
        MAX(size) / 1e6        AS max_file_mb
    FROM (DESCRIBE DETAIL silver.events)
    LATERAL VIEW explode(files) f AS file_info
""")

# Or via DeltaTable detail
from delta.tables import DeltaTable
DeltaTable.forName(spark, "silver.events").detail() \
    .select("numFiles", "sizeInBytes").show()''',
                  pills=[("File Size", "gold"), ("optimizeWrite", "gold"), ("Target Size", "gold")])

    with col2:
        code_card("head-bronze", "Speculative Execution & Stragglers", "speculative.py", "python",
                  '''\
# ── Speculative Execution: kill slow straggler tasks ──
# Spark launches duplicate of slow tasks and uses whichever finishes first

# Enable speculative execution
spark.conf.set("spark.speculation",          "true")
spark.conf.set("spark.speculation.interval", "100ms")   # check interval
spark.conf.set("spark.speculation.multiplier", "1.5")   # 1.5x slower = speculative
spark.conf.set("spark.speculation.quantile",   "0.75")  # 75% tasks done before checking
spark.conf.set("spark.speculation.minTaskRuntime", "60s")  # min runtime before flagging

# ── Task retry on failure ──
spark.conf.set("spark.task.maxFailures",      "4")    # retries per task
spark.conf.set("spark.stage.maxConsecutiveAttempts", "4")

# ── Blacklist bad executors automatically ──
spark.conf.set("spark.excludeOnFailure.enabled",             "true")
spark.conf.set("spark.excludeOnFailure.task.maxTaskFailures",  "2")
spark.conf.set("spark.excludeOnFailure.stage.maxFailedTasksPerExecutor", "2")

# ── Identify stragglers in Spark UI ──
# Stages tab → look for tasks with much longer duration than median
# Key metrics to compare: Duration, GC Time, Shuffle Read/Write

# Detect slow tasks programmatically
from pyspark.sql.functions import spark_partition_id, count
df.groupBy(spark_partition_id()) \
  .agg(count("*").alias("rows")) \
  .orderBy("rows", ascending=False) \
  .show(5)
# Partition with 10x more rows than others = skew straggler
# Fix: use salting or AQE skew join handling''',
                  pills=[("Speculative Exec", "bronze"), ("Stragglers", "bronze"), ("Task Retry", "bronze")])

        code_card("head-red", "Full Spark Optimization Cheat Config", "spark_opt_config.py", "python",
                  '''\
# ── Production-grade Spark optimization config ──
# Apply at cluster startup or notebook beginning

optimization_configs = {
    # ── AQE (Adaptive Query Execution) ──
    "spark.sql.adaptive.enabled":                          "true",
    "spark.sql.adaptive.coalescePartitions.enabled":       "true",
    "spark.sql.adaptive.skewJoin.enabled":                 "true",
    "spark.sql.adaptive.advisoryPartitionSizeInBytes":     "128MB",

    # ── Shuffle ──
    "spark.sql.shuffle.partitions":                        "400",

    # ── Join optimization ──
    "spark.sql.autoBroadcastJoinThreshold":                "50MB",
    "spark.sql.optimizer.dynamicPartitionPruning.enabled": "true",

    # ── Serialization ──
    "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
    "spark.kryo.unsafe": "true",

    # ── Memory ──
    "spark.memory.fraction":                               "0.8",
    "spark.memory.storageFraction":                        "0.3",
    "spark.memory.offHeap.enabled":                        "true",
    "spark.memory.offHeap.size":                           "4g",

    # ── Delta-specific ──
    "spark.databricks.delta.optimizeWrite.enabled":        "true",
    "spark.databricks.delta.autoCompact.enabled":          "true",
    "spark.databricks.delta.schema.autoMerge.enabled":     "false",
    "spark.databricks.delta.properties.defaults"
    ".enableDeletionVectors":                              "true",

    # ── Speculation ──
    "spark.speculation":                                   "true",
    "spark.speculation.multiplier":                        "2.0",
}

for k, v in optimization_configs.items():
    spark.conf.set(k, v)

print("✅ Optimization configs applied")''',
                  pills=[("Full Config", "red"), ("Production Ready", "red"), ("All-in-One", "red")])


# ════════════════════════════════════════════════════════
# 🔐 SECURITY & ACCESS CONTROL
# ════════════════════════════════════════════════════════
elif section == "🔐 Security & Access Control":

    col1, col2 = st.columns(2)
    with col1:
        code_card("head-red", "Unity Catalog GRANT / REVOKE", "grants.sql", "sql",
                  '''\
-- ── Grant privileges at every level ──

-- Catalog level
GRANT USE CATALOG, CREATE SCHEMA
    ON CATALOG prod TO `data-engineers@company.com`;

-- Schema level
GRANT USE SCHEMA, CREATE TABLE, CREATE VIEW, MODIFY
    ON SCHEMA prod.silver TO `data-engineers@company.com`;

GRANT USE SCHEMA, SELECT
    ON SCHEMA prod.gold TO `data-analysts@company.com`;

-- Table level
GRANT SELECT
    ON TABLE prod.gold.daily_revenue TO `reporting@company.com`;

GRANT SELECT, MODIFY
    ON TABLE prod.silver.events TO `etl-service-principal`;

-- View level (used for RLS)
GRANT SELECT
    ON VIEW prod.silver.orders_secure TO `data-analysts@company.com`;

-- Function / UDF
GRANT EXECUTE
    ON FUNCTION prod.security.mask_pii TO `data-engineers@company.com`;

-- External location / storage
GRANT READ FILES, WRITE FILES
    ON EXTERNAL LOCATION my_adls_location TO `etl-service-principal`;

-- Revoke access
REVOKE SELECT ON TABLE prod.gold.daily_revenue FROM `old-team@company.com`;

-- Show what a user can access
SHOW GRANTS ON TABLE prod.silver.events;
SHOW GRANTS ON SCHEMA prod.silver;
SHOW GRANTS ON CATALOG prod;

-- What can current user access?
SHOW GRANTS TO `me@company.com`;''',
                  pills=[("GRANT", "red"), ("REVOKE", "red"), ("Unity Catalog", "red")])

        code_card("head-blue", "Secrets Management", "secrets.py", "python",
                  '''\
# ── Databricks Secrets + Azure Key Vault ──

# CLI: create secret scope backed by Azure Key Vault
# databricks secrets create-scope \\
#   --scope kv-prod \\
#   --scope-backend-type AZURE_KEYVAULT \\
#   --resource-id /subscriptions/.../vaults/my-kv \\
#   --dns-name https://my-kv.vault.azure.net/

# CLI: create Databricks-backed scope
# databricks secrets create-scope --scope my-scope

# CLI: add secrets to Databricks scope
# databricks secrets put --scope my-scope --key db-password
# databricks secrets put --scope my-scope --key api-token

# ── Use secrets in notebooks ──
db_password  = dbutils.secrets.get(scope="kv-prod", key="db-password")
api_token    = dbutils.secrets.get(scope="kv-prod", key="api-token")
storage_key  = dbutils.secrets.get(scope="kv-prod", key="adls-key")

# Mount ADLS Gen2 using service principal
configs = {
    "fs.azure.account.auth.type": "OAuth",
    "fs.azure.account.oauth.provider.type":
        "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
    "fs.azure.account.oauth2.client.id":
        dbutils.secrets.get("kv-prod", "sp-client-id"),
    "fs.azure.account.oauth2.client.secret":
        dbutils.secrets.get("kv-prod", "sp-client-secret"),
    "fs.azure.account.oauth2.client.endpoint":
        f"https://login.microsoftonline.com/{dbutils.secrets.get('kv-prod','tenant-id')}/oauth2/token"
}

dbutils.fs.mount(
    source="abfss://silver@storageacct.dfs.core.windows.net/",
    mount_point="/mnt/silver",
    extra_configs=configs
)''',
                  pills=[("Secrets", "blue"), ("Key Vault", "blue"), ("Service Principal", "blue")])

    with col2:
        code_card("head-purple", "Audit Logging — System Tables", "audit.sql", "sql",
                  '''\
-- ── Unity Catalog System Tables for Audit & Governance ──

-- Who accessed which tables?
SELECT
    user_identity.email          AS user,
    action_name,
    request_params.full_name_arg AS table_name,
    response.status_code,
    event_time
FROM system.access.audit
WHERE action_name IN (\'getTable\',\'createTable\',\'deleteTable\')
  AND event_time >= CURRENT_TIMESTAMP - INTERVAL 7 DAYS
ORDER BY event_time DESC;

-- Failed access attempts (possible security incidents)
SELECT
    user_identity.email,
    action_name,
    request_params,
    response.error_message,
    event_time
FROM system.access.audit
WHERE response.status_code != 200
  AND event_time >= CURRENT_TIMESTAMP - INTERVAL 1 DAY
ORDER BY event_time DESC;

-- Cluster usage & cost attribution
SELECT
    workspace_id,
    cluster_id,
    owned_by,
    SUM(dbu) AS total_dbu,
    SUM(cost_usd) AS total_cost_usd
FROM system.billing.usage
WHERE usage_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY 1, 2, 3
ORDER BY total_cost_usd DESC;

-- Data access patterns (which tables are popular?)
SELECT
    request_params.full_name_arg AS table_name,
    COUNT(DISTINCT user_identity.email) AS unique_users,
    COUNT(*) AS total_accesses
FROM system.access.audit
WHERE action_name = \'getTable\'
GROUP BY 1 ORDER BY total_accesses DESC LIMIT 20;''',
                  pills=[("Audit Log", "purple"), ("system.access", "purple"), ("Compliance", "purple")])

        code_card("head-teal", "Network Security & IP Access Lists", "network.py", "python",
                  '''\
# ── Configure IP Access Lists (Databricks REST API) ──
import requests

TOKEN   = dbutils.secrets.get("kv", "admin-pat")
HOST    = "https://<workspace>.azuredatabricks.net"
HEADERS = {"Authorization": f"Bearer {TOKEN}",
           "Content-Type":  "application/json"}

# Create IP access list (allowlist)
resp = requests.post(
    f"{HOST}/api/2.0/ip-access-lists",
    headers=HEADERS,
    json={
        "label":       "corporate-vpn",
        "list_type":   "ALLOW",
        "ip_addresses": [
            "10.0.0.0/8",
            "203.0.113.0/24"
        ],
        "enabled": True
    }
)

# List all access lists
resp = requests.get(f"{HOST}/api/2.0/ip-access-lists", headers=HEADERS)
for acl in resp.json().get("ip_access_lists", []):
    print(f"{acl[\'label\']}: {acl[\'list_type\']} — {acl[\'ip_addresses\']}")

# ── Private Link setup (Azure) ──
# Done via Terraform / Azure Portal:
# 1. Create Private Endpoint for Databricks workspace
# 2. Configure DNS: workspace.azuredatabricks.net → private IP
# 3. Enable "No Public IP" (NPIP) on cluster config
# 4. Set workspace setting: enableIpAccessLists = true

# ── Cluster network isolation ──
spark.conf.set(
    "spark.databricks.pyspark.enablePy4JSecurity", "true"
)''',
                  pills=[("IP Access Lists", "teal"), ("Private Link", "teal"), ("NPIP", "teal")])


# ════════════════════════════════════════════════════════
# 📦 DEV & MLOPS
# ════════════════════════════════════════════════════════
elif section == "📦 Dev & MLOps":

    col1, col2 = st.columns(2)
    with col1:
        code_card("head-bronze", "%run vs dbutils.notebook.run()", "notebook_patterns.py", "python",
                  '''\
# ── %run: executes notebook inline (shares session) ──
# Use when you need shared variables / functions

# In a Databricks notebook cell:
# %run ./common/utils
# %run /Repos/prod/pipelines/helpers
# %run ../config/env_config $env="prod"

# After %run, all variables/functions are available:
# result_df = transform_events(raw_df)  # defined in utils

# ── dbutils.notebook.run(): isolated subprocess ──
# Use for parallel tasks or when isolation is needed

result_json = dbutils.notebook.run(
    path              = "/Repos/prod/pipelines/01_bronze",
    timeout_seconds   = 3600,
    arguments         = {
        "env":         "prod",
        "run_date":    "2024-01-15",
        "table_name":  "events"
    }
)

import json
result = json.loads(result_json)
print(f"Status: {result[\'status\']}, Rows: {result[\'rows_processed\']}")

# Parallel notebook execution
from concurrent.futures import ThreadPoolExecutor

tables = ["orders", "customers", "products"]

def process_table(table):
    return dbutils.notebook.run(
        "/Repos/prod/pipelines/silver_generic",
        timeout_seconds=1800,
        arguments={"table": table}
    )

with ThreadPoolExecutor(max_workers=3) as ex:
    futures = {ex.submit(process_table, t): t for t in tables}

# Exit current notebook with value
dbutils.notebook.exit(json.dumps({"status": "success", "rows": 9999}))''',
                  pills=[("%run", "orange"), ("dbutils.notebook", "orange"), ("Parallel Exec", "orange")])

        code_card("head-blue", "MLflow Experiment Tracking", "mlflow_tracking.py", "python",
                  '''\
import mlflow
import mlflow.spark
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator

# ── Set experiment (creates if not exists) ──
mlflow.set_experiment("/Repos/prod/ml/revenue_forecast")

with mlflow.start_run(run_name="rf_v2_tuned") as run:
    # Log parameters
    mlflow.log_param("num_trees",       200)
    mlflow.log_param("max_depth",       8)
    mlflow.log_param("feature_cols",    ["day_of_week","region","product_id"])
    mlflow.log_param("training_data",   "prod.gold.daily_revenue")

    # Train model
    rf = RandomForestRegressor(numTrees=200, maxDepth=8,
                               featuresCol="features",
                               labelCol="revenue")
    model = rf.fit(train_df)
    predictions = model.transform(test_df)

    # Log metrics
    evaluator = RegressionEvaluator(labelCol="revenue",
                                    metricName="rmse")
    rmse = evaluator.evaluate(predictions)
    r2   = RegressionEvaluator(labelCol="revenue",
                               metricName="r2").evaluate(predictions)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2",   r2)

    # Log model
    mlflow.spark.log_model(model, "random_forest_revenue",
                           registered_model_name="revenue_forecast_model")

    # Log artifact (feature importance chart)
    mlflow.log_artifact("feature_importance.png")

    print(f"Run ID: {run.info.run_id} | RMSE: {rmse:.4f}")''',
                  pills=[("MLflow", "blue"), ("Experiment", "blue"), ("Model Registry", "blue")])

    with col2:
        code_card("head-green", "Feature Store Read & Write", "feature_store.py", "python",
                  '''\
from databricks.feature_store import FeatureStoreClient
from databricks.feature_engineering import FeatureEngineeringClient

fs = FeatureStoreClient()
fe = FeatureEngineeringClient()

# ── Create & write feature table ──
feature_df = spark.table("silver.events") \
    .groupBy("customer_id") \
    .agg(
        avg("amount").alias("avg_order_value"),
        count("*").alias("order_count_30d"),
        max("event_ts").alias("last_activity_ts")
    )

fs.create_table(
    name        = "prod.features.customer_features",
    primary_keys= ["customer_id"],
    df          = feature_df,
    description = "Customer-level aggregated features (30d window)"
)

fs.write_table(
    name = "prod.features.customer_features",
    df   = feature_df,
    mode = "merge"       # or "overwrite"
)

# ── Read features for training ──
training_set = fe.create_training_set(
    df               = labels_df,   # label DataFrame
    feature_lookups  = [
        FeatureLookup(
            table_name   = "prod.features.customer_features",
            feature_names= ["avg_order_value","order_count_30d"],
            lookup_key   = "customer_id"
        )
    ],
    label            = "churned",
    exclude_columns  = ["customer_id"]
)

training_df = training_set.load_df()

# ── Log model with feature store metadata ──
fe.log_model(
    model             = trained_model,
    artifact_path     = "churn_model",
    flavor            = mlflow.sklearn,
    training_set      = training_set,
    registered_model_name = "churn_prediction_model"
)''',
                  pills=[("Feature Store", "green"), ("FeatureLookup", "green"), ("Training Set", "green")])

        code_card("head-teal", "Git Repos & CI/CD Integration", "git_cicd.py", "python",
                  '''\
# ── Databricks Repos: Git-backed notebooks ──

# CLI: clone a repo into Databricks workspace
# databricks repos create \\
#   --url https://github.com/org/etl-pipeline \\
#   --provider gitHub

# Pull latest changes
# databricks repos update --repo-id <id> --branch main

# ── CI/CD Pipeline (GitHub Actions example) ──
# .github/workflows/deploy.yml:
#
# - name: Deploy to Databricks
#   run: |
#     pip install databricks-cli
#     databricks bundle deploy --target prod
#   env:
#     DATABRICKS_HOST: ${{ secrets.DB_HOST }}
#     DATABRICKS_TOKEN: ${{ secrets.DB_TOKEN }}

# ── Run tests in CI using pytest + nutter ──
# pip install nutter
# nutter run "/Repos/prod/tests/test_silver_transform" <cluster-id>

# ── Python wheel task (production-grade) ──
# 1. Package your ETL as a Python wheel
# setup.py or pyproject.toml → python setup.py bdist_wheel
# 2. Upload to DBFS or Unity Catalog Volumes
# databricks fs cp dist/etl_pipeline-1.0-py3-none-any.whl dbfs:/mnt/wheels/

# ── Unity Catalog Volumes (preferred over DBFS) ──
spark.sql("CREATE VOLUME IF NOT EXISTS prod.etl.wheels")
dbutils.fs.cp(
    "file:/local/dist/etl-1.0-py3-none-any.whl",
    "/Volumes/prod/etl/wheels/"
)

# Install from Volume in cluster init script
# pip install /Volumes/prod/etl/wheels/etl-1.0-py3-none-any.whl''',
                  pills=[("Git Repos", "teal"), ("CI/CD", "teal"), ("Python Wheel", "teal")])


# ════════════════════════════════════════════════════════
# 🛠️ MONITORING & OBSERVABILITY
# ════════════════════════════════════════════════════════
elif section == "🛠️ Monitoring & Observability":

    col1, col2 = st.columns(2)
    with col1:
        code_card("head-teal", "System Tables — Billing & Usage", "system_tables.sql", "sql",
                  '''\
-- ── system.billing.usage — Cost Attribution ──
SELECT
    usage_date,
    workspace_id,
    sku_name,
    billing_origin_product,
    SUM(usage_quantity)   AS total_dbu,
    SUM(usage_quantity * list_price.default) AS est_cost_usd
FROM system.billing.usage
LEFT JOIN system.billing.list_prices USING (sku_name)
WHERE usage_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY 1,2,3,4
ORDER BY est_cost_usd DESC;

-- ── Top cost drivers by cluster ──
SELECT
    custom_tags.team           AS team,
    custom_tags.project        AS project,
    SUM(usage_quantity)        AS dbu,
    COUNT(DISTINCT cluster_id) AS clusters
FROM system.billing.usage,
     LATERAL VIEW explode(custom_tags) t AS tag_key, tag_val
WHERE usage_date >= CURRENT_DATE - INTERVAL 7 DAYS
GROUP BY 1, 2 ORDER BY dbu DESC LIMIT 20;

-- ── system.compute.clusters — Cluster inventory ──
SELECT
    cluster_id, cluster_name, owned_by,
    cluster_source, state,
    spark_version, node_type_id,
    num_workers, autoscale,
    created_by, created_at
FROM system.compute.clusters
WHERE state = \'RUNNING\'
ORDER BY created_at DESC;

-- ── system.compute.node_types ──
SELECT node_type_id, num_cores, memory_mb, instance_type_id
FROM system.compute.node_types
ORDER BY memory_mb DESC;''',
                  pills=[("system.billing", "teal"), ("Cost Attribution", "teal"), ("DBU Tracking", "teal")])

        code_card("head-gold", "Query History & Query Profile", "query_history.sql", "sql",
                  '''\
-- ── Query History via system tables ──
SELECT
    statement_id,
    executed_by,
    statement_text,
    status,
    execution_end_time - execution_start_time AS duration,
    total_task_duration_ms,
    rows_produced,
    read_bytes,
    spill_bytes
FROM system.query.history
WHERE executed_by        = current_user()
  AND execution_start_time >= CURRENT_TIMESTAMP - INTERVAL 24 HOURS
  AND status != \'FINISHED\'   -- slow/failed queries
ORDER BY total_task_duration_ms DESC
LIMIT 50;

-- ── Find expensive queries (last 7 days) ──
SELECT
    executed_by,
    LEFT(statement_text, 100) AS query_preview,
    total_task_duration_ms / 1000 AS duration_sec,
    spill_bytes / 1e9              AS spill_gb,
    read_bytes  / 1e9              AS read_gb
FROM system.query.history
WHERE execution_start_time >= CURRENT_TIMESTAMP - INTERVAL 7 DAYS
  AND status = \'FINISHED\'
ORDER BY total_task_duration_ms DESC
LIMIT 20;

-- ── Tables with most reads ──
SELECT
    t.table_name,
    COUNT(*)                    AS query_count,
    SUM(q.read_bytes) / 1e9     AS total_read_gb
FROM system.query.history q
JOIN system.access.table_lineage t
    ON q.statement_id = t.source_statement_id
GROUP BY 1 ORDER BY query_count DESC LIMIT 20;''',
                  pills=[("Query History", "gold"), ("Slow Queries", "gold"), ("Spill Detection", "gold")])

    with col2:
        code_card("head-purple", "Spark UI — Key Metrics to Monitor", "spark_ui_tips.py", "python",
                  '''\
# ── Spark UI Monitoring: what to look for ──

# 1. Jobs tab: identify slow/failed stages
# 2. Stages tab: find stages with high shuffle read/write
# 3. Storage tab: check cached RDD/DataFrame sizes
# 4. Executors tab: spot GC issues (GC Time > 5% = problem)
# 5. SQL tab: visual query plan with timing per node

# ── Programmatic Spark metrics ──
sc = spark.sparkContext

# Application ID (use in Spark UI URL)
print(f"App ID: {sc.applicationId}")
print(f"App Name: {sc.appName}")

# Executor memory info
for executor in sc.statusTracker().getExecutorInfos():
    print(f"Executor {executor.executorId}: "
          f"host={executor.host}, "
          f"totalCores={executor.totalCores}")

# ── Listener to capture stage metrics ──
from pyspark import SparkContext

class StageMetricsListener:
    def onStageCompleted(self, stageCompleted):
        info = stageCompleted.stageInfo()
        metrics = info.taskMetrics()
        print(f"Stage {info.stageId()} completed: "
              f"shuffle_read={metrics.shuffleReadMetrics().totalBytesRead() / 1e6:.1f}MB, "
              f"shuffle_write={metrics.shuffleWriteMetrics().bytesWritten() / 1e6:.1f}MB, "
              f"spill={metrics.memoryBytesSpilled() / 1e6:.1f}MB")

# ── Check for data skew in a DataFrame ──
from pyspark.sql.functions import spark_partition_id, count

df.groupBy(spark_partition_id().alias("partition")) \
  .agg(count("*").alias("rows")) \
  .orderBy("rows", ascending=False) \
  .show(20)
# If max partition >> avg partition → you have skew!''',
                  pills=[("Spark UI", "purple"), ("Stage Metrics", "purple"), ("Skew Detection", "purple")])

        code_card("head-green", "Cluster Event Logs & Alerts", "cluster_monitoring.py", "python",
                  '''\
# ── Monitor cluster events via REST API ──
import requests

TOKEN   = dbutils.secrets.get("kv", "databricks-pat")
HOST    = "https://<workspace>.azuredatabricks.net"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Get cluster event history
resp = requests.get(
    f"{HOST}/api/2.0/clusters/events",
    headers=HEADERS,
    json={
        "cluster_id":  "<cluster-id>",
        "limit":       50,
        "event_types": ["AUTOSCALING_STATS_REPORT",
                        "NODES_LOST",
                        "DRIVER_HEALTHY",
                        "SPARK_EXCEPTION"]
    }
)

for event in resp.json().get("events", []):
    print(f"{event[\'timestamp\']} | {event[\'type\']} | {event.get(\'details\',\'\')}")

# ── Custom job alerting (webhook notification) ──
job_run_config = {
    "tasks": [...],
    "email_notifications": {
        "on_failure": ["data-eng-alerts@company.com"],
        "on_success": [],
        "no_alert_for_skipped_runs": True
    },
    "webhook_notifications": {
        "on_failure": [{"id": "<webhook-id>"}],  # Slack/Teams
        "on_start":   [{"id": "<webhook-id>"}]
    },
    "health": {
        "rules": [{
            "metric": "RUN_DURATION_SECONDS",
            "op": "GREATER_THAN",
            "value": 3600      # alert if job > 1 hour
        }]
    }
}

# ── Log custom metrics from notebook ──
import mlflow
mlflow.log_metric("rows_processed",    1_234_567)
mlflow.log_metric("bad_rows_dropped",  42)
mlflow.log_metric("pipeline_duration", 187.4)''',
                  pills=[("Cluster Events", "green"), ("Webhook Alerts", "green"), ("Custom Metrics", "green")])


# ════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<div style='text-align:center;font-size:0.7rem;color:#8b949e;font-family:JetBrains Mono,monospace;padding:12px 0;'>
🔺 Delta Lake Cheat Sheet &nbsp;·&nbsp; Databricks + Apache Spark + Medallion Architecture &nbsp;·&nbsp; Built with Streamlit
&nbsp;|&nbsp; 17 Sections · 60+ Professional Snippets
</div>
""", unsafe_allow_html=True)

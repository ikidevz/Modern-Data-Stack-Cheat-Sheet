import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AWS Data Engineering Cheat Sheet v2",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

SECTIONS = [
    "🏠 Home",
    "🪣 Storage – S3, Lake Formation, Glue Catalog",
    "📥 Ingestion – Kinesis, MSK, Glue, DMS, AppFlow",
    "⚙️ Processing – Glue, EMR, Redshift, Athena, Lambda",
    "🏗️ Architectures – Lake, Warehouse, Lakehouse, Mesh",
    "🎼 Orchestration – MWAA, Step Functions, EventBridge",
    "🔒 Governance, Security & Quality",
    "📊 Analytics & BI – QuickSight, OpenSearch, SageMaker",
    "🔄 dbt on AWS",
    "⚖️ Comparisons",
    "🏗️ IaC – Terraform Modules",
    "🚀 Modern Patterns",
    "🐛 Debugging & Troubleshooting",
    "📐 Data Modeling Patterns",
    "💰 Cost Optimization",
    "📋 Quick Reference – CLI & SQL Snippets",
    "🧬 Master DE Pipelines – ETL/ELT, DWH, Lake, Lakehouse (Kappa)",
]

st.sidebar.title("☁️ AWS Data Eng v2")
st.sidebar.markdown("**Expanded Cheat Sheet**")
section = st.sidebar.radio("Navigate", SECTIONS, label_visibility="collapsed")
st.sidebar.markdown("---")
st.sidebar.caption("S3 · Glue · EMR · Redshift · Kinesis · MSK · DMS · Athena · MWAA · Lake Formation · Step Functions · EventBridge · AppFlow · QuickSight · OpenSearch · SageMaker · dbt · Terraform")


def hcl(s):  st.code(s.strip(), language="hcl")
def py(s):   st.code(s.strip(), language="python")
def sql(s):  st.code(s.strip(), language="sql")
def bash(s): st.code(s.strip(), language="bash")
def tip(t):  st.success(f"💡 **Tip:** {t}")
def warn(t): st.warning(f"⚠️ **Pitfall:** {t}")
def info(t): st.info(f"ℹ️ {t}")
def err(t):  st.error(f"🚫 **Never:** {t}")


# ════════════════════════════════════════════════════════════════════════════
# HOME
# ════════════════════════════════════════════════════════════════════════════
if section == "🏠 Home":
    st.title("☁️ AWS Data Engineering – Expanded Cheat Sheet v2")
    st.markdown("> **Comprehensive, opinionated reference** for data engineers building on AWS. Covers storage, ingestion, processing, architectures, orchestration, governance, analytics, dbt, IaC, debugging, data modeling, and cost.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Sections", "16")
    c2.metric("Services Covered", "25+")
    c3.metric("Terraform Snippets", "20+")
    c4.metric("New vs v1", "+6 sections")

    st.markdown("---")
    st.subheader("🆕 New in v2")
    news = {
        "📊 Analytics & BI": "QuickSight (SPICE, RLS, ML Insights), OpenSearch, SageMaker Feature Store & Processing",
        "🔄 dbt on AWS": "dbt Core vs Cloud, adapters (Redshift/Athena/Glue), models/macros/tests, dbt + Iceberg, CI/CD patterns",
        "🐛 Debugging & Troubleshooting": "Glue, EMR, Redshift, Kinesis, Athena failure patterns with solutions",
        "📐 Data Modeling": "Star/Snowflake/OBT, Medallion, Data Vault 2.0, Anchor Modeling on AWS",
        "📋 Quick Reference": "CLI one-liners, SQL snippets, Boto3 patterns, Spark configs cheat sheet",
        "🏗️ Expanded AppFlow": "SaaS ingestion (Salesforce, SAP, ServiceNow) → S3/Redshift",
    }
    for k, v in news.items():
        st.markdown(f"**{k}** — {v}")

    st.markdown("---")
    st.subheader("📚 All sections")
    all_topics = {
        "🪣 Storage": "S3 lifecycle/encryption/OTF, Lake Formation TBAC, Glue Catalog, S3 Access Points",
        "📥 Ingestion": "Kinesis family, MSK, Glue JDBC, DMS (CDC), AppFlow (SaaS)",
        "⚙️ Processing": "Glue (batch+streaming+Ray), EMR (EC2/EKS/Serverless), Redshift, Athena v3, Lambda+SFN",
        "🏗️ Architectures": "Data Lake, Warehouse, Lakehouse, Data Mart, Data Mesh, Kappa/Lambda patterns",
        "🎼 Orchestration": "MWAA Airflow, Step Functions (Express+Standard), EventBridge Pipes, Scheduler",
        "🔒 Governance": "Lake Formation, Glue DQ (DQDL), Macie, SCPs, encryption strategies, audit",
        "📊 Analytics & BI": "QuickSight SPICE+RLS, OpenSearch ingestion, SageMaker Feature Store",
        "🔄 dbt on AWS": "Adapters, model materializations, Iceberg support, CI/CD, testing",
        "⚖️ Comparisons": "Lake vs WH vs Lakehouse, Glue vs EMR, KDS vs MSK, MWAA vs SFN, Batch vs Stream",
        "🏗️ IaC": "Full Terraform modules: S3+Glue+Redshift+Kinesis+MWAA+dbt runner",
        "🚀 Modern Patterns": "Zero-ETL, S3 Tables, Streaming Lakehouse, Federated Query, Data Sharing",
        "🐛 Debugging": "Glue/EMR/Redshift/Athena/Kinesis common errors + fixes",
        "📐 Data Modeling": "Star, Snowflake, OBT, Medallion, Data Vault 2.0 on Redshift/Iceberg",
        "💰 Cost": "S3 tiers, Glue DPU tuning, Redshift reserved/serverless, Athena query optimization",
        "📋 Quick Reference": "CLI, SQL, Boto3, PySpark configs — copy-paste ready",
    }
    for k, v in all_topics.items():
        st.markdown(f"**{k}** — {v}")

# ════════════════════════════════════════════════════════════════════════════
# STORAGE
# ════════════════════════════════════════════════════════════════════════════
elif section == "🪣 Storage – S3, Lake Formation, Glue Catalog":
    st.title("🪣 Storage")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Amazon S3", "Open Table Formats", "Lake Formation", "Glue Catalog", "S3 Access Points"])

    with tab1:
        st.header("Amazon S3 – Deep Dive")
        st.subheader("Storage Classes")
        df = pd.DataFrame({
            "Class":              ["Standard", "Intelligent-Tiering", "Standard-IA", "One Zone-IA", "Glacier Instant", "Glacier Flexible", "Deep Archive"],
            "$/GB/mo":            ["$0.023", "$0.023+monitoring", "$0.0125", "$0.01", "$0.004", "$0.0036", "$0.00099"],
            "Retrieval latency":  ["ms", "ms (auto-tier)", "ms", "ms", "ms", "min–hrs", "hrs"],
            "Min storage days":   ["—", "—", "30", "30", "90", "90", "180"],
            "Min object size fee": ["—", "—", "128 KB", "128 KB", "128 KB", "40 KB", "40 KB"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("S3 Consistency Model")
        st.markdown("""
- **Strong read-after-write consistency** (since Dec 2020) for all PUTs and DELETEs  
- **Eventual consistency** for bucket policy / ACL propagation  
- **LIST operations** reflect all PUTs eventually — avoid listing immediately after batch writes in time-critical pipelines  
        """)

        st.subheader("S3 Performance Tuning")
        st.markdown("""
| Technique | When to use | Impact |
|-----------|------------|--------|
| **Multipart upload** | Objects > 100 MB | Parallelises upload, required > 5 GB |
| **Transfer Acceleration** | Cross-continent uploads | Up to 60% faster via CloudFront edge |
| **Byte-range fetch** | Large file partial reads | Parallel downloads + retry resilience |
| **S3 Select** | Filter single object | Reduce data transferred by up to 80% |
| **Prefix sharding** | > 5,500 req/s per prefix | Scale to millions req/s with different prefixes |
| **Request Payer** | Cross-account data consumers | Charge requester not bucket owner |
        """)

        st.subheader("Terraform – Complete S3 Lake Bucket")
        hcl("""
resource "aws_s3_bucket" "lake" {
  bucket = "${var.project}-lake-${var.env}"
  tags   = local.tags
}

# Block all public access
resource "aws_s3_bucket_public_access_block" "lake" {
  bucket                  = aws_s3_bucket.lake.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# KMS encryption with Bucket Key (reduces KMS API calls 99%)
resource "aws_s3_bucket_server_side_encryption_configuration" "lake" {
  bucket = aws_s3_bucket.lake.id
  rule {
    bucket_key_enabled = true
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.lake.arn
    }
  }
}

# Versioning
resource "aws_s3_bucket_versioning" "lake" {
  bucket = aws_s3_bucket.lake.id
  versioning_configuration { status = "Enabled" }
}

# Object lock for compliance zones (WORM)
resource "aws_s3_bucket_object_lock_configuration" "lake" {
  bucket = aws_s3_bucket.lake.id
  rule {
    default_retention { mode = "GOVERNANCE"; days = 365 }
  }
}

# Lifecycle tiers
resource "aws_s3_bucket_lifecycle_configuration" "lake" {
  bucket = aws_s3_bucket.lake.id
  rule {
    id = "raw-zone-tiering"; status = "Enabled"
    filter { prefix = "raw/" }
    transition { days = 30;  storage_class = "STANDARD_IA" }
    transition { days = 90;  storage_class = "GLACIER_IR"  }
    transition { days = 365; storage_class = "DEEP_ARCHIVE"}
    noncurrent_version_expiration { noncurrent_days = 90 }
  }
  rule {
    id = "delete-incomplete-multipart"; status = "Enabled"
    filter {}
    abort_incomplete_multipart_upload { days_after_initiation = 7 }
  }
}

# S3 Replication to DR region
resource "aws_s3_bucket_replication_configuration" "lake" {
  bucket = aws_s3_bucket.lake.id
  role   = aws_iam_role.replication.arn
  rule {
    id = "replicate-curated"; status = "Enabled"
    filter { prefix = "curated/" }
    destination {
      bucket        = aws_s3_bucket.lake_dr.arn
      storage_class = "STANDARD_IA"
    }
  }
}
        """)
        tip("Always enable `abort_incomplete_multipart_upload` — zombie multipart uploads silently accumulate cost.")
        warn("S3 Object Lock in COMPLIANCE mode cannot be removed even by root — use GOVERNANCE mode for testing.")

    with tab2:
        st.header("Open Table Formats on S3")
        df = pd.DataFrame({
            "Feature":             ["ACID transactions", "Time travel", "Schema evolution", "Hidden partitioning", "Partition evolution", "Row-level deletes", "CDC / MERGE", "Concurrent writers", "AWS native support", "Best for"],
            "Apache Iceberg":      ["✅", "✅ (snapshots)", "✅ Full", "✅", "✅", "✅", "✅ MERGE INTO", "Optimistic CC", "⭐⭐⭐ (Athena, Glue, EMR, Redshift)", "General purpose lakehouse"],
            "Apache Hudi":         ["✅", "✅ (commits)", "✅ Partial", "❌", "Limited", "✅ (MoR)", "✅ Upsert-first", "Limited", "⭐⭐ (EMR, Glue)", "CDC-heavy upserts"],
            "Delta Lake":          ["✅", "✅ (versions)", "✅ Full", "❌", "❌", "✅", "✅ MERGE", "Optimistic CC", "⭐ (EMR, Glue partial)", "Databricks-origin shops"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("Iceberg Table Properties Cheat Sheet")
        hcl("""
-- Key Iceberg table properties (set in Glue Catalog or CREATE TABLE)
'write.format.default'               = 'parquet'
'write.parquet.compression-codec'    = 'snappy'
'write.target-file-size-bytes'       = '134217728'   -- 128 MB target
'write.distribution-mode'            = 'hash'        -- hash | range | none
'write.merge.mode'                   = 'merge-on-read'  -- or copy-on-write

-- Partitioning (hidden – no partition cols in queries!)
PARTITIONED BY (days(event_ts), bucket(16, user_id))

-- Maintenance
'history.expire.min-snapshots-to-keep' = '5'
'history.expire.max-snapshot-age-ms'   = '604800000'  -- 7 days

-- Sorting (improves read performance)
SORTED BY (user_id, event_ts)
        """, "sql")

        st.subheader("Hudi Table Types")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Copy-on-Write (CoW)**")
            st.markdown("""
- Rewrites entire Parquet file on update  
- ✅ Fast reads  
- ❌ Slow writes (heavy I/O)  
- Best: Read-heavy, batch analytics  
            """)
        with col2:
            st.markdown("**Merge-on-Read (MoR)**")
            st.markdown("""
- Appends delta logs, merges on read  
- ✅ Fast writes  
- ❌ Slightly slower reads (merge overhead)  
- Best: High-frequency CDC, near-real-time  
            """)

        tip("Prefer **Iceberg** for new projects — best native AWS support and the most active open-source community.")

    with tab3:
        st.header("AWS Lake Formation")
        st.subheader("Permission Model")
        st.markdown("""
```
IAM (coarse) → Lake Formation (fine-grained) → Glue Catalog → S3 data
```
Lake Formation sits between IAM and the data. IAM controls service access; Lake Formation controls *data* access.
        """)
        df = pd.DataFrame({
            "Grant Type":        ["Database", "Table", "Column", "Row filter", "Tag (LF-TBAC)"],
            "Granularity":       ["DB-level", "All columns", "Specific columns", "Expression-filtered rows", "Policy-tag-based"],
            "Scale":             ["Low", "Medium", "Medium", "Medium", "⭐ High (100s of tables)"],
            "Use case":          ["Env isolation", "Team access", "PII masking", "Tenant isolation", "Enterprise governance"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("LF-TBAC (Tag-Based Access Control)")
        hcl("""
# Define LF tags
resource "aws_lakeformation_lf_tag" "sensitivity" {
  key    = "sensitivity"
  values = ["public", "internal", "confidential", "restricted"]
}

resource "aws_lakeformation_lf_tag" "domain" {
  key    = "domain"
  values = ["finance", "marketing", "engineering", "hr"]
}

# Assign tags to database
resource "aws_lakeformation_resource_lf_tags" "curated_db" {
  database { name = "curated" }
  lf_tag { key = "sensitivity"; value = "internal" }
  lf_tag { key = "domain";      value = "finance"  }
}

# Grant based on tags (scales to all matching resources automatically)
resource "aws_lakeformation_tag_based_policy" "finance_analysts" {
  principal   = aws_iam_role.finance_analyst.arn
  permissions = ["SELECT"]
  lf_tag_policy {
    resource_type = "TABLE"
    expression {
      key    = "domain"
      values = ["finance"]
    }
    expression {
      key    = "sensitivity"
      values = ["public", "internal"]
    }
  }
}
        """)
        warn("Mixing IAM-based and LF-based access control causes unpredictable permission behavior — migrate fully to LF.")
        tip("Use LF Governed Tables (Iceberg-backed) for automatic compaction, snapshots, and row-level transactions managed by AWS.")

    with tab4:
        st.header("Glue Data Catalog")
        st.subheader("Catalog Hierarchy")
        st.markdown("""
```
Account → Catalog → Database → Table → Partition
                             → Connection
                             → Classifier
                   → Crawler  (auto-populates above)
```
        """)
        st.subheader("Schema Registry (Avro/JSON/Protobuf)")
        st.markdown(
            "Use Glue Schema Registry to enforce schemas on Kinesis/MSK streams — prevents schema drift from breaking downstream consumers.")
        hcl("""
resource "aws_glue_registry" "events" {
  registry_name = "event-schemas"
  description   = "Centralised schema registry for streaming events"
}

resource "aws_glue_schema" "user_event" {
  schema_name       = "UserEvent"
  registry_arn      = aws_glue_registry.events.arn
  data_format       = "AVRO"
  compatibility     = "BACKWARD"   # new schema must read old data
  schema_definition = jsonencode({
    type   = "record"
    name   = "UserEvent"
    fields = [
      { name = "event_id",  type = "string"  },
      { name = "user_id",   type = "string"  },
      { name = "event_ts",  type = "long",   logicalType = "timestamp-millis" },
      { name = "event_type",type = "string"  },
      { name = "payload",   type = ["null","string"], default = "null" }
    ]
  })
}
        """)
        tip("Set `compatibility = BACKWARD` for Kafka/Kinesis — allows consumers on old schema to read new messages.")
        warn("Glue Crawlers can misdetect column types from CSV (e.g., leading-zero strings as longs). Define schemas manually for sensitive tables.")

    with tab5:
        st.header("S3 Access Points")
        st.markdown("""
**Problem:** One S3 bucket policy becomes a 20KB monolith shared by 30 teams.  
**Solution:** S3 Access Points — named network endpoints with their own policies, one per application/team.

```
App A  → access-point-A (policy: prefix /team-a/, VPC: vpc-111)
App B  → access-point-B (policy: prefix /team-b/, VPC: vpc-222)
BI     → access-point-bi (policy: prefix /curated/, no VPC restriction)
                    ↓
              s3://my-data-lake/
```
        """)
        hcl("""
resource "aws_s3_access_point" "analytics_team" {
  bucket = aws_s3_bucket.lake.id
  name   = "analytics-team"

  vpc_configuration { vpc_id = var.analytics_vpc_id }

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { AWS = aws_iam_role.analytics.arn }
      Action    = ["s3:GetObject", "s3:ListBucket"]
      Resource  = [
        "arn:aws:s3:us-east-1:${data.aws_caller_identity.current.account_id}:accesspoint/analytics-team",
        "arn:aws:s3:us-east-1:${data.aws_caller_identity.current.account_id}:accesspoint/analytics-team/object/curated/*"
      ]
    }]
  })
}
        """)
        tip("Use S3 Multi-Region Access Points (MRAP) for active-active multi-region architectures — routes to the lowest-latency bucket.")

# ════════════════════════════════════════════════════════════════════════════
# INGESTION
# ════════════════════════════════════════════════════════════════════════════
elif section == "📥 Ingestion – Kinesis, MSK, Glue, DMS, AppFlow":
    st.title("📥 Ingestion")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Kinesis Family", "Amazon MSK", "AWS Glue + DMS", "AppFlow (SaaS)", "Ingestion Patterns"])

    with tab1:
        st.header("Kinesis Data Streams (KDS)")
        st.subheader("Capacity & Limits")
        df = pd.DataFrame({
            "Limit":       ["Write per shard", "Read per shard (std)", "Read per shard (EFO)", "Max record size", "Retention", "Max shards (soft)", "Shard split/merge"],
            "Value":       ["1 MB/s or 1,000 records/s", "2 MB/s shared across consumers", "2 MB/s per consumer", "1 MB", "24h–8,760h (1yr)", "500", "UpdateShardCount API"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("Kinesis Producer Library (KPL) vs SDK")
        df2 = pd.DataFrame({
            "Feature":    ["Batching", "Aggregation", "Retry logic", "Compression", "Language", "Use when"],
            "KPL":        ["✅ async", "✅ up to 500 records/shard", "✅ built-in", "✅", "Java only", "High-throughput producers, max cost efficiency"],
            "AWS SDK":    ["Manual", "Manual", "Manual", "Manual", "Any", "Simple producers, Lambda, quick scripts"],
        })
        st.dataframe(df2, use_container_width=True, hide_index=True)

        st.subheader("Kinesis Firehose – Format Conversion to Parquet")
        hcl("""
resource "aws_kinesis_firehose_delivery_stream" "events_parquet" {
  name        = "events-to-parquet"
  destination = "extended_s3"

  kinesis_source_configuration {
    kinesis_stream_arn = aws_kinesis_stream.events.arn
    role_arn           = aws_iam_role.firehose.arn
  }

  extended_s3_configuration {
    role_arn           = aws_iam_role.firehose.arn
    bucket_arn         = aws_s3_bucket.lake.arn
    prefix             = "raw/events/dt=!{timestamp:yyyy-MM-dd}/"
    error_output_prefix= "errors/events/!{firehose:error-output-type}/dt=!{timestamp:yyyy-MM-dd}/"
    buffering_size     = 128   # MB (up to 128)
    buffering_interval = 300   # seconds (60–900)

    # Lambda transform (optional: enrich/filter before write)
    processing_configuration {
      enabled = true
      processors {
        type = "Lambda"
        parameters {
          parameter_name  = "LambdaArn"
          parameter_value = "${aws_lambda_function.enricher.arn}:$LATEST"
        }
      }
    }

    # JSON → Parquet inline conversion using Glue schema
    data_format_conversion_configuration {
      enabled = true
      input_format_configuration {
        deserializer { hive_json_ser_de {} }
      }
      output_format_configuration {
        serializer {
          parquet_ser_de {
            compression    = "SNAPPY"
            block_size_bytes = 67108864  # 64 MB
          }
        }
      }
      schema_configuration {
        database_name = aws_glue_catalog_database.raw.name
        table_name    = aws_glue_catalog_table.events.name
        role_arn      = aws_iam_role.firehose.arn
        region        = var.aws_region
      }
    }
  }
}
        """)
        tip("Set Firehose buffer to 128 MB / 300s for best Parquet file sizes — too-small files hurt Athena query performance.")
        warn("Firehose doesn't support Iceberg natively — write to S3 Parquet then register with Glue Crawler or Iceberg MERGE job.")

    with tab2:
        st.header("Amazon MSK")
        st.subheader("MSK Connect – Managed Kafka Connect")
        st.markdown("""
Run Kafka Connect workers fully managed by AWS. Deploy source/sink connectors without managing EC2.

**Common Connectors:**
| Connector | Direction | Use case |
|-----------|-----------|---------|
| Debezium PostgreSQL/MySQL | Source | CDC from relational DBs |
| S3 Sink | Sink | Kafka topic → S3 Parquet |
| Redshift Sink | Sink | Kafka topic → Redshift |
| DynamoDB Streams | Source | DynamoDB CDC → MSK |
| JDBC Source | Source | RDBMS polling → MSK |
        """)
        hcl("""
resource "aws_mskconnect_connector" "s3_sink" {
  name = "kafka-to-s3-sink"

  kafkaconnect_version = "2.7.1"
  capacity {
    autoscaling {
      mcu_count        = 1
      min_worker_count = 1
      max_worker_count = 4
      scale_in_policy  { cpu_utilization_percentage = 20 }
      scale_out_policy { cpu_utilization_percentage = 80 }
    }
  }

  connector_configuration = {
    "connector.class"                   = "io.confluent.connect.s3.S3SinkConnector"
    "tasks.max"                         = "4"
    "topics"                            = "user-events,order-events"
    "s3.region"                         = var.aws_region
    "s3.bucket.name"                    = aws_s3_bucket.lake.id
    "s3.part.size"                      = "67108864"
    "flush.size"                        = "10000"
    "storage.class"                     = "io.confluent.connect.s3.storage.S3Storage"
    "format.class"                      = "io.confluent.connect.s3.format.parquet.ParquetFormat"
    "parquet.codec"                     = "snappy"
    "schema.compatibility"              = "FULL"
    "locale"                            = "en_US"
    "timezone"                          = "UTC"
    "timestamp.extractor"               = "RecordField"
    "timestamp.field"                   = "event_ts"
    "partitioner.class"                 = "io.confluent.connect.storage.partitioner.TimeBasedPartitioner"
    "path.format"                       = "'year'=YYYY/'month'=MM/'day'=dd"
    "partition.duration.ms"             = "3600000"
  }

  kafka_cluster {
    apache_kafka_cluster {
      bootstrap_servers = aws_msk_cluster.main.bootstrap_brokers_tls
      vpc { security_groups = [aws_security_group.msk_connect.id]; subnets = var.private_subnet_ids }
    }
  }
  kafka_cluster_client_authentication { authentication_type = "NONE" }
  kafka_cluster_encryption_in_transit  { encryption_type    = "TLS"  }

  plugin { custom_plugin { arn = aws_mskconnect_custom_plugin.s3_sink.arn; revision = 1 } }
  service_execution_role_arn = aws_iam_role.msk_connect.arn
}
        """)
        tip("MSK Connect auto-scales workers — use autoscaling capacity instead of fixed worker counts.")

    with tab3:
        st.header("AWS Glue + DMS")
        st.subheader("Glue – Connection Types")
        df = pd.DataFrame({
            "Type":      ["JDBC", "MongoDB", "Kafka", "Kinesis", "Network", "S3", "OpenSearch"],
            "Auth":      ["User/Pass, SSL", "MongoDB URI", "SASL/SSL", "IAM", "VPC endpoint", "IAM", "Endpoint+auth"],
            "Notes":     ["RDS, Aurora, on-prem", "Atlas or DocumentDB", "MSK or self-managed", "KDS direct", "Any VPC-accessible host", "Native, no connection needed", "ES/OpenSearch domains"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("DMS – Ongoing CDC Architecture")
        st.markdown("""
```
Source DB (Oracle/PG/MySQL/SQL Server)
    │  binary log / redo log / WAL
    ▼
DMS Replication Instance
    │  Full Load then CDC
    ▼
S3 (Parquet, partitioned by date)
    │
    ▼  Glue MERGE job
Iceberg Table (curated layer)
    │
    ▼  Athena / Redshift Spectrum
Analytics
```
        """)
        st.subheader("DMS Task Mappings – Filter & Transform")
        py("""
# DMS table-mapping JSON (passed as Terraform jsonencode)
{
  "rules": [
    {
      "rule-type": "selection",
      "rule-id": "1",
      "rule-name": "include-all-public",
      "object-locator": { "schema-name": "public", "table-name": "%" },
      "rule-action": "include"
    },
    {
      "rule-type": "selection",
      "rule-id": "2",
      "rule-name": "exclude-audit",
      "object-locator": { "schema-name": "public", "table-name": "audit_%" },
      "rule-action": "exclude"
    },
    {
      "rule-type": "transformation",
      "rule-id": "3",
      "rule-name": "lowercase-schema",
      "rule-action": "convert-lowercase",
      "rule-target": "schema",
      "object-locator": { "schema-name": "%" }
    },
    {
      "rule-type": "transformation",
      "rule-id": "4",
      "rule-name": "add-prefix",
      "rule-action": "add-prefix",
      "rule-target": "table",
      "object-locator": { "schema-name": "public", "table-name": "%" },
      "value": "src_"
    }
  ]
}
        """)
        warn("DMS CDC requires source DB pre-configuration: PostgreSQL needs `wal_level=logical`, MySQL needs `binlog_format=ROW`.")
        tip("Use DMS Serverless for variable CDC workloads — auto-scales capacity, no replication instance sizing needed.")

    with tab4:
        st.header("Amazon AppFlow – SaaS Ingestion")
        st.markdown("""
**Overview:** No-code/low-code connector for SaaS → S3/Redshift ingestion. No custom ETL needed.

**Supported Sources:** Salesforce · SAP · ServiceNow · Zendesk · Slack · Google Analytics · Marketo · Shopify · HubSpot · and 50+ more  
**Supported Targets:** S3 · Redshift · Snowflake · EventBridge
        """)
        hcl("""
resource "aws_appflow_flow" "salesforce_to_s3" {
  name = "salesforce-opportunities-to-s3"

  source_flow_config {
    connector_type = "Salesforce"
    connector_profile_name = "salesforce-prod"
    source_connector_properties {
      salesforce {
        object          = "Opportunity"
        enable_dynamic_field_update = true
        include_deleted_records     = false
      }
    }
    incremental_pull_config {
      datetime_type_field_name = "LastModifiedDate"
    }
  }

  destination_flow_config {
    connector_type = "S3"
    destination_connector_properties {
      s3 {
        bucket_name   = aws_s3_bucket.lake.id
        bucket_prefix = "raw/salesforce/opportunities"
        s3_output_format_config {
          file_type = "PARQUET"
          prefix_config { prefix_type = "PATH"; prefix_format = "YEAR_MONTH_DAY" }
          aggregation_config { aggregation_type = "SingleFile" }
        }
      }
    }
  }

  # Run on trigger (new/updated records)
  trigger_config {
    trigger_type = "Scheduled"
    trigger_properties {
      scheduled {
        schedule_expression = "rate(1hour)"
        data_pull_mode      = "Incremental"
      }
    }
  }

  task {
    source_fields     = ["Id","Name","Amount","StageName","CloseDate","LastModifiedDate"]
    task_type         = "Filter"
    connector_operator { salesforce = "PROJECTION" }
  }
}
        """)
        tip("AppFlow supports field mapping and masking — mask Salesforce PII (email, phone) before it lands in S3.")

    with tab5:
        st.header("Ingestion Pattern Decision Guide")
        df = pd.DataFrame({
            "Source Type":        ["Relational DB (batch)", "Relational DB (CDC)", "SaaS app", "IoT / clickstream", "Application logs", "Message queue", "File drop (S3)"],
            "Recommended":        ["Glue JDBC / DMS Full Load", "DMS CDC → S3 → Iceberg MERGE", "AppFlow", "Kinesis Data Streams → Firehose", "Kinesis Firehose / CloudWatch → Firehose", "MSK (Kafka) → MSK Connect → S3", "S3 Event → Lambda/Glue trigger"],
            "Alternative":        ["JDBC directly in EMR", "Debezium on MSK Connect", "Lambda + API polling", "MSK + Kafka Streams", "Fluentd/Logstash → MSK", "SQS → Lambda → S3", "EventBridge Pipe → Step Functions"],
            "Avoid":              ["Row-by-row Lambda inserts", "DMS to Redshift (bottleneck)", "Custom API ETL for popular SaaS", "Polling DB for new rows", "Writing logs directly to Redshift", "Polling S3 for new files", "Cron + SSH + SCP"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════
# PROCESSING
# ════════════════════════════════════════════════════════════════════════════
elif section == "⚙️ Processing – Glue, EMR, Redshift, Athena, Lambda":
    st.title("⚙️ Processing")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["AWS Glue", "Amazon EMR", "Amazon Redshift", "Amazon Athena", "Lambda & Step Functions"])

    with tab1:
        st.header("AWS Glue – Full Reference")
        st.subheader("Worker Type Comparison")
        df = pd.DataFrame({
            "Worker":     ["G.025X", "G.1X", "G.2X", "G.4X", "G.8X", "Z.2X (Ray)"],
            "vCPU":       [2, 4, 8, 16, 32, 8],
            "RAM (GB)":   [4, 16, 32, 64, 128, 64],
            "DPU":        [0.25, 1, 2, 4, 8, 2],
            "Cost/hr":    ["$0.044", "$0.44", "$0.88", "$1.76", "$3.52", "$0.88"],
            "Best for":   ["Dev/small", "General", "Medium-large", "Large", "Huge shuffles", "Ray workloads"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("Glue Job Bookmark – How it Works")
        st.markdown("""
Job bookmarks track which S3 objects/JDBC offsets have been processed, enabling **incremental loads** without querying source state.

- **S3:** Tracks object ETags and last-modified timestamps  
- **JDBC:** Tracks max value of a numeric primary key or timestamp column  
- **Kinesis/MSK:** Uses `checkpointLocation` on S3 instead  

**Bookmark states:** `job-bookmark-enable` | `job-bookmark-disable` | `job-bookmark-pause`
        """)

        st.subheader("PySpark – Glue DynamicFrame vs Spark DataFrame")
        py("""
from awsglue.context import GlueContext
from awsglue.transforms import *
from pyspark.context import SparkContext
from pyspark.sql import functions as F

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# DynamicFrame — schema flexibility, handles nulls/mixed types
dyf = glueContext.create_dynamic_frame.from_catalog(
    database="raw", table_name="events",
    push_down_predicate="(dt >= '2024-01-01')",  # partition pruning
    additional_options={"boundedFiles": "1000"}   # limit for dev
)

# Resolve choice — handle ambiguous types
dyf_resolved = ResolveChoice.apply(dyf,
    choice="make_cols",  # create separate col per type variant
    transformation_ctx="resolve")

# Convert to DataFrame for complex transforms
df = dyf_resolved.toDF()

df_clean = (df
    .filter(F.col("event_id").isNotNull())
    .withColumn("event_date", F.to_date(F.from_unixtime(F.col("event_ts")/1000)))
    .withColumn("amount_usd", F.round(F.col("amount") * F.lit(1.0), 2))
    .dropDuplicates(["event_id"])
)

# Convert back to DynamicFrame for Glue sink
dyf_out = glueContext.create_dynamic_frame.from_dataframe(df_clean, glueContext)

# Write to S3 as Iceberg via Glue Catalog
glueContext.write_dynamic_frame.from_catalog(
    frame=dyf_out,
    database="curated",
    table_name="events",
    additional_options={
        "callSite": {"site": "curated-events-write"},
        "write.format.default": "parquet",
    }
)
        """)

        st.subheader("Glue Ray – Distributed Python (non-Spark)")
        py("""
# Glue Ray job — use for Python-native ML preprocessing, pandas workflows
import ray
import ray.data

@ray.remote
def process_partition(batch):
    import pandas as pd
    df = pd.DataFrame(batch)
    df['processed'] = df['value'].apply(lambda x: x * 2)
    return df.to_dict('records')

ray.init()

ds = ray.data.read_parquet("s3://my-lake/raw/events/")
ds_processed = ds.map_batches(process_partition, batch_format="pandas")
ds_processed.write_parquet("s3://my-lake/curated/events/")
        """)
        tip("Use Glue Ray for pandas/scikit-learn workflows — no JVM overhead, faster startup than Spark for small-medium data.")
        warn("Glue Streaming jobs have a fixed 48-hour timeout — implement restart logic or use EMR Flink for 24/7 streams.")

    with tab2:
        st.header("Amazon EMR – Deep Dive")
        st.subheader("EMR on EC2 – Cluster Architecture")
        st.markdown("""
```
┌─────────────────────────────────────────────┐
│  Master Node (1)  — NameNode, YARN RM        │
│  Core Nodes  (N)  — DataNode, YARN NM        │  ← On-Demand (stateful)
│  Task Nodes  (N)  — YARN NM only             │  ← Spot (stateless, safe to interrupt)
└─────────────────────────────────────────────┘
         │ reads/writes
      S3 (EMRFS) ← recommended over HDFS for durability
```
        """)
        st.subheader("EMR Spark Configuration Tuning")
        py("""
# spark-submit / EMR step configuration best practices
spark_config = {
    # Executor sizing: (node_memory - 1GB overhead) / executors_per_node
    "spark.executor.memory":          "14g",
    "spark.executor.cores":           "4",
    "spark.executor.instances":       "20",
    "spark.driver.memory":            "8g",

    # Shuffle
    "spark.sql.shuffle.partitions":   "400",  # ~2-3x total cores
    "spark.shuffle.service.enabled":  "true",

    # Dynamic allocation (use with shuffle service)
    "spark.dynamicAllocation.enabled":             "true",
    "spark.dynamicAllocation.minExecutors":        "2",
    "spark.dynamicAllocation.maxExecutors":        "100",
    "spark.dynamicAllocation.initialExecutors":    "10",

    # Adaptive Query Execution (Spark 3+)
    "spark.sql.adaptive.enabled":                  "true",
    "spark.sql.adaptive.coalescePartitions.enabled":"true",
    "spark.sql.adaptive.skewJoin.enabled":         "true",

    # Iceberg
    "spark.sql.extensions":           "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
    "spark.sql.catalog.glue_catalog": "org.apache.iceberg.spark.SparkCatalog",
    "spark.sql.catalog.glue_catalog.catalog-impl": "org.apache.iceberg.aws.glue.GlueCatalog",
    "spark.sql.catalog.glue_catalog.io-impl":      "org.apache.iceberg.aws.s3.S3FileIO",

    # S3 performance
    "spark.hadoop.fs.s3a.fast.upload":             "true",
    "spark.hadoop.fs.s3a.block.size":              "134217728",  # 128 MB
    "spark.hadoop.fs.s3a.multipart.size":          "67108864",   # 64 MB
    "spark.hadoop.fs.s3a.connection.maximum":      "100",
}
        """)

        st.subheader("EMR Serverless – Terraform")
        hcl("""
resource "aws_emrserverless_application" "spark" {
  name          = "${var.project}-spark"
  release_label = "emr-7.2.0"
  type          = "SPARK"

  # Pre-warm workers to avoid cold starts
  initial_capacity {
    initial_capacity_type = "Driver"
    initial_capacity_config {
      worker_count = 1
      worker_configuration { cpu = "4vCPU"; memory = "16gb" }
    }
  }
  initial_capacity {
    initial_capacity_type = "Executor"
    initial_capacity_config {
      worker_count = 5
      worker_configuration { cpu = "4vCPU"; memory = "16gb"; disk = "20gb" }
    }
  }

  maximum_capacity { cpu = "400vCPU"; memory = "3000gb"; disk = "20000gb" }

  auto_stop_configuration {
    enabled              = true
    idle_timeout_minutes = 15
  }

  network_configuration {
    security_group_ids = [aws_security_group.emr.id]
    subnet_ids         = var.private_subnet_ids
  }

  image_configuration {
    image_uri = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.region}.amazonaws.com/emr-custom:latest"
    # Custom image with pre-installed Python packages
  }
}
        """)

    with tab3:
        st.header("Amazon Redshift – Deep Dive")
        st.subheader("Distribution Styles")
        df = pd.DataFrame({
            "Style":   ["EVEN", "KEY", "ALL", "AUTO"],
            "How":     ["Round-robin", "Hash of column", "Full copy on every node", "Redshift chooses"],
            "When":    ["No obvious join key", "Large tables joined on same key", "Small dimension tables", "Let Redshift optimize"],
            "Risk":    ["Data shuffling on joins", "Hot nodes if skewed", "Storage overhead", "Less control"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("Redshift Workload Management (WLM)")
        st.markdown("""
```
WLM Queue Priority:
  ┌─────────────────────────────────────┐
  │ SQA (Short Query Acceleration)      │  < 20s queries auto-routed here
  │ ETL Queue       (concurrency: 5)    │  dedicated for COPY/INSERT jobs
  │ BI Queue        (concurrency: 15)   │  dashboards / reporting
  │ Superuser Queue (concurrency: 1)    │  admin queries, always available
  └─────────────────────────────────────┘
```

**Concurrency Scaling:** Automatically adds transient clusters during peaks. Enable per queue with `concurrency_scaling = auto`.  
**QMR (Query Monitoring Rules):** Kill/alert/hop on long-running or high-resource queries.
        """)

        st.subheader("Useful Redshift System Views")
        sql("""
-- Active running queries + wait time
SELECT pid, user_name, query, elapsed/1000000 elapsed_sec, queue_time/1000000 queue_sec
FROM stv_recents WHERE status = 'Running' ORDER BY elapsed_sec DESC;

-- Table skew and distribution quality
SELECT t.name, s.num_values, s.skew_rows, s.skew_sortkey1
FROM svv_table_info t JOIN svv_diskusage s ON t.table = s.name
ORDER BY skew_rows DESC LIMIT 20;

-- Top expensive queries last 7 days
SELECT userid, trim(querytxt) query, starttime, endtime,
       datediff(seconds, starttime, endtime) duration_sec,
       aborted
FROM stl_query
WHERE starttime > dateadd(day, -7, getdate())
ORDER BY duration_sec DESC LIMIT 20;

-- Compression recommendations
ANALYZE COMPRESSION orders;

-- Vacuum progress
SELECT * FROM svv_vacuum_progress;

-- Data lineage: which queries wrote to which tables
SELECT DISTINCT w.query, trim(q.querytxt), r.name target_table
FROM stl_insert r JOIN stl_query q ON r.query = q.query
JOIN stl_querytext w ON w.query = q.query
ORDER BY r.starttime DESC LIMIT 20;
        """)
        tip("Run `VACUUM SORT ONLY` weekly and `VACUUM DELETE ONLY` after large deletes — full VACUUM is expensive.")
        warn("Never use `SELECT *` on large Redshift tables — always project only needed columns for MPP efficiency.")

        st.subheader("Redshift Spectrum + Iceberg")
        sql("""
-- Create external schema pointing to Glue Catalog
CREATE EXTERNAL SCHEMA iceberg_curated
FROM DATA CATALOG
DATABASE 'curated'
IAM_ROLE 'arn:aws:iam::123456789:role/RedshiftSpectrumRole'
CATALOG_ROLE 'arn:aws:iam::123456789:role/GlueCatalogRole';

-- Query Iceberg table from Redshift (no data copy)
SELECT date_trunc('month', event_ts) month, count(*) events
FROM iceberg_curated.events
WHERE event_type = 'purchase'
  AND event_ts >= '2024-01-01'
GROUP BY 1 ORDER BY 1;

-- Federated query to Aurora PostgreSQL
CREATE EXTERNAL SCHEMA aurora_public
FROM POSTGRES
DATABASE 'mydb' SCHEMA 'public'
URI 'my-aurora-cluster.cluster-xyz.us-east-1.rds.amazonaws.com'
IAM_ROLE 'arn:aws:iam::123456789:role/RedshiftFedRole'
SECRET_ARN 'arn:aws:secretsmanager:us-east-1:123456789:secret:aurora-creds';
        """)

    with tab4:
        st.header("Amazon Athena – Deep Dive")
        st.subheader("Athena v3 (Trino Engine) New Features")
        df = pd.DataFrame({
            "Feature":      ["MERGE INTO", "Window functions", "MATCH_RECOGNIZE", "Grouping sets", "Lateral joins", "Approximate functions", "Cost-based optimizer"],
            "Available in": ["v3 + Iceberg", "v2 + v3", "v3", "v2 + v3", "v3", "v2 + v3", "v3"],
            "Notes":        ["Iceberg upserts natively", "RANK, DENSE_RANK, LAG, LEAD", "Complex event detection", "CUBE, ROLLUP, GROUPING SETS", "UNNEST, CROSS JOIN LATERAL", "approx_distinct, approx_percentile", "Table stats from Glue Catalog"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("Athena Query Optimization Patterns")
        sql("""
-- 1. Partition pruning (always filter on partition cols)
SELECT * FROM curated.events
WHERE dt BETWEEN '2024-01-01' AND '2024-01-31'  -- uses partition
  AND event_type = 'purchase';

-- 2. CTAS – materialise expensive query as Parquet+partitioned table
CREATE TABLE curated.monthly_summary
WITH (
  format = 'PARQUET',
  write_compression = 'SNAPPY',
  external_location = 's3://my-lake/curated/monthly_summary/',
  partitioned_by = ARRAY['year_month'],
  bucketed_by = ARRAY['user_id'],
  bucket_count = 16
)
AS
SELECT user_id, event_type,
       count(*) events, sum(amount) total_amount,
       format_datetime(date_trunc('month', event_ts), 'yyyy-MM') year_month
FROM curated.events
GROUP BY 1, 2, 5;

-- 3. Iceberg time travel
SELECT * FROM curated.orders
FOR SYSTEM_TIME AS OF TIMESTAMP '2024-06-01 00:00:00 UTC';

-- 4. Iceberg MERGE (Athena v3)
MERGE INTO curated.customers t
USING staging.customer_updates s ON t.customer_id = s.customer_id
WHEN MATCHED AND s.deleted = true THEN DELETE
WHEN MATCHED THEN UPDATE SET email = s.email, updated_at = s.updated_at
WHEN NOT MATCHED THEN INSERT (customer_id, email, created_at, updated_at)
  VALUES (s.customer_id, s.email, s.created_at, s.updated_at);

-- 5. Approximate distinct count (much faster, ~2% error)
SELECT approx_distinct(user_id) unique_users,
       approx_percentile(response_ms, 0.95) p95_latency
FROM curated.events
WHERE dt = '2024-01-15';
        """)
        tip("Use `approx_distinct()` instead of `COUNT(DISTINCT)` for analytics dashboards — 10–100x faster, ~2% error.")
        warn("Athena charges per query even for failed queries if data was scanned — set workgroup `bytes_scanned_cutoff_per_query`.")

    with tab5:
        st.header("Lambda & Step Functions")
        st.subheader("Lambda Data Engineering Patterns")
        py("""
import boto3, json, os
from datetime import datetime

# Pattern 1: S3 trigger → lightweight transform → write back
def handler_s3_transform(event, context):
    s3 = boto3.client('s3')
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key    = record['s3']['object']['key']

        obj = s3.get_object(Bucket=bucket, Key=key)
        data = json.loads(obj['Body'].read())

        # Lightweight transform
        enriched = {**data, 'processed_at': datetime.utcnow().isoformat(), 'env': os.environ['ENV']}

        out_key = key.replace('raw/', 'curated/')
        s3.put_object(Bucket=bucket, Key=out_key, Body=json.dumps(enriched))

# Pattern 2: Trigger Glue job with dynamic params
def handler_trigger_glue(event, context):
    glue = boto3.client('glue')
    response = glue.start_job_run(
        JobName=os.environ['GLUE_JOB_NAME'],
        Arguments={
            '--source_date':  event.get('date', datetime.utcnow().strftime('%Y-%m-%d')),
            '--source_table': event['table'],
        }
    )
    return {'job_run_id': response['JobRunId']}

# Pattern 3: Redshift Data API (async, no VPC needed)
def handler_redshift_query(event, context):
    rs = boto3.client('redshift-data')
    resp = rs.execute_statement(
        WorkgroupName=os.environ['WORKGROUP'],
        Database='datawarehouse',
        Sql=f"CALL sp_load_partition('{event['partition_date']}');",
    )
    return {'statement_id': resp['Id']}  # poll with describe_statement
        """)

        st.subheader("Step Functions – Map State for Parallel S3 Processing")
        py("""
{
  "Comment": "Process S3 partition list in parallel",
  "StartAt": "ListPartitions",
  "States": {
    "ListPartitions": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Parameters": {
        "FunctionName": "list-s3-partitions",
        "Payload.$": "$"
      },
      "ResultSelector": { "partitions.$": "$.Payload.partitions" },
      "Next": "ProcessInParallel"
    },
    "ProcessInParallel": {
      "Type": "Map",
      "ItemsPath": "$.partitions",
      "MaxConcurrency": 10,
      "Iterator": {
        "StartAt": "ProcessPartition",
        "States": {
          "ProcessPartition": {
            "Type": "Task",
            "Resource": "arn:aws:states:::glue:startJobRun.sync",
            "Parameters": {
              "JobName": "process-partition",
              "Arguments": {
                "--partition.$": "$"
              }
            },
            "End": true
          }
        }
      },
      "Next": "LoadToRedshift"
    },
    "LoadToRedshift": {
      "Type": "Task",
      "Resource": "arn:aws:states:::redshift-data:executeStatement.sync",
      "Parameters": {
        "WorkgroupName": "primary",
        "Database": "datawarehouse",
        "Sql": "CALL sp_refresh_all();"
      },
      "End": true
    }
  }
}
        """)

# ════════════════════════════════════════════════════════════════════════════
# ARCHITECTURES
# ════════════════════════════════════════════════════════════════════════════
elif section == "🏗️ Architectures – Lake, Warehouse, Lakehouse, Mesh":
    st.title("🏗️ Architectures")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Data Lake", "Data Warehouse", "Data Lakehouse", "Data Mesh", "Lambda vs Kappa"])

    with tab1:
        st.header("Data Lake – Medallion Architecture")
        st.markdown("""
```
┌──────────────────────────────────────────────────────────────────┐
│                     S3 Data Lake                                  │
│                                                                    │
│  [Bronze / Raw]          [Silver / Curated]    [Gold / Consumption]│
│  s3://lake/raw/          s3://lake/curated/    s3://lake/gold/    │
│  ─────────────           ────────────────────  ──────────────     │
│  • Exact source copy     • Deduplicated        • Aggregated       │
│  • JSON / CSV / Avro     • Validated           • Domain-specific  │
│  • Partitioned by date   • Parquet + Iceberg   • Parquet/Iceberg  │
│  • Immutable             • Schema enforced     • Optimized reads  │
│                          • PII masked          • Pre-joined       │
└──────────────────────────────────────────────────────────────────┘
                                                        ↓
                               Athena · EMR · Redshift Spectrum · SageMaker
```
        """)
        st.subheader("Zone Access Policies")
        df = pd.DataFrame({
            "Zone":     ["Bronze/Raw", "Silver/Curated", "Gold/Consumption"],
            "Writers":  ["Firehose, DMS, AppFlow, Glue ingest", "Glue ETL, EMR (DE team only)", "dbt, Glue agg jobs"],
            "Readers":  ["Data engineers only", "Data engineers, Data scientists", "BI, Analysts, Data scientists, APIs"],
            "LF grants": ["DE role only", "DE + DS roles", "All roles with appropriate column/row filters"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        st.header("Data Warehouse (Redshift)")
        st.subheader("Dimensional Modeling on Redshift")
        sql("""
-- Star schema example
CREATE TABLE dim_customer (
  customer_sk   BIGINT IDENTITY PRIMARY KEY,
  customer_id   VARCHAR(36) NOT NULL,
  email         VARCHAR(255) ENCODE zstd,
  country       VARCHAR(3)   ENCODE bytedict,
  created_at    TIMESTAMP,
  valid_from    TIMESTAMP,
  valid_to      TIMESTAMP,
  is_current    BOOLEAN DEFAULT true
)
DISTSTYLE ALL    -- replicated to all nodes (dimension table)
SORTKEY (customer_id, valid_from);

CREATE TABLE fact_orders (
  order_sk       BIGINT IDENTITY,
  order_id       VARCHAR(36) NOT NULL ENCODE zstd,
  customer_sk    BIGINT NOT NULL REFERENCES dim_customer(customer_sk),
  product_sk     BIGINT NOT NULL,
  order_date_sk  INT NOT NULL,
  amount_usd     DECIMAL(18,4),
  quantity       INT,
  created_at     TIMESTAMP
)
DISTSTYLE KEY DISTKEY (customer_sk)   -- co-locate with dim_customer joins
COMPOUND SORTKEY (order_date_sk, customer_sk);

-- Materialized view for dashboard acceleration
CREATE MATERIALIZED VIEW mv_monthly_revenue
AUTO REFRESH YES AS
SELECT date_trunc('month', o.created_at) month,
       c.country,
       sum(o.amount_usd) revenue,
       count(distinct o.customer_sk) customers
FROM fact_orders o JOIN dim_customer c ON o.customer_sk = c.customer_sk
GROUP BY 1,2;
        """)

    with tab3:
        st.header("Data Lakehouse (Iceberg on S3)")
        st.markdown("""
**Reference architecture:**
```
Streaming:  MSK → Glue Streaming → S3 Iceberg (curated) ──┐
Batch CDC:  DMS → S3 raw → Glue MERGE → S3 Iceberg        ├─→ Athena / Redshift Spectrum / EMR / SageMaker
Batch ETL:  S3 raw → EMR Spark → S3 Iceberg (gold)  ───────┘
```

**Key design decisions for Iceberg Lakehouse:**
        """)
        df = pd.DataFrame({
            "Decision":      ["Partition strategy", "File size target", "Compaction frequency", "Table maintenance", "Sort order", "Write mode"],
            "Recommendation": ["Days for time-series, hash bucket for high-cardinality IDs", "128–256 MB (sweet spot for Athena/Spark)", "Hourly for streaming tables, daily for batch", "Weekly snapshot expiry + orphan file cleanup", "Cluster by most-filtered column", "merge-on-read for streaming, copy-on-write for batch"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("Iceberg Maintenance Jobs (Glue PySpark)")
        st.code('''
def run_iceberg_maintenance(spark, catalog, database, table):
    # 1. Expire old snapshots (keep 7 days)
    expire_sql = f"""
        CALL {catalog}.system.expire_snapshots(
            table => '{database}.{table}',
            older_than => TIMESTAMP '2024-01-08 00:00:00',
            retain_last => 5
        )
    """
    spark.sql(expire_sql)

    # 2. Remove orphan files
    orphan_sql = f"""
        CALL {catalog}.system.remove_orphan_files(
            table => '{database}.{table}',
            older_than => TIMESTAMP '2024-01-06 00:00:00'
        )
    """
    spark.sql(orphan_sql)

    # 3. Compact small files
    compact_sql = f"""
        CALL {catalog}.system.rewrite_data_files(
            table => '{database}.{table}',
            options => map(
                'target-file-size-bytes', '134217728',
                'min-file-size-bytes',    '33554432',
                'max-file-size-bytes',    '268435456'
            )
        )
    """
    spark.sql(compact_sql)

    # 4. Rewrite manifests for faster planning
    spark.sql(f"CALL {catalog}.system.rewrite_manifests('{database}.{table}')")
        ''', language="python")

    with tab4:
        st.header("Data Mesh on AWS")
        st.markdown("""
**Data Mesh principles:**  
1. **Domain ownership** — each domain team owns its data products  
2. **Data as a product** — discoverable, trustworthy, self-serve  
3. **Self-serve platform** — central team provides infra, not pipelines  
4. **Federated governance** — global policies, local implementation  

**AWS Implementation:**
```
┌─────────────────────────────────────────────────────────────┐
│  Central Governance Account                                  │
│  • Lake Formation central catalog                           │
│  • SCPs + AWS Organizations policies                        │
│  • Shared network (Transit Gateway)                         │
└────────────────┬────────────────────────────────────────────┘
                 │  AWS RAM + Lake Formation cross-account share
     ┌───────────┼───────────┬───────────────┐
     ▼           ▼           ▼               ▼
┌─────────┐ ┌─────────┐ ┌─────────┐  ┌──────────────┐
│ Finance │ │Marketing│ │ Orders  │  │  Analytics   │
│ Account │ │ Account │ │ Account │  │  Consumer    │
│  S3+Glue│ │  S3+Glue│ │  S3+Glue│  │  Redshift    │
│  Data   │ │  Data   │ │  Data   │  │  Athena      │
│  Product│ │  Product│ │  Product│  │  SageMaker   │
└─────────┘ └─────────┘ └─────────┘  └──────────────┘
```
        """)
        tip("Use **AWS Data Zone** (managed data mesh service) to automate data product publishing, subscription, and access workflows.")

    with tab5:
        st.header("Lambda Architecture vs Kappa Architecture")
        df = pd.DataFrame({
            "Dimension":       ["Architecture", "Layers", "Complexity", "Consistency", "Reprocessing", "Best for"],
            "Lambda Arch":     ["Batch + Speed + Serving", "Three (batch, speed, serving)", "High — two code paths", "Batch is source of truth", "Yes, batch layer reprocesses", "Mixed batch+streaming with different freshness needs"],
            "Kappa Arch":      ["Streaming only", "One (streaming, replay for batch)", "Lower — one code path", "Stream is source of truth", "Replay from Kafka/KDS with offset reset", "Primarily streaming, reprocess by replaying"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)
        info("Most modern lakehouses implement a simplified Kappa-style architecture using Iceberg streaming + batch MERGE on the same table.")

# ════════════════════════════════════════════════════════════════════════════
# ORCHESTRATION
# ════════════════════════════════════════════════════════════════════════════
elif section == "🎼 Orchestration – MWAA, Step Functions, EventBridge":
    st.title("🎼 Orchestration")
    tab1, tab2, tab3, tab4 = st.tabs(
        ["MWAA (Airflow)", "Step Functions", "EventBridge", "Orchestration Patterns"])

    with tab1:
        st.header("MWAA – Managed Apache Airflow")
        st.subheader("Environment Classes")
        df = pd.DataFrame({
            "Class":        ["mw1.small", "mw1.medium", "mw1.large", "mw1.xlarge", "mw1.2xlarge"],
            "vCPU":         [2, 4, 8, 16, 32],
            "RAM (GB)":     [4, 8, 16, 32, 64],
            "Max workers":  [5, 10, 25, 50, 100],
            "Cost/hr":      ["~$0.49", "~$0.98", "~$1.96", "~$3.92", "~$7.84"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("DAG – AWS Pipeline Example")
        py("""
from airflow import DAG
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.amazon.aws.operators.emr import EmrServerlessStartJobRunOperator
from airflow.providers.amazon.aws.operators.redshift_data import RedshiftDataOperator
from airflow.providers.amazon.aws.sensors.glue import GlueJobSensor
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'data-engineering',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email': ['de-team@company.com'],
}

with DAG(
    dag_id='daily_etl_pipeline',
    default_args=default_args,
    schedule_interval='0 6 * * *',  # 6 AM UTC
    start_date=days_ago(1),
    catchup=False,
    tags=['etl', 'daily'],
) as dag:

    ingest = GlueJobOperator(
        task_id='ingest_from_rds',
        job_name='ingest-orders-from-rds',
        script_args={'--source_date': '{{ ds }}'},
        aws_conn_id='aws_default',
    )

    transform = EmrServerlessStartJobRunOperator(
        task_id='transform_with_spark',
        application_id='{{ var.value.emr_app_id }}',
        execution_role_arn='{{ var.value.emr_role_arn }}',
        job_driver={
            'sparkSubmit': {
                'entryPoint': 's3://scripts/transform_orders.py',
                'entryPointArguments': ['--date', '{{ ds }}'],
                'sparkSubmitParameters': '--conf spark.executor.cores=4',
            }
        },
        aws_conn_id='aws_default',
        wait_for_completion=True,
    )

    load = RedshiftDataOperator(
        task_id='load_to_redshift',
        database='datawarehouse',
        workgroup_name='primary',
        sql=f"CALL sp_load_orders('{{{{ ds }}}}');",
        aws_conn_id='aws_default',
        wait_for_completion=True,
    )

    ingest >> transform >> load
        """)
        tip("Use Airflow `Variables` and `Connections` stored in AWS Secrets Manager — MWAA integrates natively.")
        warn("Avoid heavy computation in DAG files — MWAA scheduler parses all DAGs every 30s. Keep DAG files thin, logic in operators.")

    with tab2:
        st.header("Step Functions – Advanced Patterns")
        st.subheader("Callback Pattern (wait for external event)")
        py("""
# Step Functions state waits for callback (taskToken) from external system
{
  "WaitForManualApproval": {
    "Type": "Task",
    "Resource": "arn:aws:states:::sqs:sendMessage.waitForTaskToken",
    "Parameters": {
      "QueueUrl": "https://sqs.us-east-1.amazonaws.com/123/approvals",
      "MessageBody": {
        "task_token.$": "$$.Task.Token",
        "pipeline_id.$": "$.pipeline_id",
        "message": "Approve data load to production?"
      }
    },
    "HeartbeatSeconds": 86400,  # 24-hour window for approval
    "Next": "LoadToProduction"
  }
}

# Lambda/external system sends callback:
import boto3
sfn = boto3.client('stepfunctions')
sfn.send_task_success(
    taskToken='<token from message>',
    output=json.dumps({'approved': True, 'approver': 'jane@company.com'})
)
        """)

        st.subheader("Step Functions vs MWAA Decision Tree")
        st.markdown("""
| Choose **Step Functions** when... | Choose **MWAA** when... |
|----------------------------------|------------------------|
| Pure AWS-service orchestration   | Rich DAG dependencies (fan-out/fan-in) |
| < 10 steps in workflow           | 10+ tasks with complex branching |
| Event-driven triggers (S3, EB)   | Schedule-heavy (cron-based) pipelines |
| Low cost priority                | Need Airflow UI / XCom / task history |
| No Python orchestration code     | Cross-cloud or on-prem connectors needed |
| Serverless, no ops               | Team familiar with Airflow |
        """)

    with tab3:
        st.header("EventBridge – Event-Driven Pipelines")
        st.subheader("EventBridge Pipes – Point-to-Point")
        st.markdown("""
**Pipes** connect a source directly to a target with optional filtering and enrichment — simpler than rules for 1:1 event flows.

```
Kinesis Stream → [Filter] → [Lambda Enrichment] → Step Functions
SQS Queue      → [Filter] → [Lambda Enrichment] → Glue Job
DynamoDB Stream→ [Filter] →                     → EventBridge Bus
```
        """)
        hcl("""
resource "aws_pipes_pipe" "kinesis_to_sfn" {
  name     = "kinesis-events-to-pipeline"
  role_arn = aws_iam_role.pipes.arn
  source   = aws_kinesis_stream.events.arn
  target   = aws_sfn_state_machine.processor.arn

  source_parameters {
    kinesis_stream_parameters {
      starting_position = "LATEST"
      batch_size        = 100
    }
    filter_criteria {
      filter {
        pattern = jsonencode({ data = { event_type = ["purchase"] } })
      }
    }
  }

  enrichment = aws_lambda_function.enricher.arn
  enrichment_parameters {
    input_template = "{\"records\": <$.>}"
  }

  target_parameters {
    step_function_state_machine_parameters {
      invocation_type = "FIRE_AND_FORGET"
    }
  }
}
        """)

        st.subheader("EventBridge Scheduler – Flexible Cron")
        hcl("""
resource "aws_scheduler_schedule" "glue_daily" {
  name       = "daily-glue-etl"
  group_name = "data-engineering"

  flexible_time_window {
    mode                      = "FLEXIBLE"
    maximum_window_in_minutes = 30  # run within 30-min window (helps spread load)
  }

  schedule_expression          = "cron(0 6 * * ? *)"
  schedule_expression_timezone = "UTC"

  target {
    arn      = "arn:aws:scheduler:::aws-sdk:glue:startJobRun"
    role_arn = aws_iam_role.scheduler.arn
    input    = jsonencode({ JobName = aws_glue_job.etl.name, Arguments = {} })
    retry_policy {
      maximum_retry_attempts       = 2
      maximum_event_age_in_seconds = 3600
    }
  }
}
        """)

    with tab4:
        st.header("Orchestration Patterns")
        df = pd.DataFrame({
            "Pattern":         ["Fan-out", "Fan-in", "Checkpoint & Resume", "Event-driven trigger", "Approval gate", "SLA monitoring"],
            "Step Functions":  ["Map state", "Map + barrier", "DynamoDB state store", "EventBridge → SFN", "Callback + taskToken", "CloudWatch alarm → SFN"],
            "MWAA (Airflow)":  ["TriggerDagRunOperator", "ExternalTaskSensor", "XCom + Airflow state", "S3KeySensor / trigger", "HttpSensor + approval API", "SLA miss callbacks"],
            "Best choice":     ["Step Fn (simpler)", "Both equal", "MWAA (built-in)", "Step Fn (native)", "Both (SFN simpler)", "MWAA (richer)"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════
# GOVERNANCE
# ════════════════════════════════════════════════════════════════════════════
elif section == "🔒 Governance, Security & Quality":
    st.title("🔒 Governance, Security & Quality")
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Governance Stack", "Data Quality (DQDL)", "Security", "Audit & Compliance"])

    with tab1:
        st.header("AWS Governance Stack")
        df = pd.DataFrame({
            "Layer":     ["Identity", "Data access", "Metadata", "Quality", "Discovery", "Lineage", "Secrets", "Compliance"],
            "Service":   ["IAM + Organizations SCPs", "Lake Formation (column/row)", "Glue Data Catalog + Schema Registry", "Glue Data Quality", "AWS Glue / Data Zone catalog", "Lake Formation lineage / OpenLineage on MWAA", "Secrets Manager / Parameter Store", "AWS Config + Audit Manager + CloudTrail"],
            "Key action": ["Least privilege roles, no long-term keys", "LF-TBAC for scale, row filters for tenancy", "Versioned schemas on Kinesis/MSK", "DQDL rules on Glue tables, quarantine bad records", "Tag-based discovery, business glossary", "Track job → table lineage automatically", "Rotate credentials, inject into Glue/Lambda", "Continuous compliance checks, evidence collection"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        st.header("Glue Data Quality – DQDL Reference")
        st.markdown(
            "**DQDL (Data Quality Definition Language)** — declarative rule language for Glue DQ jobs.")
        bash("""
# Full DQDL ruleset example
Rules = [
  # Completeness
  Completeness "order_id" >= 0.99,
  Completeness "customer_id" >= 0.995,

  # Uniqueness
  Uniqueness "order_id" >= 0.9999,

  # Value ranges
  ColumnValues "amount" between 0 and 1000000,
  ColumnValues "status" in ["PENDING", "COMPLETED", "CANCELLED", "REFUNDED"],
  ColumnValues "country_code" matches "[A-Z]{2}",

  # Referential integrity
  ReferentialIntegrity "customer_id" "customers.customer_id" >= 0.99,

  # Statistical
  ColumnStatistics "amount" with threshold { Mean between 50 and 500 },
  ColumnStatistics "amount" with threshold { StdDev < 1000 },

  # Freshness
  DataFreshness "updated_at" <= 2 hours,

  # Custom SQL rule
  CustomSql "SELECT COUNT(*) FROM primary WHERE order_date > CURRENT_DATE" = 0,

  # Row count
  RowCount >= 1000,
  RowCountMatch "orders_staging" >= 0.999
]
        """)

        st.subheader("Glue DQ – Quarantine Bad Records")
        st.code('''
from awsgluedi.transforms import *

RULESET = """
    Rules = [
        Completeness "order_id" >= 0.99,
        ColumnValues "amount" between 0 and 1000000
    ]
"""

# Apply DQ rules and route good/bad records separately
dq_results = EvaluateDataQuality.apply(
    frame=input_dyf,
    ruleset=RULESET,
    publishing_options={
        "dataQualityEvaluationContext": "order_quality_check",
        "enableDataQualityCloudWatchMetrics": True,
        "enableDataQualityResultsPublishing": True,
    },
    additional_options={"observations.scope": "ALL"},
)

good_records = SelectFromCollection.apply(dq_results, "primary")
bad_records  = SelectFromCollection.apply(dq_results, "failed_records")

# Good records → curated, bad records → quarantine
glueContext.write_dynamic_frame.from_options(good_records, "s3", {"path": "s3://lake/curated/orders/"})
glueContext.write_dynamic_frame.from_options(bad_records,  "s3", {"path": "s3://lake/quarantine/orders/"})
        ''', language="python")

    with tab3:
        st.header("Security Patterns")
        st.subheader("Encryption Strategy")
        df = pd.DataFrame({
            "Layer":          ["S3 (at rest)", "S3 (in transit)", "Redshift (at rest)", "Redshift (in transit)", "Kinesis (at rest)", "MSK (in transit)", "Glue connections", "Secrets"],
            "Recommendation": ["SSE-KMS with customer-managed key + Bucket Key", "HTTPS enforced via bucket policy", "KMS cluster encryption", "SSL required via parameter group", "KMS encryption", "TLS between brokers and clients", "SSL certificates in Secrets Manager", "Secrets Manager with auto-rotation"],
            "Terraform key":  ["`sse_algorithm = aws:kms`", "`aws:SecureTransport` condition", "`encrypted = true`", "`require_ssl = true`", "`encryption_type = KMS`", "`encryption_in_transit`", "VPC + SG isolation", "aws_secretsmanager_secret_rotation"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("S3 Bucket Policy – Enforce HTTPS + Restrict to Org")
        hcl("""
resource "aws_s3_bucket_policy" "lake_secure" {
  bucket = aws_s3_bucket.lake.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "DenyHTTP"
        Effect    = "Deny"
        Principal = "*"
        Action    = "s3:*"
        Resource  = ["${aws_s3_bucket.lake.arn}", "${aws_s3_bucket.lake.arn}/*"]
        Condition = { Bool = { "aws:SecureTransport" = "false" } }
      },
      {
        Sid       = "AllowOrgOnly"
        Effect    = "Allow"
        Principal = "*"
        Action    = ["s3:GetObject", "s3:PutObject", "s3:ListBucket"]
        Resource  = ["${aws_s3_bucket.lake.arn}", "${aws_s3_bucket.lake.arn}/*"]
        Condition = { StringEquals = { "aws:PrincipalOrgID" = var.org_id } }
      }
    ]
  })
}
        """)

    with tab4:
        st.header("Audit & Compliance")
        st.markdown("""
**CloudTrail + S3 Access Logs = full audit trail**

| Log Type | Coverage | Latency | Cost |
|----------|---------|---------|------|
| CloudTrail Management | API calls (CreateBucket, PutBucketPolicy…) | ~15 min | Free (1 trail) |
| CloudTrail Data Events | S3 GetObject, PutObject per-object | ~15 min | $0.10/100K events |
| S3 Access Logs | All HTTP requests to bucket | Minutes | Storage cost only |
| Redshift Audit Logs | Queries, connections, user activity | Near-real-time | Storage cost only |
| Lake Formation audit | Data access decisions | Near-real-time | Free |
        """)
        tip("Send all logs to a centralized **Security Account** S3 bucket with Object Lock (WORM) — ensures logs can't be tampered with.")
        warn("CloudTrail Data Events on large S3 buckets can generate millions of events/day — use selective prefixes or S3 Access Logs instead.")

# ════════════════════════════════════════════════════════════════════════════
# ANALYTICS & BI
# ════════════════════════════════════════════════════════════════════════════
elif section == "📊 Analytics & BI – QuickSight, OpenSearch, SageMaker":
    st.title("📊 Analytics & BI")
    tab1, tab2, tab3 = st.tabs(
        ["Amazon QuickSight", "Amazon OpenSearch", "SageMaker (Data Eng)"])

    with tab1:
        st.header("Amazon QuickSight")
        st.subheader("SPICE – SuperFast Parallel In-memory Calculation Engine")
        df = pd.DataFrame({
            "Attribute":    ["Storage per user", "Refresh modes", "Query speed", "Max dataset size", "Supported sources", "Cost"],
            "Detail":       ["10 GB (Standard), unlimited (Enterprise)", "Full refresh or incremental", "Sub-second on SPICE, seconds on direct query", "Up to 500 GB per dataset (SPICE)", "S3, Athena, Redshift, Aurora, RDS, Salesforce, JIRA, 30+ more", "$9/user/mo (Standard), $18/user/mo (Enterprise)"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("Row-Level Security (RLS)")
        st.markdown("""
**RLS dataset** maps users/groups → row filter conditions. Users only see their allowed rows.

```
RLS Table: quicksight_rls_rules
┌──────────────────┬─────────┬──────────────┐
│ UserName/GroupName│ region  │ department   │
├──────────────────┼─────────┼──────────────┤
│ alice@co.com     │ us-east │ *            │ ← Alice sees all depts in us-east
│ bob@co.com       │ *       │ finance      │ ← Bob sees finance in all regions
│ analytics-team   │ *       │ *            │ ← Group sees everything
└──────────────────┴─────────┴──────────────┘
```
        """)

        st.subheader("ML Insights – Built-in")
        st.markdown("""
- **Anomaly Detection** — detects outliers in time-series metrics automatically  
- **Forecasting** — ML-based point forecast + confidence intervals  
- **Narratives** — auto-generates natural language summaries of charts  
- **What-if analysis** — slider-based parameter exploration  
- **Suggested Insights** — QuickSight suggests relevant analysis based on data shape  
        """)

        hcl("""
resource "aws_quicksight_data_source" "athena" {
  data_source_id = "athena-curated"
  aws_account_id = data.aws_caller_identity.current.account_id
  name           = "Athena Curated Layer"
  type           = "ATHENA"

  parameters {
    athena { work_group = aws_athena_workgroup.analytics.name }
  }

  permission {
    principal = "arn:aws:quicksight:us-east-1:${data.aws_caller_identity.current.account_id}:group/default/data-engineering"
    actions   = ["quicksight:DescribeDataSource","quicksight:DescribeDataSourcePermissions","quicksight:PassDataSource","quicksight:UpdateDataSource","quicksight:DeleteDataSource","quicksight:UpdateDataSourcePermissions"]
  }

  ssl_properties { disable_ssl = false }
}
        """)
        tip("Use **Embedded QuickSight** to embed dashboards in internal portals with user-specific RLS filtering.")
        warn("SPICE has a 500 GB/dataset limit — for larger datasets use Direct Query mode (slower but no size limit).")

    with tab2:
        st.header("Amazon OpenSearch Service")
        st.subheader("Data Engineering Use Cases")
        df = pd.DataFrame({
            "Use case":     ["Log analytics", "Full-text search", "Real-time dashboards", "Anomaly detection", "Clickstream analysis"],
            "Ingestion":    ["Firehose → OpenSearch", "Lambda → OpenSearch client", "Kinesis → Firehose → OpenSearch", "Built-in ML plugin", "MSK → Kafka connector → OpenSearch"],
            "Index strategy": ["1 index/day (ILM policy)", "1 index/domain", "Rollover alias", "Dedicated index", "Date-based rollover"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("Firehose → OpenSearch with S3 Backup")
        hcl("""
resource "aws_kinesis_firehose_delivery_stream" "logs_to_opensearch" {
  name        = "logs-to-opensearch"
  destination = "opensearch"

  opensearch_configuration {
    domain_arn            = aws_opensearch_domain.logs.arn
    role_arn              = aws_iam_role.firehose.arn
    index_name            = "app-logs"
    index_rotation_period = "OneDay"
    buffering_interval    = 60
    buffering_size        = 5

    s3_backup_mode = "FailedDocumentsOnly"

    s3_configuration {
      role_arn   = aws_iam_role.firehose.arn
      bucket_arn = aws_s3_bucket.lake.arn
      prefix     = "opensearch-backup/logs/"
    }
  }
}
        """)

    with tab3:
        st.header("SageMaker for Data Engineers")
        st.subheader("Feature Store – ML Feature Management")
        st.markdown("""
**SageMaker Feature Store** is a managed repository for ML features with two stores:
- **Online store (Redis)** — low-latency (<10ms) feature serving for real-time inference  
- **Offline store (S3 + Glue Catalog)** — historical features for training, queryable via Athena  
        """)
        py("""
import boto3
import sagemaker
from sagemaker.feature_store.feature_group import FeatureGroup

sess = sagemaker.Session()

feature_group = FeatureGroup(name="customer-features", sagemaker_session=sess)
feature_group.load_feature_definitions(data_frame=customers_df)

feature_group.create(
    s3_uri="s3://my-lake/feature-store/",
    record_identifier_name="customer_id",
    event_time_feature_name="event_time",
    role_arn="arn:aws:iam::123456789:role/SageMakerRole",
    enable_online_store=True,
    description="Customer-level features: LTV, churn score, segment",
)

feature_group.ingest(data_frame=customers_df, max_workers=4, wait=True)

# Query offline store via Athena
athena_query = feature_group.athena_query()
athena_query.run(
    query_string=(
        'SELECT customer_id, ltv, churn_probability, segment '
        'FROM "sagemaker_featurestore"."customer-features-1234567890" '
        "WHERE write_time > (NOW() - INTERVAL '7' DAY) "
        "ORDER BY write_time DESC"
    ),
    output_location="s3://my-lake/athena-results/"
)
result_df = athena_query.as_dataframe()
        """)
        st.subheader("SageMaker Processing Jobs – Large-Scale Data Prep")
        py("""
from sagemaker.processing import ScriptProcessor, ProcessingInput, ProcessingOutput
from sagemaker import get_execution_role

processor = ScriptProcessor(
    image_uri='123456789.dkr.ecr.us-east-1.amazonaws.com/spark-processing:latest',
    command=['python3'],
    instance_type='ml.m5.4xlarge',
    instance_count=4,
    role=get_execution_role(),
    volume_size_in_gb=100,
)

processor.run(
    code='preprocess.py',
    inputs=[
        ProcessingInput(source='s3://my-lake/raw/events/', destination='/opt/ml/processing/input/')
    ],
    outputs=[
        ProcessingOutput(source='/opt/ml/processing/output/', destination='s3://my-lake/processed/events/')
    ],
    arguments=['--date', '2024-01-15'],
)
        """)
        tip("Use SageMaker Processing for ML-specific preprocessing that doesn't fit in Glue/EMR — handles custom Docker images, GPU instances.")

# ════════════════════════════════════════════════════════════════════════════
# dbt ON AWS
# ════════════════════════════════════════════════════════════════════════════
elif section == "🔄 dbt on AWS":
    st.title("🔄 dbt on AWS")
    tab1, tab2, tab3, tab4 = st.tabs(
        ["dbt Overview", "dbt Adapters", "Models & Macros", "CI/CD & Testing"])

    with tab1:
        st.header("dbt (data build tool) Overview")
        st.markdown("""
**dbt** is the transformation layer of the modern data stack. It runs SQL `SELECT` statements and handles:
- Model materializations (table, view, incremental, ephemeral)
- Testing (schema + data tests)
- Documentation & lineage
- Jinja templating + macros
- Snapshots (SCD Type 2)

**dbt Core vs dbt Cloud on AWS:**
        """)
        df = pd.DataFrame({
            "Feature":       ["Hosting", "Scheduler", "IDE", "CI/CD", "Cost", "AWS integration"],
            "dbt Core":      ["Self-hosted (MWAA, ECS, Lambda)", "MWAA DAG / Step Functions", "VS Code + dbt extension", "GitHub Actions / CodePipeline", "Free (OSS)", "Full control, any runner"],
            "dbt Cloud":     ["SaaS", "Built-in scheduler", "dbt Cloud IDE", "Native CI/CD jobs", "$50/seat/mo (Teams)", "Managed, less control"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)
        tip("Run **dbt Core on MWAA** (most common enterprise pattern) or on **AWS CodeBuild** for CI runs.")

    with tab2:
        st.header("dbt Adapters for AWS")
        df = pd.DataFrame({
            "Adapter":          ["dbt-redshift", "dbt-athena", "dbt-spark (Glue)", "dbt-trino (Athena v3)"],
            "Target":           ["Redshift / Redshift Serverless", "Athena v2 + v3", "Glue Interactive Sessions / EMR", "Athena v3 Trino engine"],
            "Iceberg support":  ["✅ (via Spectrum)", "✅ Native", "✅ via Spark", "✅ Native"],
            "Best for":         ["DWH transformations", "S3 lake transforms", "Spark-native transforms", "Lakehouse SQL transforms"],
            "Install":          ["`pip install dbt-redshift`", "`pip install dbt-athena-community`", "`pip install dbt-spark`", "`pip install dbt-trino`"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("dbt profiles.yml – Redshift + Athena")
        bash("""
# ~/.dbt/profiles.yml
data_platform:
  outputs:
    # Redshift Serverless target
    redshift_prod:
      type: redshift
      method: iam
      cluster_id: primary                          # workgroup name for serverless
      host: primary.123456789.us-east-1.redshift-serverless.amazonaws.com
      port: 5439
      database: datawarehouse
      schema: dbt_prod
      iam_duration_seconds: 900
      threads: 8
      keepalives_idle: 240
      search_path: dbt_prod,public

    # Athena target (Iceberg lakehouse)
    athena_prod:
      type: athena
      region_name: us-east-1
      s3_staging_dir: s3://my-lake/athena-results/dbt/
      s3_data_dir: s3://my-lake/curated/dbt/
      database: curated
      schema: dbt_prod
      threads: 4
      lf_tags_database: { domain: finance, sensitivity: internal }

  target: redshift_prod
        """)

    with tab3:
        st.header("Models, Macros & Snapshots")
        st.subheader("Incremental Model (Iceberg + Merge)")
        bash("""
-- models/curated/orders.sql
{{
  config(
    materialized = 'incremental',
    incremental_strategy = 'merge',   -- 'append' | 'merge' | 'delete+insert'
    unique_key = 'order_id',
    on_schema_change = 'sync_all_columns',
    file_format = 'iceberg',          -- Athena adapter
    table_type = 'iceberg',
    s3_data_dir = 's3://my-lake/curated/orders/',
    partitioned_by = ['days(order_ts)'],
    tblproperties = {
      'write.format.default': 'parquet',
      'write.parquet.compression-codec': 'snappy'
    }
  )
}}

SELECT
    order_id,
    customer_id,
    amount_usd,
    status,
    order_ts,
    updated_at,
    {{ dbt_utils.generate_surrogate_key(['order_id']) }} AS order_sk
FROM {{ source('raw', 'orders') }}

{% if is_incremental() %}
  -- Only process records updated since last run
  WHERE updated_at > (SELECT max(updated_at) FROM {{ this }})
{% endif %}
        """)

        st.subheader("SCD Type 2 Snapshot")
        bash("""
-- snapshots/customer_snapshot.sql
{% snapshot customer_snapshot %}
{{
  config(
    target_schema = 'snapshots',
    strategy = 'timestamp',
    unique_key = 'customer_id',
    updated_at = 'updated_at',
    invalidate_hard_deletes = True,
  )
}}
SELECT customer_id, email, country, plan, updated_at
FROM {{ source('raw', 'customers') }}
{% endsnapshot %}
        """)

        st.subheader("Useful Macros")
        bash("""
-- macros/generate_schema_name.sql (control schema per environment)
{% macro generate_schema_name(custom_schema_name, node) -%}
  {%- set default_schema = target.schema -%}
  {%- if custom_schema_name is none -%}
    {{ default_schema }}
  {%- else -%}
    {{ default_schema }}_{{ custom_schema_name | trim }}
  {%- endif -%}
{%- endmacro %}

-- macros/mask_pii.sql
{% macro mask_email(column_name) %}
  CASE
    WHEN {{ env_var('DBT_MASK_PII', 'false') }} = 'true'
    THEN CONCAT(LEFT({{ column_name }}, 2), '***@***.***')
    ELSE {{ column_name }}
  END
{% endmacro %}

-- Usage in model:
-- {{ mask_email('email') }} AS email
        """)

    with tab4:
        st.header("dbt Testing & CI/CD")
        st.subheader("dbt Tests")
        bash("""
# schema.yml — built-in tests
models:
  - name: orders
    description: "Fact table for all orders"
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: status
        tests:
          - accepted_values:
              values: ['PENDING', 'COMPLETED', 'CANCELLED']
      - name: customer_id
        tests:
          - relationships:
              to: ref('customers')
              field: customer_id
      - name: amount_usd
        tests:
          - dbt_utils.expression_is_true:
              expression: ">= 0"

# custom data test (tests/assert_orders_not_future_dated.sql)
# Fails if any rows returned
SELECT order_id, order_ts
FROM {{ ref('orders') }}
WHERE order_ts > CURRENT_TIMESTAMP
        """)

        st.subheader("GitHub Actions CI/CD for dbt on AWS")
        bash("""
# .github/workflows/dbt_ci.yml
name: dbt CI
on: [pull_request]
jobs:
  dbt-ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/GitHubActionsDBT
          aws-region: us-east-1

      - name: Install dbt
        run: pip install dbt-athena-community dbt-utils

      - name: dbt compile (syntax check)
        run: dbt compile --profiles-dir .dbt/ --target ci

      - name: dbt test on staging schema
        run: |
          dbt run --target ci --select state:modified+   # only changed models
          dbt test --target ci --select state:modified+

      - name: dbt docs generate
        run: dbt docs generate --target ci
        """)
        tip("Use `dbt run --select state:modified+` in CI to only run changed models and their downstream dependents — much faster than full runs.")
        warn("Never run `dbt run --full-refresh` in production without a rollback plan — it drops and recreates the target table.")

# ════════════════════════════════════════════════════════════════════════════
# COMPARISONS
# ════════════════════════════════════════════════════════════════════════════
elif section == "⚖️ Comparisons":
    st.title("⚖️ Comparisons")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["Lake vs WH vs Lakehouse", "Processing", "Streaming", "Storage Formats", "Orchestration", "When to use what"])

    with tab1:
        st.header("Lake vs Warehouse vs Lakehouse")
        df = pd.DataFrame({
            "Dimension":       ["Storage", "Schema", "ACID", "Query perf", "Cost", "Flexibility", "Compute", "Best for"],
            "Data Lake":       ["S3", "On-read", "❌ (w/o OTF)", "Medium", "Very low", "Very high", "Glue/EMR/Athena", "Raw storage, ML, exploration, archive"],
            "Data Warehouse":  ["Managed (Redshift)", "On-write", "✅", "High", "High", "Low", "Redshift MPP", "Structured BI, dashboards, finance reporting"],
            "Data Lakehouse":  ["S3 (Iceberg/Hudi)", "On-write+read", "✅", "High", "Low-medium", "High", "Multi-engine", "Unified platform, streaming+batch, ML+BI"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        st.header("Processing Engine Comparison")
        df = pd.DataFrame({
            "Dimension":    ["Infra", "Language", "Scale", "Startup", "Cost model", "Iceberg support", "Best workload"],
            "Glue":         ["Serverless", "PySpark, Python, Ray", "Auto", "2–5 min", "DPU-hour", "✅ Native", "Managed ETL, small-medium data"],
            "EMR EC2":      ["EC2 cluster", "Spark, Hive, Flink, Presto", "Manual/fleet", "5–15 min", "Instance+EMR%", "✅ Full", "Full Spark control, Spot savings"],
            "EMR Serverless": ["Serverless", "Spark, Hive", "Auto", "~30s (pre-init)", "vCPU-sec", "✅ Full", "Batch jobs, no ops overhead"],
            "Redshift":     ["Managed MPP", "SQL only", "Node/RPU", "Always on", "Node-hr/RPU", "Via Spectrum", "BI queries, structured analytics"],
            "Athena":       ["Serverless Trino", "SQL (Trino)", "Auto", "Instant", "$/TB scanned", "✅ Native", "Ad-hoc queries, infrequent, S3"],
            "Lambda":       ["Serverless", "Python, Node, Java…", "Auto (concurrency)", "Cold: 100ms-2s", "Per invocation", "❌ (via boto3)", "Event-driven, lightweight transforms"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab3:
        st.header("Streaming Services Comparison")
        df = pd.DataFrame({
            "Dimension":    ["Protocol", "Partition/Shard", "Ordering", "Replay", "Retention", "Fan-out", "Ecosystem", "Cost model", "Best for"],
            "KDS":          ["Kinesis SDK", "Shard-based", "Per shard", "✅ 1h–365d", "Up to 1 year", "Enhanced Fan-Out", "AWS-native", "Per shard-hr + PUT", "AWS-native streaming, simple consumers"],
            "MSK (Kafka)":  ["Kafka native", "Partition-based", "Per partition", "✅ Unlimited", "Configurable (days–TB)", "Consumer groups", "Kafka ecosystem (Connect, Streams)", "Broker instance+storage", "Kafka shops, complex topologies"],
            "Firehose":     ["HTTP/SDK", "Managed", "No ordering", "❌", "Buffer only", "1 destination", "AWS delivery only", "Per GB ingested+processed", "Log/event → S3/Redshift/ES"],
            "SQS":          ["HTTP/SDK", "Queue-based", "FIFO optional", "❌ (14d max)", "14 days", "1 consumer (std)", "Simple decoupling", "Per million requests", "Task queues, decoupling, retry"],
            "EventBridge":  ["Event-driven", "N/A", "No ordering", "❌", "None (fire+forget)", "Rules-based fan-out", "AWS events + SaaS", "Per event", "Event routing, triggers, SaaS"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab4:
        st.header("Storage Format Comparison")
        df = pd.DataFrame({
            "Format":         ["CSV", "JSON", "Avro", "Parquet", "ORC", "Parquet+Iceberg", "Parquet+Delta"],
            "Columnar":       ["❌", "❌", "❌", "✅", "✅", "✅", "✅"],
            "Schema":         ["None", "Flexible", "Enforced", "Optional", "Optional", "Enforced", "Enforced"],
            "Compression":    ["Low", "Low", "Good", "Excellent", "Excellent", "Excellent", "Excellent"],
            "Splittable":     ["✅", "With care", "✅", "✅", "✅", "✅", "✅"],
            "ACID":           ["❌", "❌", "❌", "❌", "❌", "✅", "✅"],
            "Athena support": ["✅", "✅", "✅", "✅", "✅", "✅", "✅ (partial)"],
            "Best for":       ["Import/export", "APIs, logs", "Kafka streams", "Analytics", "Hive/EMR", "Lakehouse", "Databricks"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab5:
        st.header("Orchestration Comparison")
        df = pd.DataFrame({
            "Dimension":     ["Model", "Interface", "Scheduling", "Complexity", "Cost", "AWS integration", "Best for"],
            "MWAA":          ["DAG (Airflow)", "Web UI + code", "Cron + sensors", "High", "Fixed env cost", "Rich (AWS providers)", "Complex multi-step pipelines, sensor-based"],
            "Step Functions": ["State machine", "Visual + JSON", "EventBridge", "Medium", "Per state transition", "Native AWS", "AWS-service orchestration, callbacks"],
            "EventBridge":   ["Event rules", "Console/IaC", "Cron or event", "Low", "Per event", "Native AWS", "Triggers, routing, fan-out"],
            "Lambda (cron)": ["Function", "Code only", "EventBridge rule", "Low", "Per invocation", "Native AWS", "Simple one-step scheduled jobs"],
            "CodePipeline":  ["Pipeline stages", "Console/IaC", "Commit/S3/manual", "Low", "Per pipeline", "CI/CD focused", "dbt CI/CD, Glue script deployment"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab6:
        st.header("Decision Guide: When to Use What")
        df = pd.DataFrame({
            "Scenario":                              ["Need to query S3 data ad-hoc", "Need to ETL 10TB+ daily", "Need near-real-time dashboard (5min lag)", "Need < 1s streaming analytics", "Need to ingest from Salesforce", "Need CDC from PostgreSQL", "Need ML feature serving", "Need enterprise governance at scale", "Need to run Airflow DAGs", "Need serverless scheduled SQL"],
            "Recommended":                           ["Athena v3 + Iceberg", "EMR Serverless or Glue G.2X+", "Kinesis → Firehose → S3 → Athena", "MSK + Flink on EMR Serverless", "AppFlow", "DMS CDC or Debezium on MSK Connect", "SageMaker Feature Store", "Lake Formation + LF-TBAC", "MWAA", "Step Functions + EventBridge Scheduler"],
            "Why":                                   ["Serverless, no infra, pay per query", "Better cost/performance than Glue at scale", "Managed, no consumers to write", "Sub-second processing with full Kafka ecosystem", "No-code, built-in Salesforce connector", "Purpose-built for DB replication", "Dual online/offline store, Athena queryable", "Scales to 1000s of tables with tag policies", "Rich DAG model, Airflow compatibility", "No Airflow overhead for simple schedules"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════
# IaC – TERRAFORM
# ════════════════════════════════════════════════════════════════════════════
elif section == "🏗️ IaC – Terraform Modules":
    st.title("🏗️ IaC – Terraform Modules")
    tab1, tab2, tab3, tab4 = st.tabs(
        ["S3 Data Lake Module", "Glue + EMR Module", "Redshift + Kinesis Pipeline", "MWAA Module"])

    with tab1:
        st.header("S3 Data Lake Module")
        hcl("""
# modules/s3_data_lake/main.tf
locals {
  zones = toset(["raw", "curated", "consumption", "quarantine"])
}

resource "aws_s3_bucket" "zones" {
  for_each = local.zones
  bucket   = "${var.prefix}-lake-${each.key}-${var.env}"
  tags     = merge(var.tags, { Zone = each.key })
}

resource "aws_s3_bucket_public_access_block" "zones" {
  for_each                = aws_s3_bucket.zones
  bucket                  = each.value.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "zones" {
  for_each = aws_s3_bucket.zones
  bucket   = each.value.id
  rule {
    bucket_key_enabled = true
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = var.kms_key_arn
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "raw" {
  bucket = aws_s3_bucket.zones["raw"].id
  rule {
    id = "raw-tiering"; status = "Enabled"
    filter {}
    transition { days = 30;  storage_class = "STANDARD_IA" }
    transition { days = 90;  storage_class = "GLACIER_IR" }
    transition { days = 365; storage_class = "DEEP_ARCHIVE" }
    abort_incomplete_multipart_upload { days_after_initiation = 7 }
  }
}

resource "aws_s3_bucket_notification" "all" {
  for_each    = aws_s3_bucket.zones
  bucket      = each.value.id
  eventbridge = true
}

output "bucket_ids"  { value = { for k,v in aws_s3_bucket.zones : k => v.id } }
output "bucket_arns" { value = { for k,v in aws_s3_bucket.zones : k => v.arn } }
        """)

    with tab2:
        st.header("Glue + EMR Serverless Module")
        hcl("""
# modules/data_processing/main.tf

# ── Glue ────────────────────────────────────────────────
resource "aws_glue_catalog_database" "dbs" {
  for_each = toset(["raw_${var.env}", "curated_${var.env}", "gold_${var.env}"])
  name     = each.key
}

resource "aws_glue_job" "etl" {
  for_each         = var.glue_jobs   # map of job_name → config
  name             = "${var.prefix}-${each.key}-${var.env}"
  role_arn         = aws_iam_role.glue.arn
  glue_version     = "4.0"
  worker_type      = each.value.worker_type
  number_of_workers= each.value.workers

  command {
    name            = "glueetl"
    script_location = "s3://${var.scripts_bucket}/${each.value.script}"
    python_version  = "3"
  }

  default_arguments = merge(
    {
      "--job-bookmark-option"            = "job-bookmark-enable"
      "--enable-metrics"                 = "true"
      "--enable-continuous-cloudwatch-log" = "true"
      "--enable-glue-datacatalog"        = "true"
      "--datalake-formats"               = "iceberg"
      "--TempDir"                        = "s3://${var.scripts_bucket}/glue-temp/"
    },
    each.value.extra_args
  )

  execution_property { max_concurrent_runs = each.value.max_concurrent_runs }
  timeout = 2880   # 48 hours
}

# ── EMR Serverless ──────────────────────────────────────
resource "aws_emrserverless_application" "spark" {
  name          = "${var.prefix}-spark-${var.env}"
  release_label = var.emr_release  # "emr-7.2.0"
  type          = "SPARK"

  initial_capacity {
    initial_capacity_type = "Executor"
    initial_capacity_config {
      worker_count = var.emr_initial_executors
      worker_configuration { cpu = "4vCPU"; memory = "16gb"; disk = "20gb" }
    }
  }

  maximum_capacity {
    cpu    = "${var.emr_max_cpu}vCPU"
    memory = "${var.emr_max_memory}gb"
    disk   = "${var.emr_max_disk}gb"
  }

  auto_stop_configuration {
    enabled              = true
    idle_timeout_minutes = var.emr_idle_timeout_minutes
  }

  network_configuration {
    security_group_ids = [aws_security_group.emr.id]
    subnet_ids         = var.private_subnet_ids
  }
}

output "glue_job_names"   { value = { for k,v in aws_glue_job.etl : k => v.name } }
output "emr_app_id"       { value = aws_emrserverless_application.spark.id }
output "glue_db_names"    { value = { for k,v in aws_glue_catalog_database.dbs : k => v.name } }
        """)

    with tab3:
        st.header("Redshift Serverless + Kinesis Pipeline")
        hcl("""
# ── Kinesis ─────────────────────────────────────────────
resource "aws_kinesis_stream" "events" {
  name             = "${var.prefix}-events-${var.env}"
  shard_count      = var.kinesis_shards
  retention_period = var.kinesis_retention_hours
  encryption_type  = "KMS"
  kms_key_id       = var.kms_key_arn
  stream_mode_details { stream_mode = var.kinesis_on_demand ? "ON_DEMAND" : "PROVISIONED" }
}

resource "aws_kinesis_firehose_delivery_stream" "raw_s3" {
  name        = "${var.prefix}-firehose-raw-${var.env}"
  destination = "extended_s3"

  kinesis_source_configuration {
    kinesis_stream_arn = aws_kinesis_stream.events.arn
    role_arn           = aws_iam_role.firehose.arn
  }

  extended_s3_configuration {
    role_arn           = aws_iam_role.firehose.arn
    bucket_arn         = var.raw_bucket_arn
    prefix             = "events/dt=!{timestamp:yyyy-MM-dd}/"
    error_output_prefix= "errors/firehose/!{firehose:error-output-type}/dt=!{timestamp:yyyy-MM-dd}/"
    buffering_size     = 128
    buffering_interval = 300
    compression_format = "SNAPPY"
  }
}

# ── Redshift Serverless ─────────────────────────────────
resource "aws_redshiftserverless_namespace" "main" {
  namespace_name      = "${var.prefix}-${var.env}"
  admin_username      = var.redshift_admin_user
  admin_user_password = var.redshift_admin_password
  db_name             = "datawarehouse"
  kms_key_id          = var.kms_key_arn
  iam_roles           = [aws_iam_role.redshift.arn]
  log_exports         = ["userlog", "connectionlog", "useractivitylog"]
}

resource "aws_redshiftserverless_workgroup" "main" {
  namespace_name     = aws_redshiftserverless_namespace.main.namespace_name
  workgroup_name     = "${var.prefix}-${var.env}"
  base_capacity      = var.redshift_base_rpu
  enhanced_vpc_routing = true
  subnet_ids         = var.private_subnet_ids
  security_group_ids = [aws_security_group.redshift.id]

  config_parameter { parameter_key = "max_query_execution_time"; parameter_value = "3600" }
  config_parameter { parameter_key = "require_ssl";              parameter_value = "true"  }
}

resource "aws_redshiftserverless_usage_limit" "daily" {
  resource_arn  = aws_redshiftserverless_workgroup.main.arn
  usage_type    = "serverless-compute"
  amount        = var.redshift_daily_rpu_limit
  period        = "daily"
  breach_action = "emit-metric"  # or "deactivate"
}

output "kinesis_stream_arn"  { value = aws_kinesis_stream.events.arn }
output "redshift_endpoint"   { value = aws_redshiftserverless_workgroup.main.endpoint }
output "redshift_workgroup"  { value = aws_redshiftserverless_workgroup.main.workgroup_name }
        """)

    with tab4:
        st.header("MWAA Module")
        hcl("""
# modules/mwaa/main.tf
resource "aws_s3_bucket" "mwaa" {
  bucket = "${var.prefix}-mwaa-${var.env}"
  tags   = var.tags
}

resource "aws_s3_bucket_versioning" "mwaa" {
  bucket = aws_s3_bucket.mwaa.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_mwaa_environment" "main" {
  name               = "${var.prefix}-airflow-${var.env}"
  airflow_version    = var.airflow_version   # "2.10.3"
  environment_class  = var.environment_class # "mw1.medium"
  min_workers        = var.min_workers
  max_workers        = var.max_workers
  execution_role_arn = aws_iam_role.mwaa.arn
  source_bucket_arn  = aws_s3_bucket.mwaa.arn
  dag_s3_path        = "dags/"
  requirements_s3_path  = "requirements.txt"
  plugins_s3_path       = "plugins.zip"

  network_configuration {
    security_group_ids = [aws_security_group.mwaa.id]
    subnet_ids         = var.private_subnet_ids  # min 2 AZs
  }

  logging_configuration {
    dag_processing_logs { enabled = true; log_level = "INFO"    }
    scheduler_logs      { enabled = true; log_level = "WARNING" }
    task_logs           { enabled = true; log_level = "INFO"    }
    webserver_logs      { enabled = true; log_level = "ERROR"   }
    worker_logs         { enabled = true; log_level = "INFO"    }
  }

  airflow_configuration_options = {
    "core.parallelism"                  = tostring(var.max_workers * 5)
    "core.dag_concurrency"              = tostring(var.max_workers * 2)
    "scheduler.catchup_by_default"      = "False"
    "secrets.backend"                   = "airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend"
    "secrets.backend_kwargs"            = jsonencode({ "connections_prefix" = "airflow/connections", "variables_prefix" = "airflow/variables" })
  }

  webserver_access_mode = "PUBLIC_ONLY"   # or PRIVATE_ONLY for VPN-only access
  tags = var.tags
}

output "webserver_url" { value = aws_mwaa_environment.main.webserver_url }
output "mwaa_arn"      { value = aws_mwaa_environment.main.arn }
        """)

# ════════════════════════════════════════════════════════════════════════════
# MODERN PATTERNS
# ════════════════════════════════════════════════════════════════════════════
elif section == "🚀 Modern Patterns":
    st.title("🚀 Modern Patterns")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Zero-ETL", "S3 Tables", "Streaming Lakehouse", "Data Sharing", "Federated Query"])

    with tab1:
        st.header("Zero-ETL")
        df = pd.DataFrame({
            "Source":            ["Aurora MySQL", "Aurora PostgreSQL", "RDS MySQL", "DynamoDB", "Salesforce (preview)", "S3 → Redshift (auto-copy)"],
            "Target":            ["Redshift", "Redshift", "Redshift", "Redshift", "Redshift", "Redshift"],
            "Latency":           ["Seconds", "Seconds", "Seconds", "Seconds", "Near-real-time", "Minutes"],
            "Setup":             ["1 API call", "1 API call", "1 API call", "1 API call", "Console", "S3 → Redshift COPY schedule"],
            "Transformation":    ["❌ Raw only", "❌ Raw only", "❌ Raw only", "❌ Raw only", "❌ Raw only", "❌ Raw only"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)
        info("Zero-ETL removes the replication infrastructure but NOT transformation. You still need dbt/Redshift stored procedures for business logic.")

    with tab2:
        st.header("S3 Tables (Table Buckets)")
        st.markdown("""
**Nov 2024:** AWS launched S3 Table Buckets — S3 native Iceberg tables with automatic maintenance.

**Auto-managed by AWS:**
- File compaction (maintains 128MB+ file sizes)
- Snapshot expiry
- Orphan file cleanup
- Manifest rewrites
- Up to **3x faster queries** and **10x faster compaction** vs self-managed Iceberg (AWS benchmarks)
        """)
        hcl("""
# S3 Table Bucket — entirely new resource type
resource "aws_s3tables_table_bucket" "analytics" {
  name = "${var.prefix}-iceberg-${var.env}"
  maintenance_configuration {
    iceberg_unreferenced_file_removal {
      status = "Enabled"
      settings {
        non_current_days         = 3
        unreferenced_days        = 3
      }
    }
  }
}

resource "aws_s3tables_namespace" "curated" {
  table_bucket_arn = aws_s3tables_table_bucket.analytics.arn
  namespace        = ["curated"]
}

resource "aws_s3tables_table" "orders" {
  table_bucket_arn = aws_s3tables_table_bucket.analytics.arn
  namespace        = aws_s3tables_namespace.curated.namespace
  name             = "orders"
  format           = "ICEBERG"
}

# Grant access via Lake Formation
resource "aws_lakeformation_permissions" "s3tables_analyst" {
  principal   = aws_iam_role.analyst.arn
  permissions = ["SELECT"]
  table {
    database_name = "curated"
    name          = "orders"
    catalog_id    = "${data.aws_caller_identity.current.account_id}:s3tablescatalog/${aws_s3tables_table_bucket.analytics.name}"
  }
}
        """)

    with tab3:
        st.header("Streaming Lakehouse")
        st.markdown("""
Write streaming data directly to Iceberg tables — no separate batch reconciliation layer.

**Pattern comparison:**
| Approach | Write path | Read path | Consistency |
|----------|-----------|----------|-------------|
| Traditional | Stream → S3 raw → Glue batch → Iceberg | Iceberg | Hourly at best |
| Streaming Lakehouse | Stream → Glue Streaming → Iceberg MERGE | Iceberg | Minutes |
| Ultra-low latency | MSK → Flink (EMR Serverless) → Iceberg | Iceberg | Seconds |
        """)
        py("""
# Flink on EMR Serverless → Iceberg streaming (SQL API)
flink_sql = \"\"\"
-- Create Kafka source
CREATE TABLE kafka_events (
    event_id    STRING,
    user_id     STRING,
    event_type  STRING,
    amount      DOUBLE,
    event_ts    TIMESTAMP(3),
    WATERMARK FOR event_ts AS event_ts - INTERVAL '5' SECOND
) WITH (
    'connector'             = 'kafka',
    'topic'                 = 'user-events',
    'properties.bootstrap.servers' = 'broker:9092',
    'format'                = 'json',
    'scan.startup.mode'     = 'latest-offset'
);

-- Create Iceberg sink
CREATE TABLE iceberg_events (
    event_id   STRING,
    user_id    STRING,
    event_type STRING,
    amount     DOUBLE,
    event_ts   TIMESTAMP(3),
    event_date STRING
) PARTITIONED BY (event_date)
WITH (
    'connector'              = 'iceberg',
    'catalog-name'           = 'glue',
    'catalog-type'           = 'glue',
    'database-name'          = 'curated',
    'table-name'             = 'events',
    'write.format.default'   = 'parquet',
    'write.upsert.enabled'   = 'true'
);

-- Stream events into Iceberg with 1-minute windows
INSERT INTO iceberg_events
SELECT
    event_id, user_id, event_type, amount, event_ts,
    DATE_FORMAT(event_ts, 'yyyy-MM-dd') AS event_date
FROM kafka_events;
\"\"\"
        """)

    with tab4:
        st.header("Redshift Data Sharing")
        st.markdown("""
Share **live Redshift data** across clusters and accounts without data movement or ETL.

```
Producer Cluster/Namespace          Consumer Cluster/Namespace
┌──────────────────────┐           ┌─────────────────────────┐
│ DATASHARE ds_finance │──share──→ │ Mount as external schema │
│ ├── schema: finance  │           │ SELECT * FROM            │
│ │   ├── fact_revenue │           │ finance_shared.fact_revenue│
│ │   └── dim_product  │           └─────────────────────────┘
│ └── (live data)      │
└──────────────────────┘
```
        """)
        sql("""
-- Producer: create and populate datashare
CREATE DATASHARE ds_analytics PUBLICACCESSIBLE FALSE;
ALTER DATASHARE ds_analytics ADD SCHEMA analytics;
ALTER DATASHARE ds_analytics ADD ALL TABLES IN SCHEMA analytics;
ALTER DATASHARE ds_analytics ADD TABLE finance.fact_revenue;

-- Grant to another account
GRANT USAGE ON DATASHARE ds_analytics TO ACCOUNT '987654321098' VIA DATA CATALOG;

-- Consumer: mount as external database
CREATE DATABASE analytics_shared
FROM DATASHARE ds_analytics OF ACCOUNT '123456789012' NAMESPACE 'abc123-...';

-- Query shared data (no copy, live data)
SELECT month, sum(revenue) FROM analytics_shared.analytics.monthly_revenue GROUP BY 1;
        """)
        tip("Data Sharing is free for same-account sharing. Cross-account charges apply for compute on the consumer side.")

    with tab5:
        st.header("Federated Query Patterns")
        sql("""
-- Athena Federated: join RDS + S3 in one query
-- Requires Lambda connector for RDS
SELECT
    r.order_id,
    r.amount,
    c.email,
    e.event_count
FROM "lambda:rds_postgres".public.orders r
JOIN curated.customers c ON r.customer_id = c.customer_id
JOIN (
    SELECT user_id, count(*) event_count
    FROM curated.events
    WHERE dt >= '2024-01-01'
    GROUP BY user_id
) e ON r.customer_id = e.user_id
WHERE r.status = 'COMPLETED'
LIMIT 10000;

-- Redshift Federated: live join Redshift ↔ Aurora
CREATE EXTERNAL SCHEMA aurora
FROM POSTGRES
DATABASE 'app_db' SCHEMA 'public'
URI 'aurora-cluster.cluster-abc.us-east-1.rds.amazonaws.com'
IAM_ROLE 'arn:aws:iam::123456789:role/RedshiftFed'
SECRET_ARN 'arn:aws:secretsmanager:us-east-1:123456789:secret:aurora-creds';

SELECT w.order_id, w.amount, a.customer_email
FROM fact_orders w
JOIN aurora.customers a ON w.customer_id = a.customer_id
WHERE w.order_date >= current_date - 7;
        """)

# ════════════════════════════════════════════════════════════════════════════
# DEBUGGING
# ════════════════════════════════════════════════════════════════════════════
elif section == "🐛 Debugging & Troubleshooting":
    st.title("🐛 Debugging & Troubleshooting")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["AWS Glue", "Amazon EMR", "Amazon Redshift", "Athena", "Kinesis / MSK"])

    with tab1:
        st.header("Glue Debugging")
        df = pd.DataFrame({
            "Error / Symptom":             ["Job runs forever / OOM", "AnalysisException: table not found", "Job bookmark not working", "DynamicFrame missing columns", "S3 403 Access Denied", "Job hangs on Iceberg write", "Spark shuffle failure", "Glue job slow on small files"],
            "Likely cause":                ["Insufficient workers, data skew", "Table not registered in Glue Catalog", "Job run with DISABLE instead of ENABLE", "Mixed/null types in source", "Missing S3 permissions on IAM role", "Concurrent writers + small transaction conflict", "Insufficient shuffle partitions", "Too many small Parquet files"],
            "Fix":                         ["Add workers or use G.2X+, add repartition()", "Run Crawler or register table via Glue API/TF", "Set `--job-bookmark-option = job-bookmark-enable`", "Use ResolveChoice transform before converting", "Add s3:GetObject/PutObject/ListBucket to Glue role", "Increase `write.target-file-size-bytes`, reduce concurrency", "Set `spark.sql.shuffle.partitions` to 2-3× total cores", "Compact files first with Iceberg `rewrite_data_files`"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("Glue – Enable Continuous CloudWatch Logging")
        hcl("""
# In Glue job default_arguments:
"--enable-continuous-cloudwatch-log" = "true"
"--enable-continuous-log-filter"     = "true"   # filter driver-only (less noise)
"--continuous-log-logGroup"          = "/aws-glue/jobs/${var.job_name}"

# Then tail logs:
# aws logs tail /aws-glue/jobs/my-job --follow
        """)
        tip("Use Glue **Interactive Sessions** (Jupyter kernel) to debug PySpark interactively before submitting full jobs.")

    with tab2:
        st.header("EMR Debugging")
        df = pd.DataFrame({
            "Error":                          ["YARN ApplicationMaster OOM", "Spark executor lost (Spot interruption)", "GC overhead limit exceeded", "S3 slow performance", "Job killed: exceeded memory limit", "FileAlreadyExistsException (Iceberg)", "EMR bootstrap failed"],
            "Fix":                            ["Increase `spark.driver.memory`, use G.2X Master", "Retry logic in job, use task-level checkpointing", "Reduce executor memory fraction: `spark.memory.fraction=0.6`", "Use EMRFS consistent view, increase s3a connection pool", "Increase `spark.executor.memory` or reduce parallelism", "Check for concurrent writers, enable Iceberg optimistic CC", "Check bootstrap action script logs in /mnt/var/log/bootstrap-actions/"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        bash("""
# EMR — SSH into master node and check logs
ssh -i my-key.pem hadoop@<master-public-dns>

# YARN application logs
yarn logs -applicationId application_1234567890_0001

# Spark History Server (if enabled)
# Browse: http://<master-dns>:18080

# Check container logs
# /var/log/hadoop-yarn/containers/<app-id>/<container-id>/

# List failed applications
yarn application -list -appStates FAILED
        """)

    with tab3:
        st.header("Redshift Debugging")
        sql("""
-- Find long-running or stuck queries
SELECT pid, user_name, starttime,
       datediff(seconds, starttime, getdate()) elapsed_sec,
       trim(querytxt) query
FROM stv_recents WHERE status = 'Running'
ORDER BY elapsed_sec DESC;

-- Kill a query
SELECT pg_cancel_backend(<pid>);   -- graceful
SELECT pg_terminate_backend(<pid>); -- force

-- Find lock contention
SELECT a.pid, a.user_name, b.pid blocker_pid, a.query
FROM stv_recents a JOIN stv_locks b ON a.pid != b.pid;

-- Diagnose query plan (look for DS_DIST_ALL → huge redistribute)
EXPLAIN SELECT o.*, c.country FROM fact_orders o JOIN dim_customer c ON o.customer_sk = c.customer_sk;

-- Find tables needing vacuum
SELECT "table", size, unsorted, stats_off, tbl_rows
FROM svv_table_info
WHERE unsorted > 10 OR stats_off > 10
ORDER BY size DESC;

-- Query error details
SELECT pid, starttime, err_code, err_reason, trim(query)
FROM stl_error WHERE starttime > dateadd(hour, -24, getdate())
ORDER BY starttime DESC LIMIT 20;

-- WLM queue wait times
SELECT service_class, num_queued_queries, num_executing_queries, queue_execution_time
FROM stv_wlm_service_class_state WHERE service_class > 4;
        """)

    with tab4:
        st.header("Athena Debugging")
        df = pd.DataFrame({
            "Error":                                    ["HIVE_PARTITION_SCHEMA_MISMATCH", "GENERIC_INTERNAL_ERROR: S3 location not found", "Query timeout", "High cost per query", "MSCK REPAIR TABLE takes forever", "Iceberg table not found after Glue Crawler"],
            "Fix":                                      ["Schema changed after partition created — drop+recreate partition or use Iceberg", "S3 path in table definition doesn't exist — update table location", "Add LIMIT, use partitioning, break into smaller queries", "Switch to Parquet+Iceberg, add partition filter, use CTAS to pre-aggregate", "Never use MSCK on large tables — use `ALTER TABLE ADD PARTITION` or Iceberg crawlers", "Crawlers don't support Iceberg — register Iceberg tables via Glue API or Terraform"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        bash("""
# Athena CLI — check query execution details
aws athena get-query-execution --query-execution-id <id>

# Get query results
aws athena get-query-results --query-execution-id <id>

# Check data scanned (cost) for recent queries
aws athena list-query-executions --work-group analytics-team \
  --query 'QueryExecutionIds[*]' --output text | \
  head -20 | xargs -I{} aws athena get-query-execution \
  --query-execution-id {} \
  --query 'QueryExecution.Statistics.DataScannedInBytes'
        """)

    with tab5:
        st.header("Kinesis & MSK Debugging")
        df = pd.DataFrame({
            "Symptom":                              ["ProvisionedThroughputExceededException", "Iterator expired", "Consumer falling behind (high GetRecords.IteratorAgeMilliseconds)", "MSK consumer group lag", "MSK broker disk full", "Firehose delivery failures"],
            "Fix":                                  ["Add shards (UpdateShardCount), use KPL aggregation, retry with exponential backoff", "Shard iterator expires after 5 min idle — re-get iterator or use Enhanced Fan-Out", "Add consumers, use Enhanced Fan-Out (2MB/s per consumer per shard), scale app", "Check consumer lag in MSK metrics, scale consumers, check processing bottleneck", "Increase broker storage or enable auto-expand, implement topic retention limits", "Check S3 permissions on Firehose role, check error prefix path for failed records"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        bash("""
# KDS — check iterator age (lag indicator)
aws cloudwatch get-metric-statistics \
  --namespace AWS/Kinesis \
  --metric-name GetRecords.IteratorAgeMilliseconds \
  --dimensions Name=StreamName,Value=user-events \
  --start-time 2024-01-15T00:00:00Z --end-time 2024-01-15T01:00:00Z \
  --period 60 --statistics Maximum

# KDS — list shards and their hash key ranges
aws kinesis list-shards --stream-name user-events

# MSK — get consumer group lag (using kafka-consumer-groups.sh on a broker)
kafka-consumer-groups.sh \
  --bootstrap-server broker:9092 \
  --describe --group my-consumer-group

# Firehose — check delivery metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Firehose \
  --metric-name DeliveryToS3.Records \
  --dimensions Name=DeliveryStreamName,Value=events-to-s3 \
  --period 300 --statistics Sum \
  --start-time 2024-01-15T00:00:00Z --end-time 2024-01-15T01:00:00Z
        """)

# ════════════════════════════════════════════════════════════════════════════
# DATA MODELING
# ════════════════════════════════════════════════════════════════════════════
elif section == "📐 Data Modeling Patterns":
    st.title("📐 Data Modeling Patterns")
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Dimensional Modeling", "Medallion Architecture", "Data Vault 2.0", "Modeling on Iceberg"])

    with tab1:
        st.header("Dimensional Modeling")
        st.subheader("Star vs Snowflake vs OBT")
        df = pd.DataFrame({
            "Attribute":     ["Join complexity", "Query speed", "Storage", "Maintenance", "Best for"],
            "Star Schema":   ["1 join per dimension", "Fast (denorm dims)", "Medium", "Simple", "BI tools, Redshift"],
            "Snowflake":     ["Multiple joins per dim", "Slower (more joins)", "Low (normalized)", "Complex", "Normalized consistency"],
            "OBT (One Big Table)": ["0 joins", "Fastest reads", "High (duplication)", "Denorm on write", "Analytics, Athena"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("SCD Type 2 on Redshift")
        sql("""
-- SCD Type 2: track customer history
CREATE TABLE dim_customer (
  customer_sk   BIGINT IDENTITY,          -- surrogate key
  customer_id   VARCHAR(36) NOT NULL,     -- natural/business key
  email         VARCHAR(255),
  plan          VARCHAR(50),
  country       VARCHAR(3),
  valid_from    TIMESTAMP NOT NULL,
  valid_to      TIMESTAMP DEFAULT '9999-12-31 00:00:00',
  is_current    BOOLEAN DEFAULT TRUE,
  row_hash      VARCHAR(64)               -- MD5 of SCD cols for change detection
)
DISTSTYLE ALL
SORTKEY (customer_id, valid_from);

-- Merge procedure (run via Step Functions / MWAA daily)
CREATE OR REPLACE PROCEDURE sp_scd2_customer() AS $$
BEGIN
  -- Close expired records
  UPDATE dim_customer SET
    valid_to = staging.updated_at - INTERVAL '1 second',
    is_current = FALSE
  FROM staging_customer_updates staging
  WHERE dim_customer.customer_id = staging.customer_id
    AND dim_customer.is_current = TRUE
    AND dim_customer.row_hash != md5(staging.email || staging.plan || staging.country);

  -- Insert new versions
  INSERT INTO dim_customer (customer_id, email, plan, country, valid_from, is_current, row_hash)
  SELECT s.customer_id, s.email, s.plan, s.country, s.updated_at, TRUE,
         md5(s.email || s.plan || s.country)
  FROM staging_customer_updates s
  LEFT JOIN dim_customer d ON s.customer_id = d.customer_id AND d.is_current = TRUE
  WHERE d.customer_id IS NULL
     OR d.row_hash != md5(s.email || s.plan || s.country);
END;
$$ LANGUAGE plpgsql;
        """)

    with tab2:
        st.header("Medallion Architecture on AWS")
        df = pd.DataFrame({
            "Layer":       ["Bronze", "Silver", "Gold"],
            "Also called": ["Raw, Landing", "Curated, Refined", "Consumption, Aggregated"],
            "S3 prefix":   ["s3://lake/raw/", "s3://lake/curated/", "s3://lake/gold/"],
            "Format":      ["Source format (JSON, CSV, Avro)", "Parquet + Iceberg", "Parquet + Iceberg"],
            "Transformation": ["None — exact copy", "Dedup, clean, mask PII, validate", "Domain aggregations, pre-joins, metrics"],
            "Write by":    ["Firehose, DMS, AppFlow", "Glue ETL, EMR", "dbt, Glue agg, Redshift stored procs"],
            "Read by":     ["Data engineers (audit/replay)", "Data scientists, DE", "BI tools, Analysts, APIs, ML"],
            "Partitioned by": ["Ingest date", "Event/business date + entity", "Business date + dimension"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab3:
        st.header("Data Vault 2.0 on AWS")
        st.markdown("""
**Data Vault 2.0** is a modeling methodology for highly auditable, scalable enterprise data warehouses.

**Core entities:**
- **Hub** — unique business keys (e.g., `hub_customer`: customer_id + load_date + record_source)  
- **Link** — relationships between hubs (e.g., `lnk_order_customer`)  
- **Satellite** — descriptive attributes of hubs/links with full history  
        """)
        sql("""
-- Hub: unique business key + metadata
CREATE TABLE hub_customer (
  customer_hk     VARCHAR(32) NOT NULL,   -- MD5 hash of natural key
  customer_id     VARCHAR(36) NOT NULL,   -- natural key
  load_dts        TIMESTAMP   NOT NULL,
  record_source   VARCHAR(100) NOT NULL
)
DISTSTYLE KEY DISTKEY (customer_hk)
SORTKEY (load_dts);

-- Satellite: attributes with full change history
CREATE TABLE sat_customer_details (
  customer_hk     VARCHAR(32) NOT NULL,
  load_dts        TIMESTAMP NOT NULL,
  load_end_dts    TIMESTAMP,             -- NULL = current version
  hash_diff       VARCHAR(32) NOT NULL,  -- MD5 of all sat cols (change detection)
  record_source   VARCHAR(100) NOT NULL,
  email           VARCHAR(255),
  plan            VARCHAR(50),
  country         VARCHAR(3)
)
DISTSTYLE KEY DISTKEY (customer_hk)
SORTKEY (customer_hk, load_dts);

-- Link: relationship between business keys
CREATE TABLE lnk_order_customer (
  order_customer_hk VARCHAR(32) NOT NULL, -- MD5 of both keys
  order_hk          VARCHAR(32) NOT NULL,
  customer_hk       VARCHAR(32) NOT NULL,
  load_dts          TIMESTAMP NOT NULL,
  record_source     VARCHAR(100) NOT NULL
)
DISTSTYLE KEY DISTKEY (order_customer_hk);
        """)
        tip("Data Vault is excellent for regulated industries (finance, pharma) needing full audit history. For fast iteration, stick to Medallion + Iceberg.")

    with tab4:
        st.header("Modeling Patterns on Iceberg")
        st.subheader("Slowly Changing Dimensions on Iceberg (SCD Type 2)")
        sql("""
-- Iceberg table supports native row-level updates — no need for complex MERGE procedures
CREATE TABLE curated.dim_customer (
  customer_id  STRING,
  email        STRING,
  plan         STRING,
  valid_from   TIMESTAMP,
  valid_to     TIMESTAMP,
  is_current   BOOLEAN
)
USING iceberg
PARTITIONED BY (is_current)  -- partition by current flag for fast lookup
TBLPROPERTIES ('write.delete.mode' = 'merge-on-read');

-- Update SCD2: close old record + insert new version (Athena v3)
MERGE INTO curated.dim_customer t
USING (
  SELECT customer_id, email, plan,
         current_timestamp AS valid_from,
         TIMESTAMP '9999-12-31' AS valid_to,
         TRUE AS is_current
  FROM staging.customer_updates
  WHERE updated_at > (SELECT max(valid_from) FROM curated.dim_customer)
) s
ON t.customer_id = s.customer_id AND t.is_current = TRUE
  AND (t.email != s.email OR t.plan != s.plan)
WHEN MATCHED THEN UPDATE SET valid_to = current_timestamp, is_current = FALSE
WHEN NOT MATCHED THEN INSERT *;

-- Then insert new versions in a second pass (or use a stored procedure)
        """)
        tip("Iceberg's row-level operations make SCD Type 2 much simpler than traditional Redshift patterns — no DELETE+INSERT tricks needed.")

# ════════════════════════════════════════════════════════════════════════════
# COST OPTIMIZATION
# ════════════════════════════════════════════════════════════════════════════
elif section == "💰 Cost Optimization":
    st.title("💰 Cost Optimization")
    tab1, tab2, tab3, tab4 = st.tabs(
        ["S3 & Storage", "Compute", "Query Optimization", "FinOps Practices"])

    with tab1:
        st.header("S3 & Storage Cost")
        df = pd.DataFrame({
            "Class":              ["Standard", "Intelligent-Tiering", "Standard-IA", "Glacier IR", "Glacier Flexible", "Deep Archive"],
            "$/GB/mo":            ["$0.023", "$0.023+$0.0025/1K obj", "$0.0125", "$0.004", "$0.0036", "$0.00099"],
            "Min obj fee":        ["None", "None", "128 KB", "128 KB", "40 KB", "40 KB"],
            "Min days":           ["—", "—", "30", "90", "90", "180"],
            "Retrieval":          ["Free", "Free (auto)", "$0.01/GB", "$0.03/GB", "$0.01/GB", "$0.02/GB"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("""
**Quick wins:**
- Enable **Bucket Key** on all KMS-encrypted buckets → ~99% KMS cost reduction  
- Use **S3 Intelligent-Tiering** for unknown/variable access patterns  
- Set lifecycle rules on raw zone (→ IA after 30d, Glacier after 90d, Deep Archive after 365d)  
- Enable **S3 Storage Lens** to identify unreferenced objects by prefix  
- Run **Iceberg compaction weekly** — small files = more requests = higher cost  
- Delete incomplete multipart uploads (`abort_incomplete_multipart_upload: 7`)  
- Use **Parquet + Snappy** — typical 5–10× compression vs CSV, 80% cost reduction  
        """)

    with tab2:
        st.header("Compute Cost Optimization")
        st.subheader("Glue Cost Levers")
        df = pd.DataFrame({
            "Action":            ["Use G.025X for small jobs", "Use Python Shell for lightweight ETL", "Enable auto-scaling", "Reduce number of workers", "Set job timeout", "Dev endpoint costs"],
            "Saving":            ["75% vs G.1X", "No Spark overhead (cheap)", "Only scale when needed", "Most over-provision by 2×", "Prevents runaway cost", "$0.44/DPU-hr — kill after dev"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("EMR Cost Levers")
        st.markdown("""
- **Task nodes → 100% Spot** (60–90% savings) — stateless, safe to interrupt with retry  
- **Core nodes → On-Demand** (stateful) — keep minimal, use S3 not HDFS  
- **EMR Serverless** — eliminate idle cluster cost, pay per-second  
- **Instance Fleets** — multiple Spot pools, survive individual AZ interruptions  
- **Auto-termination** — set `auto_termination_policy.idle_timeout = 3600`  
- **Reserved Instances** — commit 1yr for master/core On-Demand nodes: 40% savings  
        """)

        st.subheader("Redshift Cost Levers")
        df2 = pd.DataFrame({
            "Option":            ["Serverless", "Reserved Nodes (1yr)", "Reserved Nodes (3yr)", "Pause/Resume (RA3)", "Concurrency Scaling", "Spectrum vs COPY"],
            "Saving vs on-demand": ["Pay per use (no idle)", "~40%", "~60%", "100% during pause hours", "Only pay when scaling", "Spectrum $5/TB scanned vs COPY+storage"],
            "Best when":         ["Variable/intermittent load", "Steady-state 24/7 workloads", "Long-term committed", "Dev/staging clusters", "Occasional BI bursts", "Infrequent large-table queries"],
        })
        st.dataframe(df2, use_container_width=True, hide_index=True)

    with tab3:
        st.header("Query Cost Optimization")
        st.subheader("Athena – Cost Reduction Techniques")
        df = pd.DataFrame({
            "Technique":         ["Parquet vs CSV", "Partition pruning", "Iceberg file statistics", "CTAS pre-aggregation", "Result reuse cache", "Workgroup byte limit", "approx_distinct()"],
            "Scan reduction":    ["60–87%", "90%+ (with good partition)", "50–80% via bloom filters", "90%+ for repeated aggregations", "100% (free re-run)", "Prevents runaway queries", "No scan change, 10–100× faster"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("Redshift – Query Cost Reduction")
        sql("""
-- 1. Enable result cache (default ON, 24hr)
SET enable_result_cache_for_session TO TRUE;

-- 2. Use materialized views for heavy aggregations
CREATE MATERIALIZED VIEW mv_daily_sales AUTO REFRESH YES AS
SELECT date_trunc('day', order_ts) day, sum(amount) revenue
FROM fact_orders GROUP BY 1;

-- 3. Late-binding views for Spectrum (defer schema binding)
CREATE VIEW vw_s3_events WITH NO SCHEMA BINDING AS
SELECT * FROM spectrum_schema.events;

-- 4. Use APPROXIMATE COUNT DISTINCT (HyperLogLog)
SELECT approximate count(distinct user_id) FROM fact_events;

-- 5. Analyze only what changed
ANALYZE fact_orders PREDICATE COLUMNS;

-- 6. Vacuum only delete-heavy tables  
VACUUM DELETE ONLY fact_orders;
        """)

    with tab4:
        st.header("FinOps Practices")
        st.markdown("""
**Tag everything for cost attribution:**
        """)
        hcl("""
# Enforce tags via AWS Config rule
locals {
  required_tags = {
    Project     = var.project
    Environment = var.env
    Team        = var.team
    CostCenter  = var.cost_center
    ManagedBy   = "terraform"
  }
}

# Apply to all taggable resources
resource "aws_glue_job" "etl" {
  # ...
  tags = local.required_tags
}
        """)

        st.markdown("""
**Cost Anomaly Detection:**
        """)
        hcl("""
resource "aws_ce_anomaly_monitor" "data_platform" {
  name         = "DataPlatformAnomalyMonitor"
  monitor_type = "DIMENSIONAL"
  monitor_dimension = "SERVICE"
}

resource "aws_ce_anomaly_subscription" "alerts" {
  name      = "data-platform-cost-alerts"
  monitor_arn_list = [aws_ce_anomaly_monitor.data_platform.arn]
  frequency = "DAILY"
  threshold_expression {
    dimension {
      key           = "ANOMALY_TOTAL_IMPACT_ABSOLUTE"
      values        = ["100"]   # alert if >$100 anomaly
      match_options = ["GREATER_THAN_OR_EQUAL"]
    }
  }
  subscriber {
    address = var.alert_email
    type    = "EMAIL"
  }
}
        """)
        tip("Review AWS Trusted Advisor and Compute Optimizer weekly — they flag Glue job over-provisioning, idle Redshift clusters, and unused EMR nodes.")
        warn("Redshift Serverless has no maximum spend cap by default — always set a `usage_limit` resource with `breach_action = emit-metric`.")

# ════════════════════════════════════════════════════════════════════════════
# QUICK REFERENCE
# ════════════════════════════════════════════════════════════════════════════
elif section == "📋 Quick Reference – CLI & SQL Snippets":
    st.title("📋 Quick Reference – CLI & SQL Snippets")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["S3 & Glue CLI", "Redshift SQL", "Kinesis CLI", "Boto3 Patterns", "Spark Configs"])

    with tab1:
        st.header("S3 & Glue CLI Reference")
        bash("""
# ── S3 ─────────────────────────────────────────────────────────────────────
# List with human-readable sizes
aws s3 ls s3://my-lake/raw/ --recursive --human-readable --summarize

# Sync with delete (mirror)
aws s3 sync ./local/ s3://my-lake/raw/ --delete --storage-class STANDARD_IA

# Copy with KMS
aws s3 cp file.parquet s3://my-lake/curated/ --sse aws:kms --sse-kms-key-id alias/lake-key

# Move objects in bulk
aws s3 mv s3://my-lake/raw/old-prefix/ s3://my-lake/archive/ --recursive

# Get object metadata
aws s3api head-object --bucket my-lake --key raw/events/file.parquet

# Generate presigned URL (1 hour)
aws s3 presign s3://my-lake/curated/report.parquet --expires-in 3600

# Check bucket size per prefix (cost analysis)
aws s3api list-objects-v2 --bucket my-lake --prefix raw/ \
  --query 'sum(Contents[].Size)' --output text

# ── Glue ────────────────────────────────────────────────────────────────────
# Start job run with arguments
aws glue start-job-run \
  --job-name ingest-orders \
  --arguments '{"--source_date":"2024-01-15","--env":"prod"}'

# Get job run status
aws glue get-job-run --job-name ingest-orders --run-id jr_abc123

# List recent job runs
aws glue get-job-runs --job-name ingest-orders \
  --query 'JobRuns[?JobRunState!=`SUCCEEDED`].[Id,JobRunState,StartedOn,ErrorMessage]' \
  --output table

# Reset job bookmark
aws glue reset-job-bookmark --job-name ingest-orders

# Start crawler
aws glue start-crawler --name raw-events-crawler

# Get table from catalog
aws glue get-table --database-name curated --name orders \
  --query 'Table.StorageDescriptor.Location'

# List all databases
aws glue get-databases --query 'DatabaseList[].Name'

# Repair partitions
aws glue batch-create-partition \
  --database-name curated --table-name events \
  --partition-input-list '[{"Values":["2024-01-15"],"StorageDescriptor":{"Location":"s3://my-lake/curated/events/dt=2024-01-15/"}}]'
        """)

    with tab2:
        st.header("Redshift SQL Reference")
        sql("""
-- ── Admin & Monitoring ──────────────────────────────────────────────────────
-- Active queries + wait time
SELECT pid, trim(user_name), elapsed/1e6 elapsed_sec, trim(querytxt)
FROM stv_recents WHERE status='Running' ORDER BY elapsed_sec DESC;

-- Kill runaway query
SELECT pg_terminate_backend(12345);

-- User sessions
SELECT * FROM stv_sessions ORDER BY starttime DESC LIMIT 20;

-- Locks
SELECT pid, relation, mode, granted FROM pg_locks ORDER BY pid;

-- ── Table Health ────────────────────────────────────────────────────────────
-- Table info: size, unsorted, stats
SELECT "table", size, unsorted, stats_off, pct_used
FROM svv_table_info ORDER BY size DESC LIMIT 20;

-- Skew check
SELECT name, num_values, skew_rows FROM svv_diskusage ORDER BY skew_rows DESC LIMIT 10;

-- ── Performance ─────────────────────────────────────────────────────────────
-- Query execution steps
SELECT query, step, rows, bytes, label
FROM svl_query_summary WHERE query = <query_id>
ORDER BY step;

-- S3 Spectrum query performance
SELECT q.query, q.starttime, s.is_rrscan, s.perm_table_name, s.num_files, s.num_rows, s.size
FROM svl_s3query_summary s JOIN stl_query q ON s.query = q.query
WHERE s.starttime > dateadd(hour,-24,getdate())
ORDER BY s.starttime DESC LIMIT 20;

-- ── Data Loading ────────────────────────────────────────────────────────────
-- COPY with auto-detect
COPY orders
FROM 's3://my-lake/curated/orders/'
IAM_ROLE 'arn:aws:iam::123456789:role/RedshiftRole'
FORMAT AS PARQUET;

-- COPY with explicit manifest
COPY orders FROM 's3://my-lake/manifests/orders.manifest'
IAM_ROLE 'arn:aws:iam::123456789:role/RedshiftRole'
MANIFEST FORMAT AS PARQUET;

-- UNLOAD to Parquet with partitioning
UNLOAD ('SELECT * FROM fact_orders WHERE order_year = 2024')
TO 's3://my-lake/exports/orders/'
IAM_ROLE 'arn:aws:iam::123456789:role/RedshiftRole'
FORMAT PARQUET PARTITION BY (order_month) ALLOWOVERWRITE PARALLEL ON;
        """)

    with tab3:
        st.header("Kinesis & MSK CLI")
        bash("""
# ── Kinesis ────────────────────────────────────────────────────────────────
# Put test record
aws kinesis put-record \
  --stream-name user-events \
  --partition-key user-001 \
  --data $(echo '{"event_id":"abc","user_id":"user-001","type":"click"}' | base64)

# Get shard iterator
ITER=$(aws kinesis get-shard-iterator \
  --stream-name user-events \
  --shard-id shardId-000000000000 \
  --shard-iterator-type LATEST \
  --query 'ShardIterator' --output text)

# Read records
aws kinesis get-records --shard-iterator $ITER --limit 10 \
  --query 'Records[].Data' --output text | while read d; do
    echo $d | base64 -d; echo
  done

# Describe stream (shard count, retention, encryption)
aws kinesis describe-stream-summary --stream-name user-events

# Update shard count
aws kinesis update-shard-count \
  --stream-name user-events \
  --target-shard-count 8 \
  --scaling-type UNIFORM_SCALING

# List enhanced fan-out consumers
aws kinesis list-stream-consumers --stream-arn arn:aws:kinesis:us-east-1:123:stream/user-events

# ── MSK ────────────────────────────────────────────────────────────────────
# Get broker endpoints
aws kafka get-bootstrap-brokers --cluster-arn arn:aws:kafka:us-east-1:123:cluster/my-cluster/abc

# List topics (from broker)
kafka-topics.sh --bootstrap-server broker:9092 --list

# Describe topic
kafka-topics.sh --bootstrap-server broker:9092 --describe --topic user-events

# Consumer group lag
kafka-consumer-groups.sh --bootstrap-server broker:9092 \
  --describe --group my-app-consumer-group

# Reset consumer group offset (replay)
kafka-consumer-groups.sh --bootstrap-server broker:9092 \
  --group my-app-consumer-group \
  --topic user-events \
  --reset-offsets --to-earliest --execute
        """)

    with tab4:
        st.header("Boto3 Patterns")
        py("""
import boto3
import json
from datetime import datetime, timedelta

# ── S3 ────────────────────────────────────────────────────────────────────
s3 = boto3.client('s3')

# List objects with prefix (paginated)
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket='my-lake', Prefix='raw/events/')
all_keys = [obj['Key'] for page in pages for obj in page.get('Contents', [])]

# Read JSON from S3 without downloading
obj = s3.get_object(Bucket='my-lake', Key='config/settings.json')
config = json.loads(obj['Body'].read())

# Write JSON to S3
s3.put_object(
    Bucket='my-lake',
    Key=f"processed/results/{datetime.utcnow().strftime('%Y-%m-%d')}/summary.json",
    Body=json.dumps({'count': 100, 'status': 'ok'}),
    ContentType='application/json',
    ServerSideEncryption='aws:kms',
)

# ── Glue ────────────────────────────────────────────────────────────────
glue = boto3.client('glue')

# Start job and wait
run = glue.start_job_run(
    JobName='ingest-orders',
    Arguments={'--source_date': '2024-01-15'}
)
run_id = run['JobRunId']

import time
while True:
    status = glue.get_job_run(JobName='ingest-orders', RunId=run_id)['JobRun']['JobRunState']
    if status in ('SUCCEEDED', 'FAILED', 'STOPPED'):
        break
    time.sleep(30)
print(f"Job finished: {status}")

# ── Redshift Data API ────────────────────────────────────────────────────
rs = boto3.client('redshift-data')

def run_redshift_sql(sql, workgroup='primary', database='datawarehouse', wait=True):
    resp = rs.execute_statement(WorkgroupName=workgroup, Database=database, Sql=sql)
    stmt_id = resp['Id']
    if not wait:
        return stmt_id
    while True:
        desc = rs.describe_statement(Id=stmt_id)
        if desc['Status'] in ('FINISHED', 'FAILED', 'ABORTED'):
            break
        time.sleep(2)
    if desc['Status'] == 'FINISHED':
        if desc.get('HasResultSet'):
            return rs.get_statement_result(Id=stmt_id)
    else:
        raise Exception(f"SQL failed: {desc.get('Error')}")

# ── Athena ───────────────────────────────────────────────────────────────
athena = boto3.client('athena')

def run_athena(query, workgroup='analytics-team', output='s3://my-lake/athena-results/'):
    resp = athena.start_query_execution(
        QueryString=query,
        WorkGroup=workgroup,
        ResultConfiguration={'OutputLocation': output},
    )
    qid = resp['QueryExecutionId']
    while True:
        state = athena.get_query_execution(QueryExecutionId=qid)['QueryExecution']['Status']['State']
        if state in ('SUCCEEDED', 'FAILED', 'CANCELLED'):
            break
        time.sleep(2)
    if state == 'SUCCEEDED':
        return athena.get_query_results(QueryExecutionId=qid)
    raise Exception(f"Athena query {state}: {qid}")
        """)

    with tab5:
        st.header("Spark Configuration Cheat Sheet")
        df = pd.DataFrame({
            "Config key":                       ["spark.sql.shuffle.partitions", "spark.executor.memory", "spark.executor.cores", "spark.driver.memory", "spark.sql.adaptive.enabled", "spark.sql.adaptive.coalescePartitions.enabled", "spark.sql.adaptive.skewJoin.enabled", "spark.dynamicAllocation.enabled", "spark.hadoop.fs.s3a.connection.maximum", "spark.hadoop.fs.s3a.fast.upload", "spark.sql.extensions (Iceberg)", "spark.sql.catalog.glue_catalog"],
            "Recommended":                      ["2–3× total cores", "node_ram - 1GB / executors_per_node", "4–5", "4–8g", "true", "true", "true", "true", "100", "true", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions", "org.apache.iceberg.spark.SparkCatalog"],
            "Notes":                            ["Default 200 is too low for large datasets", "Leave 1GB for OS overhead", "4 is the sweet spot (parallelism + overhead)", "Keep higher for large result sets", "AQE auto-optimises joins and partition count", "Merges small shuffle partitions automatically", "Handles data skew automatically", "Must pair with external shuffle service", "Increase for S3-heavy workloads", "Faster multipart S3 uploads", "Required for Iceberg SQL extensions", "Required for Iceberg Glue Catalog"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        bash("""
# spark-submit with recommended configs
spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --executor-memory 14g \
  --executor-cores 4 \
  --num-executors 20 \
  --driver-memory 8g \
  --conf spark.sql.shuffle.partitions=400 \
  --conf spark.sql.adaptive.enabled=true \
  --conf spark.sql.adaptive.coalescePartitions.enabled=true \
  --conf spark.dynamicAllocation.enabled=true \
  --conf spark.dynamicAllocation.maxExecutors=100 \
  --conf "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions" \
  --conf "spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog" \
  --conf "spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog" \
  --conf "spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO" \
  s3://my-scripts/transform_orders.py \
  --date 2024-01-15
        """)

# ════════════════════════════════════════════════════════════════════════════
# MASTER DE PIPELINES – ETL/ELT, DWH, LAKE, LAKEHOUSE (KAPPA)
# ════════════════════════════════════════════════════════════════════════════
elif section == "🧬 Master DE Pipelines – ETL/ELT, DWH, Lake, Lakehouse (Kappa)":
    st.title("🧬 Master Data Engineer Pipelines on AWS")
    st.markdown("""> **End-to-end, production-grade pipeline blueprints** for every major DE pattern.
Each pipeline covers: architecture diagram → services → code → Terraform → orchestration → monitoring.""")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🔁 ETL/ELT Pipeline",
        "🏛️ Data Warehouse Pipeline",
        "🏞️ Data Lake Pipeline",
        "🏔️ Data Lakehouse (Kappa)",
        "⚡ Streaming Kappa Pipeline",
        "🗺️ Pipeline Decision Map",
    ])

    # ── TAB 1: ETL/ELT ─────────────────────────────────────────────────────
    with tab1:
        st.header("🔁 Master ETL / ELT Pipeline")
        st.markdown("**ETL vs ELT on AWS:**")
        df = pd.DataFrame({
            "Dimension":    ["Transform location", "Schema requirement", "Best engine", "Data volume", "When to use"],
            "ETL":          ["Before load (in Glue/EMR)", "Strict — target schema known upfront", "Glue, EMR", "Medium", "Sensitive targets (Redshift), strict schemas, PII must be masked before landing"],
            "ELT":          ["After load (in Redshift/Athena/dbt)", "Flexible — raw lands first", "Redshift, Athena, dbt", "Large", "Data lake/lakehouse, exploration-first, schema-on-read targets"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("Full ETL Pipeline Architecture")
        st.code("""
┌─────────────────────────────────────────────────────────────────────────────┐
│  SOURCES                                                                     │
│  PostgreSQL RDS ──┐                                                          │
│  MySQL Aurora  ──┤  DMS (CDC)  ──→  S3 Raw (Parquet, partitioned)           │
│  Salesforce    ──┤  AppFlow    ──→  S3 Raw                                   │
│  REST APIs     ──┘  Lambda     ──→  S3 Raw                                   │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │  S3 Event → EventBridge
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  TRANSFORM  (AWS Glue ETL Job — PySpark)                                    │
│  • Deduplicate on primary key                                                │
│  • Validate schema + null checks (Glue Data Quality)                        │
│  • Cast types, standardise timestamps to UTC                                 │
│  • Mask / tokenise PII (email, phone, SSN)                                  │
│  • Enrich: join with reference data (dim_country, dim_product)               │
│  • Partition output by business date                                         │
│  • Write as Parquet + Iceberg to S3 Curated                                  │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  LOAD  (Redshift COPY / dbt run)                                            │
│  • COPY curated Parquet → Redshift staging tables                           │
│  • dbt models: staging → intermediate → marts                               │
│  • Run dbt tests (uniqueness, not_null, referential integrity)               │
│  • Refresh materialized views                                                │
│  • Notify downstream (SNS → BI refresh trigger)                              │
└─────────────────────────────────────────────────────────────────────────────┘
        """, language="text")

        st.subheader("Glue ETL Job – Full Production Pattern")
        py("""
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql import functions as F
from pyspark.sql.types import TimestampType
import hashlib

args = getResolvedOptions(sys.argv, [
    'JOB_NAME', 'source_date', 'source_db', 'source_table',
    'target_bucket', 'target_db', 'target_table', 'env'
])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# ── 1. EXTRACT ──────────────────────────────────────────────────────────────
raw_dyf = glueContext.create_dynamic_frame.from_catalog(
    database=args['source_db'],
    table_name=args['source_table'],
    push_down_predicate=f"(dt = '{args['source_date']}')",
    transformation_ctx="extract"
)

if raw_dyf.count() == 0:
    print(f"No records for {args['source_date']} — exiting cleanly")
    job.commit()
    sys.exit(0)

df = raw_dyf.toDF()

# ── 2. TRANSFORM ────────────────────────────────────────────────────────────
# Dedup — keep latest record per natural key
window = Window.partitionBy("order_id").orderBy(F.col("updated_at").desc())
df = (df
    .withColumn("_rn", F.row_number().over(window))
    .filter(F.col("_rn") == 1)
    .drop("_rn")
)

# Standardise timestamps to UTC
df = df.withColumn("event_ts",
    F.to_utc_timestamp(F.col("event_ts").cast(TimestampType()), "America/New_York"))

# Mask PII (SHA-256 tokenisation, reversible with key)
mask_udf = F.udf(lambda v: hashlib.sha256(v.encode()).hexdigest()[:16] if v else None)
df = df.withColumn("email_token", mask_udf(F.col("email"))).drop("email")

# Type validation + null guard
df = (df
    .filter(F.col("order_id").isNotNull())
    .filter(F.col("amount").cast("double").isNotNull())
    .withColumn("amount", F.round(F.col("amount").cast("double"), 4))
    .withColumn("status", F.upper(F.trim(F.col("status"))))
    .withColumn("partition_dt", F.to_date(F.col("event_ts")))
)

# ── 3. DATA QUALITY CHECK ───────────────────────────────────────────────────
total   = df.count()
nulls   = df.filter(F.col("order_id").isNull()).count()
dupes   = total - df.dropDuplicates(["order_id"]).count()
assert nulls == 0,       f"DQ FAIL: {nulls} null order_ids"
assert dupes == 0,       f"DQ FAIL: {dupes} duplicate order_ids"
assert total > 100,      f"DQ FAIL: suspiciously low row count {total}"

# ── 4. LOAD → Iceberg (upsert) ──────────────────────────────────────────────
out_dyf = glueContext.create_dynamic_frame.from_dataframe(df, glueContext)

glueContext.write_dynamic_frame.from_options(
    frame=out_dyf,
    connection_type="custom.spark",
    connection_options={
        "path": f"s3://{args['target_bucket']}/curated/{args['target_table']}/",
        "connectionName": "IcebergConnection",
    },
    transformation_ctx="load_iceberg"
)

print(f"ETL complete: {total} rows written to {args['target_table']} for {args['source_date']}")
job.commit()
        """)

        st.subheader("Step Functions – ETL Orchestration State Machine")
        py("""
{
  "Comment": "Production ETL: Extract → Quality → Transform → Load → Notify",
  "StartAt": "ExtractFromSource",
  "States": {

    "ExtractFromSource": {
      "Type": "Task",
      "Resource": "arn:aws:states:::glue:startJobRun.sync",
      "Parameters": {
        "JobName": "dms-cdc-to-raw",
        "Arguments": { "--source_date.$": "$.execution_date" }
      },
      "Retry": [{ "ErrorEquals": ["States.ALL"], "MaxAttempts": 2, "IntervalSeconds": 120 }],
      "Catch": [{ "ErrorEquals": ["States.ALL"], "Next": "NotifyFailure" }],
      "Next": "RunDataQuality"
    },

    "RunDataQuality": {
      "Type": "Task",
      "Resource": "arn:aws:states:::glue:startJobRun.sync",
      "Parameters": {
        "JobName": "data-quality-check",
        "Arguments": { "--target_date.$": "$.execution_date" }
      },
      "Next": "CheckQualityResult"
    },

    "CheckQualityResult": {
      "Type": "Choice",
      "Choices": [{
        "Variable": "$.quality_passed",
        "BooleanEquals": true,
        "Next": "TransformAndLoad"
      }],
      "Default": "QuarantineAndAlert"
    },

    "TransformAndLoad": {
      "Type": "Parallel",
      "Branches": [
        {
          "StartAt": "GlueTransform",
          "States": {
            "GlueTransform": {
              "Type": "Task",
              "Resource": "arn:aws:states:::glue:startJobRun.sync",
              "Parameters": {
                "JobName": "raw-to-curated-etl",
                "Arguments": { "--source_date.$": "$.execution_date" }
              },
              "End": true
            }
          }
        },
        {
          "StartAt": "UpdateCatalog",
          "States": {
            "UpdateCatalog": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "Parameters": { "FunctionName": "update-glue-partitions" },
              "End": true
            }
          }
        }
      ],
      "Next": "LoadToRedshift"
    },

    "LoadToRedshift": {
      "Type": "Task",
      "Resource": "arn:aws:states:::redshift-data:executeStatement.sync",
      "Parameters": {
        "WorkgroupName": "primary",
        "Database": "datawarehouse",
        "Sql.$": "States.Format('CALL sp_load_orders(\\'{}\\');', $.execution_date)"
      },
      "Next": "RunDBTModels"
    },

    "RunDBTModels": {
      "Type": "Task",
      "Resource": "arn:aws:states:::ecs:runTask.sync",
      "Parameters": {
        "Cluster": "data-platform",
        "TaskDefinition": "dbt-runner",
        "Overrides": {
          "ContainerOverrides": [{
            "Name": "dbt",
            "Command": ["dbt", "run", "--select", "marts.sales+", "--target", "prod"]
          }]
        }
      },
      "Next": "NotifySuccess"
    },

    "NotifySuccess": {
      "Type": "Task",
      "Resource": "arn:aws:states:::sns:publish",
      "Parameters": {
        "TopicArn": "arn:aws:sns:us-east-1:123:de-pipeline-alerts",
        "Message.$": "States.Format('✅ ETL pipeline succeeded for {}', $.execution_date)"
      },
      "End": true
    },

    "QuarantineAndAlert": {
      "Type": "Task",
      "Resource": "arn:aws:states:::sns:publish",
      "Parameters": {
        "TopicArn": "arn:aws:sns:us-east-1:123:de-pipeline-alerts",
        "Message.$": "States.Format('🚨 DQ failure — data quarantined for {}', $.execution_date)"
      },
      "End": true
    },

    "NotifyFailure": {
      "Type": "Task",
      "Resource": "arn:aws:states:::sns:publish",
      "Parameters": {
        "TopicArn": "arn:aws:sns:us-east-1:123:de-pipeline-alerts",
        "Message.$": "States.Format('❌ ETL pipeline FAILED for {}', $.execution_date)"
      },
      "End": true
    }
  }
}
        """)
        tip("Run dbt models as an ECS Fargate task triggered from Step Functions — no MWAA needed for simpler pipelines.")
        warn("Never skip the DQ check gate before loading to the warehouse — bad data in Redshift is expensive to clean up retroactively.")

    # ── TAB 2: DATA WAREHOUSE ───────────────────────────────────────────────
    with tab2:
        st.header("🏛️ Master Data Warehouse Pipeline")
        st.code("""
┌──────────────────────────────────────────────────────────────────────────────┐
│  SOURCES (operational systems)                                               │
│  Aurora MySQL  →  DMS Full Load + CDC  →  S3 Staging (Parquet)              │
│  PostgreSQL    →  DMS Full Load + CDC  →  S3 Staging (Parquet)              │
│  Salesforce    →  AppFlow (hourly)     →  S3 Staging (Parquet)              │
└─────────────────────────────┬────────────────────────────────────────────────┘
                              │  Firehose / S3 Event → EventBridge → SFN
                              ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  STAGING LAYER  (Redshift)                                                   │
│  COPY s3://staging/ → stg_orders, stg_customers, stg_products               │
│  Row count validation, null checks                                           │
└─────────────────────────────┬────────────────────────────────────────────────┘
                              │  Redshift stored procs / dbt
                              ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  TRANSFORMATION LAYER  (dbt on Redshift)                                     │
│  stg_* → int_* (joins, dedup, SCD2 dims) → marts.*                          │
│  dim_customer (SCD2)  dim_product  dim_date  dim_geography                  │
│  fact_orders  fact_returns  fact_inventory                                   │
└─────────────────────────────┬────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  CONSUMPTION  (BI + APIs)                                                    │
│  QuickSight SPICE  →  Exec dashboards                                        │
│  Redshift Data API →  Internal REST API                                      │
│  Tableau / PowerBI →  Analyst self-serve                                     │
└──────────────────────────────────────────────────────────────────────────────┘
        """, language="text")

        st.subheader("Redshift – Full Warehouse Load Stored Procedure")
        sql("""
-- Master load procedure called by Step Functions daily
CREATE OR REPLACE PROCEDURE sp_load_daily(p_date DATE)
AS $$
DECLARE
  v_rows INT;
BEGIN
  -- 1. Truncate staging
  TRUNCATE TABLE stg_orders;
  TRUNCATE TABLE stg_customers;

  -- 2. COPY from S3 curated
  EXECUTE 'COPY stg_orders FROM ''s3://my-lake/curated/orders/partition_dt=' || p_date || '/''
    IAM_ROLE ''arn:aws:iam::123456789:role/RedshiftRole''
    FORMAT AS PARQUET';

  EXECUTE 'COPY stg_customers FROM ''s3://my-lake/curated/customers/partition_dt=' || p_date || '/''
    IAM_ROLE ''arn:aws:iam::123456789:role/RedshiftRole''
    FORMAT AS PARQUET';

  -- 3. Row count guard
  SELECT COUNT(*) INTO v_rows FROM stg_orders;
  IF v_rows < 100 THEN
    RAISE EXCEPTION 'DQ FAIL: stg_orders only % rows for %', v_rows, p_date;
  END IF;

  -- 4. SCD2 merge for dim_customer
  -- Close changed records
  UPDATE dim_customer SET
    valid_to   = stg.updated_at - INTERVAL '1 second',
    is_current = FALSE
  FROM stg_customers stg
  WHERE dim_customer.customer_id = stg.customer_id
    AND dim_customer.is_current   = TRUE
    AND dim_customer.row_hash    != MD5(stg.email || COALESCE(stg.plan,'') || COALESCE(stg.country,''));

  -- Insert new versions
  INSERT INTO dim_customer (customer_id, email, plan, country, valid_from, valid_to, is_current, row_hash)
  SELECT s.customer_id, s.email, s.plan, s.country,
         s.updated_at, '9999-12-31'::TIMESTAMP, TRUE,
         MD5(s.email || COALESCE(s.plan,'') || COALESCE(s.country,''))
  FROM stg_customers s
  LEFT JOIN dim_customer d ON s.customer_id = d.customer_id AND d.is_current = TRUE
  WHERE d.customer_id IS NULL
     OR d.row_hash != MD5(s.email || COALESCE(s.plan,'') || COALESCE(s.country,''));

  -- 5. Insert into fact (upsert pattern)
  DELETE FROM fact_orders WHERE order_date = p_date;

  INSERT INTO fact_orders (order_sk, order_id, customer_sk, amount_usd, order_date)
  SELECT o.order_id, o.order_id, c.customer_sk, o.amount, o.order_date
  FROM stg_orders o
  JOIN dim_customer c ON o.customer_id = c.customer_id AND c.is_current = TRUE;

  -- 6. Refresh materialized view
  REFRESH MATERIALIZED VIEW mv_monthly_revenue;

  -- 7. Vacuum + analyze incrementally
  ANALYZE dim_customer;
  ANALYZE fact_orders;

  RAISE INFO 'sp_load_daily complete for %: % orders loaded', p_date, v_rows;
END;
$$ LANGUAGE plpgsql;
        """)

        st.subheader("dbt Project Structure for DWH")
        bash("""
models/
├── staging/               # 1:1 source, minimal transforms
│   ├── _stg_sources.yml
│   ├── stg_orders.sql
│   └── stg_customers.sql
├── intermediate/          # business logic, joins, dedup
│   ├── int_orders_enriched.sql
│   └── int_customer_scd2.sql
├── marts/                 # final dimensional models
│   ├── finance/
│   │   ├── fact_orders.sql
│   │   └── fact_returns.sql
│   └── customers/
│       ├── dim_customer.sql
│       └── dim_customer_segments.sql
└── utilities/             # reusable CTEs, date spine
    └── dim_date.sql

# dbt run sequence
dbt run --select staging          # idempotent, truncate+insert
dbt run --select intermediate     # incremental
dbt run --select marts            # incremental, merge key = PK
dbt test --select marts           # uniqueness, not_null, RI, custom
dbt docs generate && dbt docs serve
        """)
        tip("Use `dbt build` to run + test in dependency order in one command — ideal for CI/CD pipelines.")

    # ── TAB 3: DATA LAKE ────────────────────────────────────────────────────
    with tab3:
        st.header("🏞️ Master Data Lake Pipeline")
        st.code("""
┌──────────────────────────────────────────────────────────────────────────────┐
│  INGESTION LAYER                                                             │
│  Event streams  → Kinesis Data Streams → Firehose → S3 Bronze (JSON/Avro)  │
│  DB CDC         → DMS                  → S3 Bronze (Parquet)               │
│  SaaS           → AppFlow              → S3 Bronze (Parquet)               │
│  Files / FTP    → Lambda + S3 trigger  → S3 Bronze                         │
└─────────────────────────────┬────────────────────────────────────────────────┘
                              │  S3 Event → EventBridge → Step Functions
                              ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  BRONZE → SILVER  (AWS Glue ETL)                                            │
│  • Schema validation (Glue Data Quality DQDL)                               │
│  • Dedup + null handling                                                     │
│  • Timestamp normalisation                                                   │
│  • PII masking (tokenisation / nulling)                                      │
│  • Convert to Parquet + Iceberg, partition by date                          │
│  • Register partitions in Glue Catalog                                      │
│  → s3://lake/silver/{domain}/{table}/year=yyyy/month=mm/day=dd/            │
└─────────────────────────────┬────────────────────────────────────────────────┘
                              │  Daily EMR Serverless job
                              ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  SILVER → GOLD  (EMR Serverless + Spark)                                    │
│  • Domain aggregations (daily revenue, user metrics, funnel)                │
│  • Pre-join common query patterns (wide tables)                             │
│  • Write Iceberg Gold tables (optimised for reads)                          │
│  • Compact + expire snapshots                                               │
│  → s3://lake/gold/{domain}/{mart}/                                          │
└─────────────────────────────┬────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  CONSUMPTION                                                                 │
│  Athena          → Ad-hoc SQL queries, notebook exploration                 │
│  Redshift Spectrum → BI dashboards via Redshift without COPY                │
│  SageMaker       → ML model training on Gold/Silver data                   │
│  Lake Formation  → Column/row security per team                             │
└──────────────────────────────────────────────────────────────────────────────┘
        """, language="text")

        st.subheader("Bronze → Silver Glue Job")
        st.code('''
# bronze_to_silver.py
import sys
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql import functions as F, Window

args = getResolvedOptions(sys.argv, ["JOB_NAME","source_date","domain","table"])
sc   = SparkContext()
glue = GlueContext(sc)
spark = glue.spark_session
job  = Job(glue)
job.init(args["JOB_NAME"], args)

src_date = args["source_date"]
domain   = args["domain"]
table    = args["table"]

# EXTRACT
bronze = spark.read.parquet(f"s3://my-lake/bronze/{domain}/{table}/dt={src_date}/")

# TRANSFORM
silver = (bronze
    .withColumn("_rn", F.row_number().over(
        Window.partitionBy("id").orderBy(F.col("updated_at").desc())))
    .filter(F.col("_rn") == 1).drop("_rn")
    .withColumn("event_ts", F.to_utc_timestamp(F.col("event_ts").cast("timestamp"), "UTC"))
    .withColumn("email", F.sha2(F.col("email"), 256))   # PII mask
    .withColumn("phone", F.lit(None).cast("string"))     # PII drop
    .filter(F.col("id").isNotNull())
    .filter(F.col("event_ts").isNotNull())
    .withColumn("_source",       F.lit(f"bronze/{domain}/{table}"))
    .withColumn("_processed_at", F.current_timestamp())
    .withColumn("_partition_dt", F.lit(src_date))
)

# DQ guards
count = silver.count()
assert count > 0, f"Silver DQ FAIL: 0 rows for {domain}.{table} dt={src_date}"
assert silver.filter(F.col("id").isNull()).count() == 0, "Silver DQ FAIL: null IDs"

# LOAD → Iceberg Silver MERGE (upsert)
silver.createOrReplaceTempView("silver_batch")
merge_sql = f"""
    MERGE INTO glue_catalog.silver.{domain}_{table} t
    USING silver_batch s ON t.id = s.id
    WHEN MATCHED THEN UPDATE SET *
    WHEN NOT MATCHED THEN INSERT *
"""
spark.sql(merge_sql)

print(f"bronze->silver: {count} rows → silver.{domain}_{table} for {src_date}")
job.commit()
        ''', language="python")

        st.subheader("Silver → Gold EMR Serverless Spark")
        st.code('''
# silver_to_gold.py — domain aggregation into Gold mart
from pyspark.sql import SparkSession, functions as F

spark = (SparkSession.builder
    .config("spark.sql.extensions",
            "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
    .config("spark.sql.catalog.glue_catalog", "org.apache.iceberg.spark.SparkCatalog")
    .config("spark.sql.catalog.glue_catalog.catalog-impl",
            "org.apache.iceberg.aws.glue.GlueCatalog")
    .config("spark.sql.catalog.glue_catalog.io-impl",
            "org.apache.iceberg.aws.s3.S3FileIO")
    .getOrCreate()
)

orders    = spark.table("glue_catalog.silver.ecommerce_orders")
customers = spark.table("glue_catalog.silver.ecommerce_customers")
products  = spark.table("glue_catalog.silver.ecommerce_products")

# Wide Gold fact (pre-joined for fast BI queries)
gold_orders = (orders
    .join(customers.select("id","country","segment"), orders.customer_id == customers.id, "left")
    .join(products.select("id","category","brand"),   orders.product_id  == products.id,  "left")
    .select(
        "order_id","customer_id","product_id","amount_usd","quantity","status","event_ts",
        "country","segment","category","brand",
        F.to_date("event_ts").alias("order_date"),
        F.date_format("event_ts","yyyy-MM").alias("order_month"),
    )
)

# Daily revenue summary Gold table
gold_daily = (gold_orders
    .groupBy("order_date","country","category","segment")
    .agg(
        F.sum("amount_usd").alias("revenue_usd"),
        F.count("order_id").alias("order_count"),
        F.countDistinct("customer_id").alias("unique_customers"),
        F.avg("amount_usd").alias("avg_order_value"),
    )
)

# MERGE into Gold Iceberg
gold_daily.createOrReplaceTempView("gold_daily_batch")
merge_sql = """
    MERGE INTO glue_catalog.gold.daily_revenue_summary t
    USING gold_daily_batch s
    ON  t.order_date = s.order_date AND t.country = s.country
    AND t.category   = s.category   AND t.segment = s.segment
    WHEN MATCHED THEN UPDATE SET *
    WHEN NOT MATCHED THEN INSERT *
"""
spark.sql(merge_sql)

# Iceberg maintenance
compact_sql = """
    CALL glue_catalog.system.rewrite_data_files(
        table => 'gold.daily_revenue_summary',
        options => map('target-file-size-bytes', '134217728')
    )
"""
spark.sql(compact_sql)
print("silver->gold complete")
        ''', language="python")
        tip("Schedule weekly Iceberg compaction on Silver tables and daily compaction on Gold tables — Gold is queried most and benefits most from optimised file layouts.")

    # ── TAB 4: DATA LAKEHOUSE ───────────────────────────────────────────────
    with tab4:
        st.header("🏔️ Master Data Lakehouse Pipeline (Batch)")
        st.markdown(
            "> **Single unified storage (Iceberg on S3)** serving both batch ETL and streaming — no separate data warehouse copy needed.")

        st.code("""
┌──────────────────────────────────────────────────────────────────────────────┐
│  SOURCES                                                                     │
│  Operational DBs → DMS CDC    → S3 Raw (Parquet)                           │
│  SaaS apps       → AppFlow    → S3 Raw (Parquet)                           │
│  Events          → Firehose   → S3 Raw (Parquet)                           │
└─────────────────────────────┬────────────────────────────────────────────────┘
                              │  Glue Job (incremental, bookmark-enabled)
                              ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  LAKEHOUSE CORE  —  S3 + Apache Iceberg + Glue Catalog                      │
│                                                                              │
│  Bronze (raw Iceberg)    → APPEND only, immutable source truth              │
│  Silver (curated Iceberg)→ MERGE upsert, schema enforced, PII masked        │
│  Gold   (domain Iceberg) → MERGE upsert, aggregated, BI-optimised          │
│                                                                              │
│  All layers: ACID · time travel · schema evolution · partition pruning      │
└──────────┬────────────────────────────────────────────────┬─────────────────┘
           │                                                │
           ▼                                                ▼
┌──────────────────────┐                     ┌─────────────────────────────┐
│  SQL CONSUMERS       │                     │  NON-SQL CONSUMERS          │
│  Athena (ad-hoc)     │                     │  SageMaker (ML training)    │
│  Redshift Spectrum   │                     │  EMR (custom Spark jobs)    │
│  Redshift federated  │                     │  Glue (further transforms)  │
│  QuickSight (direct) │                     │  Notebooks (JupyterHub)     │
└──────────────────────┘                     └─────────────────────────────┘
        """, language="text")

        st.subheader("Terraform – Full Lakehouse IaC Skeleton")
        hcl("""
# ── KMS key for all lake resources ─────────────────────────────────────────
resource "aws_kms_key" "lake" {
  description             = "Lake platform encryption key"
  deletion_window_in_days = 30
  enable_key_rotation     = true
  tags                    = local.tags
}

# ── S3 (one bucket, three zone prefixes) ───────────────────────────────────
module "lake_bucket" {
  source      = "./modules/s3_data_lake"
  prefix      = var.project
  env         = var.env
  kms_key_arn = aws_kms_key.lake.arn
  tags        = local.tags
}

# ── Glue Catalog databases per zone ────────────────────────────────────────
resource "aws_glue_catalog_database" "bronze" { name = "bronze_${var.env}" }
resource "aws_glue_catalog_database" "silver" { name = "silver_${var.env}" }
resource "aws_glue_catalog_database" "gold"   { name = "gold_${var.env}"   }

# ── Glue ETL jobs ──────────────────────────────────────────────────────────
resource "aws_glue_job" "bronze_to_silver" {
  name              = "${var.project}-bronze-silver-${var.env}"
  role_arn          = aws_iam_role.glue.arn
  glue_version      = "4.0"
  worker_type       = "G.1X"
  number_of_workers = 5
  command {
    name            = "glueetl"
    script_location = "s3://${var.scripts_bucket}/bronze_to_silver.py"
    python_version  = "3"
  }
  default_arguments = {
    "--job-bookmark-option"  = "job-bookmark-enable"
    "--datalake-formats"     = "iceberg"
    "--enable-metrics"       = "true"
  }
}

resource "aws_glue_job" "silver_to_gold" {
  name              = "${var.project}-silver-gold-${var.env}"
  role_arn          = aws_iam_role.glue.arn
  glue_version      = "4.0"
  worker_type       = "G.2X"
  number_of_workers = 8
  command {
    name            = "glueetl"
    script_location = "s3://${var.scripts_bucket}/silver_to_gold.py"
    python_version  = "3"
  }
  default_arguments = {
    "--job-bookmark-option" = "job-bookmark-enable"
    "--datalake-formats"    = "iceberg"
  }
}

# ── Lake Formation permissions ─────────────────────────────────────────────
resource "aws_lakeformation_permissions" "analyst_gold" {
  principal   = aws_iam_role.analyst.arn
  permissions = ["SELECT"]
  database { name = aws_glue_catalog_database.gold.name }
}

resource "aws_lakeformation_permissions" "de_silver" {
  principal   = aws_iam_role.data_engineer.arn
  permissions = ["ALL"]
  database { name = aws_glue_catalog_database.silver.name }
}

# ── Athena workgroup for consumption ───────────────────────────────────────
resource "aws_athena_workgroup" "lakehouse" {
  name = "${var.project}-lakehouse-${var.env}"
  configuration {
    result_configuration {
      output_location = "s3://${module.lake_bucket.bucket_ids["consumption"]}/athena-results/"
      encryption_configuration { encryption_option = "SSE_KMS"; kms_key_arn = aws_kms_key.lake.arn }
    }
    engine_version { selected_engine_version = "Athena engine version 3" }
    bytes_scanned_cutoff_per_query = 10737418240  # 10 GB guard
  }
}

# ── Step Functions pipeline ─────────────────────────────────────────────────
resource "aws_sfn_state_machine" "lakehouse_pipeline" {
  name     = "${var.project}-lakehouse-daily-${var.env}"
  role_arn = aws_iam_role.sfn.arn
  definition = jsonencode({
    StartAt = "IngestToBronze"
    States = {
      IngestToBronze = {
        Type     = "Task"
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Parameters = { JobName = "dms-cdc-ingest" }
        Next     = "BronzeToSilver"
        Retry    = [{ ErrorEquals = ["States.ALL"], MaxAttempts = 2, IntervalSeconds = 60 }]
      }
      BronzeToSilver = {
        Type     = "Task"
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Parameters = { JobName = aws_glue_job.bronze_to_silver.name }
        Next     = "SilverToGold"
        Retry    = [{ ErrorEquals = ["States.ALL"], MaxAttempts = 2, IntervalSeconds = 120 }]
      }
      SilverToGold = {
        Type     = "Task"
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Parameters = { JobName = aws_glue_job.silver_to_gold.name }
        Next     = "IcebergMaintenance"
        Retry    = [{ ErrorEquals = ["States.ALL"], MaxAttempts = 1 }]
      }
      IcebergMaintenance = {
        Type     = "Task"
        Resource = "arn:aws:states:::lambda:invoke"
        Parameters = { FunctionName = "iceberg-maintenance" }
        End = true
      }
    }
  })
}

# ── EventBridge scheduler (daily 5 AM UTC) ─────────────────────────────────
resource "aws_scheduler_schedule" "lakehouse_daily" {
  name                         = "${var.project}-daily-${var.env}"
  schedule_expression          = "cron(0 5 * * ? *)"
  schedule_expression_timezone = "UTC"
  flexible_time_window         = { mode = "OFF" }
  target = {
    arn      = aws_sfn_state_machine.lakehouse_pipeline.arn
    role_arn = aws_iam_role.scheduler.arn
    input    = jsonencode({ env = var.env })
  }
}
        """)
        tip(
            "Name all Glue jobs, Step Functions, and Athena workgroups with `${project}-${env}` prefix — makes CloudWatch filtering and cost allocation trivial.")

    # ── TAB 5: STREAMING KAPPA ──────────────────────────────────────────────
    with tab5:
        st.header("⚡ Streaming Kappa Architecture Pipeline on AWS")
        st.markdown("""> **Kappa architecture**: one streaming pipeline serves both real-time and historical use cases.
Replay is achieved by resetting consumer offsets (Kinesis/MSK) — no separate batch layer.""")

        st.code("""
┌──────────────────────────────────────────────────────────────────────────────┐
│  EVENT PRODUCERS                                                             │
│  Web / Mobile apps  → Kinesis Data Streams (user-events, order-events)     │
│  Microservices      → MSK (Kafka) topics (payments, inventory)             │
│  IoT devices        → IoT Core → Kinesis                                   │
└────────────────┬──────────────────────────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
┌──────────────┐   ┌──────────────────────────────────────────────────────┐
│  REAL-TIME   │   │  STREAM PROCESSING (Glue Streaming / Flink on EMR)   │
│  PATH        │   │                                                       │
│              │   │  1. Parse + validate schema (Glue Schema Registry)   │
│  Kinesis →   │   │  2. Deduplicate within watermark window             │
│  Lambda →    │   │  3. Enrich (join with Redis/DynamoDB ref data)       │
│  DynamoDB    │   │  4. Aggregate (tumbling/sliding windows)             │
│  (< 100ms)   │   │  5. MERGE into Iceberg (Silver) via foreachBatch    │
│              │   │  6. Emit alerts to SNS on anomalies                 │
│  Real-time   │   │                                                       │
│  API / UI    │   │  Checkpoint: s3://lake/checkpoints/{job}/           │
└──────────────┘   └──────────────────┬────────────────────────────────────┘
                                      │  Iceberg MERGE (every 60s)
                                      ▼
                   ┌──────────────────────────────────────────────────────┐
                   │  S3 ICEBERG TABLES  (single source of truth)         │
                   │  silver.events   — raw stream, partitioned by day   │
                   │  silver.sessions — sessionised, 30min idle timeout  │
                   │  gold.metrics    — pre-aggregated, refreshed hourly │
                   └──────────────────┬───────────────────────────────────┘
                                      │
                              ┌───────┴────────┐
                              ▼                ▼
                   ┌─────────────────┐  ┌─────────────────────┐
                   │ Athena (SQL)    │  │ SageMaker / EMR     │
                   │ QuickSight      │  │ (ML + batch queries) │
                   │ Redshift Spec.  │  │                      │
                   └─────────────────┘  └─────────────────────┘

REPLAY / REPROCESSING:
  Reset Kinesis shard iterator to TRIM_HORIZON (oldest available)
  OR reset Kafka consumer group offset to --to-earliest
  → Same streaming job reprocesses historical data into Iceberg
  → Iceberg MERGE ensures idempotency (no duplicates on replay)
        """, language="text")

        st.subheader("Glue Streaming Job – Kappa Pattern")
        st.code('''
# kappa_streaming_job.py — Kinesis → Iceberg (Glue Streaming)
import sys, json, boto3
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType

args  = getResolvedOptions(sys.argv, ["JOB_NAME","stream_name","checkpoint_bucket"])
sc    = SparkContext()
glue  = GlueContext(sc)
spark = glue.spark_session
job   = Job(glue)
job.init(args["JOB_NAME"], args)

for k, v in {
    "spark.sql.extensions":
        "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
    "spark.sql.catalog.glue_catalog": "org.apache.iceberg.spark.SparkCatalog",
    "spark.sql.catalog.glue_catalog.catalog-impl":
        "org.apache.iceberg.aws.glue.GlueCatalog",
    "spark.sql.catalog.glue_catalog.io-impl":
        "org.apache.iceberg.aws.s3.S3FileIO",
}.items():
    spark.conf.set(k, v)

event_schema = StructType([
    StructField("event_id",   StringType(), False),
    StructField("user_id",    StringType(), True),
    StructField("event_type", StringType(), True),
    StructField("amount",     DoubleType(), True),
    StructField("event_ts",   LongType(),   True),   # epoch ms
    StructField("session_id", StringType(), True),
])

kinesis_stream = glue.create_data_frame_from_options(
    connection_type="kinesis",
    connection_options={
        "typeOfData":       "kinesis",
        "streamARN":        f"arn:aws:kinesis:us-east-1:123456789:stream/{args['stream_name']}",
        "classification":   "json",
        "startingPosition": "LATEST",   # TRIM_HORIZON for replay
        "inferSchema":      "false",
    },
    format="json",
    transformation_ctx="kinesis_source",
)

def process_micro_batch(batch_df, batch_id):
    if batch_df.isEmpty():
        return

    parsed = (batch_df
        .withColumn("data", F.from_json(F.col("$json$data_infer_schema$_1"), event_schema))
        .select("data.*")
        .withColumn("event_ts",   F.to_timestamp(F.col("event_ts") / 1000))
        .withColumn("event_date", F.to_date("event_ts"))
        .dropDuplicates(["event_id"])
        .filter(F.col("event_id").isNotNull())
        .withColumn("_batch_id",     F.lit(batch_id))
        .withColumn("_processed_at", F.current_timestamp())
    )

    if parsed.count() == 0:
        return

    # MERGE into Silver Iceberg — exactly-once upsert
    view = f"batch_{batch_id}"
    parsed.createOrReplaceTempView(view)
    spark.sql(f"""
        MERGE INTO glue_catalog.silver.events t
        USING {view} s ON t.event_id = s.event_id
        WHEN MATCHED AND s.event_ts > t.event_ts THEN UPDATE SET *
        WHEN NOT MATCHED THEN INSERT *
    """)

    # Real-time alert: flag anomalous amounts
    anomaly_count = parsed.filter(F.col("amount") > 10000).count()
    if anomaly_count > 0:
        sns = boto3.client("sns")
        sns.publish(
            TopicArn="arn:aws:sns:us-east-1:123:anomaly-alerts",
            Message=json.dumps({"batch_id": batch_id, "anomaly_count": anomaly_count}),
        )

glue.forEachBatch(
    frame=kinesis_stream,
    batch_function=process_micro_batch,
    options={
        "windowSize":         "60 seconds",
        "checkpointLocation": f"s3://{args['checkpoint_bucket']}/streaming/{args['stream_name']}/",
        "batchMaxRetries":    3,
    },
)
job.commit()
        ''', language="python")

        st.subheader("Kappa Replay Pattern")
        bash("""
# ── Kinesis: replay from beginning ─────────────────────────────────────────
# 1. Stop running streaming job (Glue console or CLI)
aws glue stop-job-run --job-name kappa-streaming-job --run-id <run-id>

# 2. Delete checkpoint so job starts from beginning
aws s3 rm s3://my-lake/checkpoints/streaming/user-events/ --recursive

# 3. Change startingPosition to TRIM_HORIZON in job arguments
aws glue start-job-run \
  --job-name kappa-streaming-job \
  --arguments '{
    "--stream_name":       "user-events",
    "--checkpoint_bucket": "my-lake",
    "--starting_position": "TRIM_HORIZON"
  }'

# ── Kafka/MSK: replay from beginning ───────────────────────────────────────
# Reset consumer group to earliest offset
kafka-consumer-groups.sh \
  --bootstrap-server broker:9092 \
  --group kappa-streaming-consumer \
  --topic user-events \
  --reset-offsets --to-earliest --execute

# Or replay from specific timestamp
kafka-consumer-groups.sh \
  --bootstrap-server broker:9092 \
  --group kappa-streaming-consumer \
  --topic user-events \
  --reset-offsets --to-datetime 2024-01-01T00:00:00.000 --execute

# 4. Iceberg handles idempotency automatically via MERGE ON event_id
# No duplicates even if events are reprocessed
        """)

        st.subheader("Kappa Pipeline Monitoring")
        hcl("""
# CloudWatch dashboard for Kappa pipeline health
resource "aws_cloudwatch_dashboard" "kappa" {
  dashboard_name = "${var.project}-kappa-pipeline"
  dashboard_body = jsonencode({
    widgets = [
      {
        type = "metric"; properties = {
          title  = "Kinesis Iterator Age (lag)"
          metrics = [["AWS/Kinesis","GetRecords.IteratorAgeMilliseconds",
                      "StreamName","user-events",{stat="Maximum"}]]
          period = 60; view = "timeSeries"
          annotations = { horizontal = [{ value = 300000; label = "5min lag threshold" }] }
        }
      },
      {
        type = "metric"; properties = {
          title  = "Glue Streaming – Records Processed"
          metrics = [["Glue","glue.driver.streaming.numRecordsProcessed",
                      "JobName","kappa-streaming-job",{stat="Sum"}]]
          period = 60
        }
      },
      {
        type = "metric"; properties = {
          title  = "Iceberg Table – Silver Events Files"
          metrics = [["AWS/S3","NumberOfObjects","BucketName","my-lake",
                      "StorageType","AllStorageTypes",{stat="Average"}]]
          period = 3600
        }
      }
    ]
  })
}

# Alarm: streaming lag > 5 minutes
resource "aws_cloudwatch_metric_alarm" "kappa_lag" {
  alarm_name          = "kappa-streaming-lag-high"
  namespace           = "AWS/Kinesis"
  metric_name         = "GetRecords.IteratorAgeMilliseconds"
  dimensions          = { StreamName = "user-events" }
  statistic           = "Maximum"
  period              = 60
  evaluation_periods  = 3
  threshold           = 300000   # 5 minutes in ms
  comparison_operator = "GreaterThanThreshold"
  alarm_actions       = [aws_sns_topic.alerts.arn]
}
        """)
        tip("Set `startingPosition = TRIM_HORIZON` + delete checkpoint for full historical replay. Iceberg MERGE makes this idempotent — safe to replay multiple times.")
        warn("Kappa replay on Kinesis is limited by the stream's retention period (default 24h, max 1 year). For longer history, use MSK with unlimited retention or pre-populate from S3 raw files.")

    # ── TAB 6: DECISION MAP ─────────────────────────────────────────────────
    with tab6:
        st.header("🗺️ Pipeline Pattern Decision Map")
        st.markdown(
            "Use this guide to choose the right pipeline pattern for your use case.")

        st.subheader("Primary Decision Tree")
        st.code("""
What is your PRIMARY requirement?
│
├─ Need real-time / near-real-time results (< 5 min)?
│  └─→  KAPPA (Streaming) Pipeline
│       • Kinesis / MSK → Glue Streaming / Flink → Iceberg
│       • Real-time path: Lambda → DynamoDB for < 100ms API responses
│       • Replay via offset reset + Iceberg MERGE idempotency
│
├─ Need structured BI dashboards + fast SQL for business users?
│  └─→  DATA WAREHOUSE Pipeline
│       • DMS/AppFlow → S3 → Redshift COPY → dbt models → QuickSight
│       • Star schema, materialized views, WLM tuning
│       • Best: finance, sales, executive reporting
│
├─ Need flexible exploration + ML training + multi-team access?
│  └─→  DATA LAKE Pipeline
│       • All sources → S3 (Bronze/Silver/Gold)
│       • Glue ETL + EMR for transforms
│       • Athena for ad-hoc, Redshift Spectrum for BI, SageMaker for ML
│       • Best: data science teams, raw storage, archive, exploration
│
├─ Need ACID + real-time + BI + ML on the SAME data?
│  └─→  DATA LAKEHOUSE Pipeline
│       • Iceberg on S3 as single source of truth
│       • Streaming writes + batch reads on same Iceberg table
│       • Athena + Redshift Spectrum + SageMaker all query same table
│       • Best: modern unified platform, avoid data duplication
│
└─ Need to replicate operational DB to analytics with zero code?
   └─→  ZERO-ETL
        • Aurora / RDS → Redshift (AWS managed replication, seconds)
        • Still need dbt/Redshift procs for business logic
        • Best: simple source→DWH replication without custom ETL
        """, language="text")

        st.subheader("Latency vs Complexity Matrix")
        df = pd.DataFrame({
            "Pattern":          ["Zero-ETL", "ETL/ELT (Batch)", "Data Lake", "Data Lakehouse (Batch)", "Lakehouse (Streaming Kappa)", "Lambda Architecture"],
            "Data latency":     ["Seconds (replication)", "Hours (daily batch)", "Hours (daily batch)", "Hours (daily batch)", "Minutes (micro-batch)", "Seconds + Hours (dual)"],
            "Build complexity": ["⭐ Very low", "⭐⭐ Low", "⭐⭐⭐ Medium", "⭐⭐⭐ Medium", "⭐⭐⭐⭐ High", "⭐⭐⭐⭐⭐ Very high"],
            "Ops complexity":   ["⭐ Very low", "⭐⭐ Low", "⭐⭐⭐ Medium", "⭐⭐⭐ Medium", "⭐⭐⭐⭐ High", "⭐⭐⭐⭐⭐ Very high"],
            "Cost":             ["Low", "Low", "Medium", "Medium", "Medium-High", "High"],
            "Best for":         ["RDS→DWH replication", "Nightly reporting, DWH loads", "ML, exploration, archive", "Unified analytics + ML", "Real-time dashboards, fraud, IoT", "Legacy hybrid: different freshness needs"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("Service Selection per Pipeline")
        df2 = pd.DataFrame({
            "Layer":        ["Source systems", "Ingestion", "Stream processing", "Batch processing", "Storage", "Catalog", "Transformation", "Orchestration", "Query / BI", "Governance", "IaC"],
            "ETL/ELT":      ["RDS, Aurora, SaaS", "DMS, AppFlow, Glue JDBC", "—", "Glue ETL, dbt", "S3 + Redshift", "Glue Catalog", "dbt + Redshift SP", "MWAA / Step Functions", "Redshift, QuickSight", "Lake Formation", "Terraform"],
            "Data Lake":    ["All sources", "Firehose, DMS, AppFlow", "—", "Glue ETL, EMR", "S3 (Parquet + Iceberg)", "Glue Catalog", "Glue ETL, EMR Spark", "MWAA / Step Functions", "Athena, Redshift Spectrum", "Lake Formation + Macie", "Terraform"],
            "Lakehouse":    ["All sources", "Firehose, DMS, AppFlow", "—", "Glue ETL, EMR", "S3 Iceberg (Bronze/Silver/Gold)", "Glue Catalog", "Glue ETL, dbt-athena", "Step Functions + EventBridge", "Athena, Redshift Spectrum", "Lake Formation TBAC", "Terraform"],
            "Kappa Stream": ["Events, CDC streams", "Kinesis, MSK", "Glue Streaming, Flink (EMR)", "Replay via Glue Streaming", "S3 Iceberg", "Glue Catalog", "Stream MERGE + dbt (Gold)", "EventBridge Pipes + SFN", "Athena, QuickSight direct", "Lake Formation", "Terraform"],
        })
        st.dataframe(df2, use_container_width=True, hide_index=True)

        st.subheader("Key Checklist Before Going to Production")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
**Pipeline Checklist ✅**
- [ ] Idempotent jobs (safe to re-run / replay)
- [ ] Data quality gate before warehouse load
- [ ] PII masked before S3 landing
- [ ] Iceberg MERGE for upserts (not INSERT overwrite)
- [ ] Checkpoint location set for streaming jobs
- [ ] SNS alerts on job failure / DQ failure
- [ ] CloudWatch dashboard per pipeline
- [ ] Glue bookmark or streaming checkpoint enabled
- [ ] All resources tagged for cost attribution
- [ ] Lake Formation permissions reviewed
            """)
        with col2:
            st.markdown("""
**Operational Readiness ✅**
- [ ] Runbook documented for each pipeline
- [ ] Replay / backfill procedure tested
- [ ] Vacuum + Iceberg compaction scheduled
- [ ] S3 lifecycle rules on raw zone
- [ ] Redshift usage limit set (Serverless)
- [ ] DMS replication instance sized correctly
- [ ] MSK broker storage auto-expand enabled
- [ ] Kinesis shard count reviewed quarterly
- [ ] Terraform state in remote S3 + DynamoDB lock
- [ ] dbt tests run in CI on every PR
            """)

# ════════════════════════════════════════════════════════════════════════════
# Sidebar footer
# ════════════════════════════════════════════════════════════════════════════
st.sidebar.markdown("---")
st.sidebar.markdown("**v2** · 17 sections · 25+ services")
st.sidebar.caption("AWS DE Cheat Sheet · Expanded Edition")

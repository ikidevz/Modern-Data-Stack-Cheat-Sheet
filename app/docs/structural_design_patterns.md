# Structural Design Patterns

> A professional guide for Data Analytics, Data Science, Data Engineering & Analytics Engineering in Python

Structural design patterns deal with how classes and objects are composed to form larger structures. They simplify complex relationships between entities, making your architecture more flexible and efficient.

---

## 1. Adapter Pattern

**Intent:** Convert the interface of a class into another interface that clients expect. Allows classes with incompatible interfaces to work together.

**Use Case in Data:** Wrapping different data source APIs (Pandas, Spark, Polars) under a unified interface.

### Example 1 — Unified DataFrame Adapter (Pandas ↔ Polars)

```python
from abc import ABC, abstractmethod
import pandas as pd

class DataFrameInterface(ABC):
    @abstractmethod
    def to_pandas(self) -> pd.DataFrame: pass

    @abstractmethod
    def shape(self) -> tuple: pass

    @abstractmethod
    def column_names(self) -> list: pass

class PandasAdapter(DataFrameInterface):
    def __init__(self, df: pd.DataFrame):
        self._df = df

    def to_pandas(self) -> pd.DataFrame:
        return self._df

    def shape(self) -> tuple:
        return self._df.shape

    def column_names(self) -> list:
        return self._df.columns.tolist()

class PolarsAdapter(DataFrameInterface):
    """Adapts a Polars DataFrame to the unified DataFrameInterface."""
    def __init__(self, df):  # df: pl.DataFrame
        self._df = df

    def to_pandas(self) -> pd.DataFrame:
        return self._df.to_pandas()

    def shape(self) -> tuple:
        return (self._df.height, self._df.width)

    def column_names(self) -> list:
        return self._df.columns


def summarize(df_adapter: DataFrameInterface):
    """Client code — works with any adapter."""
    print(f"Shape: {df_adapter.shape()}")
    print(f"Columns: {df_adapter.column_names()}")
    return df_adapter.to_pandas().describe()


# Usage
pandas_df = pd.read_csv("sales.csv")
adapter = PandasAdapter(pandas_df)
print(summarize(adapter))

# import polars as pl
# polars_df = pl.read_parquet("sales.parquet")
# adapter = PolarsAdapter(polars_df)
# print(summarize(adapter))
```

### Example 2 — Legacy API to Modern Pipeline Adapter

```python
class LegacyReportGenerator:
    """Old system that generates flat dicts — cannot be changed."""
    def generate(self, start_date: str, end_date: str) -> list:
        # Returns flat list of dicts (legacy format)
        return [
            {"date": "2024-01-01", "sales": 1000, "region": "APAC"},
            {"date": "2024-01-02", "sales": 1500, "region": "EMEA"},
        ]

class ModernDataPipeline:
    """New pipeline expects DataFrames."""
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        df["sales_cumulative"] = df["sales"].cumsum()
        return df

class LegacyReportAdapter:
    """Adapts LegacyReportGenerator output for ModernDataPipeline."""
    def __init__(self, legacy: LegacyReportGenerator):
        self._legacy = legacy

    def get_dataframe(self, start_date: str, end_date: str) -> pd.DataFrame:
        raw = self._legacy.generate(start_date, end_date)
        df = pd.DataFrame(raw)
        df["date"] = pd.to_datetime(df["date"])
        return df


# Usage
legacy = LegacyReportGenerator()
adapter = LegacyReportAdapter(legacy)
df = adapter.get_dataframe("2024-01-01", "2024-01-31")

pipeline = ModernDataPipeline()
result = pipeline.process(df)
print(result)
```

### Example 3 — Multi-Cloud Storage Adapter

```python
from abc import ABC, abstractmethod

class StorageInterface(ABC):
    @abstractmethod
    def read(self, path: str) -> bytes: pass

    @abstractmethod
    def write(self, path: str, data: bytes): pass

class S3Adapter(StorageInterface):
    def __init__(self, bucket: str):
        import boto3
        self._client = boto3.client("s3")
        self._bucket = bucket

    def read(self, path: str) -> bytes:
        obj = self._client.get_object(Bucket=self._bucket, Key=path)
        return obj["Body"].read()

    def write(self, path: str, data: bytes):
        self._client.put_object(Bucket=self._bucket, Key=path, Body=data)

class GCSAdapter(StorageInterface):
    def __init__(self, bucket_name: str):
        from google.cloud import storage
        self._bucket = storage.Client().bucket(bucket_name)

    def read(self, path: str) -> bytes:
        return self._bucket.blob(path).download_as_bytes()

    def write(self, path: str, data: bytes):
        self._bucket.blob(path).upload_from_string(data)


def save_model_artifact(storage: StorageInterface, model_bytes: bytes, path: str):
    storage.write(path, model_bytes)
    print(f"Model artifact saved to {path}")


# Usage — swap cloud provider without changing business logic
storage = S3Adapter("ml-artifacts-bucket")
# storage = GCSAdapter("ml-artifacts-bucket")
save_model_artifact(storage, b"<model_bytes>", "models/churn/v2/model.pkl")
```

---

## 2. Bridge Pattern

**Intent:** Decouple an abstraction from its implementation so that the two can vary independently.

**Use Case in Data:** Separating pipeline logic (batch vs. streaming) from storage backends (S3, GCS, HDFS).

### Example 1 — Data Pipeline with Interchangeable Storage Backends

```python
from abc import ABC, abstractmethod
import pandas as pd

# Implementation Interface
class StorageBackend(ABC):
    @abstractmethod
    def save(self, df: pd.DataFrame, name: str): pass

    @abstractmethod
    def load(self, name: str) -> pd.DataFrame: pass

# Concrete Implementations
class S3Backend(StorageBackend):
    def __init__(self, bucket: str):
        self.bucket = bucket

    def save(self, df: pd.DataFrame, name: str):
        path = f"s3://{self.bucket}/{name}.parquet"
        df.to_parquet(path)
        print(f"[S3Backend] Saved to {path}")

    def load(self, name: str) -> pd.DataFrame:
        path = f"s3://{self.bucket}/{name}.parquet"
        return pd.read_parquet(path)

class LocalBackend(StorageBackend):
    def __init__(self, base_dir: str = "/tmp/data"):
        self.base_dir = base_dir

    def save(self, df: pd.DataFrame, name: str):
        path = f"{self.base_dir}/{name}.parquet"
        df.to_parquet(path)
        print(f"[LocalBackend] Saved to {path}")

    def load(self, name: str) -> pd.DataFrame:
        return pd.read_parquet(f"{self.base_dir}/{name}.parquet")

# Abstraction
class DataPipeline(ABC):
    def __init__(self, storage: StorageBackend):
        self.storage = storage  # Bridge to implementation

    @abstractmethod
    def run(self, source_name: str, output_name: str): pass

# Refined Abstractions
class BatchPipeline(DataPipeline):
    def run(self, source_name: str, output_name: str):
        df = self.storage.load(source_name)
        df = df.dropna().reset_index(drop=True)
        df["processed"] = True
        self.storage.save(df, output_name)
        print(f"[BatchPipeline] Processed {len(df)} rows")

class AggregationPipeline(DataPipeline):
    def __init__(self, storage: StorageBackend, group_col: str, agg_col: str):
        super().__init__(storage)
        self.group_col = group_col
        self.agg_col = agg_col

    def run(self, source_name: str, output_name: str):
        df = self.storage.load(source_name)
        result = df.groupby(self.group_col)[self.agg_col].sum().reset_index()
        self.storage.save(result, output_name)
        print(f"[AggregationPipeline] Aggregated {len(result)} groups")


# Usage — swap backend without changing pipeline logic
local = LocalBackend("/data/warehouse")
batch = BatchPipeline(local)
batch.run("raw_orders", "clean_orders")

s3 = S3Backend("prod-datalake")
agg = AggregationPipeline(s3, group_col="region", agg_col="revenue")
agg.run("clean_orders", "region_revenue_summary")
```

### Example 2 — Report Renderer with Interchangeable Format Backends

```python
from abc import ABC, abstractmethod
import pandas as pd

# Implementation: Rendering Backends
class RenderBackend(ABC):
    @abstractmethod
    def render_table(self, df: pd.DataFrame, title: str) -> str: pass

    @abstractmethod
    def render_summary(self, stats: dict) -> str: pass

class MarkdownBackend(RenderBackend):
    def render_table(self, df: pd.DataFrame, title: str) -> str:
        return f"## {title}\n\n{df.to_markdown(index=False)}\n"

    def render_summary(self, stats: dict) -> str:
        lines = ["### Summary", "| Metric | Value |", "|--------|-------|"]
        lines += [f"| {k} | {v} |" for k, v in stats.items()]
        return "\n".join(lines)

class HTMLBackend(RenderBackend):
    def render_table(self, df: pd.DataFrame, title: str) -> str:
        return f"<h2>{title}</h2>\n{df.to_html(index=False)}\n"

    def render_summary(self, stats: dict) -> str:
        rows = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in stats.items())
        return f"<table><tr><th>Metric</th><th>Value</th></tr>{rows}</table>"

# Abstraction: Report Types
class AnalyticsReport(ABC):
    def __init__(self, backend: RenderBackend):
        self.backend = backend  # Bridge to renderer

    @abstractmethod
    def generate(self, df: pd.DataFrame) -> str: pass

class SalesReport(AnalyticsReport):
    def generate(self, df: pd.DataFrame) -> str:
        stats = {
            "Total Revenue": f"${df['amount'].sum():,.2f}",
            "Avg Order Value": f"${df['amount'].mean():,.2f}",
            "Total Orders": len(df),
        }
        top10 = df.nlargest(10, "amount")[["order_id", "customer_id", "amount"]]
        return self.backend.render_summary(stats) + "\n\n" + self.backend.render_table(top10, "Top 10 Orders")

class CustomerReport(AnalyticsReport):
    def generate(self, df: pd.DataFrame) -> str:
        summary = df.groupby("region")["amount"].agg(["sum", "count", "mean"]).reset_index()
        summary.columns = ["Region", "Revenue", "Orders", "AOV"]
        stats = {"Regions": df["region"].nunique(), "Total Customers": df["customer_id"].nunique()}
        return self.backend.render_summary(stats) + "\n\n" + self.backend.render_table(summary, "Revenue by Region")


# Usage — swap renderer without changing report logic
df = pd.read_parquet("orders.parquet")

md_report = SalesReport(MarkdownBackend())
html_report = CustomerReport(HTMLBackend())

with open("sales_report.md", "w") as f:
    f.write(md_report.generate(df))

with open("customer_report.html", "w") as f:
    f.write(html_report.generate(df))
```

### Example 3 — Notification System with Interchangeable Channels

```python
from abc import ABC, abstractmethod

# Implementation: Notification Channels
class NotificationChannel(ABC):
    @abstractmethod
    def send(self, subject: str, body: str): pass

class SlackChannel(NotificationChannel):
    def __init__(self, webhook_url: str, channel: str):
        self.webhook_url = webhook_url
        self.channel = channel

    def send(self, subject: str, body: str):
        print(f"[Slack → {self.channel}] *{subject}*\n{body}")
        # requests.post(self.webhook_url, json={"text": f"*{subject}*\n{body}"})

class EmailChannel(NotificationChannel):
    def __init__(self, recipients: list):
        self.recipients = recipients

    def send(self, subject: str, body: str):
        print(f"[Email → {', '.join(self.recipients)}] Subject: {subject}\n{body}")

class PagerDutyChannel(NotificationChannel):
    def __init__(self, routing_key: str, severity: str = "critical"):
        self.routing_key = routing_key
        self.severity = severity

    def send(self, subject: str, body: str):
        print(f"[PagerDuty | {self.severity}] {subject}: {body}")

# Abstraction: Alert Types
class DataAlert(ABC):
    def __init__(self, channel: NotificationChannel):
        self.channel = channel  # Bridge

    @abstractmethod
    def trigger(self, context: dict): pass

class PipelineFailureAlert(DataAlert):
    def trigger(self, context: dict):
        subject = f"❌ Pipeline Failed: {context['pipeline']}"
        body = f"Error: {context['error']}\nTime: {context['timestamp']}\nRows processed: {context.get('rows', 'N/A')}"
        self.channel.send(subject, body)

class DataQualityAlert(DataAlert):
    def trigger(self, context: dict):
        subject = f"⚠ DQ Issue: {context['table']}"
        body = f"Null rate: {context['null_rate']:.2%} | Dup rate: {context['dup_rate']:.2%}\nThreshold breached: {context['metric']}"
        self.channel.send(subject, body)

class ModelDriftAlert(DataAlert):
    def trigger(self, context: dict):
        subject = f"🔴 Model Drift Detected: {context['model']}"
        body = f"PSI: {context['psi']:.4f} | Threshold: {context['threshold']}\nAction required: retrain or rollback."
        self.channel.send(subject, body)


# Usage — swap channel without changing alert logic
slack = SlackChannel("https://hooks.slack.com/xxx", "#data-alerts")
email = EmailChannel(["data-team@company.com", "oncall@company.com"])
pager = PagerDutyChannel(routing_key="abc123", severity="critical")

# Same alert, different channels
PipelineFailureAlert(slack).trigger({"pipeline": "daily_etl", "error": "Timeout", "timestamp": "2024-01-15 03:00Z"})
PipelineFailureAlert(pager).trigger({"pipeline": "daily_etl", "error": "Timeout", "timestamp": "2024-01-15 03:00Z"})
DataQualityAlert(email).trigger({"table": "fact_orders", "null_rate": 0.12, "dup_rate": 0.03, "metric": "null_rate"})
ModelDriftAlert(slack).trigger({"model": "churn_v3", "psi": 0.31, "threshold": 0.20})
```

---

## 3. Composite Pattern

**Intent:** Compose objects into tree structures to represent part-whole hierarchies. Lets clients treat individual objects and compositions of objects uniformly.

**Use Case in Data:** Building composite data quality check suites, hierarchical metric trees, or nested transformation pipelines.

### Example 1 — Composite Data Quality Suite

```python
from abc import ABC, abstractmethod
import pandas as pd

class DataQualityCheck(ABC):
    @abstractmethod
    def run(self, df: pd.DataFrame) -> dict: pass

# Leaf
class NullCheck(DataQualityCheck):
    def __init__(self, column: str):
        self.column = column

    def run(self, df: pd.DataFrame) -> dict:
        null_count = int(df[self.column].isnull().sum())
        return {
            "check": f"NullCheck[{self.column}]",
            "passed": null_count == 0,
            "details": f"{null_count} nulls found"
        }

class RangeCheck(DataQualityCheck):
    def __init__(self, column: str, min_val, max_val):
        self.column, self.min_val, self.max_val = column, min_val, max_val

    def run(self, df: pd.DataFrame) -> dict:
        out_of_range = int(((df[self.column] < self.min_val) | (df[self.column] > self.max_val)).sum())
        return {
            "check": f"RangeCheck[{self.column}]",
            "passed": out_of_range == 0,
            "details": f"{out_of_range} values out of [{self.min_val}, {self.max_val}]"
        }

# Composite
class QualitySuite(DataQualityCheck):
    def __init__(self, name: str):
        self.name = name
        self._checks: list[DataQualityCheck] = []

    def add(self, check: DataQualityCheck):
        self._checks.append(check)
        return self

    def run(self, df: pd.DataFrame) -> dict:
        results = [c.run(df) for c in self._checks]
        all_passed = all(r["passed"] for r in results)
        return {
            "suite": self.name,
            "passed": all_passed,
            "results": results
        }


# Usage
sales_suite = (
    QualitySuite("Sales Quality Checks")
    .add(NullCheck("order_id"))
    .add(NullCheck("customer_id"))
    .add(RangeCheck("amount", 0, 1_000_000))
    .add(RangeCheck("discount", 0, 1))
)

full_suite = (
    QualitySuite("Full DQ Suite")
    .add(sales_suite)  # Nested composite
    .add(NullCheck("created_at"))
)

df = pd.read_parquet("orders.parquet")
report = full_suite.run(df)
print(report)
```

### Example 2 — Hierarchical Metric Tree

```python
from abc import ABC, abstractmethod

class Metric(ABC):
    @abstractmethod
    def compute(self, data: dict) -> float: pass

    @abstractmethod
    def name(self) -> str: pass

class LeafMetric(Metric):
    def __init__(self, metric_name: str, fn):
        self._name = metric_name
        self._fn = fn

    def name(self) -> str:
        return self._name

    def compute(self, data: dict) -> float:
        return self._fn(data)

class CompositeMetric(Metric):
    def __init__(self, metric_name: str, aggregation="sum"):
        self._name = metric_name
        self._children: list[Metric] = []
        self._agg = aggregation

    def add(self, metric: Metric):
        self._children.append(metric)
        return self

    def name(self) -> str:
        return self._name

    def compute(self, data: dict) -> float:
        values = [c.compute(data) for c in self._children]
        if self._agg == "sum":
            return sum(values)
        elif self._agg == "avg":
            return sum(values) / len(values)
        return sum(values)


# Usage
revenue_tree = (
    CompositeMetric("Total Revenue", aggregation="sum")
    .add(LeafMetric("APAC Revenue", lambda d: d.get("apac_revenue", 0)))
    .add(LeafMetric("EMEA Revenue", lambda d: d.get("emea_revenue", 0)))
    .add(
        CompositeMetric("Americas Revenue", aggregation="sum")
        .add(LeafMetric("North America", lambda d: d.get("na_revenue", 0)))
        .add(LeafMetric("South America", lambda d: d.get("sa_revenue", 0)))
    )
)

data = {"apac_revenue": 120000, "emea_revenue": 95000, "na_revenue": 200000, "sa_revenue": 30000}
print(f"Total Revenue: ${revenue_tree.compute(data):,.0f}")
```

---

## 4. Decorator Pattern

**Intent:** Attach additional responsibilities to an object dynamically. Provides a flexible alternative to subclassing for extending functionality.

**Use Case in Data:** Adding logging, caching, validation, and retry logic to data pipeline steps without modifying core logic.

### Example 1 — Pipeline Step Decorator Chain

```python
import pandas as pd
import time
import functools
from typing import Callable

# Decorator: Logging
def log_step(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(df: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        print(f"[LOG] Running: {func.__name__} | Input shape: {df.shape}")
        result = func(df, *args, **kwargs)
        print(f"[LOG] Done: {func.__name__} | Output shape: {result.shape}")
        return result
    return wrapper

# Decorator: Timing
def timeit(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(df: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        start = time.time()
        result = func(df, *args, **kwargs)
        elapsed = time.time() - start
        print(f"[TIMER] {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

# Decorator: Null validation
def validate_no_nulls(columns: list):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(df: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
            nulls = {col: int(df[col].isnull().sum()) for col in columns if col in df.columns}
            if any(v > 0 for v in nulls.values()):
                raise ValueError(f"[VALIDATE] Null check failed: {nulls}")
            return func(df, *args, **kwargs)
        return wrapper
    return decorator


# Pipeline functions with decorators
@timeit
@log_step
@validate_no_nulls(["order_id", "customer_id"])
def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(subset=["amount"]).reset_index(drop=True)

@timeit
@log_step
def add_revenue_tier(df: pd.DataFrame) -> pd.DataFrame:
    df["revenue_tier"] = pd.cut(df["amount"], bins=[0, 100, 1000, float("inf")],
                                 labels=["low", "mid", "high"])
    return df


# Usage
df = pd.read_csv("orders.csv")
df = clean_orders(df)
df = add_revenue_tier(df)
```

### Example 2 — Retry Decorator for Data Ingestion

```python
import time
import functools

def retry(max_attempts: int = 3, delay: float = 2.0, exceptions=(Exception,)):
    """Retry decorator for flaky data source connections."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    print(f"[RETRY] Attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise RuntimeError(f"All {max_attempts} attempts failed.") from last_exc
        return wrapper
    return decorator

def cache_result(func):
    """Simple in-memory caching decorator."""
    _cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in _cache:
            _cache[args] = func(*args)
        else:
            print(f"[CACHE] Returning cached result for {args}")
        return _cache[args]
    return wrapper


@retry(max_attempts=3, delay=1.5, exceptions=(ConnectionError, TimeoutError))
@cache_result
def fetch_from_api(endpoint: str) -> dict:
    """Fetch data from an unstable external API."""
    import requests
    response = requests.get(endpoint, timeout=10)
    response.raise_for_status()
    return response.json()


# Usage
data = fetch_from_api("https://api.example.com/v1/sales?date=2024-01-01")
data_cached = fetch_from_api("https://api.example.com/v1/sales?date=2024-01-01")  # from cache
```

---

## 5. Facade Pattern

**Intent:** Provide a simplified interface to a complex subsystem.

**Use Case in Data:** A single `DataPipeline` class that hides the complexity of reading, transforming, validating, and writing data.

### Example 1 — Data Platform Facade

```python
import pandas as pd

# Complex subsystems
class DataIngestion:
    def read_parquet(self, path: str) -> pd.DataFrame:
        print(f"[Ingestion] Reading {path}")
        return pd.read_parquet(path)

class DataTransformer:
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.dropna().reset_index(drop=True)

    def enrich(self, df: pd.DataFrame) -> pd.DataFrame:
        df["processed_at"] = pd.Timestamp.utcnow()
        return df

class DataValidator:
    def check(self, df: pd.DataFrame, required_cols: list) -> bool:
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")
        return True

class DataWriter:
    def write_parquet(self, df: pd.DataFrame, path: str):
        df.to_parquet(path, index=False)
        print(f"[Writer] Written to {path}")

# Facade
class ETLFacade:
    """Simplified interface hiding the complexity of the ETL subsystem."""
    def __init__(self):
        self._ingestion = DataIngestion()
        self._transformer = DataTransformer()
        self._validator = DataValidator()
        self._writer = DataWriter()

    def run(self, source: str, destination: str, required_cols: list = None):
        df = self._ingestion.read_parquet(source)
        df = self._transformer.clean(df)
        df = self._transformer.enrich(df)
        if required_cols:
            self._validator.check(df, required_cols)
        self._writer.write_parquet(df, destination)
        print(f"[ETLFacade] Pipeline complete. {len(df)} rows processed.")
        return df


# Usage — one simple call
etl = ETLFacade()
df = etl.run(
    source="s3://raw/sales.parquet",
    destination="s3://processed/sales_clean.parquet",
    required_cols=["order_id", "customer_id", "amount"]
)
```

### Example 2 — ML Model Training Facade

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report
import joblib

class MLTrainingFacade:
    """Hides the full ML training lifecycle behind a single interface."""

    def train(self, data_path: str, target: str, model_path: str, test_size: float = 0.2):
        # Load
        df = pd.read_parquet(data_path)
        X = df.drop(columns=[target])
        y = df[target]

        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        # Train
        model = GradientBoostingClassifier(n_estimators=200, max_depth=5)
        model.fit(X_train, y_train)

        # Evaluate
        y_pred = model.predict(X_test)
        print(classification_report(y_test, y_pred))

        # Persist
        joblib.dump(model, model_path)
        print(f"[MLFacade] Model saved to {model_path}")
        return model


# Usage
facade = MLTrainingFacade()
model = facade.train(
    data_path="s3://ml-data/churn/features.parquet",
    target="churn",
    model_path="models/churn_gbm_v3.pkl"
)
```

---

## 6. Flyweight Pattern

**Intent:** Use sharing to efficiently support a large number of fine-grained objects by externalizing state.

**Use Case in Data:** Caching shared schema/column metadata objects to avoid memory explosion when processing millions of rows or many tables.

### Example 1 — Column Metadata Flyweight Cache

```python
import pandas as pd

class ColumnMetadata:
    """Shared, immutable metadata for a column — the Flyweight object."""
    def __init__(self, name: str, dtype: str, nullable: bool, description: str = ""):
        self.name = name
        self.dtype = dtype
        self.nullable = nullable
        self.description = description

    def __repr__(self):
        return f"ColumnMetadata(name={self.name}, dtype={self.dtype}, nullable={self.nullable})"

class ColumnMetadataFactory:
    """Flyweight factory — returns shared instances."""
    _pool: dict[str, ColumnMetadata] = {}

    @classmethod
    def get(cls, name: str, dtype: str, nullable: bool, description: str = "") -> ColumnMetadata:
        key = f"{name}|{dtype}|{nullable}"
        if key not in cls._pool:
            cls._pool[key] = ColumnMetadata(name, dtype, nullable, description)
            print(f"[Flyweight] Created: {key}")
        else:
            print(f"[Flyweight] Reused: {key}")
        return cls._pool[key]

    @classmethod
    def pool_size(cls) -> int:
        return len(cls._pool)


# Usage — thousands of tables share the same column metadata instances
schemas = []
for table_id in range(1000):
    schema = [
        ColumnMetadataFactory.get("order_id", "int64", False, "Unique order identifier"),
        ColumnMetadataFactory.get("customer_id", "int64", False, "Customer foreign key"),
        ColumnMetadataFactory.get("amount", "float64", True, "Order amount in USD"),
    ]
    schemas.append(schema)

print(f"\nTotal tables: 1000 | Flyweight pool size: {ColumnMetadataFactory.pool_size()}")
```

### Example 2 — Shared Data Type Registry for Schema Validation

```python
class DataTypeSpec:
    """Flyweight: immutable shared type specification."""
    def __init__(self, type_name: str, python_type: type, nullable: bool, validators: list):
        self.type_name = type_name
        self.python_type = python_type
        self.nullable = nullable
        self.validators = validators  # list of validation functions

    def validate(self, value) -> bool:
        if value is None:
            return self.nullable
        if not isinstance(value, self.python_type):
            return False
        return all(v(value) for v in self.validators)

    def __repr__(self):
        return f"DataTypeSpec({self.type_name})"

class TypeRegistry:
    """Flyweight factory for type specs — shared across all schema objects."""
    _specs: dict[str, DataTypeSpec] = {}

    @classmethod
    def register(cls, type_name: str, python_type: type, nullable: bool, validators: list = None):
        if type_name not in cls._specs:
            cls._specs[type_name] = DataTypeSpec(type_name, python_type, nullable, validators or [])
            print(f"[TypeRegistry] Registered: {type_name}")
        return cls._specs[type_name]

    @classmethod
    def get(cls, type_name: str) -> DataTypeSpec:
        if type_name not in cls._specs:
            raise KeyError(f"Unknown type: {type_name}")
        return cls._specs[type_name]

class SchemaField:
    """Extrinsic state — field name + shared intrinsic DataTypeSpec."""
    def __init__(self, field_name: str, type_spec: DataTypeSpec):
        self.field_name = field_name       # extrinsic (unique per field)
        self.type_spec = type_spec          # intrinsic (shared flyweight)

    def validate(self, value) -> bool:
        return self.type_spec.validate(value)


# Register shared type specs once
TypeRegistry.register("positive_float", float, False, [lambda v: v >= 0])
TypeRegistry.register("nullable_str", str, True)
TypeRegistry.register("positive_int", int, False, [lambda v: v > 0])

# Thousands of schema fields share the same DataTypeSpec objects
fields = []
for i in range(10_000):
    fields.append(SchemaField(f"amount_{i}", TypeRegistry.get("positive_float")))
    fields.append(SchemaField(f"note_{i}", TypeRegistry.get("nullable_str")))

import sys
spec_count = len(TypeRegistry._specs)
print(f"Fields: {len(fields):,} | Shared type specs: {spec_count} | Memory savings: huge")
print(f"All 'amount' fields share ONE spec: {fields[0].type_spec is fields[2].type_spec}")
```

### Example 3 — Cached Tokenizer for NLP Feature Engineering

```python
import re
from functools import lru_cache

class TokenizerConfig:
    """Flyweight: shared immutable tokenizer configuration."""
    def __init__(self, language: str, lowercase: bool, remove_stopwords: bool, stopwords: frozenset):
        self.language = language
        self.lowercase = lowercase
        self.remove_stopwords = remove_stopwords
        self.stopwords = stopwords  # frozenset — immutable, hashable

    def tokenize(self, text: str) -> list:
        if self.lowercase:
            text = text.lower()
        tokens = re.findall(r"\b\w+\b", text)
        if self.remove_stopwords:
            tokens = [t for t in tokens if t not in self.stopwords]
        return tokens

class TokenizerPool:
    """Flyweight factory — reuses tokenizer configs across millions of rows."""
    _pool: dict[tuple, TokenizerConfig] = {}

    @classmethod
    def get(cls, language: str, lowercase: bool, remove_stopwords: bool) -> TokenizerConfig:
        EN_STOPWORDS = frozenset(["the", "a", "an", "is", "in", "on", "at", "to", "and", "or", "of"])
        key = (language, lowercase, remove_stopwords)
        if key not in cls._pool:
            cls._pool[key] = TokenizerConfig(language, lowercase, remove_stopwords, EN_STOPWORDS)
            print(f"[TokenizerPool] Created config: {key}")
        return cls._pool[key]


# Usage — millions of text rows reuse the same tokenizer config
import pandas as pd

df = pd.DataFrame({
    "review_id": range(1_000_000),
    "text": ["The product is great and amazing"] * 1_000_000
})

# All rows share ONE tokenizer config instance — no per-row object creation
config = TokenizerPool.get("en", lowercase=True, remove_stopwords=True)
df["tokens"] = df["text"].apply(config.tokenize)

print(f"Processed {len(df):,} rows | Tokenizer configs in pool: {len(TokenizerPool._pool)}")
print(df["tokens"].iloc[0])
```

---

## 7. Proxy Pattern

**Intent:** Provide a surrogate or placeholder for another object to control access to it.

**Use Case in Data:** Lazy-loading large datasets, access-controlled data views, or transparent query result caching.

### Example 1 — Lazy-Loading Dataset Proxy

```python
import pandas as pd

class RealDataset:
    def __init__(self, path: str):
        print(f"[RealDataset] Loading dataset from {path}...")
        self._df = pd.read_parquet(path)

    def query(self, sql: str) -> pd.DataFrame:
        import pandasql as ps
        return ps.sqldf(sql, {"df": self._df})

    def shape(self) -> tuple:
        return self._df.shape

class LazyDatasetProxy:
    """Proxy: defers loading the dataset until it's actually needed."""
    def __init__(self, path: str):
        self._path = path
        self._real = None  # Not loaded yet

    def _ensure_loaded(self):
        if self._real is None:
            self._real = RealDataset(self._path)

    def query(self, sql: str) -> pd.DataFrame:
        self._ensure_loaded()
        return self._real.query(sql)

    def shape(self) -> tuple:
        self._ensure_loaded()
        return self._real.shape()


# Usage
dataset = LazyDatasetProxy("s3://datalake/fact_sales.parquet")
print("Proxy created — dataset NOT yet loaded.")

# Loads only when first accessed
shape = dataset.shape()
print(f"Shape: {shape}")
```

### Example 2 — Caching Query Proxy

```python
import hashlib
import pandas as pd

class QueryExecutor:
    """Real subject: executes SQL queries against a database."""
    def run(self, query: str) -> pd.DataFrame:
        print(f"[QueryExecutor] Running query: {query[:60]}...")
        # Simulated DB call
        return pd.DataFrame({"id": range(10), "value": range(10)})

class CachingQueryProxy:
    """Proxy: caches query results to avoid repeated expensive DB calls."""
    def __init__(self, executor: QueryExecutor):
        self._executor = executor
        self._cache: dict[str, pd.DataFrame] = {}

    def _hash(self, query: str) -> str:
        return hashlib.md5(query.encode()).hexdigest()

    def run(self, query: str) -> pd.DataFrame:
        key = self._hash(query)
        if key in self._cache:
            print(f"[CachingProxy] Cache hit for query hash: {key[:8]}")
            return self._cache[key]
        result = self._executor.run(query)
        self._cache[key] = result
        return result


# Usage
executor = QueryExecutor()
proxy = CachingQueryProxy(executor)

df1 = proxy.run("SELECT * FROM fact_sales WHERE year = 2024")
df2 = proxy.run("SELECT * FROM fact_sales WHERE year = 2024")  # cache hit
df3 = proxy.run("SELECT * FROM fact_sales WHERE year = 2023")  # new query
```

### Example 3 — Access Control Proxy

```python
import pandas as pd

class SensitiveDataset:
    def __init__(self, df: pd.DataFrame):
        self._df = df

    def get_data(self) -> pd.DataFrame:
        return self._df

class DataAccessProxy:
    """Proxy that enforces role-based column access control."""
    _allowed_columns = {
        "analyst": ["order_id", "order_date", "revenue", "region"],
        "data_scientist": ["order_id", "order_date", "revenue", "region", "customer_id"],
        "admin": None,  # All columns
    }

    def __init__(self, dataset: SensitiveDataset, role: str):
        self._dataset = dataset
        self._role = role

    def get_data(self) -> pd.DataFrame:
        df = self._dataset.get_data()
        allowed = self._allowed_columns.get(self._role)
        if allowed is None:
            return df
        available = [c for c in allowed if c in df.columns]
        print(f"[AccessProxy] Role '{self._role}' — exposing columns: {available}")
        return df[available]


# Usage
raw = pd.DataFrame({
    "order_id": [1, 2], "order_date": ["2024-01-01", "2024-01-02"],
    "revenue": [500, 750], "region": ["APAC", "EMEA"],
    "customer_id": [101, 102], "email": ["a@x.com", "b@x.com"]
})

dataset = SensitiveDataset(raw)

analyst_view = DataAccessProxy(dataset, "analyst").get_data()
ds_view = DataAccessProxy(dataset, "data_scientist").get_data()
admin_view = DataAccessProxy(dataset, "admin").get_data()
```

---

_Document covers: Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy_
_Domain: Data Analytics · Data Science · Data Engineering · Analytics Engineering_

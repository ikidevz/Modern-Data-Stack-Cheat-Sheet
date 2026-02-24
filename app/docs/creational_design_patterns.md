# Creational Design Patterns

> A professional guide for Data Analytics, Data Science, Data Engineering & Analytics Engineering in Python

Creational design patterns deal with object creation mechanisms, aiming to create objects in a manner suited to the situation. They abstract the instantiation process and help make systems independent of how their objects are created, composed, and represented.

---

## 1. Singleton Pattern

**Intent:** Ensure a class has only one instance and provide a global access point to it.

**Use Case in Data:** Database connections, configuration managers, logging systems — resources that should be shared and not duplicated.

### Example 1 — Database Connection Manager

```python
import psycopg2
from threading import Lock

class DatabaseConnectionManager:
    """Singleton for managing a single shared database connection."""
    _instance = None
    _lock: Lock = Lock()

    def __new__(cls, dsn: str = None):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._connection = psycopg2.connect(dsn)
                print("[Singleton] New DB connection established.")
        return cls._instance

    @property
    def connection(self):
        return self._connection

    def execute(self, query: str, params=None):
        cursor = self._connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()


# Usage
dsn = "dbname=analytics user=admin password=secret host=localhost"
conn1 = DatabaseConnectionManager(dsn)
conn2 = DatabaseConnectionManager(dsn)

assert conn1 is conn2  # True — same instance
results = conn1.execute("SELECT * FROM sales LIMIT 10;")
```

### Example 2 — Pipeline Configuration Manager

```python
import yaml

class PipelineConfig:
    """Singleton that loads and caches pipeline configuration once."""
    _instance = None

    def __new__(cls, config_path: str = "config.yaml"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            with open(config_path, "r") as f:
                cls._instance._config = yaml.safe_load(f)
            print(f"[Singleton] Config loaded from {config_path}")
        return cls._instance

    def get(self, key: str, default=None):
        return self._config.get(key, default)


# Usage
cfg1 = PipelineConfig("pipeline_config.yaml")
cfg2 = PipelineConfig()  # returns same instance, does NOT reload

source = cfg1.get("data_source")    # e.g. "s3://bucket/raw/"
target = cfg2.get("output_path")    # e.g. "s3://bucket/processed/"
```

### Example 3 — Centralized Logger

```python
import logging

class DataPipelineLogger:
    """Singleton logger to unify logs across all pipeline modules."""
    _instance = None

    def __new__(cls, log_file: str = "pipeline.log"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            logger = logging.getLogger("DataPipeline")
            logger.setLevel(logging.DEBUG)
            fh = logging.FileHandler(log_file)
            fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
            logger.addHandler(fh)
            cls._instance._logger = logger
        return cls._instance

    def info(self, msg): self._logger.info(msg)
    def warning(self, msg): self._logger.warning(msg)
    def error(self, msg): self._logger.error(msg)


# Usage across different modules
log = DataPipelineLogger("etl.log")
log.info("ETL job started")
log.warning("Null values detected in column 'revenue'")
log.error("Failed to connect to data warehouse")
```

---

## 2. Factory Method Pattern

**Intent:** Define an interface for creating an object, but let subclasses decide which class to instantiate.

**Use Case in Data:** Creating different data readers/writers (CSV, Parquet, JSON) without changing the client code.

### Example 1 — Data Source Reader Factory

```python
from abc import ABC, abstractmethod
import pandas as pd

class DataReader(ABC):
    @abstractmethod
    def read(self, path: str) -> pd.DataFrame:
        pass

class CSVReader(DataReader):
    def read(self, path: str) -> pd.DataFrame:
        print(f"[CSVReader] Reading {path}")
        return pd.read_csv(path)

class ParquetReader(DataReader):
    def read(self, path: str) -> pd.DataFrame:
        print(f"[ParquetReader] Reading {path}")
        return pd.read_parquet(path)

class JSONReader(DataReader):
    def read(self, path: str) -> pd.DataFrame:
        print(f"[JSONReader] Reading {path}")
        return pd.read_json(path)

class DataReaderFactory:
    """Factory method to return the correct reader based on file extension."""
    @staticmethod
    def get_reader(file_format: str) -> DataReader:
        readers = {
            "csv": CSVReader,
            "parquet": ParquetReader,
            "json": JSONReader,
        }
        if file_format not in readers:
            raise ValueError(f"Unsupported format: {file_format}")
        return readers[file_format]()


# Usage
reader = DataReaderFactory.get_reader("parquet")
df = reader.read("s3://data-lake/sales/2024/sales.parquet")
```

### Example 2 — ML Model Factory

```python
from abc import ABC, abstractmethod
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression

class BaseModel(ABC):
    @abstractmethod
    def build(self, **kwargs):
        pass

class RandomForestModel(BaseModel):
    def build(self, **kwargs):
        return RandomForestClassifier(**kwargs)

class GradientBoostModel(BaseModel):
    def build(self, **kwargs):
        return GradientBoostingClassifier(**kwargs)

class LogisticModel(BaseModel):
    def build(self, **kwargs):
        return LogisticRegression(**kwargs)

class ModelFactory:
    _registry = {
        "random_forest": RandomForestModel,
        "gradient_boost": GradientBoostModel,
        "logistic": LogisticModel,
    }

    @classmethod
    def create(cls, model_type: str, **kwargs):
        if model_type not in cls._registry:
            raise ValueError(f"Unknown model type: {model_type}")
        return cls._registry[model_type]().build(**kwargs)


# Usage
model = ModelFactory.create("random_forest", n_estimators=200, max_depth=10)
model.fit(X_train, y_train)
```

### Example 3 — Data Validator Factory

```python
from abc import ABC, abstractmethod
import pandas as pd

class DataValidator(ABC):
    @abstractmethod
    def validate(self, df: pd.DataFrame) -> dict:
        pass

class NullValidator(DataValidator):
    def validate(self, df: pd.DataFrame) -> dict:
        nulls = df.isnull().sum()
        return {"null_counts": nulls[nulls > 0].to_dict()}

class DuplicateValidator(DataValidator):
    def validate(self, df: pd.DataFrame) -> dict:
        return {"duplicate_rows": int(df.duplicated().sum())}

class SchemaValidator(DataValidator):
    def __init__(self, expected_schema: dict):
        self.expected_schema = expected_schema

    def validate(self, df: pd.DataFrame) -> dict:
        mismatches = {
            col: str(df[col].dtype)
            for col, dtype in self.expected_schema.items()
            if col in df.columns and str(df[col].dtype) != dtype
        }
        return {"schema_mismatches": mismatches}

class ValidatorFactory:
    @staticmethod
    def get_validator(validator_type: str, **kwargs) -> DataValidator:
        validators = {
            "null": NullValidator,
            "duplicate": DuplicateValidator,
            "schema": SchemaValidator,
        }
        cls = validators.get(validator_type)
        if not cls:
            raise ValueError(f"Unknown validator: {validator_type}")
        return cls(**kwargs) if kwargs else cls()


# Usage
df = pd.read_parquet("orders.parquet")
null_check = ValidatorFactory.get_validator("null").validate(df)
dup_check = ValidatorFactory.get_validator("duplicate").validate(df)
schema_check = ValidatorFactory.get_validator(
    "schema", expected_schema={"order_id": "int64", "amount": "float64"}
).validate(df)
```

---

## 3. Abstract Factory Pattern

**Intent:** Provide an interface for creating families of related or dependent objects without specifying their concrete classes.

**Use Case in Data:** Creating full pipeline families — e.g., a "cloud" pipeline uses S3Reader + RedshiftWriter, while a "local" pipeline uses LocalReader + SQLiteWriter.

### Example 1 — Cloud vs. Local Data Pipeline Factory

```python
from abc import ABC, abstractmethod
import pandas as pd

# Abstract Products
class DataIngester(ABC):
    @abstractmethod
    def ingest(self, source: str) -> pd.DataFrame: pass

class DataWriter(ABC):
    @abstractmethod
    def write(self, df: pd.DataFrame, destination: str): pass

# Concrete Products — Cloud
class S3Ingester(DataIngester):
    def ingest(self, source: str) -> pd.DataFrame:
        print(f"[S3Ingester] Fetching from {source}")
        return pd.read_parquet(source)  # boto3 s3 path

class RedshiftWriter(DataWriter):
    def write(self, df: pd.DataFrame, destination: str):
        print(f"[RedshiftWriter] Writing {len(df)} rows to {destination}")
        # df.to_sql(destination, redshift_engine, if_exists="append")

# Concrete Products — Local
class LocalCSVIngester(DataIngester):
    def ingest(self, source: str) -> pd.DataFrame:
        print(f"[LocalCSVIngester] Reading {source}")
        return pd.read_csv(source)

class SQLiteWriter(DataWriter):
    def write(self, df: pd.DataFrame, destination: str):
        import sqlite3
        conn = sqlite3.connect("local_warehouse.db")
        df.to_sql(destination, conn, if_exists="replace", index=False)
        print(f"[SQLiteWriter] Written to table '{destination}'")

# Abstract Factory
class PipelineFactory(ABC):
    @abstractmethod
    def create_ingester(self) -> DataIngester: pass

    @abstractmethod
    def create_writer(self) -> DataWriter: pass

# Concrete Factories
class CloudPipelineFactory(PipelineFactory):
    def create_ingester(self) -> DataIngester: return S3Ingester()
    def create_writer(self) -> DataWriter: return RedshiftWriter()

class LocalPipelineFactory(PipelineFactory):
    def create_ingester(self) -> DataIngester: return LocalCSVIngester()
    def create_writer(self) -> DataWriter: return SQLiteWriter()

# Client
def run_pipeline(factory: PipelineFactory, source: str, destination: str):
    ingester = factory.create_ingester()
    writer = factory.create_writer()
    df = ingester.ingest(source)
    # transform...
    writer.write(df, destination)


# Usage
env = "cloud"  # or "local"
factory = CloudPipelineFactory() if env == "cloud" else LocalPipelineFactory()
run_pipeline(factory, "s3://raw/sales.parquet", "fact_sales")
```

### Example 2 — Multi-Environment Feature Store Factory

```python
from abc import ABC, abstractmethod

class FeatureReader(ABC):
    @abstractmethod
    def get_features(self, entity_id: str) -> dict: pass

class FeatureWriter(ABC):
    @abstractmethod
    def save_features(self, entity_id: str, features: dict): pass

# Online (low-latency, Redis)
class RedisFeatureReader(FeatureReader):
    def get_features(self, entity_id: str) -> dict:
        print(f"[Redis] Fetching features for {entity_id}")
        return {}  # redis_client.hgetall(entity_id)

class RedisFeatureWriter(FeatureWriter):
    def save_features(self, entity_id: str, features: dict):
        print(f"[Redis] Saving features for {entity_id}: {features}")
        # redis_client.hmset(entity_id, features)

# Offline (batch, BigQuery)
class BigQueryFeatureReader(FeatureReader):
    def get_features(self, entity_id: str) -> dict:
        print(f"[BigQuery] Fetching features for {entity_id}")
        return {}  # bq_client.query(...)

class BigQueryFeatureWriter(FeatureWriter):
    def save_features(self, entity_id: str, features: dict):
        print(f"[BigQuery] Saving features for {entity_id}")

class FeatureStoreFactory(ABC):
    @abstractmethod
    def create_reader(self) -> FeatureReader: pass
    @abstractmethod
    def create_writer(self) -> FeatureWriter: pass

class OnlineFeatureStoreFactory(FeatureStoreFactory):
    def create_reader(self): return RedisFeatureReader()
    def create_writer(self): return RedisFeatureWriter()

class OfflineFeatureStoreFactory(FeatureStoreFactory):
    def create_reader(self): return BigQueryFeatureReader()
    def create_writer(self): return BigQueryFeatureWriter()


# Usage
def compute_and_store(factory: FeatureStoreFactory, entity_id: str, raw_data: dict):
    writer = factory.create_writer()
    features = {k: v * 2 for k, v in raw_data.items()}  # mock transform
    writer.save_features(entity_id, features)

factory = OnlineFeatureStoreFactory()
compute_and_store(factory, "user_123", {"age": 25, "spend": 5000})
```

---

## 4. Builder Pattern

**Intent:** Separate the construction of a complex object from its representation, allowing the same construction process to create different representations.

**Use Case in Data:** Building complex SQL queries, ML experiment configs, or ETL pipeline configurations step-by-step.

### Example 1 — SQL Query Builder

```python
class SQLQueryBuilder:
    """Fluent SQL query builder for analytics queries."""

    def __init__(self):
        self._select = []
        self._from = None
        self._joins = []
        self._where = []
        self._group_by = []
        self._having = []
        self._order_by = []
        self._limit = None

    def select(self, *columns):
        self._select.extend(columns)
        return self

    def from_table(self, table: str):
        self._from = table
        return self

    def join(self, table: str, on: str, join_type: str = "INNER"):
        self._joins.append(f"{join_type} JOIN {table} ON {on}")
        return self

    def where(self, condition: str):
        self._where.append(condition)
        return self

    def group_by(self, *columns):
        self._group_by.extend(columns)
        return self

    def having(self, condition: str):
        self._having.append(condition)
        return self

    def order_by(self, column: str, direction: str = "ASC"):
        self._order_by.append(f"{column} {direction}")
        return self

    def limit(self, n: int):
        self._limit = n
        return self

    def build(self) -> str:
        query = "SELECT " + (", ".join(self._select) or "*")
        query += f"\nFROM {self._from}"
        if self._joins:
            query += "\n" + "\n".join(self._joins)
        if self._where:
            query += "\nWHERE " + " AND ".join(self._where)
        if self._group_by:
            query += "\nGROUP BY " + ", ".join(self._group_by)
        if self._having:
            query += "\nHAVING " + " AND ".join(self._having)
        if self._order_by:
            query += "\nORDER BY " + ", ".join(self._order_by)
        if self._limit:
            query += f"\nLIMIT {self._limit}"
        return query


# Usage
query = (
    SQLQueryBuilder()
    .select("c.customer_id", "c.name", "SUM(o.amount) AS total_revenue")
    .from_table("customers c")
    .join("orders o", "c.customer_id = o.customer_id")
    .where("o.order_date >= '2024-01-01'")
    .where("o.status = 'completed'")
    .group_by("c.customer_id", "c.name")
    .having("SUM(o.amount) > 10000")
    .order_by("total_revenue", "DESC")
    .limit(100)
    .build()
)
print(query)
```

### Example 2 — ML Experiment Config Builder

```python
from dataclasses import dataclass, field
from typing import Any

@dataclass
class ExperimentConfig:
    model_type: str
    dataset: str
    features: list
    target: str
    hyperparams: dict
    preprocessing: dict
    evaluation_metrics: list
    output_path: str
    tags: dict = field(default_factory=dict)

class ExperimentConfigBuilder:
    def __init__(self):
        self._config = {}

    def model(self, model_type: str):
        self._config["model_type"] = model_type
        return self

    def dataset(self, path: str):
        self._config["dataset"] = path
        return self

    def features(self, *cols):
        self._config["features"] = list(cols)
        return self

    def target(self, col: str):
        self._config["target"] = col
        return self

    def hyperparams(self, **kwargs):
        self._config["hyperparams"] = kwargs
        return self

    def preprocessing(self, **kwargs):
        self._config["preprocessing"] = kwargs
        return self

    def evaluate_with(self, *metrics):
        self._config["evaluation_metrics"] = list(metrics)
        return self

    def output(self, path: str):
        self._config["output_path"] = path
        return self

    def tag(self, **kwargs):
        self._config["tags"] = kwargs
        return self

    def build(self) -> ExperimentConfig:
        return ExperimentConfig(**self._config)


# Usage
config = (
    ExperimentConfigBuilder()
    .model("xgboost")
    .dataset("s3://ml-data/churn/train.parquet")
    .features("tenure", "monthly_charges", "contract_type", "num_services")
    .target("churn")
    .hyperparams(n_estimators=300, max_depth=6, learning_rate=0.05)
    .preprocessing(scale=True, encode_categoricals="onehot")
    .evaluate_with("accuracy", "roc_auc", "f1")
    .output("s3://ml-models/churn-v2/")
    .tag(version="v2", team="ds-platform", experiment="baseline")
    .build()
)
print(config)
```

### Example 3 — ETL Pipeline Builder

```python
from typing import Callable

class ETLPipeline:
    def __init__(self, source, transformations, destination, error_handler):
        self.source = source
        self.transformations = transformations
        self.destination = destination
        self.error_handler = error_handler

    def run(self):
        import pandas as pd
        try:
            df = self.source()
            for transform in self.transformations:
                df = transform(df)
            self.destination(df)
            print(f"[ETL] Pipeline complete. {len(df)} rows written.")
        except Exception as e:
            self.error_handler(e)

class ETLPipelineBuilder:
    def __init__(self):
        self._source = None
        self._transforms = []
        self._destination = None
        self._error_handler = lambda e: print(f"[ETL Error] {e}")

    def extract_from(self, source_fn: Callable):
        self._source = source_fn
        return self

    def transform(self, fn: Callable):
        self._transforms.append(fn)
        return self

    def load_to(self, destination_fn: Callable):
        self._destination = destination_fn
        return self

    def on_error(self, handler: Callable):
        self._error_handler = handler
        return self

    def build(self) -> ETLPipeline:
        assert self._source and self._destination, "Source and destination required"
        return ETLPipeline(self._source, self._transforms, self._destination, self._error_handler)


# Usage
import pandas as pd

pipeline = (
    ETLPipelineBuilder()
    .extract_from(lambda: pd.read_parquet("s3://raw/events.parquet"))
    .transform(lambda df: df.dropna(subset=["user_id", "event_type"]))
    .transform(lambda df: df[df["event_date"] >= "2024-01-01"])
    .transform(lambda df: df.assign(revenue=df["quantity"] * df["unit_price"]))
    .load_to(lambda df: df.to_parquet("s3://processed/events_clean.parquet", index=False))
    .on_error(lambda e: print(f"Pipeline failed: {e}"))
    .build()
)
pipeline.run()
```

---

## 5. Prototype Pattern

**Intent:** Create new objects by cloning an existing object (the prototype), avoiding the cost of creating objects from scratch.

**Use Case in Data:** Cloning dataset preprocessing pipelines, experiment configurations, or report templates.

### Example 1 — Cloneable Feature Engineering Pipeline

```python
import copy
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

class FeaturePipelinePrototype:
    """Prototype for a reusable, cloneable feature engineering pipeline."""

    def __init__(self, numeric_cols, categorical_cols):
        self.numeric_cols = numeric_cols
        self.categorical_cols = categorical_cols
        self._pipeline = self._build()

    def _build(self):
        numeric_transformer = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ])
        categorical_transformer = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ])
        return ColumnTransformer([
            ("num", numeric_transformer, self.numeric_cols),
            ("cat", categorical_transformer, self.categorical_cols),
        ])

    def clone(self):
        """Return a deep copy of this pipeline prototype."""
        return copy.deepcopy(self)

    @property
    def pipeline(self):
        return self._pipeline


# Usage
base_pipeline = FeaturePipelinePrototype(
    numeric_cols=["age", "income", "tenure"],
    categorical_cols=["gender", "region"]
)

# Clone for two different models without rebuilding
pipeline_model_a = base_pipeline.clone()
pipeline_model_b = base_pipeline.clone()

# Customize model_b's clone
pipeline_model_b.numeric_cols.append("credit_score")
```

### Example 2 — Report Template Prototype

```python
import copy
from datetime import datetime

class ReportTemplate:
    """Prototype for analytics report templates."""

    def __init__(self, title: str, sections: list, metadata: dict):
        self.title = title
        self.sections = sections  # list of section dicts
        self.metadata = metadata
        self.created_at = datetime.utcnow().isoformat()

    def clone(self):
        return copy.deepcopy(self)

    def render(self) -> str:
        lines = [f"# {self.title}", f"_Generated: {self.created_at}_", ""]
        for sec in self.sections:
            lines.append(f"## {sec['heading']}")
            lines.append(sec.get("content", "_No content_"))
            lines.append("")
        return "\n".join(lines)


# Base template
base_report = ReportTemplate(
    title="Monthly KPI Report",
    sections=[
        {"heading": "Executive Summary", "content": "TBD"},
        {"heading": "Revenue Analysis", "content": "TBD"},
        {"heading": "Customer Metrics", "content": "TBD"},
    ],
    metadata={"author": "Analytics Team", "version": "1.0"}
)

# Clone and customize per region
apac_report = base_report.clone()
apac_report.title = "Monthly KPI Report — APAC"
apac_report.sections[0]["content"] = "APAC revenue grew 12% MoM."

emea_report = base_report.clone()
emea_report.title = "Monthly KPI Report — EMEA"
emea_report.sections[0]["content"] = "EMEA revenue remained stable."

print(apac_report.render())
```

### Example 3 — Experiment Configuration Prototype

```python
import copy

class ExperimentPrototype:
    """Prototype for ML experiments — clone a base config and tweak."""

    def __init__(self, base_config: dict):
        self._config = copy.deepcopy(base_config)

    def clone(self):
        return copy.deepcopy(self)

    def set(self, key: str, value):
        self._config[key] = value
        return self

    @property
    def config(self):
        return self._config


# Base experiment
base_experiment = ExperimentPrototype({
    "model": "xgboost",
    "n_estimators": 100,
    "learning_rate": 0.1,
    "max_depth": 5,
    "dataset": "churn_v1",
    "features": ["tenure", "monthly_charges"],
    "target": "churn",
})

# Run a grid search via cloning — no manual dict creation
variants = []
for lr in [0.01, 0.05, 0.1]:
    for depth in [3, 5, 7]:
        exp = base_experiment.clone()
        exp.set("learning_rate", lr).set("max_depth", depth)
        variants.append(exp.config)

print(f"Generated {len(variants)} experiment variants")
for v in variants[:3]:
    print(v)
```

---

_Document covers: Singleton, Factory Method, Abstract Factory, Builder, Prototype_
_Domain: Data Analytics · Data Science · Data Engineering · Analytics Engineering_

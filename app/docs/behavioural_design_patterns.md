# Behavioural Design Patterns

> A professional guide for Data Analytics, Data Science, Data Engineering & Analytics Engineering in Python

Behavioural design patterns are concerned with algorithms and the assignment of responsibilities between objects. They characterize complex control flow that is difficult to follow at run-time.

---

## 1. Chain of Responsibility

**Intent:** Pass a request along a chain of handlers. Each handler decides to process it or pass it to the next.

**Use Case in Data:** Building modular data validation/quality check pipelines where each handler checks one rule and passes the DataFrame downstream.

### Example 1 — Data Quality Check Chain

```python
from abc import ABC, abstractmethod
import pandas as pd
from typing import Optional

class DataHandler(ABC):
    def __init__(self):
        self._next: Optional["DataHandler"] = None

    def set_next(self, handler: "DataHandler") -> "DataHandler":
        self._next = handler
        return handler

    def handle(self, df: pd.DataFrame) -> pd.DataFrame:
        if self._next:
            return self._next.handle(df)
        return df

    @abstractmethod
    def process(self, df: pd.DataFrame) -> pd.DataFrame: pass

    def handle(self, df: pd.DataFrame) -> pd.DataFrame:
        result = self.process(df)
        if self._next:
            return self._next.handle(result)
        return result

class NullDropHandler(DataHandler):
    def __init__(self, critical_cols: list):
        super().__init__()
        self.critical_cols = critical_cols

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        before = len(df)
        df = df.dropna(subset=self.critical_cols)
        print(f"[NullDrop] Dropped {before - len(df)} rows with nulls in {self.critical_cols}")
        return df

class DuplicateHandler(DataHandler):
    def __init__(self, key_cols: list):
        super().__init__()
        self.key_cols = key_cols

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        before = len(df)
        df = df.drop_duplicates(subset=self.key_cols)
        print(f"[DedupHandler] Removed {before - len(df)} duplicate rows")
        return df

class OutlierHandler(DataHandler):
    def __init__(self, col: str, lower: float, upper: float):
        super().__init__()
        self.col, self.lower, self.upper = col, lower, upper

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        before = len(df)
        df = df[(df[self.col] >= self.lower) & (df[self.col] <= self.upper)]
        print(f"[OutlierHandler] Filtered {before - len(df)} outliers in '{self.col}'")
        return df


# Build the chain
null_handler = NullDropHandler(critical_cols=["order_id", "customer_id"])
dedup_handler = DuplicateHandler(key_cols=["order_id"])
outlier_handler = OutlierHandler(col="amount", lower=0, upper=100_000)

null_handler.set_next(dedup_handler).set_next(outlier_handler)

df = pd.read_parquet("raw_orders.parquet")
clean_df = null_handler.handle(df)
print(f"Final shape: {clean_df.shape}")
```

### Example 2 — ETL Pipeline Stage Chain

```python
from abc import ABC, abstractmethod
import pandas as pd

class PipelineStage(ABC):
    def __init__(self, name: str):
        self.name = name
        self._next = None

    def then(self, stage: "PipelineStage") -> "PipelineStage":
        self._next = stage
        return stage

    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        print(f"[{self.name}] Processing {len(df)} rows...")
        df = self.transform(df)
        if self._next:
            return self._next.execute(df)
        return df

    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame: pass

class NormalizeColumns(PipelineStage):
    def transform(self, df):
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
        return df

class CastDateColumns(PipelineStage):
    def __init__(self, date_cols: list):
        super().__init__("CastDates")
        self.date_cols = date_cols

    def transform(self, df):
        for col in self.date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")
        return df

class AddAuditColumns(PipelineStage):
    def transform(self, df):
        df["_loaded_at"] = pd.Timestamp.utcnow()
        df["_row_hash"] = pd.util.hash_pandas_object(df, index=False)
        return df


# Assemble chain
stage1 = NormalizeColumns("NormalizeCols")
stage2 = CastDateColumns(["order_date", "ship_date"])
stage3 = AddAuditColumns("AddAudit")
stage1.then(stage2).then(stage3)

df = pd.read_csv("raw_orders.csv")
result = stage1.execute(df)
```

---

## 2. Command Pattern

**Intent:** Encapsulate a request as an object, allowing parameterization, queuing, logging, and undoable operations.

**Use Case in Data:** Queuing and executing data transformation commands, supporting undo/redo in data preparation workflows.

### Example 1 — Undoable Data Transformation Commands

```python
from abc import ABC, abstractmethod
import pandas as pd

class TransformCommand(ABC):
    @abstractmethod
    def execute(self, df: pd.DataFrame) -> pd.DataFrame: pass

    @abstractmethod
    def undo(self, df: pd.DataFrame) -> pd.DataFrame: pass

class DropNullsCommand(TransformCommand):
    def __init__(self, cols: list):
        self.cols = cols
        self._dropped_indices = None

    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        mask = df[self.cols].isnull().any(axis=1)
        self._dropped_indices = df[mask].index
        return df.dropna(subset=self.cols).reset_index(drop=True)

    def undo(self, df: pd.DataFrame) -> pd.DataFrame:
        print("[Undo] DropNulls — restoring dropped rows not directly possible. Revert to snapshot.")
        return df  # In practice, use snapshotting

class RenameColumnCommand(TransformCommand):
    def __init__(self, old_name: str, new_name: str):
        self.old_name, self.new_name = old_name, new_name

    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.rename(columns={self.old_name: self.new_name})

    def undo(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.rename(columns={self.new_name: self.old_name})

class DataTransformInvoker:
    """Stores and executes commands with history tracking."""
    def __init__(self, df: pd.DataFrame):
        self._df = df
        self._history: list[TransformCommand] = []
        self._snapshots: list[pd.DataFrame] = []

    def execute(self, command: TransformCommand):
        self._snapshots.append(self._df.copy())
        self._df = command.execute(self._df)
        self._history.append(command)
        print(f"[Invoker] Executed: {command.__class__.__name__} | Shape: {self._df.shape}")

    def undo(self):
        if self._snapshots:
            self._df = self._snapshots.pop()
            cmd = self._history.pop()
            print(f"[Invoker] Undone: {cmd.__class__.__name__}")

    @property
    def result(self) -> pd.DataFrame:
        return self._df


# Usage
df = pd.read_csv("orders.csv")
invoker = DataTransformInvoker(df)
invoker.execute(DropNullsCommand(["order_id", "amount"]))
invoker.execute(RenameColumnCommand("amt", "amount_usd"))
invoker.undo()  # Undo rename
print(invoker.result.head())
```

### Example 2 — Queued SQL Command Executor

```python
from abc import ABC, abstractmethod
from typing import Callable
import time

class SQLCommand(ABC):
    @abstractmethod
    def execute(self, connection) -> any: pass

    @abstractmethod
    def description(self) -> str: pass

class CreateTableCommand(SQLCommand):
    def __init__(self, table: str, ddl: str):
        self.table = table
        self.ddl = ddl

    def execute(self, connection):
        print(f"[CreateTable] Executing: CREATE TABLE {self.table}")
        connection.execute(self.ddl)

    def description(self) -> str:
        return f"CREATE TABLE {self.table}"

class InsertDataCommand(SQLCommand):
    def __init__(self, table: str, df):
        self.table = table
        self.df = df

    def execute(self, connection):
        print(f"[InsertData] Loading {len(self.df)} rows into {self.table}")
        self.df.to_sql(self.table, connection, if_exists="append", index=False)

    def description(self) -> str:
        return f"INSERT {len(self.df)} rows into {self.table}"

class AnalyzeTableCommand(SQLCommand):
    def __init__(self, table: str):
        self.table = table

    def execute(self, connection):
        print(f"[AnalyzeTable] Running ANALYZE on {self.table}")
        connection.execute(f"ANALYZE {self.table}")

    def description(self) -> str:
        return f"ANALYZE {self.table}"

class SQLCommandQueue:
    """Queue-based command invoker with execution log."""
    def __init__(self):
        self._queue: list[SQLCommand] = []
        self._execution_log: list[dict] = []

    def enqueue(self, command: SQLCommand):
        self._queue.append(command)
        print(f"[Queue] Added: {command.description()}")

    def run_all(self, connection):
        print(f"\n[Queue] Executing {len(self._queue)} commands...")
        for cmd in self._queue:
            start = time.time()
            cmd.execute(connection)
            elapsed = time.time() - start
            self._execution_log.append({
                "command": cmd.description(),
                "duration_ms": round(elapsed * 1000, 2),
                "status": "success"
            })
        print(f"[Queue] All commands executed. Log: {self._execution_log}")
        self._queue.clear()


# Usage
import pandas as pd
import sqlite3

conn = sqlite3.connect(":memory:")
queue = SQLCommandQueue()

df_sales = pd.DataFrame({"order_id": range(100), "amount": range(100, 200)})

queue.enqueue(CreateTableCommand("fact_sales", "CREATE TABLE IF NOT EXISTS fact_sales (order_id INT, amount FLOAT)"))
queue.enqueue(InsertDataCommand("fact_sales", df_sales))
queue.enqueue(AnalyzeTableCommand("fact_sales"))
queue.run_all(conn)
```

### Example 3 — Macro Command for Multi-Step Data Pipeline

```python
from abc import ABC, abstractmethod
import pandas as pd

class PipelineCommand(ABC):
    @abstractmethod
    def execute(self) -> pd.DataFrame: pass

    @abstractmethod
    def name(self) -> str: pass

class ExtractCommand(PipelineCommand):
    def __init__(self, path: str):
        self.path = path

    def execute(self) -> pd.DataFrame:
        print(f"[Extract] Reading from {self.path}")
        return pd.read_parquet(self.path)

    def name(self): return "Extract"

class CleanCommand(PipelineCommand):
    def __init__(self, df_ref: list, required_cols: list):
        self.df_ref = df_ref  # mutable reference
        self.required_cols = required_cols

    def execute(self) -> pd.DataFrame:
        df = self.df_ref[0].dropna(subset=self.required_cols)
        print(f"[Clean] {len(df)} rows after null drop")
        return df

    def name(self): return "Clean"

class AggregateCommand(PipelineCommand):
    def __init__(self, df_ref: list, group_col: str, agg_col: str):
        self.df_ref = df_ref
        self.group_col = group_col
        self.agg_col = agg_col

    def execute(self) -> pd.DataFrame:
        df = self.df_ref[0].groupby(self.group_col)[self.agg_col].sum().reset_index()
        print(f"[Aggregate] {len(df)} groups on '{self.group_col}'")
        return df

    def name(self): return "Aggregate"

class MacroPipelineCommand:
    """Macro command — composes multiple commands into a sequential pipeline."""
    def __init__(self):
        self._commands: list[PipelineCommand] = []

    def add(self, command: PipelineCommand):
        self._commands.append(command)
        return self

    def execute(self) -> pd.DataFrame:
        df_ref = [None]
        for cmd in self._commands:
            result = cmd.execute()
            if result is not None:
                df_ref[0] = result
        print(f"[Macro] All {len(self._commands)} commands complete.")
        return df_ref[0]


# Usage
df_holder = [None]
macro = MacroPipelineCommand()
macro.add(ExtractCommand("s3://raw/orders.parquet"))
# In real usage, subsequent commands reference a shared context dict or dataclass
result = macro.execute()
```

---

## 3. Interpreter Pattern

**Intent:** Given a language, define a representation for its grammar and an interpreter that uses the grammar to interpret sentences.

**Use Case in Data:** Building mini DSLs (domain-specific languages) for metric definitions, filter expressions, or custom aggregation rules.

### Example 1 — Metric Expression Interpreter

```python
from abc import ABC, abstractmethod
import pandas as pd

class MetricExpression(ABC):
    @abstractmethod
    def interpret(self, df: pd.DataFrame) -> float: pass

class ColumnSumExpression(MetricExpression):
    def __init__(self, column: str):
        self.column = column

    def interpret(self, df: pd.DataFrame) -> float:
        return df[self.column].sum()

class ColumnMeanExpression(MetricExpression):
    def __init__(self, column: str):
        self.column = column

    def interpret(self, df: pd.DataFrame) -> float:
        return df[self.column].mean()

class AddExpression(MetricExpression):
    def __init__(self, left: MetricExpression, right: MetricExpression):
        self.left, self.right = left, right

    def interpret(self, df: pd.DataFrame) -> float:
        return self.left.interpret(df) + self.right.interpret(df)

class MultiplyExpression(MetricExpression):
    def __init__(self, left: MetricExpression, scalar: float):
        self.left, self.scalar = left, scalar

    def interpret(self, df: pd.DataFrame) -> float:
        return self.left.interpret(df) * self.scalar

class DivideExpression(MetricExpression):
    def __init__(self, numerator: MetricExpression, denominator: MetricExpression):
        self.numerator, self.denominator = numerator, denominator

    def interpret(self, df: pd.DataFrame) -> float:
        denom = self.denominator.interpret(df)
        return self.numerator.interpret(df) / denom if denom != 0 else 0


# Usage: Define "average_order_value = total_revenue / total_orders"
total_revenue = ColumnSumExpression("amount")
total_orders = ColumnSumExpression("order_id")
aov = DivideExpression(total_revenue, total_orders)

df = pd.read_parquet("orders.parquet")
print(f"Average Order Value: ${aov.interpret(df):.2f}")

# Composite: "blended_revenue = online_revenue + (offline_revenue * 1.1)"
online = ColumnSumExpression("online_amount")
offline = MultiplyExpression(ColumnSumExpression("offline_amount"), 1.1)
blended = AddExpression(online, offline)
print(f"Blended Revenue: ${blended.interpret(df):,.2f}")
```

### Example 2 — Filter DSL Interpreter

```python
from abc import ABC, abstractmethod
import pandas as pd

class FilterExpression(ABC):
    @abstractmethod
    def apply(self, df: pd.DataFrame) -> pd.DataFrame: pass

class GreaterThan(FilterExpression):
    def __init__(self, col: str, value):
        self.col, self.value = col, value

    def apply(self, df):
        return df[df[self.col] > self.value]

class LessThan(FilterExpression):
    def __init__(self, col: str, value):
        self.col, self.value = col, value

    def apply(self, df):
        return df[df[self.col] < self.value]

class EqualsFilter(FilterExpression):
    def __init__(self, col: str, value):
        self.col, self.value = col, value

    def apply(self, df):
        return df[df[self.col] == self.value]

class AndFilter(FilterExpression):
    def __init__(self, *filters: FilterExpression):
        self.filters = filters

    def apply(self, df):
        for f in self.filters:
            df = f.apply(df)
        return df

class OrFilter(FilterExpression):
    def __init__(self, *filters: FilterExpression):
        self.filters = filters

    def apply(self, df):
        masks = [f.apply(df).index for f in self.filters]
        combined = masks[0]
        for m in masks[1:]:
            combined = combined.union(m)
        return df.loc[combined]


# Usage
df = pd.read_parquet("orders.parquet")

filter_expr = AndFilter(
    GreaterThan("amount", 500),
    EqualsFilter("status", "completed"),
    LessThan("discount", 0.3)
)
filtered = filter_expr.apply(df)
print(f"Filtered rows: {len(filtered)}")
```

---

## 4. Iterator Pattern

**Intent:** Provide a way to sequentially access elements of a collection without exposing its underlying representation.

**Use Case in Data:** Custom iterators for batch processing large datasets, paginating API results, or chunked file reading.

### Example 1 — Batch Dataset Iterator

```python
import pandas as pd
import math

class BatchIterator:
    """Iterates over a DataFrame in fixed-size batches."""
    def __init__(self, df: pd.DataFrame, batch_size: int):
        self._df = df
        self._batch_size = batch_size
        self._current = 0
        self._total_batches = math.ceil(len(df) / batch_size)

    def __iter__(self):
        return self

    def __next__(self) -> pd.DataFrame:
        if self._current >= len(self._df):
            raise StopIteration
        batch = self._df.iloc[self._current: self._current + self._batch_size]
        self._current += self._batch_size
        return batch

    def __len__(self):
        return self._total_batches


# Usage
df = pd.read_parquet("large_transactions.parquet")
iterator = BatchIterator(df, batch_size=10_000)

for i, batch in enumerate(iterator):
    # Process each batch: score, transform, write
    batch["scored"] = batch["amount"] > 1000
    print(f"Batch {i + 1}/{len(iterator)} | Rows: {len(batch)}")
```

### Example 2 — Paginated API Iterator

```python
from typing import Optional
import requests

class PaginatedAPIIterator:
    """Iterates through all pages of a paginated REST API."""
    def __init__(self, base_url: str, page_size: int = 100, params: dict = None):
        self._base_url = base_url
        self._page_size = page_size
        self._params = params or {}
        self._page = 1
        self._exhausted = False

    def __iter__(self):
        return self

    def __next__(self) -> list:
        if self._exhausted:
            raise StopIteration

        params = {**self._params, "page": self._page, "page_size": self._page_size}
        response = requests.get(self._base_url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        records = data.get("results", [])
        if not records or not data.get("next"):
            self._exhausted = True

        if not records:
            raise StopIteration

        self._page += 1
        return records


# Usage
import pandas as pd

all_records = []
api_iter = PaginatedAPIIterator(
    base_url="https://api.example.com/v1/transactions",
    page_size=500,
    params={"start_date": "2024-01-01", "end_date": "2024-12-31"}
)

for page_records in api_iter:
    all_records.extend(page_records)

df = pd.DataFrame(all_records)
print(f"Total records fetched: {len(df)}")
```

### Example 3 — Chunked File Iterator

```python
import pandas as pd
import os

class ChunkedFileIterator:
    """Iterates over a large CSV or Parquet file in memory-efficient chunks."""
    def __init__(self, file_path: str, chunk_size: int = 50_000):
        self._path = file_path
        self._chunk_size = chunk_size
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".csv":
            self._reader = pd.read_csv(file_path, chunksize=chunk_size)
        elif ext == ".parquet":
            import pyarrow.parquet as pq
            pf = pq.ParquetFile(file_path)
            self._reader = pf.iter_batches(batch_size=chunk_size)
            self._is_parquet = True
        self._is_parquet = ext == ".parquet"

    def __iter__(self):
        return self

    def __next__(self) -> pd.DataFrame:
        chunk = next(self._reader)
        if self._is_parquet:
            return chunk.to_pandas()
        return chunk


# Usage
total_revenue = 0.0
for chunk in ChunkedFileIterator("fact_sales_2024.parquet", chunk_size=100_000):
    total_revenue += chunk["amount"].sum()

print(f"Total Revenue: ${total_revenue:,.2f}")
```

---

## 5. Mediator Pattern

**Intent:** Define an object that encapsulates how a set of objects interact. Promotes loose coupling by keeping objects from referring to each other explicitly.

**Use Case in Data:** Coordinating multiple pipeline components (extractor, transformer, loader, notifier) through a central orchestrator.

### Example 1 — Pipeline Orchestrator as Mediator

```python
from abc import ABC, abstractmethod
import pandas as pd

class PipelineComponent(ABC):
    def __init__(self, mediator=None):
        self._mediator = mediator

    def set_mediator(self, mediator):
        self._mediator = mediator

    @abstractmethod
    def execute(self, context: dict): pass

class DataExtractor(PipelineComponent):
    def execute(self, context: dict):
        print("[Extractor] Extracting data...")
        df = pd.DataFrame({"id": range(100), "amount": range(100, 200)})
        context["raw_df"] = df
        self._mediator.notify(self, "extracted", context)

class DataTransformer(PipelineComponent):
    def execute(self, context: dict):
        print("[Transformer] Transforming data...")
        df = context["raw_df"]
        df["amount_usd"] = df["amount"] * 1.1
        context["transformed_df"] = df
        self._mediator.notify(self, "transformed", context)

class DataLoader(PipelineComponent):
    def execute(self, context: dict):
        print("[Loader] Loading data...")
        df = context["transformed_df"]
        df.to_parquet("/tmp/output.parquet", index=False)
        context["loaded"] = True
        self._mediator.notify(self, "loaded", context)

class AlertNotifier(PipelineComponent):
    def execute(self, context: dict):
        print(f"[Notifier] Pipeline complete. Rows: {len(context.get('transformed_df', []))}")

class PipelineMediator:
    """Coordinates all pipeline components."""
    def __init__(self):
        self.extractor = DataExtractor(self)
        self.transformer = DataTransformer(self)
        self.loader = DataLoader(self)
        self.notifier = AlertNotifier(self)

    def notify(self, sender: PipelineComponent, event: str, context: dict):
        if event == "extracted":
            self.transformer.execute(context)
        elif event == "transformed":
            self.loader.execute(context)
        elif event == "loaded":
            self.notifier.execute(context)

    def run(self):
        context = {}
        self.extractor.execute(context)


# Usage
orchestrator = PipelineMediator()
orchestrator.run()
```

### Example 2 — Data Quality Coordinator Mediator

```python
from abc import ABC, abstractmethod
import pandas as pd

class DQComponent(ABC):
    def __init__(self, mediator=None):
        self._mediator = mediator

    def set_mediator(self, mediator): self._mediator = mediator

class ProfilerComponent(DQComponent):
    def profile(self, df: pd.DataFrame) -> dict:
        report = {
            "row_count": len(df),
            "null_rates": df.isnull().mean().to_dict(),
            "dup_count": int(df.duplicated().sum()),
        }
        print(f"[Profiler] Profile complete: {len(df)} rows")
        self._mediator.on_profile_complete(report, df)
        return report

class AnomalyDetectorComponent(DQComponent):
    def detect(self, df: pd.DataFrame, null_threshold: float = 0.05) -> list:
        issues = []
        for col, rate in df.isnull().mean().items():
            if rate > null_threshold:
                issues.append({"type": "high_nulls", "column": col, "null_rate": rate})
        if df.duplicated().mean() > 0.01:
            issues.append({"type": "duplicates", "dup_rate": df.duplicated().mean()})
        print(f"[AnomalyDetector] Found {len(issues)} issues")
        self._mediator.on_anomalies_found(issues)
        return issues

class ReportWriterComponent(DQComponent):
    def write(self, profile: dict, issues: list, output_path: str):
        import json
        report = {"profile": profile, "issues": issues, "passed": len(issues) == 0}
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2, default=str)
        print(f"[ReportWriter] DQ report saved to {output_path}")

class DQCoordinatorMediator:
    """Mediator coordinating profiler → anomaly detection → report writing."""
    def __init__(self, output_path: str = "dq_report.json"):
        self.profiler = ProfilerComponent(self)
        self.detector = AnomalyDetectorComponent(self)
        self.writer = ReportWriterComponent(self)
        self._profile = None
        self._output_path = output_path

    def on_profile_complete(self, profile: dict, df: pd.DataFrame):
        self._profile = profile
        self.detector.detect(df)

    def on_anomalies_found(self, issues: list):
        self.writer.write(self._profile, issues, self._output_path)

    def run(self, df: pd.DataFrame):
        print("[DQCoordinator] Starting data quality check...")
        self.profiler.profile(df)


# Usage
df = pd.read_parquet("fact_orders.parquet")
dq = DQCoordinatorMediator(output_path="reports/dq_fact_orders.json")
dq.run(df)
```

### Example 3 — Feature Engineering Coordinator Mediator

```python
from abc import ABC, abstractmethod
import pandas as pd

class FeatureComponent(ABC):
    def __init__(self):
        self._mediator = None

    def set_mediator(self, mediator): self._mediator = mediator

class RawDataLoader(FeatureComponent):
    def load(self, path: str) -> pd.DataFrame:
        df = pd.read_parquet(path)
        print(f"[Loader] Loaded {len(df)} rows from {path}")
        self._mediator.on_data_loaded(df)
        return df

class FeatureTransformer(FeatureComponent):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["log_amount"] = df["amount"].apply(lambda x: __import__("math").log1p(max(x, 0)))
        df["is_high_value"] = (df["amount"] > df["amount"].quantile(0.9)).astype(int)
        print(f"[Transformer] Engineered features: log_amount, is_high_value")
        self._mediator.on_features_engineered(df)
        return df

class FeatureStore(FeatureComponent):
    def save(self, df: pd.DataFrame, name: str):
        path = f"feature_store/{name}.parquet"
        df.to_parquet(path, index=False)
        print(f"[FeatureStore] Saved {len(df)} rows to {path}")

class FeatureEngineeringMediator:
    def __init__(self, feature_set_name: str):
        self.loader = RawDataLoader()
        self.transformer = FeatureTransformer()
        self.store = FeatureStore()
        self.feature_set_name = feature_set_name
        for comp in [self.loader, self.transformer, self.store]:
            comp.set_mediator(self)

    def on_data_loaded(self, df: pd.DataFrame):
        self.transformer.transform(df)

    def on_features_engineered(self, df: pd.DataFrame):
        self.store.save(df, self.feature_set_name)

    def run(self, source_path: str):
        self.loader.load(source_path)


# Usage
mediator = FeatureEngineeringMediator("churn_features_v3")
mediator.run("s3://raw/customer_transactions.parquet")
```

---

## 6. Memento Pattern

**Intent:** Without violating encapsulation, capture and externalize an object's internal state so that the object can be restored to that state later.

**Use Case in Data:** Saving checkpoints of DataFrame states during data wrangling, enabling undo/rollback in interactive data exploration.

### Example 1 — DataFrame Wrangling Checkpoint System

```python
import pandas as pd
import copy

class DataFrameMemento:
    """Stores a snapshot of a DataFrame state."""
    def __init__(self, df: pd.DataFrame, label: str):
        self._state = df.copy()
        self._label = label

    @property
    def state(self) -> pd.DataFrame:
        return self._state.copy()

    @property
    def label(self) -> str:
        return self._label

class DataWrangler:
    """Originator — performs transformations and creates mementos."""
    def __init__(self, df: pd.DataFrame):
        self._df = df

    def save_checkpoint(self, label: str) -> DataFrameMemento:
        print(f"[Wrangler] Checkpoint saved: '{label}'")
        return DataFrameMemento(self._df, label)

    def restore(self, memento: DataFrameMemento):
        self._df = memento.state
        print(f"[Wrangler] Restored to checkpoint: '{memento.label}'")

    def drop_nulls(self, cols: list):
        self._df = self._df.dropna(subset=cols)
        return self

    def filter_rows(self, condition: str):
        self._df = self._df.query(condition)
        return self

    def add_column(self, col: str, fn):
        self._df[col] = fn(self._df)
        return self

    @property
    def data(self) -> pd.DataFrame:
        return self._df

class CheckpointCaretaker:
    """Manages multiple named checkpoints."""
    def __init__(self):
        self._checkpoints: dict[str, DataFrameMemento] = {}

    def save(self, label: str, memento: DataFrameMemento):
        self._checkpoints[label] = memento

    def restore(self, label: str) -> DataFrameMemento:
        if label not in self._checkpoints:
            raise KeyError(f"No checkpoint: '{label}'")
        return self._checkpoints[label]

    def list(self):
        return list(self._checkpoints.keys())


# Usage
df = pd.read_csv("raw_data.csv")
wrangler = DataWrangler(df)
caretaker = CheckpointCaretaker()

# Save initial state
caretaker.save("raw", wrangler.save_checkpoint("raw"))

# Transform
wrangler.drop_nulls(["order_id", "amount"])
caretaker.save("after_null_drop", wrangler.save_checkpoint("after_null_drop"))

wrangler.filter_rows("amount > 100")
caretaker.save("after_filter", wrangler.save_checkpoint("after_filter"))

wrangler.add_column("revenue_tier", lambda df: pd.cut(df["amount"], bins=[0, 500, 5000, float("inf")],
                                                        labels=["low", "mid", "high"]))

print(f"Current shape: {wrangler.data.shape}")
print(f"Checkpoints: {caretaker.list()}")

# Rollback
wrangler.restore(caretaker.restore("after_null_drop"))
print(f"After rollback shape: {wrangler.data.shape}")
```

### Example 2 — ML Experiment State Snapshots

```python
import copy
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class ExperimentState:
    """The state captured by a Memento."""
    model_params: dict
    feature_cols: list
    metrics: dict
    iteration: int
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

class ExperimentMemento:
    def __init__(self, state: ExperimentState):
        self._state = copy.deepcopy(state)

    @property
    def state(self) -> ExperimentState:
        return copy.deepcopy(self._state)

class MLExperiment:
    """Originator — holds current experiment configuration and metrics."""
    def __init__(self, name: str):
        self.name = name
        self._state = ExperimentState(
            model_params={"n_estimators": 100, "max_depth": 3, "lr": 0.1},
            feature_cols=["tenure", "monthly_charges"],
            metrics={},
            iteration=0
        )

    def update_params(self, **kwargs):
        self._state.model_params.update(kwargs)
        self._state.iteration += 1

    def add_features(self, *cols):
        self._state.feature_cols.extend(cols)

    def record_metrics(self, **kwargs):
        self._state.metrics.update(kwargs)

    def snapshot(self, label: str) -> tuple:
        print(f"[Experiment] Snapshot at iteration {self._state.iteration}")
        return label, ExperimentMemento(self._state)

    def restore(self, memento: ExperimentMemento):
        self._state = memento.state
        print(f"[Experiment] Restored to iteration {self._state.iteration}")

    @property
    def current_state(self) -> ExperimentState:
        return self._state

class ExperimentHistory:
    """Caretaker — manages named experiment snapshots."""
    def __init__(self):
        self._history: dict[str, ExperimentMemento] = {}

    def save(self, label: str, memento: ExperimentMemento):
        self._history[label] = memento
        print(f"[History] Saved snapshot: '{label}'")

    def load(self, label: str) -> ExperimentMemento:
        return self._history[label]

    def list_snapshots(self) -> list:
        return list(self._history.keys())


# Usage
exp = MLExperiment("churn_prediction")
history = ExperimentHistory()

# Baseline
label, snap = exp.snapshot("baseline")
history.save(label, snap)

# Try deeper trees
exp.update_params(max_depth=8, n_estimators=300)
exp.add_features("contract_type", "num_products")
exp.record_metrics(roc_auc=0.81, f1=0.72)
label, snap = exp.snapshot("deep_trees")
history.save(label, snap)

# Try high learning rate — worse results
exp.update_params(lr=0.5)
exp.record_metrics(roc_auc=0.74, f1=0.65)

# Roll back to best snapshot
print(f"\nCurrent AUC: {exp.current_state.metrics.get('roc_auc')}")
exp.restore(history.load("deep_trees"))
print(f"Restored AUC: {exp.current_state.metrics.get('roc_auc')}")
print(f"Available snapshots: {history.list_snapshots()}")
```

### Example 3 — Pipeline Configuration Rollback System

```python
import copy
import json
from datetime import datetime

class PipelineConfigMemento:
    """Stores a version of the pipeline configuration."""
    def __init__(self, config: dict, version: str, author: str):
        self._config = copy.deepcopy(config)
        self.version = version
        self.author = author
        self.created_at = datetime.utcnow().isoformat()

    @property
    def config(self) -> dict:
        return copy.deepcopy(self._config)

    def summary(self) -> str:
        return f"v{self.version} by {self.author} at {self.created_at}"

class PipelineConfigManager:
    """Originator — manages the active pipeline configuration."""
    def __init__(self, initial_config: dict):
        self._config = copy.deepcopy(initial_config)

    def update(self, key: str, value):
        self._config[key] = value
        print(f"[Config] Updated '{key}' = {value}")

    def save_version(self, version: str, author: str) -> PipelineConfigMemento:
        memento = PipelineConfigMemento(self._config, version, author)
        print(f"[Config] Saved version {version}")
        return memento

    def rollback(self, memento: PipelineConfigMemento):
        self._config = memento.config
        print(f"[Config] Rolled back to {memento.summary()}")

    def export(self) -> str:
        return json.dumps(self._config, indent=2)

class ConfigVersionControl:
    """Caretaker — stores and manages config history like a VCS."""
    def __init__(self):
        self._versions: list[PipelineConfigMemento] = []

    def commit(self, memento: PipelineConfigMemento):
        self._versions.append(memento)

    def latest(self) -> PipelineConfigMemento:
        return self._versions[-1]

    def get_version(self, version: str) -> PipelineConfigMemento:
        for m in self._versions:
            if m.version == version:
                return m
        raise KeyError(f"Version {version} not found")

    def log(self):
        print("\n[Version Log]")
        for m in self._versions:
            print(f"  → {m.summary()}")


# Usage
initial = {
    "source": "s3://raw/orders.parquet",
    "batch_size": 10000,
    "target_table": "fact_orders",
    "schedule": "0 2 * * *"
}

manager = PipelineConfigManager(initial)
vcs = ConfigVersionControl()

vcs.commit(manager.save_version("1.0.0", "alice"))

manager.update("batch_size", 50000)
manager.update("schedule", "0 1 * * *")
vcs.commit(manager.save_version("1.1.0", "bob"))

manager.update("source", "s3://raw/orders_v2.parquet")
vcs.commit(manager.save_version("1.2.0", "alice"))

# Oh no — v1.2.0 broke production
vcs.log()
manager.rollback(vcs.get_version("1.1.0"))
print(f"\nActive config: {manager.export()}")
```

---

## 7. Observer Pattern

**Intent:** Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified automatically.

**Use Case in Data:** Pipeline event broadcasting — notify dashboards, loggers, alerting systems when pipeline stages complete.

### Example 1 — Pipeline Event System

```python
from abc import ABC, abstractmethod
from typing import Any

class PipelineObserver(ABC):
    @abstractmethod
    def update(self, event: str, data: Any): pass

class PipelineSubject:
    def __init__(self):
        self._observers: list[PipelineObserver] = []

    def subscribe(self, observer: PipelineObserver):
        self._observers.append(observer)

    def unsubscribe(self, observer: PipelineObserver):
        self._observers.remove(observer)

    def notify(self, event: str, data: Any = None):
        for obs in self._observers:
            obs.update(event, data)

# Concrete Observers
class PipelineLogger(PipelineObserver):
    def update(self, event: str, data: Any):
        print(f"[Logger] Event: {event} | Data: {data}")

class SlackAlerter(PipelineObserver):
    def __init__(self, webhook_url: str, alert_on: list):
        self.webhook_url = webhook_url
        self.alert_on = alert_on

    def update(self, event: str, data: Any):
        if event in self.alert_on:
            print(f"[Slack] ALERT → {event}: {data}")
            # requests.post(self.webhook_url, json={"text": f"{event}: {data}"})

class DataQualityMonitor(PipelineObserver):
    def update(self, event: str, data: Any):
        if event == "pipeline_complete":
            row_count = data.get("rows", 0)
            if row_count < 1000:
                print(f"[QualityMonitor] ⚠ Low row count alert: {row_count} rows")
            else:
                print(f"[QualityMonitor] ✓ Row count OK: {row_count}")

class MetricsDashboard(PipelineObserver):
    def update(self, event: str, data: Any):
        if event in ("pipeline_start", "pipeline_complete"):
            print(f"[Dashboard] Updating metrics for: {event}")

# Data Pipeline using Subject
class DataPipeline(PipelineSubject):
    def run(self, source: str):
        import pandas as pd

        self.notify("pipeline_start", {"source": source})
        df = pd.read_parquet(source)  # or simulated
        df = df.dropna()
        self.notify("transform_complete", {"rows": len(df)})
        df.to_parquet("/tmp/output.parquet", index=False)
        self.notify("pipeline_complete", {"rows": len(df), "output": "/tmp/output.parquet"})
        return df


# Usage
pipeline = DataPipeline()
pipeline.subscribe(PipelineLogger())
pipeline.subscribe(SlackAlerter("https://hooks.slack.com/...", alert_on=["pipeline_complete"]))
pipeline.subscribe(DataQualityMonitor())
pipeline.subscribe(MetricsDashboard())

pipeline.run("s3://datalake/orders.parquet")
```

### Example 2 — Model Drift Observer

```python
from abc import ABC, abstractmethod
import numpy as np

class DriftObserver(ABC):
    @abstractmethod
    def on_drift_detected(self, metric: str, value: float, threshold: float): pass

class DriftEmailAlert(DriftObserver):
    def on_drift_detected(self, metric, value, threshold):
        print(f"[Email Alert] Drift detected! {metric}={value:.4f} exceeds threshold {threshold}")

class DriftMLflowLogger(DriftObserver):
    def on_drift_detected(self, metric, value, threshold):
        print(f"[MLflow] Logging drift event: {metric}={value:.4f}")
        # mlflow.log_metric(f"drift_{metric}", value)

class ModelDriftMonitor:
    """Subject that tracks model prediction drift."""
    def __init__(self, thresholds: dict):
        self._thresholds = thresholds
        self._observers: list[DriftObserver] = []

    def subscribe(self, obs: DriftObserver):
        self._observers.append(obs)

    def check(self, metric: str, value: float):
        threshold = self._thresholds.get(metric, float("inf"))
        if value > threshold:
            for obs in self._observers:
                obs.on_drift_detected(metric, value, threshold)


# Usage
monitor = ModelDriftMonitor(thresholds={"psi": 0.2, "js_divergence": 0.1})
monitor.subscribe(DriftEmailAlert())
monitor.subscribe(DriftMLflowLogger())

# Simulate monitoring loop
metrics = {"psi": 0.35, "js_divergence": 0.08}
for metric, value in metrics.items():
    monitor.check(metric, value)
```

---

## 8. State Pattern

**Intent:** Allow an object to alter its behaviour when its internal state changes. The object will appear to change its class.

**Use Case in Data:** Modelling ETL job lifecycle states (Idle → Running → Completed / Failed), or data quality gate states.

### Example 1 — ETL Job State Machine

```python
from abc import ABC, abstractmethod
from datetime import datetime

class JobState(ABC):
    @abstractmethod
    def start(self, job): pass

    @abstractmethod
    def complete(self, job): pass

    @abstractmethod
    def fail(self, job, error: str): pass

    @abstractmethod
    def retry(self, job): pass

class IdleState(JobState):
    def start(self, job):
        print("[Idle → Running] Job started.")
        job.state = RunningState()
        job.started_at = datetime.utcnow()

    def complete(self, job): print("[Idle] Cannot complete — job not running.")
    def fail(self, job, error): print("[Idle] Cannot fail — job not running.")
    def retry(self, job): print("[Idle] Nothing to retry.")

class RunningState(JobState):
    def start(self, job): print("[Running] Job already running.")

    def complete(self, job):
        elapsed = (datetime.utcnow() - job.started_at).total_seconds()
        print(f"[Running → Completed] Job finished in {elapsed:.2f}s.")
        job.state = CompletedState()

    def fail(self, job, error: str):
        print(f"[Running → Failed] Error: {error}")
        job.state = FailedState(error)

    def retry(self, job): print("[Running] Already running.")

class CompletedState(JobState):
    def start(self, job): print("[Completed] Starting a new run...")
    def complete(self, job): print("[Completed] Already completed.")
    def fail(self, job, error): print("[Completed] Cannot fail — already done.")
    def retry(self, job): print("[Completed] No need to retry.")

class FailedState(JobState):
    def __init__(self, error: str):
        self.error = error

    def start(self, job): print(f"[Failed] Cannot start — previous error: {self.error}")

    def complete(self, job): print("[Failed] Cannot complete — job failed.")

    def fail(self, job, error): print(f"[Failed] Already failed: {self.error}")

    def retry(self, job):
        print(f"[Failed → Running] Retrying after error: {self.error}")
        job.state = RunningState()
        job.started_at = datetime.utcnow()

class ETLJob:
    def __init__(self, name: str):
        self.name = name
        self.state: JobState = IdleState()
        self.started_at = None

    def start(self): self.state.start(self)
    def complete(self): self.state.complete(self)
    def fail(self, error: str): self.state.fail(self, error)
    def retry(self): self.state.retry(self)


# Usage
job = ETLJob("daily_sales_etl")
job.start()                         # Idle → Running
job.fail("Connection timeout")      # Running → Failed
job.retry()                         # Failed → Running
job.complete()                      # Running → Completed
job.retry()                         # No-op
```

### Example 2 — Data Quality Gate State

```python
from abc import ABC, abstractmethod
import pandas as pd

class QualityGateState(ABC):
    @abstractmethod
    def evaluate(self, gate, df: pd.DataFrame): pass

class PendingState(QualityGateState):
    def evaluate(self, gate, df: pd.DataFrame):
        print("[Pending → Evaluating] Running quality checks...")
        gate.state = EvaluatingState()
        gate.state.evaluate(gate, df)

class EvaluatingState(QualityGateState):
    def evaluate(self, gate, df: pd.DataFrame):
        null_rate = df.isnull().mean().max()
        dup_rate = df.duplicated().mean()
        if null_rate > gate.null_threshold or dup_rate > gate.dup_threshold:
            issues = []
            if null_rate > gate.null_threshold:
                issues.append(f"null_rate={null_rate:.2%}")
            if dup_rate > gate.dup_threshold:
                issues.append(f"dup_rate={dup_rate:.2%}")
            print(f"[Evaluating → Rejected] Issues: {', '.join(issues)}")
            gate.state = RejectedState(issues)
        else:
            print(f"[Evaluating → Approved] Null rate: {null_rate:.2%}, Dup rate: {dup_rate:.2%}")
            gate.state = ApprovedState()

class ApprovedState(QualityGateState):
    def evaluate(self, gate, df):
        print("[Approved] Data already approved — proceeding to load.")

class RejectedState(QualityGateState):
    def __init__(self, issues: list):
        self.issues = issues

    def evaluate(self, gate, df):
        print(f"[Rejected] Data rejected due to: {self.issues}")
        print("[Rejected] Manual review required before re-evaluation.")

class DataQualityGate:
    def __init__(self, null_threshold: float = 0.05, dup_threshold: float = 0.01):
        self.null_threshold = null_threshold
        self.dup_threshold = dup_threshold
        self.state: QualityGateState = PendingState()

    def evaluate(self, df: pd.DataFrame):
        self.state.evaluate(self, df)

    @property
    def is_approved(self) -> bool:
        return isinstance(self.state, ApprovedState)


# Usage
df_clean = pd.DataFrame({"id": range(1000), "amount": range(1000, 2000)})
df_dirty = pd.DataFrame({"id": [None] * 100 + list(range(900)), "amount": range(1000)})

gate_clean = DataQualityGate(null_threshold=0.05, dup_threshold=0.01)
gate_clean.evaluate(df_clean)
print(f"Approved: {gate_clean.is_approved}")

gate_dirty = DataQualityGate(null_threshold=0.05, dup_threshold=0.01)
gate_dirty.evaluate(df_dirty)
print(f"Approved: {gate_dirty.is_approved}")
```

---

_Document covers: Chain of Responsibility, Command, Interpreter, Iterator, Mediator, Memento, Observer, State_
_Domain: Data Analytics · Data Science · Data Engineering · Analytics Engineering_

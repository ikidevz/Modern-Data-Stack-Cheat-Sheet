import streamlit as st

st.set_page_config(
    page_title="Data & Statistics Cheat Sheet",
    page_icon="📊",
    layout="wide",
)

st.markdown("""
<style>
    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 99px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        margin-bottom: 0.4rem;
        margin-right: 4px;
    }
    .analyst       { background: #dbeafe; color: #1e40af; }
    .analytics_eng { background: #dcfce7; color: #166534; }
    .data_eng      { background: #fef9c3; color: #854d0e; }
    .data_sci      { background: #f3e8ff; color: #6b21a8; }
    .foundational  { background: #f1f5f9; color: #475569; }
    .intermediate  { background: #fff3cd; color: #92400e; }
    .advanced      { background: #fee2e2; color: #991b1b; }
    .expert        { background: #1e1b4b; color: #c7d2fe; }
    .section-label {
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: white;
        margin-top: 0.75rem;
        margin-bottom: 0.2rem;
    }
    .def-box {
        background: transparent;
        border-left: 3px solid #3b82f6;
        padding: 8px 12px;
        border-radius: 0 4px 4px 0;
        font-size: 0.87rem;
        margin: 1rem 0;
    }
    .formula-box {
        background: transparent;
        color: #a9d0f5;
        padding: 10px 14px;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
        font-size: 0.83rem;
        white-space: pre-wrap;
        margin: 1rem 0;
    }
    .example-box {
        background: transparent;
        border-left: 3px solid #22c55e;
        padding: 8px 12px;
        border-radius: 0 4px 4px 0;
        font-size: 0.86rem;
        margin: 1rem 0;
    }
    .warn-box {
        background: transparent;
        border-left: 3px solid #f97316;
        padding: 8px 12px;
        border-radius: 0 4px 4px 0;
        font-size: 0.86rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 📊 Data & Statistics Cheat Sheet")
st.markdown("#### A structured reference by role and difficulty level")
st.markdown("---")


def render_topic(t):
    roles_html = "".join(
        f'<span class="badge {ROLE_BADGE.get(r, "analyst")}">{r}</span>'
        for r in t.get("roles", [])
    )
    diff_cls = t.get("difficulty", "foundational").lower()
    diff_html = f'<span class="badge {diff_cls}">{t.get("difficulty", "")}</span>'
    st.markdown(roles_html + "&nbsp;" + diff_html, unsafe_allow_html=True)

    if t.get("definition"):
        st.markdown('<p class="section-label">📌 Definition</p>',
                    unsafe_allow_html=True)
        st.markdown(
            f'<div class="def-box">{t["definition"]}</div>', unsafe_allow_html=True)

    if t.get("formula"):
        st.markdown('<p class="section-label">🔢 Formula</p>',
                    unsafe_allow_html=True)
        st.markdown(
            f'<div class="formula-box">{t["formula"]}</div>', unsafe_allow_html=True)

    if t.get("description"):
        st.markdown('<p class="section-label">📖 How It Works</p>',
                    unsafe_allow_html=True)
        st.markdown(t["description"])

    if t.get("example"):
        st.markdown('<p class="section-label">💡 Example</p>',
                    unsafe_allow_html=True)
        st.markdown(
            f'<div class="example-box">{t["example"]}</div>', unsafe_allow_html=True)

    if t.get("use_cases"):
        st.markdown('<p class="section-label">🧰 Use Cases</p>',
                    unsafe_allow_html=True)
        for uc in t["use_cases"]:
            st.markdown(f"- {uc}")

    if t.get("watch_out"):
        st.markdown('<p class="section-label">⚠️ Watch Out</p>',
                    unsafe_allow_html=True)
        st.markdown(
            f'<div class="warn-box">{t["watch_out"]}</div>', unsafe_allow_html=True)

    if t.get("python_code"):
        st.markdown('<p class="section-label">🐍 Python Code</p>',
                    unsafe_allow_html=True)
        st.code(t["python_code"], language="python")


ROLE_BADGE = {
    "Data Analyst":       "analyst",
    "Analytics Engineer": "analytics_eng",
    "Data Engineer":      "data_eng",
    "Data Scientist":     "data_sci",
}

ALL_TOPICS = [

    # ── FOUNDATIONAL ─────────────────────────────────────────────────────────

    {
        "title": "1. Percentages & Proportions",
        "roles": ["Data Analyst", "Analytics Engineer"],
        "difficulty": "Foundational",
        "definition": "A proportion expresses a part relative to a whole, either as a decimal (0–1) or a percentage (0–100%).",
        "formula": "Percentage  = (Part / Whole) × 100\nProportion  = Part / Whole",
        "description": "Proportions and percentages are the most fundamental building blocks of data analysis. Every rate, share, or conversion figure is fundamentally a proportion.",
        "example": "500 purchases out of 10,000 visitors → 500 / 10,000 = 0.05 → <strong>5% conversion rate</strong>",
        "use_cases": ["Conversion rate tracking", "Market share analysis", "Funnel stage drop-off", "Survey response breakdowns"],
        "watch_out": "Always confirm what the denominator is. '50% increase' means nothing without knowing the base.",
        "python_code": """\
import pandas as pd

part, whole = 500, 10_000
proportion = part / whole
percentage  = proportion * 100
print(f"Proportion: {proportion:.4f}  |  Percentage: {percentage:.2f}%")

df = pd.DataFrame({
    "stage": ["visited", "signed_up", "purchased"],
    "users":  [10_000, 1_500, 500],
})
df["proportion"] = df["users"] / df["users"].iloc[0]
df["pct"]        = df["proportion"] * 100
print(df)

statuses = pd.Series(["active","active","churned","active","churned","trial"])
print(statuses.value_counts(normalize=True) * 100)
""",
    },

    {
        "title": "2. Rates of Change",
        "roles": ["Data Analyst", "Analytics Engineer"],
        "difficulty": "Foundational",
        "definition": "The percentage increase or decrease between two values over time.",
        "formula": "Rate of Change = ((New − Old) / Old) × 100",
        "description": "Rates of change let you express growth or decline in a normalized, comparable way regardless of the original scale.",
        "example": "Revenue: $80K → $100K → (100K−80K)/80K × 100 = <strong>+25%</strong><br>Signups: 1,000 → 850 → <strong>−15%</strong>",
        "use_cases": ["Monthly/quarterly KPI reporting", "User growth tracking", "Revenue trend analysis", "Price change comparisons"],
        "watch_out": "A large % change on a tiny base is misleading. 100% growth from 2 to 4 users ≠ 100% growth from 10,000 to 20,000.",
        "python_code": """\
import pandas as pd
import numpy as np

old, new = 80_000, 100_000
roc = (new - old) / old * 100
print(f"Rate of change: {roc:.2f}%")

revenue = pd.Series([80_000, 85_000, 95_000, 100_000],
                    index=pd.date_range("2024-01", periods=4, freq="ME"))
print(revenue.pct_change() * 100)

arr = np.array([1_000, 1_200, 1_050, 1_400])
changes = np.diff(arr) / arr[:-1] * 100
print(changes.round(2))
""",
    },

    {
        "title": "3. Year-over-Year (YoY) Comparisons",
        "roles": ["Data Analyst", "Analytics Engineer"],
        "difficulty": "Foundational",
        "definition": "Comparing a metric for the same period across consecutive years to measure true growth while eliminating seasonal noise.",
        "formula": "YoY Growth = ((This Year − Last Year) / Last Year) × 100",
        "description": "Seasonal businesses have naturally high and low periods. Comparing Dec to Nov looks like a drop even in a great year. YoY fixes this by comparing equivalent periods.",
        "example": "Dec 2023 revenue = $120K, Dec 2024 = $150K → YoY = <strong>+25%</strong>. Always compare Dec vs Dec, not Dec vs Nov.",
        "use_cases": ["Retail and e-commerce performance", "Subscription revenue tracking", "Seasonal demand analysis", "Executive dashboards"],
        "watch_out": "One-off events (pandemic years, product launches) distort YoY. Always annotate anomalies on your charts.",
        "python_code": """\
import pandas as pd

dates   = pd.date_range("2023-01", periods=24, freq="ME")
revenue = pd.Series([120,130,125,140,150,160,170,155,145,135,140,150,
                     145,155,150,165,175,185,200,180,170,160,165,175],
                    index=dates, name="revenue_k")

df = revenue.reset_index().rename(columns={"index": "date"})
df["year"]  = df["date"].dt.year
df["month"] = df["date"].dt.month

pivot = df.pivot(index="month", columns="year", values="revenue_k")
pivot["yoy_pct"] = (pivot[2024] - pivot[2023]) / pivot[2023] * 100
print(pivot.round(2))
""",
    },

    {
        "title": "4. Mean, Median, Mode",
        "roles": ["Data Analyst", "Analytics Engineer", "Data Scientist"],
        "difficulty": "Foundational",
        "definition": "Three measures of central tendency describing where the 'center' of a dataset lies.",
        "formula": "Mean   = Σx / n\nMedian = middle value when sorted\nMode   = most frequently occurring value",
        "description": "| Measure | Best For | Weakness |\n|---------|----------|----------|\n| Mean | Symmetric distributions | Pulled by outliers |\n| Median | Skewed data, income, prices | Ignores extremes |\n| Mode | Categorical data | May not be unique |",
        "example": "Salaries: [30K, 35K, 40K, 42K, 500K]<br>Mean = 129.4K (misleading), Median = 40K (representative)",
        "use_cases": ["Summarizing user ages, incomes, scores", "Comparing product ratings", "Reporting central performance metrics"],
        "watch_out": "Never report just the mean for skewed data. Always check if outliers are pulling it away from reality.",
        "python_code": """\
import numpy as np
import pandas as pd
from scipy import stats

salaries = np.array([30_000, 35_000, 40_000, 42_000, 500_000])
print(f"Mean   : {np.mean(salaries):,.0f}")
print(f"Median : {np.median(salaries):,.0f}")
print(f"Mode   : {stats.mode(salaries, keepdims=True).mode[0]:,.0f}")

s = pd.Series(salaries)
print(s.describe())

trimmed = stats.trim_mean(salaries, proportiontocut=0.1)
print(f"Trimmed mean: {trimmed:,.0f}")
""",
    },

    {
        "title": "5. Range, Variance & Std. Deviation",
        "roles": ["Data Analyst", "Data Scientist"],
        "difficulty": "Foundational",
        "definition": "Measures of spread that describe how dispersed or consistent the values in a dataset are.",
        "formula": "Range    = Max − Min\nVariance = Σ(x − μ)² / n\nStd Dev  = √Variance\nIQR      = Q3 − Q1",
        "description": "Spread tells you how reliable your average is. A mean of 50 with SD=2 means values cluster tightly. The same mean with SD=30 means values scatter widely.",
        "example": "Scores [48,49,50,51,52] → SD ≈ 1.4 (consistent)<br>Scores [10,30,50,70,90] → SD ≈ 28.3 (spread out)",
        "use_cases": ["Quality control (manufacturing)", "Risk assessment in finance", "Model performance evaluation", "A/B test variance analysis"],
        "watch_out": "Variance is in squared units — harder to interpret. Always prefer std. deviation when communicating to stakeholders.",
        "python_code": """\
import numpy as np
import pandas as pd
from scipy import stats

scores = np.array([48, 49, 50, 51, 52])
spread = np.array([10, 30, 50, 70, 90])

for arr, label in [(scores, "tight"), (spread, "wide")]:
    print(f"--- {label} ---")
    print(f"  Range    : {arr.max() - arr.min()}")
    print(f"  Variance : {np.var(arr, ddof=1):.2f}")
    print(f"  Std Dev  : {np.std(arr, ddof=1):.2f}")
    print(f"  IQR      : {stats.iqr(arr):.2f}")
""",
    },

    {
        "title": "6. Basic Probability",
        "roles": ["Data Analyst", "Data Scientist"],
        "difficulty": "Foundational",
        "definition": "The likelihood of a specific event occurring, expressed between 0 (impossible) and 1 (certain).",
        "formula": "P(event)  = Favorable outcomes / Total outcomes\nP(not A)  = 1 − P(A)\nP(A or B) = P(A) + P(B) − P(A and B)\nP(A and B)= P(A) × P(B)  [if independent]",
        "description": "Probability is the foundation of all predictive modeling and decision-making under uncertainty. Every classifier, risk model, and simulation relies on it.",
        "example": "20 out of 100 users churned → P(churn) = 0.2 → P(no churn) = <strong>0.8</strong>",
        "use_cases": ["Churn prediction models", "Lead scoring", "Fraud detection thresholds", "Insurance risk models"],
        "watch_out": "Don't confuse probability with frequency. P=0.2 means a 20% chance — not that exactly 1 in 5 events will always occur.",
        "python_code": """\
import numpy as np
from scipy import stats

churned = np.array([0]*80 + [1]*20)
p_churn    = churned.mean()
p_no_churn = 1 - p_churn
print(f"P(churn) = {p_churn:.2f}  |  P(no churn) = {p_no_churn:.2f}")

n, p, k = 10, 0.2, 3
binom = stats.binom(n, p)
print(f"P(exactly 3 churn in 10) = {binom.pmf(k):.4f}")
print(f"P(at most 3 churn in 10) = {binom.cdf(k):.4f}")

rng = np.random.default_rng(42)
simulated = rng.binomial(1, 0.2, size=100_000)
print(f"Simulated P(churn) ≈ {simulated.mean():.4f}")
""",
    },

    {
        "title": "7. Frequency Distributions & Histograms",
        "roles": ["Data Analyst", "Data Scientist"],
        "difficulty": "Foundational",
        "definition": "A frequency distribution shows how often each value (or range) appears. A histogram is its visual form.",
        "formula": "Relative Frequency = Count in bin / Total count\nSkewness = (1/n) × Σ((x−μ)/σ)³",
        "description": "Histograms reveal the shape of your data:\n- **Normal**: symmetric bell\n- **Right-skewed**: long right tail (income)\n- **Left-skewed**: long left tail (retirement age)\n- **Bimodal**: two peaks → two subpopulations",
        "example": "User session lengths: most users at 2–5 min, power users 60+ min → right-skewed.",
        "use_cases": ["Exploratory data analysis (EDA)", "Detecting outliers", "Choosing the right statistical test", "Feature distribution checks before modeling"],
        "watch_out": "Bin size matters! Too few bins hides structure; too many creates noise. Try multiple bin widths.",
        "python_code": """\
import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(42)
sessions = np.concatenate([
    rng.exponential(scale=4, size=900),
    rng.uniform(30, 90, size=100),
])
s = pd.Series(sessions)
binned = pd.cut(s, bins=10)
print(binned.value_counts().sort_index())

print(f"Skewness : {stats.skew(sessions):.3f}")
print(f"Kurtosis : {stats.kurtosis(sessions):.3f}")
""",
    },

    {
        "title": "8. Data Types",
        "roles": ["Data Analyst", "Analytics Engineer", "Data Engineer"],
        "difficulty": "Foundational",
        "definition": "A classification for the kind of values a variable holds, determining valid operations and chart types.",
        "formula": "N/A — conceptual framework",
        "description": "| Type | Subtype | Examples | Valid Ops |\n|------|---------|----------|-----------|\n| Categorical | Nominal | Country, color | Count, mode |\n| Categorical | Ordinal | Rating 1–5 | Count, rank |\n| Numerical | Discrete | # orders, clicks | All arithmetic |\n| Numerical | Continuous | Revenue, time | All arithmetic |",
        "example": "Customer plan (Free/Pro/Enterprise) = nominal. Satisfaction (1–5) = ordinal. Revenue ($) = continuous.",
        "use_cases": ["Choosing the right chart type", "Selecting appropriate statistical tests", "Encoding variables for ML models"],
        "watch_out": "Numeric-looking codes (zip codes, user IDs) are categorical. Averaging zip codes produces meaningless results.",
        "python_code": """\
import pandas as pd

df = pd.DataFrame({
    "user_id":      [101, 102, 103, 104],
    "plan":         ["Free","Pro","Enterprise","Free"],
    "satisfaction": pd.Categorical([3,5,4,2], categories=[1,2,3,4,5], ordered=True),
    "orders":       [2, 15, 8, 1],
    "revenue":      [0.0, 299.99, 99.99, 0.0],
})
df["plan"]    = df["plan"].astype("category")
df["user_id"] = df["user_id"].astype(str)
print(df.dtypes)
print(df.select_dtypes(include="number").describe())
print(df["plan"].value_counts())
""",
    },

    {
        "title": "9. Pareto Analysis (80/20 Rule)",
        "roles": ["Data Analyst"],
        "difficulty": "Foundational",
        "definition": "Roughly 80% of effects come from 20% of causes — used to prioritize high-impact actions.",
        "formula": "Cumulative % = Σ(sorted values) / Total × 100\nFind where cumulative crosses ~80%",
        "description": "Sort, cumulate, and find the cutoff. Appears across business: customers, bugs, revenue drivers, support tickets.",
        "example": "20% of customers generate 80% of revenue. Identify those customers and prioritize their retention.",
        "use_cases": ["Customer value segmentation", "Bug prioritization", "Support ticket root cause analysis", "Supply chain optimization"],
        "watch_out": "The 80/20 split is a heuristic — in some contexts it's 90/10 or 70/30. It's a prioritization principle, not a universal law.",
        "python_code": """\
import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
df = pd.DataFrame({
    "customer": [f"C{i:03d}" for i in range(1, 51)],
    "revenue":  rng.exponential(scale=5_000, size=50).round(2),
})
df = df.sort_values("revenue", ascending=False).reset_index(drop=True)
df["cum_revenue"] = df["revenue"].cumsum()
df["cum_pct"]     = df["cum_revenue"] / df["revenue"].sum() * 100
df["cust_pct"]    = (df.index + 1) / len(df) * 100

cutoff = df[df["cum_pct"] >= 80].iloc[0]
print(f"Top {cutoff['cust_pct']:.1f}% of customers → {cutoff['cum_pct']:.1f}% of revenue")
""",
    },

    {
        "title": "10. SQL Window Functions for Analytics",
        "roles": ["Data Analyst", "Analytics Engineer"],
        "difficulty": "Foundational",
        "definition": "Window functions perform calculations across a set of rows related to the current row, without collapsing the result like GROUP BY.",
        "formula": "FUNCTION() OVER (\n  PARTITION BY col\n  ORDER BY col\n  ROWS BETWEEN ... AND ...\n)",
        "description": "Key functions: **ROW_NUMBER**, **RANK**, **DENSE_RANK**, **LAG / LEAD**, **SUM / AVG OVER**, **NTILE**, **FIRST_VALUE / LAST_VALUE**.",
        "example": "Running total of revenue per user: `SUM(revenue) OVER (PARTITION BY user_id ORDER BY date)`",
        "use_cases": ["Running totals", "Period-over-period comparisons", "Ranking within groups", "Moving averages in SQL"],
        "watch_out": "ORDER BY inside OVER affects frame boundaries. Default frame is RANGE UNBOUNDED PRECEDING — always specify ROWS when doing rolling calcs.",
        "python_code": """\
import pandas as pd

df = pd.DataFrame({
    "user_id": [1,1,1,2,2],
    "date":    pd.date_range("2024-01", periods=5, freq="ME"),
    "revenue": [100, 200, 150, 300, 250],
})
df["running_total"] = df.groupby("user_id")["revenue"].cumsum()
df["prev_month"]    = df.groupby("user_id")["revenue"].shift(1)
df["moving_avg_2"]  = (df.groupby("user_id")["revenue"]
                       .transform(lambda x: x.rolling(2).mean()))
print(df)
# Equivalent SQL:
# SELECT *, SUM(revenue) OVER (PARTITION BY user_id ORDER BY date) AS running_total
# LAG(revenue) OVER (PARTITION BY user_id ORDER BY date) AS prev_month
# FROM df
""",
    },

    {
        "title": "11. Data Modeling — Star & Snowflake Schema",
        "roles": ["Analytics Engineer", "Data Engineer"],
        "difficulty": "Foundational",
        "definition": "Dimensional modeling patterns organizing data into fact tables (metrics) and dimension tables (context) for analytical queries.",
        "formula": "Star Schema:      Fact ← Dimensions (denormalized)\nSnowflake Schema: Fact ← Dimensions ← Sub-dimensions (normalized)",
        "description": "- **Fact table**: measurable events (sales, clicks) with foreign keys\n- **Dimension table**: descriptive context (customer, product, date)\n- **Star**: fast queries, some redundancy\n- **Snowflake**: less storage, more joins",
        "example": "fact_orders (order_id, customer_id, product_id, date_id, amount) joins dim_customer, dim_product, dim_date.",
        "use_cases": ["Data warehouse design", "dbt project structure", "BI tool performance", "Reporting layer design"],
        "watch_out": "Snowflake looks clean but adds query complexity. Prefer star schema for BI performance unless storage cost is critical.",
        "python_code": """\
import pandas as pd

fact_orders = pd.DataFrame({
    "order_id":    [1, 2, 3],
    "customer_id": [101, 102, 101],
    "product_id":  [10, 11, 10],
    "amount":      [250.0, 89.99, 310.0],
})
dim_customer = pd.DataFrame({
    "customer_id": [101, 102],
    "name":        ["Alice", "Bob"],
    "region":      ["APAC", "EMEA"],
})
dim_product = pd.DataFrame({
    "product_id": [10, 11],
    "product":    ["Laptop", "Mouse"],
    "category":   ["Electronics", "Accessories"],
})
result = (fact_orders
          .merge(dim_customer, on="customer_id")
          .merge(dim_product,  on="product_id"))
print(result[["order_id","name","product","amount"]])
""",
    },

    # ── INTERMEDIATE ─────────────────────────────────────────────────────────

    {
        "title": "12. Z-Scores & Normal Distribution",
        "roles": ["Data Analyst", "Data Scientist"],
        "difficulty": "Intermediate",
        "definition": "A Z-score measures how many standard deviations a value is from the mean. The normal distribution is a symmetric bell-shaped curve defined by mean and std. deviation.",
        "formula": "Z = (x − μ) / σ\n\nEmpirical Rule:\n  68%  of data within ±1 SD\n  95%  of data within ±2 SD\n  99.7% of data within ±3 SD",
        "description": "Z-scores standardize values across different scales, making them directly comparable. Foundation for hypothesis tests, outlier detection, and anomaly flagging.",
        "example": "μ = $50, σ = $10. An order of $80 → Z = (80−50)/10 = <strong>3.0</strong> → top 0.13% — likely a VIP or data entry error.",
        "use_cases": ["Outlier and anomaly detection", "Standardizing ML features", "Comparing scores across different scales", "Fraud detection"],
        "watch_out": "Z-scores assume normality. On skewed data use the modified Z-score (based on median and MAD).",
        "python_code": """\
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.preprocessing import StandardScaler

orders = np.array([30, 45, 50, 52, 48, 55, 80, 51, 49, 200])
z = stats.zscore(orders, ddof=1)
outliers = orders[np.abs(z) > 3]
print(f"Outliers: {outliers}")

z_val = (80 - 50) / 10
pct = stats.norm.cdf(z_val) * 100
print(f"Z=3.0 → top {100 - pct:.2f}% of orders")

scaler = StandardScaler()
scaled = scaler.fit_transform(orders.reshape(-1, 1))
print(scaled.flatten().round(2))
""",
    },

    {
        "title": "13. Correlation (Pearson & Spearman)",
        "roles": ["Data Analyst", "Data Scientist"],
        "difficulty": "Intermediate",
        "definition": "A measure of the strength and direction of the relationship between two variables, ranging from −1 to +1.",
        "formula": "Pearson r  = Σ((x−x̄)(y−ȳ)) / (n·σx·σy)\nSpearman ρ = 1 − (6·Σd²) / (n·(n²−1))\n\n|r| < 0.3  → weak\n|r| 0.3–0.7 → moderate\n|r| > 0.7  → strong",
        "description": "| Method | Measures | When to Use |\n|--------|----------|-------------|\n| Pearson | Linear relationship | Normal continuous data |\n| Spearman | Monotonic relationship | Ordinal or ranked data |",
        "example": "Ad spend vs revenue: r = 0.85 → strong positive correlation.",
        "use_cases": ["Feature selection for ML", "Identifying business drivers", "Multicollinearity checks in regression"],
        "watch_out": "<strong>Correlation ≠ causation.</strong> Ice cream sales and drowning rates are correlated (both driven by summer).",
        "python_code": """\
import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(42)
ad_spend = rng.uniform(1_000, 10_000, 100)
revenue  = 5_000 + 3 * ad_spend + rng.normal(0, 2_000, 100)

r, p   = stats.pearsonr(ad_spend, revenue)
rho, p2 = stats.spearmanr(ad_spend, revenue)
print(f"Pearson r={r:.3f} (p={p:.4f})")
print(f"Spearman ρ={rho:.3f} (p={p2:.4f})")

df = pd.DataFrame({"ad_spend": ad_spend, "revenue": revenue})
print(df.corr(method="pearson").round(3))
""",
    },

    {
        "title": "14. Hypothesis Testing & P-Values",
        "roles": ["Data Analyst", "Analytics Engineer", "Data Scientist"],
        "difficulty": "Intermediate",
        "definition": "A formal framework for determining whether an observed effect is statistically significant or due to random chance.",
        "formula": "H₀: no effect (null hypothesis)\nH₁: effect exists (alternative)\n\np-value = P(seeing this result | H₀ is true)\np < 0.05  → reject H₀  (significant)\np ≥ 0.05  → fail to reject H₀",
        "description": "Common tests:\n- **t-test**: compare means of two groups\n- **Chi-square**: compare categorical distributions\n- **ANOVA**: compare means across 3+ groups\n- **Mann-Whitney U**: non-parametric alternative to t-test",
        "example": "Variant B: 4.5% conv vs control: 4.0%. p = 0.03 → significant at α=0.05 → safe to ship.",
        "use_cases": ["A/B test analysis", "Product experiment evaluation", "Clinical trial analysis", "Quality control testing"],
        "watch_out": "p < 0.05 ≠ 'large effect'. A tiny difference can be significant with a huge sample. Always report effect size.",
        "python_code": """\
import numpy as np
from scipy import stats

rng = np.random.default_rng(42)
control = rng.normal(loc=4.0, scale=1.0, size=500)
variant = rng.normal(loc=4.5, scale=1.0, size=500)

t_stat, p_val = stats.ttest_ind(control, variant)
print(f"t={t_stat:.3f}  p={p_val:.4f}")
print("Significant!" if p_val < 0.05 else "Not significant")

pooled_std = np.sqrt((control.std()**2 + variant.std()**2) / 2)
cohens_d   = (variant.mean() - control.mean()) / pooled_std
print(f"Cohen's d = {cohens_d:.3f}  (small<0.2, medium<0.5, large>0.8)")

observed = np.array([[400, 100], [420, 80]])
chi2, p_chi, dof, expected = stats.chi2_contingency(observed)
print(f"Chi2={chi2:.3f}  p={p_chi:.4f}")
""",
    },

    {
        "title": "15. Confidence Intervals",
        "roles": ["Data Analyst", "Data Scientist"],
        "difficulty": "Intermediate",
        "definition": "A range of values that, with a specified confidence level (typically 95%), contains the true population parameter.",
        "formula": "CI = x̄ ± (z* × SE)\nSE  = σ / √n\n\nz* for 95% CI = 1.96\nz* for 99% CI = 2.576",
        "description": "A 95% CI means: if repeated 100 times, ~95 of those intervals contain the true value. It is NOT a 95% probability for one specific interval.",
        "example": "Conversion rate: 4.2%, n=2,000 → 95% CI = [3.8%, 4.6%].",
        "use_cases": ["Reporting survey results", "A/B test decision-making", "Model accuracy ranges", "Communicating uncertainty"],
        "watch_out": "Wider CI = less precision, not a flaw. Chasing narrow CIs by ignoring uncertainty misleads decision-makers.",
        "python_code": """\
import numpy as np
from scipy import stats
import statsmodels.stats.proportion as smp

rng = np.random.default_rng(42)
data = rng.normal(loc=4.2, scale=1.0, size=2_000)
ci = stats.t.interval(0.95, df=len(data)-1, loc=data.mean(), scale=stats.sem(data))
print(f"Mean CI 95%: {ci[0]:.3f} – {ci[1]:.3f}")

ci_prop = smp.proportion_confint(84, 2_000, alpha=0.05, method="wilson")
print(f"Proportion CI 95%: {ci_prop[0]*100:.2f}% – {ci_prop[1]*100:.2f}%")

boot_means = np.array([rng.choice(data, size=len(data), replace=True).mean()
                       for _ in range(5_000)])
boot_ci = np.percentile(boot_means, [2.5, 97.5])
print(f"Bootstrap CI 95%: {boot_ci[0]:.3f} – {boot_ci[1]:.3f}")
""",
    },

    {
        "title": "16. Sampling & Sampling Bias",
        "roles": ["Data Analyst", "Analytics Engineer", "Data Scientist"],
        "difficulty": "Intermediate",
        "definition": "Sampling selects a subset of a population for analysis. Bias occurs when the sample systematically differs from the population.",
        "formula": "Margin of Error = z* × √(p(1−p)/n)\nRequired n ≈ (z*/ME)² × p(1−p)",
        "description": "**Types of bias:**\n- **Selection bias**: non-random inclusion\n- **Survivorship bias**: analyzing only those who survived\n- **Response bias**: self-selection skews respondents\n- **Convenience bias**: sampling whoever is easiest to reach",
        "example": "Surveying NPS only from users who logged in this month excludes churned users — satisfaction looks artificially high.",
        "use_cases": ["Survey design", "A/B test setup", "Market research", "Product feedback analysis"],
        "watch_out": "Always ask: 'Who is NOT in my sample and why?' The absence of data is often as informative as the data itself.",
        "python_code": """\
import pandas as pd
import numpy as np
from statsmodels.stats.proportion import samplesize_confint_proportion

rng = np.random.default_rng(42)
df = pd.DataFrame({
    "user_id": range(10_000),
    "plan":    rng.choice(["free","pro","enterprise"], 10_000, p=[0.7,0.2,0.1]),
    "revenue": rng.exponential(50, 10_000),
})
sample_strat = df.groupby("plan", group_keys=False).apply(
    lambda x: x.sample(frac=0.05, random_state=42)
)
print("Stratified sample plan distribution:")
print(sample_strat["plan"].value_counts(normalize=True).round(3))

n_required = samplesize_confint_proportion(0.5, half_length=0.03, alpha=0.05)
print(f"Required n for ±3% margin: {int(np.ceil(n_required))}")
""",
    },

    {
        "title": "17. Linear Regression & Coefficients",
        "roles": ["Data Analyst", "Analytics Engineer", "Data Scientist"],
        "difficulty": "Intermediate",
        "definition": "A model estimating the relationship between independent variables (X) and a dependent variable (Y) by fitting a line.",
        "formula": "Simple:   Y = β₀ + β₁X + ε\nMultiple: Y = β₀ + β₁X₁ + β₂X₂ + ... + ε\n\nR² = 1 − (SS_res / SS_tot)\nRMSE = √(Σ(y − ŷ)² / n)",
        "description": "- **β₀ (intercept)**: predicted Y when all X = 0\n- **β₁ (coefficient)**: change in Y per 1-unit increase in X\n- **R²**: proportion of variance explained\n- **Residuals (ε)**: unexplained portion — should be random",
        "example": "β₁ for ad spend = 2.5 → every $1 more in ads associated with $2.50 more in revenue (holding other factors constant).",
        "use_cases": ["Demand forecasting", "Price elasticity analysis", "Sales attribution modeling", "Feature importance estimation"],
        "watch_out": "R² inflates as you add variables. Use Adjusted R² for multiple regression. Regression shows association, not causation.",
        "python_code": """\
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import statsmodels.api as sm

rng = np.random.default_rng(42)
ad_spend = rng.uniform(1_000, 10_000, 200)
revenue  = 5_000 + 2.5 * ad_spend + rng.normal(0, 2_000, 200)

model = LinearRegression().fit(ad_spend.reshape(-1, 1), revenue)
print(f"β₀={model.intercept_:,.2f}  β₁={model.coef_[0]:.4f}")
print(f"R²={r2_score(revenue, model.predict(ad_spend.reshape(-1,1))):.4f}")
print(f"RMSE={mean_squared_error(revenue, model.predict(ad_spend.reshape(-1,1)))**0.5:,.2f}")

X_sm = sm.add_constant(ad_spend)
ols  = sm.OLS(revenue, X_sm).fit()
print(ols.summary())
""",
    },

    {
        "title": "18. Conditional Probability & Bayes' Theorem",
        "roles": ["Data Scientist"],
        "difficulty": "Intermediate",
        "definition": "Conditional probability is the likelihood of event A given B occurred. Bayes' theorem updates probabilities as new evidence arrives.",
        "formula": "P(A|B) = P(A and B) / P(B)\n\nBayes' Theorem:\nP(A|B) = P(B|A) × P(A) / P(B)\n\nPosterior ∝ Likelihood × Prior",
        "description": "Bayes formalizes belief updating: start with a prior, observe evidence, update to a posterior. Foundation of spam filters, medical diagnostics, and recommendation systems.",
        "example": "99% accurate test, 1% disease prevalence → P(disease | positive) ≈ <strong>50%</strong> — most positives are false alarms due to rare base rate.",
        "use_cases": ["Spam email classification", "Medical diagnosis models", "Lead scoring", "Fraud detection"],
        "watch_out": "Base rate neglect is extremely common. Even a highly accurate test produces mostly false positives for rare conditions.",
        "python_code": """\
p_disease               = 0.01
p_pos_given_disease     = 0.99
p_pos_given_no_disease  = 0.01

p_positive = (p_pos_given_disease * p_disease +
              p_pos_given_no_disease * (1 - p_disease))
p_disease_given_pos = (p_pos_given_disease * p_disease) / p_positive
print(f"P(disease | positive) = {p_disease_given_pos*100:.1f}%")

from sklearn.naive_bayes import GaussianNB
from sklearn.datasets import load_iris
import numpy as np

iris = load_iris()
nb = GaussianNB()
nb.fit(iris.data, iris.target)
sample = np.array([[5.1, 3.5, 1.4, 0.2]])
probs  = nb.predict_proba(sample)[0]
print("Class probabilities:", dict(zip(iris.target_names, probs.round(4))))
""",
    },

    {
        "title": "19. Cohort & Segmentation Analysis",
        "roles": ["Data Analyst", "Analytics Engineer"],
        "difficulty": "Intermediate",
        "definition": "Cohort analysis groups users sharing a common characteristic at a point in time and tracks their behavior over time.",
        "formula": "Retention Rate at n =\n  Active from cohort still active at n / Original cohort size × 100",
        "description": "Cohorts separate the effect of time (how long a user has been around) from calendar period (what's happening in the product now). Without cohorts, retention improvements are hidden by old cohorts churning.",
        "example": "Jan cohort: 40% retention at 6 months. Jun cohort: 25% → product or acquisition quality likely declined.",
        "use_cases": ["SaaS retention analysis", "LTV calculation", "Evaluating product changes", "Acquisition channel quality comparison"],
        "watch_out": "Don't compare cohorts of different sizes without normalization. Distinguish early churn (onboarding) from long-term churn (value decay).",
        "python_code": """\
import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
n = 2_000
df = pd.DataFrame({
    "user_id":     range(n),
    "signup_date": pd.to_datetime(rng.choice(pd.date_range("2024-01-01","2024-06-01", freq="D"), n)),
    "last_active": pd.to_datetime(rng.choice(pd.date_range("2024-01-01","2024-12-01", freq="D"), n)),
})
df["cohort_month"]  = df["signup_date"].dt.to_period("M")
df["periods_since"] = ((df["last_active"].dt.to_period("M") - df["cohort_month"])
                       .apply(lambda x: x.n))
cohort_size = df.groupby("cohort_month")["user_id"].nunique()
retention   = (df.groupby(["cohort_month","periods_since"])["user_id"]
               .nunique().reset_index()
               .pivot(index="cohort_month", columns="periods_since", values="user_id"))
print((retention.divide(cohort_size, axis=0) * 100).round(1).iloc[:, :6])
""",
    },

    {
        "title": "20. Index Numbers & Weighted Averages",
        "roles": ["Data Analyst", "Analytics Engineer"],
        "difficulty": "Intermediate",
        "definition": "An index expresses a value relative to a reference (base) period. A weighted average assigns different importance to values based on size or relevance.",
        "formula": "Index        = (Current Value / Base Value) × 100\nWeighted Avg = Σ(value × weight) / Σ(weight)",
        "description": "**When to use weighted averages:** When groups have very different sizes, a simple average is misleading. A 90% retention from 10 users should NOT equal 90% from 10,000 users.",
        "example": "Simple avg of [50%, 90%] = 70%.<br>Sizes 100 and 1,000: weighted = (50×100 + 90×1000)/1100 = <strong>86.4%</strong>",
        "use_cases": ["CPI and price indices", "Portfolio performance", "Blended NPS across segments", "Weighted KPIs"],
        "watch_out": "Wrong weights massively distort results. Document your weighting methodology and revisit as group sizes change.",
        "python_code": """\
import numpy as np
import pandas as pd

prices = pd.Series([100,108,115,122,130], index=[2020,2021,2022,2023,2024])
index  = prices / prices.iloc[0] * 100
print("Price index (base 2020=100):"); print(index.round(1))

values  = np.array([50, 90])
weights = np.array([100, 1_000])
print(f"Simple avg  : {values.mean():.1f}%")
print(f"Weighted avg: {np.average(values, weights=weights):.1f}%")

nps = pd.DataFrame({"channel":["email","app","web"], "nps":[45,62,38], "users":[5_000,12_000,8_000]})
print(f"Blended NPS: {np.average(nps['nps'], weights=nps['users']):.1f}")
""",
    },

    {
        "title": "21. ETL / ELT Pipeline Concepts",
        "roles": ["Data Engineer", "Analytics Engineer"],
        "difficulty": "Intermediate",
        "definition": "ETL (Extract-Transform-Load) and ELT (Extract-Load-Transform) are patterns for moving and shaping data between systems.",
        "formula": "ETL: Source → Transform → Warehouse\nELT: Source → Warehouse → Transform (in-warehouse)",
        "description": "- **ETL**: transformations happen before loading (traditional, good for sensitive data)\n- **ELT**: raw data lands first, transformations run in the warehouse (modern, dbt-style)\n- Key concerns: idempotency, incremental loads, schema evolution, error handling",
        "example": "dbt runs SQL transformations inside BigQuery/Snowflake after raw data lands from Fivetran → ELT pattern.",
        "use_cases": ["Data warehouse ingestion", "dbt project design", "Real-time streaming pipelines", "Data lake architecture"],
        "watch_out": "Non-idempotent pipelines cause duplicates on reruns. Always design transformations to be safe to re-execute.",
        "python_code": """\
import pandas as pd

def transform_orders(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    df["order_date"]  = pd.to_datetime(df["order_date"])
    df["revenue_usd"] = df["amount"] * df["fx_rate"]
    df = df.drop_duplicates(subset="order_id")   # idempotent dedup
    df = df[df["status"] == "completed"]
    return df

raw = pd.DataFrame({
    "order_id":   [1, 2, 2, 3],
    "order_date": ["2024-01-01","2024-01-02","2024-01-02","2024-01-03"],
    "amount":     [100, 200, 200, 150],
    "fx_rate":    [1.0, 1.0, 1.0, 1.1],
    "status":     ["completed","completed","completed","pending"],
})
print(transform_orders(raw))
""",
    },

    {
        "title": "22. Data Quality & Profiling",
        "roles": ["Analytics Engineer", "Data Engineer"],
        "difficulty": "Intermediate",
        "definition": "The process of examining datasets to understand their structure, completeness, consistency, accuracy, and fitness for purpose.",
        "formula": "Completeness = Non-null rows / Total rows × 100\nUniqueness  = Distinct values / Total rows × 100\nValidity    = Rows passing rules / Total rows × 100",
        "description": "**Key dimensions:** Completeness, Uniqueness, Validity, Timeliness, Consistency, Accuracy.",
        "example": "email column: 98% non-null, 95% match regex, 2% duplicate → flag for deduplication and validation.",
        "use_cases": ["Data contract validation", "Pipeline monitoring", "dbt tests", "Data observability"],
        "watch_out": "Null ≠ missing ≠ zero. Understand what null means in each column's business context before imputing.",
        "python_code": """\
import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
df = pd.DataFrame({
    "user_id": range(1000),
    "email":   [f"u{i}@x.com" if rng.random()>0.03 else None for i in range(1000)],
    "revenue": rng.exponential(100, 1000),
    "country": rng.choice(["PH","US","SG",None], 1000, p=[0.4,0.3,0.2,0.1]),
})

profile = pd.DataFrame({
    "completeness_pct": (df.notna().mean() * 100).round(2),
    "uniqueness_pct":   (df.nunique() / len(df) * 100).round(2),
    "dtype":            df.dtypes.astype(str),
})
print(profile)
print(f"Duplicate rows: {df.duplicated().sum()}")
outliers = (((df.revenue - df.revenue.mean()) / df.revenue.std()).abs() > 3).sum()
print(f"Revenue outliers (>3σ): {outliers}")
""",
    },

    # ── ADVANCED ─────────────────────────────────────────────────────────────

    {
        "title": "23. Multiple Regression",
        "roles": ["Data Analyst", "Data Scientist"],
        "difficulty": "Advanced",
        "definition": "An extension of linear regression modeling a dependent variable against two or more independent variables simultaneously.",
        "formula": "Y = β₀ + β₁X₁ + β₂X₂ + β₃X₃ + ε\n\nAdj. R² = 1 − [(1−R²)(n−1)/(n−k−1)]\nVIF > 10 → multicollinearity problem",
        "description": "**Key checks before trusting results:**\n- **Multicollinearity**: correlated predictors distort coefficients (use VIF)\n- **Heteroscedasticity**: unequal residual variance (use Breusch-Pagan)\n- **Overfitting**: high train R², low test R² (cross-validate)",
        "example": "Revenue = 10,000 + 2.5(AdSpend) + 500(SalesReps) − 200(ChurnRate). Each coefficient holds others constant.",
        "use_cases": ["Marketing mix modeling", "Price optimization", "Sales forecasting", "Causal inference"],
        "watch_out": "Adding variables always increases R². Use Adjusted R² or cross-validation to assess true quality.",
        "python_code": """\
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

rng = np.random.default_rng(42)
n = 300
df = pd.DataFrame({
    "ad_spend":   rng.uniform(1_000, 10_000, n),
    "sales_reps": rng.integers(1, 20, n).astype(float),
    "churn_rate": rng.uniform(0.01, 0.3, n),
})
df["revenue"] = (10_000 + 2.5*df["ad_spend"]
                 + 500*df["sales_reps"]
                 - 200*df["churn_rate"]*100
                 + rng.normal(0, 3_000, n))

X = sm.add_constant(df[["ad_spend","sales_reps","churn_rate"]])
ols = sm.OLS(df["revenue"], X).fit()
print(ols.summary())

vif = pd.DataFrame({"feature": X.columns,
    "VIF": [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]})
print(vif)
""",
    },

    {
        "title": "24. Time Series Analysis",
        "roles": ["Data Analyst", "Analytics Engineer", "Data Scientist"],
        "difficulty": "Advanced",
        "definition": "Methods for modeling sequences of data points collected at successive time intervals: decomposition, forecasting, anomaly detection.",
        "formula": "Decomposition: Y(t) = Trend(t) + Seasonality(t) + Noise(t)\nMoving Avg:   MA(k) = (1/k) × Σ Yᵢ  [i=t−k+1 to t]\nARIMA(p,d,q): AutoRegressive Integrated Moving Average",
        "description": "**Components:** Trend (long-term direction), Seasonality (repeating fixed patterns), Cyclicality (irregular waves), Noise.\n\nCommon models: ARIMA, Exponential Smoothing, Facebook Prophet.",
        "example": "E-commerce sales: upward trend + December spikes + daily noise. 7-day MA smooths noise to reveal trend.",
        "use_cases": ["Demand forecasting", "Financial market analysis", "Anomaly detection in metrics", "Capacity planning"],
        "watch_out": "Most models (ARIMA) require stationarity. Test with Augmented Dickey-Fuller (ADF) first.",
        "python_code": """\
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

rng = np.random.default_rng(42)
dates    = pd.date_range("2022-01-01", periods=104, freq="W")
trend    = np.linspace(100, 200, 104)
seasonal = 20 * np.sin(2 * np.pi * np.arange(104) / 52)
sales    = pd.Series(trend + seasonal + rng.normal(0, 5, 104), index=dates)

sales_df = sales.to_frame("sales")
sales_df["MA7"]  = sales.rolling(7).mean()
sales_df["MA13"] = sales.rolling(13).mean()

result = seasonal_decompose(sales, model="additive", period=52)

adf_stat, p_val, *_ = adfuller(sales)
print(f"ADF p-value: {p_val:.4f}")
print("Stationary" if p_val < 0.05 else "Not stationary → consider differencing")
""",
    },

    {
        "title": "25. A/B Testing & Experimental Design",
        "roles": ["Data Analyst", "Analytics Engineer", "Data Scientist"],
        "difficulty": "Advanced",
        "definition": "A controlled experiment randomly assigning users to variants to measure the causal impact of a change on a defined metric.",
        "formula": "Min sample size per variant:\nn ≈ 2σ²(z_α/2 + z_β)² / δ²\n\nz_α/2 = 1.96 (95% confidence)\nz_β   = 0.84 (80% power)\nδ = minimum detectable effect",
        "description": "**Best practices:** Pre-calculate sample size, randomize properly, define one primary metric, never stop early, run full business cycles.",
        "example": "Blue CTA vs grey. Run until n=5,000 per variant. Blue=4.8%, grey=4.0%, p=0.02 → significant → ship it.",
        "use_cases": ["Product feature launches", "Email subject line optimization", "Pricing page changes", "Onboarding flow improvements"],
        "watch_out": "Early stopping is the #1 mistake. Peeking and stopping inflates false positive rate to 25%+ even at α=0.05.",
        "python_code": """\
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest, proportion_effectsize
from statsmodels.stats.power import NormalIndPower

effect_size = proportion_effectsize(0.045, 0.040)
n_per_group = NormalIndPower().solve_power(effect_size=effect_size, alpha=0.05, power=0.80)
print(f"Required n per variant: {int(np.ceil(n_per_group)):,}")

rng = np.random.default_rng(42)
n = 5_000
control = rng.binomial(1, 0.040, n)
variant = rng.binomial(1, 0.048, n)

z, p = proportions_ztest([variant.sum(), control.sum()], [len(variant), len(control)])
print(f"z={z:.3f}  p={p:.4f}")
print("Ship it!" if p < 0.05 else "Keep testing")

lift = (variant.mean() - control.mean()) / control.mean() * 100
print(f"Relative lift: {lift:.2f}%")
""",
    },

    {
        "title": "26. Statistical Power & Sample Size",
        "roles": ["Data Analyst", "Data Scientist"],
        "difficulty": "Advanced",
        "definition": "Statistical power is the probability a test correctly detects a real effect when one exists (1 − β, target ≥ 0.80).",
        "formula": "Power = 1 − β  (target ≥ 0.80)\n\nPower ↑ when: sample size ↑, effect size ↑, α ↑, variance ↓\n\n| | H₀ True | H₀ False |\n|--|---------|----------|\n| Reject H₀ | Type I (α) | Correct |\n| Fail to Reject | Correct | Type II (β) |",
        "description": "Underpowered tests miss real effects. Overpowered tests detect trivially small, irrelevant effects.",
        "example": "Testing 0.5% lift on 4% base → ~75,000 users per variant at 80% power. Low-traffic sites may wait months.",
        "use_cases": ["A/B test planning", "Clinical trial design", "Minimum viable experiment scoping"],
        "watch_out": "Post-hoc power analysis is misleading. Always calculate required sample size BEFORE starting the experiment.",
        "python_code": """\
import numpy as np
from statsmodels.stats.power import TTestIndPower

analysis = TTestIndPower()
n = analysis.solve_power(effect_size=0.3, alpha=0.05, power=0.80)
print(f"n per group for d=0.3, α=0.05, power=0.80: {int(np.ceil(n))}")

sample_sizes = np.arange(10, 500, 10)
powers = [analysis.solve_power(effect_size=0.3, alpha=0.05, nobs1=n, ratio=1)
          for n in sample_sizes]

for n, pw in zip(sample_sizes[::5], powers[::5]):
    print(f"n={n:3d} → power={pw:.3f}")
""",
    },

    {
        "title": "27. Survival / Retention Analysis",
        "roles": ["Data Analyst", "Data Scientist"],
        "difficulty": "Advanced",
        "definition": "Methods for modeling time until a specific event (churn, conversion), accounting for users who haven't experienced it yet (censoring).",
        "formula": "Kaplan-Meier Estimator:\nS(t) = Π [ (nᵢ − dᵢ) / nᵢ ]  for all tᵢ ≤ t\n\nnᵢ = at-risk count at t\ndᵢ = events at t",
        "description": "- **S(t)**: probability of surviving (not churning) past time t\n- **Hazard rate**: instantaneous churn risk at t\n- **Censoring**: users still active\n- **Cox PH**: extends survival analysis with covariates",
        "example": "80% active at 30 days, 50% at 90 days, 30% at 180 days. Steepest drop first 2 weeks → onboarding problem.",
        "use_cases": ["SaaS churn prediction", "Customer LTV modeling", "Credit risk duration modeling"],
        "watch_out": "Censoring must be non-informative — users shouldn't drop out because they're about to churn.",
        "python_code": """\
# pip install lifelines
import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter, CoxPHFitter

rng = np.random.default_rng(42)
n = 500
df = pd.DataFrame({
    "duration":  rng.integers(1, 365, n),
    "event":     rng.binomial(1, 0.6, n),
    "plan_pro":  rng.binomial(1, 0.4, n),
    "logins_pw": rng.poisson(5, n),
})
kmf = KaplanMeierFitter()
kmf.fit(df["duration"], event_observed=df["event"])
print(f"Median survival time: {kmf.median_survival_time_} days")

cph = CoxPHFitter()
cph.fit(df, duration_col="duration", event_col="event")
cph.print_summary()
""",
    },

    {
        "title": "28. Simpson's Paradox & Statistical Pitfalls",
        "roles": ["Data Analyst", "Data Scientist"],
        "difficulty": "Advanced",
        "definition": "A trend appearing in aggregate data disappears or reverses when broken down by subgroups.",
        "formula": "No formula — structural reasoning failure.\nCheck: Do aggregate trends match all subgroup trends?",
        "description": "**Common pitfalls:** Simpson's Paradox, P-hacking (multiple comparisons), HARKing, Base rate neglect, Ecological fallacy.",
        "example": "Hospital A has higher overall survival than B. But B is better for BOTH mild and severe cases — it handles more severe cases.",
        "use_cases": ["Multi-segment reporting", "Policy evaluation", "Medical and social research", "Experiment post-mortems"],
        "watch_out": "Always segment your data before drawing conclusions. A single aggregate number almost never tells the whole story.",
        "python_code": """\
import pandas as pd
from statsmodels.stats.multitest import multipletests
from scipy.stats import ttest_ind
import numpy as np

data = {"hospital":["A","A","B","B"], "severity":["mild","severe","mild","severe"],
        "survived":[800,200,900,400], "total":[900,300,950,500]}
df = pd.DataFrame(data)
df["rate"] = df["survived"] / df["total"]
agg = df.groupby("hospital")[["survived","total"]].sum()
agg["rate"] = agg["survived"] / agg["total"]
print("Aggregate:"); print(agg["rate"].round(3))
print("\\nBy severity:")
print(df.pivot(index="severity", columns="hospital", values="rate").round(3))

rng = np.random.default_rng(42)
pvals = [ttest_ind(rng.normal(0,1,100), rng.normal(0,1,100)).pvalue for _ in range(20)]
reject_bh, *_ = multipletests(pvals, method="fdr_bh")[:2]
print(f"\\nRaw α=0.05 rejections : {sum(p<0.05 for p in pvals)}/20")
print(f"BH FDR rejections      : {sum(reject_bh)}/20")
""",
    },

    {
        "title": "29. Slowly Changing Dimensions (SCD)",
        "roles": ["Data Engineer", "Analytics Engineer"],
        "difficulty": "Advanced",
        "definition": "Techniques for tracking how dimensional attribute values change over time in a data warehouse.",
        "formula": "SCD Type 1: Overwrite old value (no history)\nSCD Type 2: New row per change  (full history)\nSCD Type 3: Add column for previous value (limited history)",
        "description": "- **Type 1**: simple, no history — use for corrections\n- **Type 2**: add effective_date, expiry_date, is_current — full history, most common\n- **Type 3**: one previous value only — rare",
        "example": "Customer moves city: Type 2 closes old row (expiry=today), inserts new row (city=Manila, is_current=True).",
        "use_cases": ["Customer address tracking", "Product price history", "Employee role changes", "dbt snapshots"],
        "watch_out": "Type 2 tables grow large and complicate queries. Always add a surrogate key and is_current flag.",
        "python_code": """\
import pandas as pd
from datetime import date

existing = pd.DataFrame({
    "surrogate_key":  [1],
    "customer_id":    [101],
    "city":           ["Cebu"],
    "effective_date": [date(2023, 1, 1)],
    "expiry_date":    [date(9999, 12, 31)],
    "is_current":     [True],
})

def scd2_update(df, customer_id, new_city, change_date):
    df = df.copy()
    mask = (df["customer_id"] == customer_id) & (df["is_current"])
    df.loc[mask, "expiry_date"] = change_date
    df.loc[mask, "is_current"]  = False
    new_row = {"surrogate_key": df["surrogate_key"].max() + 1,
               "customer_id": customer_id, "city": new_city,
               "effective_date": change_date,
               "expiry_date": date(9999, 12, 31), "is_current": True}
    return pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

result = scd2_update(existing, 101, "Manila", date(2024, 6, 1))
print(result)
""",
    },

    # ── EXPERT ───────────────────────────────────────────────────────────────

    {
        "title": "30. Entropy & Information Gain",
        "roles": ["Data Scientist"],
        "difficulty": "Expert",
        "definition": "Entropy measures impurity of a dataset. Information Gain measures how much a feature reduces entropy after a split.",
        "formula": "H(S) = −Σ pᵢ × log₂(pᵢ)\n\nIG(S,A) = H(S) − Σ (|Sᵥ|/|S|) × H(Sᵥ)\n\nH = 0  → pure (all one class)\nH = 1  → maximum disorder (50/50)",
        "description": "Decision tree algorithms (ID3, C4.5) greedily choose splits that maximize information gain, reducing entropy toward 0 at each node.",
        "example": "50% spam, 50% not → H=1.0. After splitting on 'contains FREE': 90% spam | 10% spam → large IG → good split.",
        "use_cases": ["Decision tree feature selection", "Random forest variable importance", "Text classification", "Feature ranking"],
        "watch_out": "IG favors features with many unique values (like IDs). Use Gain Ratio (C4.5) or Gini impurity (CART) to correct.",
        "python_code": """\
import numpy as np
from scipy.stats import entropy
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.feature_selection import mutual_info_classif
from sklearn.datasets import load_iris

def calc_entropy(labels):
    _, counts = np.unique(labels, return_counts=True)
    return entropy(counts / counts.sum(), base=2)

print(f"Mixed : {calc_entropy(np.array([0]*50+[1]*50)):.4f}")
print(f"Pure  : {calc_entropy(np.array([0]*100)):.4f}")

iris = load_iris()
dt = DecisionTreeClassifier(criterion="entropy", max_depth=3, random_state=42)
dt.fit(iris.data, iris.target)
for feat, imp in zip(iris.feature_names, dt.feature_importances_):
    print(f"{feat}: {imp:.4f}")
""",
    },

    {
        "title": "31. Bias–Variance Tradeoff",
        "roles": ["Data Scientist"],
        "difficulty": "Expert",
        "definition": "The fundamental ML tension between a model too simple to capture patterns (high bias) and one too complex that memorizes noise (high variance).",
        "formula": "Total Error = Bias² + Variance + Irreducible Noise\n\nHigh Bias:     train error ≈ test error (both high)\nHigh Variance: train error << test error",
        "description": "| | High Bias | High Variance |\n|---|---|---|\n| Also called | Underfitting | Overfitting |\n| Train error | High | Low |\n| Test error | High | High |\n| Fix | More complexity | Regularization / more data |",
        "example": "Decision tree depth=1: underfits. Depth=30: memorizes. Optimal depth (5–7) balances both.",
        "use_cases": ["Model selection", "Hyperparameter tuning", "Diagnosing train vs validation gaps"],
        "watch_out": "More data reduces variance but NOT bias. If underfitting, more data won't help — increase model capacity.",
        "python_code": """\
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import validation_curve
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=1_000, n_features=20, random_state=42, n_informative=10)
depths = np.arange(1, 20)
train_s, val_s = validation_curve(
    DecisionTreeClassifier(random_state=42), X, y,
    param_name="max_depth", param_range=depths, cv=5, scoring="accuracy")

for d, tr, vl in zip(depths, train_s.mean(axis=1), val_s.mean(axis=1)):
    if d in [1, 5, 10, 15, 19]:
        print(f"depth={d:2d}  train={tr:.3f}  val={vl:.3f}")
""",
    },

    {
        "title": "32. Cross-Validation",
        "roles": ["Data Scientist"],
        "difficulty": "Expert",
        "definition": "A technique to estimate model generalization by training and testing on multiple non-overlapping splits of the data.",
        "formula": "k-Fold CV Score = (1/k) × Σ score(fold_i)\n\nReport: mean ± std across folds",
        "description": "Stratified k-Fold preserves class balance in each fold — essential for imbalanced datasets. Nested CV is used for simultaneous hyperparameter tuning and evaluation.",
        "example": "5-fold CV: [0.82, 0.85, 0.81, 0.84, 0.83] → CV = <strong>0.83 ± 0.015</strong>. Far more reliable than one split.",
        "use_cases": ["Model selection and comparison", "Hyperparameter tuning (nested CV)", "Performance estimation before deployment"],
        "watch_out": "Data leakage through CV is critical: preprocessing must be fit INSIDE each fold, never on the full dataset.",
        "python_code": """\
from sklearn.datasets import make_classification
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate, StratifiedKFold

X, y = make_classification(n_samples=1_000, n_features=20, random_state=42, n_informative=10)
pipe = Pipeline([("scaler", StandardScaler()), ("clf", LogisticRegression(max_iter=1_000))])
skf  = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
res  = cross_validate(pipe, X, y, cv=skf,
                      scoring=["accuracy","roc_auc","f1"],
                      return_train_score=True)
for m in ["test_accuracy","test_roc_auc","test_f1"]:
    print(f"{m}: {res[m].mean():.4f} ± {res[m].std():.4f}")
""",
    },

    {
        "title": "33. Regularization (L1 & L2)",
        "roles": ["Data Scientist"],
        "difficulty": "Expert",
        "definition": "A penalty added to the loss function to discourage large coefficients, reducing overfitting by constraining model complexity.",
        "formula": "L1 (Lasso):  Loss = MSE + λ × Σ|βᵢ|\nL2 (Ridge):  Loss = MSE + λ × Σβᵢ²\nElastic Net: Loss = MSE + λ₁Σ|βᵢ| + λ₂Σβᵢ²",
        "description": "| | L1 (Lasso) | L2 (Ridge) |\n|--|--|--|\n| Effect | Zeros some coefficients | Shrinks all toward 0 |\n| Result | Sparse model (feature selection) | Dense model |\n| Use when | Many irrelevant features | All features contribute |",
        "example": "With 100 features, Lasso (λ=0.1) zeros out 80 — automatic feature selection, leaving 20 predictors.",
        "use_cases": ["Preventing overfitting", "Automatic feature selection (L1)", "Neural network weight decay (L2)", "High-dimensional datasets"],
        "watch_out": "λ is critical. Too high → underfitting. Too low → no regularization. Use LassoCV/RidgeCV for auto-tuning.",
        "python_code": """\
from sklearn.linear_model import Lasso, Ridge, ElasticNet, LassoCV
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

X, y = make_regression(n_samples=500, n_features=100, n_informative=20, noise=30, random_state=42)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
sc = StandardScaler()
X_tr = sc.fit_transform(X_tr); X_te = sc.transform(X_te)

for name, model in [("Lasso", Lasso(0.5)), ("Ridge", Ridge(1.0)), ("ElasticNet", ElasticNet(0.5, l1_ratio=0.5))]:
    model.fit(X_tr, y_tr)
    print(f"{name:12s}  R²={(r2_score(y_te, model.predict(X_te))):.4f}  zeros={(model.coef_==0).sum()}/100")

lcv = LassoCV(cv=5, random_state=42).fit(X_tr, y_tr)
print(f"LassoCV best α={lcv.alpha_:.4f}  active={(lcv.coef_!=0).sum()}/100")
""",
    },

    {
        "title": "34. Gradient Descent",
        "roles": ["Data Scientist"],
        "difficulty": "Expert",
        "definition": "An iterative optimization algorithm that minimizes a loss function by updating parameters in the direction of the steepest negative gradient.",
        "formula": "θ := θ − α × ∇J(θ)\n\nα     = learning rate\n∇J(θ) = gradient of loss w.r.t. θ\n\nAdam: adaptive per-parameter learning rates",
        "description": "| Variant | Data/step | Pros | Cons |\n|---------|-----------|------|------|\n| Batch GD | All data | Stable convergence | Slow on large data |\n| SGD | 1 sample | Fast updates | Very noisy |\n| Mini-batch | 32–512 | Best of both | Needs tuning |",
        "example": "In linear regression, gradient descent iteratively adjusts weights proportional to prediction error.",
        "use_cases": ["Training neural networks", "Logistic regression optimization", "Any differentiable loss minimization"],
        "watch_out": "Learning rate α is critical. Too large → diverge. Too small → slow convergence. Use schedulers in production.",
        "python_code": """\
import numpy as np

rng = np.random.default_rng(42)
X = rng.uniform(0, 10, (200, 1))
y = 3 * X.flatten() + 7 + rng.normal(0, 1, 200)

X_b   = np.c_[np.ones(len(X)), X]
theta = np.zeros(2)
alpha = 0.01
losses = []

for epoch in range(300):
    error = X_b @ theta - y
    theta -= alpha * (2 / len(y)) * X_b.T @ error
    losses.append((error**2).mean())

print(f"Learned: intercept={theta[0]:.3f}, slope={theta[1]:.3f}")
print(f"True:    intercept=7.000, slope=3.000")
print(f"Final MSE loss: {losses[-1]:.4f}")
""",
    },

    {
        "title": "35. Confusion Matrix & Classification Metrics",
        "roles": ["Data Scientist", "Analytics Engineer"],
        "difficulty": "Expert",
        "definition": "A confusion matrix summarizes classifier performance by comparing actual vs. predicted labels across all classes.",
        "formula": "Accuracy  = (TP+TN) / (TP+TN+FP+FN)\nPrecision = TP / (TP+FP)\nRecall    = TP / (TP+FN)\nF1        = 2×(P×R) / (P+R)\nMCC       = (TP×TN−FP×FN) / √((TP+FP)(TP+FN)(TN+FP)(TN+FN))",
        "description": "- **Precision**: of predicted positives, how many are correct?\n- **Recall**: of actual positives, how many caught?\n- **F1**: harmonic mean, balances precision and recall\n- **AUC-ROC**: discriminative ability across all thresholds\n- **MCC**: best single metric for imbalanced classes",
        "example": "Fraud detection: missing fraud (FN) is costly → maximize Recall. Spam filter: FP deletes real emails → maximize Precision.",
        "use_cases": ["Model evaluation", "Threshold selection", "Class imbalance analysis"],
        "watch_out": "Accuracy is useless for imbalanced classes. A model always predicting 'no fraud' gets 99% accuracy on 1% fraud data.",
        "python_code": """\
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (classification_report, roc_auc_score,
                              matthews_corrcoef, roc_curve)

X, y = make_classification(n_samples=2_000, weights=[0.9, 0.1], random_state=42)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42)
clf.fit(X_tr, y_tr)
y_pred = clf.predict(X_te)
y_prob = clf.predict_proba(X_te)[:, 1]

print(classification_report(y_te, y_pred))
print(f"AUC-ROC : {roc_auc_score(y_te, y_prob):.4f}")
print(f"MCC     : {matthews_corrcoef(y_te, y_pred):.4f}")
""",
    },

    {
        "title": "36. Dimensionality Reduction (PCA, t-SNE, UMAP)",
        "roles": ["Data Scientist"],
        "difficulty": "Expert",
        "definition": "Techniques to reduce features while preserving important structure, relationships, or variance in the data.",
        "formula": "PCA: Eigendecompose covariance matrix\nExplained Variance Ratio = λ_k / Σλ\n\nt-SNE minimizes KL divergence between\nhigh-dim and low-dim distributions",
        "description": "| Method | Type | Preserves | Speed | Use For |\n|--------|------|-----------|-------|---------|\n| PCA | Linear | Global variance | Fast | Preprocessing |\n| t-SNE | Non-linear | Local clusters | Slow | 2D/3D viz |\n| UMAP | Non-linear | Local + global | Moderate | Viz + ML |",
        "example": "100-feature dataset → 10 PCA components explain 95% variance → train on 10, less overfitting, faster.",
        "use_cases": ["Visualization of high-dimensional data", "Noise reduction before modeling", "Feature extraction", "Genomics and NLP embeddings"],
        "watch_out": "t-SNE axes carry no meaning and inter-cluster distances are unreliable. Never use t-SNE output as ML input features.",
        "python_code": """\
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_digits

digits = load_digits()
X_s    = StandardScaler().fit_transform(digits.data)

pca    = PCA().fit(X_s)
cumvar = np.cumsum(pca.explained_variance_ratio_)
n_95   = np.searchsorted(cumvar, 0.95) + 1
print(f"Components for 95% variance: {n_95}")

X_pca = PCA(n_components=n_95).fit_transform(X_s)
print(f"Reduced shape: {X_pca.shape}")

X_2d = TSNE(n_components=2, random_state=42, perplexity=30).fit_transform(X_s)
print(f"t-SNE shape: {X_2d.shape}")
""",
    },

    {
        "title": "37. Loss Functions",
        "roles": ["Data Scientist"],
        "difficulty": "Expert",
        "definition": "A function quantifying the gap between model predictions and actual values — the objective minimized during training.",
        "formula": "MSE      = (1/n) × Σ(yᵢ − ŷᵢ)²\nMAE      = (1/n) × Σ|yᵢ − ŷᵢ|\nHuber    = MSE if |e|≤δ, else δ(|e|−δ/2)\nLog Loss = −(1/n) × Σ[y·log(ŷ) + (1−y)·log(1−ŷ)]",
        "description": "| Loss | Outlier Sensitive | Task |\n|------|-------------------|------|\n| MSE | Yes (squares errors) | Regression |\n| MAE | No | Regression |\n| Huber | No | Robust regression |\n| Log Loss | — | Binary classification |\n| Cross-entropy | — | Multi-class |",
        "example": "House prices with $2M outlier: MSE penalizes it 4× more than MAE. Use Huber when outliers are expected.",
        "use_cases": ["Training all supervised ML", "Custom business-constrained objectives", "Model evaluation"],
        "watch_out": "Log loss heavily penalizes confident wrong predictions. Miscalibrated models need Platt scaling or isotonic regression.",
        "python_code": """\
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, log_loss

rng = np.random.default_rng(42)
y_true = rng.normal(100, 20, 200)
y_pred = y_true + rng.normal(0, 10, 200)
y_pred_out = y_pred.copy(); y_pred_out[0] = 500

print(f"MSE  (clean)  : {mean_squared_error(y_true, y_pred):.2f}")
print(f"MSE  (outlier): {mean_squared_error(y_true, y_pred_out):.2f}")
print(f"MAE  (clean)  : {mean_absolute_error(y_true, y_pred):.2f}")
print(f"MAE  (outlier): {mean_absolute_error(y_true, y_pred_out):.2f}")

def huber(y, yh, d=10):
    e = y - yh
    return np.where(np.abs(e)<=d, 0.5*e**2, d*(np.abs(e)-0.5*d)).mean()
print(f"Huber (outlier): {huber(y_true, y_pred_out):.2f}")

y_cls  = np.array([0, 0, 1, 1, 1])
y_prob = np.array([0.1, 0.2, 0.8, 0.9, 0.7])
print(f"Log Loss: {log_loss(y_cls, y_prob):.4f}")
""",
    },

    {
        "title": "38. Feature Engineering & Encoding",
        "roles": ["Data Scientist", "Analytics Engineer"],
        "difficulty": "Expert",
        "definition": "Transforming raw data into informative, model-ready features that improve predictive performance.",
        "formula": "Min-Max:       x' = (x − min) / (max − min)\nZ-score:       x' = (x − μ) / σ\nLog transform: x' = log(x + 1)",
        "description": "**Encoding:** One-hot (nominal, low cardinality), Label (ordinal only), Target encoding (leakage risk), Frequency encoding.\n**Transforms:** Log (right skew), Polynomial (non-linear), Binning (continuous → ordinal).",
        "example": "City with 50 unique values → target encoding replaces each city with its historical conversion rate — must be computed inside CV folds.",
        "use_cases": ["All supervised ML pipelines", "Reducing cardinality in tree models", "NLP preprocessing"],
        "watch_out": "Target encoding leaks label info. Always compute inside CV folds using only training data — never on full dataset before splitting.",
        "python_code": """\
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

rng = np.random.default_rng(42)
df = pd.DataFrame({
    "revenue":   rng.exponential(1_000, 500),
    "city":      rng.choice(["Manila","Davao","Cebu"], 500),
    "logins":    rng.integers(0, 100, 500),
    "converted": rng.binomial(1, 0.3, 500),
})
df["log_revenue"] = np.log1p(df["revenue"])
df["city_freq"]   = df["city"].map(df["city"].value_counts())

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), ["logins", "log_revenue"]),
    ("cat", OneHotEncoder(drop="first", sparse_output=False), ["city"]),
])
X = preprocessor.fit_transform(df.drop(columns="converted"))
print(f"Transformed shape: {X.shape}")
""",
    },

    {
        "title": "39. Class Imbalance Techniques",
        "roles": ["Data Scientist"],
        "difficulty": "Expert",
        "definition": "Methods to handle datasets where one class significantly outnumbers another, biasing models toward the majority class.",
        "formula": "SMOTE: interpolate between k-nearest minority neighbors\n\nClass weight:\n  w_minority = n_total / (2 × n_minority)\n  w_majority = n_total / (2 × n_majority)",
        "description": "| Approach | Method | When |\n|----------|--------|------|\n| Data-level | SMOTE oversampling | Moderate imbalance |\n| Data-level | Undersampling | Very large majority |\n| Algorithm | Class weighting | Most sklearn classifiers |\n| Threshold | Adjust decision cutoff | Tune precision/recall |",
        "example": "Fraud: 99% non-fraud. Always predicting 'no fraud' → 99% accuracy, 0% recall. Apply 1:99 weights → recall improves.",
        "use_cases": ["Fraud detection", "Medical diagnosis", "Rare event prediction", "Anomaly detection"],
        "watch_out": "SMOTE creates synthetic points that may not reflect real data. Never oversample the test set — only inside training folds.",
        "python_code": """\
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
# pip install imbalanced-learn
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

X, y = make_classification(n_samples=5_000, weights=[0.97, 0.03], random_state=42)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

# Baseline
base = LogisticRegression(max_iter=1_000).fit(X_tr, y_tr)
print("Baseline:"); print(classification_report(y_te, base.predict(X_te), digits=3))

# SMOTE pipeline
pipe = ImbPipeline([("smote", SMOTE(random_state=42)),
                    ("clf", LogisticRegression(max_iter=1_000))])
pipe.fit(X_tr, y_tr)
print("SMOTE:"); print(classification_report(y_te, pipe.predict(X_te), digits=3))
""",
    },

    {
        "title": "40. Bayesian vs Frequentist Statistics",
        "roles": ["Data Scientist"],
        "difficulty": "Expert",
        "definition": "Two frameworks for statistical inference differing in how probability is defined and how unknown parameters are treated.",
        "formula": "Frequentist: P(data | hypothesis) → p-value\n\nBayesian: P(hypothesis | data) ∝ P(data|H) × P(H)\n          posterior ∝ likelihood × prior",
        "description": "| | Frequentist | Bayesian |\n|---|---|---|\n| Probability | Long-run frequency | Degree of belief |\n| Parameters | Fixed, unknown | Random, have distributions |\n| Output | p-values, CIs | Posterior distributions |\n| Prior knowledge | Not incorporated | Explicitly used |",
        "example": "Bayesian A/B: 'P(B > A) = 94%' — directly interpretable for business. No need for fixed sample size.",
        "use_cases": ["A/B testing with small samples", "Incremental model updating", "Spam filtering (Naive Bayes)", "Medical decisions"],
        "watch_out": "Results depend on the prior. Document prior assumptions explicitly and test sensitivity to prior choice.",
        "python_code": """\
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest

rng = np.random.default_rng(42)
n = 1_000
ctrl = rng.binomial(1, 0.05, n)
var  = rng.binomial(1, 0.07, n)

z, p = proportions_ztest([var.sum(), ctrl.sum()], [n, n])
print(f"Frequentist p-value: {p:.4f}")

a_ctrl = 1 + ctrl.sum(); b_ctrl = 1 + (n - ctrl.sum())
a_var  = 1 + var.sum();  b_var  = 1 + (n - var.sum())

s_ctrl = stats.beta.rvs(a_ctrl, b_ctrl, size=100_000, random_state=42)
s_var  = stats.beta.rvs(a_var,  b_var,  size=100_000, random_state=42)
prob   = (s_var > s_ctrl).mean()
print(f"Bayesian P(variant > control) = {prob*100:.1f}%")
""",
    },

    {
        "title": "41. Monte Carlo Simulation",
        "roles": ["Data Scientist", "Data Analyst"],
        "difficulty": "Expert",
        "definition": "A technique using repeated random sampling to estimate the probability distribution of outcomes with uncertain inputs.",
        "formula": "E[f(X)] ≈ (1/N) × Σ f(xᵢ)  where xᵢ ~ P(X)\n\nLaw of Large Numbers: estimate → true value as N → ∞",
        "description": "**Steps:** Define input distributions → Sample N times (10,000+) → Compute output each iteration → Analyze output distribution (mean, CI, P(loss)).",
        "example": "Revenue ~ N($500K,$50K), cost ~ N($400K,$40K). 100K simulations → P(profit>0)=89%, median=$95K.",
        "use_cases": ["Financial risk (VaR)", "Supply chain scenario planning", "Option pricing", "Project timeline estimation"],
        "watch_out": "Results are only as good as input distributions — garbage in, garbage out. Always run sensitivity analysis.",
        "python_code": """\
import numpy as np

rng = np.random.default_rng(42)
N = 100_000
revenue = rng.normal(500_000, 50_000, N)
cost    = rng.normal(400_000, 40_000, N)
profit  = revenue - cost

print(f"P(profit > 0)  : {(profit > 0).mean()*100:.1f}%")
print(f"Median profit  : ${np.median(profit):,.0f}")
print(f"5th percentile : ${np.percentile(profit, 5):,.0f}  (worst-case / VaR)")
print(f"95% CI         : ${np.percentile(profit, 2.5):,.0f} – ${np.percentile(profit, 97.5):,.0f}")

corr_rev = np.corrcoef(revenue, profit)[0,1]
corr_cst = np.corrcoef(cost, profit)[0,1]
print(f"Revenue sensitivity: {corr_rev:.3f}")
print(f"Cost sensitivity   : {corr_cst:.3f}")
""",
    },

    {
        "title": "42. Stream Processing Concepts",
        "roles": ["Data Engineer"],
        "difficulty": "Expert",
        "definition": "Processing data records continuously as they arrive, enabling low-latency analytics and real-time pipelines.",
        "formula": "Tumbling window: fixed, non-overlapping intervals\nSliding window:  fixed size, slides by step\nSession window:  gaps in activity define boundaries",
        "description": "**Key concepts:** Watermarks (late data handling), Exactly-once semantics, Backpressure, State stores.\n\n**Tools:** Apache Kafka, Apache Flink, Spark Structured Streaming, AWS Kinesis.",
        "example": "Count page views per user per 5-minute tumbling window → alert if views > 1000 (bot detection).",
        "use_cases": ["Real-time dashboards", "Fraud detection pipelines", "IoT sensor processing", "Event-driven architectures"],
        "watch_out": "Out-of-order events and late data are the #1 challenge. Always define watermark policies and test with delayed records.",
        "python_code": """\
import pandas as pd

events = pd.DataFrame({
    "user_id":    [1,1,2,1,2,2,1],
    "event_time": pd.to_datetime([
        "2024-01-01 10:00:01","2024-01-01 10:02:30",
        "2024-01-01 10:03:00","2024-01-01 10:06:00",
        "2024-01-01 10:07:00","2024-01-01 10:08:00",
        "2024-01-01 10:11:00",
    ]),
    "value": [1,1,1,1,1,1,1],
})

# 5-minute tumbling window aggregation
events = events.set_index("event_time").sort_index()
result = (events.groupby("user_id")
          .resample("5min")["value"].sum().reset_index())
result.columns = ["user_id","window_start","event_count"]
result["window_end"] = result["window_start"] + pd.Timedelta(minutes=5)
print(result)

# Equivalent Spark Structured Streaming:
# df.groupBy("user_id", window("event_time", "5 minutes")).count()
""",
    },

    {
        "title": "43. Graph Metrics & Network Analysis",
        "roles": ["Data Scientist", "Data Engineer"],
        "difficulty": "Expert",
        "definition": "Mathematical measures describing properties of nodes and edges in a network to find influential nodes, communities, and paths.",
        "formula": "Degree Centrality     = degree(v) / (n−1)\nBetweenness          = Σ σ(s,t|v) / σ(s,t)\nPageRank             = (1−d)/n + d × Σ (PR(u)/L(u))\nClustering Coeff     = 2×triangles / (degree×(degree−1))",
        "description": "**Key metrics:** Degree (connections), Betweenness (bridge importance), Closeness (reach), PageRank (influence), Clustering coefficient (local density).",
        "example": "High betweenness user bridges two communities — removing them disconnects the network (critical node).",
        "use_cases": ["Fraud ring detection", "Recommendation systems", "Supply chain mapping", "Social influence analysis"],
        "watch_out": "PageRank assumes a random surfer model. Betweenness is O(n³) — expensive on large graphs. Use approximations.",
        "python_code": """\
# pip install networkx
import networkx as nx

G = nx.karate_club_graph()
print(f"Nodes: {G.number_of_nodes()}  Edges: {G.number_of_edges()}")

degree_cent  = nx.degree_centrality(G)
between_cent = nx.betweenness_centrality(G)
pagerank     = nx.pagerank(G, alpha=0.85)

top3 = lambda d: sorted(d.items(), key=lambda x: -x[1])[:3]
print("Top degree      :", top3(degree_cent))
print("Top betweenness :", top3(between_cent))
print("Top PageRank    :", top3(pagerank))
print(f"Avg clustering  : {nx.average_clustering(G):.4f}")
print(f"Diameter        : {nx.diameter(G)}")
""",
    },

    {
        "title": "44. Vector Embeddings & Similarity Search",
        "roles": ["Data Scientist", "Data Engineer"],
        "difficulty": "Expert",
        "definition": "Representing objects (text, images, users) as dense numerical vectors where semantic similarity maps to geometric proximity.",
        "formula": "Cosine Similarity = (A · B) / (|A| × |B|)\nEuclidean Distance = √Σ(aᵢ − bᵢ)²\nDot Product        = Σ aᵢ × bᵢ",
        "description": "**Vector DBs:** Pinecone, Weaviate, pgvector, Chroma, Qdrant.\n\nUsed in RAG (Retrieval-Augmented Generation), semantic search, and recommendations.",
        "example": "User embedding vs product embedding → cosine sim = 0.98 → recommend product.",
        "use_cases": ["Semantic search", "Recommendation systems", "RAG pipelines", "Duplicate detection"],
        "watch_out": "Cosine similarity ignores magnitude. Two vectors can be 'similar' in direction but very different in scale. Use dot product when magnitude matters.",
        "python_code": """\
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

rng = np.random.default_rng(42)
embeddings = rng.normal(0, 1, (5, 64))
labels = ["product_A","product_B","user_1","product_C","user_2"]

cos_sim = cosine_similarity(embeddings)
print("Cosine similarity matrix:")
print(pd.DataFrame(cos_sim, index=labels, columns=labels).round(3))

query = embeddings[2]  # user_1
sims  = cosine_similarity([query], embeddings)[0]
ranked = sorted(zip(labels, sims), key=lambda x: -x[1])
print("\\nRanked similarity to user_1:")
for name, score in ranked:
    print(f"  {name}: {score:.4f}")
""",
    },

]


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
ROLE_OPTIONS = ["Data Analyst", "Analytics Engineer",
                "Data Engineer", "Data Scientist"]
DIFF_OPTIONS = ["Foundational", "Intermediate", "Advanced", "Expert"]

ROLE_BADGE = {
    "Data Analyst":       "analyst",
    "Analytics Engineer": "analytics_eng",
    "Data Engineer":      "data_eng",
    "Data Scientist":     "data_sci",
}

st.sidebar.title("⚙️ Filters")

st.sidebar.markdown("**🧑‍💼 Category I — Role**")
role_filter = st.sidebar.multiselect(
    "Filter by role:",
    options=ROLE_OPTIONS,
    default=ROLE_OPTIONS,
    label_visibility="collapsed",
)

st.sidebar.markdown("**📈 Category II — Difficulty**")
diff_filter = st.sidebar.multiselect(
    "Filter by difficulty:",
    options=DIFF_OPTIONS,
    default=DIFF_OPTIONS,
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
search = st.sidebar.text_input(
    "🔍 Search", placeholder="e.g. entropy, p-value, SCD")

st.sidebar.markdown("---")
st.sidebar.markdown("**📚 Topics by Role**")
for role in ROLE_OPTIONS:
    count = sum(1 for t in ALL_TOPICS if role in t.get("roles", []))
    badge = ROLE_BADGE[role]
    st.sidebar.markdown(
        f'<span class="badge {badge}">{role}</span> **{count} topics**',
        unsafe_allow_html=True,
    )

st.sidebar.markdown("---")
st.sidebar.markdown("**📊 Topics by Difficulty**")
for d in DIFF_OPTIONS:
    count = sum(1 for t in ALL_TOPICS if t.get("difficulty") == d)
    cls = d.lower()
    st.sidebar.markdown(
        f'<span class="badge {cls}">{d}</span> **{count} topics**',
        unsafe_allow_html=True,
    )

st.sidebar.markdown("---")
st.sidebar.caption(
    f"{len(ALL_TOPICS)} topics · 4 roles · 4 levels · Python examples")


# ── FILTER ────────────────────────────────────────────────────────────────────
def topic_matches(t, q):
    q = q.lower()
    return any(
        q in (t.get(k) or "").lower()
        for k in ["title", "definition", "description", "example", "formula", "watch_out", "python_code"]
    ) or any(q in uc.lower() for uc in t.get("use_cases", []))


filtered = [
    t for t in ALL_TOPICS
    if any(r in role_filter for r in t.get("roles", []))
    and t.get("difficulty") in diff_filter
    and (not search or topic_matches(t, search))
]


# ── LEGEND ────────────────────────────────────────────────────────────────────
st.markdown("##### 🧑‍💼 Category I — Role")
leg1 = st.columns(4)
role_legend = [("Data Analyst", "analyst"), ("Analytics Engineer", "analytics_eng"),
               ("Data Engineer", "data_eng"), ("Data Scientist", "data_sci")]
for col, (label, cls) in zip(leg1, role_legend):
    col.markdown(
        f'<span class="badge {cls}">{label}</span>', unsafe_allow_html=True)

st.markdown("##### 📈 Category II — Difficulty")
leg2 = st.columns(4)
diff_legend = [("Foundational", "foundational"), ("Intermediate", "intermediate"),
               ("Advanced", "advanced"), ("Expert", "expert")]
for col, (label, cls) in zip(leg2, diff_legend):
    col.markdown(
        f'<span class="badge {cls}">{label}</span>', unsafe_allow_html=True)

st.markdown("---")


# ── RENDER ────────────────────────────────────────────────────────────────────
if not filtered:
    st.info("No topics found for the current filters. Try adjusting role, difficulty, or search.")
else:
    st.markdown(f"Showing **{len(filtered)}** of {len(ALL_TOPICS)} topics")
    st.markdown("")
    cols = st.columns(2)
    for i, topic in enumerate(filtered):
        with cols[i % 2]:
            with st.expander(f"**{topic['title']}**", expanded=False):
                render_topic(topic)

st.markdown("---")
st.caption(
    f"📊 Data & Statistics Cheat Sheet · {len(filtered)} topics shown · 🐍 Python examples included")

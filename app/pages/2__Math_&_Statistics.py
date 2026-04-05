import streamlit as st

from components import sidebar
from utility.seo import inject_seo

st.set_page_config(
    page_title="Data & Statistics Cheat Sheet",
    page_icon="📊",
    layout="wide",
)

inject_seo('Math & Statistics')

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

sidebar()

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
    {
        "title": "Percentages & Proportions",
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
        "title": "Rates of Change",
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
        "title": "Year-over-Year (YoY) Comparisons",
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
        "title": "Mean, Median, Mode",
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
        "title": "Range, Variance & Std. Deviation",
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
        "title": "Basic Probability",
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
        "title": "Frequency Distributions & Histograms",
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
        "title": "Data Types",
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
        "title": "Pareto Analysis (80/20 Rule)",
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
        "title": "SQL Window Functions for Analytics",
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
        "title": "Data Modeling — Star & Snowflake Schema",
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

    {
        "title": "Z-Scores & Normal Distribution",
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
        "title": "Correlation (Pearson & Spearman)",
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
        "title": "Hypothesis Testing & P-Values",
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
        "title": "Confidence Intervals",
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
        "title": "Sampling & Sampling Bias",
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
        "title": "Linear Regression & Coefficients",
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
        "title": "Conditional Probability & Bayes' Theorem",
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
        "title": "Cohort & Segmentation Analysis",
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
        "title": "Index Numbers & Weighted Averages",
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
        "title": "ETL / ELT Pipeline Concepts",
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
        "title": "Data Quality & Profiling",
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
        "title": "Multiple Regression",
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
        "title": "Time Series Analysis",
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
        "title": "A/B Testing & Experimental Design",
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
        "title": "Statistical Power & Sample Size",
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
        "title": "Survival / Retention Analysis",
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
        "title": "Simpson's Paradox & Statistical Pitfalls",
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
        "title": "Slowly Changing Dimensions (SCD)",
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

    {
        "title": "Entropy & Information Gain",
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
        "title": "Bias–Variance Tradeoff",
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
        "title": "Cross-Validation",
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
        "title": "Regularization (L1 & L2)",
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
        "title": "Gradient Descent",
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
        "title": "Confusion Matrix & Classification Metrics",
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
        "title": "Dimensionality Reduction (PCA, t-SNE, UMAP)",
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
        "title": "Loss Functions",
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
        "title": "Feature Engineering & Encoding",
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
        "title": "Class Imbalance Techniques",
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
        "title": "Bayesian vs Frequentist Statistics",
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
        "title": "Monte Carlo Simulation",
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
        "title": "Stream Processing Concepts",
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
        "title": "Graph Metrics & Network Analysis",
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
        "title": "Vector Embeddings & Similarity Search",
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

    {
        "title": "Cumulative Distribution Functions (CDF)",
        "roles": ["Data Analyst", "Data Scientist"],
        "difficulty": "Foundational",
        "definition": "The CDF gives the probability that a random variable X takes a value less than or equal to x: F(x) = P(X ≤ x).",
        "formula": "F(x) = P(X ≤ x)\n\nFor discrete: F(x) = Σ P(X = xᵢ) for all xᵢ ≤ x\nFor continuous: F(x) = ∫ f(t) dt from −∞ to x\n\nPercentile: x at which F(x) = p",
        "description": "The CDF answers: 'what fraction of observations fall below this value?' It's the cumulative version of the PDF/PMF. The inverse CDF (quantile function) answers: 'below what value do X% of observations fall?'",
        "example": "Page load times: CDF(2s) = 0.80 → 80% of users experience load times under 2 seconds. P90 = 3.5s means 90% of users load in under 3.5s.",
        "use_cases": ["SLA and percentile reporting (P50, P95, P99)", "Setting thresholds for alerting", "Comparing distributions visually", "Risk exceedance curves"],
        "watch_out": "CDFs look smooth but hide multi-modality. Always plot the PDF/histogram alongside the CDF to reveal shape.",
        "python_code": """\
import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(42)
load_times = rng.exponential(scale=1.5, size=10_000)

for p in [50, 75, 90, 95, 99]:
    print(f"P{p:2d}: {np.percentile(load_times, p):.3f}s")

pct_under_2s = (load_times < 2).mean() * 100
print(f"\\n% under 2s: {pct_under_2s:.1f}%")

fitted = stats.expon.fit(load_times, floc=0)
cdf_val = stats.expon.cdf(2.0, *fitted)
print(f"Theoretical CDF(2s): {cdf_val:.4f}")

ecdf_x = np.sort(load_times)
ecdf_y = np.arange(1, len(load_times) + 1) / len(load_times)
idx = np.searchsorted(ecdf_x, 2.0)
print(f"Empirical CDF(2s)  : {ecdf_y[idx]:.4f}")
""",
    },

    {
        "title": "Pivot Tables & Cross-tabulation",
        "roles": ["Data Analyst", "Analytics Engineer"],
        "difficulty": "Foundational",
        "definition": "A pivot table reshapes data from long to wide format, aggregating values at the intersection of row and column categories.",
        "formula": "Cell value = AGGREGATE(metric)\n  where row ∈ row_group AND col ∈ col_group\n\nChi-square test of independence:\n  χ² = Σ (O − E)² / E",
        "description": "Pivot tables are the analyst's workhorse for cross-dimensional summaries. Cross-tabulation counts occurrences at group intersections — the raw material for chi-square independence tests.",
        "example": "Rows = acquisition channel, Cols = subscription plan, Values = count of users → reveals which channel drives the highest-value plan.",
        "use_cases": ["Channel × plan conversion analysis", "Region × product revenue breakdowns", "Cohort × week retention heatmaps", "Survey response cross-tabs"],
        "watch_out": "Pivot tables hide sample sizes inside cells. A 100% conversion rate from 1 user is noise, not signal — always expose n.",
        "python_code": """\
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

rng = np.random.default_rng(42)
n = 2_000
df = pd.DataFrame({
    "channel": rng.choice(["organic","paid","referral"], n, p=[0.5,0.3,0.2]),
    "plan":    rng.choice(["free","pro","enterprise"], n, p=[0.65,0.25,0.10]),
    "revenue": rng.exponential(100, n),
})

pivot_count = pd.pivot_table(df, values="revenue", index="channel",
                              columns="plan", aggfunc="count", fill_value=0)
print("Count pivot:")
print(pivot_count)

pivot_rev = pd.pivot_table(df, values="revenue", index="channel",
                            columns="plan", aggfunc="mean").round(2)
print("\\nMean revenue pivot:")
print(pivot_rev)

ct = pd.crosstab(df["channel"], df["plan"])
chi2, p, dof, expected = chi2_contingency(ct)
print(f"\\nChi-square: {chi2:.3f}  p={p:.4f}  dof={dof}")
print("Channel and plan are NOT independent" if p < 0.05 else "No significant association")
""",
    },

    {
        "title": "Moving Averages (SMA, EMA, WMA)",
        "roles": ["Data Analyst", "Analytics Engineer"],
        "difficulty": "Foundational",
        "definition": "Moving averages smooth time series by averaging over a rolling window, suppressing noise to reveal underlying trends.",
        "formula": "SMA(k) = (1/k) × Σ yᵢ  [last k periods]\n\nEMA(t)  = α × y(t) + (1−α) × EMA(t−1)\n  where α = 2 / (k+1)\n\nWMA(k) = Σ(wᵢ × yᵢ) / Σwᵢ  [recent points heavier]",
        "description": "| Type | Lag | Responds To | Best For |\n|------|-----|-------------|----------|\n| SMA | High | Slow trend | Long-term smoothing |\n| EMA | Low | Recent changes | Reactive dashboards |\n| WMA | Medium | Weighted recency | Custom emphasis |",
        "example": "7-day SMA on daily revenue: weekend spikes disappear, underlying weekly growth trend becomes visible.",
        "use_cases": ["Daily KPI dashboards", "Trend line overlays", "Signal denoising", "Technical analysis (finance)"],
        "watch_out": "SMA introduces significant lag — it trails the actual series. EMA responds faster but is noisier. Choose window based on business cycle, not personal preference.",
        "python_code": """\
import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
dates = pd.date_range("2024-01-01", periods=90, freq="D")
revenue = pd.Series(
    np.linspace(100, 200, 90) + 30 * np.sin(np.arange(90) * 2 * np.pi / 7)
    + rng.normal(0, 10, 90),
    index=dates, name="revenue"
)

df = revenue.to_frame()
df["SMA_7"]  = revenue.rolling(7).mean()
df["SMA_14"] = revenue.rolling(14).mean()
df["EMA_7"]  = revenue.ewm(span=7, adjust=False).mean()

weights = np.arange(1, 8)
df["WMA_7"] = revenue.rolling(7).apply(
    lambda x: np.dot(x, weights) / weights.sum(), raw=True
)

print(df.tail(10).round(2))
print(f"\\nSMA lag vs EMA lag (last 7 days):")
print(f"  SMA vs raw: {(df['SMA_7'] - df['revenue']).tail(7).abs().mean():.2f}")
print(f"  EMA vs raw: {(df['EMA_7'] - df['revenue']).tail(7).abs().mean():.2f}")
""",
    },

    {
        "title": "Outlier Detection Methods",
        "roles": ["Data Analyst", "Data Scientist"],
        "difficulty": "Intermediate",
        "definition": "Systematic approaches to identifying observations that deviate significantly from expected patterns, either through statistical rules or machine learning.",
        "formula": "IQR Method:   outlier if x < Q1 − 1.5×IQR or x > Q3 + 1.5×IQR\nModified Z:   Mz = 0.6745 × (x − median) / MAD\n              outlier if |Mz| > 3.5\nIsolation Forest: anomaly score ≈ 2^(−E[h(x)]/c(n))",
        "description": "| Method | Assumption | Handles Multivariate? | Notes |\n|--------|------------|-----------------------|-------|\n| IQR | Symmetric | No | Simple, robust |\n| Z-score | Normal | No | Sensitive to extreme outliers |\n| Modified Z | Non-normal | No | Uses median/MAD |\n| Isolation Forest | None | Yes | ML-based, scalable |",
        "example": "Revenue column: IQR fence = [$0, $2,400]. Orders above $2,400 flagged for manual review — catches data entry errors and fraud.",
        "use_cases": ["Data quality checks in pipelines", "Fraud signal detection", "Sensor anomaly detection", "Pre-modeling data cleaning"],
        "watch_out": "Masking: one large outlier inflates the mean/std, making other outliers look normal. Always use robust statistics (median/MAD) first.",
        "python_code": """\
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import IsolationForest

rng = np.random.default_rng(42)
data = np.concatenate([rng.normal(100, 15, 200), [250, 280, -30, 500]])

def iqr_outliers(x):
    q1, q3 = np.percentile(x, [25, 75])
    iqr = q3 - q1
    return (x < q1 - 1.5*iqr) | (x > q3 + 1.5*iqr)

mad = np.median(np.abs(data - np.median(data)))
modified_z = 0.6745 * (data - np.median(data)) / mad

print(f"IQR outliers       : {iqr_outliers(data).sum()}")
print(f"Modified Z outliers: {(np.abs(modified_z) > 3.5).sum()}")
print(f"Z-score outliers   : {(np.abs(stats.zscore(data)) > 3).sum()}")

X = data.reshape(-1, 1)
iso = IsolationForest(contamination=0.02, random_state=42).fit(X)
iso_labels = iso.predict(X)
print(f"Isolation Forest   : {(iso_labels == -1).sum()} outliers")

df = pd.DataFrame({"value": data, "iqr": iqr_outliers(data),
                   "mod_z": np.abs(modified_z) > 3.5,
                   "iso_forest": iso_labels == -1})
print(df[df.any(axis=1)].head(10))
""",
    },

    {
        "title": "Statistical Process Control (SPC)",
        "roles": ["Data Analyst", "Analytics Engineer"],
        "difficulty": "Intermediate",
        "definition": "A method using control charts to monitor process stability over time, distinguishing natural variation (common cause) from unexpected shifts (special cause).",
        "formula": "X̄ chart (means):\n  UCL = X̄̄ + 3σ\n  LCL = X̄̄ − 3σ\n\nP chart (proportions):\n  UCL = p̄ + 3√(p̄(1−p̄)/n)\n  LCL = p̄ − 3√(p̄(1−p̄)/n)\n\nNelson Rule 1: Any point beyond ±3σ",
        "description": "**Nelson Rules (signal = special cause):**\n- Rule 1: 1 point beyond 3σ\n- Rule 2: 9 consecutive points same side of mean\n- Rule 3: 6 points in a row trending up or down\n- Rule 4: 14 alternating up/down\n\nControl limits ≠ specification limits. One is about process behavior; the other is about customer requirements.",
        "example": "Error rate control chart: UCL = 3.2%. Alert fires when three consecutive days exceed 2.5% (approaching UCL) — catch drift before it breaches.",
        "use_cases": ["Data pipeline error rate monitoring", "API latency control charts", "Product quality tracking", "Business metric anomaly detection"],
        "watch_out": "Recalculate control limits after confirmed process changes. Stale limits from old baselines will either over-alert or miss real shifts.",
        "python_code": """\
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n_days = 60
error_rate = pd.Series(
    np.concatenate([rng.normal(0.02, 0.003, 40),
                    rng.normal(0.035, 0.003, 20)]),  # shift at day 40
    name="error_rate"
)

mean_rate = error_rate[:30].mean()
std_rate  = error_rate[:30].std()
ucl = mean_rate + 3 * std_rate
lcl = max(0, mean_rate - 3 * std_rate)

print(f"Center line: {mean_rate:.4f}")
print(f"UCL: {ucl:.4f}  |  LCL: {lcl:.4f}")

violations = error_rate[error_rate > ucl]
print(f"\\nRule 1 violations (>{ucl:.4f}): {len(violations)} points")
print(violations)

run_above = (error_rate > mean_rate).rolling(9).sum() == 9
print(f"Rule 2 violations (9-in-a-row): {run_above.sum()} windows")

p_chart = pd.DataFrame({
    "day": range(n_days),
    "rate": error_rate,
    "ucl": ucl,
    "lcl": lcl,
    "violation": error_rate > ucl,
})
print(p_chart[p_chart["violation"]].head())
""",
    },

    {
        "title": "Logistic Regression",
        "roles": ["Data Scientist", "Data Analyst"],
        "difficulty": "Intermediate",
        "definition": "A classification model that predicts the probability of a binary outcome using the logistic (sigmoid) function, keeping predictions between 0 and 1.",
        "formula": "log(p / (1−p)) = β₀ + β₁X₁ + β₂X₂ + ...\n\np = 1 / (1 + e^(−(β₀ + β₁X)))\n\nOdds Ratio = e^β\nlog-likelihood: ℓ = Σ[y·log(p) + (1−y)·log(1−p)]",
        "description": "Logistic regression is the foundational binary classifier. The coefficients are in log-odds units — exponentiate to get interpretable odds ratios.\n\n- **Positive β**: feature increases probability of the positive class\n- **Odds Ratio > 1**: feature increases odds\n- **Pseudo-R²**: McFadden's R² = 1 − (ℓ_model / ℓ_null)",
        "example": "Churn model: β(last_login_days) = 0.05 → OR = 1.051 → each additional day since login increases churn odds by 5.1%.",
        "use_cases": ["Churn prediction", "Credit default scoring", "Medical diagnosis", "Lead conversion probability"],
        "watch_out": "Assumes linear relationship between log-odds and predictors. Check with calibration curves — a high AUC model can still be badly miscalibrated.",
        "python_code": """\
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm

rng = np.random.default_rng(42)
n = 2_000
df = pd.DataFrame({
    "days_since_login": rng.integers(0, 90, n).astype(float),
    "sessions_month":  rng.integers(0, 30, n).astype(float),
    "plan_pro":        rng.binomial(1, 0.3, n).astype(float),
})
df["churn"] = (
    (0.03 * df["days_since_login"]
     - 0.05 * df["sessions_month"]
     - 0.5 * df["plan_pro"]
     + rng.normal(0, 1, n)) > 0
).astype(int)

X = df.drop("churn", axis=1)
y = df["churn"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

sc = StandardScaler()
X_tr_s = sc.fit_transform(X_tr)
X_te_s  = sc.transform(X_te)

clf = LogisticRegression(max_iter=1_000)
clf.fit(X_tr_s, y_tr)
print(classification_report(y_te, clf.predict(X_te_s)))
print(f"AUC-ROC: {roc_auc_score(y_te, clf.predict_proba(X_te_s)[:,1]):.4f}")

X_sm = sm.add_constant(X_tr_s)
logit = sm.Logit(y_tr, X_sm).fit(disp=0)
odds_ratios = np.exp(logit.params)
print("\\nOdds ratios:"); print(odds_ratios.round(4))
""",
    },

    {
        "title": "TF-IDF & Text Vectorization",
        "roles": ["Data Scientist"],
        "difficulty": "Intermediate",
        "definition": "TF-IDF (Term Frequency–Inverse Document Frequency) weights terms by how often they appear in a document relative to how common they are across all documents.",
        "formula": "TF(t,d)  = count(t in d) / total terms in d\nIDF(t)   = log(N / df(t))\nTF-IDF   = TF × IDF\n\nN   = total documents\ndf(t) = documents containing term t",
        "description": "- **High TF-IDF**: term is frequent in this document but rare across the corpus — informative\n- **Low TF-IDF**: term is either rare in the doc or common everywhere (e.g., 'the', 'is') — uninformative\n\n**Pipeline:** Tokenize → remove stopwords → stem/lemmatize → vectorize → optional SVD/LSA reduction.",
        "example": "Document about Python: 'python' has high TF-IDF; 'the' has near-zero IDF (appears everywhere).",
        "use_cases": ["Document classification", "Search relevance ranking", "Duplicate document detection", "Feature extraction for NLP models"],
        "watch_out": "TF-IDF ignores word order and semantics. 'not good' and 'good' look similar. Use sentence transformers for semantic meaning.",
        "python_code": """\
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

docs = [
    "python data analysis pandas numpy statistics",
    "machine learning python scikit-learn model training",
    "sql database query analytics warehouse bigquery",
    "python machine learning deep learning neural network",
    "data warehouse etl pipeline ingestion analytics",
]

tfidf = TfidfVectorizer(ngram_range=(1,2), max_features=20, stop_words="english")
matrix = tfidf.fit_transform(docs)
df = pd.DataFrame(matrix.toarray().round(3),
                  columns=tfidf.get_feature_names_out())
print("TF-IDF matrix (top terms):")
print(df.iloc[:, :8])

sim = cosine_similarity(matrix)
print("\\nDocument similarity matrix:")
print(pd.DataFrame(sim.round(3)).to_string())

query = tfidf.transform(["python analytics pipeline"])
scores = cosine_similarity(query, matrix)[0]
ranked = sorted(enumerate(scores), key=lambda x: -x[1])
print("\\nQuery 'python analytics pipeline' → ranked results:")
for idx, score in ranked:
    print(f"  Doc {idx}: {score:.4f} | {docs[idx][:50]}")
""",
    },

    {
        "title": "SQL Query Optimization for Analytics",
        "roles": ["Analytics Engineer", "Data Engineer"],
        "difficulty": "Intermediate",
        "definition": "Techniques for reducing query execution time and cost in analytical databases by understanding how query planners process SQL.",
        "formula": "Cost ≈ rows_scanned × bytes_per_row × CPU_factor\n\nPartition pruning: scans 1 of N partitions\nClustering benefit: scans 1/k of micro-partitions",
        "description": "**Key principles:**\n- **Filter early**: push WHERE clauses as far upstream as possible\n- **Avoid SELECT \\***: read only needed columns (columnar storage)\n- **Partition pruning**: filter on partition keys (date) to skip entire partitions\n- **CTEs vs subqueries**: CTEs materialize in some engines — benchmark both\n- **Avoid functions on indexed columns**: WHERE DATE(created_at) = today breaks partition pruning",
        "example": "Replacing `SELECT *` with named columns on a 10-column table in BigQuery reduces bytes billed by 80% if only 2 columns are needed.",
        "use_cases": ["Cost optimization in BigQuery/Snowflake/Redshift", "dbt model performance", "Dashboard query acceleration", "Large-scale ETL efficiency"],
        "watch_out": "EXPLAIN / EXPLAIN ANALYZE is your best friend. Never optimize without measuring — the query planner often surprises you.",
        "python_code": """\
# Illustrative patterns — run in your actual SQL engine with EXPLAIN

bad_patterns = {
    "full_scan":       "SELECT * FROM orders",
    "no_partition":    "SELECT * FROM orders WHERE DATE(created_at) = '2024-01-01'",
    "correlated_sub":  "SELECT * FROM users u WHERE (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) > 5",
    "implicit_cast":   "SELECT * FROM events WHERE user_id = 12345",  # if user_id is VARCHAR
}

good_patterns = {
    "column_pruning":  "SELECT order_id, user_id, revenue FROM orders",
    "partition_key":   "SELECT * FROM orders WHERE created_at >= '2024-01-01' AND created_at < '2024-01-02'",
    "join_approach":   "SELECT u.* FROM users u JOIN (SELECT DISTINCT user_id FROM orders GROUP BY user_id HAVING COUNT(*) > 5) o ON u.id = o.user_id",
    "explicit_cast":   "SELECT * FROM events WHERE user_id = '12345'",
}

import pandas as pd
comparison = pd.DataFrame({
    "anti_pattern": list(bad_patterns.keys()),
    "preferred":    list(good_patterns.keys()),
    "why_it_matters": [
        "Columnar DBs charge per byte read — only read needed cols",
        "Function on column prevents partition pruning, full table scan",
        "Executes subquery once per outer row — O(n²) cost",
        "Implicit cast disables index/clustering benefit",
    ]
})
print(comparison.to_string(index=False))
""",
    },

    {
        "title": "Clustering Algorithms (K-Means, DBSCAN, Hierarchical)",
        "roles": ["Data Scientist"],
        "difficulty": "Advanced",
        "definition": "Unsupervised methods that group observations into clusters based on similarity, without pre-defined labels.",
        "formula": "K-Means objective:\n  minimize Σ Σ ||xᵢ − μk||²\n\nDBSCAN:\n  core point if |N_ε(x)| ≥ min_pts\n  N_ε(x) = {y : dist(x,y) ≤ ε}\n\nElbow: find k where inertia drop levels off\nSilhouette: s(i) = (b−a) / max(a,b)",
        "description": "| Algorithm | Shape | Outliers | k needed | Notes |\n|-----------|-------|----------|----------|-------|\n| K-Means | Spherical | Sensitive | Yes | Fast, scalable |\n| DBSCAN | Arbitrary | Robust | No | Finds noise points |\n| Hierarchical | Any | Moderate | No | Dendrogram output |",
        "example": "RFM customer segmentation: K-Means with k=4 → Champions, At-Risk, Lost, New — each needs a different marketing strategy.",
        "use_cases": ["Customer segmentation", "Anomaly detection (DBSCAN)", "Document grouping", "Image compression"],
        "watch_out": "K-Means assumes spherical, equal-size clusters. Normalize features first — otherwise high-magnitude features dominate distance calculations.",
        "python_code": """\
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.datasets import make_blobs

X, _ = make_blobs(n_samples=500, centers=4, cluster_std=0.8, random_state=42)
X_s  = StandardScaler().fit_transform(X)

# Elbow method
inertias = [KMeans(n_clusters=k, random_state=42, n_init=10).fit(X_s).inertia_
            for k in range(2, 9)]
print("Inertias k=2..8:", [f"{v:.0f}" for v in inertias])

km = KMeans(n_clusters=4, random_state=42, n_init=10).fit(X_s)
print(f"K-Means silhouette: {silhouette_score(X_s, km.labels_):.4f}")

db = DBSCAN(eps=0.4, min_samples=5).fit(X_s)
n_clusters = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
noise      = (db.labels_ == -1).sum()
print(f"DBSCAN: {n_clusters} clusters, {noise} noise points")

hc = AgglomerativeClustering(n_clusters=4).fit(X_s)
print(f"Hierarchical silhouette: {silhouette_score(X_s, hc.labels_):.4f}")
""",
    },

    {
        "title": "Causal Inference & Difference-in-Differences",
        "roles": ["Data Analyst", "Data Scientist"],
        "difficulty": "Advanced",
        "definition": "Methods for estimating causal effects from observational data where true randomization was not possible.",
        "formula": "DiD Estimator:\n  τ = (Ȳ_treat,post − Ȳ_treat,pre)\n    − (Ȳ_ctrl,post − Ȳ_ctrl,pre)\n\nRegression form:\n  Y = β₀ + β₁·Treat + β₂·Post + β₃·(Treat×Post) + ε\n  τ = β₃",
        "description": "**Causal toolkit:**\n- **DiD**: parallel trends assumption — control group shows what would have happened\n- **RDD**: exploit arbitrary threshold cutoffs\n- **IV**: instrument variable correlated with treatment but not outcome directly\n- **PSM**: propensity score matching to balance treatment/control\n\n**Parallel trends**: the treatment and control groups would have followed the same trend absent the intervention.",
        "example": "Feature rolled out to Region A (treatment). Region B is control. DiD removes seasonal trends common to both — isolates the feature's true causal effect.",
        "use_cases": ["Evaluating non-randomized product rollouts", "Policy impact analysis", "Marketing channel attribution", "Pricing experiment analysis"],
        "watch_out": "DiD requires the parallel trends assumption — test it visually with pre-period data. Violation makes the estimate biased.",
        "python_code": """\
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

rng = np.random.default_rng(42)
n = 400

df = pd.DataFrame({
    "unit_id":   np.tile(range(n // 2), 2),
    "period":    np.repeat(["pre","post"], n // 2),
    "treated":   np.tile(rng.binomial(1, 0.5, n // 2), 2),
})
df["post"]  = (df["period"] == "post").astype(int)
df["trend"] = rng.normal(0, 5, n)
true_effect = 15
df["outcome"] = (
    50
    + 5 * df["treated"]        # baseline difference
    + 8 * df["post"]           # time trend
    + true_effect * df["treated"] * df["post"]  # treatment effect
    + df["trend"]
)

model = smf.ols("outcome ~ treated * post", data=df).fit()
print(model.summary().tables[1])
print(f"\\nTrue causal effect  : {true_effect}")
print(f"DiD estimate (β₃)  : {model.params['treated:post']:.3f}")
print(f"95% CI             : [{model.conf_int().loc['treated:post',0]:.3f}, {model.conf_int().loc['treated:post',1]:.3f}]")
""",
    },

    {
        "title": "Ensemble Methods (Bagging & Boosting)",
        "roles": ["Data Scientist"],
        "difficulty": "Advanced",
        "definition": "Ensemble methods combine multiple weak learners into a stronger predictor. Bagging trains models in parallel on bootstrap samples; boosting trains sequentially, each correcting the last.",
        "formula": "Bagging prediction: ŷ = (1/B) × Σ f_b(x)\n\nBoosting (AdaBoost):\n  F_m(x) = F_{m-1}(x) + α_m × h_m(x)\n  where h_m focuses on previously misclassified points\n\nGBM gradient step:\n  F_m(x) = F_{m-1}(x) − γ × ∇L(F_{m-1})",
        "description": "| Method | Reduces | Sequential? | Key Param |\n|--------|---------|-------------|----------|\n| Bagging / RF | Variance | No | n_estimators, max_features |\n| AdaBoost | Bias+Variance | Yes | n_estimators, learning_rate |\n| Gradient Boosting | Bias | Yes | n_estimators, max_depth, learning_rate |\n| XGBoost/LightGBM | Both | Yes | same + reg_lambda |",
        "example": "Single decision tree: 75% accuracy. Random Forest (100 trees): 89%. XGBoost: 92% — each corrects remaining error.",
        "use_cases": ["Tabular data prediction (XGBoost/LightGBM dominate Kaggle)", "Feature importance ranking", "Fraud detection", "Churn and LTV prediction"],
        "watch_out": "Boosting is prone to overfitting if learning rate is too high or trees too deep. Always tune with early stopping on a validation set.",
        "python_code": """\
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import (RandomForestClassifier, AdaBoostClassifier,
                               GradientBoostingClassifier, BaggingClassifier)
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score

X, y = make_classification(n_samples=2_000, n_features=20, n_informative=10,
                            random_state=42)

models = {
    "Single Tree":    DecisionTreeClassifier(max_depth=5, random_state=42),
    "Bagging":        BaggingClassifier(n_estimators=50, random_state=42),
    "Random Forest":  RandomForestClassifier(n_estimators=100, random_state=42),
    "AdaBoost":       AdaBoostClassifier(n_estimators=100, learning_rate=0.1, random_state=42),
    "Gradient Boost": GradientBoostingClassifier(n_estimators=100, max_depth=3,
                                                  learning_rate=0.1, random_state=42),
}
for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=5, scoring="roc_auc")
    print(f"{name:18s}  AUC = {scores.mean():.4f} ± {scores.std():.4f}")

rf = RandomForestClassifier(n_estimators=100, random_state=42).fit(X, y)
importances = sorted(zip(range(20), rf.feature_importances_),
                     key=lambda x: -x[1])[:5]
print("\\nTop 5 features (Random Forest):")
for feat, imp in importances:
    print(f"  feature_{feat}: {imp:.4f}")
""",
    },

    {
        "title": "Forecasting — Exponential Smoothing & Prophet",
        "roles": ["Data Analyst", "Data Scientist"],
        "difficulty": "Advanced",
        "definition": "Exponential smoothing models weight recent observations more heavily using a decay factor. Prophet decomposes time series into trend + seasonality + holidays using an additive model.",
        "formula": "Simple ES:  S_t = α·y_t + (1−α)·S_{t−1}\n  α ∈ (0,1) — smoothing parameter\n\nHolt-Winters (additive):\n  Level:    L_t = α(y_t − S_{t−m}) + (1−α)(L_{t−1}+T_{t−1})\n  Trend:    T_t = β(L_t − L_{t−1}) + (1−β)T_{t−1}\n  Seasonal: S_t = γ(y_t − L_t) + (1−γ)S_{t−m}\n  Forecast: ŷ_{t+h} = L_t + h·T_t + S_{t+h−m}",
        "description": "| Model | Handles Trend | Handles Seasonality | Notes |\n|-------|--------------|---------------------|-------|\n| SES | No | No | Simplest |\n| Holt | Yes | No | Double ES |\n| Holt-Winters | Yes | Yes | Triple ES |\n| Prophet | Yes | Multi-period | Handles holidays, missing data |",
        "example": "E-commerce weekly revenue: Holt-Winters captures the upward trend AND December spikes. Prophet additionally handles Black Friday anomalies.",
        "use_cases": ["Demand planning", "Revenue forecasting dashboards", "Inventory optimization", "Capacity planning"],
        "watch_out": "Forecasting uncertainty compounds: a 6-month forecast is far wider than a 1-month forecast. Always communicate prediction intervals, not point estimates.",
        "python_code": """\
import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX

rng = np.random.default_rng(42)
dates = pd.date_range("2022-01", periods=104, freq="W")
trend    = np.linspace(100, 250, 104)
seasonal = 30 * np.sin(2 * np.pi * np.arange(104) / 52)
series   = pd.Series(trend + seasonal + rng.normal(0, 8, 104), index=dates)

train, test = series[:-12], series[-12:]

hw = ExponentialSmoothing(train, trend="add", seasonal="add",
                          seasonal_periods=52).fit()
hw_forecast = hw.forecast(12)
hw_mae = np.abs(test - hw_forecast).mean()
print(f"Holt-Winters MAE: {hw_mae:.2f}")

sarima = SARIMAX(train, order=(1,1,1), seasonal_order=(1,1,1,52)).fit(disp=False)
sarima_fc = sarima.forecast(12)
sarima_mae = np.abs(test - sarima_fc).mean()
print(f"SARIMA MAE      : {sarima_mae:.2f}")

print("\\nHolt-Winters 12-week forecast:")
print(hw_forecast.round(2).to_string())

# Prophet usage (requires: pip install prophet)
# from prophet import Prophet
# df_p = series.reset_index().rename(columns={"index":"ds", 0:"y"})
# m = Prophet(yearly_seasonality=True).fit(df_p[:-12])
# future = m.make_future_dataframe(periods=12, freq="W")
# forecast = m.predict(future)
""",
    },

    {
        "title": "Data Contracts & Observability SLAs",
        "roles": ["Data Engineer", "Analytics Engineer"],
        "difficulty": "Advanced",
        "definition": "A data contract is a formal, versioned agreement between data producers and consumers specifying schema, semantics, quality guarantees, and SLAs.",
        "formula": "Freshness SLA  : max(current_time − max(updated_at)) < threshold\nVolume SLA     : |row_count − expected_rows| / expected_rows < tolerance\nSchema SLA     : all required columns present with correct dtype\nNull SLA       : null_rate < max_null_rate per column",
        "description": "**Contract components:**\n- Schema: column names, types, required/optional\n- Semantics: what each field means (not just its type)\n- Quality: null rates, value ranges, uniqueness rules\n- SLAs: freshness, volume, availability\n- Ownership: team, on-call contact, escalation path\n\n**Observability triad:** Freshness, Volume, Schema.",
        "example": "Contract for `fact_orders`: `order_id` must be unique, non-null; `revenue` > 0; updated daily by 06:00 UTC; row count within ±10% of prior 7-day average.",
        "use_cases": ["Data mesh governance", "dbt contract testing", "Incident SLA alerting", "Cross-team data sharing agreements"],
        "watch_out": "Contracts without enforcement are documentation, not contracts. Automate checks in CI/CD and alert on breach before downstream consumers notice.",
        "python_code": """\
import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ColumnContract:
    name: str
    dtype: str
    nullable: bool = False
    unique: bool = False
    min_val: Optional[float] = None
    max_val: Optional[float] = None
    max_null_rate: float = 0.0

@dataclass
class TableContract:
    table_name: str
    columns: list
    freshness_hours: float = 24.0
    volume_tolerance: float = 0.15

def validate(df: pd.DataFrame, contract: TableContract) -> dict:
    results = {}
    for col in contract.columns:
        c = col
        if c.name not in df.columns:
            results[c.name] = "MISSING COLUMN"
            continue
        issues = []
        null_rate = df[c.name].isna().mean()
        if null_rate > c.max_null_rate:
            issues.append(f"null_rate={null_rate:.3f} > {c.max_null_rate}")
        if c.unique and df[c.name].duplicated().any():
            issues.append("uniqueness violated")
        if c.min_val is not None and (df[c.name] < c.min_val).any():
            issues.append(f"values below min={c.min_val}")
        results[c.name] = "PASS" if not issues else " | ".join(issues)
    return results

contract = TableContract("fact_orders", columns=[
    ColumnContract("order_id", "int64", nullable=False, unique=True),
    ColumnContract("revenue",  "float64", nullable=False, min_val=0.0),
    ColumnContract("country",  "object", nullable=True, max_null_rate=0.05),
])
rng = np.random.default_rng(42)
df = pd.DataFrame({
    "order_id": [1, 2, 2, 4],   # duplicate!
    "revenue":  [100.0, -5.0, 200.0, 300.0],   # negative!
    "country":  ["PH", None, "US", "SG"],
})
print(validate(df, contract))
""",
    },

    {
        "title": "Recommendation Systems (Collaborative Filtering & Matrix Factorization)",
        "roles": ["Data Scientist", "Data Engineer"],
        "difficulty": "Expert",
        "definition": "Algorithms that predict a user's preference for items based on behavioral patterns, either from similar users (collaborative) or item features (content-based).",
        "formula": "User-User CF similarity:\n  sim(u,v) = (rᵤ · rᵥ) / (|rᵤ| × |rᵥ|)  [cosine]\n\nMatrix Factorization (SVD):\n  R ≈ U × Σ × Vᵀ\n  r̂(u,i) = μ + bᵤ + bᵢ + qᵢᵀ · pᵤ\n\nImplicit ALS minimizes:\n  Σ cᵤᵢ(pᵤᵀ qᵢ − rᵤᵢ)² + λ(||pᵤ||² + ||qᵢ||²)",
        "description": "| Method | Data Needed | Cold Start | Scalability |\n|--------|-------------|------------|-------------|\n| User-User CF | Ratings | Poor | Low (O(n²)) |\n| Item-Item CF | Ratings | Medium | Medium |\n| Matrix Factorization | Ratings | Poor | High |\n| ALS (implicit) | Interactions | Poor | High |\n| Two-tower neural | Features | Good | High |",
        "example": "Netflix: user-item interaction matrix factorized into 50-dim latent factors. dot(user_vector, item_vector) → predicted rating.",
        "use_cases": ["E-commerce product recommendations", "Content feed ranking", "Playlist generation", "Cross-sell/upsell engines"],
        "watch_out": "Cold start problem: new users/items have no interaction history. Hybrid approaches combine collaborative + content features.",
        "python_code": """\
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from scipy.sparse import csr_matrix

rng = np.random.default_rng(42)
n_users, n_items = 100, 50
ratings_dense = rng.integers(0, 6, (n_users, n_items)).astype(float)
ratings_dense[ratings_dense < 3] = 0   # sparse: many zeros = no interaction
R = csr_matrix(ratings_dense)

# Item-item collaborative filtering
item_sim = cosine_similarity(R.T)
np.fill_diagonal(item_sim, 0)
top3_for_item0 = np.argsort(item_sim[0])[::-1][:3]
print(f"Items most similar to item_0: {top3_for_item0}")

# Matrix factorization via SVD
svd = TruncatedSVD(n_components=10, random_state=42)
user_factors = svd.fit_transform(R)
item_factors = svd.components_.T
print(f"User factors shape: {user_factors.shape}")
print(f"Explained variance: {svd.explained_variance_ratio_.sum():.3f}")

# Predict ratings for user 0
predicted_ratings = user_factors[0] @ item_factors.T
top5_items = np.argsort(predicted_ratings)[::-1][:5]
print(f"Top 5 recommended items for user_0: {top5_items}")

# RMSE on observed entries
mask = ratings_dense > 0
R_approx = user_factors @ item_factors.T
rmse = np.sqrt(((ratings_dense[mask] - R_approx[mask])**2).mean())
print(f"SVD reconstruction RMSE: {rmse:.4f}")
""",
    },

    {
        "title": "Uplift Modeling & Heterogeneous Treatment Effects",
        "roles": ["Data Scientist"],
        "difficulty": "Expert",
        "definition": "Uplift modeling predicts the incremental causal effect of a treatment on an individual, targeting those for whom treatment makes a meaningful difference (true positives).",
        "formula": "Uplift = P(Y=1 | T=1, X=x) − P(Y=1 | T=0, X=x)\n\nQINI coefficient (area between uplift and random):\n  Q = ∫ [U(φ) − random] dφ\n\nTwo-model approach:\n  uplift(x) = model_treat.predict(x) − model_ctrl.predict(x)",
        "description": "**The four segments:**\n- **Persuadables**: respond only to treatment — target these\n- **Sure Things**: convert regardless — wasted spend\n- **Lost Causes**: won't convert either way — ignore\n- **Do Not Disturb**: treatment has negative effect — actively avoid",
        "example": "Email campaign: targeting top decile by uplift score vs. top decile by propensity score doubles incremental revenue for the same send volume.",
        "use_cases": ["Targeted marketing campaigns", "Clinical trial subgroup analysis", "Retention intervention targeting", "Pricing personalization"],
        "watch_out": "Uplift models require randomized training data (treatment must be randomly assigned). Observational data requires causal adjustment first.",
        "python_code": """\
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

rng = np.random.default_rng(42)
n = 5_000
X = rng.normal(0, 1, (n, 5))
treatment = rng.binomial(1, 0.5, n)

# Heterogeneous treatment effects: feature X[:,0] determines who responds
base_prob  = 0.1 + 0.05 * X[:, 1]
treat_prob = base_prob + np.where(X[:, 0] > 0, 0.15, 0.02)  # responders if X0 > 0
prob       = np.where(treatment == 1, treat_prob, base_prob)
prob       = np.clip(prob, 0, 1)
outcome    = rng.binomial(1, prob, n)

df = pd.DataFrame(X, columns=[f"x{i}" for i in range(5)])
df["treatment"] = treatment
df["outcome"]   = outcome

X_tr, X_te, y_tr, y_te = train_test_split(df, df.index, test_size=0.2, random_state=42)
feat_cols = [c for c in df.columns if c.startswith("x")]

treated_mask = X_tr["treatment"] == 1
ctrl_mask    = X_tr["treatment"] == 0

m_treat = LogisticRegression(max_iter=500).fit(X_tr.loc[treated_mask, feat_cols], X_tr.loc[treated_mask, "outcome"])
m_ctrl  = LogisticRegression(max_iter=500).fit(X_tr.loc[ctrl_mask,   feat_cols], X_tr.loc[ctrl_mask,   "outcome"])

uplift_score = (m_treat.predict_proba(X_te[feat_cols])[:, 1]
                - m_ctrl.predict_proba(X_te[feat_cols])[:, 1])

X_te = X_te.copy()
X_te["uplift"] = uplift_score
top_decile = X_te.nlargest(int(0.1 * len(X_te)), "uplift")
random_decile = X_te.sample(frac=0.1, random_state=42)

print(f"Top decile conversion rate  : {top_decile['outcome'].mean():.4f}")
print(f"Random decile conversion    : {random_decile['outcome'].mean():.4f}")
print(f"Incremental lift            : {top_decile['outcome'].mean() - random_decile['outcome'].mean():.4f}")
""",
    },

    {
        "title": "Online Learning & Multi-Armed Bandit Algorithms",
        "roles": ["Data Scientist", "Data Engineer"],
        "difficulty": "Expert",
        "definition": "Online learning updates models incrementally as new data arrives. Bandits balance exploring new options against exploiting known good ones — formalizing the explore/exploit tradeoff.",
        "formula": "ε-Greedy:\n  exploit (best arm) with prob 1−ε\n  explore (random arm) with prob ε\n\nUCB1:\n  score(a) = μ̂(a) + √(2·ln(N) / n(a))\n  N = total pulls, n(a) = pulls of arm a\n\nThompson Sampling:\n  θ(a) ~ Beta(α_a, β_a)\n  play argmax θ(a)",
        "description": "| Algorithm | Exploration | Regret | Use When |\n|-----------|-------------|--------|----------|\n| ε-Greedy | Fixed random | O(√T) | Simple baseline |\n| UCB1 | Uncertainty-based | O(log T) | Known horizon |\n| Thompson Sampling | Bayesian posterior | O(log T) | Best practical performance |",
        "example": "Auto-optimizing A/B test: Thompson Sampling allocates more traffic to winning variants as evidence accumulates — reducing regret vs. fixed 50/50.",
        "use_cases": ["Adaptive A/B testing", "Ad serving optimization", "Recommendation exploration", "Clinical trial adaptive design"],
        "watch_out": "Bandits assume stationarity — arm quality doesn't change over time. Use contextual bandits (LinUCB) or sliding-window approaches for non-stationary rewards.",
        "python_code": """\
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
true_rates = [0.04, 0.07, 0.05, 0.06]  # true conversion rates per variant
n_arms = len(true_rates)
n_steps = 10_000

# Thompson Sampling
alpha = np.ones(n_arms)
beta  = np.ones(n_arms)
ts_rewards = []
ts_choices = []

for t in range(n_steps):
    theta  = rng.beta(alpha, beta)
    arm    = np.argmax(theta)
    reward = rng.binomial(1, true_rates[arm])
    alpha[arm] += reward
    beta[arm]  += 1 - reward
    ts_rewards.append(reward)
    ts_choices.append(arm)

ts_rewards = np.array(ts_rewards)
ts_choices = np.array(ts_choices)
print("Thompson Sampling results:")
for arm in range(n_arms):
    mask = ts_choices == arm
    chosen_pct = mask.mean() * 100
    obs_rate   = ts_rewards[mask].mean() if mask.sum() > 0 else 0
    print(f"  Arm {arm} (true={true_rates[arm]:.2f}): chosen {chosen_pct:.1f}% | obs_rate={obs_rate:.4f}")

best_arm_rate = max(true_rates)
regret = best_arm_rate * n_steps - ts_rewards.sum()
print(f"\\nCumulative regret: {regret:.0f} (vs optimal {best_arm_rate * n_steps:.0f})")

# UCB1 for comparison
counts  = np.zeros(n_arms)
sums    = np.zeros(n_arms)
ucb_rew = 0
for t in range(1, n_steps + 1):
    if t <= n_arms:
        arm = t - 1
    else:
        ucb = sums / counts + np.sqrt(2 * np.log(t) / counts)
        arm = np.argmax(ucb)
    reward = rng.binomial(1, true_rates[arm])
    counts[arm] += 1
    sums[arm]   += reward
    ucb_rew     += reward

print(f"UCB1 total reward      : {ucb_rew}")
print(f"Thompson total reward  : {ts_rewards.sum()}")
""",
    },
    {
        "title": "Percentiles & Quantiles",
        "roles": ["Data Analyst", "Data Scientist"],
        "difficulty": "Foundational",
        "definition": "A percentile indicates the value below which a given percentage of observations fall. Quantiles divide a distribution into equal-sized intervals.",
        "formula": "P_k = value at which k% of data falls below\n\nQuartiles: Q1=P25, Q2=P50 (median), Q3=P75\nIQR = Q3 − Q1\nDeciles: P10, P20, ..., P90\nNTILE(n): SQL function dividing rows into n buckets",
        "description": "Percentiles are more robust than means for skewed distributions. P50 (median) is the central value. P95 and P99 capture tail behavior — critical for SLA monitoring and outlier analysis.",
        "example": "User session times: P50=2min, P95=12min, P99=45min. The average (5min) misrepresents most users — P50 is more honest.",
        "use_cases": ["SLA threshold setting (P95, P99 latency)", "Salary band benchmarking", "Revenue decile segmentation", "Test score norming"],
        "watch_out": "Interpolation method matters for small samples. Pandas, NumPy, and SQL engines use slightly different interpolation — results can differ.",
        "python_code": """\
import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(42)
sessions = rng.exponential(scale=3, size=10_000)

for p in [25, 50, 75, 90, 95, 99]:
    print(f"P{p:2d}: {np.percentile(sessions, p):.3f} min")

s = pd.Series(sessions)
print("\\nDescribe:")
print(s.describe(percentiles=[.25,.5,.75,.9,.95,.99]).round(3))

df = pd.DataFrame({"user_id": range(1000),
                   "revenue": rng.exponential(200, 1000)})
df["decile"] = pd.qcut(df["revenue"], q=10, labels=False) + 1
print("\\nMean revenue by decile:")
print(df.groupby("decile")["revenue"].mean().round(2))
""",
    },

    {
        "title": "Null Handling & Imputation Strategies",
        "roles": ["Data Analyst", "Analytics Engineer", "Data Scientist"],
        "difficulty": "Foundational",
        "definition": "Nulls represent missing, unknown, or inapplicable values. Imputation fills them with estimated values to enable analysis and modeling.",
        "formula": "Mean imputation:   x̂ = μ\nMedian imputation: x̂ = median\nKNN imputation:    x̂ = weighted avg of k nearest neighbors\nMICE:              iterative multivariate regression imputation",
        "description": "**Types of missingness:**\n- **MCAR** (Missing Completely At Random): safe to drop\n- **MAR** (Missing At Random): depends on observed data → impute\n- **MNAR** (Missing Not At Random): systematic → investigate root cause\n\nAlways ask *why* the value is missing before deciding how to handle it.",
        "example": "Revenue is null for free-plan users → MNAR, not random. Replacing with 0 is correct; replacing with mean would be wrong.",
        "use_cases": ["Pre-modeling data prep", "Survey analysis", "Pipeline data cleaning", "Feature engineering"],
        "watch_out": "Mean imputation reduces variance and distorts correlations. For ML, prefer KNN or model-based imputation. For reporting, flag imputed values explicitly.",
        "python_code": """\
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.experimental import enable_iterative_imputer  # noqa
from sklearn.impute import IterativeImputer

rng = np.random.default_rng(42)
df = pd.DataFrame({
    "age":     rng.integers(18, 65, 200).astype(float),
    "income":  rng.exponential(50_000, 200),
    "score":   rng.normal(70, 15, 200),
})
df.loc[rng.choice(200, 30, replace=False), "age"]    = np.nan
df.loc[rng.choice(200, 40, replace=False), "income"] = np.nan

print("Missing rate:")
print((df.isna().mean() * 100).round(2))

mean_imp = SimpleImputer(strategy="mean")
median_imp = SimpleImputer(strategy="median")
knn_imp  = KNNImputer(n_neighbors=5)
mice_imp = IterativeImputer(random_state=42, max_iter=10)

results = {}
for name, imp in [("mean", mean_imp), ("median", median_imp),
                  ("knn", knn_imp), ("mice", mice_imp)]:
    filled = pd.DataFrame(imp.fit_transform(df), columns=df.columns)
    results[name] = filled["income"].std()

print("\\nIncome std dev after imputation (original:", df["income"].std().round(2), ")")
for name, std in results.items():
    print(f"  {name:8s}: {std:.2f}")
""",
    },

    {
        "title": "Data Joins — Types & Pitfalls",
        "roles": ["Data Analyst", "Analytics Engineer", "Data Engineer"],
        "difficulty": "Foundational",
        "definition": "Joins combine rows from two or more tables based on a related column. The join type determines which rows appear in the result.",
        "formula": "INNER JOIN  : only matching rows in both tables\nLEFT JOIN   : all left rows + matching right (null if no match)\nRIGHT JOIN  : all right rows + matching left\nFULL OUTER  : all rows from both, null where no match\nCROSS JOIN  : every row × every row (Cartesian product)\nSELF JOIN   : table joined to itself",
        "description": "**Fan-out trap**: joining on a non-unique key causes row multiplication. One-to-many becomes many-to-many if both sides have duplicates.\n\n**Rule of thumb**: always check row counts before and after joins during development.",
        "example": "orders (500 rows) LEFT JOIN customers → still 500 rows if customer_id is unique in customers. If customers has duplicates on customer_id → fan-out to 600+ rows.",
        "use_cases": ["Fact-dimension joins in data warehouse", "Pipeline data enrichment", "Deduplication diagnosis", "Attribution joining"],
        "watch_out": "INNER JOIN silently drops unmatched rows. Use LEFT JOIN + WHERE right.key IS NULL to find orphan records before deciding to drop them.",
        "python_code": """\
import pandas as pd
import numpy as np

orders = pd.DataFrame({
    "order_id":    [1, 2, 3, 4, 5],
    "customer_id": [101, 102, 103, 101, 999],
    "amount":      [50, 80, 30, 120, 200],
})
customers = pd.DataFrame({
    "customer_id": [101, 102, 103],
    "name":        ["Alice", "Bob", "Carol"],
})

inner = orders.merge(customers, on="customer_id", how="inner")
left  = orders.merge(customers, on="customer_id", how="left")
print(f"Original orders : {len(orders)}")
print(f"INNER JOIN      : {len(inner)}  (order 999 dropped)")
print(f"LEFT JOIN       : {len(left)}   (order 999 kept, name=NaN)")

orphans = left[left["name"].isna()]
print(f"\\nOrphan orders (no matching customer):")
print(orphans)

dup_customers = pd.concat([customers,
    pd.DataFrame({"customer_id": [101], "name": ["Alice_dup"]})])
fan_out = orders.merge(dup_customers, on="customer_id", how="inner")
print(f"\\nWith duplicate customer 101 → {len(fan_out)} rows (fan-out!)")
""",
    },

    {
        "title": "Funnel Analysis",
        "roles": ["Data Analyst", "Analytics Engineer"],
        "difficulty": "Intermediate",
        "definition": "Funnel analysis tracks user progression through a defined sequence of steps, measuring conversion and drop-off at each stage.",
        "formula": "Step conversion rate  = Users reaching step N / Users at step N−1\nOverall conversion    = Users at final step / Users at first step\nDrop-off rate         = 1 − step conversion rate\nTime-to-convert       = median(timestamp_final − timestamp_first)",
        "description": "Funnels reveal where users abandon a flow. The critical insight is not just the drop-off rate but *why* — segment by device, channel, cohort to isolate the cause.",
        "example": "Checkout funnel: Cart (1,000) → Shipping (700, −30%) → Payment (420, −40%) → Confirm (380, −9%). Payment is the biggest friction point.",
        "use_cases": ["E-commerce checkout optimization", "SaaS onboarding flow analysis", "Marketing campaign attribution", "Feature adoption tracking"],
        "watch_out": "Ordered vs. unordered funnels give different results. Decide whether users must complete steps in sequence or can take any path.",
        "python_code": """\
import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
n = 5_000
events = []
steps = ["visit", "signup", "activate", "purchase"]
probs = [1.0, 0.35, 0.55, 0.40]  # cumulative probability of reaching each step

for user_id in range(n):
    ts = pd.Timestamp("2024-01-01")
    for step, prob in zip(steps, probs):
        if rng.random() < prob:
            events.append({"user_id": user_id, "step": step,
                           "ts": ts + pd.Timedelta(hours=rng.integers(0, 48))})
            ts += pd.Timedelta(hours=rng.integers(1, 24))
        else:
            break

df = pd.DataFrame(events)

funnel = df.groupby("step")["user_id"].nunique().reindex(steps)
funnel_df = pd.DataFrame({
    "step":        steps,
    "users":       funnel.values,
    "pct_of_top":  (funnel.values / funnel.values[0] * 100).round(1),
    "step_conv":   [100.0] + (funnel.values[1:] / funnel.values[:-1] * 100).round(1).tolist(),
    "dropoff":     [0.0] + (100 - funnel.values[1:] / funnel.values[:-1] * 100).round(1).tolist(),
})
print(funnel_df.to_string(index=False))

time_to_purchase = (
    df[df["step"] == "purchase"].merge(df[df["step"] == "visit"], on="user_id")
    .assign(hours=lambda x: (x["ts_x"] - x["ts_y"]).dt.total_seconds() / 3600)
)
print(f"\\nMedian time to purchase: {time_to_purchase['hours'].median():.1f} hours")
""",
    },

    {
        "title": "Customer Lifetime Value (LTV / CLV)",
        "roles": ["Data Analyst", "Analytics Engineer"],
        "difficulty": "Intermediate",
        "definition": "The total net revenue a business can expect from a customer over their entire relationship. Used to justify acquisition costs and segment customers by strategic value.",
        "formula": "Simple LTV    = ARPU × Average Customer Lifespan\nSimple LTV    = ARPU / Churn Rate\n\nDiscounted LTV = Σ [ margin_t / (1+d)^t ]\n  d = discount rate, t = period\n\nCAC Payback   = CAC / (ARPU × Gross Margin %)",
        "description": "**Key relationships:**\n- LTV > CAC → profitable acquisition\n- LTV/CAC ≥ 3 → healthy SaaS unit economics\n- CAC Payback < 12 months → strong cash efficiency\n\n**BG/NBD model**: probabilistic LTV using transaction frequency and recency.",
        "example": "ARPU = $50/month, churn = 5%/month → LTV = $50 / 0.05 = $1,000. If CAC = $200 → LTV/CAC = 5x → healthy.",
        "use_cases": ["Marketing budget allocation", "Customer acquisition bid optimization", "Cohort health comparison", "Investor unit economics reporting"],
        "watch_out": "LTV projections depend heavily on churn rate. A 1% improvement in monthly churn doubles LTV at low churn rates. Never report LTV without confidence intervals.",
        "python_code": """\
import numpy as np
import pandas as pd

arpu       = 50
churn_rate = 0.05
gross_margin = 0.70
discount_rate = 0.10 / 12  # monthly
cac        = 200

simple_ltv    = arpu / churn_rate
discounted_ltv = sum(
    (arpu * gross_margin * (1 - churn_rate)**t) / (1 + discount_rate)**t
    for t in range(120)  # 10 years
)
payback_months = cac / (arpu * gross_margin)

print(f"Simple LTV         : ${simple_ltv:,.0f}")
print(f"Discounted LTV     : ${discounted_ltv:,.0f}")
print(f"LTV / CAC          : {discounted_ltv / cac:.1f}x")
print(f"CAC Payback        : {payback_months:.1f} months")

churn_rates = np.arange(0.02, 0.15, 0.01)
ltvs = arpu / churn_rates
sensitivity = pd.DataFrame({"churn_rate": churn_rates.round(2),
                             "ltv": ltvs.round(0),
                             "ltv_cac_ratio": (ltvs / cac).round(2)})
print("\\nLTV sensitivity to churn rate:")
print(sensitivity.to_string(index=False))
""",
    },

    {
        "title": "Time-Based Train/Test Splits",
        "roles": ["Data Scientist", "Analytics Engineer"],
        "difficulty": "Intermediate",
        "definition": "For time series data, train/test splits must respect temporal order — training only on past data and evaluating on future data to prevent lookahead bias.",
        "formula": "Walk-forward validation:\n  Train: [t₀, t₁]  → Test: [t₁, t₂]\n  Train: [t₀, t₂]  → Test: [t₂, t₃]\n  ... (expanding window)\n\nSliding window:\n  Train: [t₀, t₁]  → Test: [t₁, t₂]\n  Train: [t₁, t₂]  → Test: [t₂, t₃]\n  ... (fixed window size)",
        "description": "**Why random splits fail for time series:**\n- Data leakage: future values inform past predictions\n- Autocorrelation: nearby time points are correlated\n- Non-stationarity: distribution shifts over time\n\nAlways visualize the split boundary on a time axis before modeling.",
        "example": "Predicting December sales using data from Jan–Nov as training is valid. Using random 80/20 split leaks December patterns into training — artificially inflates performance.",
        "use_cases": ["Demand forecasting model evaluation", "Financial model backtesting", "Churn model with temporal features", "Fraud detection pipelines"],
        "watch_out": "Feature engineering leakage is subtle — rolling averages or lag features computed on the full dataset before splitting will contain future information.",
        "python_code": """\
import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error

rng = np.random.default_rng(42)
dates = pd.date_range("2022-01-01", periods=104, freq="W")
y = pd.Series(
    np.linspace(100, 200, 104) + 20 * np.sin(np.arange(104) * 2 * np.pi / 52)
    + rng.normal(0, 8, 104), index=dates
)

df = pd.DataFrame({"y": y})
for lag in [1, 2, 4, 8, 13, 26, 52]:
    df[f"lag_{lag}"] = df["y"].shift(lag)
df = df.dropna()

tscv = TimeSeriesSplit(n_splits=5)
X = df.drop("y", axis=1).values
Y = df["y"].values

maes = []
for fold, (tr_idx, te_idx) in enumerate(tscv.split(X)):
    model = Ridge().fit(X[tr_idx], Y[tr_idx])
    preds = model.predict(X[te_idx])
    mae   = mean_absolute_error(Y[te_idx], preds)
    maes.append(mae)
    print(f"Fold {fold+1}: train={len(tr_idx):3d}  test={len(te_idx):2d}  MAE={mae:.2f}")

print(f"\\nMean MAE across folds: {np.mean(maes):.2f} ± {np.std(maes):.2f}")
""",
    },

    {
        "title": "RFM Analysis",
        "roles": ["Data Analyst", "Analytics Engineer"],
        "difficulty": "Intermediate",
        "definition": "RFM segments customers by Recency (how recently they purchased), Frequency (how often), and Monetary value (how much they spend).",
        "formula": "Recency  = days since last purchase (lower = better)\nFrequency = total transactions in window\nMonetary = total or average spend in window\n\nRFM score = rank each metric into quintiles (1–5)\nCombined  = concat(R_score, F_score, M_score)",
        "description": "**Typical RFM segments:**\n- **Champions** (555): recent, frequent, high spend\n- **At-Risk** (155): once loyal, haven't bought recently\n- **Lost** (111): haven't bought in a long time\n- **New Customers** (511): recent, low frequency\n- **Potential Loyalists** (452): recent, growing frequency",
        "example": "Champion customers: offer loyalty rewards. At-Risk customers: win-back campaign with discount. Lost customers: low-cost re-engagement or accept churn.",
        "use_cases": ["CRM segmentation", "Email campaign targeting", "Retention program design", "LTV proxy scoring"],
        "watch_out": "Quintile-based RFM is sensitive to data distribution. Heavy skew in monetary value means quintile 5 captures a tiny group with enormous spend — adjust bin edges if needed.",
        "python_code": """\
import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
n = 2_000
snapshot_date = pd.Timestamp("2024-12-31")

df = pd.DataFrame({
    "customer_id": rng.integers(1, 501, n),
    "order_date":  pd.to_datetime(rng.choice(
        pd.date_range("2023-01-01", "2024-12-31"), n)),
    "revenue":     rng.exponential(150, n),
})

rfm = df.groupby("customer_id").agg(
    recency  =("order_date", lambda x: (snapshot_date - x.max()).days),
    frequency=("order_date", "count"),
    monetary =("revenue", "sum"),
).reset_index()

rfm["R"] = pd.qcut(rfm["recency"],  5, labels=[5,4,3,2,1])
rfm["F"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1,2,3,4,5])
rfm["M"] = pd.qcut(rfm["monetary"], 5, labels=[1,2,3,4,5])
rfm["RFM_score"] = rfm["R"].astype(str) + rfm["F"].astype(str) + rfm["M"].astype(str)

def segment(row):
    r, f, m = int(row["R"]), int(row["F"]), int(row["M"])
    if r >= 4 and f >= 4: return "Champion"
    if r >= 3 and f >= 3: return "Loyal"
    if r >= 4 and f <= 2: return "New Customer"
    if r <= 2 and f >= 3: return "At-Risk"
    if r <= 2 and f <= 2: return "Lost"
    return "Potential Loyalist"

rfm["segment"] = rfm.apply(segment, axis=1)
print(rfm.groupby("segment")[["recency","frequency","monetary"]].mean().round(1))
print("\\nSegment counts:")
print(rfm["segment"].value_counts())
""",
    },
    {
        "title": "Propensity Score Matching (PSM)",
        "roles": ["Data Scientist", "Data Analyst"],
        "difficulty": "Advanced",
        "definition": "A technique that reduces selection bias in observational studies by matching treated and control units with similar probability of receiving treatment, given observed covariates.",
        "formula": "Propensity score: e(X) = P(T=1 | X)\n\nEstimated via logistic regression:\n  e(X) = 1 / (1 + exp(−Xβ))\n\nATT (Average Treatment Effect on Treated):\n  ATT = E[Y(1) − Y(0) | T=1]\n      ≈ mean(Y_treated) − mean(Y_matched_control)",
        "description": "**PSM pipeline:**\n1. Estimate propensity scores (logistic regression)\n2. Check common support — overlap in score distributions\n3. Match on score (nearest neighbor, caliper, kernel)\n4. Check covariate balance after matching (SMD < 0.1)\n5. Estimate treatment effect on matched sample",
        "example": "Email campaign sent to active users (not random). PSM matches each recipient with a similar non-recipient — isolates email effect from activity bias.",
        "use_cases": ["Observational A/B analysis", "Marketing attribution", "Policy evaluation", "Retrospective clinical studies"],
        "watch_out": "PSM only controls for *observed* confounders. Unmeasured confounders still bias results. Always conduct sensitivity analysis (Rosenbaum bounds).",
        "python_code": """\
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

rng = np.random.default_rng(42)
n = 2_000
age      = rng.integers(18, 65, n).astype(float)
logins   = rng.poisson(10, n).astype(float)
treatment = (0.05 * logins + rng.normal(0, 1, n) > 0).astype(int)
outcome  = 0.3 * logins + 2.5 * treatment + rng.normal(0, 2, n)

df = pd.DataFrame({"age": age, "logins": logins, "treatment": treatment, "outcome": outcome})
X = df[["age", "logins"]]
sc = StandardScaler()
X_s = sc.fit_transform(X)

lr = LogisticRegression().fit(X_s, df["treatment"])
df["pscore"] = lr.predict_proba(X_s)[:, 1]

treated = df[df["treatment"] == 1].copy()
control = df[df["treatment"] == 0].copy()

nn = NearestNeighbors(n_neighbors=1).fit(control[["pscore"]])
_, indices = nn.kneighbors(treated[["pscore"]])
matched_ctrl = control.iloc[indices.flatten()].copy()

naive_ate = treated["outcome"].mean() - control["outcome"].mean()
psm_att   = treated["outcome"].mean() - matched_ctrl["outcome"].mean()
true_att  = 2.5

print(f"True ATT          : {true_att:.3f}")
print(f"Naive estimate    : {naive_ate:.3f}  (biased — selection into treatment)")
print(f"PSM ATT estimate  : {psm_att:.3f}")

smd_before = (treated["logins"].mean() - control["logins"].mean()) / df["logins"].std()
smd_after  = (treated["logins"].mean() - matched_ctrl["logins"].mean()) / df["logins"].std()
print(f"\\nLogins SMD before matching: {smd_before:.3f}")
print(f"Logins SMD after  matching: {smd_after:.3f}  (target < 0.1)")
""",
    },

    {
        "title": "Bayesian A/B Testing",
        "roles": ["Data Scientist", "Data Analyst"],
        "difficulty": "Advanced",
        "definition": "A Bayesian approach to experiment analysis that outputs the full posterior distribution over the treatment effect, enabling direct probability statements like P(B > A).",
        "formula": "Prior:      p ~ Beta(α₀, β₀)\nLikelihood: k successes in n trials ~ Binomial(n, p)\nPosterior:  p | data ~ Beta(α₀+k, β₀+n−k)\n\nP(B > A) = P(p_B > p_A) estimated by Monte Carlo\nExpected loss = E[max(0, p_A − p_B) | data]",
        "description": "**Frequentist vs Bayesian output:**\n- Frequentist: p=0.03 → reject H₀ (binary decision, no prob statement on effect)\n- Bayesian: P(B > A) = 97%, expected lift = +0.8%, credible interval [+0.2%, +1.5%]\n\nBayesian testing allows continuous monitoring without inflating false positive rate.",
        "example": "After 3,000 users: P(variant > control) = 94.2%, expected loss if we ship = 0.003% → ship it.",
        "use_cases": ["Early stopping A/B tests safely", "Small sample experiments", "Revenue metric testing", "Sequential analysis"],
        "watch_out": "Prior choice affects results significantly with small samples. Use a weakly informative prior (Beta(1,1) or historical data) and document it explicitly.",
        "python_code": """\
import numpy as np
from scipy import stats

rng = np.random.default_rng(42)

# Prior: Beta(1,1) = uniform (no prior knowledge)
alpha_prior, beta_prior = 1, 1

# Observed data
n_ctrl, conv_ctrl = 2_000, 82   # ~4.1%
n_var,  conv_var  = 2_000, 104  # ~5.2%

# Posterior: Beta(alpha + successes, beta + failures)
ctrl_post = stats.beta(alpha_prior + conv_ctrl, beta_prior + n_ctrl - conv_ctrl)
var_post  = stats.beta(alpha_prior + conv_var,  beta_prior + n_var  - conv_var)

# Monte Carlo estimate
N = 200_000
s_ctrl = ctrl_post.rvs(N, random_state=42)
s_var  = var_post.rvs(N, random_state=42)

prob_var_wins = (s_var > s_ctrl).mean()
expected_lift = (s_var - s_ctrl).mean()
expected_loss = np.maximum(0, s_ctrl - s_var).mean()
ci = np.percentile(s_var - s_ctrl, [2.5, 97.5])

print(f"Control  posterior mean : {ctrl_post.mean()*100:.2f}%")
print(f"Variant  posterior mean : {var_post.mean()*100:.2f}%")
print(f"\\nP(variant > control)    : {prob_var_wins*100:.1f}%")
print(f"Expected lift           : {expected_lift*100:.3f}%")
print(f"Expected loss if ship   : {expected_loss*100:.4f}%")
print(f"95% credible interval   : [{ci[0]*100:.2f}%, {ci[1]*100:.2f}%]")
""",
    },

    {
        "title": "Model Calibration",
        "roles": ["Data Scientist"],
        "difficulty": "Advanced",
        "definition": "A model is well-calibrated when its predicted probabilities match observed event frequencies — a model that predicts 70% confidence should be right roughly 70% of the time.",
        "formula": "Expected Calibration Error (ECE):\n  ECE = Σ (|B_m| / n) × |acc(B_m) − conf(B_m)|\n\nBrier Score:\n  BS = (1/n) × Σ (p̂ᵢ − yᵢ)²\n  Range [0,1], lower is better\n  Brier Skill Score = 1 − BS/BS_ref",
        "description": "**Why calibration matters:**\n- AUC measures ranking ability — calibration measures probability accuracy\n- A model with AUC=0.95 can still be badly miscalibrated\n- Risk scoring, medical diagnosis, and financial models require calibrated probabilities\n\n**Fixes:** Platt scaling (logistic regression on scores), Isotonic regression (non-parametric).",
        "example": "Churn model: users predicted at 80% probability actually churn 40% of the time → model is overconfident. Platt scaling fixes this.",
        "use_cases": ["Credit risk scoring", "Medical diagnosis models", "Insurance pricing", "Any model where the probability itself is consumed"],
        "watch_out": "Calibration and discrimination are independent. Always evaluate both. A model can have poor AUC but great calibration, or vice versa.",
        "python_code": """\
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.model_selection import train_test_split
from sklearn.metrics import brier_score_loss

X, y = make_classification(n_samples=5_000, n_features=20, random_state=42,
                            weights=[0.85, 0.15])
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42)

rf = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_tr, y_tr)
rf_cal = CalibratedClassifierCV(rf, method="isotonic", cv=5).fit(X_tr, y_tr)

for name, model in [("Random Forest (uncal)", rf), ("RF + Isotonic Cal", rf_cal)]:
    probs = model.predict_proba(X_te)[:, 1]
    frac_pos, mean_pred = calibration_curve(y_te, probs, n_bins=10)
    ece = np.mean(np.abs(frac_pos - mean_pred))
    bs  = brier_score_loss(y_te, probs)
    print(f"{name:25s}  ECE={ece:.4f}  Brier={bs:.4f}")

# Reliability diagram data
probs_rf = rf.predict_proba(X_te)[:, 1]
frac, pred = calibration_curve(y_te, probs_rf, n_bins=10)
print("\\nReliability diagram (predicted → actual):")
for p, f in zip(pred.round(2), frac.round(2)):
    bar = "█" * int(f * 20)
    print(f"  {p:.2f} → {f:.2f}  {bar}")
""",
    },

    {
        "title": "Shapley Values & Model Explainability (SHAP)",
        "roles": ["Data Scientist"],
        "difficulty": "Expert",
        "definition": "SHAP (SHapley Additive exPlanations) assigns each feature a contribution value to a specific prediction, based on Shapley values from cooperative game theory.",
        "formula": "φᵢ = Σ [|S|!(|F|−|S|−1)!/|F|!] × [f(S∪{i}) − f(S)]\n  S ⊆ F\\{i}\n\nPrediction = base_value + Σ SHAP(feature_i)\n\nSHAP properties:\n  Efficiency: Σ φᵢ = f(x) − E[f(X)]\n  Symmetry, Dummy, Additivity",
        "description": "**Types of SHAP explanations:**\n- **Local**: why did this specific prediction happen?\n- **Global**: which features matter most overall?\n- **Dependence plots**: how does feature X interact with feature Y?\n\nSHAP is model-agnostic but has efficient exact implementations for tree models (TreeSHAP: O(TLD²)).",
        "example": "Loan denial: SHAP shows credit_score=−0.32, debt_ratio=−0.18, income=+0.12 → credit score was the primary reason for rejection.",
        "use_cases": ["Regulatory compliance (model explainability laws)", "Debugging model behavior", "Feature selection", "Customer-facing explanations"],
        "watch_out": "SHAP values explain the model, not the true causal effect. A high SHAP value means the model relies on a feature — not that the feature causes the outcome.",
        "python_code": """\
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer
# pip install shap
import shap

data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
model = GradientBoostingClassifier(n_estimators=100, random_state=42).fit(X_tr, y_tr)

explainer   = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_te)

mean_abs_shap = pd.Series(
    np.abs(shap_values).mean(axis=0),
    index=data.feature_names
).sort_values(ascending=False)

print("Top 10 features by mean |SHAP|:")
print(mean_abs_shap.head(10).round(4))

instance_idx = 0
instance_shap = pd.Series(shap_values[instance_idx], index=data.feature_names)
print(f"\\nPrediction for instance {instance_idx}:")
print(f"  Base value   : {explainer.expected_value:.4f}")
print(f"  SHAP sum     : {instance_shap.sum():.4f}")
print(f"  Final logit  : {explainer.expected_value + instance_shap.sum():.4f}")
print("\\nTop 5 contributors:")
print(instance_shap.abs().sort_values(ascending=False).head(5).round(4))
""",
    },

    {
        "title": "Instrumental Variables & Two-Stage Least Squares",
        "roles": ["Data Scientist"],
        "difficulty": "Expert",
        "definition": "An instrumental variable (IV) is a variable that affects the treatment but has no direct effect on the outcome — used to estimate causal effects when confounders are unobserved.",
        "formula": "Validity conditions:\n  Relevance:  Cov(Z, T) ≠ 0  (instrument affects treatment)\n  Exclusion:  Cov(Z, ε) = 0  (instrument only affects Y through T)\n  Exogeneity: Z is independent of confounders\n\n2SLS:\n  Stage 1: T̂ = γ₀ + γ₁Z + controls\n  Stage 2: Y  = β₀ + β₁T̂ + controls + ε\n  β₁ is the LATE (Local Average Treatment Effect)",
        "description": "2SLS isolates the variation in treatment caused by the instrument — which is (by assumption) unconfounded. The price: you only identify LATE (effect for compliers), and IV estimates have higher variance than OLS.",
        "example": "Effect of education on earnings: instrument = distance to nearest college (affects years of schooling but not earnings directly). Removes ability bias from OLS.",
        "use_cases": ["Estimating causal returns to treatment in observational data", "Mendelian randomization in genetics", "Policy evaluation with partial compliance", "Pricing elasticity with cost instruments"],
        "watch_out": "Weak instruments (F < 10 in Stage 1) produce biased and imprecise IV estimates. Always report the first-stage F-statistic.",
        "python_code": """\
import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.iv import IV2SLS

rng = np.random.default_rng(42)
n = 2_000

# Data generating process
ability      = rng.normal(0, 1, n)         # unobserved confounder
instrument_z = rng.binomial(1, 0.5, n)     # distance to college (instrument)
education    = 12 + 2 * instrument_z + 1.5 * ability + rng.normal(0, 1, n)
earnings     = 20 + 3 * education + 4 * ability + rng.normal(0, 5, n)

df = pd.DataFrame({"earnings": earnings, "education": education,
                   "instrument": instrument_z, "ability": ability})

# Naive OLS (biased — ability is unobserved)
X_ols = sm.add_constant(df["education"])
ols = sm.OLS(df["earnings"], X_ols).fit()
print(f"OLS β (biased)   : {ols.params['education']:.3f}  (true = 3.0, bias from ability)")

# 2SLS
X_2sls = df[["education"]]
Z_2sls = df[["instrument"]]
endog  = df["education"]
exog   = pd.DataFrame({"const": np.ones(n)})

iv_model = IV2SLS(df["earnings"], exog, X_2sls, Z_2sls).fit(cov_type="robust")
print(f"2SLS β (causal)  : {iv_model.params['education']:.3f}  (closer to true = 3.0)")
print(f"First-stage F    : {iv_model.first_stage.diagnostics['f.stat'].values[0]:.1f}  (need > 10)")

# Oracle OLS with ability (would never have in practice)
X_oracle = sm.add_constant(df[["education", "ability"]])
oracle = sm.OLS(df["earnings"], X_oracle).fit()
print(f"Oracle OLS β     : {oracle.params['education']:.3f}  (ideal with observed ability)")
""",
    },

    {
        "title": "Transformer Architecture & Attention Mechanism",
        "roles": ["Data Scientist"],
        "difficulty": "Expert",
        "definition": "The transformer is a neural network architecture using self-attention to model relationships between all positions in a sequence simultaneously, without recurrence.",
        "formula": "Attention(Q,K,V) = softmax(QKᵀ / √d_k) × V\n\nQ = XW_Q  (queries)\nK = XW_K  (keys)\nV = XW_V  (values)\nd_k = key dimension (scaling prevents vanishing gradients)\n\nMulti-Head: concat(head₁,...,headₕ) × W_O\nPositional encoding: PE(pos,2i) = sin(pos/10000^(2i/d))",
        "description": "**Key components:**\n- **Self-attention**: each token attends to all others — captures long-range dependencies\n- **Multi-head attention**: multiple attention patterns in parallel\n- **Feed-forward**: per-position MLP after attention\n- **Layer norm + residual**: training stability\n\nFoundation of BERT, GPT, T5, and all modern LLMs.",
        "example": "In 'The animal didn't cross the street because it was too tired', attention links 'it' to 'animal' — resolves coreference across distance.",
        "use_cases": ["Text classification and generation (LLMs)", "Tabular data (TabTransformer)", "Time series (Temporal Fusion Transformer)", "Recommendation systems"],
        "watch_out": "Attention complexity is O(n²) in sequence length. For long sequences use efficient variants (Longformer, Flash Attention).",
        "python_code": """\
import numpy as np

def softmax(x, axis=-1):
    e = np.exp(x - x.max(axis=axis, keepdims=True))
    return e / e.sum(axis=axis, keepdims=True)

def scaled_dot_product_attention(Q, K, V):
    d_k = Q.shape[-1]
    scores = Q @ K.T / np.sqrt(d_k)      # (seq, seq)
    weights = softmax(scores, axis=-1)    # attention weights
    return weights @ V, weights

rng = np.random.default_rng(42)
seq_len, d_model = 5, 16
d_k = d_v = 8

X    = rng.normal(0, 1, (seq_len, d_model))
W_Q  = rng.normal(0, 0.1, (d_model, d_k))
W_K  = rng.normal(0, 0.1, (d_model, d_k))
W_V  = rng.normal(0, 0.1, (d_model, d_v))

Q = X @ W_Q
K = X @ W_K
V = X @ W_V

output, attn_weights = scaled_dot_product_attention(Q, K, V)
print(f"Input  shape : {X.shape}")
print(f"Output shape : {output.shape}")
print(f"Attn weights shape: {attn_weights.shape}")
print("\\nAttention weight matrix (row i = how much token i attends to each token):")
print(attn_weights.round(3))
print(f"\\nEach row sums to: {attn_weights.sum(axis=1).round(4)}")
""",
    },

    {
        "title": "Approximate Nearest Neighbor Search (ANN)",
        "roles": ["Data Scientist", "Data Engineer"],
        "difficulty": "Expert",
        "definition": "Algorithms that find the most similar vectors in high-dimensional spaces in sub-linear time by trading exact recall for speed, enabling real-time similarity search at scale.",
        "formula": "Exact NN: O(n × d) — linear scan\n\nHNSW (Hierarchical Navigable Small World):\n  Build: O(n × log n)\n  Query: O(log n)\n  Space: O(n × M)  [M = connections per node]\n\nIVF (Inverted File Index):\n  Cluster into C centroids\n  Query: search top nprobe clusters only",
        "description": "**Key algorithms:**\n| Method | Speed | Recall | Memory | Notes |\n|--------|-------|--------|--------|---------|\n| Brute force | Slow | 100% | Low | Ground truth |\n| LSH | Fast | ~85% | Low | Hash-based |\n| HNSW | Fast | ~99% | High | Best accuracy/speed |\n| IVF+PQ | Fast | ~95% | Low | Compressed vectors |",
        "example": "1M product embeddings (768d) → HNSW index builds in 3 minutes, queries in <1ms at 98% recall. Brute force: 200ms per query.",
        "use_cases": ["Vector database backends (Pinecone, Weaviate, pgvector)", "RAG retrieval", "Real-time recommendations", "Semantic search at scale"],
        "watch_out": "Recall vs. speed is tunable via `ef_search` (HNSW) or `nprobe` (IVF). Benchmark at your target latency, not maximum recall.",
        "python_code": """\
import numpy as np
import time
# pip install faiss-cpu
import faiss

rng = np.random.default_rng(42)
d = 128          # embedding dimension
n_corpus = 100_000
n_queries = 100

corpus  = rng.random((n_corpus, d)).astype("float32")
queries = rng.random((n_queries, d)).astype("float32")
faiss.normalize_L2(corpus)
faiss.normalize_L2(queries)

# Brute force (exact)
t0 = time.time()
index_flat = faiss.IndexFlatIP(d)
index_flat.add(corpus)
_, I_exact = index_flat.search(queries, k=5)
t_exact = time.time() - t0
print(f"Exact (Flat IP)  : {t_exact*1000:.1f}ms  recall=100%")

# HNSW (approximate)
index_hnsw = faiss.IndexHNSWFlat(d, 32)  # M=32 connections
index_hnsw.hnsw.efConstruction = 64
index_hnsw.add(corpus)
t0 = time.time()
_, I_hnsw = index_hnsw.search(queries, k=5)
t_hnsw = time.time() - t0

overlap = sum(len(set(I_exact[i]) & set(I_hnsw[i])) for i in range(n_queries))
recall = overlap / (n_queries * 5)
print(f"HNSW             : {t_hnsw*1000:.1f}ms  recall={recall:.3f}")
print(f"Speedup          : {t_exact/t_hnsw:.1f}x")
""",
    },

    {
        "title": "Decision Trees (CART Algorithm)",
        "roles": ["Data Scientist", "Data Analyst"],
        "difficulty": "Intermediate",
        "definition": "A tree-structured model that recursively splits data using binary rules on features, creating a hierarchy of decisions that maps inputs to outputs.",
        "formula": "Split criterion (Gini impurity):\n  Gini(t) = 1 − Σ pᵢ²\n\nSplit criterion (Variance reduction for regression):\n  ΔVar = Var(parent) − [n_L/n × Var(left) + n_R/n × Var(right)]\n\nLeaf prediction:\n  Classification: majority class\n  Regression:     mean of leaf samples",
        "description": "CART (Classification and Regression Trees) finds the single best binary split at each node by exhaustively searching all features and thresholds. Stops when max_depth, min_samples_leaf, or pure leaves are reached.\n\n**Pruning** removes branches that add little predictive power, trading accuracy on training data for better generalization.",
        "example": "Churn tree: first split on `days_since_login > 30` → left node (high churn risk) → next split on `plan == free` → leaf: 72% churn probability.",
        "use_cases": ["Interpretable business rules", "Feature importance baseline", "Building block for Random Forests / XGBoost", "Decision support systems"],
        "watch_out": "Unpruned trees memorize training data perfectly. A single tree is high-variance — small data changes produce very different trees. Use as a baseline, not a final model.",
        "python_code": """\
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_text
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

data = load_breast_cancer()
X, y = data.data, data.target
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

for depth in [2, 4, 6, None]:
    dt = DecisionTreeClassifier(max_depth=depth, criterion="gini", random_state=42)
    dt.fit(X_tr, y_tr)
    tr_acc = accuracy_score(y_tr, dt.predict(X_tr))
    te_acc = accuracy_score(y_te, dt.predict(X_te))
    n_leaves = dt.get_n_leaves()
    print(f"depth={str(depth):4s}  train={tr_acc:.3f}  test={te_acc:.3f}  leaves={n_leaves:3d}")

best = DecisionTreeClassifier(max_depth=4, random_state=42).fit(X_tr, y_tr)
print("\\nTree structure (depth=4):")
print(export_text(best, feature_names=list(data.feature_names), max_depth=3))

importances = pd.Series(best.feature_importances_, index=data.feature_names)
print("Top 5 features:")
print(importances.nlargest(5).round(4))
""",
    },

    {
        "title": "Neural Networks & Backpropagation",
        "roles": ["Data Scientist"],
        "difficulty": "Advanced",
        "definition": "A neural network is a layered composition of linear transformations and non-linear activation functions. Backpropagation uses the chain rule to compute gradients of the loss with respect to every weight.",
        "formula": "Forward pass:\n  z⁽ˡ⁾ = W⁽ˡ⁾ a⁽ˡ⁻¹⁾ + b⁽ˡ⁾\n  a⁽ˡ⁾ = σ(z⁽ˡ⁾)\n\nBackward pass (chain rule):\n  δ⁽ˡ⁾ = (W⁽ˡ⁺¹⁾ᵀ δ⁽ˡ⁺¹⁾) ⊙ σ′(z⁽ˡ⁾)\n  ∂L/∂W⁽ˡ⁾ = δ⁽ˡ⁾ (a⁽ˡ⁻¹⁾)ᵀ\n\nActivations: ReLU = max(0,x), Sigmoid = 1/(1+e⁻ˣ)",
        "description": "**Common activations:**\n| Function | Range | Use Case |\n|----------|-------|----------|\n| ReLU | [0, ∞) | Hidden layers (default) |\n| Sigmoid | (0, 1) | Binary output |\n| Softmax | (0,1) sum=1 | Multi-class output |\n| Tanh | (−1, 1) | RNNs, zero-centered |\n| LeakyReLU | (−∞,∞) | Avoids dying ReLU |",
        "example": "3-layer MLP: input(20) → hidden(64, ReLU) → hidden(32, ReLU) → output(1, Sigmoid). Backprop adjusts all 64×20 + 32×64 + 1×32 weights each step.",
        "use_cases": ["Image classification", "Tabular deep learning", "Time series (LSTM/GRU)", "Foundation for all deep learning architectures"],
        "watch_out": "Vanishing gradients: deep sigmoid networks stop learning in early layers. Use ReLU + batch normalization + residual connections to fix.",
        "python_code": """\
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

X, y = make_classification(n_samples=2_000, n_features=20, n_informative=10, random_state=42)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
sc = StandardScaler()
X_tr = sc.fit_transform(X_tr); X_te = sc.transform(X_te)

X_tr_t = torch.FloatTensor(X_tr); y_tr_t = torch.FloatTensor(y_tr)
X_te_t = torch.FloatTensor(X_te)

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(20, 64), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(64, 32), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(32, 1),  nn.Sigmoid()
        )
    def forward(self, x): return self.net(x).squeeze()

model    = MLP()
optim    = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn  = nn.BCELoss()
loader   = DataLoader(TensorDataset(X_tr_t, y_tr_t), batch_size=64, shuffle=True)

for epoch in range(20):
    for xb, yb in loader:
        optim.zero_grad()
        loss_fn(model(xb), yb).backward()
        optim.step()

model.eval()
with torch.no_grad():
    probs = model(X_te_t).numpy()
print(f"AUC-ROC: {roc_auc_score(y_te, probs):.4f}")
""",
    },

    {
        "title": "Hyperparameter Tuning",
        "roles": ["Data Scientist"],
        "difficulty": "Advanced",
        "definition": "The process of finding the optimal configuration of model settings (not learned from data) that maximizes generalization performance.",
        "formula": "Grid Search:    exhaustive search over all combinations\nRandom Search:  sample n random combinations\n\nBayesian Optimization:\n  Fit surrogate model (GP) on observed (params → score)\n  Maximize acquisition function (EI, UCB)\n  Evaluate at argmax → update surrogate\n\nEI(x) = E[max(0, f(x) − f(x⁺))]",
        "description": "| Method | Evaluations | Best For |\n|--------|-------------|----------|\n| Grid Search | All combos | ≤3 params, small ranges |\n| Random Search | n samples | 4+ params |\n| Bayesian (Optuna) | Intelligent | Expensive models |\n| Successive Halving | Budget-aware | Large search spaces |",
        "example": "XGBoost with 5 hyperparameters: grid search = 10,000 fits. Random search with 100 trials finds 95% as good in 1% of the time.",
        "use_cases": ["All ML model training pipelines", "Neural architecture search", "AutoML systems", "Competition optimization"],
        "watch_out": "Tune hyperparameters on a validation set, never the test set. Nested CV is required for unbiased performance estimates when tuning and evaluating simultaneously.",
        "python_code": """\
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import (train_test_split, RandomizedSearchCV,
                                      cross_val_score)
from sklearn.metrics import roc_auc_score
from scipy.stats import uniform, randint
import optuna
optuna.logging.set_verbosity(optuna.logging.WARNING)

X, y = make_classification(n_samples=2_000, n_features=20, n_informative=10, random_state=42)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

param_dist = {
    "n_estimators":    randint(50, 300),
    "max_depth":       randint(2, 8),
    "learning_rate":   uniform(0.01, 0.3),
    "subsample":       uniform(0.6, 0.4),
    "min_samples_leaf": randint(5, 50),
}
rs = RandomizedSearchCV(GradientBoostingClassifier(random_state=42),
                        param_dist, n_iter=30, cv=5, scoring="roc_auc",
                        random_state=42, n_jobs=-1)
rs.fit(X_tr, y_tr)
print(f"RandomSearch best AUC: {rs.best_score_:.4f}")
print(f"Best params: {rs.best_params_}")

def objective(trial):
    params = {
        "n_estimators":  trial.suggest_int("n_estimators", 50, 300),
        "max_depth":     trial.suggest_int("max_depth", 2, 8),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
        "subsample":     trial.suggest_float("subsample", 0.6, 1.0),
    }
    model = GradientBoostingClassifier(**params, random_state=42)
    return cross_val_score(model, X_tr, y_tr, cv=3, scoring="roc_auc").mean()

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=30, show_progress_bar=False)
print(f"Optuna best AUC: {study.best_value:.4f}")
""",
    },

    {
        "title": "Model Drift & Monitoring",
        "roles": ["Data Scientist", "Data Engineer"],
        "difficulty": "Advanced",
        "definition": "Model drift is the degradation of model performance over time due to changes in the real-world data distribution (data drift) or the relationship between inputs and outputs (concept drift).",
        "formula": "Data drift (PSI — Population Stability Index):\n  PSI = Σ (Actual% − Expected%) × ln(Actual%/Expected%)\n  PSI < 0.1 → stable\n  PSI 0.1–0.25 → monitor\n  PSI > 0.25 → retrain\n\nKS Test: max|F_train(x) − F_prod(x)|",
        "description": "**Types of drift:**\n- **Data drift (covariate shift)**: P(X) changes, P(Y|X) stable\n- **Concept drift**: P(Y|X) changes — the world changed\n- **Label drift**: P(Y) changes — class balance shifts\n- **Upstream drift**: schema change or pipeline bug\n\n**Monitoring stack**: prediction distribution → feature distributions → PSI/KS alerts → performance metrics (when labels available).",
        "example": "Fraud model trained in 2023: PSI for transaction_amount spikes to 0.38 in Q1 2024 after inflation. Model flags too many legitimate transactions — retrain required.",
        "use_cases": ["Production ML model health", "Scheduled retraining triggers", "Data pipeline quality gates", "SLA compliance"],
        "watch_out": "Performance metrics lag reality — you need ground truth labels to compute them. Drift metrics (PSI, KS) give earlier warning without labels.",
        "python_code": """\
import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(42)
train_data = rng.normal(50, 10, 5_000)
stable_prod = rng.normal(50, 10, 1_000)
drifted_prod = rng.normal(65, 15, 1_000)

def psi(expected, actual, n_bins=10):
    bins = np.percentile(expected, np.linspace(0, 100, n_bins + 1))
    bins[0], bins[-1] = -np.inf, np.inf
    exp_pct = np.histogram(expected, bins=bins)[0] / len(expected)
    act_pct = np.histogram(actual,   bins=bins)[0] / len(actual)
    exp_pct = np.where(exp_pct == 0, 1e-6, exp_pct)
    act_pct = np.where(act_pct == 0, 1e-6, act_pct)
    return np.sum((act_pct - exp_pct) * np.log(act_pct / exp_pct))

ks_stable  = stats.ks_2samp(train_data, stable_prod)
ks_drifted = stats.ks_2samp(train_data, drifted_prod)

print("--- Stable production data ---")
print(f"  PSI : {psi(train_data, stable_prod):.4f}  (<0.1 = stable)")
print(f"  KS  : stat={ks_stable.statistic:.4f}  p={ks_stable.pvalue:.4f}")

print("\\n--- Drifted production data ---")
print(f"  PSI : {psi(train_data, drifted_prod):.4f}  (>0.25 = retrain)")
print(f"  KS  : stat={ks_drifted.statistic:.4f}  p={ks_drifted.pvalue:.6f}")

window_size = 100
rolling_means = pd.Series(drifted_prod).rolling(window_size).mean()
drift_detected = rolling_means[rolling_means > 60].index[0] if any(rolling_means > 60) else None
print(f"\\nRolling mean breach detected at index: {drift_detected}")
""",
    },

    {
        "title": "Reinforcement Learning Fundamentals",
        "roles": ["Data Scientist"],
        "difficulty": "Expert",
        "definition": "A learning paradigm where an agent learns to maximize cumulative reward by taking actions in an environment, receiving feedback, and updating its policy.",
        "formula": "Bellman equation:\n  V(s) = max_a [ R(s,a) + γ × Σ P(s′|s,a) × V(s′) ]\n\nQ-learning update:\n  Q(s,a) ← Q(s,a) + α[r + γ × max_a′ Q(s′,a′) − Q(s,a)]\n\nPolicy gradient (REINFORCE):\n  ∇J(θ) = E[∇logπ_θ(a|s) × G_t]",
        "description": "**Key concepts:**\n- **State (s)**: current situation\n- **Action (a)**: choice made by agent\n- **Reward (r)**: feedback signal\n- **Policy (π)**: mapping from state to action\n- **Value function V(s)**: expected cumulative reward from state s\n- **Discount factor γ**: weight of future rewards (0=myopic, 1=far-sighted)",
        "example": "Recommender as RL: state = user context, action = item to show, reward = click/purchase. Policy learns to maximize long-term engagement, not just immediate clicks.",
        "use_cases": ["Game playing (AlphaGo, OpenAI Five)", "Robotic control", "Ad bid optimization", "LLM fine-tuning (RLHF)"],
        "watch_out": "Sample efficiency is the core challenge — RL requires millions of environment interactions to learn. Reward shaping bugs cause catastrophic unexpected behavior.",
        "python_code": """\
import numpy as np

rng = np.random.default_rng(42)

# Simple grid world Q-learning
n_states, n_actions = 16, 4   # 4x4 grid, 4 directions
goal_state = 15
Q = np.zeros((n_states, n_actions))

alpha, gamma, epsilon = 0.1, 0.95, 0.3

def step(state, action):
    row, col = state // 4, state % 4
    moves = [(-1,0),(1,0),(0,-1),(0,1)]   # up, down, left, right
    dr, dc = moves[action]
    new_row = max(0, min(3, row + dr))
    new_col = max(0, min(3, col + dc))
    next_state = new_row * 4 + new_col
    reward = 10.0 if next_state == goal_state else -0.1
    done = next_state == goal_state
    return next_state, reward, done

for episode in range(2_000):
    state = rng.integers(0, 15)
    for _ in range(50):
        if rng.random() < epsilon:
            action = rng.integers(0, n_actions)
        else:
            action = np.argmax(Q[state])
        next_state, reward, done = step(state, action)
        td_target = reward + gamma * np.max(Q[next_state]) * (1 - done)
        Q[state, action] += alpha * (td_target - Q[state, action])
        state = next_state
        if done: break

print("Learned Q-values (best action per state):")
policy_names = ["↑","↓","←","→"]
for s in range(n_states):
    best = policy_names[np.argmax(Q[s])]
    val  = Q[s].max()
    print(f"  s={s:2d}: {best}  V={val:.3f}", end="  " if s % 4 < 3 else "\\n")
""",
    },

    {
        "title": "Anomaly Detection in Time Series",
        "roles": ["Data Scientist", "Analytics Engineer"],
        "difficulty": "Advanced",
        "definition": "Identifying time points where a metric deviates significantly from its expected value given its historical pattern, seasonality, and trend.",
        "formula": "STL residual method:\n  residual(t) = y(t) − trend(t) − seasonal(t)\n  anomaly if |residual(t)| > k × σ_residual\n\nFacebook Prophet anomaly:\n  anomaly if y(t) ∉ [yhat_lower, yhat_upper]\n\nIQR on residuals:\n  anomaly if residual < Q1 − 3×IQR or > Q3 + 3×IQR",
        "description": "**Types of time series anomalies:**\n- **Point anomaly**: single outlier spike\n- **Contextual anomaly**: normal value in wrong context (e.g., Sunday traffic on Monday)\n- **Collective anomaly**: sequence of values that together are abnormal\n\nKey challenge: distinguishing real anomalies from seasonal patterns and trend changes.",
        "example": "Daily signups: sudden spike on Tuesday → anomaly. But December always spikes → seasonal, not anomaly. STL decomposition separates these.",
        "use_cases": ["Infrastructure metric alerting", "Business KPI anomaly detection", "Fraud pattern detection", "IoT sensor monitoring"],
        "watch_out": "Static thresholds fail as the metric grows. Always use relative thresholds (% deviation from expected) or model-based bounds, not absolute cutoffs.",
        "python_code": """\
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL

rng = np.random.default_rng(42)
dates = pd.date_range("2023-01-01", periods=365, freq="D")
trend    = np.linspace(100, 150, 365)
seasonal = 20 * np.sin(2 * np.pi * np.arange(365) / 7)
noise    = rng.normal(0, 5, 365)
signal   = trend + seasonal + noise

signal[100] += 80   # point anomaly
signal[200:205] += 40  # collective anomaly

series = pd.Series(signal, index=dates, name="signups")

stl = STL(series, period=7, robust=True).fit()
residuals = stl.resid

q1, q3 = np.percentile(residuals, [25, 75])
iqr = q3 - q1
lower, upper = q1 - 3 * iqr, q3 + 3 * iqr

anomalies = series[(residuals < lower) | (residuals > upper)]
print(f"Detected {len(anomalies)} anomalies:")
print(anomalies.round(1))

sigma = residuals.std()
zscore_anomalies = series[np.abs(residuals) > 3 * sigma]
print(f"\\nZ-score method (3σ): {len(zscore_anomalies)} anomalies")
print(f"Trend range  : {stl.trend.min():.1f} – {stl.trend.max():.1f}")
print(f"Seasonal amp : ±{stl.seasonal.std():.1f}")
""",
    },

    {
        "title": "DAU / MAU / WAU & Engagement Ratios",
        "roles": ["Data Analyst", "Analytics Engineer"],
        "difficulty": "Foundational",
        "definition": "Activity metrics counting unique users who interact with a product in a given time window: Daily, Weekly, or Monthly Active Users.",
        "formula": "DAU  = distinct users active on a given day\nWAU  = distinct users active in a rolling 7-day window\nMAU  = distinct users active in a rolling 28/30-day window\n\nDAU/MAU ratio (stickiness) = DAU / MAU\n  > 0.20 → good retention signal\n  > 0.50 → exceptional (WhatsApp-level)\n\nL7 = users active on 7 of last 7 days (power users)",
        "description": "**Common traps:**\n- MAU hides churn: you can grow MAU while losing core users if acquisition > churn\n- Definition matters: 'active' must be a meaningful action, not just a login or session open\n- Rolling vs calendar windows give different results — document which you use",
        "example": "App: MAU=500K, DAU=75K → stickiness=15% (needs improvement). Competitor: MAU=300K, DAU=90K → stickiness=30% (much healthier engagement).",
        "use_cases": ["Product health dashboards", "Investor reporting", "Growth vs retention decomposition", "Benchmark against competitors"],
        "watch_out": "Stickiness alone is misleading for weekly-use products (e.g. gym apps). Always contextualize with product use-case frequency.",
        "python_code": """\
import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
n_events = 50_000
events = pd.DataFrame({
    "user_id": rng.integers(1, 10_001, n_events),
    "date":    pd.to_datetime(rng.choice(
        pd.date_range("2024-01-01", "2024-03-31"), n_events)),
})

dau = events.groupby("date")["user_id"].nunique().rename("DAU")

mau_list = []
for date in pd.date_range("2024-01-28", "2024-03-31"):
    window = events[(events["date"] > date - pd.Timedelta(days=28)) &
                    (events["date"] <= date)]
    mau_list.append({"date": date, "MAU": window["user_id"].nunique()})
mau = pd.DataFrame(mau_list).set_index("date")["MAU"]

metrics = pd.concat([dau, mau], axis=1).dropna()
metrics["stickiness"] = (metrics["DAU"] / metrics["MAU"]).round(3)

print(metrics.tail(10))
print(f"\\nAvg DAU         : {metrics['DAU'].mean():,.0f}")
print(f"Avg MAU         : {metrics['MAU'].mean():,.0f}")
print(f"Avg stickiness  : {metrics['stickiness'].mean():.3f}")

power_users = (events.groupby("user_id")["date"]
               .nunique()
               .pipe(lambda s: (s >= 21).sum()))
print(f"Power users (active 21+ days): {power_users:,}")
""",
    },

    {
        "title": "North Star Metric & Metric Trees",
        "roles": ["Data Analyst", "Analytics Engineer"],
        "difficulty": "Foundational",
        "definition": "A North Star Metric (NSM) is the single metric that best captures the core value a product delivers to users. A metric tree decomposes it into measurable, actionable sub-metrics.",
        "formula": "NSM decomposition (multiplicative):\n  NSM = Driver₁ × Driver₂ × Driver₃\n\nExample (e-commerce revenue):\n  Revenue = Visitors × CVR × AOV\n  CVR     = Sessions with purchase / Total sessions\n  AOV     = Revenue / Orders\n\nWoW growth decomposition:\n  ΔNSM = ΔNSM_new + ΔNSM_retained − ΔNSM_churned",
        "description": "**Good NSM criteria:**\n- Reflects value delivered to users (not just business value)\n- Leads revenue, not lags it\n- Actionable by multiple teams\n- Sensitive to product changes\n\n**Examples:** Airbnb = nights booked, Spotify = time listening, Slack = messages sent, LinkedIn = weekly active professionals.",
        "example": "NSM = Weekly Active Buyers. Tree: WAB = MAU × purchase_rate. MAU = new_users + retained_users. purchase_rate = sessions_with_purchase / sessions.",
        "use_cases": ["OKR / goal setting", "Team metric alignment", "Root cause analysis frameworks", "Dashboard design"],
        "watch_out": "Optimizing a sub-metric without watching the NSM leads to local maxima. A team improving CTR while degrading purchase rate is moving in the wrong direction.",
        "python_code": """\
import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
weeks = pd.date_range("2024-01-01", periods=12, freq="W")

data = pd.DataFrame({
    "week":         weeks,
    "visitors":     rng.integers(80_000, 120_000, 12),
    "sessions":     rng.integers(100_000, 160_000, 12),
    "purchases":    rng.integers(3_000, 5_000, 12),
    "revenue":      rng.uniform(400_000, 700_000, 12),
})

data["CVR"]  = data["purchases"] / data["visitors"]
data["AOV"]  = data["revenue"]   / data["purchases"]
data["NSM"]  = data["revenue"]              # North Star = Revenue
data["NSM_check"] = data["visitors"] * data["CVR"] * data["AOV"]

data["NSM_wow"] = data["NSM"].pct_change() * 100
data["CVR_wow"] = data["CVR"].pct_change() * 100
data["AOV_wow"] = data["AOV"].pct_change() * 100
data["vis_wow"] = data["visitors"].pct_change() * 100

print(data[["week","NSM","CVR","AOV","NSM_wow","CVR_wow","AOV_wow"]].round(2).to_string(index=False))

latest = data.iloc[-1]
print(f"\\nLatest NSM drivers:")
print(f"  Visitors : {latest['visitors']:,}")
print(f"  CVR      : {latest['CVR']*100:.2f}%")
print(f"  AOV      : ${latest['AOV']:.2f}")
print(f"  Revenue  : ${latest['NSM']:,.0f}")
""",
    },

    {
        "title": "SaaS Business Metrics (MRR, ARR, NRR, NDR)",
        "roles": ["Data Analyst", "Analytics Engineer"],
        "difficulty": "Intermediate",
        "definition": "Standardized financial metrics for subscription businesses that track revenue predictability, growth, and the quality of existing customer relationships.",
        "formula": "MRR = Σ monthly recurring revenue across all active subscriptions\nARR = MRR × 12\n\nMRR movement:\n  Net New MRR = New MRR + Expansion MRR − Churned MRR − Contraction MRR\n\nNRR (Net Revenue Retention):\n  NRR = (Beginning MRR + Expansion − Churn − Contraction) / Beginning MRR × 100\n\nGross Revenue Retention (GRR):\n  GRR = (Beginning MRR − Churn − Contraction) / Beginning MRR × 100",
        "description": "**Benchmarks:**\n- NRR > 100%: revenue grows from existing customers alone (expansion > churn)\n- NRR > 120%: world-class (Snowflake, Datadog territory)\n- GRR > 90%: healthy downgrade/churn control\n- Quick Ratio = (New + Expansion) / (Churn + Contraction) > 4 = efficient growth",
        "example": "Jan MRR=$100K. Feb: +$20K new, +$8K expansion, −$5K churn, −$2K contraction. Feb MRR=$121K. NRR=(100+8−5−2)/100=101%.",
        "use_cases": ["Investor reporting", "Board dashboards", "Sales and CS team targets", "Valuation multiples (ARR-based)"],
        "watch_out": "NRR > 100% does NOT mean you don't have churn. It means expansion revenue is outpacing churn. GRR reveals the true churn picture.",
        "python_code": """\
import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
months = pd.date_range("2024-01", periods=12, freq="ME")

mrr = pd.DataFrame({
    "month":       months,
    "new_mrr":     rng.integers(15_000, 30_000, 12),
    "expansion":   rng.integers(5_000, 12_000, 12),
    "churn_mrr":   rng.integers(3_000, 8_000, 12),
    "contraction": rng.integers(1_000, 3_000, 12),
})
mrr["beginning_mrr"] = 100_000
for i in range(1, len(mrr)):
    mrr.loc[i, "beginning_mrr"] = (
        mrr.loc[i-1, "beginning_mrr"]
        + mrr.loc[i-1, "new_mrr"]
        + mrr.loc[i-1, "expansion"]
        - mrr.loc[i-1, "churn_mrr"]
        - mrr.loc[i-1, "contraction"]
    )

mrr["ending_mrr"] = (mrr["beginning_mrr"] + mrr["new_mrr"] +
                     mrr["expansion"] - mrr["churn_mrr"] - mrr["contraction"])
mrr["NRR"] = ((mrr["beginning_mrr"] + mrr["expansion"] -
               mrr["churn_mrr"] - mrr["contraction"]) /
               mrr["beginning_mrr"] * 100).round(1)
mrr["GRR"] = ((mrr["beginning_mrr"] - mrr["churn_mrr"] -
               mrr["contraction"]) / mrr["beginning_mrr"] * 100).round(1)
mrr["quick_ratio"] = ((mrr["new_mrr"] + mrr["expansion"]) /
                       (mrr["churn_mrr"] + mrr["contraction"])).round(2)
mrr["ARR"] = mrr["ending_mrr"] * 12

print(mrr[["month","ending_mrr","NRR","GRR","quick_ratio","ARR"]].to_string(index=False))
print(f"\\nAvg NRR: {mrr['NRR'].mean():.1f}%  |  Avg GRR: {mrr['GRR'].mean():.1f}%")
print(f"Final ARR: ${mrr['ARR'].iloc[-1]:,.0f}")
""",
    },

    {
        "title": "Chart Selection & Data Visualization Principles",
        "roles": ["Data Analyst", "Analytics Engineer"],
        "difficulty": "Foundational",
        "definition": "Choosing the right chart type based on the relationship being communicated and the data types involved, following perceptual principles that maximize clarity.",
        "formula": "Lie Factor (Tufte) = size of effect in graphic / size of effect in data\n  Ideal = 1.0\n\nData-Ink Ratio = data ink / total ink\n  Maximize: remove non-data ink\n\nChart selection logic:\n  Comparison over time   → line chart\n  Part-to-whole          → bar chart (not pie)\n  Distribution           → histogram / box plot\n  Correlation            → scatter plot\n  Composition over time  → stacked area\n  Ranking                → horizontal bar",
        "description": "**Core principles (Tufte, Few):**\n- Maximize data-ink ratio — remove grid lines, borders, chart junk\n- Start y-axis at zero for bar charts (never for line charts)\n- Use color to encode meaning, not decoration\n- Order categorical axes by value, not alphabetically\n- Avoid 3D charts — they distort perception",
        "example": "Comparing 5 categories over time: use line chart (not grouped bar chart — too busy). Showing single month's breakdown: horizontal bar chart sorted by value.",
        "use_cases": ["Dashboard design", "Executive presentation", "Exploratory data analysis", "Stakeholder reporting"],
        "watch_out": "Pie charts fail beyond 3–4 slices. Human perception is poor at comparing angles — use bar charts instead.",
        "python_code": """\
import pandas as pd
import numpy as np

chart_guide = pd.DataFrame({
    "question": [
        "How does X change over time?",
        "How do categories compare?",
        "What is the distribution?",
        "How are two variables related?",
        "What is the part-whole breakdown?",
        "How do groups differ statistically?",
        "Where are things located?",
        "How does X correlate across many vars?",
    ],
    "best_chart": [
        "Line chart",
        "Horizontal bar (sorted by value)",
        "Histogram / KDE / Box plot",
        "Scatter plot",
        "Bar chart (not pie)",
        "Box plot / Violin plot",
        "Map / Scatter with geo coords",
        "Heatmap (correlation matrix)",
    ],
    "avoid": [
        "Bar chart",
        "Pie / Donut chart",
        "Line chart",
        "Bar chart",
        "Pie chart (>3 slices)",
        "Bar chart of means only",
        "Bar chart",
        "Individual scatter plots",
    ],
    "data_types": [
        "Continuous Y, datetime X",
        "Continuous Y, categorical X",
        "Continuous X",
        "Continuous X and Y",
        "Proportions of categorical",
        "Continuous Y, categorical groups",
        "Lat/lon + metric",
        "Multiple continuous vars",
    ]
})
print(chart_guide.to_string(index=False))

rng = np.random.default_rng(42)
data = pd.DataFrame({
    "category": list("ABCDE"),
    "value":    rng.integers(10, 100, 5),
})
print("\\nSorted horizontal bar data (correct):")
print(data.sort_values("value", ascending=False))
print("\\nAlphabetical order (wrong — harder to compare):")
print(data.sort_values("category"))
""",
    },

    {
        "title": "dbt Testing & Documentation Patterns",
        "roles": ["Analytics Engineer"],
        "difficulty": "Intermediate",
        "definition": "dbt tests validate data quality assertions on transformed models. Documentation creates a queryable data catalog with column-level descriptions and lineage.",
        "formula": "Built-in dbt tests:\n  unique:       SELECT count(*) > 0 WHERE count(col) > 1\n  not_null:     SELECT count(*) WHERE col IS NULL\n  accepted_values: SELECT col NOT IN (list)\n  relationships:  FK integrity check\n\nTest severity:\n  error   → pipeline fails\n  warn    → logs warning, continues",
        "description": "**Test pyramid for dbt:**\n- **Source tests**: raw data freshness + schema\n- **Staging tests**: uniqueness + not_null on PKs\n- **Mart tests**: business logic assertions, referential integrity\n- **Custom tests**: SQL macros for complex rules (revenue > 0, date ranges)\n\ndbt-expectations and dbt-utils extend native tests significantly.",
        "example": "fact_orders: `order_id` unique + not_null. `revenue` > 0 (custom test). `customer_id` references dim_customers. Freshness: source updated within 24h.",
        "use_cases": ["Data contract enforcement in CI/CD", "Pipeline observability", "Onboarding documentation", "Governance and compliance"],
        "watch_out": "Tests without severity=error are suggestions, not guards. Set error thresholds on business-critical columns and warn on secondary columns.",
        "python_code": """\
# dbt schema.yml equivalent — shown as Python dict for illustration
# In practice this lives in schema.yml alongside your .sql model files

schema_config = {
    "version": 2,
    "models": [
        {
            "name": "fact_orders",
            "description": "One row per completed order. Grain: order_id.",
            "columns": [
                {
                    "name": "order_id",
                    "description": "Surrogate key for each order.",
                    "tests": ["unique", "not_null"],
                },
                {
                    "name": "customer_id",
                    "description": "FK to dim_customers.",
                    "tests": [{"relationships": {"to": "ref('dim_customers')",
                                                  "field": "customer_id"}}],
                },
                {
                    "name": "revenue_usd",
                    "description": "Order revenue in USD, post-refund.",
                    "tests": [{"dbt_expectations.expect_column_values_to_be_between":
                                {"min_value": 0, "max_value": 1_000_000,
                                 "severity": "error"}}],
                },
                {
                    "name": "order_date",
                    "tests": ["not_null",
                              {"dbt_expectations.expect_column_values_to_be_of_type":
                               {"column_type": "date"}}],
                },
            ],
        }
    ],
    "sources": [
        {
            "name": "raw_postgres",
            "freshness": {"warn_after": {"count": 12, "period": "hour"},
                          "error_after": {"count": 24, "period": "hour"}},
            "tables": [{"name": "orders", "loaded_at_field": "updated_at"}],
        }
    ],
}

import json
print(json.dumps(schema_config, indent=2))
""",
    },

    {
        "title": "dbt Materializations & Incremental Models",
        "roles": ["Analytics Engineer"],
        "difficulty": "Intermediate",
        "definition": "dbt materializations control how a model is persisted in the warehouse. Incremental models process only new or changed records, dramatically reducing compute cost for large tables.",
        "formula": "Incremental filter (standard):\n  WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})\n\nUnique key merge (upsert):\n  MERGE INTO target USING source ON target.id = source.id\n  WHEN MATCHED   → UPDATE\n  WHEN NOT MATCHED → INSERT\n\nPartition-based incremental (BigQuery):\n  WHERE DATE(_PARTITIONTIME) >= DATE_SUB(CURRENT_DATE, INTERVAL 3 DAY)",
        "description": "| Materialization | Behavior | Best For |\n|-----------------|----------|----------|\n| view | Query runs each time | Small, simple models |\n| table | Full rebuild each run | Medium tables, slow sources |\n| incremental | Append/merge new rows | Large event tables |\n| ephemeral | CTE, no storage | Intermediate logic only |\n| snapshot | SCD Type 2 | Slowly changing dimensions |",
        "example": "events table: 2 billion rows. Full rebuild = 45 minutes. Incremental processing last 3 days = 90 seconds.",
        "use_cases": ["Large event stream processing", "Cost optimization in cloud warehouses", "Near-real-time data pipelines", "SCD tracking (snapshots)"],
        "watch_out": "Incremental models can drift from full refreshes if the filter logic or source data changes. Schedule periodic full refreshes and always test with `dbt run --full-refresh`.",
        "python_code": """\
# Illustrative dbt incremental model logic in Python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

rng = np.random.default_rng(42)

def simulate_source(n=10_000):
    return pd.DataFrame({
        "event_id":   range(n),
        "user_id":    rng.integers(1, 1_001, n),
        "event_type": rng.choice(["click","view","purchase"], n),
        "revenue":    np.where(rng.random(n) < 0.1, rng.exponential(50, n), 0),
        "updated_at": pd.date_range("2024-01-01", periods=n, freq="1min"),
    })

def incremental_load(source: pd.DataFrame, existing: pd.DataFrame,
                     unique_key: str, watermark_col: str) -> pd.DataFrame:
    if existing.empty:
        return source
    max_watermark = existing[watermark_col].max()
    new_records   = source[source[watermark_col] > max_watermark]
    print(f"New records to process: {len(new_records):,}")
    updated = new_records[new_records[unique_key].isin(existing[unique_key])]
    inserted = new_records[~new_records[unique_key].isin(existing[unique_key])]
    result = existing[~existing[unique_key].isin(updated[unique_key])]
    return pd.concat([result, updated, inserted]).sort_values("updated_at")

source_data = simulate_source(10_000)
existing_table = source_data.iloc[:8_000].copy()

result = incremental_load(source_data, existing_table, "event_id", "updated_at")
print(f"Existing rows: {len(existing_table):,}")
print(f"After incremental load: {len(result):,}")
print(f"Revenue total check: ${result['revenue'].sum():,.2f}")
""",
    },

    {
        "title": "Table Partitioning & Clustering Strategies",
        "roles": ["Data Engineer", "Analytics Engineer"],
        "difficulty": "Advanced",
        "definition": "Partitioning divides a table into physical segments by column value. Clustering sorts data within partitions to reduce bytes scanned per query.",
        "formula": "Partition pruning savings:\n  bytes_scanned = total_bytes × (matching_partitions / total_partitions)\n\nBigQuery partition types:\n  - Ingestion time: _PARTITIONTIME\n  - Column: DATE/TIMESTAMP column\n  - Integer range: RANGE BUCKET\n\nSnowflake clustering depth:\n  CD = (total_constant + 0.5 × total_overlapping) / total_partitions\n  Lower depth = better clustering",
        "description": "**Partition strategy selection:**\n- Partition on the column most commonly used in WHERE filters\n- Date/timestamp is almost always the right partition key for event tables\n- Cardinality too high (user_id) → too many partitions\n- Cardinality too low (country, 5 values) → little benefit\n\n**Clustering** (Snowflake/BigQuery): secondary sort within partition — use for columns commonly in JOIN ON or additional WHERE conditions.",
        "example": "events table partitioned by event_date, clustered by user_id. Query: `WHERE event_date = '2024-01-15' AND user_id = 12345` → scans 1 partition × small cluster range.",
        "use_cases": ["Cloud warehouse cost optimization", "Query performance tuning", "Large table design", "dbt model configuration"],
        "watch_out": "Partitioning on low-cardinality columns (e.g., boolean) gives minimal benefit. Partitioning on high-cardinality columns creates too many small partitions — worse performance.",
        "python_code": """\
import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
n = 1_000_000
events = pd.DataFrame({
    "event_id":   range(n),
    "event_date": pd.to_datetime(rng.choice(
        pd.date_range("2024-01-01", "2024-12-31"), n)),
    "user_id":    rng.integers(1, 100_001, n),
    "event_type": rng.choice(["click","view","purchase"], n),
    "revenue":    rng.exponential(50, n),
})

# Simulate partition pruning benefit
target_date = pd.Timestamp("2024-06-15")
total_partitions = 366

full_scan_rows = len(events)
partition_scan = len(events[events["event_date"] == target_date])
pruning_benefit = (1 - partition_scan / full_scan_rows) * 100

print(f"Total rows        : {full_scan_rows:,}")
print(f"Rows in partition : {partition_scan:,}")
print(f"Pruning benefit   : {pruning_benefit:.1f}% bytes saved")

partition_stats = (events.groupby("event_date")
                   .agg(row_count=("event_id","count"),
                        revenue_sum=("revenue","sum"))
                   .describe().round(0))
print("\\nPartition size distribution:")
print(partition_stats)

print("\nSQL DDL examples:")
print('''
        - - BigQuery partitioned + clustered table
        CREATE TABLE `project.dataset.events`
        PARTITION BY DATE(event_date)
        CLUSTER BY user_id, event_type
        AS SELECT * FROM source;

        -- Snowflake
        CREATE TABLE events
        CLUSTER BY(event_date, user_id)
        AS SELECT * FROM source;
        ''')
""",
    },

    {
        "title": "Change Data Capture (CDC)",
        "roles": ["Data Engineer"],
        "difficulty": "Advanced",
        "definition": "CDC is a pattern for tracking row-level changes (inserts, updates, deletes) in source databases and propagating them to downstream systems in near-real-time.",
        "formula": "Log-based CDC latency:\n  lag = current_time − log_sequence_number_timestamp\n\nDeduplication for out-of-order events:\n  keep row with MAX(lsn) per primary key\n\nMerge pattern:\n  WHEN op='d' → DELETE\n  WHEN op='u' → UPDATE\n  WHEN op='i' → INSERT",
        "description": "**CDC methods:**\n| Method | Latency | Source Impact | Notes |\n|--------|---------|---------------|-------|\n| Timestamp polling | Minutes | Read load | Misses deletes |\n| Trigger-based | Seconds | Write overhead | Fragile |\n| Log-based (Debezium) | Sub-second | Near-zero | Best practice |\n\n**Common tools:** Debezium (Kafka), AWS DMS, Fivetran, Airbyte, Striim.",
        "example": "PostgreSQL → Debezium reads WAL → Kafka topic `postgres.public.orders` → Flink job merges into Iceberg table. End-to-end latency: ~3 seconds.",
        "use_cases": ["Real-time data warehouse sync", "Event-driven microservices", "Audit trail creation", "Cache invalidation"],
        "watch_out": "Log-based CDC requires database log retention configuration. If the consumer falls behind and logs rotate, you lose events — set retention ≥ 24 hours.",
        "python_code": """\
import pandas as pd
import numpy as np
from datetime import datetime

# Simulate CDC event stream (Debezium-style messages)
cdc_events = pd.DataFrame({
    "lsn":        [1001, 1002, 1003, 1004, 1005, 1006],
    "op":         ["i", "i", "u", "i", "d", "u"],
    "id":         [1, 2, 1, 3, 2, 3],
    "name":       ["Alice", "Bob", "Alice Updated", "Carol", "Bob", "Carol Updated"],
    "revenue":    [100.0, 200.0, 150.0, 300.0, None, 320.0],
    "ts":         pd.date_range("2024-01-01 10:00", periods=6, freq="30s"),
})

print("CDC event stream:")
print(cdc_events)

def apply_cdc(events: pd.DataFrame) -> pd.DataFrame:
    target = {}
    for _, row in events.sort_values("lsn").iterrows():
        pk = row["id"]
        if row["op"] == "d":
            target.pop(pk, None)
        else:
            target[pk] = {"id": pk, "name": row["name"],
                          "revenue": row["revenue"], "lsn": row["lsn"]}
    return pd.DataFrame(target.values()).sort_values("id").reset_index(drop=True)

result = apply_cdc(cdc_events)
print("\\nTarget table after applying CDC:")
print(result)

# Deduplication for out-of-order events
ooo_events = cdc_events.sample(frac=1, random_state=42)
deduped = (ooo_events.sort_values("lsn", ascending=False)
           .drop_duplicates(subset="id", keep="first")
           .query("op != 'd'")
           .sort_values("id"))
print("\\nDeduplicated (latest state per id):")
print(deduped[["id","name","revenue","lsn"]])
""",
    },

    {
        "title": "Data Lakehouse Architecture",
        "roles": ["Data Engineer", "Analytics Engineer"],
        "difficulty": "Advanced",
        "definition": "A lakehouse combines the low-cost storage of a data lake with the ACID transactions, schema enforcement, and query performance of a data warehouse using open table formats.",
        "formula": "Open table formats (Delta Lake / Iceberg / Hudi):\n  Storage = Parquet data files + transaction log\n  ACID via optimistic concurrency control\n\nZ-ordering (data skipping):\n  co-locate related data within files\n  bytes_skipped = files_where_min > filter OR max < filter\n\nVacuum: removes files older than retention_hours",
        "description": "**Architecture layers:**\n1. **Bronze** (raw): append-only, full history, schema-on-read\n2. **Silver** (cleaned): validated, deduplicated, typed\n3. **Gold** (curated): aggregated, business-ready, modeled\n\n**Key features vs traditional lake:**\n- ACID transactions (no partial writes)\n- Time travel (query as-of any version)\n- Schema evolution with enforcement\n- Unified batch + streaming",
        "example": "Medallion architecture: raw Kafka events → Bronze Iceberg table → Silver (deduped, typed) → Gold (daily aggregates for BI).",
        "use_cases": ["Unified batch + streaming pipelines", "Cost-efficient large-scale analytics", "ML feature stores", "Regulatory data retention"],
        "watch_out": "Small file problem: streaming writes create many small Parquet files, degrading read performance. Schedule compaction jobs (OPTIMIZE / REWRITE DATA FILES).",
        "python_code": """\
import pandas as pd
import numpy as np
from datetime import datetime

# Simulate medallion architecture layers
rng = np.random.default_rng(42)
n = 10_000

# Bronze: raw ingestion (append-only, duplicates allowed)
bronze = pd.DataFrame({
    "raw_id":     range(n),
    "event_id":   rng.integers(1, 8_001, n),   # intentional duplicates
    "user_id":    rng.integers(1, 2_001, n),
    "event_type": rng.choice(["click","view","purchase",None], n, p=[.4,.4,.15,.05]),
    "amount_raw": rng.choice(["$50.00","100","75.5",None,"invalid"], n,
                             p=[.3,.3,.2,.1,.1]),
    "ingested_at": datetime.now(),
})
print(f"Bronze rows : {len(bronze):,}  (with dups + nulls + bad data)")

# Silver: clean + deduplicate + type
def clean_amount(x):
    try: return float(str(x).replace("$",""))
    except: return np.nan

silver = (bronze
    .dropna(subset=["event_type"])
    .assign(amount=lambda df: df["amount_raw"].apply(clean_amount))
    .drop_duplicates(subset="event_id", keep="last")
    .drop(columns=["raw_id","amount_raw","ingested_at"])
    .assign(processed_at=datetime.now())
)
print(f"Silver rows : {len(silver):,}  (deduped, typed, validated)")

# Gold: business aggregates
gold = (silver
    .groupby(["user_id","event_type"])
    .agg(event_count=("event_id","count"),
         total_amount=("amount","sum"),
         avg_amount=("amount","mean"))
    .reset_index()
    .assign(updated_at=datetime.now())
)
print(f"Gold rows   : {len(gold):,}  (aggregated, BI-ready)")
print(gold.head())
""",
    },

    {
        "title": "Differential Privacy & k-Anonymity",
        "roles": ["Data Scientist", "Data Engineer"],
        "difficulty": "Expert",
        "definition": "Privacy-preserving techniques that mathematically bound the information that can be inferred about individuals from published data or model outputs.",
        "formula": "k-Anonymity:\n  every record is indistinguishable from ≥ k−1 others\n  on quasi-identifier columns\n\nDifferential Privacy:\n  P[M(D) ∈ S] ≤ e^ε × P[M(D′) ∈ S]\n  D, D′ differ by one individual\n  ε = privacy budget (lower = more private)\n\nLaplace mechanism: add noise ~ Laplace(0, Δf/ε)\n  Δf = global sensitivity of query f",
        "description": "**Privacy hierarchy:**\n- k-Anonymity: simple, deterministic, vulnerable to homogeneity attacks\n- l-Diversity: extends k-anonymity with diverse sensitive values\n- t-Closeness: distribution of sensitive values matches population\n- Differential Privacy: gold standard — probabilistic, composable, mathematical guarantees",
        "example": "Census: add Laplace noise with ε=1.0 to each county count. Individual's presence changes any count by at most 1, noise overwhelms that signal.",
        "use_cases": ["Census data publication", "ML model training on sensitive data", "Analytics on health/financial data", "Federated learning"],
        "watch_out": "ε composition: running multiple queries consumes privacy budget. Total ε = sum of individual ε values — budget exhaustion degrades privacy guarantees.",
        "python_code": """\
import numpy as np
import pandas as pd
from itertools import combinations

rng = np.random.default_rng(42)
n = 1_000

df = pd.DataFrame({
    "age":     rng.integers(18, 80, n),
    "zipcode": rng.choice(["94101","94102","94103","94104","94105"], n),
    "gender":  rng.choice(["M","F","NB"], n),
    "disease": rng.choice(["None","Diabetes","Hypertension"], n, p=[0.7,0.15,0.15]),
})

def generalize_age(age, bucket=10):
    return f"{(age // bucket) * bucket}-{(age // bucket) * bucket + 9}"

def k_anonymize(df, quasi_ids, k=3):
    df_anon = df.copy()
    df_anon["age_gen"] = df_anon["age"].apply(generalize_age)
    groups = df_anon.groupby(quasi_ids + ["age_gen"]).size()
    suppressed = (groups < k).sum()
    min_group  = groups.min()
    print(f"Min group size: {min_group}  |  Groups < k={k}: {suppressed}")
    return df_anon

anon = k_anonymize(df, ["gender","zipcode"], k=3)

def laplace_mechanism(true_value, sensitivity, epsilon):
    noise = rng.laplace(0, sensitivity / epsilon)
    return true_value + noise

true_count = (df["disease"] == "Diabetes").sum()
for eps in [0.1, 0.5, 1.0, 5.0]:
    noisy = laplace_mechanism(true_count, sensitivity=1, epsilon=eps)
    print(f"ε={eps:.1f}  true={true_count}  noisy={noisy:.0f}  error={abs(noisy-true_count):.1f}")
""",
    },

    {
        "title": "Fairness & Bias in ML Models",
        "roles": ["Data Scientist"],
        "difficulty": "Expert",
        "definition": "Algorithmic fairness measures whether model predictions systematically disadvantage protected groups (race, gender, age). Multiple fairness definitions exist and often conflict.",
        "formula": "Demographic Parity:\n  P(Ŷ=1|A=0) = P(Ŷ=1|A=1)\n\nEqualized Odds:\n  TPR_A=0 = TPR_A=1  AND  FPR_A=0 = FPR_A=1\n\nPredictive Parity:\n  P(Y=1|Ŷ=1,A=0) = P(Y=1|Ŷ=1,A=1)\n\nDisparate Impact Ratio:\n  DIR = P(Ŷ=1|A=minority) / P(Ŷ=1|A=majority)\n  < 0.8 → adverse impact (US EEOC threshold)",
        "description": "**Impossibility theorem (Chouldechova 2017):** Demographic parity, equalized odds, and predictive parity cannot all be satisfied simultaneously when base rates differ across groups.\n\n**Bias sources:** historical bias in labels, representation bias in training data, measurement bias, aggregation bias.",
        "example": "Hiring model: approval rate 45% for Group A, 28% for Group B → DIR=0.62 → below 0.8 threshold → adverse impact. Investigate feature importance for protected proxies.",
        "use_cases": ["Hiring and lending models", "Criminal justice risk scoring", "Ad targeting compliance", "Healthcare treatment recommendations"],
        "watch_out": "Removing protected attributes does NOT prevent discrimination. Proxy variables (zip code, name, browsing history) can reconstruct protected characteristics.",
        "python_code": """\
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

rng = np.random.default_rng(42)
n = 5_000
group      = rng.binomial(1, 0.4, n)
ability    = rng.normal(0.5 * group, 1, n)  # historical bias: group A has lower mean
approved   = (ability + 0.3 * group + rng.normal(0, 0.5, n) > 0.5).astype(int)

X = pd.DataFrame({"ability": ability, "group": group})
X_tr, X_te, y_tr, y_te = train_test_split(X, approved, test_size=0.3, random_state=42)

clf = LogisticRegression().fit(X_tr, y_tr)
y_pred = clf.predict(X_te)
groups = X_te["group"]

def fairness_report(y_true, y_pred, group):
    results = {}
    for g in [0, 1]:
        mask = group == g
        yt, yp = y_true[mask], y_pred[mask]
        tn, fp, fn, tp = confusion_matrix(yt, yp).ravel()
        results[f"group_{g}"] = {
            "approval_rate": yp.mean().round(3),
            "TPR (recall)":  (tp / (tp + fn)).round(3),
            "FPR":           (fp / (fp + tn)).round(3),
            "precision":     (tp / (tp + fp)).round(3),
        }
    df = pd.DataFrame(results)
    df["disparity_ratio"] = (df["group_0"] / df["group_1"]).round(3)
    return df

report = fairness_report(y_te.values, y_pred, groups.values)
print(report)
dir_val = report.loc["approval_rate", "disparity_ratio"]
print(f"\\nDisparate Impact Ratio: {dir_val:.3f}  {'⚠ ADVERSE IMPACT' if dir_val < 0.8 else '✓ OK'}")
""",
    },

    {
        "title": "Query Cost Optimization in Cloud Warehouses",
        "roles": ["Analytics Engineer", "Data Engineer"],
        "difficulty": "Advanced",
        "definition": "Techniques for minimizing compute and storage costs in cloud-billed analytical databases like BigQuery, Snowflake, and Redshift through query and schema design.",
        "formula": "BigQuery cost:\n  bytes_billed = bytes_scanned (rounded up to 10MB)\n  cost = bytes_billed × $6.25 / TB\n\nSnowflake cost:\n  credits = warehouse_seconds / 3600 × credits_per_hour\n  cost = credits × credit_price\n\nCost reduction levers:\n  1. Partition pruning → fewer bytes scanned\n  2. Column pruning → SELECT named cols vs SELECT *\n  3. Materialization → avoid repeated heavy transforms\n  4. Result caching → identical queries = $0",
        "description": "**Quick wins ranked by impact:**\n1. Add date partition filter to all queries on event tables\n2. Replace `SELECT *` with named columns\n3. Use `APPROX_COUNT_DISTINCT` instead of `COUNT(DISTINCT)` for dashboards\n4. Materialize expensive CTEs as tables if queried frequently\n5. Use clustering keys matching your join and filter columns\n6. Cache BI tool queries — avoid per-user re-computation",
        "example": "Daily dashboard query on 3TB events table: `SELECT *` with no date filter = $18.75/run × 50 users = $937/day. Add partition + columns = $0.06/run.",
        "use_cases": ["Cloud cost reduction", "dbt model design", "BI tool backend optimization", "Data platform budgeting"],
        "watch_out": "Premature optimization wastes engineering time. Profile query costs first — 80% of cost often comes from 20% of queries. Fix those first.",
        "python_code": """\
import pandas as pd

cost_patterns = pd.DataFrame({
    "pattern": [
        "SELECT * — no filter",
        "SELECT * — with date filter",
        "SELECT 3 cols — with date filter",
        "SELECT * — wrong date function",
        "APPROX_COUNT_DISTINCT",
        "COUNT(DISTINCT id)",
        "Uncached repeated query",
        "Cached repeated query (BQ)",
    ],
    "example_sql": [
        "SELECT * FROM events",
        "SELECT * FROM events WHERE date = '2024-01-01'",
        "SELECT id, type, revenue FROM events WHERE date = '2024-01-01'",
        "SELECT * FROM events WHERE DATE(created_at) = '2024-01-01'",
        "SELECT APPROX_COUNT_DISTINCT(user_id) FROM events",
        "SELECT COUNT(DISTINCT user_id) FROM events",
        "SELECT SUM(revenue) FROM fact_orders -- run 50x/day",
        "SELECT SUM(revenue) FROM fact_orders -- result reused",
    ],
    "tb_scanned": [3.0, 0.008, 0.001, 3.0, 3.0, 3.0, 0.05, 0.0],
    "bq_cost_usd": [18.75, 0.05, 0.006, 18.75, 18.75, 18.75, 0.31, 0.0],
    "note": [
        "Full table scan, all columns",
        "Partition pruning — 99.7% savings",
        "Partition + column pruning — 99.97% savings",
        "Function breaks partition pruning!",
        "~2% error, 10x faster",
        "Exact but expensive",
        "50 × $6.25/TB × 50MB",
        "Cached — free in BigQuery",
    ]
})
cost_patterns["daily_cost_50x"] = cost_patterns["bq_cost_usd"] * 50
print(cost_patterns[["pattern","tb_scanned","bq_cost_usd","daily_cost_50x"]].to_string(index=False))
""",
    },

    {
        "title": "Semantic Layer & Metrics Layer",
        "roles": ["Analytics Engineer"],
        "difficulty": "Advanced",
        "definition": "A semantic layer is a centralized, governed definition of business metrics and dimensions that sits between the warehouse and BI tools, ensuring consistent metric definitions across all reports.",
        "formula": "Metric definition components:\n  name:        unique identifier\n  type:        simple | ratio | cumulative | derived\n  measure:     SUM/COUNT/AVG of a column\n  filters:     WHERE conditions on the metric\n  dimensions:  columns to slice/group by\n  time_grains: day | week | month | quarter\n\nRatio metric:\n  value = numerator_measure / denominator_measure",
        "description": "**Problem it solves:** Without a semantic layer, every analyst hard-codes metric logic in SQL. Revenue is defined differently in 5 dashboards. The semantic layer is the single source of truth.\n\n**Tools:** dbt Semantic Layer (MetricFlow), LookML (Looker), Cube.dev, AtScale.",
        "example": "Conversion rate defined once: `conversions / sessions` where status='complete'. Every dashboard queries this definition — impossible to have inconsistent numbers.",
        "use_cases": ["Consistent KPI definitions across BI tools", "Self-service analytics governance", "Metric versioning and deprecation", "Cross-tool metric reuse"],
        "watch_out": "A semantic layer adds abstraction overhead. Don't build one for 10 metrics — it pays off at 50+ metrics with multiple teams and BI tools.",
        "python_code": """\
# Illustrative metric definitions (dbt Semantic Layer / MetricFlow style)
# In practice: metrics.yml in dbt project

metrics_config = {
    "metrics": [
        {
            "name": "monthly_revenue",
            "label": "Monthly Revenue",
            "type": "simple",
            "type_params": {"measure": {"name": "revenue_usd", "agg": "sum"}},
            "filter": "{{ Dimension('order__status') }} = 'completed'",
            "time_spine": {"node_relation": {"alias": "orders"},
                          "time_column": "order_date"},
        },
        {
            "name": "conversion_rate",
            "label": "Conversion Rate",
            "type": "ratio",
            "type_params": {
                "numerator":   {"name": "purchases", "agg": "count"},
                "denominator": {"name": "sessions",  "agg": "count"},
            },
        },
        {
            "name": "nrr",
            "label": "Net Revenue Retention",
            "type": "derived",
            "type_params": {
                "expr": "ending_mrr / beginning_mrr",
                "metrics": [
                    {"name": "ending_mrr"},
                    {"name": "beginning_mrr"},
                ],
            },
        },
    ]
}

import json
print(json.dumps(metrics_config, indent=2))

# Python equivalent — metric registry pattern
class MetricRegistry:
    def __init__(self): self._metrics = {}
    def register(self, name, fn): self._metrics[name] = fn
    def compute(self, name, df): return self._metrics[name](df)

import pandas as pd, numpy as np
rng = np.random.default_rng(42)
df = pd.DataFrame({"revenue": rng.exponential(100, 1000),
                   "status": rng.choice(["completed","pending"], 1000, p=[.8,.2]),
                   "sessions": np.ones(1000)})

registry = MetricRegistry()
registry.register("monthly_revenue",
    lambda df: df[df["status"]=="completed"]["revenue"].sum())
registry.register("conversion_rate",
    lambda df: (df["status"]=="completed").sum() / len(df))

print(f"\nmonthly_revenue : ${registry.compute('monthly_revenue', df):,.2f}")
print(f"conversion_rate : {registry.compute('conversion_rate', df)*100:.1f}%")
""",
    },

    {
        "title": "Kafka Architecture & Message Queue Fundamentals",
        "roles": ["Data Engineer"],
        "difficulty": "Advanced",
        "definition": "Apache Kafka is a distributed event streaming platform using a log-based, partitioned, replicated architecture for high-throughput, fault-tolerant data transport.",
        "formula": "Throughput:\n  max_throughput = partitions × consumer_threads × msg/s_per_thread\n\nRetention:\n  bytes_retained = partitions × retention_hours × write_rate_bytes/s\n\nConsumer lag:\n  lag = latest_offset − committed_offset\n  lag_seconds ≈ lag / (throughput_msgs/s)",
        "description": "**Core concepts:**\n- **Topic**: named category of messages\n- **Partition**: ordered, immutable log — unit of parallelism\n- **Offset**: position of message within partition\n- **Producer**: writes to topic (with partitioner)\n- **Consumer group**: each partition consumed by one member\n- **Broker**: server storing partitions\n- **Replication factor**: number of replicas for durability\n\n**Delivery semantics:**\n- At-most-once: may lose messages\n- At-least-once: may duplicate (default)\n- Exactly-once: requires transactions + idempotent consumers",
        "example": "Orders topic: 12 partitions, 3 brokers, replication=3. 12 consumer instances process in parallel. Max consumer lag alert: >10,000 messages.",
        "use_cases": ["Real-time event streaming", "Microservice decoupling", "CDC pipeline transport", "Activity tracking at scale"],
        "watch_out": "Consumer lag is the key health metric. Growing lag means consumers can't keep up with producers — scale consumer group or optimize processing logic.",
        "python_code": """\
import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from collections import defaultdict, deque
from typing import Dict, List

@dataclass
class KafkaMessage:
    key: str
    value: dict
    offset: int
    partition: int

class SimulatedKafkaTopic:
    def __init__(self, name: str, n_partitions: int = 3):
        self.name = name
        self.partitions: Dict[int, deque] = {i: deque() for i in range(n_partitions)}
        self.offsets: Dict[int, int] = {i: 0 for i in range(n_partitions)}
        self.n_partitions = n_partitions

    def produce(self, key: str, value: dict):
        partition = hash(key) % self.n_partitions
        offset = self.offsets[partition]
        msg = KafkaMessage(key=key, value=value, offset=offset, partition=partition)
        self.partitions[partition].append(msg)
        self.offsets[partition] += 1
        return partition, offset

    def consume(self, partition: int, from_offset: int = 0) -> List[KafkaMessage]:
        return [m for m in self.partitions[partition] if m.offset >= from_offset]

topic = SimulatedKafkaTopic("orders", n_partitions=3)

rng = np.random.default_rng(42)
for i in range(20):
    user_id = str(rng.integers(1, 6))
    topic.produce(key=user_id, value={"order_id": i, "user_id": user_id,
                                      "amount": rng.exponential(100).round(2)})

print("Partition distribution:")
for p in range(3):
    msgs = topic.consume(p)
    print(f"  Partition {p}: {len(msgs)} messages  "
          f"keys={set(m.key for m in msgs)}")

committed_offsets = {0: 2, 1: 1, 2: 3}
lags = {p: topic.offsets[p] - committed_offsets[p] for p in range(3)}
total_lag = sum(lags.values())
print(f"\\nConsumer group lag per partition: {lags}")
print(f"Total lag: {total_lag} messages")
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
            with st.expander(f"**{i + 1} - {topic['title']}**", expanded=False):
                render_topic(topic)

st.markdown("---")
st.caption(
    f"📊 Data & Statistics Cheat Sheet · {len(filtered)} topics shown · 🐍 Python examples included")

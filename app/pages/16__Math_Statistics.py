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
        margin-bottom: 0.6rem;
    }
    .beginner     { background: #dcfce7; color: #166534; }
    .intermediate { background: #dbeafe; color: #1e40af; }
    .advanced     { background: #fff3cd; color: #92400e; }
    .ds           { background: #f3e8ff; color: #6b21a8; }
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
st.markdown("#### A structured reference for analysts and data scientists")
st.markdown("---")


def render_topic(t):
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


sections = {
    "🟢 Beginner": {
        "badge": "beginner",
        "topics": [
            {
                "title": "1. Percentages & Proportions",
                "definition": "A proportion expresses a part relative to a whole, either as a decimal (0–1) or a percentage (0–100%).",
                "formula": "Percentage  = (Part / Whole) × 100\nProportion  = Part / Whole",
                "description": "Proportions and percentages are the most fundamental building blocks of data analysis. Every rate, share, or conversion figure is fundamentally a proportion.",
                "example": "500 purchases out of 10,000 visitors → 500 / 10,000 = 0.05 → <strong>5% conversion rate</strong>",
                "use_cases": ["Conversion rate tracking", "Market share analysis", "Funnel stage drop-off", "Survey response breakdowns"],
                "watch_out": "Always confirm what the denominator is. '50% increase' means nothing without knowing the base.",
                "python_code": """\
import pandas as pd
import numpy as np

# --- Basic proportion & percentage ---
part, whole = 500, 10_000
proportion = part / whole          # 0.05
percentage  = proportion * 100     # 5.0
print(f"Proportion: {proportion:.4f}  |  Percentage: {percentage:.2f}%")

# --- With a DataFrame ---
df = pd.DataFrame({
    "stage": ["visited", "signed_up", "purchased"],
    "users":  [10_000,    1_500,        500],
})
df["proportion"] = df["users"] / df["users"].iloc[0]
df["pct"]        = df["proportion"] * 100
print(df)

# --- value_counts with normalize ---
statuses = pd.Series(["active","active","churned","active","churned","trial"])
print(statuses.value_counts(normalize=True) * 100)   # % share per category
"""
            },
            {
                "title": "2. Rates of Change",
                "definition": "The percentage increase or decrease between two values over time.",
                "formula": "Rate of Change = ((New − Old) / Old) × 100",
                "description": "Rates of change let you express growth or decline in a normalized, comparable way — regardless of the original scale of the numbers.",
                "example": "Revenue: $80K → $100K → (100K−80K)/80K × 100 = <strong>+25%</strong><br>Signups: 1,000 → 850 → (850−1000)/1000 × 100 = <strong>−15%</strong>",
                "use_cases": ["Monthly/quarterly KPI reporting", "User growth tracking", "Revenue trend analysis", "Price change comparisons"],
                "watch_out": "A large % change on a tiny base is misleading. 100% growth from 2 to 4 users ≠ 100% growth from 10,000 to 20,000.",
                "python_code": """\
import pandas as pd
import numpy as np

# --- Manual rate of change ---
old, new = 80_000, 100_000
roc = (new - old) / old * 100        # 25.0 %
print(f"Rate of change: {roc:.2f}%")

# --- pandas pct_change() on a time series ---
revenue = pd.Series([80_000, 85_000, 95_000, 100_000],
                    index=pd.date_range("2024-01", periods=4, freq="ME"))
print(revenue.pct_change() * 100)    # month-over-month %

# --- np.diff for quick deltas ---
arr = np.array([1_000, 1_200, 1_050, 1_400])
changes = np.diff(arr) / arr[:-1] * 100
print(changes.round(2))              # % change between consecutive values
"""
            },
            {
                "title": "3. Year-over-Year (YoY) Comparisons",
                "definition": "Comparing a metric for the same time period across consecutive years to measure true growth while eliminating seasonal noise.",
                "formula": "YoY Growth = ((This Year − Last Year) / Last Year) × 100",
                "description": "Seasonal businesses have naturally high and low periods. Comparing December to November looks like a drop even in a great year. YoY fixes this by comparing equivalent periods.",
                "example": "Dec 2023 revenue = $120K, Dec 2024 = $150K → YoY = <strong>+25%</strong>. Always compare Dec vs Dec, not Dec vs Nov.",
                "use_cases": ["Retail and e-commerce performance", "Subscription revenue tracking", "Seasonal demand analysis", "Executive dashboards"],
                "watch_out": "One-off events (pandemic years, product launches) distort YoY. Always annotate anomalies on your charts.",
                "python_code": """\
import pandas as pd

# --- Build a monthly revenue series ---
dates   = pd.date_range("2023-01", periods=24, freq="ME")
revenue = pd.Series([120,130,125,140,150,160,170,155,145,135,140,150,
                     145,155,150,165,175,185,200,180,170,160,165,175],
                    index=dates, name="revenue_k")

df = revenue.reset_index().rename(columns={"index": "date"})
df["year"]  = df["date"].dt.year
df["month"] = df["date"].dt.month

# Pivot and compute YoY
pivot = df.pivot(index="month", columns="year", values="revenue_k")
pivot["yoy_pct"] = (pivot[2024] - pivot[2023]) / pivot[2023] * 100
print(pivot.round(2))

# --- shift() approach ---
df_sorted = df.sort_values("date")
df_sorted["prev_year_rev"] = df_sorted["revenue_k"].shift(12)
df_sorted["yoy_pct"]       = (
    (df_sorted["revenue_k"] - df_sorted["prev_year_rev"])
    / df_sorted["prev_year_rev"] * 100
)
print(df_sorted.dropna().tail(6))
"""
            },
            {
                "title": "4. Mean, Median, Mode",
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

# --- describe() gives everything at once ---
s = pd.Series(salaries)
print(s.describe())

# --- Trimmed mean (ignores top/bottom 10%) ---
trimmed = stats.trim_mean(salaries, proportiontocut=0.1)
print(f"Trimmed mean: {trimmed:,.0f}")
"""
            },
            {
                "title": "5. Range, Variance & Std. Deviation",
                "definition": "Measures of spread that describe how dispersed or consistent the values in a dataset are.",
                "formula": "Range    = Max − Min\nVariance = Σ(x − μ)² / n\nStd Dev  = √Variance",
                "description": "Spread tells you how reliable your average is. A mean of 50 with SD=2 means values cluster tightly. The same mean with SD=30 means values scatter wildly.",
                "example": "Scores [48,49,50,51,52] → SD ≈ 1.4 (consistent)<br>Scores [10,30,50,70,90] → SD ≈ 28.3 (spread out)",
                "use_cases": ["Quality control (manufacturing)", "Risk assessment in finance", "Model performance evaluation", "A/B test variance analysis"],
                "watch_out": "Variance is in squared units — harder to interpret directly. Always prefer std. deviation when communicating to stakeholders.",
                "python_code": """\
import numpy as np
import pandas as pd
from scipy import stats

scores = np.array([48, 49, 50, 51, 52])
spread = np.array([10, 30, 50, 70, 90])

for arr, label in [(scores, "tight"), (spread, "wide")]:
    print(f"--- {label} ---")
    print(f"  Range    : {arr.max() - arr.min()}")
    print(f"  Variance : {np.var(arr, ddof=1):.2f}")   # ddof=1 → sample variance
    print(f"  Std Dev  : {np.std(arr, ddof=1):.2f}")
    print(f"  IQR      : {stats.iqr(arr):.2f}")

# --- pandas convenience ---
df = pd.DataFrame({"tight": scores, "wide": spread})
print(df.std())          # sample std dev (ddof=1 by default)
print(df.var())          # sample variance
"""
            },
            {
                "title": "6. Basic Probability",
                "definition": "The likelihood of a specific event occurring, expressed as a number between 0 (impossible) and 1 (certain).",
                "formula": "P(event)  = Favorable outcomes / Total outcomes\nP(not A)  = 1 − P(A)\nP(A or B) = P(A) + P(B) − P(A and B)",
                "description": "Probability is the foundation of all predictive modeling and decision-making under uncertainty. Every classifier, risk model, and simulation relies on it.",
                "example": "20 out of 100 users churned → P(churn) = 0.2 → P(no churn) = 1 − 0.2 = <strong>0.8</strong>",
                "use_cases": ["Churn prediction models", "Lead scoring", "Fraud detection thresholds", "Insurance risk models"],
                "watch_out": "Don't confuse probability with frequency. P=0.2 means a 20% chance — not that exactly 1 in 5 events will always occur.",
                "python_code": """\
import numpy as np
from scipy import stats

# --- Basic probability from data ---
churned = np.array([0]*80 + [1]*20)   # 100 users, 20 churned
p_churn    = churned.mean()            # 0.20
p_no_churn = 1 - p_churn              # 0.80
print(f"P(churn) = {p_churn:.2f}  |  P(no churn) = {p_no_churn:.2f}")

# --- Binomial: P(exactly k successes in n trials) ---
n, p, k = 10, 0.2, 3
binom = stats.binom(n, p)
print(f"P(exactly 3 churn in 10) = {binom.pmf(k):.4f}")
print(f"P(at most 3 churn in 10) = {binom.cdf(k):.4f}")

# --- Monte Carlo estimate ---
rng = np.random.default_rng(42)
simulated = rng.binomial(1, 0.2, size=100_000)
print(f"Simulated P(churn) ≈ {simulated.mean():.4f}")
"""
            },
            {
                "title": "7. Frequency Distributions & Histograms",
                "definition": "A frequency distribution shows how many times each value (or range) appears in a dataset. A histogram is its visual form.",
                "formula": "Relative Frequency = Count in bin / Total count",
                "description": "Histograms reveal the shape of your data. This shape matters because many statistical methods assume normality.\n\n- **Normal**: symmetric bell\n- **Right-skewed**: long right tail (e.g., income)\n- **Left-skewed**: long left tail (e.g., age at retirement)\n- **Bimodal**: two peaks → two subpopulations",
                "example": "Plotting user session lengths: most users cluster at 2–5 min, but power users go 60+ min → right-skewed distribution.",
                "use_cases": ["Exploratory data analysis (EDA)", "Detecting outliers and anomalies", "Choosing the right statistical test", "Feature distribution checks before modeling"],
                "watch_out": "Bin size matters! Too few bins hides structure; too many creates noise. Try multiple bin widths before deciding.",
                "python_code": """\
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(42)
sessions = np.concatenate([
    rng.exponential(scale=4, size=900),   # typical users
    rng.uniform(30, 90, size=100),        # power users
])

# --- numpy histogram (counts) ---
counts, edges = np.histogram(sessions, bins=30)
rel_freq = counts / counts.sum()

# --- pandas cut for binning ---
s = pd.Series(sessions)
binned = pd.cut(s, bins=10)
print(binned.value_counts().sort_index())

# --- plot ---
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(sessions, bins=30, edgecolor="white", color="#3b82f6", alpha=0.8)
ax.set_xlabel("Session length (min)")
ax.set_ylabel("Count")
ax.set_title("User session distribution")
plt.tight_layout()
plt.savefig("histogram.png", dpi=150)
plt.show()

# --- skewness & kurtosis ---
print(f"Skewness : {stats.skew(sessions):.3f}")
print(f"Kurtosis : {stats.kurtosis(sessions):.3f}")
"""
            },
            {
                "title": "8. Data Types",
                "definition": "A classification for the kind of values a variable holds, which determines valid statistical operations and appropriate chart types.",
                "formula": "N/A — this is a conceptual framework",
                "description": "| Type | Subtype | Examples | Valid Operations |\n|------|---------|----------|------------------|\n| Categorical | Nominal | Country, color, plan | Count, mode |\n| Categorical | Ordinal | Rating (low/mid/high) | Count, rank |\n| Numerical | Discrete | # orders, clicks | All arithmetic |\n| Numerical | Continuous | Revenue, time | All arithmetic + calculus |",
                "example": "Customer plan (Free/Pro/Enterprise) = nominal. Satisfaction score (1–5) = ordinal. Monthly revenue ($) = continuous.",
                "use_cases": ["Choosing the right chart type", "Selecting appropriate statistical tests", "Encoding variables for ML models"],
                "watch_out": "Numeric-looking codes (zip codes, user IDs) are actually categorical. Averaging zip codes produces meaningless results.",
                "python_code": """\
import pandas as pd

df = pd.DataFrame({
    "user_id":      [101, 102, 103, 104],          # nominal (don't average!)
    "plan":         ["Free","Pro","Enterprise","Free"],  # nominal
    "satisfaction": pd.Categorical([3,5,4,2],
                        categories=[1,2,3,4,5], ordered=True),  # ordinal
    "orders":       [2, 15, 8, 1],                 # discrete numeric
    "revenue":      [0.0, 299.99, 99.99, 0.0],     # continuous numeric
})

print(df.dtypes)
print("\\n--- Inspect each type ---")
print(df.select_dtypes(include="number").describe())        # numeric summary
print(df["plan"].value_counts())                            # categorical counts
print(df["satisfaction"].value_counts().sort_index())       # ordinal counts

# --- Convert to proper types ---
df["plan"] = df["plan"].astype("category")
df["user_id"] = df["user_id"].astype(str)   # prevent accidental arithmetic
print(df.dtypes)
"""
            },
            {
                "title": "9. Pareto Analysis (80/20 Rule)",
                "definition": "The observation that roughly 80% of effects come from 20% of causes, used to prioritize high-impact actions.",
                "formula": "Cumulative % = Σ(sorted values) / Total × 100\nIdentify the 20% where cumulative crosses ~80%",
                "description": "Originally observed in wealth distribution, the Pareto principle appears across business: customers, bugs, revenue drivers, and more. Sort, cumulate, and find the cutoff.",
                "example": "20% of your customers generate 80% of revenue. Identify those customers, analyze their traits, and prioritize retention efforts on them.",
                "use_cases": ["Customer value segmentation", "Bug prioritization in engineering", "Support ticket root cause analysis", "Supply chain optimization"],
                "watch_out": "The 80/20 split is a heuristic — in some contexts it's 90/10 or 70/30. It's a principle for prioritization, not a universal law.",
                "python_code": """\
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

# --- Pareto chart ---
fig, ax1 = plt.subplots(figsize=(10, 4))
ax1.bar(df["customer"], df["revenue"], color="#3b82f6", alpha=0.7)
ax2 = ax1.twinx()
ax2.plot(df["customer"], df["cum_pct"], color="#f97316", linewidth=2)
ax2.axhline(80, linestyle="--", color="red", linewidth=1, label="80% line")
ax1.set_xticklabels(df["customer"], rotation=90, fontsize=6)
ax2.set_ylabel("Cumulative %")
ax1.set_ylabel("Revenue ($)")
plt.title("Pareto Chart — Customer Revenue")
plt.tight_layout()
plt.savefig("pareto.png", dpi=150)
plt.show()
"""
            },
        ]
    },

    "🔵 Intermediate": {
        "badge": "intermediate",
        "topics": [
            {
                "title": "10. Z-Scores & Normal Distribution",
                "definition": "A Z-score measures how many standard deviations a value is from the mean. The normal distribution is a symmetric bell-shaped distribution defined by its mean and std. deviation.",
                "formula": "Z = (x − μ) / σ\n\nEmpirical Rule:\n  68%  of data within ±1 SD\n  95%  of data within ±2 SD\n  99.7% of data within ±3 SD",
                "description": "Z-scores standardize values across different scales, making them directly comparable. They're the foundation for hypothesis tests, outlier detection, and anomaly flagging.",
                "example": "μ = $50, σ = $10. An order of $80 → Z = (80−50)/10 = <strong>3.0</strong> → top 0.13% — likely a VIP or data entry error.",
                "use_cases": ["Outlier and anomaly detection", "Standardizing features before ML", "Comparing scores across different scales", "Fraud detection"],
                "watch_out": "Z-scores assume normality. On heavily skewed data, use the modified Z-score (based on median and MAD) instead.",
                "python_code": """\
import numpy as np
import pandas as pd
from scipy import stats

orders = np.array([30, 45, 50, 52, 48, 55, 80, 51, 49, 200])

# --- Manual Z-score ---
mu, sigma = orders.mean(), orders.std(ddof=1)
z_scores = (orders - mu) / sigma
print(pd.DataFrame({"order": orders, "z_score": z_scores.round(2)}))

# --- scipy zscore ---
z = stats.zscore(orders, ddof=1)

# --- Flag outliers beyond ±3 SD ---
outliers = orders[np.abs(z) > 3]
print(f"Outliers: {outliers}")

# --- Percentile from Z ---
z_val = (80 - 50) / 10
percentile = stats.norm.cdf(z_val) * 100
print(f"Z=3.0 → top {100 - percentile:.2f}% of orders")

# --- sklearn StandardScaler (preferred for ML pipelines) ---
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaled = scaler.fit_transform(orders.reshape(-1, 1))
print(scaled.flatten().round(2))
"""
            },
            {
                "title": "11. Correlation (Pearson & Spearman)",
                "definition": "A measure of the strength and direction of the relationship between two variables, ranging from −1 to +1.",
                "formula": "Pearson r  = Σ((x−x̄)(y−ȳ)) / (n·σx·σy)\nSpearman ρ = 1 − (6·Σd²) / (n·(n²−1))\n\n|r| < 0.3  → weak\n|r| 0.3–0.7 → moderate\n|r| > 0.7  → strong",
                "description": "| Method | Measures | When to Use |\n|--------|----------|-------------|\n| Pearson | Linear relationship | Continuous, normally distributed data |\n| Spearman | Monotonic relationship | Ordinal or ranked data |",
                "example": "Ad spend vs revenue: r = 0.85 → strong positive correlation. As ad spend increases, revenue tends to increase.",
                "use_cases": ["Feature selection for ML models", "Identifying business drivers", "Multicollinearity checks in regression"],
                "watch_out": "<strong>Correlation ≠ causation.</strong> Ice cream sales and drowning rates are correlated (both driven by summer). Always seek a causal mechanism.",
                "python_code": """\
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(42)
df = pd.DataFrame({
    "ad_spend": rng.uniform(1_000, 10_000, 100),
    "revenue":  rng.uniform(5_000, 50_000, 100),
    "rating":   rng.integers(1, 6, 100),
})
df["revenue"] += df["ad_spend"] * 3   # induce correlation

# --- pandas corr matrix ---
print(df.corr(method="pearson").round(3))

# --- scipy for p-values ---
r, p = stats.pearsonr(df["ad_spend"], df["revenue"])
rho, p2 = stats.spearmanr(df["ad_spend"], df["revenue"])
print(f"Pearson r={r:.3f} (p={p:.4f})")
print(f"Spearman ρ={rho:.3f} (p={p2:.4f})")

# --- Heatmap ---
fig, ax = plt.subplots(figsize=(5, 4))
sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
plt.tight_layout()
plt.savefig("correlation_heatmap.png", dpi=150)
plt.show()
"""
            },
            {
                "title": "12. Hypothesis Testing & P-Values",
                "definition": "A formal framework for determining whether an observed effect is statistically significant or likely due to random chance.",
                "formula": "H₀: no effect (null hypothesis)\nH₁: effect exists (alternative hypothesis)\n\np-value = P(seeing this result | H₀ is true)\np < 0.05  → reject H₀  (statistically significant)\np ≥ 0.05  → fail to reject H₀",
                "description": "Common tests:\n- **t-test**: compare means of two groups\n- **Chi-square**: compare categorical distributions\n- **ANOVA**: compare means across 3+ groups\n\nThe p-value answers: 'If nothing changed, how likely is this result by chance?'",
                "example": "Variant B: 4.5% conversion vs control: 4.0%. p = 0.03 → significant at α=0.05 → safe to ship.",
                "use_cases": ["A/B test analysis", "Product experiment evaluation", "Clinical trial analysis", "Quality control testing"],
                "watch_out": "p < 0.05 ≠ 'large effect' or 'practically important.' A tiny difference can be significant with a huge sample. Always report effect size alongside the p-value.",
                "python_code": """\
import numpy as np
from scipy import stats

rng = np.random.default_rng(42)
control  = rng.normal(loc=4.0, scale=1.0, size=500)  # 4% conv
variant  = rng.normal(loc=4.5, scale=1.0, size=500)  # 4.5% conv

# --- Independent t-test ---
t_stat, p_val = stats.ttest_ind(control, variant)
print(f"t={t_stat:.3f}  p={p_val:.4f}")
print("Significant!" if p_val < 0.05 else "Not significant")

# --- Effect size (Cohen's d) ---
pooled_std = np.sqrt((control.std()**2 + variant.std()**2) / 2)
cohens_d   = (variant.mean() - control.mean()) / pooled_std
print(f"Cohen's d = {cohens_d:.3f}  (small<0.2, medium<0.5, large>0.8)")

# --- Chi-square (categorical) ---
observed = np.array([[400, 100], [420, 80]])   # [control, variant] x [no/yes]
chi2, p_chi, dof, expected = stats.chi2_contingency(observed)
print(f"Chi2={chi2:.3f}  p={p_chi:.4f}")

# --- One-way ANOVA (3+ groups) ---
g1 = rng.normal(50, 10, 100)
g2 = rng.normal(55, 10, 100)
g3 = rng.normal(60, 10, 100)
f_stat, p_anova = stats.f_oneway(g1, g2, g3)
print(f"ANOVA F={f_stat:.3f}  p={p_anova:.4f}")
"""
            },
            {
                "title": "13. Confidence Intervals",
                "definition": "A range of values that, with a specified level of confidence (typically 95%), contains the true population parameter.",
                "formula": "CI = x̄ ± (z* × SE)\nSE  = σ / √n\n\nz* for 95% CI = 1.96\nz* for 99% CI = 2.576",
                "description": "A 95% CI means: if you repeated this experiment 100 times, ~95 of those intervals would contain the true value. It is NOT a 95% probability that this specific interval contains the true value.",
                "example": "Conversion rate: 4.2%, n=2,000 → 95% CI = [3.8%, 4.6%]. We're 95% confident the true rate is within this range.",
                "use_cases": ["Reporting survey results", "A/B test decision-making", "Presenting model accuracy ranges", "Communicating uncertainty to stakeholders"],
                "watch_out": "Wider CI = less precision, not a flaw. Chasing narrow CIs by ignoring uncertainty misleads decision-makers.",
                "python_code": """\
import numpy as np
from scipy import stats
import statsmodels.stats.proportion as smp

rng = np.random.default_rng(42)
data = rng.normal(loc=4.2, scale=1.0, size=2_000)

# --- t-interval for a mean ---
ci = stats.t.interval(0.95, df=len(data)-1,
                      loc=data.mean(),
                      scale=stats.sem(data))
print(f"Mean CI 95%: {ci[0]:.3f} – {ci[1]:.3f}")

# --- Proportion CI (e.g. conversion rate) ---
n, successes = 2_000, 84   # 4.2% of 2000
ci_prop = smp.proportion_confint(successes, n, alpha=0.05, method="wilson")
print(f"Proportion CI 95%: {ci_prop[0]*100:.2f}% – {ci_prop[1]*100:.2f}%")

# --- Bootstrap CI (model-free) ---
boot_means = [rng.choice(data, size=len(data), replace=True).mean()
              for _ in range(5_000)]
boot_means = np.array(boot_means)
boot_ci = np.percentile(boot_means, [2.5, 97.5])
print(f"Bootstrap CI 95%: {boot_ci[0]:.3f} – {boot_ci[1]:.3f}")
"""
            },
            {
                "title": "14. Sampling & Sampling Bias",
                "definition": "Sampling selects a subset of a population for analysis. Sampling bias occurs when the sample systematically differs from the population it represents.",
                "formula": "Margin of Error = z* × √(p(1−p)/n)\nRequired n ≈ (z*/ME)² × p(1−p)",
                "description": "**Types of bias:**\n- **Selection bias**: non-random inclusion\n- **Survivorship bias**: analyzing only those who 'survived'\n- **Response bias**: self-selection skews who responds\n- **Convenience bias**: sampling whoever is easiest to reach",
                "example": "Surveying NPS only from users who logged in this month excludes churned users — making satisfaction look artificially high.",
                "use_cases": ["Survey design", "A/B test setup", "Market research", "Product feedback analysis"],
                "watch_out": "Always ask: 'Who is NOT in my sample and why?' The absence of data is often as informative as the data itself.",
                "python_code": """\
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(42)
df = pd.DataFrame({
    "user_id": range(10_000),
    "plan":    rng.choice(["free","pro","enterprise"], 10_000, p=[0.7,0.2,0.1]),
    "revenue": rng.exponential(50, 10_000),
})

# --- Simple random sample ---
sample_random = df.sample(n=500, random_state=42)

# --- Stratified sample (preserves plan proportions) ---
sample_strat = df.groupby("plan", group_keys=False).apply(
    lambda x: x.sample(frac=0.05, random_state=42)
)
print("Stratified sample plan distribution:")
print(sample_strat["plan"].value_counts(normalize=True).round(3))

# --- Train/test split (stratified) ---
X = df.drop(columns="revenue")
y = df["revenue"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=df["plan"], random_state=42
)
print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")

# --- Required sample size for a proportion ---
from statsmodels.stats.proportion import samplesize_confint_proportion
n_required = samplesize_confint_proportion(0.5, half_length=0.03, alpha=0.05)
print(f"Required n for ±3% margin: {int(np.ceil(n_required))}")
"""
            },
            {
                "title": "15. Linear Regression & Coefficients",
                "definition": "A statistical model that estimates the relationship between one or more independent variables (X) and a dependent variable (Y) by fitting a line.",
                "formula": "Simple:   Y = β₀ + β₁X + ε\nMultiple: Y = β₀ + β₁X₁ + β₂X₂ + ... + ε\n\nR² = 1 − (SS_res / SS_tot)",
                "description": "- **β₀ (intercept)**: predicted Y when all X = 0\n- **β₁ (coefficient)**: change in Y per 1-unit increase in X\n- **R²**: proportion of variance explained by the model\n- **Residuals (ε)**: the unexplained portion — should be random",
                "example": "β₁ for ad spend = 2.5 → every $1 more in ads is associated with $2.50 more in revenue (holding other factors constant).",
                "use_cases": ["Demand forecasting", "Price elasticity analysis", "Sales attribution modeling", "Feature importance estimation"],
                "watch_out": "R² inflates as you add variables. Use Adjusted R² for multiple regression. Regression shows association, not causation.",
                "python_code": """\
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import statsmodels.api as sm

rng = np.random.default_rng(42)
ad_spend = rng.uniform(1_000, 10_000, 200)
revenue  = 5_000 + 2.5 * ad_spend + rng.normal(0, 2_000, 200)

# --- sklearn ---
X = ad_spend.reshape(-1, 1)
y = revenue
model = LinearRegression().fit(X, y)
print(f"Intercept β₀ : {model.intercept_:,.2f}")
print(f"Coefficient β₁: {model.coef_[0]:.4f}")
print(f"R²           : {r2_score(y, model.predict(X)):.4f}")
print(f"RMSE         : {mean_squared_error(y, model.predict(X))**0.5:,.2f}")

# --- statsmodels (gives p-values and CIs) ---
X_sm = sm.add_constant(ad_spend)
ols  = sm.OLS(revenue, X_sm).fit()
print(ols.summary())
"""
            },
            {
                "title": "16. Conditional Probability & Bayes' Theorem",
                "definition": "Conditional probability is the likelihood of event A given event B has occurred. Bayes' theorem updates probabilities as new evidence arrives.",
                "formula": "P(A|B) = P(A and B) / P(B)\n\nBayes' Theorem:\nP(A|B) = P(B|A) × P(A) / P(B)\n\nPosterior ∝ Likelihood × Prior",
                "description": "Bayes formalizes belief updating: start with a prior, observe evidence, update to a posterior. This is how spam filters, medical diagnostics, and recommendation systems work.",
                "example": "99% accurate test, 1% disease prevalence. P(disease | positive test) ≈ <strong>50%</strong> — surprisingly low due to rare base rate. Most positives are false alarms.",
                "use_cases": ["Spam email classification", "Medical diagnosis models", "Lead scoring with RFM", "Fraud detection"],
                "watch_out": "Base rate neglect is extremely common. Even a highly accurate test produces mostly false positives for rare conditions.",
                "python_code": """\
import numpy as np
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.datasets import load_iris

# --- Manual Bayes (medical test example) ---
p_disease   = 0.01       # prevalence (prior)
p_pos_given_disease   = 0.99   # sensitivity
p_pos_given_no_disease = 0.01  # 1 - specificity (false positive rate)

p_positive = (p_pos_given_disease * p_disease +
              p_pos_given_no_disease * (1 - p_disease))
p_disease_given_pos = (p_pos_given_disease * p_disease) / p_positive

print(f"P(disease | positive test) = {p_disease_given_pos:.4f}  "
      f"({p_disease_given_pos*100:.1f}%)")

# --- sklearn Naive Bayes classifier ---
iris = load_iris()
X, y = iris.data, iris.target
nb = GaussianNB()
nb.fit(X, y)
sample = np.array([[5.1, 3.5, 1.4, 0.2]])
probs  = nb.predict_proba(sample)[0]
print("Class probabilities:", dict(zip(iris.target_names, probs.round(4))))
"""
            },
            {
                "title": "17. Cohort & Segmentation Analysis",
                "definition": "Cohort analysis groups users who share a common characteristic at a specific point in time and tracks their behavior over time.",
                "formula": "Retention Rate at period n =\n  (Active users from cohort still active at n) / Original cohort size × 100",
                "description": "Cohorts separate the effect of time (how long a user has been around) from calendar period (what's happening in the product now). Without cohorts, new retention improvements can be hidden by old cohorts churning.",
                "example": "Jan cohort: 40% retention at 6 months. Jun cohort: 25% at 6 months → product or acquisition quality likely declined.",
                "use_cases": ["SaaS retention analysis", "LTV calculation", "Evaluating product changes over time", "Acquisition channel quality comparison"],
                "watch_out": "Don't compare cohorts of different sizes without normalization. Distinguish early churn (onboarding failure) from long-term churn (value decay).",
                "python_code": """\
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)
n = 2_000
df = pd.DataFrame({
    "user_id":    range(n),
    "signup_date": pd.to_datetime(
        rng.choice(pd.date_range("2024-01-01","2024-06-01", freq="D"), n)
    ),
    "last_active": pd.to_datetime(
        rng.choice(pd.date_range("2024-01-01","2024-12-01", freq="D"), n)
    ),
})
df["cohort_month"] = df["signup_date"].dt.to_period("M")
df["active_month"] = df["last_active"].dt.to_period("M")
df["periods_since"] = (df["active_month"] - df["cohort_month"]).apply(lambda x: x.n)

cohort_size = df.groupby("cohort_month")["user_id"].nunique()
retention   = df.groupby(["cohort_month","periods_since"])["user_id"].nunique()
retention   = retention.reset_index()
retention   = retention.pivot(index="cohort_month", columns="periods_since", values="user_id")
retention   = retention.divide(cohort_size, axis=0).round(3) * 100

# --- Heatmap ---
fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(retention.iloc[:, :7], annot=True, fmt=".0f",
            cmap="YlGnBu", ax=ax, cbar_kws={"label": "Retention %"})
ax.set_title("Monthly Cohort Retention (%)")
plt.tight_layout()
plt.savefig("cohort_heatmap.png", dpi=150)
plt.show()
"""
            },
        ]
    },

    "🟠 Advanced": {
        "badge": "advanced",
        "topics": [
            {
                "title": "18. Multiple Regression",
                "definition": "An extension of linear regression that models the relationship between a dependent variable and two or more independent variables simultaneously.",
                "formula": "Y = β₀ + β₁X₁ + β₂X₂ + β₃X₃ + ε\n\nAdjusted R² = 1 − [(1−R²)(n−1)/(n−k−1)]\nVIF > 10   → multicollinearity problem",
                "description": "Multiple regression isolates each variable's effect while controlling for others.\n\n**Key checks before trusting results:**\n- **Multicollinearity**: correlated predictors distort coefficients (use VIF)\n- **Heteroscedasticity**: unequal residual variance (use Breusch-Pagan test)\n- **Overfitting**: high train R², low test R²",
                "example": "Revenue = 10,000 + 2.5(AdSpend) + 500(SalesReps) − 200(ChurnRate). Each coefficient is interpreted holding all other variables constant.",
                "use_cases": ["Marketing mix modeling", "Price optimization", "Sales forecasting", "Causal inference (with care)"],
                "watch_out": "Adding variables always increases R². Use Adjusted R² or cross-validation to assess true quality. Never trust coefficients without checking all assumptions.",
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
    "sales_reps": rng.integers(1, 20, n),
    "churn_rate": rng.uniform(0.01, 0.3, n),
})
df["revenue"] = (10_000
                 + 2.5 * df["ad_spend"]
                 + 500  * df["sales_reps"]
                 - 200  * df["churn_rate"] * 100
                 + rng.normal(0, 3_000, n))

# --- statsmodels OLS with full summary ---
X = sm.add_constant(df[["ad_spend","sales_reps","churn_rate"]])
ols = sm.OLS(df["revenue"], X).fit()
print(ols.summary())

# --- VIF check ---
vif_data = pd.DataFrame({
    "feature": X.columns,
    "VIF":     [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
})
print(vif_data)

# --- Cross-validated R² ---
lr = LinearRegression()
cv_scores = cross_val_score(lr, df[["ad_spend","sales_reps","churn_rate"]],
                            df["revenue"], cv=5, scoring="r2")
print(f"CV R²: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
"""
            },
            {
                "title": "19. Time Series Basics",
                "definition": "A sequence of data points collected at successive, equally-spaced intervals. Time series analysis decomposes, models, and forecasts these sequences.",
                "formula": "Decomposition: Y(t) = Trend(t) + Seasonality(t) + Noise(t)\nMoving Avg:    MA(k) = (1/k) × Σ Yᵢ  [i = t−k+1 to t]",
                "description": "**Components:**\n- **Trend**: long-term direction\n- **Seasonality**: repeating patterns at fixed intervals\n- **Cyclicality**: irregular longer waves (economic cycles)\n- **Noise**: random unexplained variation\n\nCommon models: ARIMA, Exponential Smoothing, Facebook Prophet",
                "example": "E-commerce sales: upward trend (growth) + December spikes (seasonality) + daily noise. A 7-day moving average smooths the noise to reveal the trend.",
                "use_cases": ["Demand forecasting", "Financial market analysis", "Anomaly detection in metrics", "Capacity planning"],
                "watch_out": "Many models (ARIMA) require stationarity — mean and variance must not change over time. Always test with the Augmented Dickey-Fuller (ADF) test first.",
                "python_code": """\
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

rng = np.random.default_rng(42)
dates = pd.date_range("2022-01-01", periods=104, freq="W")
trend = np.linspace(100, 200, 104)
seasonal = 20 * np.sin(2 * np.pi * np.arange(104) / 52)
noise = rng.normal(0, 5, 104)
sales = pd.Series(trend + seasonal + noise, index=dates, name="sales")

# --- Moving averages ---
sales_df = sales.to_frame()
sales_df["MA7"]  = sales.rolling(7).mean()
sales_df["MA13"] = sales.rolling(13).mean()

# --- Decomposition ---
result = seasonal_decompose(sales, model="additive", period=52)
result.plot()
plt.tight_layout()
plt.savefig("ts_decompose.png", dpi=150)
plt.show()

# --- ADF stationarity test ---
adf_stat, p_val, *_ = adfuller(sales)
print(f"ADF Statistic: {adf_stat:.4f}  p-value: {p_val:.4f}")
print("Stationary" if p_val < 0.05 else "Not stationary → consider differencing")

# --- First difference to achieve stationarity ---
sales_diff = sales.diff().dropna()
adf2, p2, *_ = adfuller(sales_diff)
print(f"After diff: ADF={adf2:.4f}  p={p2:.4f}")
"""
            },
            {
                "title": "20. A/B Testing & Experimental Design",
                "definition": "A controlled experiment that randomly assigns users to variants to measure the causal impact of a change on a defined metric.",
                "formula": "Min sample size per variant:\nn ≈ 2σ²(z_α/2 + z_β)² / δ²\n\nz_α/2 = 1.96  (95% confidence)\nz_β   = 0.84  (80% power)\nδ = minimum detectable effect",
                "description": "**Best practices:**\n1. Formulate hypothesis before running\n2. Pre-calculate required sample size\n3. Randomize assignment (not by date)\n4. Define one primary metric upfront\n5. Do NOT stop early (p-hacking)\n6. Run for full business cycles (full weeks)",
                "example": "Hypothesis: blue CTA button increases signups vs grey. Run until n=5,000 per variant. Result: blue=4.8%, grey=4.0%, p=0.02 → statistically significant → ship it.",
                "use_cases": ["Product feature launches", "Email subject line optimization", "Pricing page changes", "Onboarding flow improvements"],
                "watch_out": "Early stopping is the #1 mistake. Random fluctuation makes early results unreliable. Peeking and stopping inflates your false positive rate to 25%+ even at α=0.05.",
                "python_code": """\
import numpy as np
from scipy import stats
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportions_ztest, proportion_effectsize

# --- Pre-experiment: required sample size ---
baseline_rate = 0.04    # 4% current conversion
mde           = 0.005   # detect +0.5% lift (relative or absolute)
alpha, power  = 0.05, 0.80

effect_size = proportion_effectsize(baseline_rate + mde, baseline_rate)
analysis    = NormalIndPower()
n_per_group = analysis.solve_power(effect_size=effect_size,
                                   alpha=alpha, power=power, ratio=1)
print(f"Required n per variant: {int(np.ceil(n_per_group)):,}")

# --- Simulate experiment results ---
rng = np.random.default_rng(42)
n = 5_000
control  = rng.binomial(1, 0.040, n)
variant  = rng.binomial(1, 0.048, n)

# --- Proportions z-test ---
count   = np.array([variant.sum(), control.sum()])
nobs    = np.array([len(variant),  len(control)])
z, p    = proportions_ztest(count, nobs)
print(f"z={z:.3f}  p={p:.4f}")
print("Ship it! ✓" if p < alpha else "Not significant — keep testing")

# --- Relative lift ---
lift = (variant.mean() - control.mean()) / control.mean() * 100
print(f"Relative lift: {lift:.2f}%")
"""
            },
            {
                "title": "21. Statistical Power & Sample Size",
                "definition": "Statistical power is the probability a test correctly detects a real effect when one exists (1 − β, target ≥ 0.80).",
                "formula": "Power = 1 − β  (target ≥ 0.80)\n\nPower ↑ when:\n  Sample size ↑\n  Effect size ↑\n  α ↑ (less strict)\n  Variance ↓",
                "description": "| | H₀ True | H₀ False |\n|--|---------|----------|\n| Reject H₀ | ❌ Type I Error (α) | ✅ Correct |\n| Fail to Reject | ✅ Correct | ❌ Type II Error (β) |\n\nUnderpowered tests miss real effects. Overpowered tests detect trivially small, irrelevant effects.",
                "example": "Testing 0.5% lift on a 4% base conversion requires ~75,000 users per variant at 80% power. Low-traffic sites may need months to reach this.",
                "use_cases": ["A/B test planning", "Clinical trial design", "Minimum viable experiment scoping"],
                "watch_out": "Post-hoc power analysis (calculating power after seeing results) is misleading. Always calculate required sample size before starting the experiment.",
                "python_code": """\
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.power import TTestIndPower, NormalIndPower

# --- Solve for sample size ---
analysis = TTestIndPower()
n = analysis.solve_power(effect_size=0.3, alpha=0.05, power=0.80)
print(f"n per group for d=0.3, α=0.05, power=0.80: {int(np.ceil(n))}")

# --- Power curve: power vs sample size ---
sample_sizes = np.arange(10, 500, 10)
powers = [analysis.solve_power(effect_size=0.3, alpha=0.05, nobs1=n, ratio=1)
          for n in sample_sizes]

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(sample_sizes, powers, linewidth=2, color="#3b82f6")
ax.axhline(0.80, linestyle="--", color="#f97316", label="80% power target")
ax.axvline(int(np.ceil(n)), linestyle="--", color="#22c55e", label=f"n={int(np.ceil(n))}")
ax.set_xlabel("Sample size per group")
ax.set_ylabel("Power")
ax.set_title("Statistical Power vs Sample Size (d=0.3, α=0.05)")
ax.legend()
plt.tight_layout()
plt.savefig("power_curve.png", dpi=150)
plt.show()
"""
            },
            {
                "title": "22. Survival / Retention Analysis",
                "definition": "Statistical methods for modeling the time until a specific event occurs (churn, conversion, failure), accounting for users who haven't experienced it yet (censoring).",
                "formula": "Kaplan-Meier Estimator:\nS(t) = Π [ (nᵢ − dᵢ) / nᵢ ]  for all tᵢ ≤ t\n\nnᵢ = users at risk at time t\ndᵢ = events (churn) at time t",
                "description": "**Key concepts:**\n- **S(t)**: probability of surviving (not churning) past time t\n- **Hazard rate**: instantaneous churn risk at time t\n- **Censoring**: users still active (can't be ignored)\n- **Cox Proportional Hazards**: extends survival analysis with covariates (age, plan, etc.)",
                "example": "K-M curve: 80% active at 30 days, 50% at 90 days, 30% at 180 days. Steepest drop in first 2 weeks → onboarding problem.",
                "use_cases": ["SaaS churn prediction", "Customer LTV modeling", "Medical device failure analysis", "Credit risk duration modeling"],
                "watch_out": "Censoring must be non-informative — users shouldn't drop out because they're about to churn. Violation of this biases the survival estimates significantly.",
                "python_code": """\
# pip install lifelines
import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter, CoxPHFitter

rng = np.random.default_rng(42)
n = 500
df = pd.DataFrame({
    "duration":  rng.integers(1, 365, n),       # days until churn or censoring
    "event":     rng.binomial(1, 0.6, n),        # 1 = churned, 0 = still active
    "plan_pro":  rng.binomial(1, 0.4, n),        # 1 = Pro plan
    "logins_pw": rng.poisson(5, n),              # avg logins per week
})

# --- Kaplan-Meier ---
kmf = KaplanMeierFitter()
kmf.fit(df["duration"], event_observed=df["event"], label="All users")
print(kmf.median_survival_time_)                 # median time to churn
kmf.plot_survival_function()

# --- KM by plan ---
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(8, 5))
for plan, grp in df.groupby("plan_pro"):
    kmf.fit(grp["duration"], event_observed=grp["event"],
            label=f"Pro={bool(plan)}")
    kmf.plot_survival_function(ax=ax)
ax.set_title("Survival Curve by Plan")
plt.tight_layout()
plt.savefig("survival_curve.png", dpi=150)
plt.show()

# --- Cox Proportional Hazards ---
cph = CoxPHFitter()
cph.fit(df, duration_col="duration", event_col="event")
cph.print_summary()
"""
            },
            {
                "title": "23. Simpson's Paradox & Statistical Pitfalls",
                "definition": "Simpson's Paradox: a trend that appears in aggregate data disappears or reverses when broken down by subgroups.",
                "formula": "No formula — it's a structural reasoning failure.\nCheck: Do aggregate trends match all subgroup trends?",
                "description": "**Common pitfalls:**\n- **Simpson's Paradox**: aggregate trend reverses when segmented\n- **P-hacking**: running many tests and reporting only significant ones\n- **HARKing**: Hypothesizing After Results are Known\n- **Base rate neglect**: ignoring how rare an event is\n- **Ecological fallacy**: inferring individual behavior from group statistics",
                "example": "Hospital A has higher overall survival than Hospital B. But Hospital B is better for BOTH mild and severe cases — it just handles more severe cases. Aggregate % hides this.",
                "use_cases": ["Multi-segment reporting", "Policy evaluation", "Medical and social research", "Experiment post-mortems"],
                "watch_out": "Always segment your data before drawing conclusions. A single aggregate number almost never tells the whole story.",
                "python_code": """\
import pandas as pd
import numpy as np

# --- Simpson's Paradox example ---
data = {
    "hospital": ["A","A","B","B"],
    "severity":  ["mild","severe","mild","severe"],
    "survived":  [800, 200, 900, 400],
    "total":     [900, 300, 950, 500],
}
df = pd.DataFrame(data)
df["rate"] = df["survived"] / df["total"]

# Aggregate (misleading)
agg = df.groupby("hospital")[["survived","total"]].sum()
agg["rate"] = agg["survived"] / agg["total"]
print("Aggregate survival rate:")
print(agg["rate"].round(3))

# Segmented (true picture)
print("\\nBy severity group:")
print(df.pivot(index="severity", columns="hospital", values="rate").round(3))

# --- Detecting p-hacking: multiple comparisons correction ---
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests

rng = np.random.default_rng(42)
p_values = [ttest_ind(rng.normal(0,1,100), rng.normal(0,1,100)).pvalue
            for _ in range(20)]  # 20 tests on random data

reject_raw = [p < 0.05 for p in p_values]
reject_bonf, *_ = multipletests(p_values, method="bonferroni")[:2]
reject_bh,   *_ = multipletests(p_values, method="fdr_bh")[:2]

print(f"\\nRaw α=0.05 rejections : {sum(reject_raw)} / 20")
print(f"Bonferroni rejections  : {sum(reject_bonf)} / 20")
print(f"BH FDR rejections      : {sum(reject_bh)} / 20")
"""
            },
            {
                "title": "24. Index Numbers & Weighted Averages",
                "definition": "An index expresses a value relative to a reference (base) period. A weighted average assigns different importance to values based on their relative size or relevance.",
                "formula": "Index         = (Current Value / Base Value) × 100\nWeighted Avg  = Σ(value × weight) / Σ(weight)",
                "description": "**When to use weighted averages:** When groups have very different sizes, a simple average is misleading. A 90% retention rate from 10 users should NOT be weighted equally with 90% from 10,000 users.",
                "example": "Simple avg of [50%, 90%] = 70%.<br>If group sizes are 100 and 1,000: weighted avg = (50×100 + 90×1000) / 1100 = <strong>86.4%</strong>",
                "use_cases": ["CPI and price indices", "Portfolio performance", "Blended metrics across segments", "NPS and satisfaction indices"],
                "watch_out": "Wrong weights massively distort results. Document your weighting methodology explicitly, and revisit it as group sizes change over time.",
                "python_code": """\
import numpy as np
import pandas as pd

# --- Index numbers ---
prices = pd.Series([100, 108, 115, 122, 130],
                   index=[2020,2021,2022,2023,2024], name="price")
index  = prices / prices.iloc[0] * 100
print("Price index (base 2020=100):")
print(index.round(1))

# --- Weighted average vs simple average ---
segments = pd.DataFrame({
    "segment":   ["small","large"],
    "retention": [0.50, 0.90],
    "users":     [100,   1_000],
})
simple   = segments["retention"].mean()
weighted = np.average(segments["retention"], weights=segments["users"])
print(f"\\nSimple average  : {simple*100:.1f}%")
print(f"Weighted average: {weighted*100:.1f}%")

# --- numpy average with weights ---
values  = np.array([50, 90])
weights = np.array([100, 1_000])
print(f"np.average: {np.average(values, weights=weights):.2f}%")

# --- Weighted NPS calculation ---
nps_scores = pd.DataFrame({
    "channel": ["email","app","web"],
    "nps":     [45, 62, 38],
    "users":   [5_000, 12_000, 8_000],
})
blended_nps = np.average(nps_scores["nps"], weights=nps_scores["users"])
print(f"Blended NPS: {blended_nps:.1f}")
"""
            },
        ]
    },

    "🟣 Data Science": {
        "badge": "ds",
        "topics": [
            {
                "title": "25. Entropy & Information Gain",
                "definition": "Entropy measures the impurity or disorder of a dataset. Information Gain measures how much a feature reduces entropy after a split.",
                "formula": "H(S) = −Σ pᵢ × log₂(pᵢ)\n\nIG(S,A) = H(S) − Σ (|Sᵥ|/|S|) × H(Sᵥ)",
                "description": "- H = 0 → perfectly pure (all one class)\n- H = 1 → maximum disorder (50/50 binary split)\n\nDecision tree algorithms (ID3, C4.5) greedily choose splits that maximize information gain, reducing entropy toward 0 at each node.",
                "example": "50% spam, 50% not → H=1.0. After splitting on 'contains FREE': 90% spam | 10% spam → large entropy drop → high information gain → good split.",
                "use_cases": ["Decision tree feature selection", "Random forest variable importance", "Text classification", "Feature ranking"],
                "watch_out": "Information gain favors features with many unique values (like IDs). Use Gain Ratio (C4.5) or Gini impurity (CART) to correct for this bias.",
                "python_code": """\
import numpy as np
from scipy.stats import entropy
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.feature_selection import mutual_info_classif
from sklearn.datasets import load_iris

# --- Manual entropy ---
def calc_entropy(labels):
    classes, counts = np.unique(labels, return_counts=True)
    probs = counts / counts.sum()
    return entropy(probs, base=2)

labels_mixed = np.array([0]*50 + [1]*50)   # 50/50 → max entropy
labels_pure  = np.array([0]*100)            # all same → 0 entropy
print(f"Mixed entropy : {calc_entropy(labels_mixed):.4f}")
print(f"Pure entropy  : {calc_entropy(labels_pure):.4f}")

# --- Decision tree & feature importance ---
iris = load_iris()
X, y = iris.data, iris.target
dt = DecisionTreeClassifier(criterion="entropy", max_depth=3, random_state=42)
dt.fit(X, y)
print(export_text(dt, feature_names=list(iris.feature_names)))

importance = dict(zip(iris.feature_names, dt.feature_importances_))
for feat, imp in sorted(importance.items(), key=lambda x: -x[1]):
    print(f"{feat}: {imp:.4f}")

# --- Mutual information (sklearn) ---
mi = mutual_info_classif(X, y, random_state=42)
print(dict(zip(iris.feature_names, mi.round(4))))
"""
            },
            {
                "title": "26. Bias–Variance Tradeoff",
                "definition": "The fundamental ML tension between a model too simple to capture patterns (high bias / underfitting) and one too complex that memorizes noise (high variance / overfitting).",
                "formula": "Total Error = Bias² + Variance + Irreducible Noise\n\nHigh Bias:     train error ≈ test error (both high)\nHigh Variance: train error << test error",
                "description": "| | High Bias | High Variance |\n|---|---|---|\n| Also called | Underfitting | Overfitting |\n| Train error | High | Low |\n| Test error | High | High |\n| Fix | More complexity | Regularization / more data |\n| Example | Linear model on nonlinear data | Deep tree, no pruning |",
                "example": "Decision tree depth=1 (stump): underfits. Depth=30: memorizes training data. Optimal depth (e.g., 5–7) balances both.",
                "use_cases": ["Model selection", "Hyperparameter tuning", "Diagnosing train vs. validation performance gaps"],
                "watch_out": "More data reduces variance but NOT bias. If a model is underfitting, getting more data won't help — you need to increase model capacity.",
                "python_code": """\
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import learning_curve, validation_curve
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=1_000, n_features=20,
                            random_state=42, n_informative=10)

# --- Validation curve: depth vs train/val score ---
depths = np.arange(1, 20)
train_scores, val_scores = validation_curve(
    DecisionTreeClassifier(random_state=42), X, y,
    param_name="max_depth", param_range=depths,
    cv=5, scoring="accuracy"
)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(depths, train_scores.mean(axis=1), label="Train", color="#3b82f6")
ax.plot(depths, val_scores.mean(axis=1),   label="Validation", color="#f97316")
ax.fill_between(depths,
                train_scores.mean(axis=1) - train_scores.std(axis=1),
                train_scores.mean(axis=1) + train_scores.std(axis=1), alpha=0.1)
ax.set_xlabel("max_depth")
ax.set_ylabel("Accuracy")
ax.set_title("Validation Curve — Bias–Variance")
ax.legend()
plt.tight_layout()
plt.savefig("bias_variance.png", dpi=150)
plt.show()
"""
            },
            {
                "title": "27. Cross-Validation",
                "definition": "A technique to estimate model generalization by training and testing on multiple non-overlapping splits of the data.",
                "formula": "k-Fold CV Score = (1/k) × Σ score(fold_i)\n\nReport: mean ± std across folds",
                "description": "**How k-Fold CV works:**\n1. Split data into k equal folds (typically k=5 or 10)\n2. Train on k−1 folds, test on the held-out fold\n3. Rotate until each fold has been the test set once\n4. Average the k scores\n\n**Stratified k-Fold** preserves class balance in each fold — essential for imbalanced datasets.",
                "example": "5-fold CV scores: [0.82, 0.85, 0.81, 0.84, 0.83] → CV = <strong>0.83 ± 0.015</strong>. Far more reliable than one train/test split.",
                "use_cases": ["Model selection and comparison", "Hyperparameter tuning (nested CV)", "Performance estimation before deployment"],
                "watch_out": "Data leakage through the CV loop is critical: preprocessing steps (scaling, imputation) must be fit INSIDE each fold, never on the full dataset.",
                "python_code": """\
import numpy as np
from sklearn.datasets import make_classification
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (cross_val_score, StratifiedKFold,
                                     cross_validate)

X, y = make_classification(n_samples=1_000, n_features=20,
                            random_state=42, n_informative=10)

# --- Basic cross_val_score ---
skf    = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(LogisticRegression(max_iter=1_000), X, y,
                         cv=skf, scoring="roc_auc")
print(f"AUC: {scores.mean():.4f} ± {scores.std():.4f}")

# --- Pipeline prevents data leakage ---
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("clf",    LogisticRegression(max_iter=1_000)),
])
results = cross_validate(pipe, X, y, cv=skf,
                         scoring=["accuracy","roc_auc","f1"],
                         return_train_score=True)
for metric in ["test_accuracy","test_roc_auc","test_f1"]:
    print(f"{metric}: {results[metric].mean():.4f} ± {results[metric].std():.4f}")
"""
            },
            {
                "title": "28. Regularization (L1 & L2)",
                "definition": "A technique adding a penalty to the loss function to discourage large coefficients, reducing overfitting by constraining model complexity.",
                "formula": "L1 (Lasso):   Loss = MSE + λ × Σ|βᵢ|\nL2 (Ridge):   Loss = MSE + λ × Σβᵢ²\nElastic Net:  Loss = MSE + λ₁Σ|βᵢ| + λ₂Σβᵢ²",
                "description": "| | L1 (Lasso) | L2 (Ridge) |\n|--|--|--|\n| Effect | Drives some coefficients to exactly 0 | Shrinks all toward 0 |\n| Result | Sparse model (feature selection) | Dense model |\n| Use when | Many irrelevant features | All features contribute |",
                "example": "With 100 features, Lasso (λ=0.1) zeros out 80 — effectively automatic feature selection, leaving 20 active predictors.",
                "use_cases": ["Preventing overfitting in regression", "Automatic feature selection (L1)", "Neural network weight decay (L2)", "High-dimensional datasets"],
                "watch_out": "λ is a critical hyperparameter. Too high → underfitting. Too low → no regularization. Use LassoCV or RidgeCV for automatic cross-validated tuning.",
                "python_code": """\
import numpy as np
from sklearn.linear_model import Lasso, Ridge, ElasticNet, LassoCV, RidgeCV
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

X, y = make_regression(n_samples=500, n_features=100,
                        n_informative=20, noise=30, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

for name, model in [("Lasso",      Lasso(alpha=0.5)),
                    ("Ridge",      Ridge(alpha=1.0)),
                    ("ElasticNet", ElasticNet(alpha=0.5, l1_ratio=0.5))]:
    model.fit(X_train_s, y_train)
    r2    = r2_score(y_test, model.predict(X_test_s))
    zeros = (model.coef_ == 0).sum()
    print(f"{name:12s}  R²={r2:.4f}  zero_coefs={zeros}/100")

# --- LassoCV: auto-tune alpha ---
lcv = LassoCV(cv=5, random_state=42).fit(X_train_s, y_train)
print(f"\\nLassoCV best alpha: {lcv.alpha_:.4f}")
print(f"Active features   : {(lcv.coef_ != 0).sum()}/100")
"""
            },
            {
                "title": "29. Gradient Descent",
                "definition": "An iterative optimization algorithm that minimizes a loss function by repeatedly updating parameters in the direction of the steepest negative gradient.",
                "formula": "θ := θ − α × ∇J(θ)\n\nα     = learning rate\n∇J(θ) = gradient of loss w.r.t. parameters θ",
                "description": "| Variant | Data per step | Pros | Cons |\n|---------|--------------|------|------|\n| Batch GD | All data | Stable convergence | Slow on large datasets |\n| SGD | 1 sample | Fast updates | Very noisy |\n| Mini-batch | 32–512 samples | Best of both | Needs tuning |\n\nAdaptive optimizers (Adam, RMSprop) automatically adjust α per parameter.",
                "example": "In linear regression, gradient descent iteratively adjusts weights: if predicted value is too high, reduce the coefficient proportionally to the prediction error.",
                "use_cases": ["Training neural networks", "Logistic regression optimization", "Any differentiable loss minimization", "Deep learning (Adam optimizer)"],
                "watch_out": "Learning rate α is critical. Too large → diverge (overshoot minimum). Too small → extremely slow convergence. Use learning rate schedulers in production.",
                "python_code": """\
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler

# --- Manual batch gradient descent for linear regression ---
rng = np.random.default_rng(42)
X = rng.uniform(0, 10, (200, 1))
y = 3 * X.flatten() + 7 + rng.normal(0, 1, 200)

X_b    = np.c_[np.ones(len(X)), X]   # add bias column
theta  = np.zeros(2)
alpha  = 0.01
losses = []

for epoch in range(200):
    preds = X_b @ theta
    error = preds - y
    grad  = (2 / len(y)) * X_b.T @ error
    theta -= alpha * grad
    losses.append(((error**2).mean()))

print(f"Learned: intercept={theta[0]:.3f}, slope={theta[1]:.3f}")
print(f"True:    intercept=7.000, slope=3.000")

fig, ax = plt.subplots(figsize=(7, 3))
ax.plot(losses, color="#3b82f6")
ax.set_xlabel("Epoch"); ax.set_ylabel("MSE Loss")
ax.set_title("Gradient Descent Convergence")
plt.tight_layout()
plt.savefig("gradient_descent.png", dpi=150)
plt.show()

# --- sklearn SGDRegressor ---
scaler = StandardScaler()
sgd = SGDRegressor(learning_rate="adaptive", eta0=0.01, max_iter=1_000, random_state=42)
sgd.fit(scaler.fit_transform(X), y)
print(f"SGD coef: {sgd.coef_[0]:.3f}  intercept: {sgd.intercept_[0]:.3f}")
"""
            },
            {
                "title": "30. Confusion Matrix & Classification Metrics",
                "definition": "A confusion matrix summarizes classifier performance by comparing actual vs. predicted labels across all classes.",
                "formula": "Accuracy  = (TP+TN) / (TP+TN+FP+FN)\nPrecision = TP / (TP+FP)\nRecall    = TP / (TP+FN)\nF1        = 2×(P×R) / (P+R)\nMCC       = (TP×TN−FP×FN) / √((TP+FP)(TP+FN)(TN+FP)(TN+FN))",
                "description": "|  | Predicted + | Predicted − |\n|--|--|--|\n| **Actual +** | TP ✅ | FN ❌ (missed) |\n| **Actual −** | FP ❌ (false alarm) | TN ✅ |\n\n- **Precision**: of all predicted positives, how many are correct?\n- **Recall**: of all actual positives, how many did we catch?\n- **F1**: harmonic mean, balances precision and recall\n- **AUC-ROC**: overall discriminative ability across all thresholds",
                "example": "Fraud detection: missing fraud (FN) is very costly → maximize Recall. Spam filter: false positives delete real emails → maximize Precision. When both matter → use F1.",
                "use_cases": ["Model evaluation", "Threshold selection", "Class imbalance analysis", "Reporting classifier performance"],
                "watch_out": "Accuracy is useless for imbalanced classes. A model predicting 'no fraud' always gets 99% accuracy on a 1% fraud dataset. Use F1, AUC-ROC, or MCC instead.",
                "python_code": """\
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (confusion_matrix, classification_report,
                              roc_auc_score, roc_curve,
                              matthews_corrcoef, f1_score)

X, y = make_classification(n_samples=2_000, weights=[0.9, 0.1],
                            random_state=42)   # imbalanced
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
y_prob = clf.predict_proba(X_test)[:, 1]

print(classification_report(y_test, y_pred))
print(f"AUC-ROC : {roc_auc_score(y_test, y_prob):.4f}")
print(f"MCC     : {matthews_corrcoef(y_test, y_pred):.4f}")

# --- Confusion matrix heatmap ---
cm = confusion_matrix(y_test, y_pred)
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=axes[0])
axes[0].set_title("Confusion Matrix")

fpr, tpr, _ = roc_curve(y_test, y_prob)
axes[1].plot(fpr, tpr, color="#3b82f6", linewidth=2)
axes[1].plot([0,1],[0,1], "k--")
axes[1].set_xlabel("FPR"); axes[1].set_ylabel("TPR")
axes[1].set_title(f"ROC Curve (AUC={roc_auc_score(y_test, y_prob):.3f})")
plt.tight_layout()
plt.savefig("confusion_roc.png", dpi=150)
plt.show()
"""
            },
            {
                "title": "31. Dimensionality Reduction (PCA, t-SNE, UMAP)",
                "definition": "Techniques to reduce the number of features while preserving important structure, relationships, or variance in the data.",
                "formula": "PCA steps:\n  1. Standardize data (mean=0, SD=1)\n  2. Compute covariance matrix\n  3. Eigendecomposition → principal components\n  4. Project onto top k eigenvectors\n\nExplained Variance Ratio = λ_k / Σλ",
                "description": "| Method | Type | Preserves | Speed | Use For |\n|--------|------|-----------|-------|---------|\n| PCA | Linear | Global variance | Fast | Preprocessing, noise reduction |\n| t-SNE | Non-linear | Local clusters | Slow | 2D/3D visualization |\n| UMAP | Non-linear | Local + global | Moderate | Visualization + downstream ML |",
                "example": "100-feature customer dataset → 10 PCA components explain 95% of variance → train on 10 components, reducing overfitting and training time significantly.",
                "use_cases": ["Visualization of high-dimensional data", "Noise reduction before modeling", "Feature extraction", "Genomics and NLP embeddings"],
                "watch_out": "t-SNE is for visualization only — its axes carry no meaning and inter-cluster distances are unreliable. Never use t-SNE output as ML input features.",
                "python_code": """\
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_digits

digits = load_digits()
X, y   = digits.data, digits.target   # 1797 samples, 64 features

scaler = StandardScaler()
X_s    = scaler.fit_transform(X)

# --- PCA: explained variance ---
pca = PCA().fit(X_s)
cumvar = np.cumsum(pca.explained_variance_ratio_)
n_95  = np.searchsorted(cumvar, 0.95) + 1
print(f"Components for 95% variance: {n_95}")

# Reduce to n_95 components
X_pca = PCA(n_components=n_95).fit_transform(X_s)
print(f"Reduced shape: {X_pca.shape}")

# --- t-SNE for visualization ---
X_2d = TSNE(n_components=2, random_state=42, perplexity=30).fit_transform(X_s)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].plot(cumvar[:30], marker="o", ms=4, color="#3b82f6")
axes[0].axhline(0.95, ls="--", color="red")
axes[0].set_xlabel("# Components"); axes[0].set_ylabel("Cumulative variance")
axes[0].set_title("PCA Explained Variance")

sc = axes[1].scatter(X_2d[:,0], X_2d[:,1], c=y, cmap="tab10", s=5, alpha=0.7)
plt.colorbar(sc, ax=axes[1])
axes[1].set_title("t-SNE of Digits Dataset")
plt.tight_layout()
plt.savefig("pca_tsne.png", dpi=150)
plt.show()
"""
            },
            {
                "title": "32. Loss Functions",
                "definition": "A loss function quantifies the gap between a model's predictions and actual values, serving as the objective to minimize during training.",
                "formula": "MSE      = (1/n) × Σ(yᵢ − ŷᵢ)²\nMAE      = (1/n) × Σ|yᵢ − ŷᵢ|\nLog Loss = −(1/n) × Σ[yᵢlog(ŷᵢ) + (1−yᵢ)log(1−ŷᵢ)]",
                "description": "| Loss | Task | Outlier Sensitive | |\n|------|------|-------------------|--|\n| MSE | Regression | Yes (squares errors) | Smooth gradient |\n| MAE | Regression | No | Non-differentiable at 0 |\n| Huber | Regression | No | Best of both |\n| Log Loss | Binary classification | — | Penalizes confident errors |\n| Cross-entropy | Multi-class | — | Standard in deep learning |",
                "example": "House prices with a $2M outlier: MSE penalizes it 4× more than MAE. Use Huber loss when outliers are expected but shouldn't dominate training.",
                "use_cases": ["Training all supervised ML models", "Custom objectives for business constraints", "Evaluating model performance", "Choosing model objectives"],
                "watch_out": "Log loss heavily penalizes confident wrong predictions (e.g., P=0.99 for the wrong class). If your model is miscalibrated, use Platt scaling or isotonic regression.",
                "python_code": """\
import numpy as np
from sklearn.metrics import (mean_squared_error, mean_absolute_error,
                              log_loss, mean_absolute_percentage_error)

rng = np.random.default_rng(42)
y_true = rng.normal(100, 20, 200)
y_pred = y_true + rng.normal(0, 10, 200)
y_pred_outlier = y_pred.copy()
y_pred_outlier[0] = 500   # introduce one big outlier

print("Without outlier:")
print(f"  MSE  : {mean_squared_error(y_true, y_pred):.2f}")
print(f"  RMSE : {mean_squared_error(y_true, y_pred, squared=False):.2f}")
print(f"  MAE  : {mean_absolute_error(y_true, y_pred):.2f}")
print(f"  MAPE : {mean_absolute_percentage_error(y_true, y_pred)*100:.2f}%")

print("\\nWith outlier (MSE inflates, MAE stays stable):")
print(f"  MSE  : {mean_squared_error(y_true, y_pred_outlier):.2f}")
print(f"  MAE  : {mean_absolute_error(y_true, y_pred_outlier):.2f}")

# --- Huber loss (manual) ---
def huber_loss(y, yhat, delta=10):
    err = y - yhat
    return np.where(np.abs(err) <= delta,
                    0.5 * err**2,
                    delta * (np.abs(err) - 0.5 * delta)).mean()

print(f"  Huber: {huber_loss(y_true, y_pred_outlier):.2f}")

# --- Log loss for classification ---
y_cls  = np.array([0, 0, 1, 1, 1])
y_prob = np.array([0.1, 0.2, 0.8, 0.9, 0.7])
print(f"\\nLog Loss: {log_loss(y_cls, y_prob):.4f}")
"""
            },
            {
                "title": "33. Feature Engineering & Encoding",
                "definition": "The process of transforming raw data into informative, model-ready features that improve predictive performance.",
                "formula": "Min-Max:      x' = (x − min) / (max − min)\nZ-score:      x' = (x − μ) / σ\nLog transform: x' = log(x + 1)",
                "description": "**Encoding categorical variables:**\n- **One-hot**: binary column per category (nominal, low cardinality)\n- **Label encoding**: integers 0,1,2 (ordinal only)\n- **Target encoding**: replace with mean target value (leakage risk)\n- **Frequency encoding**: replace with category count\n\n**Numerical transformations:**\n- Log transform: reduces right skew\n- Polynomial features: captures non-linear relationships\n- Binning: converts continuous to ordinal",
                "example": "City with 50 unique values → target encoding replaces each city with its historical conversion rate. Far fewer dimensions than one-hot, but must be computed inside CV folds.",
                "use_cases": ["All supervised ML pipelines", "Reducing cardinality in tree models", "Preparing features for neural networks", "NLP preprocessing"],
                "watch_out": "Target encoding leaks label information. Always compute it inside CV folds using only training data — never on the full dataset before splitting.",
                "python_code": """\
import numpy as np
import pandas as pd
from sklearn.preprocessing import (StandardScaler, MinMaxScaler,
                                    OneHotEncoder, LabelEncoder,
                                    PolynomialFeatures)
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

rng = np.random.default_rng(42)
df = pd.DataFrame({
    "revenue":  rng.exponential(1_000, 500),       # right-skewed
    "city":     rng.choice(["Manila","Davao","Cebu"], 500),  # nominal
    "plan":     rng.choice(["basic","pro","enterprise"], 500), # ordinal-ish
    "logins":   rng.integers(0, 100, 500),
    "converted": rng.binomial(1, 0.3, 500),
})

# --- Log transform skewed feature ---
df["log_revenue"] = np.log1p(df["revenue"])

# --- Frequency encoding ---
freq = df["city"].value_counts()
df["city_freq"] = df["city"].map(freq)

# --- One-hot encoding ---
ohe = OneHotEncoder(sparse_output=False, drop="first")
city_ohe = ohe.fit_transform(df[["city"]])
print("OHE columns:", ohe.get_feature_names_out())

# --- sklearn ColumnTransformer pipeline ---
num_features  = ["logins", "log_revenue"]
cat_features  = ["city", "plan"]
preprocessor  = ColumnTransformer([
    ("num", StandardScaler(), num_features),
    ("cat", OneHotEncoder(drop="first", sparse_output=False), cat_features),
])
X_transformed = preprocessor.fit_transform(df)
print(f"Transformed shape: {X_transformed.shape}")
"""
            },
            {
                "title": "34. Class Imbalance Techniques",
                "definition": "Methods to handle datasets where one class significantly outnumbers another, causing models to be biased toward predicting the majority class.",
                "formula": "SMOTE: interpolate between k-nearest minority neighbors\n\nClass weight:\n  w_minority = n_total / (2 × n_minority)\n  w_majority = n_total / (2 × n_majority)",
                "description": "| Approach | Method | When to Use |\n|----------|--------|-------------|\n| Data-level | SMOTE oversampling | Moderate imbalance |\n| Data-level | Random undersampling | Very large majority class |\n| Algorithm-level | Class weighting | Most sklearn classifiers support it |\n| Threshold-level | Adjust decision threshold | Tune precision/recall tradeoff |\n| Ensemble | BalancedBagging | Complex tasks |",
                "example": "Fraud: 99% non-fraud. Model predicts 'no fraud' always → 99% accuracy, 0% recall. Apply 1:99 class weights → recall improves dramatically.",
                "use_cases": ["Fraud detection", "Medical diagnosis", "Rare event prediction", "Anomaly detection"],
                "watch_out": "SMOTE creates synthetic points that may not reflect real data. Never oversample the test set — always oversample only inside training folds.",
                "python_code": """\
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import classification_report, f1_score
from sklearn.pipeline import Pipeline
# pip install imbalanced-learn
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

X, y = make_classification(n_samples=5_000, weights=[0.97, 0.03],
                            random_state=42)   # 97/3 imbalance
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.2, random_state=42)

print(f"Train minority count: {y_train.sum()} / {len(y_train)}")

# --- Baseline (no correction) ---
base = LogisticRegression(max_iter=1_000).fit(X_train, y_train)
print("\\nBaseline:")
print(classification_report(y_test, base.predict(X_test), digits=3))

# --- Class weights ---
wt = LogisticRegression(class_weight="balanced", max_iter=1_000).fit(X_train, y_train)
print("Class-weighted:")
print(classification_report(y_test, wt.predict(X_test), digits=3))

# --- SMOTE inside a pipeline ---
smote_pipe = ImbPipeline([
    ("smote", SMOTE(random_state=42)),
    ("clf",   LogisticRegression(max_iter=1_000)),
])
smote_pipe.fit(X_train, y_train)
print("SMOTE:")
print(classification_report(y_test, smote_pipe.predict(X_test), digits=3))
"""
            },
            {
                "title": "35. Bayesian vs Frequentist Statistics",
                "definition": "Two competing philosophical frameworks for statistical inference that differ in how they define probability and treat unknown parameters.",
                "formula": "Frequentist: P(data | hypothesis)  →  p-value\n\nBayesian:    P(hypothesis | data) ∝ P(data | hypothesis) × P(hypothesis)\n             posterior ∝ likelihood × prior",
                "description": "| Dimension | Frequentist | Bayesian |\n|-----------|-------------|----------|\n| Probability means | Long-run frequency | Degree of belief |\n| Parameters | Fixed, unknown | Random, have distributions |\n| Output | p-values, CIs | Posterior distributions |\n| Prior knowledge | Not incorporated | Explicitly used |\n| Sample size | Fixed upfront | Can update incrementally |",
                "example": "Bayesian A/B test output: 'P(B > A) = 94%' — directly interpretable for business decisions. No need to wait for fixed sample size; can stop when posterior is conclusive.",
                "use_cases": ["A/B testing with small samples", "Updating models incrementally", "Spam filtering (Naive Bayes)", "Medical decisions under uncertainty"],
                "watch_out": "Bayesian results depend on the prior. Uninformative priors reduce this but don't eliminate it. Document your prior assumptions explicitly and test sensitivity.",
                "python_code": """\
import numpy as np
from scipy import stats

rng = np.random.default_rng(42)

# ── Frequentist A/B test ──────────────────────────────────────────────────────
n_ctrl, n_var = 1_000, 1_000
conv_ctrl = rng.binomial(1, 0.05, n_ctrl)
conv_var  = rng.binomial(1, 0.07, n_var)

from statsmodels.stats.proportion import proportions_ztest
z, p = proportions_ztest([conv_var.sum(), conv_ctrl.sum()],
                          [n_var, n_ctrl])
print(f"Frequentist p-value: {p:.4f}")
print("Significant!" if p < 0.05 else "Not significant")

# ── Bayesian A/B test (Beta-Binomial conjugate) ───────────────────────────────
# Prior: Beta(1,1) = uniform (no prior knowledge)
alpha_prior, beta_prior = 1, 1

# Posteriors
a_ctrl = alpha_prior + conv_ctrl.sum()
b_ctrl = beta_prior  + (n_ctrl - conv_ctrl.sum())
a_var  = alpha_prior + conv_var.sum()
b_var  = beta_prior  + (n_var  - conv_var.sum())

# Monte Carlo estimate of P(variant > control)
samples_ctrl = stats.beta.rvs(a_ctrl, b_ctrl, size=100_000, random_state=42)
samples_var  = stats.beta.rvs(a_var,  b_var,  size=100_000, random_state=42)
prob_var_wins = (samples_var > samples_ctrl).mean()
print(f"\\nBayesian P(variant > control) = {prob_var_wins:.4f} ({prob_var_wins*100:.1f}%)")
print(f"Posterior mean ctrl: {a_ctrl/(a_ctrl+b_ctrl):.4f}")
print(f"Posterior mean var : {a_var/(a_var+b_var):.4f}")
"""
            },
            {
                "title": "36. Monte Carlo Simulation",
                "definition": "A computational technique using repeated random sampling to estimate the probability distribution of outcomes that depend on uncertain inputs.",
                "formula": "E[f(X)] ≈ (1/N) × Σ f(xᵢ)   where xᵢ ~ P(X)\n\nLaw of Large Numbers:\n  estimate → true value as N → ∞",
                "description": "**Steps:**\n1. Define probability distributions for each uncertain input\n2. Randomly sample from each distribution (N=10,000+ iterations)\n3. Compute output for each scenario\n4. Analyze resulting output distribution (mean, CI, P(loss))\n\n**Common input distributions:** Normal, Uniform, Triangular, Poisson",
                "example": "Project profit: revenue ~ N($500K, $50K), cost ~ N($400K, $40K). 100K simulations → P(profit > 0) = 89%, median profit = $95K, 5th percentile = −$20K.",
                "use_cases": ["Financial risk modeling (VaR)", "Supply chain scenario planning", "Option pricing", "Project timeline estimation", "Sensitivity analysis"],
                "watch_out": "Results are only as good as your input distributions — garbage in, garbage out. Always run sensitivity analysis to identify which inputs drive the most output variance.",
                "python_code": """\
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(42)
N = 100_000

# --- Project profit simulation ---
revenue = rng.normal(loc=500_000, scale=50_000, size=N)
cost    = rng.normal(loc=400_000, scale=40_000, size=N)
profit  = revenue - cost

p_positive = (profit > 0).mean()
ci_95      = np.percentile(profit, [2.5, 97.5])
print(f"P(profit > 0)    : {p_positive:.3f} ({p_positive*100:.1f}%)")
print(f"Median profit    : ${np.median(profit):,.0f}")
print(f"95% CI           : ${ci_95[0]:,.0f} – ${ci_95[1]:,.0f}")
print(f"5th percentile   : ${np.percentile(profit, 5):,.0f}  (worst-case)")
print(f"Value at Risk 5% : ${-np.percentile(profit, 5):,.0f}")

# --- Sensitivity: which input drives most variance? ---
corr_rev = np.corrcoef(revenue, profit)[0,1]
corr_cst = np.corrcoef(cost,    profit)[0,1]
print(f"\\nCorr(revenue, profit) : {corr_rev:.3f}")
print(f"Corr(cost,    profit) : {corr_cst:.3f}")

# --- Plot ---
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(profit / 1_000, bins=80, edgecolor="none", color="#3b82f6", alpha=0.8)
ax.axvline(0, color="red", linewidth=1.5, label="Break-even")
ax.axvline(np.percentile(profit, 5) / 1_000, color="#f97316",
           linestyle="--", label="5th pct")
ax.set_xlabel("Profit ($K)")
ax.set_ylabel("Frequency")
ax.set_title("Monte Carlo: Project Profit Distribution")
ax.legend()
plt.tight_layout()
plt.savefig("monte_carlo.png", dpi=150)
plt.show()
"""
            },
        ]
    }
}


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
st.sidebar.title("⚙️ Options")

level_filter = st.sidebar.multiselect(
    "Filter by level:",
    options=list(sections.keys()),
    default=list(sections.keys()),
)

st.sidebar.markdown("---")
search = st.sidebar.text_input(
    "🔍 Search", placeholder="e.g. entropy, p-value, SMOTE")

st.sidebar.markdown("---")
st.sidebar.markdown("**📚 Index**")
for level, content in sections.items():
    st.sidebar.markdown(f"{level}: **{len(content['topics'])} topics**")

st.sidebar.markdown("---")
st.sidebar.caption("36 topics · 4 levels · Python examples included")


# ─────────────────────────────────────────────
# RENDER
# ─────────────────────────────────────────────
def topic_matches(t, q):
    q = q.lower()
    return any(
        q in (t.get(k) or "").lower()
        for k in ["title", "definition", "description", "example",
                  "formula", "watch_out", "python_code"]
    ) or any(q in uc.lower() for uc in t.get("use_cases", []))


total_shown = 0

for level, content in sections.items():
    if level not in level_filter:
        continue

    topics = [t for t in content["topics"]
              if not search or topic_matches(t, search)]
    if not topics:
        continue

    total_shown += len(topics)
    st.markdown(
        f'<span class="badge {content["badge"]}">{level}</span>',
        unsafe_allow_html=True)

    cols = st.columns(2)
    for i, topic in enumerate(topics):
        with cols[i % 2]:
            with st.expander(f"**{topic['title']}**", expanded=True):
                render_topic(topic)

    st.markdown("---")

if search and total_shown == 0:
    st.info(f"No topics found for **'{search}'**. Try a different keyword.")

st.caption(
    f"📊 Data & Statistics Cheat Sheet · {total_shown} topics shown · 🐍 Python examples included")

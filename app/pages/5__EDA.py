import streamlit as st
import pandas as pd
from pathlib import Path
from utility.seo import inject_seo
from components import sidebar
from components.EDA import (
    domain_spotify,
    load_dataset,
    section_overview,
    section_descriptive,
    section_outliers,
    section_univariate,
    section_bivariate,
    section_target,
    section_correlation,
    section_insights,
    domain_airbnb,
    domain_co2,
    domain_education,
    domain_used_cars,
    domain_diamonds,
    domain_socioeconomic,
    domain_manufacturing,
    domain_insurance,
    domain_hr,
    domain_retail_shopping,
    domain_retail_superstore,
    domain_finance_loan,
    domain_finance_credit,
    domain_telecom,
    domain_healthcare_generic
)


APP_DIR = Path(__file__).resolve().parents[1]

st.set_page_config(
    page_title="EDA Guide",
    page_icon="📊",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; }
    .badge {
        display: inline-block;
        background: #e8f4fd;
        color: #1a6fa8;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
sidebar()

inject_seo('EDA')


st.title("📊 Exploratory Data Analysis (EDA)")
st.caption("A structured study guide to understanding your data before modeling.")


tab_doc, tab_ex = st.tabs(["📖 Documentation", "💡 Examples"])
DATASETS = {
    "Credit Risk": APP_DIR / "data" / 'EDA' / "credit_risk.csv",
    "Heart Disease": APP_DIR / "data" / 'EDA' / "heart_disease.csv",
    "Superstore": APP_DIR / "data" / 'EDA' / "superstore.csv",
    "Loan Prediction": APP_DIR / "data" / 'EDA' / "loan_prediction.csv",
    "Pima Indians Diabetes": APP_DIR / "data" / 'EDA' / "diabetes.csv",
    "Breast Cancer": APP_DIR / "data" / 'EDA' / "breast_cancer.csv",
    "Stroke Prediction": APP_DIR / "data" / 'EDA' / "stroke_prediction.csv",
    "Customer Shopping": APP_DIR / "data" / 'EDA' / "customer_shopping.csv",
    "HR Attrition": APP_DIR / "data" / 'EDA' / "hr_analytics.csv",
    "Employee (Human Resources)": APP_DIR / "data" / 'EDA' / "Employee.csv",
    "US Health Insurance": APP_DIR / "data" / 'EDA' / "health_insurance.csv",
    "Predictive Maintenance": APP_DIR / "data" / 'EDA' / "predictive_maintenance.csv",
    "Adult Census Income": APP_DIR / "data" / 'EDA' / "adult_census.csv",
    "Diamonds": APP_DIR / "data" / 'EDA' / "diamonds.csv",
    "Used Cars": APP_DIR / "data" / 'EDA' / "used_cars.csv",
    "Student Performance": APP_DIR / "data" / 'EDA' / "student_performance.csv",
    "Telco Customer Churn": APP_DIR / "data" / 'EDA' / "telco_customer_churn.csv",
    "Spotify Tracks": APP_DIR / "data" / 'EDA' / "spotify_tracks.csv",
    "Airbnb NYC": APP_DIR / "data" / 'EDA' / "airbnb_ny.csv",
    "CO2 Emissions": APP_DIR / "data" / 'EDA' / "co2_emissions.csv",
}

# ═════════════════════════════════════════════════════════════════════════════
# DOCUMENTATION TAB
# ═════════════════════════════════════════════════════════════════════════════
with tab_doc:

    # ── 1 · Data Overview ────────────────────────────────────────────────────
    with st.container(border=True):
        st.markdown('<span class="badge">Step 1</span>',
                    unsafe_allow_html=True)
        st.subheader("🗄️ Data Overview")
        st.write(
            "The first step in any EDA is understanding the **shape and structure** of "
            "your dataset — how many rows and columns it has, what the column names are, "
            "and what data types each column holds."
        )
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Key operations**")
            st.markdown(
                "- `df.shape` — rows × columns\n"
                "- `df.dtypes` — data type of each column\n"
                "- `df.head()` / `df.tail()` — preview first/last rows\n"
                "- `df.info()` — concise column summary\n"
                "- `df.columns.tolist()` — list all column names"
            )
        with col2:
            st.markdown("**Common data types**")
            st.markdown(
                "| Type | Example use case |\n|---|---|\n"
                "| `int64` | Age, Count |\n"
                "| `float64` | Price, Score |\n"
                "| `object` | Name, Category |\n"
                "| `bool` | Flag, Is_Active |\n"
                "| `datetime64` | Timestamp, Date |"
            )
        st.markdown("**Why it matters**")
        st.write(
            "Knowing your data types upfront prevents silent type errors during analysis. "
            "For example, a numeric column stored as `object` won't compute statistics "
            "correctly until it's cast to the right type."
        )

    st.write("")

    # ── 2 · Missing Values Analysis ──────────────────────────────────────────
    with st.container(border=True):
        st.markdown('<span class="badge">Step 2</span>',
                    unsafe_allow_html=True)
        st.subheader("❓ Missing Values Analysis")
        st.write(
            "Missing data can bias model results or cause outright errors during training. "
            "This step **quantifies null counts and their percentages** per column, "
            "helping you decide how to handle each gap."
        )
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Key operations**")
            st.markdown(
                "- `df.isnull().sum()` — null count per column\n"
                "- `df.isnull().mean() * 100` — % missing\n"
                "- `df.notnull().sum()` — available count\n"
                "- Visualise with a bar chart or heatmap"
            )
        with col2:
            st.markdown("**Handling strategies**")
            st.markdown(
                "| Strategy | When to use |\n|---|---|\n"
                "| Mean / Median fill | Numeric, low missingness |\n"
                "| Mode fill | Categorical columns |\n"
                "| Forward / back fill | Time-series data |\n"
                "| Add indicator column | When absence has signal |\n"
                "| Drop rows / cols | > 50 % missing |"
            )
        st.markdown("**Why it matters**")
        st.write(
            "Most ML algorithms cannot handle NaN values natively. "
            "Imputing carelessly (e.g., mean-filling a bimodal distribution) can "
            "introduce its own distortions — always understand the pattern of "
            "missingness (MCAR, MAR, or MNAR) before choosing a strategy."
        )

    st.write("")

    # ── 3 · Descriptive Statistics ───────────────────────────────────────────
    with st.container(border=True):
        st.markdown('<span class="badge">Step 3</span>',
                    unsafe_allow_html=True)
        st.subheader("🧮 Descriptive Statistics")
        st.write(
            "Summary statistics give a **numeric snapshot** of your data's central "
            "tendency and spread. They are the foundation for spotting anomalies and "
            "understanding distributions before any visualisation."
        )
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Central tendency**")
            st.markdown(
                "- **Mean (μ)** — arithmetic average; sensitive to outliers\n"
                "- **Median (M)** — middle value; robust to outliers\n"
                "- **Mode** — most frequent value; useful for categories"
            )
        with col2:
            st.markdown("**Spread & shape**")
            st.markdown(
                "- **Std Dev (σ)** — average distance from the mean\n"
                "- **Variance (σ²)** — squared std dev\n"
                "- **Range** — max − min\n"
                "- **IQR** — Q3 − Q1 (interquartile range)\n"
                "- **Skewness / Kurtosis** — shape of distribution"
            )
        st.markdown("**Key command**")
        st.code(
            "df.describe()  # count, mean, std, min, 25%, 50%, 75%, max", language="python")
        st.write(
            "For categorical columns use `df.describe(include='object')` to get "
            "count, unique values, top, and frequency."
        )

    st.write("")

    # ── 4 · Univariate Analysis ──────────────────────────────────────────────
    with st.container(border=True):
        st.markdown('<span class="badge">Step 4</span>',
                    unsafe_allow_html=True)
        st.subheader("📈 Univariate Analysis")
        st.write(
            "Univariate analysis examines **one variable at a time** to understand "
            "its individual distribution. Histograms reveal shape and modality; "
            "box plots expose spread, quartiles, and potential outliers."
        )
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Numeric features**")
            st.markdown(
                "- **Histogram** — frequency distribution across bins\n"
                "- **KDE plot** — smooth density estimate\n"
                "- **Box plot** — IQR, median, and whiskers\n"
                "- **Violin plot** — KDE + box combined"
            )
        with col2:
            st.markdown("**Categorical features**")
            st.markdown(
                "- **Count / bar plot** — frequency per category\n"
                "- **Pie chart** — proportions (use sparingly)\n"
                "- `value_counts()` — quick tabular frequency\n"
                "- `value_counts(normalize=True)` — relative frequency"
            )
        st.markdown("**What to look for**")
        st.markdown(
            "- **Unimodal vs multimodal** — single vs multiple peaks\n"
            "- **Skewness** — asymmetric distribution\n"
            "- **Heavy tails** — more extreme values than expected\n"
            "- **Unexpected spikes** — possible data-entry errors or clumping"
        )

    st.write("")

    # ── 5 · Bivariate Analysis ───────────────────────────────────────────────
    with st.container(border=True):
        st.markdown('<span class="badge">Step 5</span>',
                    unsafe_allow_html=True)
        st.subheader("🔀 Bivariate Analysis")
        st.write(
            "Bivariate analysis examines the **relationship between two variables** "
            "to uncover associations, trends, or class separability. It is the bridge "
            "between raw distributions and feature selection."
        )
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Numeric vs Numeric**")
            st.markdown(
                "- **Scatter plot** — direction, strength, and outliers\n"
                "- **Line plot** — trends over a continuous axis\n"
                "- **Regression line** — visualise linear fit\n"
                "- `df.corr()` — numeric correlation matrix"
            )
        with col2:
            st.markdown("**Numeric vs Categorical**")
            st.markdown(
                "- **Grouped box / violin plots** — spread per group\n"
                "- **Bar chart of means** — average per category\n"
                "- **Strip / swarm plot** — individual points per group\n"
                "- **Pair plot** — all numeric pairs (`sns.pairplot`)"
            )
        st.markdown("**Categorical vs Categorical**")
        st.markdown(
            "- **Crosstab / heatmap** — frequency of co-occurrence\n"
            "- **Grouped bar chart** — count per combination\n"
            "- `pd.crosstab(df.A, df.B)` — quick frequency table"
        )

    st.write("")

    # ── 6 · Correlation Analysis ─────────────────────────────────────────────
    with st.container(border=True):
        st.markdown('<span class="badge">Step 6</span>',
                    unsafe_allow_html=True)
        st.subheader("🌡️ Correlation Analysis")
        st.write(
            "Correlation analysis measures the **strength and direction of linear "
            "relationships** between all numeric feature pairs simultaneously. "
            "A heatmap makes it easy to spot multicollinearity and feature redundancy."
        )
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**How to read the heatmap**")
            st.markdown(
                "- **+1** — perfect positive correlation\n"
                "- **0** — no linear relationship\n"
                "- **−1** — perfect negative correlation\n"
                "- |r| > 0.8 often signals multicollinearity\n"
                "- Diagonal is always 1 (self-correlation)"
            )
        with col2:
            st.markdown("**Correlation methods**")
            st.markdown(
                "| Method | Best for |\n|---|---|\n"
                "| **Pearson** | Continuous, linear relationship |\n"
                "| **Spearman** | Ordinal or monotonic relationship |\n"
                "| **Kendall** | Small samples or many tied ranks |\n"
                "| **Point-biserial** | Binary vs continuous |"
            )
        st.markdown("**Why it matters**")
        st.write(
            "Highly correlated features carry redundant information. For linear models "
            "(Linear / Logistic Regression), multicollinearity inflates coefficient "
            "variance and makes interpretation unreliable. Use correlation analysis to "
            "decide which features to keep, drop, or combine."
        )

    st.write("")

    # ── 7 · Outlier Detection ────────────────────────────────────────────────
    with st.container(border=True):
        st.markdown('<span class="badge">Step 7</span>',
                    unsafe_allow_html=True)
        st.subheader("🎯 Outlier Detection")
        st.write(
            "Outliers are data points that deviate significantly from the bulk of the "
            "distribution. They may reflect genuine rare events, measurement errors, "
            "or data-entry mistakes — understanding the cause determines the treatment."
        )
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Detection methods**")
            st.markdown(
                "- **IQR rule** — flag points outside Q1 − 1.5×IQR or Q3 + 1.5×IQR\n"
                "- **Z-score** — flag observations where |z| > 3\n"
                "- **Box plot** — visual whisker inspection\n"
                "- **Scatter plot** — visual for bivariate outliers\n"
                "- **Isolation Forest** — ML-based, works in high dimensions"
            )
        with col2:
            st.markdown("**Handling strategies**")
            st.markdown(
                "| Strategy | When to use |\n|---|---|\n"
                "| Remove | Confirmed data / entry error |\n"
                "| Cap / floor (Winsorize) | Keep but limit extreme values |\n"
                "| Log / sqrt transform | Compress the range |\n"
                "| Separate model | Outliers are the target class |\n"
                "| Keep | Genuine rare events of interest |"
            )
        st.markdown("**IQR formula reference**")
        st.code(
            "Q1 = df['col'].quantile(0.25)\n"
            "Q3 = df['col'].quantile(0.75)\n"
            "IQR = Q3 - Q1\n"
            "lower = Q1 - 1.5 * IQR\n"
            "upper = Q3 + 1.5 * IQR\n"
            "outliers = df[(df['col'] < lower) | (df['col'] > upper)]",
            language="python",
        )

    st.write("")

    # ── 8 · Feature Distribution ─────────────────────────────────────────────
    with st.container(border=True):
        st.markdown('<span class="badge">Step 8</span>',
                    unsafe_allow_html=True)
        st.subheader("📉 Feature Distribution")
        st.write(
            "Understanding the **shape and spread** of each feature — especially skewness "
            "— is critical because many ML algorithms assume roughly normal inputs. "
            "Knowing the distribution guides appropriate transformations."
        )
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Skewness types**")
            st.markdown(
                "- **Symmetric** — mean ≈ median (ideal for most models)\n"
                "- **Positive (right) skew** — long right tail; mean > median\n"
                "- **Negative (left) skew** — long left tail; mean < median\n"
                "- `df.skew()` — skewness coefficient per column\n"
                "- |skew| > 1 is generally considered highly skewed"
            )
        with col2:
            st.markdown("**Transformations**")
            st.markdown(
                "| Skew type | Recommended transform |\n|---|---|\n"
                "| Positive | Log (`np.log1p`) |\n"
                "| Positive (moderate) | Square root |\n"
                "| Negative | Reflect then log |\n"
                "| Wide spread | Standardise (z-score) |\n"
                "| Any | Box-Cox or Yeo-Johnson |"
            )
        st.markdown("**Kurtosis**")
        st.write(
            "Kurtosis measures the heaviness of the tails. "
            "A normal distribution has kurtosis ≈ 3 (excess kurtosis = 0). "
            "High kurtosis (leptokurtic) means more extreme outlier risk; "
            "low kurtosis (platykurtic) means lighter tails than normal."
        )

    st.write("")

    # ── 9 · Insights & Observations ──────────────────────────────────────────
    with st.container(border=True):
        st.markdown('<span class="badge">Step 9</span>',
                    unsafe_allow_html=True)
        st.subheader("💡 Insights & Observations")
        st.write(
            "The final step synthesises everything discovered above into **actionable "
            "findings**. Document the patterns, trends, and assumptions that will "
            "drive your feature engineering and model selection decisions."
        )
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**🔍 Patterns Identified**")
            st.write(
                "Recurring structures or groupings in the data — e.g., customer "
                "segments, seasonal cycles, or feature clusters."
            )
        with col2:
            st.markdown("**📈 Trends Revealed**")
            st.write(
                "Directional changes over time or across groups — e.g., sales "
                "growth, demographic shifts, or feature drift."
            )
        with col3:
            st.markdown("**✅ Assumptions Validated**")
            st.write(
                "Confirm or challenge modelling prerequisites — e.g., linearity, "
                "independence, normality, or class balance."
            )
        st.divider()
        st.markdown("**Pre-modelling checklist**")
        st.markdown(
            "- [ ] Dataset shape, columns, and data types confirmed\n"
            "- [ ] Missing values quantified and handled\n"
            "- [ ] Descriptive statistics reviewed\n"
            "- [ ] Distributions understood; skewed features transformed if needed\n"
            "- [ ] Outliers identified and a treatment decision made\n"
            "- [ ] Correlations checked; multicollinear features flagged\n"
            "- [ ] Key patterns, anomalies, and assumptions documented"
        )


# ═════════════════════════════════════════════════════════════════════════════
# EXAMPLES TAB
# ═════════════════════════════════════════════════════════════════════════════

DATASET_CONFIG = {
    "Credit Risk": {
        "domain": "finance",
        "target": "loan_status",
        "target_type": "binary",
        "target_positive_label": 1,
        "key_num": ["person_age", "person_income", "loan_amnt", "loan_int_rate"],
        "group_cols": ["loan_grade", "loan_intent"],
        "derived": [("loan_to_income", lambda df: df["loan_amnt"] / df["person_income"])],
        "color_pair": ["#378ADD", "#E24B4A"],
        "thresholds": {},
    },
    "Heart Disease": {
        "domain": "healthcare",
        "target": "target",
        "target_type": "binary",
        "target_positive_label": 1,
        "key_num": ["age", "trestbps", "chol", "thalach", "oldpeak"],
        "group_cols": ["cp"],
        "derived": [],
        "color_pair": ["#1D9E75", "#E24B4A"],
        "thresholds": {"trestbps": (130, "Hypertension threshold (130)"),
                       "thalach": (100, "Bradycardia threshold (100)")},
    },
    "Superstore": {
        "domain": "retail",
        "target": None,
        "key_num": ["Sales", "Profit", "Discount", "Quantity"],
        "group_cols": ["Category", "Region", "Sub-Category", "Ship Mode"],
        "derived": [("profit_margin", lambda df: df["Profit"] / df["Sales"] * 100)],
        "date_col": "Order Date",
        "value_col": "Sales",
        "color_pair": ["#BA7517", "#1D9E75"],
        "thresholds": {},
    },
    "Loan Prediction": {
        "domain": "finance",
        "target": "Loan_Status",
        "target_type": "binary_str",
        "target_positive_label": "Y",
        "key_num": ["ApplicantIncome", "CoapplicantIncome", "LoanAmount", "Loan_Amount_Term"],
        "group_cols": ["Education", "Self_Employed", "Credit_History"],
        "derived": [("loan_to_income", lambda df: df["LoanAmount"] / (df["ApplicantIncome"] / 1000))],
        "color_pair": ["#378ADD", "#E24B4A"],
        "thresholds": {},
    },
    "Pima Indians Diabetes": {
        "domain": "healthcare",
        "target": "Outcome",
        "target_type": "binary",
        "target_positive_label": 1,
        "key_num": ["Glucose", "BloodPressure", "BMI", "Age", "Insulin", "SkinThickness"],
        "group_cols": [],
        "derived": [],
        "color_pair": ["#1D9E75", "#E24B4A"],
        "thresholds": {"Glucose": (126, "Diabetic threshold (126 mg/dL)"),
                       "BloodPressure": (90, "Hypertension (90 mmHg)"),
                       "BMI": (30, "Obesity threshold (BMI 30)")},
    },
    "Breast Cancer": {
        "domain": "healthcare",
        "target": "diagnosis",
        "target_type": "binary_str",
        "target_positive_label": "M",
        "key_num": ["radius_mean", "texture_mean", "perimeter_mean", "area_mean", "smoothness_mean"],
        "group_cols": [],
        "derived": [],
        "color_pair": ["#1D9E75", "#E24B4A"],
        "thresholds": {},
        "mean_feature_suffix": "_mean",
    },
    "Stroke Prediction": {
        "domain": "healthcare",
        "target": "stroke",
        "target_type": "binary",
        "target_positive_label": 1,
        "key_num": ["age", "avg_glucose_level", "bmi"],
        "group_cols": ["gender", "smoking_status", "work_type", "ever_married"],
        "derived": [],
        "color_pair": ["#534AB7", "#E24B4A"],
        "thresholds": {"avg_glucose_level": (126, "Diabetic threshold (126)"),
                       "bmi": (30, "Obesity threshold (BMI 30)")},
    },
    "Customer Shopping": {
        "domain": "retail",
        "target": None,
        "key_num": ["quantity", "price", "total_spend", "age"],
        "group_cols": ["category", "gender", "payment_method", "shopping_mall"],
        "derived": [("total_spend", lambda df: df["quantity"] * df["price"])],
        "date_col": "invoice_date",
        "value_col": "total_spend",
        "color_pair": ["#BA7517", "#378ADD"],
        "thresholds": {},
        "rfm": True,
    },
    "HR Attrition": {
        "domain": "hr",
        "target": "Attrition",
        "target_type": "binary_str",
        "target_positive_label": "Yes",
        "key_num": ["Age", "MonthlyIncome", "YearsAtCompany", "JobSatisfaction", "WorkLifeBalance"],
        "group_cols": ["Department", "JobRole", "OverTime", "Gender"],
        "derived": [],
        "color_pair": ["#534AB7", "#E24B4A"],
        "thresholds": {},
    },
    "Employee (Human Resources)": {
        "domain": "hr",
        "target": None,
        "key_num": [],
        "group_cols": [],
        "derived": [],
        "color_pair": ["#534AB7", "#E24B4A"],
        "thresholds": {},
    },
    "US Health Insurance": {
        "domain": "insurance",
        "target": None,
        "key_num": ["age", "bmi", "children", "charges"],
        "group_cols": ["smoker", "region", "sex"],
        "derived": [],
        "color_pair": ["#993C1D", "#1D9E75"],
        "thresholds": {"bmi": (30, "Obesity threshold (BMI 30)")},
        "primary_metric": "charges",
    },
    "Predictive Maintenance": {
        "domain": "manufacturing",
        "target": "Target",
        "target_type": "binary",
        "target_positive_label": 1,
        "key_num": [],
        "group_cols": [],
        "derived": [],
        "color_pair": ["#3B6D11", "#E24B4A"],
        "thresholds": {},
    },
    "Adult Census Income": {
        "domain": "socioeconomic",
        "target": "income",
        "target_type": "binary_str",
        "target_positive_label": ">50K",
        "key_num": ["age", "hours.per.week", "capital.gain", "capital.loss", "education.num"],
        "group_cols": ["education", "occupation", "sex", "race"],
        "derived": [],
        "color_pair": ["#73726c", "#3266ad"],
        "thresholds": {"hours.per.week": (40, "Standard 40 hrs/week")},
    },
    "Diamonds": {
        "domain": "pricing",
        "target": None,
        "key_num": ["carat", "depth", "table", "price", "x", "y", "z"],
        "group_cols": ["cut", "color", "clarity"],
        "derived": [],
        "color_pair": ["#BA7517", "#378ADD"],
        "thresholds": {},
        "primary_metric": "price",
        "ordinal": {
            "cut": ["Fair", "Good", "Very Good", "Premium", "Ideal"],
            "color": ["J", "I", "H", "G", "F", "E", "D"],
            "clarity": ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"],
        },
    },
    "Used Cars": {
        "domain": "automotive",
        "target": None,
        "key_num": [],
        "group_cols": [],
        "derived": [],
        "color_pair": ["#BA7517", "#378ADD"],
        "thresholds": {},
    },
    "Student Performance": {
        "domain": "education",
        "target": None,
        "key_num": [],
        "group_cols": ["gender"],
        "derived": [],
        "color_pair": ["#7F77DD", "#D85A30"],
        "thresholds": {},
        "score_suffix": "score",
    },
    "Telco Customer Churn": {
        "domain": "telecom",
        "target": "Churn",
        "target_type": "binary_str",
        "target_positive_label": "Yes",
        "key_num": ["tenure", "MonthlyCharges", "TotalCharges"],
        "group_cols": ["Contract", "InternetService", "PaymentMethod"],
        "derived": [],
        "color_pair": ["#185FA5", "#E24B4A"],
        "thresholds": {},
    },
    "Spotify Tracks": {
        "domain": "entertainment",
        "target": None,
        "key_num": ["popularity", "danceability", "energy", "loudness", "speechiness",
                    "acousticness", "instrumentalness", "liveness", "valence", "tempo"],
        "group_cols": [],
        "derived": [("duration_min", lambda df: df["duration_ms"] / 60000
                     if "duration_ms" in df.columns else None)],
        "color_pair": ["#1DB954", "#E24B4A"],
        "thresholds": {},
    },
    "Airbnb NYC": {
        "domain": "real_estate",
        "target": None,
        "key_num": ["price", "minimum_nights", "number_of_reviews", "availability_365"],
        "group_cols": ["neighbourhood_group", "room_type"],
        "derived": [],
        "color_pair": ["#FF5A5F", "#378ADD"],
        "thresholds": {},
        "primary_metric": "price",
        "geo": True,
    },
    "CO2 Emissions": {
        "domain": "environment",
        "target": None,
        "key_num": [],
        "group_cols": [],
        "derived": [],
        "color_pair": ["#2D6A4F", "#E24B4A"],
        "thresholds": {},
        "time_series": True,
    },
}
with tab_ex:
    st.subheader("Exploratory Data Analysis")

    col_select, col_info = st.columns([3, 2])
    with col_select:
        dataset_name = st.selectbox(
            "Select a dataset:", list(DATASETS.keys()), key="example_dataset"
        )
    with col_info:
        cfg = DATASET_CONFIG.get(dataset_name, {})
        domain = cfg.get("domain", "general")
        st.caption(f"Domain: **{domain.replace('_', ' ').title()}**")
        if cfg.get("target"):
            st.caption(f"Target column: `{cfg['target']}`")

    # Load data
    with st.spinner("Loading dataset..."):
        data = load_dataset(DATASETS[dataset_name])

    if data is None or data.empty:
        st.error("Could not load dataset. Check the file path.")

    if dataset_name == "Telco Customer Churn" and "TotalCharges" in data.columns:
        data = data.copy()
        data["TotalCharges"] = pd.to_numeric(
            data["TotalCharges"], errors="coerce")
    if dataset_name == "Adult Census Income":
        data = data.copy()
        data = data.apply(lambda col: col.str.strip()
                          if col.dtype == "object" else col)
        data.replace("?", pd.NA, inplace=True)
    if dataset_name == "Breast Cancer" and "Unnamed: 32" in data.columns:
        data = data.drop(columns=["Unnamed: 32"])

    # Raw data preview
    with st.expander("Preview raw data"):
        st.dataframe(data.head(100), width='stretch')

    tab_overview, tab_desc, tab_outliers, tab_uni, tab_bi, tab_target, tab_domain, tab_corr, tab_insights = st.tabs([
        "📋 Overview",
        "📊 Descriptive",
        "🎯 Outliers",
        "📈 Univariate",
        "🔀 Bivariate",
        "🏷️ Target",
        "🔬 Domain",
        "🌡️ Correlation",
        "💡 Insights",
    ])

    with tab_overview:
        section_overview(data, cfg)

    with tab_desc:
        section_descriptive(data, cfg)

    with tab_outliers:
        section_outliers(data, cfg)

    with tab_uni:
        section_univariate(data, cfg)

    with tab_target:
        section_target(data, cfg)

    with tab_bi:
        section_bivariate(data, cfg)

    with tab_corr:
        section_correlation(data, cfg)

    with tab_domain:
        st.markdown(f"#### Domain-Specific Analysis — {dataset_name}")
        domain = cfg.get("domain", "general")

        if dataset_name == "Credit Risk":
            domain_finance_credit(data, cfg)
        elif dataset_name == "Loan Prediction":
            domain_finance_loan(data, cfg)
        elif dataset_name == "Superstore":
            domain_retail_superstore(data, cfg)
        elif dataset_name == "Customer Shopping":
            domain_retail_shopping(data, cfg)
        elif dataset_name in ("HR Attrition", "Employee (Human Resources)"):
            domain_hr(data, cfg, dataset_name)
        elif dataset_name == "US Health Insurance":
            domain_insurance(data, cfg)
        elif dataset_name == "Predictive Maintenance":
            domain_manufacturing(data, cfg)
        elif dataset_name == "Adult Census Income":
            domain_socioeconomic(data, cfg)
        elif dataset_name == "Diamonds":
            domain_diamonds(data, cfg)
        elif dataset_name == "Used Cars":
            domain_used_cars(data, cfg)
        elif dataset_name == "Student Performance":
            domain_education(data, cfg)
        elif dataset_name == "Telco Customer Churn":
            domain_telecom(data, cfg)
        elif dataset_name == "Spotify Tracks":
            domain_spotify(data, cfg)
        elif dataset_name == "Airbnb NYC":
            domain_airbnb(data, cfg)
        elif dataset_name == "CO2 Emissions":
            domain_co2(data, cfg)
        elif domain == "healthcare":
            domain_healthcare_generic(data, cfg)
        else:
            st.info("General domain — see Overview, Univariate, and Bivariate tabs.")

    with tab_insights:
        st.markdown("#### Key Insights")
        section_insights(data, cfg, dataset_name)

    # ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "Exploratory Data Analysis (EDA) is the critical first step in any data science project. ")

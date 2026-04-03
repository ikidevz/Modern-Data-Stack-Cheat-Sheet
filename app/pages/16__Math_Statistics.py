import streamlit as st

st.set_page_config(
    page_title="Data & Statistics Cheat Sheet",
    page_icon="📊",
    layout="wide",
)

st.markdown("""
<style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 980px; }
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
        color: #9ca3af;
        margin-top: 0.75rem;
        margin-bottom: 0.2rem;
    }
    .def-box {
        background: #f0f7ff;
        border-left: 3px solid #3b82f6;
        padding: 8px 12px;
        border-radius: 0 4px 4px 0;
        font-size: 0.87rem;
    }
    .formula-box {
        background: #1a1a2e;
        color: #a9d0f5;
        padding: 10px 14px;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
        font-size: 0.83rem;
        white-space: pre-wrap;
    }
    .example-box {
        background: #f0fdf4;
        border-left: 3px solid #22c55e;
        padding: 8px 12px;
        border-radius: 0 4px 4px 0;
        font-size: 0.86rem;
    }
    .warn-box {
        background: #fff7ed;
        border-left: 3px solid #f97316;
        padding: 8px 12px;
        border-radius: 0 4px 4px 0;
        font-size: 0.86rem;
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
                "watch_out": "Always confirm what the denominator is. '50% increase' means nothing without knowing the base."
            },
            {
                "title": "2. Rates of Change",
                "definition": "The percentage increase or decrease between two values over time.",
                "formula": "Rate of Change = ((New − Old) / Old) × 100",
                "description": "Rates of change let you express growth or decline in a normalized, comparable way — regardless of the original scale of the numbers.",
                "example": "Revenue: $80K → $100K → (100K−80K)/80K × 100 = <strong>+25%</strong><br>Signups: 1,000 → 850 → (850−1000)/1000 × 100 = <strong>−15%</strong>",
                "use_cases": ["Monthly/quarterly KPI reporting", "User growth tracking", "Revenue trend analysis", "Price change comparisons"],
                "watch_out": "A large % change on a tiny base is misleading. 100% growth from 2 to 4 users ≠ 100% growth from 10,000 to 20,000."
            },
            {
                "title": "3. Year-over-Year (YoY) Comparisons",
                "definition": "Comparing a metric for the same time period across consecutive years to measure true growth while eliminating seasonal noise.",
                "formula": "YoY Growth = ((This Year − Last Year) / Last Year) × 100",
                "description": "Seasonal businesses have naturally high and low periods. Comparing December to November looks like a drop even in a great year. YoY fixes this by comparing equivalent periods.",
                "example": "Dec 2023 revenue = $120K, Dec 2024 = $150K → YoY = <strong>+25%</strong>. Always compare Dec vs Dec, not Dec vs Nov.",
                "use_cases": ["Retail and e-commerce performance", "Subscription revenue tracking", "Seasonal demand analysis", "Executive dashboards"],
                "watch_out": "One-off events (pandemic years, product launches) distort YoY. Always annotate anomalies on your charts."
            },
            {
                "title": "4. Mean, Median, Mode",
                "definition": "Three measures of central tendency describing where the 'center' of a dataset lies.",
                "formula": "Mean   = Σx / n\nMedian = middle value when sorted\nMode   = most frequently occurring value",
                "description": "| Measure | Best For | Weakness |\n|---------|----------|----------|\n| Mean | Symmetric distributions | Pulled by outliers |\n| Median | Skewed data, income, prices | Ignores extremes |\n| Mode | Categorical data | May not be unique |",
                "example": "Salaries: [30K, 35K, 40K, 42K, 500K]<br>Mean = 129.4K (misleading), Median = 40K (representative)",
                "use_cases": ["Summarizing user ages, incomes, scores", "Comparing product ratings", "Reporting central performance metrics"],
                "watch_out": "Never report just the mean for skewed data. Always check if outliers are pulling it away from reality."
            },
            {
                "title": "5. Range, Variance & Std. Deviation",
                "definition": "Measures of spread that describe how dispersed or consistent the values in a dataset are.",
                "formula": "Range    = Max − Min\nVariance = Σ(x − μ)² / n\nStd Dev  = √Variance",
                "description": "Spread tells you how reliable your average is. A mean of 50 with SD=2 means values cluster tightly. The same mean with SD=30 means values scatter wildly.",
                "example": "Scores [48,49,50,51,52] → SD ≈ 1.4 (consistent)<br>Scores [10,30,50,70,90] → SD ≈ 28.3 (spread out)",
                "use_cases": ["Quality control (manufacturing)", "Risk assessment in finance", "Model performance evaluation", "A/B test variance analysis"],
                "watch_out": "Variance is in squared units — harder to interpret directly. Always prefer std. deviation when communicating to stakeholders."
            },
            {
                "title": "6. Basic Probability",
                "definition": "The likelihood of a specific event occurring, expressed as a number between 0 (impossible) and 1 (certain).",
                "formula": "P(event)  = Favorable outcomes / Total outcomes\nP(not A)  = 1 − P(A)\nP(A or B) = P(A) + P(B) − P(A and B)",
                "description": "Probability is the foundation of all predictive modeling and decision-making under uncertainty. Every classifier, risk model, and simulation relies on it.",
                "example": "20 out of 100 users churned → P(churn) = 0.2 → P(no churn) = 1 − 0.2 = <strong>0.8</strong>",
                "use_cases": ["Churn prediction models", "Lead scoring", "Fraud detection thresholds", "Insurance risk models"],
                "watch_out": "Don't confuse probability with frequency. P=0.2 means a 20% chance — not that exactly 1 in 5 events will always occur."
            },
            {
                "title": "7. Frequency Distributions & Histograms",
                "definition": "A frequency distribution shows how many times each value (or range) appears in a dataset. A histogram is its visual form.",
                "formula": "Relative Frequency = Count in bin / Total count",
                "description": "Histograms reveal the shape of your data. This shape matters because many statistical methods assume normality.\n\n- **Normal**: symmetric bell\n- **Right-skewed**: long right tail (e.g., income)\n- **Left-skewed**: long left tail (e.g., age at retirement)\n- **Bimodal**: two peaks → two subpopulations",
                "example": "Plotting user session lengths: most users cluster at 2–5 min, but power users go 60+ min → right-skewed distribution.",
                "use_cases": ["Exploratory data analysis (EDA)", "Detecting outliers and anomalies", "Choosing the right statistical test", "Feature distribution checks before modeling"],
                "watch_out": "Bin size matters! Too few bins hides structure; too many creates noise. Try multiple bin widths before deciding."
            },
            {
                "title": "8. Data Types",
                "definition": "A classification for the kind of values a variable holds, which determines valid statistical operations and appropriate chart types.",
                "formula": "N/A — this is a conceptual framework",
                "description": "| Type | Subtype | Examples | Valid Operations |\n|------|---------|----------|------------------|\n| Categorical | Nominal | Country, color, plan | Count, mode |\n| Categorical | Ordinal | Rating (low/mid/high) | Count, rank |\n| Numerical | Discrete | # orders, clicks | All arithmetic |\n| Numerical | Continuous | Revenue, time | All arithmetic + calculus |",
                "example": "Customer plan (Free/Pro/Enterprise) = nominal. Satisfaction score (1–5) = ordinal. Monthly revenue ($) = continuous.",
                "use_cases": ["Choosing the right chart type", "Selecting appropriate statistical tests", "Encoding variables for ML models"],
                "watch_out": "Numeric-looking codes (zip codes, user IDs) are actually categorical. Averaging zip codes produces meaningless results."
            },
            {
                "title": "9. Pareto Analysis (80/20 Rule)",
                "definition": "The observation that roughly 80% of effects come from 20% of causes, used to prioritize high-impact actions.",
                "formula": "Cumulative % = Σ(sorted values) / Total × 100\nIdentify the 20% where cumulative crosses ~80%",
                "description": "Originally observed in wealth distribution, the Pareto principle appears across business: customers, bugs, revenue drivers, and more. Sort, cumulate, and find the cutoff.",
                "example": "20% of your customers generate 80% of revenue. Identify those customers, analyze their traits, and prioritize retention efforts on them.",
                "use_cases": ["Customer value segmentation", "Bug prioritization in engineering", "Support ticket root cause analysis", "Supply chain optimization"],
                "watch_out": "The 80/20 split is a heuristic — in some contexts it's 90/10 or 70/30. It's a principle for prioritization, not a universal law."
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
                "watch_out": "Z-scores assume normality. On heavily skewed data, use the modified Z-score (based on median and MAD) instead."
            },
            {
                "title": "11. Correlation (Pearson & Spearman)",
                "definition": "A measure of the strength and direction of the relationship between two variables, ranging from −1 to +1.",
                "formula": "Pearson r  = Σ((x−x̄)(y−ȳ)) / (n·σx·σy)\nSpearman ρ = 1 − (6·Σd²) / (n·(n²−1))\n\n|r| < 0.3  → weak\n|r| 0.3–0.7 → moderate\n|r| > 0.7  → strong",
                "description": "| Method | Measures | When to Use |\n|--------|----------|-------------|\n| Pearson | Linear relationship | Continuous, normally distributed data |\n| Spearman | Monotonic relationship | Ordinal or ranked data |",
                "example": "Ad spend vs revenue: r = 0.85 → strong positive correlation. As ad spend increases, revenue tends to increase.",
                "use_cases": ["Feature selection for ML models", "Identifying business drivers", "Multicollinearity checks in regression"],
                "watch_out": "<strong>Correlation ≠ causation.</strong> Ice cream sales and drowning rates are correlated (both driven by summer). Always seek a causal mechanism."
            },
            {
                "title": "12. Hypothesis Testing & P-Values",
                "definition": "A formal framework for determining whether an observed effect is statistically significant or likely due to random chance.",
                "formula": "H₀: no effect (null hypothesis)\nH₁: effect exists (alternative hypothesis)\n\np-value = P(seeing this result | H₀ is true)\np < 0.05  → reject H₀  (statistically significant)\np ≥ 0.05  → fail to reject H₀",
                "description": "Common tests:\n- **t-test**: compare means of two groups\n- **Chi-square**: compare categorical distributions\n- **ANOVA**: compare means across 3+ groups\n\nThe p-value answers: 'If nothing changed, how likely is this result by chance?'",
                "example": "Variant B: 4.5% conversion vs control: 4.0%. p = 0.03 → significant at α=0.05 → safe to ship.",
                "use_cases": ["A/B test analysis", "Product experiment evaluation", "Clinical trial analysis", "Quality control testing"],
                "watch_out": "p < 0.05 ≠ 'large effect' or 'practically important.' A tiny difference can be significant with a huge sample. Always report effect size alongside the p-value."
            },
            {
                "title": "13. Confidence Intervals",
                "definition": "A range of values that, with a specified level of confidence (typically 95%), contains the true population parameter.",
                "formula": "CI = x̄ ± (z* × SE)\nSE  = σ / √n\n\nz* for 95% CI = 1.96\nz* for 99% CI = 2.576",
                "description": "A 95% CI means: if you repeated this experiment 100 times, ~95 of those intervals would contain the true value. It is NOT a 95% probability that this specific interval contains the true value.",
                "example": "Conversion rate: 4.2%, n=2,000 → 95% CI = [3.8%, 4.6%]. We're 95% confident the true rate is within this range.",
                "use_cases": ["Reporting survey results", "A/B test decision-making", "Presenting model accuracy ranges", "Communicating uncertainty to stakeholders"],
                "watch_out": "Wider CI = less precision, not a flaw. Chasing narrow CIs by ignoring uncertainty misleads decision-makers."
            },
            {
                "title": "14. Sampling & Sampling Bias",
                "definition": "Sampling selects a subset of a population for analysis. Sampling bias occurs when the sample systematically differs from the population it represents.",
                "formula": "Margin of Error = z* × √(p(1−p)/n)\nRequired n ≈ (z*/ME)² × p(1−p)",
                "description": "**Types of bias:**\n- **Selection bias**: non-random inclusion\n- **Survivorship bias**: analyzing only those who 'survived'\n- **Response bias**: self-selection skews who responds\n- **Convenience bias**: sampling whoever is easiest to reach",
                "example": "Surveying NPS only from users who logged in this month excludes churned users — making satisfaction look artificially high.",
                "use_cases": ["Survey design", "A/B test setup", "Market research", "Product feedback analysis"],
                "watch_out": "Always ask: 'Who is NOT in my sample and why?' The absence of data is often as informative as the data itself."
            },
            {
                "title": "15. Linear Regression & Coefficients",
                "definition": "A statistical model that estimates the relationship between one or more independent variables (X) and a dependent variable (Y) by fitting a line.",
                "formula": "Simple:   Y = β₀ + β₁X + ε\nMultiple: Y = β₀ + β₁X₁ + β₂X₂ + ... + ε\n\nR² = 1 − (SS_res / SS_tot)",
                "description": "- **β₀ (intercept)**: predicted Y when all X = 0\n- **β₁ (coefficient)**: change in Y per 1-unit increase in X\n- **R²**: proportion of variance explained by the model\n- **Residuals (ε)**: the unexplained portion — should be random",
                "example": "β₁ for ad spend = 2.5 → every $1 more in ads is associated with $2.50 more in revenue (holding other factors constant).",
                "use_cases": ["Demand forecasting", "Price elasticity analysis", "Sales attribution modeling", "Feature importance estimation"],
                "watch_out": "R² inflates as you add variables. Use Adjusted R² for multiple regression. Regression shows association, not causation."
            },
            {
                "title": "16. Conditional Probability & Bayes' Theorem",
                "definition": "Conditional probability is the likelihood of event A given event B has occurred. Bayes' theorem updates probabilities as new evidence arrives.",
                "formula": "P(A|B) = P(A and B) / P(B)\n\nBayes' Theorem:\nP(A|B) = P(B|A) × P(A) / P(B)\n\nPosterior ∝ Likelihood × Prior",
                "description": "Bayes formalizes belief updating: start with a prior, observe evidence, update to a posterior. This is how spam filters, medical diagnostics, and recommendation systems work.",
                "example": "99% accurate test, 1% disease prevalence. P(disease | positive test) ≈ <strong>50%</strong> — surprisingly low due to rare base rate. Most positives are false alarms.",
                "use_cases": ["Spam email classification", "Medical diagnosis models", "Lead scoring with RFM", "Fraud detection"],
                "watch_out": "Base rate neglect is extremely common. Even a highly accurate test produces mostly false positives for rare conditions."
            },
            {
                "title": "17. Cohort & Segmentation Analysis",
                "definition": "Cohort analysis groups users who share a common characteristic at a specific point in time and tracks their behavior over time.",
                "formula": "Retention Rate at period n =\n  (Active users from cohort still active at n) / Original cohort size × 100",
                "description": "Cohorts separate the effect of time (how long a user has been around) from calendar period (what's happening in the product now). Without cohorts, new retention improvements can be hidden by old cohorts churning.",
                "example": "Jan cohort: 40% retention at 6 months. Jun cohort: 25% at 6 months → product or acquisition quality likely declined.",
                "use_cases": ["SaaS retention analysis", "LTV calculation", "Evaluating product changes over time", "Acquisition channel quality comparison"],
                "watch_out": "Don't compare cohorts of different sizes without normalization. Distinguish early churn (onboarding failure) from long-term churn (value decay)."
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
                "watch_out": "Adding variables always increases R². Use Adjusted R² or cross-validation to assess true quality. Never trust coefficients without checking all assumptions."
            },
            {
                "title": "19. Time Series Basics",
                "definition": "A sequence of data points collected at successive, equally-spaced intervals. Time series analysis decomposes, models, and forecasts these sequences.",
                "formula": "Decomposition: Y(t) = Trend(t) + Seasonality(t) + Noise(t)\nMoving Avg:    MA(k) = (1/k) × Σ Yᵢ  [i = t−k+1 to t]",
                "description": "**Components:**\n- **Trend**: long-term direction\n- **Seasonality**: repeating patterns at fixed intervals\n- **Cyclicality**: irregular longer waves (economic cycles)\n- **Noise**: random unexplained variation\n\nCommon models: ARIMA, Exponential Smoothing, Facebook Prophet",
                "example": "E-commerce sales: upward trend (growth) + December spikes (seasonality) + daily noise. A 7-day moving average smooths the noise to reveal the trend.",
                "use_cases": ["Demand forecasting", "Financial market analysis", "Anomaly detection in metrics", "Capacity planning"],
                "watch_out": "Many models (ARIMA) require stationarity — mean and variance must not change over time. Always test with the Augmented Dickey-Fuller (ADF) test first."
            },
            {
                "title": "20. A/B Testing & Experimental Design",
                "definition": "A controlled experiment that randomly assigns users to variants to measure the causal impact of a change on a defined metric.",
                "formula": "Min sample size per variant:\nn ≈ 2σ²(z_α/2 + z_β)² / δ²\n\nz_α/2 = 1.96  (95% confidence)\nz_β   = 0.84  (80% power)\nδ = minimum detectable effect",
                "description": "**Best practices:**\n1. Formulate hypothesis before running\n2. Pre-calculate required sample size\n3. Randomize assignment (not by date)\n4. Define one primary metric upfront\n5. Do NOT stop early (p-hacking)\n6. Run for full business cycles (full weeks)",
                "example": "Hypothesis: blue CTA button increases signups vs grey. Run until n=5,000 per variant. Result: blue=4.8%, grey=4.0%, p=0.02 → statistically significant → ship it.",
                "use_cases": ["Product feature launches", "Email subject line optimization", "Pricing page changes", "Onboarding flow improvements"],
                "watch_out": "Early stopping is the #1 mistake. Random fluctuation makes early results unreliable. Peeking and stopping inflates your false positive rate to 25%+ even at α=0.05."
            },
            {
                "title": "21. Statistical Power & Sample Size",
                "definition": "Statistical power is the probability a test correctly detects a real effect when one exists (1 − β, target ≥ 0.80).",
                "formula": "Power = 1 − β  (target ≥ 0.80)\n\nPower ↑ when:\n  Sample size ↑\n  Effect size ↑\n  α ↑ (less strict)\n  Variance ↓",
                "description": "| | H₀ True | H₀ False |\n|--|---------|----------|\n| Reject H₀ | ❌ Type I Error (α) | ✅ Correct |\n| Fail to Reject | ✅ Correct | ❌ Type II Error (β) |\n\nUnderpowered tests miss real effects. Overpowered tests detect trivially small, irrelevant effects.",
                "example": "Testing 0.5% lift on a 4% base conversion requires ~75,000 users per variant at 80% power. Low-traffic sites may need months to reach this.",
                "use_cases": ["A/B test planning", "Clinical trial design", "Minimum viable experiment scoping"],
                "watch_out": "Post-hoc power analysis (calculating power after seeing results) is misleading. Always calculate required sample size before starting the experiment."
            },
            {
                "title": "22. Survival / Retention Analysis",
                "definition": "Statistical methods for modeling the time until a specific event occurs (churn, conversion, failure), accounting for users who haven't experienced it yet (censoring).",
                "formula": "Kaplan-Meier Estimator:\nS(t) = Π [ (nᵢ − dᵢ) / nᵢ ]  for all tᵢ ≤ t\n\nnᵢ = users at risk at time t\ndᵢ = events (churn) at time t",
                "description": "**Key concepts:**\n- **S(t)**: probability of surviving (not churning) past time t\n- **Hazard rate**: instantaneous churn risk at time t\n- **Censoring**: users still active (can't be ignored)\n- **Cox Proportional Hazards**: extends survival analysis with covariates (age, plan, etc.)",
                "example": "K-M curve: 80% active at 30 days, 50% at 90 days, 30% at 180 days. Steepest drop in first 2 weeks → onboarding problem.",
                "use_cases": ["SaaS churn prediction", "Customer LTV modeling", "Medical device failure analysis", "Credit risk duration modeling"],
                "watch_out": "Censoring must be non-informative — users shouldn't drop out because they're about to churn. Violation of this biases the survival estimates significantly."
            },
            {
                "title": "23. Simpson's Paradox & Statistical Pitfalls",
                "definition": "Simpson's Paradox: a trend that appears in aggregate data disappears or reverses when broken down by subgroups.",
                "formula": "No formula — it's a structural reasoning failure.\nCheck: Do aggregate trends match all subgroup trends?",
                "description": "**Common pitfalls:**\n- **Simpson's Paradox**: aggregate trend reverses when segmented\n- **P-hacking**: running many tests and reporting only significant ones\n- **HARKing**: Hypothesizing After Results are Known\n- **Base rate neglect**: ignoring how rare an event is\n- **Ecological fallacy**: inferring individual behavior from group statistics",
                "example": "Hospital A has higher overall survival than Hospital B. But Hospital B is better for BOTH mild and severe cases — it just handles more severe cases. Aggregate % hides this.",
                "use_cases": ["Multi-segment reporting", "Policy evaluation", "Medical and social research", "Experiment post-mortems"],
                "watch_out": "Always segment your data before drawing conclusions. A single aggregate number almost never tells the whole story."
            },
            {
                "title": "24. Index Numbers & Weighted Averages",
                "definition": "An index expresses a value relative to a reference (base) period. A weighted average assigns different importance to values based on their relative size or relevance.",
                "formula": "Index         = (Current Value / Base Value) × 100\nWeighted Avg  = Σ(value × weight) / Σ(weight)",
                "description": "**When to use weighted averages:** When groups have very different sizes, a simple average is misleading. A 90% retention rate from 10 users should NOT be weighted equally with 90% from 10,000 users.",
                "example": "Simple avg of [50%, 90%] = 70%.<br>If group sizes are 100 and 1,000: weighted avg = (50×100 + 90×1000) / 1100 = <strong>86.4%</strong>",
                "use_cases": ["CPI and price indices", "Portfolio performance", "Blended metrics across segments", "NPS and satisfaction indices"],
                "watch_out": "Wrong weights massively distort results. Document your weighting methodology explicitly, and revisit it as group sizes change over time."
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
                "watch_out": "Information gain favors features with many unique values (like IDs). Use Gain Ratio (C4.5) or Gini impurity (CART) to correct for this bias."
            },
            {
                "title": "26. Bias–Variance Tradeoff",
                "definition": "The fundamental ML tension between a model too simple to capture patterns (high bias / underfitting) and one too complex that memorizes noise (high variance / overfitting).",
                "formula": "Total Error = Bias² + Variance + Irreducible Noise\n\nHigh Bias:     train error ≈ test error (both high)\nHigh Variance: train error << test error",
                "description": "| | High Bias | High Variance |\n|---|---|---|\n| Also called | Underfitting | Overfitting |\n| Train error | High | Low |\n| Test error | High | High |\n| Fix | More complexity | Regularization / more data |\n| Example | Linear model on nonlinear data | Deep tree, no pruning |",
                "example": "Decision tree depth=1 (stump): underfits. Depth=30: memorizes training data. Optimal depth (e.g., 5–7) balances both.",
                "use_cases": ["Model selection", "Hyperparameter tuning", "Diagnosing train vs. validation performance gaps"],
                "watch_out": "More data reduces variance but NOT bias. If a model is underfitting, getting more data won't help — you need to increase model capacity."
            },
            {
                "title": "27. Cross-Validation",
                "definition": "A technique to estimate model generalization by training and testing on multiple non-overlapping splits of the data.",
                "formula": "k-Fold CV Score = (1/k) × Σ score(fold_i)\n\nReport: mean ± std across folds",
                "description": "**How k-Fold CV works:**\n1. Split data into k equal folds (typically k=5 or 10)\n2. Train on k−1 folds, test on the held-out fold\n3. Rotate until each fold has been the test set once\n4. Average the k scores\n\n**Stratified k-Fold** preserves class balance in each fold — essential for imbalanced datasets.",
                "example": "5-fold CV scores: [0.82, 0.85, 0.81, 0.84, 0.83] → CV = <strong>0.83 ± 0.015</strong>. Far more reliable than one train/test split.",
                "use_cases": ["Model selection and comparison", "Hyperparameter tuning (nested CV)", "Performance estimation before deployment"],
                "watch_out": "Data leakage through the CV loop is critical: preprocessing steps (scaling, imputation) must be fit INSIDE each fold, never on the full dataset."
            },
            {
                "title": "28. Regularization (L1 & L2)",
                "definition": "A technique adding a penalty to the loss function to discourage large coefficients, reducing overfitting by constraining model complexity.",
                "formula": "L1 (Lasso):   Loss = MSE + λ × Σ|βᵢ|\nL2 (Ridge):   Loss = MSE + λ × Σβᵢ²\nElastic Net:  Loss = MSE + λ₁Σ|βᵢ| + λ₂Σβᵢ²",
                "description": "| | L1 (Lasso) | L2 (Ridge) |\n|--|--|--|\n| Effect | Drives some coefficients to exactly 0 | Shrinks all toward 0 |\n| Result | Sparse model (feature selection) | Dense model |\n| Use when | Many irrelevant features | All features contribute |",
                "example": "With 100 features, Lasso (λ=0.1) zeros out 80 — effectively automatic feature selection, leaving 20 active predictors.",
                "use_cases": ["Preventing overfitting in regression", "Automatic feature selection (L1)", "Neural network weight decay (L2)", "High-dimensional datasets"],
                "watch_out": "λ is a critical hyperparameter. Too high → underfitting. Too low → no regularization. Use LassoCV or RidgeCV for automatic cross-validated tuning."
            },
            {
                "title": "29. Gradient Descent",
                "definition": "An iterative optimization algorithm that minimizes a loss function by repeatedly updating parameters in the direction of the steepest negative gradient.",
                "formula": "θ := θ − α × ∇J(θ)\n\nα     = learning rate\n∇J(θ) = gradient of loss w.r.t. parameters θ",
                "description": "| Variant | Data per step | Pros | Cons |\n|---------|--------------|------|------|\n| Batch GD | All data | Stable convergence | Slow on large datasets |\n| SGD | 1 sample | Fast updates | Very noisy |\n| Mini-batch | 32–512 samples | Best of both | Needs tuning |\n\nAdaptive optimizers (Adam, RMSprop) automatically adjust α per parameter.",
                "example": "In linear regression, gradient descent iteratively adjusts weights: if predicted value is too high, reduce the coefficient proportionally to the prediction error.",
                "use_cases": ["Training neural networks", "Logistic regression optimization", "Any differentiable loss minimization", "Deep learning (Adam optimizer)"],
                "watch_out": "Learning rate α is critical. Too large → diverge (overshoot minimum). Too small → extremely slow convergence. Use learning rate schedulers in production."
            },
            {
                "title": "30. Confusion Matrix & Classification Metrics",
                "definition": "A confusion matrix summarizes classifier performance by comparing actual vs. predicted labels across all classes.",
                "formula": "Accuracy  = (TP+TN) / (TP+TN+FP+FN)\nPrecision = TP / (TP+FP)\nRecall    = TP / (TP+FN)\nF1        = 2×(P×R) / (P+R)\nMCC       = (TP×TN−FP×FN) / √((TP+FP)(TP+FN)(TN+FP)(TN+FN))",
                "description": "|  | Predicted + | Predicted − |\n|--|--|--|\n| **Actual +** | TP ✅ | FN ❌ (missed) |\n| **Actual −** | FP ❌ (false alarm) | TN ✅ |\n\n- **Precision**: of all predicted positives, how many are correct?\n- **Recall**: of all actual positives, how many did we catch?\n- **F1**: harmonic mean, balances precision and recall\n- **AUC-ROC**: overall discriminative ability across all thresholds",
                "example": "Fraud detection: missing fraud (FN) is very costly → maximize Recall. Spam filter: false positives delete real emails → maximize Precision. When both matter → use F1.",
                "use_cases": ["Model evaluation", "Threshold selection", "Class imbalance analysis", "Reporting classifier performance"],
                "watch_out": "Accuracy is useless for imbalanced classes. A model predicting 'no fraud' always gets 99% accuracy on a 1% fraud dataset. Use F1, AUC-ROC, or MCC instead."
            },
            {
                "title": "31. Dimensionality Reduction (PCA, t-SNE, UMAP)",
                "definition": "Techniques to reduce the number of features while preserving important structure, relationships, or variance in the data.",
                "formula": "PCA steps:\n  1. Standardize data (mean=0, SD=1)\n  2. Compute covariance matrix\n  3. Eigendecomposition → principal components\n  4. Project onto top k eigenvectors\n\nExplained Variance Ratio = λ_k / Σλ",
                "description": "| Method | Type | Preserves | Speed | Use For |\n|--------|------|-----------|-------|---------|\n| PCA | Linear | Global variance | Fast | Preprocessing, noise reduction |\n| t-SNE | Non-linear | Local clusters | Slow | 2D/3D visualization |\n| UMAP | Non-linear | Local + global | Moderate | Visualization + downstream ML |",
                "example": "100-feature customer dataset → 10 PCA components explain 95% of variance → train on 10 components, reducing overfitting and training time significantly.",
                "use_cases": ["Visualization of high-dimensional data", "Noise reduction before modeling", "Feature extraction", "Genomics and NLP embeddings"],
                "watch_out": "t-SNE is for visualization only — its axes carry no meaning and inter-cluster distances are unreliable. Never use t-SNE output as ML input features."
            },
            {
                "title": "32. Loss Functions",
                "definition": "A loss function quantifies the gap between a model's predictions and actual values, serving as the objective to minimize during training.",
                "formula": "MSE      = (1/n) × Σ(yᵢ − ŷᵢ)²\nMAE      = (1/n) × Σ|yᵢ − ŷᵢ|\nLog Loss = −(1/n) × Σ[yᵢlog(ŷᵢ) + (1−yᵢ)log(1−ŷᵢ)]",
                "description": "| Loss | Task | Outlier Sensitive | |\n|------|------|-------------------|--|\n| MSE | Regression | Yes (squares errors) | Smooth gradient |\n| MAE | Regression | No | Non-differentiable at 0 |\n| Huber | Regression | No | Best of both |\n| Log Loss | Binary classification | — | Penalizes confident errors |\n| Cross-entropy | Multi-class | — | Standard in deep learning |",
                "example": "House prices with a $2M outlier: MSE penalizes it 4× more than MAE. Use Huber loss when outliers are expected but shouldn't dominate training.",
                "use_cases": ["Training all supervised ML models", "Custom objectives for business constraints", "Evaluating model performance", "Choosing model objectives"],
                "watch_out": "Log loss heavily penalizes confident wrong predictions (e.g., P=0.99 for the wrong class). If your model is miscalibrated, use Platt scaling or isotonic regression."
            },
            {
                "title": "33. Feature Engineering & Encoding",
                "definition": "The process of transforming raw data into informative, model-ready features that improve predictive performance.",
                "formula": "Min-Max:      x' = (x − min) / (max − min)\nZ-score:      x' = (x − μ) / σ\nLog transform: x' = log(x + 1)",
                "description": "**Encoding categorical variables:**\n- **One-hot**: binary column per category (nominal, low cardinality)\n- **Label encoding**: integers 0,1,2 (ordinal only)\n- **Target encoding**: replace with mean target value (leakage risk)\n- **Frequency encoding**: replace with category count\n\n**Numerical transformations:**\n- Log transform: reduces right skew\n- Polynomial features: captures non-linear relationships\n- Binning: converts continuous to ordinal",
                "example": "City with 50 unique values → target encoding replaces each city with its historical conversion rate. Far fewer dimensions than one-hot, but must be computed inside CV folds.",
                "use_cases": ["All supervised ML pipelines", "Reducing cardinality in tree models", "Preparing features for neural networks", "NLP preprocessing"],
                "watch_out": "Target encoding leaks label information. Always compute it inside CV folds using only training data — never on the full dataset before splitting."
            },
            {
                "title": "34. Class Imbalance Techniques",
                "definition": "Methods to handle datasets where one class significantly outnumbers another, causing models to be biased toward predicting the majority class.",
                "formula": "SMOTE: interpolate between k-nearest minority neighbors\n\nClass weight:\n  w_minority = n_total / (2 × n_minority)\n  w_majority = n_total / (2 × n_majority)",
                "description": "| Approach | Method | When to Use |\n|----------|--------|-------------|\n| Data-level | SMOTE oversampling | Moderate imbalance |\n| Data-level | Random undersampling | Very large majority class |\n| Algorithm-level | Class weighting | Most sklearn classifiers support it |\n| Threshold-level | Adjust decision threshold | Tune precision/recall tradeoff |\n| Ensemble | BalancedBagging | Complex tasks |",
                "example": "Fraud: 99% non-fraud. Model predicts 'no fraud' always → 99% accuracy, 0% recall. Apply 1:99 class weights → recall improves dramatically.",
                "use_cases": ["Fraud detection", "Medical diagnosis", "Rare event prediction", "Anomaly detection"],
                "watch_out": "SMOTE creates synthetic points that may not reflect real data. Never oversample the test set — always oversample only inside training folds."
            },
            {
                "title": "35. Bayesian vs Frequentist Statistics",
                "definition": "Two competing philosophical frameworks for statistical inference that differ in how they define probability and treat unknown parameters.",
                "formula": "Frequentist: P(data | hypothesis)  →  p-value\n\nBayesian:    P(hypothesis | data) ∝ P(data | hypothesis) × P(hypothesis)\n             posterior ∝ likelihood × prior",
                "description": "| Dimension | Frequentist | Bayesian |\n|-----------|-------------|----------|\n| Probability means | Long-run frequency | Degree of belief |\n| Parameters | Fixed, unknown | Random, have distributions |\n| Output | p-values, CIs | Posterior distributions |\n| Prior knowledge | Not incorporated | Explicitly used |\n| Sample size | Fixed upfront | Can update incrementally |",
                "example": "Bayesian A/B test output: 'P(B > A) = 94%' — directly interpretable for business decisions. No need to wait for fixed sample size; can stop when posterior is conclusive.",
                "use_cases": ["A/B testing with small samples", "Updating models incrementally", "Spam filtering (Naive Bayes)", "Medical decisions under uncertainty"],
                "watch_out": "Bayesian results depend on the prior. Uninformative priors reduce this but don't eliminate it. Document your prior assumptions explicitly and test sensitivity."
            },
            {
                "title": "36. Monte Carlo Simulation",
                "definition": "A computational technique using repeated random sampling to estimate the probability distribution of outcomes that depend on uncertain inputs.",
                "formula": "E[f(X)] ≈ (1/N) × Σ f(xᵢ)   where xᵢ ~ P(X)\n\nLaw of Large Numbers:\n  estimate → true value as N → ∞",
                "description": "**Steps:**\n1. Define probability distributions for each uncertain input\n2. Randomly sample from each distribution (N=10,000+ iterations)\n3. Compute output for each scenario\n4. Analyze resulting output distribution (mean, CI, P(loss))\n\n**Common input distributions:** Normal, Uniform, Triangular, Poisson",
                "example": "Project profit: revenue ~ N($500K, $50K), cost ~ N($400K, $40K). 100K simulations → P(profit > 0) = 89%, median profit = $95K, 5th percentile = −$20K.",
                "use_cases": ["Financial risk modeling (VaR)", "Supply chain scenario planning", "Option pricing", "Project timeline estimation", "Sensitivity analysis"],
                "watch_out": "Results are only as good as your input distributions — garbage in, garbage out. Always run sensitivity analysis to identify which inputs drive the most output variance."
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
st.sidebar.caption("36 topics · 4 levels")


# ─────────────────────────────────────────────
# RENDER
# ─────────────────────────────────────────────
def topic_matches(t, q):
    q = q.lower()
    return any(
        q in (t.get(k) or "").lower()
        for k in ["title", "definition", "description", "example", "formula", "watch_out"]
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
        f'<span class="badge {content["badge"]}">{level}</span>', unsafe_allow_html=True)

    cols = st.columns(2)
    for i, topic in enumerate(topics):
        with cols[i % 2]:
            with st.expander(f"**{topic['title']}**", expanded=False):
                render_topic(topic)

    st.markdown("---")

if search and total_shown == 0:
    st.info(f"No topics found for **'{search}'**. Try a different keyword.")

st.caption(f"📊 Data & Statistics Cheat Sheet · {total_shown} topics shown")

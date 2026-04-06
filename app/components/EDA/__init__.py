import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


@st.cache_data
def load_dataset(csv_file):
    return pd.read_csv(csv_file, encoding='latin-1')


def _num_cat(df):
    num = df.select_dtypes(include="number").columns.tolist()
    cat = df.select_dtypes(include=["object", "category"]).columns.tolist()
    return num, cat


def _missing(df):
    m = df.isnull().sum()
    mdf = pd.DataFrame(
        {"Missing": m, "Missing %": (m / len(df) * 100).round(2)})
    return mdf[mdf["Missing"] > 0]


def _iqr_outliers(df, col):
    Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
    IQR = Q3 - Q1
    mask = (df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)
    return mask.sum()


def _color_pair(cfg):
    return cfg.get("color_pair", ["#4C72B0", "#DD8452"])


def section_overview(df, cfg):
    num_cols, cat_cols = _num_cat(df)
    mdf = _missing(df)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", f"{len(df):,}")
    c2.metric("Columns", df.shape[1])
    c3.metric("Numeric", len(num_cols))
    c4.metric("Missing cols", len(mdf))

    with st.expander("Column types & sample data"):
        dtype_df = pd.DataFrame(
            {"Column": df.columns, "Type": df.dtypes.astype(str).values})
        st.dataframe(dtype_df, width='stretch', hide_index=True)

    if not mdf.empty:
        st.markdown("**Missing Values**")
        fig = px.bar(mdf.reset_index(), x="index", y="Missing %",
                     color="Missing %", color_continuous_scale="Reds",
                     labels={"index": "Column"})
        fig.update_layout(height=300, margin=dict(t=30, b=0))
        st.plotly_chart(fig, width='stretch')
    else:
        st.success("✓ No missing values")


def section_descriptive(df, cfg):
    num_cols, _ = _num_cat(df)
    if not num_cols:
        st.info("No numeric columns.")
        return

    st.dataframe(df[num_cols].describe().round(3), width='stretch')

    skew_kurt = pd.DataFrame({
        "Skewness": df[num_cols].skew().round(3),
        "Kurtosis": df[num_cols].kurtosis().round(3),
    })
    high_skew = skew_kurt[skew_kurt["Skewness"].abs() > 1].index.tolist()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Skewness & Kurtosis**")
        st.dataframe(skew_kurt, width='stretch')
    with col2:
        if high_skew:
            st.warning(f"⚠️ Highly skewed (|skew| > 1): {', '.join(high_skew)}\n\n"
                       "Consider log-transform before modeling.")
        else:
            st.success("✓ No highly skewed columns")


def section_outliers(df, cfg):
    num_cols, _ = _num_cat(df)
    if not num_cols:
        return

    rows = []
    for col in num_cols:
        n = _iqr_outliers(df, col)
        rows.append({"Column": col, "Outlier Count": n,
                     "Outlier %": round(n / len(df) * 100, 2)})
    odf = pd.DataFrame(rows).set_index("Column")

    fig = px.bar(odf.reset_index(), x="Column", y="Outlier %",
                 color="Outlier %", color_continuous_scale="Oranges")
    fig.update_layout(height=320, margin=dict(t=30, b=0))
    st.plotly_chart(fig, width='stretch')

    with st.expander("Full outlier table"):
        st.dataframe(odf, width='stretch')


def section_univariate(df, cfg):
    num_cols, cat_cols = _num_cat(df)
    colors = _color_pair(cfg)

    if num_cols:
        st.markdown("**Numeric Distributions**")
        cols_per_row = 3
        cols_to_show = num_cols[:12]  # cap at 12 to keep it readable
        rows = (len(cols_to_show) + cols_per_row - 1) // cols_per_row
        fig = make_subplots(rows=rows, cols=cols_per_row,
                            subplot_titles=cols_to_show)
        for i, col in enumerate(cols_to_show):
            r, c = divmod(i, cols_per_row)
            fig.add_trace(
                go.Histogram(x=df[col], name=col, showlegend=False,
                             marker_color=colors[0]),
                row=r + 1, col=c + 1
            )
        fig.update_layout(height=280 * rows, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')

    if cat_cols:
        st.markdown("**Categorical Distributions**")
        show_cats = [c for c in cat_cols if df[c].nunique() <= 30][:6]
        if show_cats:
            for i in range(0, len(show_cats), 3):
                row_cols = st.columns(3)
                for j, col in enumerate(show_cats[i:i+3]):
                    vc = df[col].value_counts().head(15).reset_index()
                    vc.columns = [col, "count"]
                    fig = px.bar(vc, x=col, y="count",
                                 color="count", color_continuous_scale="Blues")
                    fig.update_layout(height=260, margin=dict(t=30, b=0),
                                      showlegend=False, coloraxis_showscale=False)
                    row_cols[j].plotly_chart(fig, width='stretch')


def section_target(df, cfg):
    target = cfg.get("target")
    if not target or target not in df.columns:
        st.info("No target column configured for this dataset.")
        return

    colors = _color_pair(cfg)
    ttype = cfg.get("target_type", "binary")
    pos = cfg.get("target_positive_label", 1)

    vc = df[target].value_counts().reset_index()
    vc.columns = [target, "count"]

    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(vc, names=target, values="count",
                     color_discrete_sequence=colors)
        fig.update_layout(height=300, margin=dict(t=30, b=0))
        st.plotly_chart(fig, width='stretch')

    with c2:
        if ttype == "binary":
            rate = df[target].mean() * 100
        else:
            rate = (df[target] == pos).mean() * 100

        st.metric("Positive class rate", f"{rate:.2f}%")
        if rate < 15 or rate > 85:
            imb = max(rate, 100 - rate) / min(rate, 100 - rate)
            st.warning(f"⚠️ Class imbalance detected ({imb:.1f}:1 ratio).\n\n"
                       "Consider SMOTE or `class_weight='balanced'`.")
        else:
            st.success("✓ Reasonably balanced classes")

    # Bivariate: key numerics vs target
    key_num = [c for c in cfg.get("key_num", []) if c in df.columns][:4]
    if key_num:
        st.markdown("**Key Features vs Target**")
        cols_row = st.columns(len(key_num))
        for i, col in enumerate(key_num):
            fig = px.box(df, x=str(target), y=col,
                         color=str(target), color_discrete_sequence=colors)
            fig.update_layout(height=280, margin=dict(
                t=30, b=0), showlegend=False)
            cols_row[i].plotly_chart(fig, width='stretch')


def section_bivariate(df, cfg):
    num_cols, _ = _num_cat(df)
    colors = _color_pair(cfg)

    # Pair plot (sample)
    pair_candidates = [c for c in cfg.get(
        "key_num", []) if c in df.columns][:5]
    if not pair_candidates:
        pair_candidates = num_cols[:5]

    target = cfg.get("target")
    if len(pair_candidates) >= 3:
        st.markdown("**Pair Plot** (sampled)")
        sample = df.sample(min(2000, len(df)), random_state=42)
        fig = px.scatter_matrix(
            sample, dimensions=pair_candidates,
            color=str(target) if target and target in df.columns else None,
            color_discrete_sequence=colors, opacity=0.45,
        )
        fig.update_traces(diagonal_visible=False, showupperhalf=False)
        fig.update_layout(height=550, margin=dict(t=30, b=0))
        st.plotly_chart(fig, width='stretch')

    # Group cols bar charts vs target
    group_cols = [c for c in cfg.get("group_cols", []) if c in df.columns][:4]
    if group_cols and target and target in df.columns:
        st.markdown(f"**Categorical Breakdown vs {target}**")
        for i in range(0, len(group_cols), 2):
            row_cols = st.columns(2)
            for j, col in enumerate(group_cols[i:i+2]):
                grp = df.groupby([col, str(target)]).size(
                ).reset_index(name="count")
                fig = px.bar(grp, x=col, y="count", color=str(target),
                             barmode="group", color_discrete_sequence=colors)
                fig.update_layout(height=300, margin=dict(t=30, b=0))
                row_cols[j].plotly_chart(fig, width='stretch')


def section_correlation(df, cfg):
    num_cols, _ = _num_cat(df)
    if len(num_cols) < 2:
        st.info("Not enough numeric columns for correlation.")
        return

    use_cols = num_cols[:20]  # cap
    corr = df[use_cols].corr().round(2)

    fig = px.imshow(corr, color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
                    text_auto=True, aspect="auto")
    fig.update_layout(height=max(400, len(use_cols) * 35),
                      margin=dict(t=30, b=0))
    st.plotly_chart(fig, width='stretch')

    high_corr = [
        (c1, c2, round(corr.loc[c1, c2], 2))
        for c1 in corr.columns for c2 in corr.columns
        if c1 < c2 and abs(corr.loc[c1, c2]) > 0.8
    ]
    if high_corr:
        st.warning("⚠️ High correlations (|r| > 0.8) — multicollinearity risk:")
        hc_df = pd.DataFrame(high_corr, columns=[
                             "Feature A", "Feature B", "r"])
        st.dataframe(hc_df, width='stretch', hide_index=True)
    else:
        st.success("✓ No severe multicollinearity detected (|r| ≤ 0.8)")


def section_insights(df, cfg, dataset_name):
    num_cols, cat_cols = _num_cat(df)
    mdf = _missing(df)
    target = cfg.get("target")
    colors = _color_pair(cfg)

    items = [
        f"**Total records:** {len(df):,}",
        f"**Numeric columns:** {len(num_cols)}",
        f"**Categorical columns:** {len(cat_cols)}",
    ]

    if mdf.empty:
        items.append("**Missing values:** None ✓")
    else:
        items.append(f"**Missing values:** {list(mdf.index)}")

    if num_cols:
        skew = df[num_cols].skew()
        high_skew = skew[skew.abs() > 1].index.tolist()
        if high_skew:
            items.append(
                f"**Highly skewed cols:** {high_skew} — consider log-transform")

    if target and target in df.columns:
        ttype = cfg.get("target_type", "binary")
        pos = cfg.get("target_positive_label", 1)
        if ttype == "binary":
            rate = df[target].mean() * 100
        else:
            rate = (df[target] == pos).mean() * 100
        items.append(f"**Positive class rate:** {rate:.2f}%")
        if rate < 15:
            items.append(
                "⚠️ **Class imbalance** — recommend SMOTE or `class_weight='balanced'`")

    if len(num_cols) >= 2:
        corr = df[num_cols[:20]].corr()
        high_corr = [
            (c1, c2, round(corr.loc[c1, c2], 2))
            for c1 in corr.columns for c2 in corr.columns
            if c1 < c2 and abs(corr.loc[c1, c2]) > 0.8
        ]
        if high_corr:
            items.append(f"**High correlations (|r|>0.8):** {high_corr[:3]}")

    # Domain-specific KPIs
    domain = cfg.get("domain")
    if domain == "retail" and "Sales" in df.columns:
        items.append(f"**Total sales:** ${df['Sales'].sum():,.2f}")
        if "Profit" in df.columns:
            items.append(
                f"**Profit margin:** {df['Profit'].sum()/df['Sales'].sum()*100:.2f}%")
    if "charges" in df.columns:
        items.append(f"**Avg charges:** ${df['charges'].mean():,.2f}")
    if "price" in df.columns and domain == "real_estate":
        items.append(
            f"**Avg listing price:** ${pd.to_numeric(df['price'], errors='coerce').mean():,.2f}/night")
    if "popularity" in df.columns:
        items.append(
            f"**Avg track popularity:** {df['popularity'].mean():.1f}/100")

    for item in items:
        st.markdown(f"- {item}")


def domain_finance_credit(df, cfg):
    colors = _color_pair(cfg)
    target = cfg.get("target")

    if "loan_grade" in df.columns and target and target in df.columns:
        grade_def = df.groupby("loan_grade")[target].mean().reset_index()
        grade_def.columns = ["loan_grade", "default_rate"]
        grade_def["default_rate"] = (grade_def["default_rate"] * 100).round(2)
        grade_def = grade_def.sort_values("loan_grade")
        fig = px.bar(grade_def, x="loan_grade", y="default_rate",
                     color="default_rate", color_continuous_scale="Reds",
                     title="Default Rate by Loan Grade",
                     labels={"default_rate": "Default Rate (%)"})
        fig.update_layout(height=320, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')

    if "loan_intent" in df.columns and target and target in df.columns:
        intent_def = df.groupby("loan_intent")[target].mean().reset_index()
        intent_def.columns = ["loan_intent", "default_rate"]
        intent_def["default_rate"] = (
            intent_def["default_rate"] * 100).round(2)
        intent_def = intent_def.sort_values("default_rate", ascending=False)
        fig = px.bar(intent_def, x="loan_intent", y="default_rate",
                     color="default_rate", color_continuous_scale="Reds",
                     title="Default Rate by Loan Intent")
        fig.update_layout(height=320, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')

    if "loan_amnt" in df.columns and "person_income" in df.columns:
        df = df.copy()
        df["loan_to_income"] = (
            df["loan_amnt"] / df["person_income"]).replace([np.inf, -np.inf], np.nan)
        fig = px.histogram(df, x="loan_to_income", nbins=50,
                           color=str(
                               target) if target and target in df.columns else None,
                           title="Loan-to-Income Ratio",
                           color_discrete_sequence=colors, opacity=0.75)
        fig.update_layout(height=320, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')


def domain_finance_loan(df, cfg):
    colors = _color_pair(cfg)
    target = cfg.get("target")

    if "ApplicantIncome" in df.columns and "LoanAmount" in df.columns:
        fig = px.scatter(df, x="ApplicantIncome", y="LoanAmount",
                         color=str(
                             target) if target and target in df.columns else None,
                         title="Applicant Income vs Loan Amount",
                         color_discrete_sequence=colors, opacity=0.6)
        fig.update_layout(height=360, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')

    for col in ["Education", "Self_Employed", "Credit_History"]:
        if col in df.columns and target and target in df.columns:
            grp = df.groupby([col, target]).size().reset_index(name="count")
            fig = px.bar(grp, x=col, y="count", color=str(target), barmode="group",
                         title=f"Loan Status by {col}",
                         color_discrete_sequence=colors)
            fig.update_layout(height=300, margin=dict(t=40, b=0))
            st.plotly_chart(fig, width='stretch')


def domain_retail_superstore(df, cfg):
    colors = _color_pair(cfg)

    if "Order Date" in df.columns:
        df = df.copy()
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
        df["Order Year"] = df["Order Date"].dt.year

    if "Order Date" in df.columns and "Sales" in df.columns:
        monthly = df.groupby(df["Order Date"].dt.to_period("M"))[
            "Sales"].sum().reset_index()
        monthly["Order Date"] = monthly["Order Date"].astype(str)
        fig = px.line(monthly, x="Order Date", y="Sales", markers=True,
                      title="Monthly Sales Over Time",
                      color_discrete_sequence=[colors[0]])
        fig.update_xaxes(tickangle=45)
        fig.update_layout(height=340, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')

    if "Category" in df.columns:
        cat_sum = df.groupby("Category")[
            ["Sales", "Profit"]].sum().reset_index()
        fig = px.bar(cat_sum.melt(id_vars="Category", value_vars=["Sales", "Profit"]),
                     x="Category", y="value", color="variable", barmode="group",
                     title="Sales & Profit by Category",
                     color_discrete_sequence=colors)
        fig.update_layout(height=320, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')

    if "Sub-Category" in df.columns and "Profit" in df.columns:
        subcat = df.groupby("Sub-Category")["Profit"].sum().reset_index()
        subcat = subcat.sort_values("Profit", ascending=False).head(10)
        fig = px.bar(subcat, x="Profit", y="Sub-Category", orientation="h",
                     title="Top 10 Sub-Categories by Profit",
                     color="Profit", color_continuous_scale="RdYlGn")
        fig.update_layout(yaxis={"categoryorder": "total ascending"},
                          height=340, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')

    if "Discount" in df.columns and "Profit" in df.columns:
        fig = px.scatter(df, x="Discount", y="Profit",
                         color="Category" if "Category" in df.columns else None,
                         title="Discount vs Profit",
                         opacity=0.5, color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(height=340, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')


def domain_retail_shopping(df, cfg):
    colors = _color_pair(cfg)
    df = df.copy()
    if "quantity" in df.columns and "price" in df.columns and "total_spend" not in df.columns:
        df["total_spend"] = df["quantity"] * df["price"]

    if "invoice_date" in df.columns:
        df["invoice_date"] = pd.to_datetime(
            df["invoice_date"], dayfirst=True, errors="coerce")
        monthly = df.groupby(df["invoice_date"].dt.to_period("M"))[
            "total_spend"].sum().reset_index()
        monthly["invoice_date"] = monthly["invoice_date"].astype(str)
        fig = px.line(monthly, x="invoice_date", y="total_spend", markers=True,
                      title="Monthly Total Spend",
                      color_discrete_sequence=[colors[0]])
        fig.update_layout(height=320, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')

    for col in ["category", "shopping_mall", "payment_method"]:
        if col in df.columns and "total_spend" in df.columns:
            grp = df.groupby(col)["total_spend"].sum().reset_index(
            ).sort_values("total_spend", ascending=False).head(10)
            fig = px.bar(grp, x=col, y="total_spend",
                         title=f"Total Spend by {col.replace('_', ' ').title()}",
                         color="total_spend", color_continuous_scale="Oranges")
            fig.update_layout(height=300, margin=dict(t=40, b=0))
            st.plotly_chart(fig, width='stretch')


def domain_hr(df, cfg, dataset_name):
    colors = _color_pair(cfg)
    target = cfg.get("target")

    if dataset_name == "HR Attrition":
        if "YearsAtCompany" in df.columns and target and target in df.columns:
            df = df.copy()
            df["tenure_band"] = pd.cut(df["YearsAtCompany"],
                                       bins=[0, 2, 5, 10, 100],
                                       labels=["0–2 yrs", "3–5 yrs", "6–10 yrs", "10+ yrs"])
            tb = df.groupby("tenure_band", observed=True)[target].apply(
                lambda x: (x == "Yes").mean() * 100
            ).reset_index()
            tb.columns = ["tenure_band", "attrition_rate"]
            fig = px.bar(tb, x="tenure_band", y="attrition_rate",
                         color="attrition_rate", color_continuous_scale="Reds",
                         title="Attrition Rate by Tenure Band",
                         labels={"attrition_rate": "Attrition Rate (%)"})
            fig.update_layout(height=320, margin=dict(t=40, b=0))
            st.plotly_chart(fig, width='stretch')

        if "JobRole" in df.columns and "MonthlyIncome" in df.columns:
            inc = df.groupby("JobRole")["MonthlyIncome"].median(
            ).reset_index().sort_values("MonthlyIncome", ascending=False)
            fig = px.bar(inc, x="MonthlyIncome", y="JobRole", orientation="h",
                         title="Median Monthly Income by Job Role",
                         color="MonthlyIncome", color_continuous_scale="Purples")
            fig.update_layout(yaxis={"categoryorder": "total ascending"},
                              height=360, margin=dict(t=40, b=0))
            st.plotly_chart(fig, width='stretch')

        if "Gender" in df.columns and "MonthlyIncome" in df.columns and "JobLevel" in df.columns:
            fig = px.box(df, x="JobLevel", y="MonthlyIncome", color="Gender",
                         title="Income by Job Level & Gender (Pay Equity)",
                         color_discrete_sequence=colors)
            fig.update_layout(height=340, margin=dict(t=40, b=0))
            st.plotly_chart(fig, width='stretch')

        for col in ["JobSatisfaction", "WorkLifeBalance", "EnvironmentSatisfaction", "OverTime"]:
            if col in df.columns and target and target in df.columns:
                grp = df.groupby([col, target]).size(
                ).reset_index(name="count")
                fig = px.bar(grp, x=col, y="count", color=str(target), barmode="group",
                             title=f"{col} vs {target}",
                             color_discrete_sequence=colors)
                fig.update_layout(height=300, margin=dict(t=40, b=0))
                st.plotly_chart(fig, width='stretch')

    else:
        # Generic employee dataset
        cat_cols = df.select_dtypes(
            include=["object", "category"]).columns.tolist()
        for col in cat_cols[:4]:
            vc = df[col].value_counts().reset_index()
            vc.columns = [col, "count"]
            fig = px.bar(vc, x=col, y="count", title=f"{col} Distribution",
                         color="count", color_continuous_scale="Purples")
            fig.update_layout(height=300, margin=dict(t=40, b=0))
            st.plotly_chart(fig, width='stretch')


def domain_insurance(df, cfg):
    colors = _color_pair(cfg)

    if "charges" in df.columns:
        fig = px.histogram(df, x="charges", nbins=50,
                           title="Insurance Charges Distribution",
                           color_discrete_sequence=[colors[0]])
        fig.add_vline(x=df["charges"].median(), line_dash="dash", line_color="gray",
                      annotation_text=f"Median ${df['charges'].median():,.0f}")
        fig.update_layout(height=320, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')

    if "smoker" in df.columns and "charges" in df.columns:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.box(df, x="smoker", y="charges", color="smoker",
                         title="Charges by Smoker Status",
                         color_discrete_sequence=colors)
            fig.update_layout(height=320, margin=dict(
                t=40, b=0), showlegend=False)
            st.plotly_chart(fig, width='stretch')
        with c2:
            sa = df[df["smoker"] == "yes"]["charges"].mean()
            nsa = df[df["smoker"] == "no"]["charges"].mean()
            st.metric("Smoker avg charges", f"${sa:,.0f}")
            st.metric("Non-smoker avg charges", f"${nsa:,.0f}")
            st.metric("Smoker premium", f"{sa/nsa:.1f}×")

    if "bmi" in df.columns and "charges" in df.columns and "smoker" in df.columns:
        fig = px.scatter(df, x="bmi", y="charges", color="smoker",
                         title="BMI vs Charges (smoker amplifies relationship)",
                         opacity=0.6, color_discrete_sequence=colors)
        fig.add_vline(x=30, line_dash="dash", line_color="gray",
                      annotation_text="Obesity threshold (30)")
        fig.update_layout(height=360, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')

    if "region" in df.columns and "charges" in df.columns:
        fig = px.box(df, x="region", y="charges", color="region",
                     title="Charges by Region",
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(height=320, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')


def domain_manufacturing(df, cfg):
    colors = _color_pair(cfg)

    target_col = next((c for c in df.columns
                       if "failure" in c.lower() and "type" not in c.lower()), None)
    failure_type_col = next((c for c in df.columns
                             if "failure" in c.lower() and "type" in c.lower()), None)
    type_col = next((c for c in df.columns
                     if df[c].dtype == object and "type" in c.lower()
                     and "failure" not in c.lower()), None)
    sensor_cols = [c for c in df.select_dtypes(include="number").columns
                   if any(k in c.lower() for k in ["temp", "speed", "torque", "wear", "tool"])]

    if not sensor_cols:
        num_cols, _ = _num_cat(df)
        sensor_cols = [c for c in num_cols if c.lower() not in [
            "udi", "target"]]

    if failure_type_col:
        vc = df[failure_type_col].value_counts().reset_index()
        vc.columns = [failure_type_col, "count"]
        fig = px.bar(vc, x=failure_type_col, y="count",
                     title="Failure Type Distribution",
                     color="count", color_continuous_scale="Greens")
        fig.update_layout(height=300, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')

    if sensor_cols and target_col and target_col in df.columns:
        st.markdown("**Sensor Readings by Failure**")
        for i in range(0, min(len(sensor_cols), 4), 2):
            row_cols = st.columns(2)
            for j, col in enumerate(sensor_cols[i:i+2]):
                fig = px.box(df, x=str(target_col), y=col,
                             color=str(target_col),
                             title=f"{col} by Failure",
                             color_discrete_sequence=colors)
                fig.update_layout(height=280, margin=dict(
                    t=40, b=0), showlegend=False)
                row_cols[j].plotly_chart(fig, width='stretch')

    if type_col and sensor_cols:
        col = sensor_cols[0]
        fig = px.box(df, x=type_col, y=col, color=type_col,
                     title=f"{col} by Machine Type",
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(height=320, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')


def domain_socioeconomic(df, cfg):
    colors = _color_pair(cfg)
    target = cfg.get("target")

    education_order = [
        "Preschool", "1st-4th", "5th-6th", "7th-8th", "9th", "10th", "11th", "12th",
        "HS-grad", "Some-college", "Assoc-voc", "Assoc-acdm", "Bachelors",
        "Prof-school", "Masters", "Doctorate"
    ]

    if "education" in df.columns and target and target in df.columns:
        available_edu = [
            e for e in education_order if e in df["education"].unique()]
        edu_rate = df.groupby("education")[target].apply(
            lambda x: (x == ">50K").mean() * 100
        ).reset_index()
        edu_rate.columns = ["education", "high_income_rate"]
        edu_rate["education"] = pd.Categorical(edu_rate["education"],
                                               categories=available_edu, ordered=True)
        edu_rate = edu_rate.sort_values("education")
        fig = px.bar(edu_rate, x="education", y="high_income_rate",
                     title="% Earning >50K by Education Level",
                     color="high_income_rate", color_continuous_scale="Blues")
        fig.update_xaxes(tickangle=35)
        fig.update_layout(height=360, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')

    for col in ["sex", "race", "occupation"]:
        if col in df.columns and target and target in df.columns:
            grp = df.groupby([col, target]).size().reset_index(name="count")
            fig = px.bar(grp, x=col, y="count", color=str(target), barmode="group",
                         title=f"{col.capitalize()} by Income",
                         color_discrete_sequence=colors)
            fig.update_xaxes(tickangle=20)
            fig.update_layout(height=300, margin=dict(t=40, b=0))
            st.plotly_chart(fig, width='stretch')

    if "hours.per.week" in df.columns:
        fig = px.histogram(df, x="hours.per.week",
                           color=str(
                               target) if target and target in df.columns else None,
                           title="Hours Per Week Distribution",
                           color_discrete_sequence=colors, opacity=0.75)
        fig.add_vline(x=40, line_dash="dash", line_color="gray",
                      annotation_text="Standard 40 hrs")
        fig.update_layout(height=320, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')


def domain_diamonds(df, cfg):
    colors = _color_pair(cfg)
    ordinal = cfg.get("ordinal", {})

    for grade_col, order in ordinal.items():
        if grade_col in df.columns and "price" in df.columns:
            available = [o for o in order if o in df[grade_col].unique()]
            fig = px.box(df, x=grade_col, y="price", color=grade_col,
                         category_orders={grade_col: available},
                         title=f"Price by {grade_col.capitalize()}",
                         color_discrete_sequence=px.colors.sequential.Oranges)
            fig.update_layout(height=320, margin=dict(t=40, b=0))
            st.plotly_chart(fig, width='stretch')

    if "carat" in df.columns and "price" in df.columns:
        fig = px.scatter(df.sample(min(5000, len(df)), random_state=42),
                         x="carat", y="price",
                         color="cut" if "cut" in df.columns else None,
                         title="Carat vs Price",
                         opacity=0.5, color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(height=380, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')


def domain_used_cars(df, cfg):
    colors = _color_pair(cfg)
    price_col = next((c for c in df.columns if "price" in c.lower()), None)
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    num_cols, _ = _num_cat(df)

    if price_col:
        fig = px.histogram(df, x=price_col, nbins=50,
                           title=f"{price_col} Distribution",
                           color_discrete_sequence=[colors[0]])
        fig.update_layout(height=320, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')

    if price_col and cat_cols:
        for col in cat_cols[:2]:
            if df[col].nunique() <= 20:
                fig = px.box(df, x=col, y=price_col,
                             title=f"{price_col} by {col}",
                             color_discrete_sequence=colors)
                fig.update_xaxes(tickangle=20)
                fig.update_layout(height=320, margin=dict(t=40, b=0))
                st.plotly_chart(fig, width='stretch')


def domain_education(df, cfg):
    colors = _color_pair(cfg)
    score_cols = [c for c in df.columns if "score" in c.lower()]
    if not score_cols:
        return

    if "average_score" not in df.columns:
        df = df.copy()
        df["average_score"] = df[score_cols].mean(axis=1)

    # Score distributions
    fig = make_subplots(rows=1, cols=len(score_cols),
                        subplot_titles=score_cols)
    for i, col in enumerate(score_cols):
        fig.add_trace(go.Histogram(x=df[col], name=col, showlegend=False,
                                   marker_color=colors[0]), row=1, col=i + 1)
    fig.update_layout(height=320, margin=dict(t=40, b=0))
    st.plotly_chart(fig, width='stretch')

    if "gender" in df.columns:
        for col in score_cols:
            fig = px.box(df, x="gender", y=col, color="gender",
                         title=f"{col} by Gender",
                         color_discrete_sequence=colors)
            fig.update_layout(height=300, margin=dict(
                t=40, b=0), showlegend=False)
            st.plotly_chart(fig, width='stretch')

    prep_col = next((c for c in df.columns if "prep" in c.lower()), None)
    if prep_col and "average_score" in df.columns:
        fig = px.box(df, x=prep_col, y="average_score", color=prep_col,
                     title="Average Score by Test Preparation",
                     color_discrete_sequence=colors)
        fig.update_layout(height=320, margin=dict(t=40, b=0), showlegend=False)
        st.plotly_chart(fig, width='stretch')

    edu_col = next((c for c in df.columns if "parental" in c.lower()), None)
    if edu_col and "average_score" in df.columns:
        edu_avg = df.groupby(edu_col)["average_score"].mean(
        ).reset_index().sort_values("average_score", ascending=False)
        fig = px.bar(edu_avg, x=edu_col, y="average_score",
                     title="Avg Score by Parental Education",
                     color="average_score", color_continuous_scale="Purples")
        fig.update_xaxes(tickangle=20)
        fig.update_layout(height=320, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')


def domain_telecom(df, cfg):
    colors = _color_pair(cfg)
    target = cfg.get("target")

    if "Contract" in df.columns and "InternetService" in df.columns and target and target in df.columns:
        pivot = df.groupby(["Contract", "InternetService"])[target].apply(
            lambda x: (x == "Yes").mean() * 100
        ).reset_index()
        pivot.columns = ["Contract", "InternetService", "Churn Rate %"]
        matrix = pivot.pivot(
            index="Contract", columns="InternetService", values="Churn Rate %")
        fig = px.imshow(matrix, title="Churn Rate % — Contract × Internet Service",
                        color_continuous_scale="Reds", text_auto=".1f")
        fig.update_layout(height=320, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')
        st.caption("⚠️ Month-to-month + Fiber optic = highest-risk segment")

    for col in ["Contract", "InternetService", "PaymentMethod"]:
        if col in df.columns and target and target in df.columns:
            grp = df.groupby([col, target]).size().reset_index(name="count")
            fig = px.bar(grp, x=col, y="count", color=str(target), barmode="group",
                         title=f"Churn by {col}",
                         color_discrete_sequence=colors)
            fig.update_layout(height=300, margin=dict(t=40, b=0))
            st.plotly_chart(fig, width='stretch')

    if "tenure" in df.columns and target and target in df.columns:
        fig = px.histogram(df, x="tenure", color=str(target), barmode="overlay",
                           title="Tenure by Churn Status",
                           color_discrete_sequence=colors, opacity=0.75)
        fig.update_layout(height=320, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')


def domain_spotify(df, cfg):
    colors = _color_pair(cfg)
    audio_features = [c for c in [
        "danceability", "energy", "loudness", "speechiness",
        "acousticness", "instrumentalness", "liveness", "valence", "tempo"
    ] if c in df.columns]

    if "popularity" in df.columns:
        fig = px.histogram(df, x="popularity", nbins=50,
                           title="Track Popularity Distribution",
                           color_discrete_sequence=[colors[0]])
        fig.add_vline(x=df["popularity"].median(), line_dash="dash", line_color="gray",
                      annotation_text=f"Median {df['popularity'].median():.0f}")
        fig.update_layout(height=320, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')

    if "energy" in df.columns and "danceability" in df.columns:
        sample = df.sample(min(5000, len(df)), random_state=42)
        fig = px.scatter(sample, x="energy", y="danceability",
                         color="valence" if "valence" in df.columns else None,
                         title="Energy vs Danceability (colored by Valence)",
                         opacity=0.5, color_continuous_scale="RdYlGn")
        fig.update_layout(height=360, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')

    if audio_features:
        rows = (len(audio_features) + 2) // 3
        fig = make_subplots(rows=rows, cols=3, subplot_titles=audio_features)
        for i, col in enumerate(audio_features):
            r, c = divmod(i, 3)
            fig.add_trace(go.Histogram(x=df[col], name=col, showlegend=False,
                                       marker_color=colors[0]), row=r + 1, col=c + 1)
        fig.update_layout(height=280 * rows, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')

    genre_col = next((c for c in df.columns if "genre" in c.lower()), None)
    if genre_col:
        top = df[genre_col].value_counts().head(15).reset_index()
        top.columns = [genre_col, "count"]
        fig = px.bar(top, x="count", y=genre_col, orientation="h",
                     title="Top 15 Genres by Track Count",
                     color="count", color_continuous_scale="Greens")
        fig.update_layout(yaxis={"categoryorder": "total ascending"},
                          height=400, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')


def domain_airbnb(df, cfg):
    colors = _color_pair(cfg)

    if "price" in df.columns:
        df = df.copy()
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        p99 = df["price"].quantile(0.99)
        df_p = df[df["price"] < p99]
        fig = px.histogram(df_p, x="price", nbins=80,
                           title="Price Distribution (< 99th percentile)",
                           color_discrete_sequence=[colors[0]])
        fig.add_vline(x=df["price"].median(), line_dash="dash", line_color="gray",
                      annotation_text=f"Median ${df['price'].median():.0f}")
        fig.update_layout(height=320, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')

    borough_col = next(
        (c for c in df.columns if "neighbourhood_group" in c.lower()), None)
    if borough_col:
        c1, c2 = st.columns(2)
        with c1:
            vc = df[borough_col].value_counts().reset_index()
            vc.columns = [borough_col, "count"]
            fig = px.pie(vc, names=borough_col, values="count",
                         title="Listings by Borough",
                         color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_layout(height=320, margin=dict(t=40, b=0))
            st.plotly_chart(fig, width='stretch')
        with c2:
            if "price" in df.columns:
                fig = px.box(df[df["price"] < df["price"].quantile(0.99)],
                             x=borough_col, y="price", color=borough_col,
                             title="Price by Borough",
                             color_discrete_sequence=px.colors.qualitative.Set2)
                fig.update_layout(height=320, margin=dict(
                    t=40, b=0), showlegend=False)
                st.plotly_chart(fig, width='stretch')

    if "room_type" in df.columns and "price" in df.columns:
        fig = px.box(df[df["price"] < df["price"].quantile(0.99)],
                     x="room_type", y="price", color="room_type",
                     title="Price by Room Type",
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(height=320, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')

    if all(c in df.columns for c in ["latitude", "longitude", "price"]):
        sample_map = df[(df["price"] > 0) & (df["price"] < 500)].sample(
            min(3000, len(df)), random_state=42
        )
        fig = px.scatter_mapbox(sample_map, lat="latitude", lon="longitude",
                                color="price", zoom=10,
                                color_continuous_scale="Reds",
                                title="Listing Locations (price colored)",
                                mapbox_style="carto-positron")
        fig.update_layout(height=450, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')


def domain_co2(df, cfg):
    colors = _color_pair(cfg)

    country_col = next((c for c in df.columns if "country" in c.lower()), None)
    year_col = next((c for c in df.columns if "year" in c.lower()), None)
    co2_col = next((c for c in df.columns if "co2" in c.lower()
                   or "emission" in c.lower()), None)
    if co2_col is None:
        num_candidates = [c for c in df.select_dtypes(include="number").columns
                          if c.lower() not in ["year", "code", "id"]]
        co2_col = num_candidates[0] if num_candidates else None

    if year_col and co2_col:
        global_trend = df.groupby(year_col)[co2_col].sum().reset_index()
        global_trend["YoY %"] = global_trend[co2_col].pct_change() * 100
        fig = px.line(global_trend, x=year_col, y=co2_col, markers=True,
                      title="Global Total CO2 Emissions Over Time",
                      color_discrete_sequence=[colors[0]])
        for yr, label, color in [(2015, "Paris Agreement", "red"), (2020, "COVID-19", "orange")]:
            if yr in global_trend[year_col].values:
                fig.add_vline(x=yr, line_dash="dash", line_color=color,
                              annotation_text=label)
        fig.update_layout(height=380, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')

        latest_year = df[year_col].max()
        df_latest = df[df[year_col] == latest_year]

        if country_col:
            top15 = df_latest.nlargest(15, co2_col)[[country_col, co2_col]]
            fig = px.bar(top15, x=co2_col, y=country_col, orientation="h",
                         title=f"Top 15 CO2 Emitters ({latest_year})",
                         color=co2_col, color_continuous_scale="Reds")
            fig.update_layout(yaxis={"categoryorder": "total ascending"},
                              height=400, margin=dict(t=40, b=0))
            st.plotly_chart(fig, width='stretch')

            fig = px.choropleth(df_latest, locations=country_col,
                                locationmode="country names",
                                color=co2_col,
                                title=f"Global CO2 Emissions Map ({latest_year})",
                                color_continuous_scale="YlOrRd")
            fig.update_layout(height=420, margin=dict(t=40, b=0))
            st.plotly_chart(fig, width='stretch')

            top5 = df_latest.nlargest(5, co2_col)[country_col].tolist()
            df_top5 = df[df[country_col].isin(top5)]
            fig = px.line(df_top5, x=year_col, y=co2_col, color=country_col,
                          title="CO2 Trend: Top 5 Emitters Over Time",
                          color_discrete_sequence=px.colors.qualitative.Set1)
            fig.update_layout(height=380, margin=dict(t=40, b=0))
            st.plotly_chart(fig, width='stretch')


def domain_healthcare_generic(df, cfg):
    """Shared rendering for Heart Disease, Pima Diabetes, Breast Cancer, Stroke."""
    colors = _color_pair(cfg)
    target = cfg.get("target")
    thresholds = cfg.get("thresholds", {})

    # Clinical threshold histograms
    for col, (threshold, label) in thresholds.items():
        if col in df.columns:
            color_by = str(target) if target and target in df.columns else None
            fig = px.histogram(df, x=col, color=color_by,
                               barmode="overlay",
                               title=f"{col} Distribution",
                               color_discrete_sequence=colors, opacity=0.75)
            fig.add_vline(x=threshold, line_dash="dash", line_color="red",
                          annotation_text=label)
            fig.update_layout(height=320, margin=dict(t=40, b=0))
            st.plotly_chart(fig, width='stretch')

    # Domain-specific scatter
    if cfg.get("mean_feature_suffix") == "_mean":
        # Breast cancer
        if "radius_mean" in df.columns and "area_mean" in df.columns:
            color_by = str(target) if target and target in df.columns else None
            fig = px.scatter(df, x="radius_mean", y="area_mean", color=color_by,
                             title="Radius Mean vs Area Mean",
                             opacity=0.7, color_discrete_sequence=colors)
            fig.update_layout(height=380, margin=dict(t=40, b=0))
            st.plotly_chart(fig, width='stretch')

    if "Glucose" in df.columns and "BMI" in df.columns:
        # Pima diabetes
        color_by = None
        if target and target in df.columns:
            if df[target].dtype in [int, float]:
                df = df.copy()
                df["_label"] = df[target].map(
                    {1: "Diabetic", 0: "Non-Diabetic"})
                color_by = "_label"
        fig = px.scatter(df, x="Glucose", y="BMI", color=color_by,
                         title="Glucose vs BMI",
                         opacity=0.6, color_discrete_sequence=colors)
        fig.add_vline(x=126, line_dash="dash", line_color="gray",
                      annotation_text="Glucose 126")
        fig.add_hline(y=30, line_dash="dash", line_color="gray",
                      annotation_text="BMI 30")
        fig.update_layout(height=380, margin=dict(t=40, b=0))
        st.plotly_chart(fig, width='stretch')

    # Categorical group charts
    group_cols = [c for c in cfg.get("group_cols", []) if c in df.columns]
    if group_cols and target and target in df.columns:
        for col in group_cols[:3]:
            grp = df.groupby([col, str(target)]).size(
            ).reset_index(name="count")
            fig = px.bar(grp, x=col, y="count", color=str(target),
                         barmode="group", title=f"Outcome by {col}",
                         color_discrete_sequence=colors)
            fig.update_layout(height=300, margin=dict(t=40, b=0))
            st.plotly_chart(fig, width='stretch')

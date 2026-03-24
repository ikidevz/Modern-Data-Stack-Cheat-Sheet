import streamlit as st
import pandas as pd

from components import sidebar
from components.feature_engineering import get_cheatsheet_data
from utils.seo import inject_seo

st.set_page_config(
    page_title="Feature Engineering Cheat Sheet",
    page_icon="⚙️",
    layout="wide",
)
inject_seo('Feature_Engineering')
st.markdown("""
<style>
    .block-container { padding: 1.2rem 2rem 2rem 2rem; max-width: 100%; }
    h1, h2, h3 { font-weight: 600; letter-spacing: -0.3px; }

    .sb-label {
        font-size: 0.68rem; font-weight: 700; letter-spacing: 0.09em;
        color: #6e7681; text-transform: uppercase; padding: 0.5rem 0 0.25rem 0;
    }
    .stat-card {
        background: #161b22; border: 1px solid #30363d; border-radius: 8px;
        padding: 0.65rem 1rem;
    }
    .stat-label { font-size: 0.68rem; color: #6e7681; text-transform: uppercase; letter-spacing: 0.06em; }
    .stat-value { font-size: 1.45rem; font-weight: 700; color: #e6edf3; line-height: 1.25; }

    .sector-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(158px, 1fr));
        gap: 8px;
        margin: 0.6rem 0 1.2rem 0;
    }
    .sector-card {
        background: #161b22; border: 1.5px solid #30363d; border-radius: 10px;
        padding: 0.6rem 0.8rem;
    }
    .sector-card-icon  { font-size: 1.35rem; line-height: 1; }
    .sector-card-name  {
        font-size: 0.77rem; font-weight: 600; color: #c9d1d9;
        margin-top: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    .sector-card-count { font-size: 0.67rem; color: #6e7681; margin-top: 1px; }

    .feature-name { font-size: 0.84rem; font-weight: 600; color: #c9d1d9; padding-top: 5px; }
    .code-block {
        background: #161b22; border: 1px solid #30363d; border-radius: 6px;
        padding: 0.4rem 0.65rem;
        font-family: 'JetBrains Mono','Fira Code','Consolas',monospace;
        font-size: 0.77rem; color: #79c0ff;
        white-space: pre-wrap; word-break: break-all;
    }
    .copy-hint { font-size: 0.63rem; color: #484f58; margin-top: 2px; }

    .cat-banner { border-radius: 0 6px 6px 0; padding: 0.3rem 0.75rem; margin: 1rem 0 0.4rem 0; }
    .cat-banner-text { font-size: 0.76rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; }

    .pill-row { display: flex; flex-wrap: wrap; gap: 5px; margin: 0.4rem 0 1rem 0; }
    .pill {
        background: #21262d; color: #8b949e; border: 1px solid #30363d;
        border-radius: 20px; padding: 2px 10px; font-size: 0.7rem;
    }
    .pill-active { background: #1f6feb22; color: #58a6ff; border-color: #1f6feb; }

    [data-testid="stTextInput"] input {
        background: #161b22 !important; border: 1px solid #30363d !important;
        color: #e6edf3 !important; border-radius: 6px !important; font-size: 0.84rem !important;
    }
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background: #161b22 !important; border: 1px solid #30363d !important;
        color: #e6edf3 !important;
    }
    hr { border-color: #21262d; margin: 0.5rem 0; }
    .empty-state { text-align: center; padding: 3rem; color: #484f58; }
</style>
""", unsafe_allow_html=True)
sidebar()


@st.cache_data
def load_data():
    return {k: pd.DataFrame(v) for k, v in get_cheatsheet_data().items()}


SECTOR_META = {
    "Finance":            ("#3fb950", "📈"),
    "Marketing":          ("#f78166", "📣"),
    "Healthcare":         ("#58a6ff", "🏥"),
    "Retail":             ("#d2a8ff", "🛍️"),
    "Manufacturing":      ("#ffa657", "🏭"),
    "E-Commerce":         ("#79c0ff", "🛒"),
    "Logistics":          ("#56d364", "🚚"),
    "Supply Chain":       ("#e3b341", "🔗"),
    "Telecommunications": ("#bc8cff", "📡"),
    "Energy & Utilities": ("#ff7b72", "⚡"),
    "Agriculture":        ("#7ee787", "🌾"),
    "Transportation":     ("#a5d6ff", "🚆"),
}

sector_dfs = load_data()
sector_names = list(SECTOR_META.keys())
total_all = sum(len(v) for v in sector_dfs.values())

if "selected_sector" not in st.session_state:
    st.session_state.selected_sector = "Finance"


st.title("⚗️ Feature Engineering Cheat Sheet")
st.caption(
    "This page provides a collection of practical feature engineering snippets using Pandas, tailored for 12 key industry sectors. Each snippet is designed to help data professionals quickly transform raw data into meaningful features that can enhance model performance and insights.")

st.markdown(f"""
<div class="hero">
    <span class="hero-badge">🗂 12 Sectors</span>
    <span class="hero-badge">📐 {total_all:,} Features</span>
    <span class="hero-badge">🐼 pandas + numpy</span>
    <span class="hero-badge">🔍 Searchable</span>
</div>
""", unsafe_allow_html=True)


col_sec, col_srch, col_cat = st.columns([2, 2, 2])

with col_sec:
    st.markdown('<p class="section-label">Sector</p>', unsafe_allow_html=True)
    chosen_sector = st.selectbox(
        "sector",
        options=sector_names,
        index=sector_names.index(st.session_state.selected_sector),
        format_func=lambda s: f"{SECTOR_META[s][1]}  {s}  ({len(sector_dfs[s])})",
        label_visibility="collapsed",
        key="sector_select",
    )
    if chosen_sector != st.session_state.selected_sector:
        st.session_state.selected_sector = chosen_sector
        st.rerun()

with col_srch:
    st.markdown('<p class="section-label">Search</p>', unsafe_allow_html=True)
    search = st.text_input(
        "search",
        placeholder="feature name, code, category…",
        label_visibility="collapsed",
        key="search_box",
    )

# Resolve active sector before rendering category filter
selected_sector = st.session_state.selected_sector
accent_color, sector_icon = SECTOR_META[selected_sector]
df_all = sector_dfs[selected_sector]

with col_cat:
    st.markdown('<p class="section-label">Category</p>',
                unsafe_allow_html=True)
    cats = ["All"] + sorted(df_all["category"].unique().tolist())
    selected_cat = st.selectbox(
        "category",
        cats,
        label_visibility="collapsed",
        key="cat_select",
    )


st.markdown('<hr class="divider-line">', unsafe_allow_html=True)
grid_html = '<div class="sector-grid">'
for s in sector_names:
    color, icon = SECTOR_META[s]
    cnt = len(sector_dfs[s])
    is_active = s == selected_sector
    b_sty = f"border-color:{color};" if is_active else ""
    bg_sty = "background:#1c2128;" if is_active else ""
    n_sty = f"color:{color};" if is_active else ""
    grid_html += (
        f'<div class="sector-card" style="{b_sty}{bg_sty}">'
        f'<div class="sector-card-icon">{icon}</div>'
        f'<div class="sector-card-name" style="{n_sty}">{s}</div>'
        f'<div class="sector-card-count">{cnt} features</div>'
        f'</div>'
    )
grid_html += "</div>"
st.markdown(grid_html, unsafe_allow_html=True)

st.markdown('<hr class="divider-line">', unsafe_allow_html=True)

st.markdown(
    f'<h2 style="margin:0 0 0.05rem 0;">'
    f'{sector_icon}&nbsp;<span style="color:{accent_color};">{selected_sector}</span>'
    f'&nbsp;Feature Engineering</h2>'
    f'<p style="color:#6e7681;font-size:0.8rem;margin:0 0 1rem 0;">',
    unsafe_allow_html=True,
)


df = df_all.copy()
if selected_cat != "All":
    df = df[df["category"] == selected_cat]
if search.strip():
    q = search.strip().lower()
    mask = (
        df["feature"].str.lower().str.contains(q, regex=False) |
        df["code"].str.lower().str.contains(q, regex=False) |
        df["category"].str.lower().str.contains(q, regex=False)
    )
    df = df[mask]

total_filtered = len(df)

s1, s2, s3, s4, s5 = st.columns(5)
with s1:
    st.markdown(
        f'<div class="stat-card"><div class="stat-label">Sector Total</div>'
        f'<div class="stat-value" style="color:{accent_color};">{len(df_all)}</div></div>',
        unsafe_allow_html=True,
    )
with s2:
    st.markdown(
        f'<div class="stat-card"><div class="stat-label">Showing</div>'
        f'<div class="stat-value">{total_filtered}</div></div>',
        unsafe_allow_html=True,
    )
with s3:
    st.markdown(
        f'<div class="stat-card"><div class="stat-label">Categories</div>'
        f'<div class="stat-value">{df_all["category"].nunique()}</div></div>',
        unsafe_allow_html=True,
    )
with s4:
    st.markdown(
        f'<div class="stat-card"><div class="stat-label">All Sectors</div>'
        f'<div class="stat-value">{total_all:,}</div></div>',
        unsafe_allow_html=True,
    )
with s5:
    st.markdown(
        f'<div class="stat-card"><div class="stat-label">Active Filter</div>'
        f'<div class="stat-value" style="font-size:0.88rem;padding-top:6px;">{selected_cat}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown('<hr class="divider-line">', unsafe_allow_html=True)

pills_html = '<div class="pill-row">'
for c in sorted(df_all["category"].unique()):
    act = "pill-active" if c == selected_cat else ""
    cat_cnt = len(df_all[df_all["category"] == c])
    pills_html += f'<span class="pill {act}">{c} <b>({cat_cnt})</b></span>'
pills_html += "</div>"
st.markdown(pills_html, unsafe_allow_html=True)

if total_filtered == 0:
    st.markdown("""
    <div class="empty-state">
        <div style="font-size:2.5rem;">🔍</div>
        <b style="color:#c9d1d9;">No features found</b><br>
        <span style="font-size:0.84rem;color:#6e7681;">
            Try a different search term, sector, or category
        </span>
    </div>""", unsafe_allow_html=True)
    st.stop()

st.markdown(
    f'<p style="color:#484f58;font-size:0.72rem;margin-bottom:0.3rem;">'
    f'{total_filtered} features</p>',
    unsafe_allow_html=True,
)


current_cat = None
for _, row in df.iterrows():
    if row["category"] != current_cat:
        current_cat = row["category"]
        st.markdown(
            f'<div class="cat-banner" style="background:{accent_color}16;'
            f'border-left:3px solid {accent_color};">'
            f'<span class="cat-banner-text" style="color:{accent_color};">'
            f'{current_cat}</span></div>',
            unsafe_allow_html=True,
        )
    left, right = st.columns([1, 3])
    with left:
        st.markdown(
            f'<div class="feature-name">{row["feature"]}</div>',
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            f'<div class="code-block">{row["code"]}</div>'
            f'<div class="copy-hint">Click to select · Ctrl+C to copy</div>',
            unsafe_allow_html=True,
        )
    st.markdown('<hr style="margin:0.27rem 0;border-color:#21262d;">',
                unsafe_allow_html=True)

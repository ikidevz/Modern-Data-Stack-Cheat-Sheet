import streamlit as st
import pandas as pd
from pathlib import Path
import re

from components import sidebar

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"

st.set_page_config(
    page_title="Design Patterns Docs",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)
DOCS = {
    "🟢 Creational": {
        "file": DOCS_DIR / "creational_design_patterns.md",
        "pill": "pill-creational",
        "accent": "#10b981",
        "patterns": [
            ("1", "Singleton",
             "One shared instance — config, DB connection, logger."),
            ("2", "Factory Method",
             "Let subclasses decide which object to instantiate."),
            ("3", "Abstract Factory",
             "Create families of related objects without concrete classes."),
            ("4", "Builder",          "Construct complex objects step-by-step fluently."),
            ("5", "Prototype",
             "Clone existing objects instead of building from scratch."),
        ]
    },
    "🔵 Structural": {
        "file": DOCS_DIR / "structural_design_patterns.md",
        "pill": "pill-structural",
        "accent": "#3b82f6",
        "patterns": [
            ("1", "Adapter",   "Make incompatible interfaces work together."),
            ("2", "Bridge",    "Decouple abstraction from implementation independently."),
            ("3", "Composite", "Treat individual objects and groups uniformly."),
            ("4", "Decorator", "Add behaviour to objects dynamically without subclassing."),
            ("5", "Facade",    "Simplify a complex subsystem behind one clean interface."),
            ("6", "Flyweight", "Share fine-grained objects for memory efficiency."),
            ("7", "Proxy",     "Control access to another object via a surrogate."),
        ]
    },
    "🟣 Behavioural": {
        "file": DOCS_DIR / "behavioural_design_patterns.md",
        "pill": "pill-behavioural",
        "accent": "#8b5cf6",
        "patterns": [
            ("1",  "Chain of Responsibility",
             "Pass requests along a chain of handlers."),
            ("2",  "Command",
             "Encapsulate requests as objects — queue, undo, log."),
            ("3",  "Interpreter",
             "Define a grammar and interpreter for a mini DSL."),
            ("4",  "Iterator",
             "Traverse a collection without exposing its structure."),
            ("5",  "Mediator",
             "Centralise communication between components."),
            ("6",  "Memento",
             "Capture and restore object state — checkpoints."),
            ("7",  "Observer",
             "Notify many dependents when one object changes."),
            ("8",  "State",
             "Alter behaviour when internal state changes."),
        ]
    },
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Fraunces:ital,wght@0,400;0,700;0,900;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

.main .block-container {
    padding: 2.5rem 3rem 5rem 3rem;
    max-width: 960px;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    border-right: none;
    width: 290px !important;
}
section[data-testid="stSidebar"] * { color: #d6d3d1 !important; }

.sidebar-logo {
    padding: 24px 20px 16px;
    border-bottom: 1px solid #292524;
    margin-bottom: 20px;
}
.sidebar-logo h1 {
    font-family: 'Fraunces', serif !important;
    font-size: 1.4rem;
    font-weight: 900;
    color: #fafaf9 !important;
    margin: 0;
    line-height: 1.2;
}
.sidebar-logo .sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: #57534e !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    display: block;
    margin-top: 5px;
}
.nav-section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #57534e !important;
    padding: 14px 20px 5px;
    display: block;
}
.nav-item {
    display: block;
    padding: 7px 20px;
    font-size: 0.86rem;
    color: #a8a29e !important;
    border-left: 2px solid transparent;
}

/* ── Category pills ── */
.cat-pill {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 4px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.pill-creational  { background: #d1fae5; color: #065f46; }
.pill-structural  { background: #dbeafe; color: #1e3a5f; }
.pill-behavioural { background: #ede9fe; color: #4c1d95; }

/* ── Page titles ── */
.doc-title {
    font-family: 'Fraunces', serif !important;
    font-size: 2.8rem;
    font-weight: 900;
    line-height: 1.1;
    color: #1c1917;
    margin-bottom: 4px;
}
.doc-subtitle {
    font-size: 0.9rem;
    color: #78716c;
    margin-bottom: 32px;
}

/* ── Pattern cards ── */
.pattern-card {
    border: 1px solid #e7e5e4;
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 10px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.pattern-card .pnum {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: #a8a29e;
    display: block;
    margin-bottom: 4px;
}
.pattern-card h4 {
    font-family: 'Fraunces', serif;
    font-size: 1.1rem;
    font-weight: 700;
    margin: 0 0 6px;
}
.pattern-card p {
    font-size: 0.83rem;
    margin: 0;
    line-height: 1.5;
}

/* ── Intent / use-case blocks ── */
.intent-block {
    background: transparent;
    border: 1px solid #fde68a;
    border-left: 4px solid #f59e0b;
    border-radius: 0 8px 8px 0;
    padding: 13px 18px;
    margin: 14px 0 10px;
    font-size: 0.875rem;
    color:#fde68a;
    line-height: 1.6;
}
.intent-block strong { color: #fde68a; }
.usecase-block {
    background: transparent;
    border: 1px solid #bae6fd;
    border-left: 4px solid #0284c7;
    border-radius: 0 8px 8px 0;
    padding: 13px 18px;
    margin: 0 0 22px;
    font-size: 0.875rem;
    color: #bae6fd;
    line-height: 1.6;
}

/* ── Example label ── */
.example-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #78716c;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 22px 0 8px;
    padding-bottom: 5px;
    border-bottom: 1px solid #e7e5e4;
}

/* ── Stats chips ── */
.stat-row { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 28px; }
.stat-chip {
    background: #fff;
    border: 1px solid #e7e5e4;
    border-radius: 8px;
    padding: 10px 16px;
    min-width: 90px;
    text-align: center;
}
.stat-chip .val {
    font-family: 'Fraunces', serif;
    font-size: 1.5rem;
    font-weight: 900;
    color: #1c1917;
    line-height: 1;
}
.stat-chip .lbl {
    font-size: 0.66rem;
    color: #a8a29e;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-family: 'IBM Plex Mono', monospace;
}

/* ── TOC ── */
.toc-box {
    background: transparent;
    border: 1px solid #e7e5e4;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 28px;
}
.toc-box h4 {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: white;
    margin: 0 0 10px;
}
.toc-row {
    font-size: 0.85rem;
    color: white;
    padding: 3px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.toc-num { font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; color: #a8a29e; min-width: 18px; }
.toc-ex  { font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; color: #a8a29e; }

/* ── Divider ── */
.doc-divider { border: none; border-top: 1px solid #e7e5e4; margin: 38px 0; }

 /* ── Category definition block ── */
.definition-block {
    background: transparent;
    border: 1px solid #e7e5e4;
    border-radius: 12px;
    padding: 22px 26px;
    margin: 0 0 28px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    position: relative;
    overflow: hidden;
}
.definition-block::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px;
    height: 100%;
    background: var(--def-accent, #f59e0b);
    border-radius: 12px 0 0 12px;
}
.definition-block .def-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: white;
    margin-bottom: 8px;
    display: block;
}
.definition-block .def-text {
    font-size: 0.95rem;
    color: white;
    line-height: 1.75;
    font-weight: 400;
    margin: 0;
}   

/* ── Search ── */
.stTextInput input {
    background: #292524 !important;
    border: 1px solid #3c3734 !important;
    border-radius: 8px !important;
    color: #fafaf9 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.82rem !important;
}
.stTextInput input::placeholder { color: #57534e !important; }
.stTextInput input:focus { border-color: #f59e0b !important; box-shadow: none !important; }
.stTextInput > label { display: none !important; }
</style>
""", unsafe_allow_html=True)


def load_md(filepath):
    path = Path(filepath)
    if path.exists():
        return path.read_text(encoding="utf-8")
    return f"""# File not found: `{filepath}`"""


def parse_patterns(content):
    """Parse ## N. PatternName sections from markdown. Returns list of dicts."""
    sections = []
    parts = re.split(r'\n(?=## \d+\.)', content)
    for part in parts:
        part = part.strip()
        if not part or not re.match(r'^## \d+', part):
            continue
        m = re.match(r'^## (\d+)\. (.+)', part)
        if not m:
            continue
        intent_m = re.search(r'\*\*Intent:\*\*\s*(.+?)(?:\n|$)', part)
        usecase_m = re.search(r'\*\*Use Case[^:]*:\*\*\s*(.+?)(?:\n|$)', part)
        codes = re.findall(r'```python(.*?)```', part, re.DOTALL)
        ex_names = re.findall(r'### (Example \d+[^\n]*)', part)
        sections.append({
            "number":      m.group(1),
            "title":       m.group(2).strip(),
            "intent":      intent_m.group(1).strip() if intent_m else "",
            "use_case":    usecase_m.group(1).strip() if usecase_m else "",
            "code_blocks": codes,
            "ex_names":    ex_names,
            "n_examples":  len(codes),
        })
    return sections


def render_pattern(p):
    """Render one pattern's docs: intent, use case, code tabs."""
    st.markdown(
        f"<span style='font-family:IBM Plex Mono,monospace;font-size:0.65rem;color:#a8a29e;'>"
        f"Pattern #{p['number']}</span>",
        unsafe_allow_html=True
    )
    st.markdown(f"## {p['title']}")

    if p["intent"]:
        st.markdown(
            f"<div class='intent-block'><strong>Intent —</strong> {p['intent']}</div>",
            unsafe_allow_html=True
        )
    if p["use_case"]:
        st.markdown(
            f"<div class='usecase-block'><strong>Data Use Case —</strong> {p['use_case']}</div>",
            unsafe_allow_html=True
        )

    codes = p["code_blocks"]
    names = p["ex_names"]
    n = len(codes)

    if n == 0:
        st.info("No code examples found in this section.")
    elif n == 1:
        st.markdown("<div class='example-label'>Example 1</div>",
                    unsafe_allow_html=True)
        st.code(codes[0].strip(), language="python")
    else:
        # Build tab labels from parsed ### Example headings, fall back to generic
        labels = (names[:n] if len(names) >= n else [
                  f"Example {i+1}" for i in range(n)])
        labels = [lbl.replace("### ", "").strip()[:55] for lbl in labels]
        tabs = st.tabs(labels)
        for tab, code in zip(tabs, codes):
            with tab:
                st.code(code.strip(), language="python")

    st.markdown("<hr class='doc-divider'>", unsafe_allow_html=True)


def parse_category_definition(content):
    """
    Extract the category-level definition paragraph from the markdown file.
    It sits between the blockquote subtitle (> ...) and the first ## heading.
    """
    # Remove the # title line and > blockquote line at the top
    lines = content.split("\n")
    body_lines = []
    skip_prefixes = ("#", ">", "---")
    started = False
    for line in lines:
        stripped = line.strip()
        # Start collecting after the blockquote
        if stripped.startswith(">"):
            started = True
            continue
        if not started:
            continue
        # Stop at the first ## pattern heading
        if stripped.startswith("## "):
            break
        # Skip horizontal rules
        if stripped == "---":
            continue
        body_lines.append(line)

    definition = "\n".join(body_lines).strip()
    return definition


def search_all(query, all_sections):
    q = query.lower()
    results = []
    for cat, sections in all_sections.items():
        for p in sections:
            blob = f"{p['title']} {p['intent']} {p['use_case']} {''.join(p['code_blocks'])}".lower(
            )
            if q in blob:
                results.append((cat, p))
    return results


@st.cache_data
def load_all():
    content = {cat: load_md(meta["file"]) for cat, meta in DOCS.items()}
    sections = {cat: parse_patterns(content[cat]) for cat in DOCS}
    definitions = {cat: parse_category_definition(
        content[cat]) for cat in DOCS}
    return content, sections, definitions


_, all_sections, all_definitions = load_all()
sidebar()
with st.sidebar:
    # Search input
    search_query = st.text_input(
        "search", placeholder="🔍  Search patterns…", label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Page navigator
    page_options = ["📖 Overview"] + list(DOCS.keys())
    selected_page = st.selectbox(
        "Go to", page_options, label_visibility="visible")

    # Pattern index (only shown when not searching)
    if not search_query:
        for cat, meta in DOCS.items():
            label = cat.split(" ", 1)[1]
            st.markdown(
                f"<span class='nav-section-label'>{label}</span>",
                unsafe_allow_html=True
            )
            for num, name, _ in meta["patterns"]:
                st.markdown(
                    f"<span class='nav-item'>{num}. {name}</span>",
                    unsafe_allow_html=True
                )


if search_query:
    results = search_all(search_query, all_sections)
    st.markdown("<h1 class='doc-title'>Search</h1>", unsafe_allow_html=True)
    st.markdown(
        f"<p class='doc-subtitle'>Results for <strong>\"{search_query}\"</strong></p>",
        unsafe_allow_html=True
    )
    if not results:
        st.markdown("""
        <div style='text-align:center;padding:60px 0;'>
            <div style='font-size:2.5rem;'>🔍</div>
            <div style='font-family:Fraunces,serif;font-size:1.4rem;color:#57534e;margin-top:12px;'>No results found</div>
            <div style='font-size:0.85rem;color:#a8a29e;margin-top:6px;'>Try a pattern name, keyword, or concept</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(
            f"<p style='color:#78716c;font-size:0.85rem;margin-bottom:20px;'>"
            f"Found <strong>{len(results)}</strong> match(es)</p>",
            unsafe_allow_html=True
        )
        for cat, pattern in results:
            pill = DOCS[cat]["pill"]
            cat_label = cat.split(" ", 1)[1]
            st.markdown(
                f"<span class='cat-pill {pill}'>{cat_label}</span>", unsafe_allow_html=True)
            render_pattern(pattern)

elif selected_page == "📖 Overview":
    st.markdown("<h1 class='doc-title'>Design Patterns</h1>",
                unsafe_allow_html=True)
    st.markdown(
        "<p class='doc-subtitle'>A comprehensive Python reference for Data Engineering, "
        "Analytics Engineering, Data Science & Analytics</p>",
        unsafe_allow_html=True
    )

    total_ex = sum(p["n_examples"]
                   for secs in all_sections.values() for p in secs)
    st.markdown(f"""
    <div class='stat-row'>
        <div class='stat-chip'><div class='val'>20</div><div class='lbl'>Patterns</div></div>
        <div class='stat-chip'><div class='val'>3</div><div class='lbl'>Categories</div></div>
        <div class='stat-chip'><div class='val'>{total_ex}</div><div class='lbl'>Examples</div></div>
        <div class='stat-chip'><div class='val'>Python</div><div class='lbl'>Language</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='doc-divider'>", unsafe_allow_html=True)

    # Category overview with pattern cards
    for cat, meta in DOCS.items():
        cat_label = cat.split(" ", 1)[1]
        pill = meta["pill"]

        st.markdown(
            f"<span class='cat-pill {pill}'>{cat_label} Patterns</span>", unsafe_allow_html=True)

        cols = st.columns(2)
        for i, (num, name, desc) in enumerate(meta["patterns"]):
            with cols[i % 2]:
                st.markdown(f"""
                <div class='pattern-card'>
                    <span class='pnum'>#{num}</span>
                    <h4>{name}</h4>
                    <p>{desc}</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<hr class='doc-divider'>", unsafe_allow_html=True)

else:
    cat = selected_page
    meta = DOCS[cat]
    label = cat.split(" ", 1)[1]
    pill = meta["pill"]
    sections = all_sections[cat]

    st.markdown(
        f"<span class='cat-pill {pill}'>{label}</span>", unsafe_allow_html=True)
    st.markdown(
        f"<h1 class='doc-title'>{label} Patterns</h1>", unsafe_allow_html=True)
    st.markdown(
        f"<p class='doc-subtitle'>{len(meta['patterns'])} patterns · Python · Data & Analytics</p>",
        unsafe_allow_html=True
    )

    total_ex = sum(p["n_examples"] for p in sections)
    st.markdown(f"""
    <div class='stat-row'>
        <div class='stat-chip'><div class='val'>{len(meta['patterns'])}</div><div class='lbl'>Patterns</div></div>
        <div class='stat-chip'><div class='val'>{total_ex}</div><div class='lbl'>Examples</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Category definition
    definition = all_definitions.get(cat, "")
    accent_map = {
        "🟢 Creational":  "#10b981",
        "🔵 Structural":  "#3b82f6",
        "🟣 Behavioural": "#8b5cf6",
    }
    accent_color = accent_map.get(cat, "#f59e0b")
    if definition:
        st.markdown(
            f"""<div class='definition-block' style='--def-accent:{accent_color};'>
            <span class='def-label'>What are {label} Design Patterns?</span>
            <p class='def-text'>{definition}</p>
            </div>""",
            unsafe_allow_html=True
        )

    # Table of contents
    if sections:
        toc_rows = "".join([
            f"<div class='toc-row'>"
            f"<span class='toc-num'>{p['number']}.</span>"
            f"<span>{p['title']}</span>"
            f"<span class='toc-ex'>({p['n_examples']} examples)</span>"
            f"</div>"
            for p in sections
        ])
        st.markdown(f"""
        <div class='toc-box'>
            <h4>Contents</h4>
            {toc_rows}
        </div>
        """, unsafe_allow_html=True)

    # Jump-to selector
    pattern_names = ["All patterns"] + [p["title"] for p in sections]
    selected_filter = st.selectbox("Jump to pattern", pattern_names)
    st.markdown("<hr class='doc-divider'>", unsafe_allow_html=True)

    to_show = (
        sections if selected_filter == "All patterns"
        else [p for p in sections if p["title"] == selected_filter]
    )

    if not to_show:
        st.info(
            "No patterns to display. Check that your markdown files are in the `docs/` folder.")
    else:
        for pattern in to_show:
            render_pattern(pattern)

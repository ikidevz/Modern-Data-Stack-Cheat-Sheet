import streamlit as st


def sidebar():
    with st.sidebar:
        st.title("📊🧱⚙️  The Modern Data Stack Cheat Sheet")

        st.markdown("""
        <style>
            .block-container { padding: 3.75rem 2rem 2rem 2rem; max-width: 100%; }
        </style>
        """, unsafe_allow_html=True)

        st.sidebar.caption(
            "Made by [Franz Monzales](https://github.com/ikigamisama)")


def init_layout_state(left_defaults, right_defaults):
    if "layout_left_column" not in st.session_state:
        st.session_state["layout_left_column"] = left_defaults.copy()

    if "layout_right_column" not in st.session_state:
        st.session_state["layout_right_column"] = right_defaults.copy()


def reset_layout(left_defaults, right_defaults):
    st.session_state.layout_left_column = left_defaults.copy()
    st.session_state.layout_right_column = right_defaults.copy()

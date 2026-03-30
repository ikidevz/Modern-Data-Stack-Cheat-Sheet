import streamlit as st


def sidebar():
    with st.sidebar:

        st.markdown('<img src="https://tdhghaslnufgtzjybhhf.supabase.co/storage/v1/object/public/resume/moden_data_stack_cheat_sheet_main_logo.png" alt="main-banner" style="width:100%; object-fit: cover; height: 90px;"/>', unsafe_allow_html=True)

        st.markdown("""
        <style>
            .block-container { padding: 3.75rem 2rem 2rem 2rem; max-width: 100%; }
            [data-testid="stSidebar"] {
                background-color: #161b22 !important;
                border-right: 1px solid #30363d;
            }
            [data-testid="stSidebar"] * {
                color: #e6edf3 !important;
            }

        </style>
        """, unsafe_allow_html=True)

        st.sidebar.caption(
            "Made by [Franz Monzales](https://ikidevs.vercel.app)")


def init_layout_state(left_defaults, right_defaults):
    if "layout_left_column" not in st.session_state:
        st.session_state["layout_left_column"] = left_defaults.copy()

    if "layout_right_column" not in st.session_state:
        st.session_state["layout_right_column"] = right_defaults.copy()


def reset_layout(left_defaults, right_defaults):
    st.session_state.layout_left_column = left_defaults.copy()
    st.session_state.layout_right_column = right_defaults.copy()

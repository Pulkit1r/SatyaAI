"""
Theme management
"""
import streamlit as st


def apply_theme(theme: str = "dark"):
    """Apply theme styling"""
    if theme == "light":
        st.markdown("""
        <style>
            .stApp {
                background-color: #ffffff;
                color: #1f2937;
            }
            h1, h2, h3 { color: #1e40af !important; }
            .stMetric {
                background-color: #f3f4f6;
                border: 1px solid #e5e7eb;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            .stApp {
                background-color: #0e1117;
                color: #fafafa;
            }
            h1, h2, h3 { color: #4fd1c5 !important; }
            .stMetric {
                background: #111827;
                box-shadow: 0px 0px 10px rgba(79,209,197,0.2);
            }
        </style>
        """, unsafe_allow_html=True)


def render_theme_selector():
    """Render theme selector"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎨 Theme")
    
    theme = st.sidebar.selectbox(
        "Select Theme",
        ["Dark", "Light"],
        key="theme_selector",
        label_visibility="collapsed"
    )
    
    st.session_state.theme = theme.lower()
    return theme.lower()
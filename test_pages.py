"""
Test if pages render correctly
"""
import streamlit as st
import sys
import os

st.set_page_config(page_title="Page Test", layout="wide")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

st.title("🧪 Page Rendering Test")

from core.narratives.narrative_explorer import get_all_narratives
narratives = get_all_narratives()

st.write(f"Loaded {len(narratives)} narratives")

tab1, tab2 = st.tabs(["Analytics", "Exports"])

with tab1:
    st.header("Testing Analytics Page")
    try:
        from ui.modules.analytics_page import render_analytics_page
        render_analytics_page(narratives)
        st.success("✅ Analytics page rendered")
    except Exception as e:
        st.error(f"❌ Error: {e}")
        import traceback
        st.code(traceback.format_exc())

with tab2:
    st.header("Testing Exports Page")
    try:
        from ui.modules.exports_page import render_export_page
        render_export_page(narratives)
        st.success("✅ Exports page rendered")
    except Exception as e:
        st.error(f"❌ Error: {e}")
        import traceback
        st.code(traceback.format_exc())
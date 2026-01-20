"""
Export & Reports UI
Robust, capability-based export handling (hackathon-safe)
"""
import streamlit as st
import os
from datetime import datetime

# ----------------------------
# Capability-based imports
# ----------------------------

EXPORT_JSON = False
EXPORT_CSV = False
EXPORT_PDF = False

# JSON (REQUIRED – you already have this)
try:
    from core.exports.json_exporter import (
        export_all_narratives_json,
        export_narrative_history_json
    )
    EXPORT_JSON = True
except ImportError as e:
    JSON_IMPORT_ERROR = str(e)

# CSV (OPTIONAL)
try:
    from core.exports.csv_exporter import (
        export_all_narratives_csv,
        export_narrative_history_csv
    )
    EXPORT_CSV = True
except ImportError:
    pass

# PDF (OPTIONAL)
try:
    from core.exports.pdf_exporter import export_narrative_report_pdf
    from core.narratives.narrative_intelligence import compute_narrative_stats
    EXPORT_PDF = True
except ImportError:
    EXPORT_PDF = False
    compute_narrative_stats = None


# ----------------------------
# Main render function
# ----------------------------

def render_export_page(narratives: dict):
    st.title("📤 Export & Reports")
    st.write("Export narrative data for analysis, reporting, and archival.")

    # ----------------------------
    # System status
    # ----------------------------
    st.markdown("---")
    st.subheader("📊 Export System Status")

    total_narratives = len(narratives) if narratives else 0
    total_memories = sum(len(v) for v in narratives.values()) if narratives else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🧠 Narratives", total_narratives)
    c2.metric("📚 Memories", total_memories)
    c3.metric("📄 JSON Export", "✅ Ready" if EXPORT_JSON else "❌ Missing")
    c4.metric("📑 PDF Support", "✅ Ready" if EXPORT_PDF else "⚠️ Optional")

    if not EXPORT_JSON:
        st.error("❌ JSON export module not available.")
        st.code(JSON_IMPORT_ERROR)
        return

    # ----------------------------
    # Empty state
    # ----------------------------
    if not narratives:
        st.info("📦 No narratives available yet. Add data to enable exports.")
        return

    # ----------------------------
    # Bulk export
    # ----------------------------
    st.markdown("---")
    st.header("📦 Bulk Export (All Narratives)")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📄 Export All (JSON)", use_container_width=True):
            try:
                with st.spinner("Generating JSON export..."):
                    path = export_all_narratives_json(narratives)

                st.success("✅ JSON export generated")
                _download_file(path, "application/json")
            except Exception as e:
                st.error(f"Export failed: {e}")

    with col2:
        if EXPORT_CSV:
            if st.button("📊 Export All (CSV)", use_container_width=True):
                try:
                    with st.spinner("Generating CSV export..."):
                        path = export_all_narratives_csv(narratives)

                    st.success("✅ CSV export generated")
                    _download_file(path, "text/csv")
                except Exception as e:
                    st.error(f"Export failed: {e}")
        else:
            st.warning("CSV exporter not installed")

    with col3:
        st.info("""
        **Formats**
        • JSON → Full structured data  
        • CSV → Spreadsheet analysis  
        • PDF → Reports (optional)
        """)

    # ----------------------------
    # Individual narrative export
    # ----------------------------
    st.markdown("---")
    st.header("🎯 Individual Narrative Export")

    narrative_ids = sorted(
        narratives.keys(),
        key=lambda k: len(narratives[k]),
        reverse=True
    )

    selected = st.selectbox(
        "Select Narrative",
        narrative_ids,
        format_func=lambda k: f"{k} ({len(narratives[k])} memories)"
    )

    memories = narratives[selected]

    # Overview
    st.subheader("📊 Narrative Overview")

    years = [m.get("year") for m in memories if isinstance(m.get("year"), int)]
    sources = sorted(set(m.get("source") for m in memories if m.get("source")))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Memories", len(memories))
    c2.metric("First Seen", min(years) if years else "—")
    c3.metric("Last Seen", max(years) if years else "—")
    c4.metric("Sources", len(sources))

    st.write(f"**Platforms:** {', '.join(sources)}")

    with st.expander("👀 Preview Memories (first 5)"):
        for m in memories[:5]:
            st.json(m)

    # ----------------------------
    # Individual export actions
    # ----------------------------
    st.subheader("📤 Export Options")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📄 Export JSON", use_container_width=True):
            try:
                path = export_narrative_history_json(selected, memories)
                st.success("JSON exported")
                _download_file(path, "application/json")
            except Exception as e:
                st.error(f"Export failed: {e}")

    with col2:
        if EXPORT_CSV:
            if st.button("📊 Export CSV", use_container_width=True):
                try:
                    path = export_narrative_history_csv(selected, memories)
                    st.success("CSV exported")
                    _download_file(path, "text/csv")
                except Exception as e:
                    st.error(f"Export failed: {e}")
        else:
            st.warning("CSV exporter not installed")

    with col3:
        if EXPORT_PDF and compute_narrative_stats:
            if st.button("📑 Generate PDF Report", use_container_width=True):
                try:
                    stats = compute_narrative_stats(memories)
                    path = export_narrative_report_pdf(selected, memories, stats)
                    st.success("PDF generated")
                    _download_file(path, "application/pdf")
                except Exception as e:
                    st.error(f"PDF generation failed: {e}")
        else:
            st.warning("PDF support not available")

    st.markdown("---")
    st.caption("📁 All exports are saved in the `exports/` directory.")


# ----------------------------
# Helper: download button
# ----------------------------

def _download_file(path: str, mime: str):
    size_kb = os.path.getsize(path) / 1024
    st.caption(f"📁 File size: {size_kb:.1f} KB")

    with open(path, "rb") as f:
        st.download_button(
            "⬇️ Download file",
            f,
            file_name=os.path.basename(path),
            mime=mime,
            use_container_width=True
        )

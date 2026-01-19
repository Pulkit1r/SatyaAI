"""
Enhanced Export functionality UI with always-visible content
"""
import streamlit as st
import json
from datetime import datetime

# Try importing export modules with fallback
EXPORT_AVAILABLE = False
IMPORT_ERROR = None

try:
    from core.exports.json_exporter import (
        export_all_narratives_json,
        export_narrative_history_json
    )
    from core.exports.csv_exporter import (
        export_all_narratives_csv,
        export_narrative_history_csv
    )
    EXPORT_AVAILABLE = True
except ImportError as e:
    IMPORT_ERROR = str(e)

try:
    from core.exports.pdf_exporter import REPORTLAB_AVAILABLE, export_narrative_report_pdf
except ImportError:
    REPORTLAB_AVAILABLE = False

try:
    from core.narratives.narrative_intelligence import compute_narrative_stats
except ImportError:
    compute_narrative_stats = None


def render_export_page(narratives):
    """Render export options page"""
    
    st.title("📤 Export & Reports")
    st.write("Export narrative data in various formats for external analysis")
    
    # Always show system status
    st.markdown("---")
    st.subheader("📊 Export System Status")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("💾 Narratives Available", len(narratives) if narratives else 0)
    col2.metric("📄 Export Modules", "✅ Loaded" if EXPORT_AVAILABLE else "⚠️ Missing")
    col3.metric("📑 PDF Support", "✅ Yes" if REPORTLAB_AVAILABLE else "❌ No")
    
    if not EXPORT_AVAILABLE:
        st.error("⚠️ Export modules not found!")
        if IMPORT_ERROR:
            with st.expander("Show error details"):
                st.code(IMPORT_ERROR)
        st.info("""
        **To fix this:**
        1. Make sure `core/exports/` folder exists
        2. Required files:
           - `core/exports/__init__.py`
           - `core/exports/json_exporter.py`
           - `core/exports/csv_exporter.py`
           - `core/exports/pdf_exporter.py`
        3. Run: `python quick_setup.py`
        """)
        return
    
    # Show guide if no data
    if not narratives or len(narratives) == 0:
        st.info("📦 No data available for export yet.")
        
        # Show getting started guide
        st.markdown("---")
        st.subheader("🚀 Getting Started with Exports")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### ➕ Add Data First
            
            Before exporting, add some narratives:
            
            1. Go to **"Add New Claim"** tab
            2. Enter text claims
            3. Upload images  
            4. Upload videos
            
            **Quick setup:**
            
            Run: python quick_setup.py
            """)
        
        with col2:
            st.markdown("""
            ### 📤 Export Formats
            
            Once you have data, export as:
            
            - **📄 JSON** - Full structured data
            - **📊 CSV** - Spreadsheet format
            - **📑 PDF** - Professional reports
            
            Both bulk and individual exports available
            """)
        
        # Show sample export preview
        st.markdown("---")
        st.subheader("📋 Sample Export Preview")
        st.caption("This is what your exports will look like")
        
        sample_data = {
            "narrative_id": "NAR_sample123",
            "total_memories": 5,
            "first_seen": 2020,
            "last_seen": 2024,
            "lifespan": 4,
            "sources": ["twitter", "facebook", "whatsapp"],
            "threat_level": "MEDIUM",
            "memories": [
                {
                    "year": 2020,
                    "source": "twitter",
                    "claim": "Sample misinformation claim",
                    "type": "text"
                },
                {
                    "year": 2022,
                    "source": "facebook",
                    "claim": "Same claim resurfaces",
                    "type": "text"
                }
            ]
        }
        
        tab1, tab2, tab3 = st.tabs(["JSON Preview", "CSV Preview", "Export Info"])
        
        with tab1:
            st.json(sample_data)
            st.caption("Complete structured data with all metadata")
        
        with tab2:
            st.code("""narrative_id,year,source,claim,type
NAR_sample123,2020,twitter,Sample misinformation claim,text
NAR_sample123,2022,facebook,Same claim resurfaces,text
NAR_sample123,2024,whatsapp,Viral again during crisis,text""")
            st.caption("Flat format for spreadsheet analysis")
        
        with tab3:
            st.markdown("""
            **When to use each format:**
            
            - **JSON**: Full data preservation, re-importing, programmatic analysis
            - **CSV**: Excel/spreadsheet analysis, visualization tools
            - **PDF**: Professional reports, presentations, sharing
            
            All exports saved to `exports/` folder
            """)
        
        st.info("💡 Add real narratives to unlock export functionality!")
        return
    
    # FULL EXPORT FUNCTIONALITY WITH DATA
    total_memories = sum(len(v) for v in narratives.values())
    
    st.markdown("---")
    st.success(f"✅ Ready to export: **{len(narratives)} narratives** with **{total_memories} memories**")
    
    # Export All Narratives
    st.header("📦 Bulk Export (All Narratives)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export All (JSON)", use_container_width=True):
            try:
                with st.spinner("Generating JSON..."):
                    filepath = export_all_narratives_json(narratives)
                st.success(f"✅ Exported to: `{filepath}`")
                
                with open(filepath, 'rb') as f:
                    st.download_button(
                        "⬇️ Download JSON",
                        f,
                        file_name=filepath.split('/')[-1].split('\\')[-1],
                        mime='application/json',
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Export failed: {e}")
    
    with col2:
        if st.button("📊 Export All (CSV)", use_container_width=True):
            try:
                with st.spinner("Generating CSV..."):
                    filepath = export_all_narratives_csv(narratives)
                st.success(f"✅ Exported to: `{filepath}`")
                
                with open(filepath, 'rb') as f:
                    st.download_button(
                        "⬇️ Download CSV",
                        f,
                        file_name=filepath.split('/')[-1].split('\\')[-1],
                        mime='text/csv',
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Export failed: {e}")
    
    with col3:
        st.info("💡 **Tip:** JSON for complete data, CSV for spreadsheets")
    
    st.markdown("---")
    
    # Individual Narrative Export
    st.header("🎯 Individual Narrative Export")
    
    narrative_ids = list(narratives.keys())
    narrative_ids.sort(key=lambda x: len(narratives[x]), reverse=True)
    
    selected_narrative = st.selectbox(
        "Select Narrative to Export",
        narrative_ids,
        format_func=lambda x: f"{x} ({len(narratives[x])} memories)"
    )
    
    if selected_narrative:
        memories = narratives[selected_narrative]
        
        # Display preview
        st.markdown("### 📋 Narrative Preview")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💾 Memories", len(memories))
        
        years = [m.get('year') for m in memories if m.get('year')]
        if years:
            col2.metric("📅 First Seen", min(years))
            col3.metric("📅 Last Seen", max(years))
            col4.metric("⏳ Lifespan", f"{max(years) - min(years)} yrs")
        
        sources = list(set(m.get('source') for m in memories if m.get('source')))
        st.write(f"**🌐 Sources:** {', '.join(sources)}")
        
        modalities = list(set(m.get('type') for m in memories if m.get('type')))
        st.write(f"**📝 Types:** {', '.join(modalities)}")
        
        # Sample preview
        with st.expander("👀 Preview Sample Memories"):
            for i, m in enumerate(memories[:3], 1):
                st.write(f"**Memory {i}:**")
                st.json(m)
            if len(memories) > 3:
                st.caption(f"... and {len(memories) - 3} more")
        
        st.markdown("### 📤 Export This Narrative")
        
        # Export buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Export JSON", use_container_width=True):
                try:
                    filepath = export_narrative_history_json(selected_narrative, memories)
                    st.success(f"✅ Exported!")
                    
                    with open(filepath, 'rb') as f:
                        st.download_button(
                            "⬇️ Download",
                            f,
                            file_name=f"narrative_{selected_narrative}.json",
                            mime='application/json',
                            key='download_json',
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"Export failed: {e}")
        
        with col2:
            if st.button("📊 Export CSV", use_container_width=True):
                try:
                    filepath = export_narrative_history_csv(selected_narrative, memories)
                    st.success(f"✅ Exported!")
                    
                    with open(filepath, 'rb') as f:
                        st.download_button(
                            "⬇️ Download",
                            f,
                            file_name=f"narrative_{selected_narrative}.csv",
                            mime='text/csv',
                            key='download_csv',
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"Export failed: {e}")
        
        with col3:
            if REPORTLAB_AVAILABLE and compute_narrative_stats:
                if st.button("📑 Export PDF", use_container_width=True):
                    try:
                        with st.spinner("Generating PDF..."):
                            stats = compute_narrative_stats(memories)
                            filepath = export_narrative_report_pdf(selected_narrative, memories, stats)
                        st.success(f"✅ PDF generated!")
                        
                        with open(filepath, 'rb') as f:
                            st.download_button(
                                "⬇️ Download PDF",
                                f,
                                file_name=f"narrative_{selected_narrative}.pdf",
                                mime='application/pdf',
                                key='download_pdf',
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f"Export failed: {e}")
            else:
                st.warning("📑 PDF unavailable\n\nInstall: `pip install reportlab`")
    
    st.markdown("---")
    st.info("📁 All exports saved to `exports/` folder in your project directory")
"""
Enhanced Export functionality UI with always-visible content
"""
import streamlit as st
import json
from datetime import datetime
import os

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
    """Render export options page with enhanced features"""
    
    st.title("📤 Export & Reports")
    st.write("Export narrative data in various formats for external analysis and reporting")
    
    # Always show system status
    st.markdown("---")
    st.subheader("📊 Export System Status")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💾 Narratives", len(narratives) if narratives else 0)
    total_memories = sum(len(v) for v in narratives.values()) if narratives else 0
    col2.metric("📚 Memories", total_memories)
    col3.metric("📄 Export Modules", "✅ Ready" if EXPORT_AVAILABLE else "⚠️ Missing")
    col4.metric("📑 PDF Support", "✅ Active" if REPORTLAB_AVAILABLE else "❌ Install")
    
    if not EXPORT_AVAILABLE:
        st.error("⚠️ Export modules not found!")
        if IMPORT_ERROR:
            with st.expander("🔍 Show error details"):
                st.code(IMPORT_ERROR)
        st.info("""
        **To fix this:**
        1. Ensure `core/exports/` folder exists
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
            
            1. Go to **"➕ Add New Claim"** tab
            2. Enter text claims with metadata
            3. Upload images for visual analysis
            4. Upload videos for multimodal tracking
            
            **Quick setup:**
```bash
            python quick_setup.py
```
            This loads 20+ demo narratives automatically.
            """)
        
        with col2:
            st.markdown("""
            ### 📤 Available Export Formats
            
            Once you have data, export as:
            
            - **📄 JSON** - Complete structured data with metadata
            - **📊 CSV** - Flat spreadsheet format for Excel
            - **📑 PDF** - Professional formatted reports
            
            **Export types:**
            - **Bulk**: All narratives at once
            - **Individual**: Selected narrative with analytics
            """)
        
        # Show sample export preview
        st.markdown("---")
        st.subheader("📋 Sample Export Preview")
        st.caption("Preview what your exports will look like with real data")
        
        sample_data = {
            "narrative_id": "NAR_sample123",
            "total_memories": 5,
            "first_seen": 2020,
            "last_seen": 2024,
            "lifespan": 4,
            "sources": ["twitter", "facebook", "whatsapp"],
            "threat_level": "MEDIUM",
            "memory_strength": 75,
            "state": "ACTIVE",
            "memories": [
                {
                    "year": 2020,
                    "source": "twitter",
                    "claim": "Sample misinformation claim about floods",
                    "type": "text"
                },
                {
                    "year": 2022,
                    "source": "facebook",
                    "claim": "Same claim resurfaces with modifications",
                    "type": "text"
                },
                {
                    "year": 2024,
                    "source": "whatsapp",
                    "claim": "Viral again during monsoon season",
                    "type": "text"
                }
            ]
        }
        
        tab1, tab2, tab3 = st.tabs(["📄 JSON Preview", "📊 CSV Preview", "ℹ️ Export Guide"])
        
        with tab1:
            st.json(sample_data)
            st.caption("✅ Complete structured data with all metadata and relationships")
        
        with tab2:
            st.code("""narrative_id,year,source,claim,type,threat_level
NAR_sample123,2020,twitter,Sample misinformation claim about floods,text,MEDIUM
NAR_sample123,2022,facebook,Same claim resurfaces with modifications,text,MEDIUM
NAR_sample123,2024,whatsapp,Viral again during monsoon season,text,MEDIUM""")
            st.caption("✅ Flat format perfect for Excel, Google Sheets, and data analysis")
        
        with tab3:
            st.markdown("""
            ### 📚 Export Format Guide
            
            **When to use each format:**
            
            | Format | Best For | Features |
            |--------|----------|----------|
            | **JSON** | Programmatic analysis, Re-importing, Backups | Complete data, Nested structures, All metadata |
            | **CSV** | Spreadsheet analysis, Pivot tables, Charts | Flat format, Excel-friendly, Easy filtering |
            | **PDF** | Reports, Presentations, Sharing, Archival | Professional layout, Visual charts, Executive summaries |
            
            **Export locations:**
            - All exports saved to `exports/` folder
            - Timestamped filenames for version control
            - Download buttons for immediate access
            """)
        
        st.info("💡 **Tip:** Add real narratives to unlock export functionality!")
        return
    
    # FULL EXPORT FUNCTIONALITY WITH DATA
    st.markdown("---")
    st.success(f"✅ Export ready: **{len(narratives)} narratives** • **{total_memories} total memories**")
    
    # Export All Narratives
    st.header("📦 Bulk Export (All Narratives)")
    st.write("Export your entire narrative database in one operation")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export All (JSON)", use_container_width=True, key="bulk_json"):
            try:
                with st.spinner("🔄 Generating JSON export..."):
                    filepath = export_all_narratives_json(narratives)
                st.success(f"✅ Exported to: `{filepath}`")
                
                # Show file size
                file_size = os.path.getsize(filepath) / 1024  # KB
                st.caption(f"📁 File size: {file_size:.1f} KB")
                
                with open(filepath, 'rb') as f:
                    st.download_button(
                        "⬇️ Download JSON File",
                        f,
                        file_name=os.path.basename(filepath),
                        mime='application/json',
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"❌ Export failed: {e}")
    
    with col2:
        if st.button("📊 Export All (CSV)", use_container_width=True, key="bulk_csv"):
            try:
                with st.spinner("🔄 Generating CSV export..."):
                    filepath = export_all_narratives_csv(narratives)
                st.success(f"✅ Exported to: `{filepath}`")
                
                # Show file size
                file_size = os.path.getsize(filepath) / 1024  # KB
                st.caption(f"📁 File size: {file_size:.1f} KB")
                
                with open(filepath, 'rb') as f:
                    st.download_button(
                        "⬇️ Download CSV File",
                        f,
                        file_name=os.path.basename(filepath),
                        mime='text/csv',
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"❌ Export failed: {e}")
    
    with col3:
        st.info("""
        **💡 Quick Guide:**
        
        • JSON = Full data
        • CSV = Spreadsheets
        • Both timestamped
        """)
    
    st.markdown("---")
    
    # Individual Narrative Export
    st.header("🎯 Individual Narrative Export")
    st.write("Export a specific narrative with detailed analytics and visualizations")
    
    narrative_ids = list(narratives.keys())
    narrative_ids.sort(key=lambda x: len(narratives[x]), reverse=True)
    
    selected_narrative = st.selectbox(
        "📋 Select Narrative to Export",
        narrative_ids,
        format_func=lambda x: f"{x} ({len(narratives[x])} memories)",
        help="Narratives sorted by memory count (most to least)"
    )
    
    if selected_narrative:
        memories = narratives[selected_narrative]
        
        # Display preview with enhanced metrics
        st.markdown("### 📊 Narrative Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💾 Total Memories", len(memories))
        
        years = [m.get('year') for m in memories if m.get('year')]
        if years:
            col2.metric("📅 First Seen", min(years))
            col3.metric("📅 Last Seen", max(years))
            lifespan = max(years) - min(years)
            col4.metric("⏳ Lifespan", f"{lifespan} yrs", 
                       delta=f"{lifespan} years" if lifespan > 0 else "Same year")
        
        # Additional metrics
        col1, col2, col3 = st.columns(3)
        
        sources = list(set(m.get('source') for m in memories if m.get('source')))
        col1.metric("🌐 Unique Sources", len(sources))
        
        modalities = list(set(m.get('type') for m in memories if m.get('type')))
        col2.metric("📝 Content Types", len(modalities))
        
        # Calculate if resurfacing
        resurfacing = lifespan >= 1 and len(memories) >= 3 if years else False
        col3.metric("🔄 Resurfacing", "YES ✅" if resurfacing else "NO ❌")
        
        st.write(f"**🌐 Platforms:** {', '.join(sources)}")
        st.write(f"**📝 Modalities:** {', '.join(modalities)}")
        
        # Sample preview with expandable section
        with st.expander("👀 Preview Sample Memories (First 5)"):
            for i, m in enumerate(memories[:5], 1):
                st.markdown(f"**Memory {i}** | Year: {m.get('year', 'N/A')} | Source: {m.get('source', 'Unknown')}")
                st.json(m)
                if i < min(5, len(memories)):
                    st.markdown("---")
            if len(memories) > 5:
                st.caption(f"💡 **+{len(memories) - 5} more memories** available in full export")
        
        st.markdown("### 📤 Export Options for This Narrative")
        
        # Export buttons with enhanced UI
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Export as JSON", use_container_width=True, key="ind_json"):
                try:
                    with st.spinner("🔄 Generating JSON..."):
                        filepath = export_narrative_history_json(selected_narrative, memories)
                    st.success(f"✅ JSON exported!")
                    
                    file_size = os.path.getsize(filepath) / 1024
                    st.caption(f"📁 {file_size:.1f} KB")
                    
                    with open(filepath, 'rb') as f:
                        st.download_button(
                            "⬇️ Download JSON",
                            f,
                            file_name=f"narrative_{selected_narrative}.json",
                            mime='application/json',
                            key='download_json',
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"❌ Export failed: {e}")
        
        with col2:
            if st.button("📊 Export as CSV", use_container_width=True, key="ind_csv"):
                try:
                    with st.spinner("🔄 Generating CSV..."):
                        filepath = export_narrative_history_csv(selected_narrative, memories)
                    st.success(f"✅ CSV exported!")
                    
                    file_size = os.path.getsize(filepath) / 1024
                    st.caption(f"📁 {file_size:.1f} KB")
                    
                    with open(filepath, 'rb') as f:
                        st.download_button(
                            "⬇️ Download CSV",
                            f,
                            file_name=f"narrative_{selected_narrative}.csv",
                            mime='text/csv',
                            key='download_csv',
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"❌ Export failed: {e}")
        
        with col3:
            if REPORTLAB_AVAILABLE and compute_narrative_stats:
                if st.button("📑 Generate PDF Report", use_container_width=True, key="ind_pdf"):
                    try:
                        with st.spinner("🔄 Generating professional PDF report..."):
                            stats = compute_narrative_stats(memories)
                            filepath = export_narrative_report_pdf(selected_narrative, memories, stats)
                        st.success(f"✅ PDF report generated!")
                        
                        file_size = os.path.getsize(filepath) / 1024
                        st.caption(f"📁 {file_size:.1f} KB")
                        
                        with open(filepath, 'rb') as f:
                            st.download_button(
                                "⬇️ Download PDF Report",
                                f,
                                file_name=f"report_{selected_narrative}.pdf",
                                mime='application/pdf',
                                key='download_pdf',
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f"❌ PDF generation failed: {e}")
                        with st.expander("Show error details"):
                            import traceback
                            st.code(traceback.format_exc())
            else:
                st.warning("📑 PDF Unavailable")
                st.caption("Install ReportLab:")
                st.code("pip install reportlab")
    
    st.markdown("---")
    
    # Export information footer
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        📁 **Export Location**
        
        All files saved to:
        `exports/` folder
        
        Timestamped filenames for version control
        """)
    
    with col2:
        st.success("""
        ✅ **Export Features**
        
        • Instant downloads
        • Timestamped files
        • Multiple formats
        • Full metadata
        """)
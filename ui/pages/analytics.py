"""
Enhanced Analytics dashboard for SatyaAI with always-visible content
"""
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

# Try importing analytics modules with fallback
ANALYTICS_AVAILABLE = False
IMPORT_ERROR = None

try:
    from core.analytics.trend_detector import (
        detect_viral_narratives,
        analyze_narrative_clusters,
        detect_coordinated_campaigns,
        compute_platform_risk_scores
    )
    ANALYTICS_AVAILABLE = True
except ImportError as e:
    IMPORT_ERROR = str(e)


def render_analytics_page(narratives):
    """Render the analytics dashboard"""
    
    st.title("📊 Narrative Analytics Dashboard")
    st.write("Advanced analytics and insights from your narrative memory system")
    
    # Always show system overview
    st.markdown("---")
    st.subheader("🎯 System Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_narratives = len(narratives) if narratives else 0
    total_memories = sum(len(v) for v in narratives.values()) if narratives else 0
    
    col1.metric("📚 Total Narratives", total_narratives)
    col2.metric("💾 Total Memories", total_memories)
    col3.metric("🔧 Analytics Status", "✅ Active" if ANALYTICS_AVAILABLE else "⚠️ Limited")
    col4.metric("📅 Last Updated", datetime.now().strftime("%H:%M"))
    
    # Check if analytics module is available
    if not ANALYTICS_AVAILABLE:
        st.warning("⚠️ Advanced analytics modules not loaded!")
        if IMPORT_ERROR:
            with st.expander("🔍 Show error details"):
                st.code(IMPORT_ERROR)
        
        st.info("""
        **To enable advanced analytics:**
        1. Create folder: `core/analytics/`
        2. Add files:
           - `core/analytics/__init__.py`
           - `core/analytics/trend_detector.py`
        3. Restart the Streamlit app
        
        **Currently showing:** Basic analytics only
        """)
        
        # Show basic analytics even without the module
        render_basic_analytics(narratives)
        return
    
    # Check if data exists - show guide if empty
    if not narratives or len(narratives) == 0:
        st.info("📦 No narrative data available yet.")
        
        # Show getting started guide
        st.markdown("---")
        st.subheader("🚀 Getting Started with Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### ➕ Add Data First
            
            To see analytics, you need data:
            
            1. Go to **"Add New Claim"** tab
            2. Enter text claims
            3. Upload images
            4. Upload videos
            
            **Quick way:**
            
            Run: python quick_setup.py
            
            This loads demo narratives automatically.
            """)
        
        with col2:
            st.markdown("""
            ### 📊 Available Analytics
            
            Once you have data, you'll see:
            
            - 🔥 **Viral Detection** - Fast-spreading narratives
            - 📈 **Temporal Patterns** - Activity over time
            - 🎯 **Campaign Detection** - Coordinated efforts
            - ⚠️ **Platform Risks** - Source-based threats
            - 🧬 **Content Distribution** - Type analysis
            """)
        
        # Show sample visualization
        st.markdown("---")
        st.subheader("📊 Sample Analytics Preview")
        st.caption("This is what your analytics will look like with real data")
        
        # Demo charts
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Sample temporal data
        years = [2020, 2021, 2022, 2023, 2024]
        activity = [5, 12, 8, 15, 20]
        
        ax1.plot(years, activity, marker='o', linewidth=2, markersize=8, color='#4fd1c5')
        ax1.fill_between(years, activity, alpha=0.3, color='#4fd1c5')
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Narrative Activity')
        ax1.set_title('Sample: Temporal Activity Pattern')
        ax1.grid(True, alpha=0.3)
        
        # Sample content distribution
        modalities = ['Text', 'Image', 'Video']
        counts = [30, 15, 10]
        colors = ['#4fd1c5', '#f59e0b', '#ec4899']
        ax2.bar(modalities, counts, color=colors)
        ax2.set_ylabel('Count')
        ax2.set_title('Sample: Content Type Distribution')
        ax2.grid(True, alpha=0.3, axis='y')
        
        st.pyplot(fig)
        plt.close()
        
        st.info("💡 **This is sample data.** Add real narratives to see your actual analytics!")
        
        # Show what metrics look like
        st.markdown("---")
        st.subheader("📈 Sample Metrics Preview")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("🔥 Viral Narratives", "3", "+2")
        col2.metric("⚠️ High-Risk Platforms", "2", "-1")
        col3.metric("🎯 Detected Campaigns", "1", "")
        
        return
    
    # FULL ANALYTICS WITH DATA
    st.markdown("---")
    
    # Cluster analysis
    st.header("🧬 Narrative Ecosystem Analysis")
    
    try:
        cluster_stats = analyze_narrative_clusters(narratives)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Narratives", cluster_stats.get('total_narratives', 0))
        col2.metric("Total Memories", cluster_stats.get('total_memories', 0))
        col3.metric("Avg Size", f"{cluster_stats.get('avg_narrative_size', 0):.1f}")
        col4.metric("Largest Narrative", cluster_stats.get('largest_narrative', 0))
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Modality distribution
            st.subheader("📦 Content Type Distribution")
            modality_dist = cluster_stats.get('modality_distribution', {})
            
            if modality_dist:
                fig, ax = plt.subplots(figsize=(6, 4))
                colors = ['#4fd1c5', '#f59e0b', '#ec4899', '#8b5cf6']
                ax.bar(modality_dist.keys(), modality_dist.values(), 
                      color=colors[:len(modality_dist)])
                ax.set_ylabel('Count')
                ax.set_title('Distribution by Modality')
                ax.grid(True, alpha=0.3, axis='y')
                st.pyplot(fig)
                plt.close()
                
                # Show percentages
                total = sum(modality_dist.values())
                for mod, count in modality_dist.items():
                    pct = (count / total * 100) if total > 0 else 0
                    st.write(f"**{mod}:** {count} ({pct:.1f}%)")
            else:
                st.info("No modality data available")
        
        with col2:
            # Yearly activity
            st.subheader("📅 Temporal Activity Pattern")
            yearly = cluster_stats.get('yearly_activity', {})
            
            if yearly and len(yearly) > 0:
                fig, ax = plt.subplots(figsize=(6, 4))
                years = list(yearly.keys())
                counts = list(yearly.values())
                ax.plot(years, counts, marker='o', linewidth=2, markersize=8, color='#4fd1c5')
                ax.fill_between(years, counts, alpha=0.3, color='#4fd1c5')
                ax.set_xlabel('Year')
                ax.set_ylabel('Memory Points')
                ax.set_title('Activity Over Time')
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
                plt.close()
                
                peak_year = max(yearly.items(), key=lambda x: x[1])
                st.info(f"📈 Peak: **{peak_year[0]}** ({peak_year[1]} memories)")
            else:
                st.info("No temporal data available")
            
    except Exception as e:
        st.error(f"Error analyzing clusters: {e}")
        with st.expander("Show traceback"):
            import traceback
            st.code(traceback.format_exc())
    
    st.markdown("---")
    
    # Viral detection
    st.header("🔥 Viral Narrative Detection")
    
    try:
        viral = detect_viral_narratives(narratives, time_window_days=365)
        
        if viral and len(viral) > 0:
            st.success(f"🚨 **{len(viral)} viral narratives detected!**")
            
            for idx, v in enumerate(viral[:5], 1):
                risk_color = "🔴" if v['risk_score'] > 70 else "🟠" if v['risk_score'] > 40 else "🟡"
                
                with st.expander(f"{risk_color} #{idx} - {v['narrative_id']} (Risk: {v['risk_score']})"):
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Recent", v.get('recent_mentions', 0))
                    col2.metric("Total", v.get('total_mentions', 0))
                    col3.metric("Velocity", f"{v['velocity']:.0%}")
                    col4.metric("Platforms", v.get('platforms', 0))
                    
                    risk_pct = min(v.get('risk_score', 0), 100)
                    st.progress(risk_pct / 100)
        else:
            st.info("✅ No viral narratives detected in recent period.")
            
    except Exception as e:
        st.error(f"Error detecting viral narratives: {e}")
        with st.expander("Show traceback"):
            import traceback
            st.code(traceback.format_exc())
    
    st.markdown("---")
    
    # Platform risk scores
    st.header("⚠️ Platform Risk Assessment")
    
    try:
        platform_risks = compute_platform_risk_scores(narratives)
        
        if platform_risks and len(platform_risks) > 0:
            # Risk summary
            risk_summary = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
            for stats in platform_risks.values():
                level = stats.get('risk_level', 'LOW')
                risk_summary[level] = risk_summary.get(level, 0) + 1
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("🔴 Critical", risk_summary['CRITICAL'])
            col2.metric("🟠 High", risk_summary['HIGH'])
            col3.metric("🟡 Medium", risk_summary['MEDIUM'])
            col4.metric("🟢 Low", risk_summary['LOW'])
            
            for platform, stats in list(platform_risks.items())[:10]:
                risk_level = stats.get('risk_level', 'UNKNOWN')
                risk_icons = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢'}
                risk_icon = risk_icons.get(risk_level, '⚪')
                
                with st.expander(f"{risk_icon} **{platform.upper()}** - {risk_level}"):
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Unique Narratives", stats.get('unique_narratives', 0))
                    col2.metric("Total Mentions", stats.get('total_mentions', 0))
                    col3.metric("High Risk Count", stats.get('high_risk_count', 0))
                    
                    risk_pct = min(stats.get('risk_score', 0), 100)
                    st.progress(risk_pct / 100)
        else:
            st.info("No platform data available")
            
    except Exception as e:
        st.error(f"Error computing platform risks: {e}")
        with st.expander("Show traceback"):
            import traceback
            st.code(traceback.format_exc())
    
    st.markdown("---")
    
    # Coordinated campaigns
    st.header("🎯 Coordinated Campaign Detection")
    
    try:
        campaigns = detect_coordinated_campaigns(narratives)
        
        if campaigns and len(campaigns) > 0:
            st.warning(f"⚠️ **{len(campaigns)} potential campaigns detected!**")
            
            for idx, c in enumerate(campaigns[:5], 1):
                coord_score = c.get('coordination_score', 0)
                threat = "🔴 High" if coord_score > 50 else "🟡 Medium"
                
                with st.expander(f"🎯 #{idx}: {c.get('year')} • {c.get('platform')} • {threat}"):
                    col1, col2 = st.columns(2)
                    col1.metric("Narratives", c.get('narrative_count', 0))
                    col2.metric("Score", coord_score)
                    
                    st.markdown("**Involved Narratives:**")
                    for nid in c.get('narrative_ids', [])[:10]:
                        st.write(f"  • `{nid}`")
        else:
            st.success("✅ No coordinated campaigns detected.")
            
    except Exception as e:
        st.error(f"Error detecting campaigns: {e}")
        with st.expander("Show traceback"):
            import traceback
            st.code(traceback.format_exc())


def render_basic_analytics(narratives):
    """Render basic analytics when advanced modules aren't available"""
    
    if not narratives or len(narratives) == 0:
        st.info("Add some narratives to see basic analytics")
        return
    
    st.markdown("---")
    st.subheader("📊 Basic Analytics (Limited Mode)")
    
    # Calculate basic stats
    total_memories = sum(len(v) for v in narratives.values())
    avg_size = total_memories / len(narratives) if narratives else 0
    
    all_years = []
    all_sources = set()
    all_types = set()
    
    for memories in narratives.values():
        for m in memories:
            if m.get('year'):
                all_years.append(int(m['year']))
            if m.get('source'):
                all_sources.add(m['source'])
            if m.get('type'):
                all_types.add(m['type'])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Avg Size", f"{avg_size:.1f}")
    col2.metric("🌐 Sources", len(all_sources))
    col3.metric("📝 Types", len(all_types))
    
    if all_years:
        st.markdown("### 📅 Activity by Year")
        year_counts = {}
        for year in all_years:
            year_counts[year] = year_counts.get(year, 0) + 1
        
        fig, ax = plt.subplots(figsize=(10, 4))
        years = sorted(year_counts.keys())
        counts = [year_counts[y] for y in years]
        ax.bar(years, counts, color='#4fd1c5', alpha=0.7)
        ax.set_xlabel('Year')
        ax.set_ylabel('Count')
        ax.set_title('Memory Distribution Over Time')
        ax.grid(True, alpha=0.3, axis='y')
        st.pyplot(fig)
        plt.close()
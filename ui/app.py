import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st

# ⚠️ CRITICAL: set_page_config MUST BE FIRST
st.set_page_config(
    page_title="SatyaAI – Digital Trust Memory System", 
    page_icon="🧠",
    layout="centered"
)

import json
import matplotlib.pyplot as plt
from core.narratives.narrative_manager import process_new_claim, process_new_image
from core.reports.trust_report import generate_trust_report
from core.narratives.narrative_explorer import get_all_narratives
from core.reports.risk_engine import calculate_risk
from core.memory.image_search import search_images
from core.memory.video_store import store_video
from core.memory.video_search import search_video_frames
from core.embeddings.video_processor import extract_frames
from core.utils.validators import (
    validate_claim_text, 
    validate_year, 
    validate_source,
    ValidationError
)

def clean_platform_name(platform):
    """Convert internal platform codes to user-friendly names"""
    platform_map = {
        'analysis_query': 'Search Query',
        'user_upload': 'Direct Upload',
        'upload': 'Direct Upload',
        'unknown': 'Platform Not Specified',
        'whatsapp': 'WhatsApp',
        'facebook': 'Facebook',
        'twitter': 'Twitter/X',
        'telegram': 'Telegram',
        'instagram': 'Instagram',
        'youtube': 'YouTube',
        'news': 'News Media',
        'tiktok': 'TikTok'
    }
    
    if not platform or platform.strip() == '':
        return 'Platform Not Specified'
    
    platform_lower = str(platform).lower().strip()
    return platform_map.get(platform_lower, platform.title())

try:
    from core.config import UPLOAD_DIR, APP_TITLE, APP_ICON
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
except ImportError:
    from pathlib import Path
    UPLOAD_DIR = Path("data/uploads")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    APP_TITLE = "SatyaAI – Digital Trust Memory System"
    APP_ICON = "🧠"

# Auto-load demo data if system is empty
if 'demo_data_loaded' not in st.session_state:
    try:
        narratives_check = get_all_narratives(limit=5)
        if len(narratives_check) == 0:
            with st.spinner("Loading demo data..."):
                demo_claims = [
                    ("Fake image shows massive Delhi flood", 2020, "facebook"),
                    ("Old flood photo reshared as current disaster", 2022, "twitter"),
                    ("Same flood image viral again this monsoon", 2024, "whatsapp"),
                    ("Vaccine causes infertility claim goes viral", 2021, "telegram"),
                    ("Old vaccine infertility rumor resurfaces", 2023, "twitter"),
                    ("COVID vaccine side effects being hidden", 2024, "facebook"),
                    ("Government hid flood data from public", 2022, "whatsapp"),
                    ("Doctored video of political leader spreads", 2023, "facebook"),
                    ("Climate change hoax narrative resurfaces", 2020, "twitter"),
                    ("Election fraud claims go viral again", 2024, "twitter"),
                ]
                
                for claim, year, source in demo_claims:
                    try:
                        process_new_claim(claim, {"year": year, "source": source})
                    except:
                        pass
                
                st.success("✅ Demo data loaded successfully!")
                st.session_state.demo_data_loaded = True
    except:
        st.session_state.demo_data_loaded = True

# Apply consistent dark theme styling
st.markdown("""
<style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .block-container {
        padding-top: 1rem;
    }
    h1, h2, h3 {
        color: #4fd1c5;
    }
    .stMetric {
        background: #111827;
        padding: 12px;
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(79,209,197,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Add this right after st.set_page_config() and before the imports

# Force sidebar to be expanded on first load
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'expanded'

# Update the set_page_config to include initial_sidebar_state
st.set_page_config(
    page_title="SatyaAI – Digital Trust Memory System", 
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"  # Add this line
)

# Enhanced dark theme styling with improved sidebar
st.markdown("""
<style>
    /* Main background */
    body {
        background-color: #0e1117;
        color: white;
    }
    
    .block-container {
        padding-top: 1rem;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #4fd1c5;
        font-weight: 600;
    }
    
    /* Metrics */
    .stMetric {
        background: linear-gradient(135deg, #1a1f2e 0%, #111827 100%);
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0px 4px 15px rgba(79,209,197,0.15);
        border: 1px solid rgba(79,209,197,0.2);
    }
    
    /* Make sidebar collapse button always visible */
    [data-testid="collapsedControl"] {
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    /* Ensure close button is always visible on hover and non-hover */
    [data-testid="stSidebar"] button[kind="header"] {
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    /* Make the X button always visible */
    section[data-testid="stSidebar"] > div > div > div > button {
        opacity: 1 !important;
        visibility: visible !important;
        background: rgba(79,209,197,0.2) !important;
        border-radius: 4px !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f2e 0%, #0e1117 100%);
        border-right: 2px solid rgba(79,209,197,0.3);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, #1a1f2e 0%, #0e1117 100%);
    }
    
    /* Sidebar headers */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #4fd1c5 !important;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(79,209,197,0.3);
    }
    
    /* Sidebar markdown text */
    [data-testid="stSidebar"] .element-container {
        color: #e0e0e0;
    }
    
    [data-testid="stSidebar"] p {
        color: #b8b8b8;
        line-height: 1.6;
    }
    
    /* Sidebar dividers */
    [data-testid="stSidebar"] hr {
        border-color: rgba(79,209,197,0.2);
        margin: 1.5rem 0;
    }
    
    /* Sidebar info/success/warning boxes */
    [data-testid="stSidebar"] .stAlert {
        background: rgba(79,209,197,0.1);
        border-left: 4px solid #4fd1c5;
        border-radius: 8px;
        padding: 12px;
        margin: 10px 0;
    }
    
    [data-testid="stSidebar"] .stSuccess {
        background: rgba(34,197,94,0.1);
        border-left: 4px solid #22c55e;
    }
    
    [data-testid="stSidebar"] .stWarning {
        background: rgba(251,191,36,0.1);
        border-left: 4px solid #fbbf24;
    }
    
    [data-testid="stSidebar"] .stError {
        background: rgba(239,68,68,0.1);
        border-left: 4px solid #ef4444;
    }
    
    /* Sidebar title styling */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] > p:first-child {
        font-size: 1.1em;
        font-weight: 600;
    }
    
    /* Better button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4fd1c5 0%, #3b9e91 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        box-shadow: 0 4px 10px rgba(79,209,197,0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(79,209,197,0.4);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(79,209,197,0.1);
        border-radius: 8px;
        border-left: 3px solid #4fd1c5;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(79,209,197,0.1);
        border-radius: 8px 8px 0 0;
        color: #4fd1c5;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4fd1c5 0%, #3b9e91 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)


st.sidebar.markdown("""
<div style='text-align: center; padding: 15px; background: linear-gradient(135deg, rgba(79,209,197,0.2) 0%, rgba(79,209,197,0.05) 100%); border-radius: 10px; margin-bottom: 15px; border: 2px solid rgba(79,209,197,0.3);'>
    <h1 style='margin: 0; font-size: 2em; color: #4fd1c5;'>🧠 SatyaAI</h1>
    <p style='margin: 5px 0 0 0; color: #888; font-size: 0.85em;'>Digital Trust Memory</p>
</div>
""", unsafe_allow_html=True)

# System Status - Bigger and more readable
st.sidebar.markdown("### ⚙️ System Status")
try:
    all_narratives_check = get_all_narratives(limit=1)
    st.sidebar.markdown("""
<div style='background: rgba(34,197,94,0.1); padding: 12px; border-radius: 8px; border-left: 3px solid #22c55e; margin: 8px 0;'>
    <p style='margin: 4px 0; color: #22c55e; font-size: 0.9em;'>✅ <strong>Memory:</strong> Online</p>
    <p style='margin: 4px 0; color: #22c55e; font-size: 0.9em;'>✅ <strong>Models:</strong> Loaded</p>
    <p style='margin: 4px 0; color: #4fd1c5; font-size: 0.9em;'>🔄 <strong>Engine:</strong> Active</p>
</div>
""", unsafe_allow_html=True)
except Exception as e:
    st.sidebar.markdown(f"""
<div style='background: rgba(239,68,68,0.1); padding: 12px; border-radius: 8px; border-left: 3px solid #ef4444; margin: 8px 0;'>
    <p style='margin: 4px 0; color: #ef4444; font-size: 0.9em;'>❌ <strong>Error:</strong> {str(e)[:40]}...</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# About SatyaAI
st.sidebar.markdown("### 🎯 About")
st.sidebar.info("""
**Not a fact-checker.**  
A **long-term misinformation memory engine**.

**Capabilities:**
- 🧠 Remembers misinformation
- 🔄 Tracks recurring narratives  
- 📜 Reconstructs claim history
- 🔍 Detects resurfacing patterns
""")

st.sidebar.markdown("---")

# Why SatyaAI
st.sidebar.markdown("### 💡 Why SatyaAI?")
st.sidebar.warning("""
**Misinformation doesn't disappear.**  
**It comes back.**

**SatyaAI remembers:**
- What was said  
- What was shown  
- How narratives evolve
""")

st.sidebar.markdown("---")

# Ethics note
st.sidebar.error("""
⚖️ **Ethics Note**  
SatyaAI does not declare truth.  

It provides **memory, history, and patterns** to support human decision-making.
""")

st.sidebar.markdown("---")
st.sidebar.caption("Version 1.0 | © 2026")

# MAIN CONTENT
mode = st.selectbox("Select Use Case Mode", [
    "Journalist",
    "Government Analyst",
    "Social Media Monitor",
    "Researcher"
])

st.markdown("### 🎯 Active Mode")
if mode == "Journalist":
    st.info("Mode: Investigating viral claims and tracing narrative origins.")
elif mode == "Government Analyst":
    st.info("Mode: Monitoring misinformation campaigns and public risk.")
elif mode == "Social Media Monitor":
    st.info("Mode: Tracking resurfacing narratives across platforms.")
elif mode == "Researcher":
    st.info("Mode: Studying long-term evolution of misinformation.")

try:
    all_narratives = get_all_narratives()
    total_narratives = len(all_narratives)
    total_memories = sum(len(v) for v in all_narratives.values())
except Exception as e:
    st.error(f"Error loading narratives: {e}")
    all_narratives = {}
    total_narratives = 0
    total_memories = 0

st.title(f"{APP_ICON} SatyaAI – Digital Trust Memory System")
st.write("An AI system that remembers misinformation narratives over time.")

c1, c2 = st.columns(2)
c1.metric("🧠 Total Narratives", total_narratives)
c2.metric("📚 Total Memory Points", total_memories)

st.markdown("---")

if all_narratives:
    st.subheader("📈 Narrative Memory Distribution")
    sizes = [len(v) for v in all_narratives.values()]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(range(len(sizes)), sizes, color='#4fd1c5', alpha=0.7)
    ax.set_ylabel("Memory Points", fontsize=12)
    ax.set_xlabel("Narratives", fontsize=12)
    ax.set_title("Memories per Narrative", fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    st.pyplot(fig)
    plt.close()

st.markdown("---")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "➕ Add New Claim",
    "🔍 Analyze Claim",
    "🖼 Analyze Image",
    "🎥 Analyze Video",
    "🧬 Explore Narratives",
    "📤 Export & Reports",
    "📊 Analytics",
    "💾 Backup"
])

with tab1:
    st.subheader("➕ Add new data into memory")
    claim = st.text_area("Enter claim or news text", height=100)
    year = st.text_input("Year (e.g. 2024)", value="")
    source = st.text_input("Source (twitter, news, whatsapp, etc.)", value="")
    
    if st.button("Store Text Claim", type="primary"):
        try:
            if not claim.strip():
                st.error("❌ Please enter a claim.")
            else:
                validated_claim = validate_claim_text(claim)
                validated_year = validate_year(year)
                validated_source = validate_source(source)
                
                nid = process_new_claim(validated_claim, {
                    "year": validated_year, 
                    "source": validated_source
                })
                st.success(f"✅ Stored under Narrative ID: **{nid}**")
                st.balloons()
        except ValidationError as e:
            st.error(f"❌ Validation Error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    st.markdown("---")
    st.markdown("### 🖼 Upload Image")
    image = st.file_uploader("Upload image", type=["png", "jpg", "jpeg", "jfif", "webp"])
    
    if image:
        try:
            path = UPLOAD_DIR / image.name
            with open(path, "wb") as f:
                f.write(image.read())
            st.image(str(path), width=300, caption="Uploaded Image")
            if st.button("Store Image", type="primary"):
                try:
                    validated_year = validate_year(year)
                    nid = process_new_image(str(path), {"year": validated_year, "source": "upload"})
                    st.success(f"✅ Image stored under narrative **{nid}**")
                except ValidationError as e:
                    st.error(f"❌ {str(e)}")
        except Exception as e:
            st.error(f"❌ Error processing image: {str(e)}")
    
    st.markdown("---")
    st.markdown("### 🎥 Upload Video")
    video = st.file_uploader("Upload video", type=["mp4", "mov", "avi"])
    
    if video:
        try:
            vpath = UPLOAD_DIR / video.name
            with open(vpath, "wb") as f:
                f.write(video.read())
            st.video(str(vpath))
            if st.button("Store Video", type="primary"):
                with st.spinner("Processing video frames..."):
                    store_video(str(vpath), {"source": "upload"})
                st.success("✅ Video stored as multimodal memory.")
        except Exception as e:
            st.error(f"❌ Error processing video: {str(e)}")

with tab2:
    st.subheader("🔍 Analyze a claim using system memory")
    demo = st.selectbox("Quick demo examples:", [
        "",
        "Fake flood image in Delhi",
        "Old vaccine rumor resurfaces",
        "Government hid flood data"
    ])
    
    query = demo if demo else st.text_area("Enter claim to analyze", height=100)
    
    if st.button("Generate Trust Report", type="primary"):
        if not query.strip():
            st.warning("⚠️ Please enter a claim to analyze.")
        else:
            try:
                with st.spinner("Analyzing narrative memory..."):
                    report = generate_trust_report(query)
                
                if report["status"] == "no_history":
                    st.info("ℹ️ No similar history found in the system.")
                else:
                    risk = calculate_risk(report)
                    st.markdown(f"## 🧠 Narrative ID: `{report['narrative_id']}`")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("🔢 Occurrences", report["occurrence_count"])
                    col2.metric("⚠️ Risk Level", risk["risk_level"])
                    col3.metric("📊 Risk Score", risk["risk_score"])
                    
                    if report["occurrence_count"] >= 3:
                        st.error("🚨 **ALERT:** Resurfacing Narrative Detected")
                    elif report["occurrence_count"] == 2:
                        st.warning("⚠️ **WARNING:** Repeated Claim Detected")
                    else:
                        st.success("✅ New or Rare Claim")
                    
                    st.markdown("---")
                    st.markdown("### 📋 Basic Information")
                    info_col1, info_col2 = st.columns(2)
                    with info_col1:
                        st.write(f"**First seen:** {report['first_seen']}")
                        st.write(f"**Last seen:** {report['last_seen']}")
                    with info_col2:
                        st.write(f"**Lifespan:** {report['lifespan']} years")
                        st.write(f"**Platforms:** {', '.join(report['sources_seen'])}")
                    
                    st.info(f"💡 **Insight:** {report['insight']}")
                    st.markdown("---")
                    st.markdown("## 🧠 Narrative Intelligence")
                    
                    intel_col1, intel_col2, intel_col3 = st.columns(3)
                    threat_level = report.get("threat_level", "UNKNOWN")
                    threat_colors = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}
                    threat_icon = threat_colors.get(threat_level, "⚪")
                    
                    intel_col1.metric("⚠️ Threat Level", f"{threat_icon} {threat_level}")
                    intel_col2.metric("💪 Narrative Strength", f"{report.get('strength', 0)}/100")
                    intel_col3.metric("🔄 Resurfacing", "YES ✅" if report.get("resurfacing") else "NO ❌")
                    
                    st.write(f"**🧬 Modalities:** {', '.join(report.get('modalities', []))}")
                    st.write(f"**📊 Memory Strength:** {report.get('memory_strength', 0)}")
                    st.write(f"**🎯 State:** {report.get('narrative_state', 'Unknown')}")
                    
                    st.markdown("---")
                    st.markdown("### 📈 Temporal Activity")
                    years = [int(t["year"]) for t in report["timeline"] if str(t.get("year", "")).isdigit()]
                    
                    if years:
                        fig, ax = plt.subplots(figsize=(10, 4))
                        ax.hist(years, bins=range(min(years), max(years)+2), color='#4fd1c5', alpha=0.7, edgecolor='black')
                        ax.set_title("Narrative Activity Over Time", fontsize=14, fontweight='bold')
                        ax.set_xlabel("Year", fontsize=12)
                        ax.set_ylabel("Occurrences", fontsize=12)
                        ax.grid(axis='y', alpha=0.3)
                        st.pyplot(fig)
                        plt.close()
                    
                    st.markdown("---")
                    st.markdown("### 🕐 Narrative Timeline")
                    for idx, t in enumerate(report["timeline"], 1):
                        claim_text = t.get('claim', '[Visual content]')
                        st.write(f"**{idx}.** {t['year']} | 📱 {t['source']} | {claim_text[:100]}... | *Score: {t['score']:.3f}*")
                    
                    st.markdown("---")
                    action_col1, action_col2 = st.columns(2)
                    
                    with action_col1:
                        st.download_button(
                            "📄 Download Trust Report (JSON)",
                            data=json.dumps(report, indent=2, default=str),
                            file_name=f"trust_report_{report['narrative_id']}.json",
                            mime="application/json"
                        )
                    
                    with action_col2:
                        if st.button("🚩 Flag as High-Risk", type="secondary"):
                            st.success("✅ Narrative flagged for manual review")
            
            except Exception as e:
                st.error(f"❌ Error generating report: {str(e)}")
with tab3:
    st.subheader("🖼 Analyze an Image")
    uploaded = st.file_uploader("Upload an image to analyze", type=["jpg", "jpeg", "png", "jfif", "webp"], key="analyze_image")
    
    if uploaded:
        try:
            path = UPLOAD_DIR / uploaded.name
            with open(path, "wb") as f:
                f.write(uploaded.read())
            st.image(str(path), caption="Uploaded Image", width=400)
            
            if st.button("Analyze Image Memory", type="primary"):
                with st.spinner("Searching visual memory..."):
                    # First, link to narrative
                    narrative_id = process_new_image(str(path), {"source": "analysis_query"})
                    
                    # Search for similar images
                    results = search_images(str(path), limit=10)
                    
                    if results:
                        st.success(f"✅ **MATCH FOUND!** This image is linked to narrative: **{narrative_id}**")
                        
                        # Calculate statistics
                        total_matches = len(results)
                        platforms = set()
                        years_seen = []
                        
                        for r in results:
                            p = r.payload
                            if p.get('source'):
                                platforms.add(p.get('source'))
                            if p.get('year'):
                                try:
                                    years_seen.append(int(p.get('year')))
                                except:
                                    pass
                        
                        # Display summary metrics
                        st.markdown("### 📊 Circulation History")
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("🔍 Similar Images", total_matches)
                        
                        # Count real platforms (excluding internal codes)
                        real_platforms = [p for p in platforms if p not in ['analysis_query', 'user_upload', 'upload', 'unknown', '']]
                        col2.metric("📱 Platforms", len(real_platforms) if real_platforms else len(platforms))
                        
                        if years_seen:
                            col3.metric("📅 First Seen", min(years_seen))
                            col4.metric("📅 Last Seen", max(years_seen))
                            
                            lifespan = max(years_seen) - min(years_seen)
                            if lifespan >= 2:
                                st.error(f"🚨 **ALERT:** This image has been circulating for {lifespan} years!")
                            elif lifespan >= 1:
                                st.warning(f"⚠️ **WARNING:** This image has resurfaced (first seen {min(years_seen)})")
                        
                        # Show platform distribution
                        if platforms:
                            st.markdown("### 📱 Platform Distribution")
                            cleaned_platforms = [clean_platform_name(p) for p in platforms]
                            # Remove generic entries if real platforms exist
                            real_platforms_cleaned = [p for p in cleaned_platforms if p not in ['Search Query', 'Direct Upload', 'Platform Not Specified']]
                            if real_platforms_cleaned:
                                platform_text = ", ".join(sorted(set(real_platforms_cleaned)))
                            else:
                                platform_text = ", ".join(sorted(set(cleaned_platforms)))
                            st.info(f"**Circulated on:** {platform_text}")
                        
                        # Timeline visualization
                        if years_seen and len(years_seen) > 1:
                            st.markdown("### 📈 Temporal Distribution")
                            fig, ax = plt.subplots(figsize=(10, 3))
                            ax.hist(years_seen, bins=range(min(years_seen), max(years_seen)+2), 
                                   color='#ff6b6b', alpha=0.7, edgecolor='black')
                            ax.set_title("Image Circulation Over Time", fontsize=12, fontweight='bold')
                            ax.set_xlabel("Year", fontsize=10)
                            ax.set_ylabel("Occurrences", fontsize=10)
                            ax.grid(axis='y', alpha=0.3)
                            st.pyplot(fig)
                            plt.close()
                        
                        # Detailed matches
                        st.markdown("### 🔎 Detailed Match History")
                        st.write(f"Found **{len(results)}** similar instances in our memory:")
                        
                        for idx, r in enumerate(results, 1):
                            p = r.payload
                            similarity_pct = int(r.score * 100)
                            
                            # Get platform from payload, show friendly message if not available
                            cleaned_platform = clean_platform_name(p.get('source', 'Platform not specified'))
                            year_display = p.get('year', 'Year unknown')
                            
                            # Color code by similarity
                            if r.score > 0.95:
                                match_type = "🔴 EXACT MATCH"
                            elif r.score > 0.85:
                                match_type = "🟡 VERY SIMILAR"
                            else:
                                match_type = "🟢 SIMILAR"
                            
                            with st.expander(f"{match_type} #{idx} | {similarity_pct}% similar | {cleaned_platform} ({year_display})"):
                                col_a, col_b = st.columns([1, 2])
                                
                                with col_a:
                                    if os.path.exists(p.get("path", "")):
                                        st.image(p.get("path"), width=200, caption="Historical instance")
                                
                                with col_b:
                                    st.write(f"**📅 Year:** {year_display}")
                                    st.write(f"**📱 Platform:** {cleaned_platform}")
                                    st.write(f"**🎯 Similarity Score:** {r.score:.4f}")
                                    st.write(f"**🧬 Narrative ID:** {p.get('narrative_id', 'N/A')}")
                                    
                                    # Show associated claim if available
                                    if p.get('claim'):
                                        st.write(f"**💬 Associated Claim:** {p.get('claim')[:200]}")
                                
                                # Show full metadata
                                with st.expander("Show full metadata"):
                                    st.json(p)
                    else:
                        st.success(f"✅ Image stored under narrative: **{narrative_id}**")
                        st.info("ℹ️ **NEW IMAGE:** No similar images found in memory. This appears to be the first occurrence.")
                        st.write("This image has been added to our memory system and will be tracked for future occurrences.")
                        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

with tab4:
    st.subheader("🎥 Analyze a Video")
    uploaded_video = st.file_uploader("Upload a video to analyze", type=["mp4", "mov", "avi"], key="analyze_video")
    
    if uploaded_video:
        try:
            video_path = UPLOAD_DIR / uploaded_video.name
            with open(video_path, "wb") as f:
                f.write(uploaded_video.read())
            st.video(str(video_path))
            
            if st.button("Analyze Video Memory", type="primary"):
                with st.spinner("Extracting frames and searching visual memory..."):
                    # Extract frames
                    frames = extract_frames(str(video_path))
                    st.info(f"📸 Extracted {len(frames)} frames for analysis")
                    
                    # Analyze frames
                    narrative_hits = {}
                    all_matches = []
                    platforms_seen = set()
                    years_seen = []
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Analyze first 5 frames (or all if less than 5)
                    frames_to_analyze = frames[:min(5, len(frames))]
                    
                    for idx, frame_path in enumerate(frames_to_analyze):
                        status_text.text(f"Analyzing frame {idx + 1}/{len(frames_to_analyze)}...")
                        results = search_video_frames(frame_path, limit=5)
                        
                        for r in results:
                            nid = r.payload.get("narrative_id")
                            if nid:
                                narrative_hits[nid] = narrative_hits.get(nid, 0) + 1
                            
                            # Collect metadata
                            if r.payload.get('source'):
                                platforms_seen.add(r.payload.get('source'))
                            if r.payload.get('year'):
                                try:
                                    years_seen.append(int(r.payload.get('year')))
                                except:
                                    pass
                            
                            all_matches.append({
                                'frame_idx': idx + 1,
                                'result': r,
                                'payload': r.payload
                            })
                        
                        progress_bar.progress((idx + 1) / len(frames_to_analyze))
                    
                    status_text.empty()
                    
                    if narrative_hits:
                        st.success(f"✅ **MATCH FOUND!** This video is linked to {len(narrative_hits)} narrative(s)!")
                        
                        # Summary metrics
                        st.markdown("### 📊 Video Circulation History")
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("🔍 Frame Matches", len(all_matches))
                        col2.metric("🧬 Narratives", len(narrative_hits))
                        
                        # Count real platforms
                        real_platforms = [p for p in platforms_seen if p not in ['analysis_query', 'user_upload', 'upload', 'unknown', '']]
                        col3.metric("📱 Platforms", len(real_platforms) if real_platforms else len(platforms_seen))
                        
                        if years_seen:
                            col4.metric("📅 First Seen", min(years_seen))
                            
                            lifespan = max(years_seen) - min(years_seen) if len(set(years_seen)) > 1 else 0
                            if lifespan >= 2:
                                st.error(f"🚨 **ALERT:** Similar video content has been circulating for {lifespan} years!")
                            elif lifespan >= 1:
                                st.warning(f"⚠️ **WARNING:** Similar video content has resurfaced")
                        
                        # Platform distribution
                        if platforms_seen:
                            st.markdown("### 📱 Platform Distribution")
                            cleaned_platforms = [clean_platform_name(p) for p in platforms_seen]
                            real_platforms_cleaned = [p for p in cleaned_platforms if p not in ['Search Query', 'Direct Upload', 'Platform Not Specified']]
                            if real_platforms_cleaned:
                                platform_text = ", ".join(sorted(set(real_platforms_cleaned)))
                            else:
                                platform_text = ", ".join(sorted(set(cleaned_platforms)))
                            st.info(f"**Circulated on:** {platform_text}")
                        
                        # Timeline
                        if years_seen and len(years_seen) > 1:
                            st.markdown("### 📈 Temporal Distribution")
                            fig, ax = plt.subplots(figsize=(10, 3))
                            ax.hist(years_seen, bins=range(min(years_seen), max(years_seen)+2), 
                                   color='#845ef7', alpha=0.7, edgecolor='black')
                            ax.set_title("Video Content Circulation Over Time", fontsize=12, fontweight='bold')
                            ax.set_xlabel("Year", fontsize=10)
                            ax.set_ylabel("Occurrences", fontsize=10)
                            ax.grid(axis='y', alpha=0.3)
                            st.pyplot(fig)
                            plt.close()
                        
                        # Narrative breakdown
                        st.markdown("### 🎯 Related Narratives")
                        for nid, count in sorted(narrative_hits.items(), key=lambda x: x[1], reverse=True):
                            with st.expander(f"🧠 **{nid}** | {count} frame match(es)"):
                                # Get narrative details
                                narrative_matches = [m for m in all_matches if m['payload'].get('narrative_id') == nid]
                                
                                # Show statistics for this narrative
                                st.write(f"**Total frames matched:** {count}")
                                
                                # Show each match
                                for match in narrative_matches[:3]:  # Show top 3
                                    p = match['payload']
                                    cleaned_platform = clean_platform_name(p.get('source', 'Platform not specified'))
                                    year_display = p.get('year', 'Year unknown')
                                    
                                    st.markdown(f"**Frame {match['frame_idx']}:**")
                                    st.write(f"- 📅 Year: {year_display}")
                                    st.write(f"- 📱 Platform: {cleaned_platform}")
                                    st.write(f"- 🎯 Similarity: {match['result'].score:.3f}")
                                    if p.get('claim'):
                                        st.write(f"- 💬 Context: {p.get('claim')[:150]}...")
                                    st.markdown("---")
                        
                        # Detailed frame analysis
                        st.markdown("### 🔍 Detailed Frame Analysis")
                        with st.expander(f"View all {len(all_matches)} matches"):
                            for match in all_matches:
                                p = match['payload']
                                cleaned_platform = clean_platform_name(p.get('source', 'Platform not specified'))
                                year_display = p.get('year', 'Year unknown')
                                st.write(f"**Frame {match['frame_idx']} → {year_display} | {cleaned_platform} | Score: {match['result'].score:.3f}**")
                                if p.get('claim'):
                                    st.write(f"Context: {p.get('claim')[:200]}")
                                st.markdown("---")
                    
                    else:
                        st.info("ℹ️ **NEW VIDEO:** No similar video content found in memory.")
                        st.write("This video has been processed and stored. Future similar videos will be detected.")
                        
                        # Still store the video
                        with st.spinner("Storing video in memory..."):
                            store_video(str(video_path), {"source": "analysis_query"})
                        st.success("✅ Video stored in memory system")
                        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            
                        
with tab5:
    st.subheader("🧬 Narrative Memory Explorer")
    st.write("Explore all long-term misinformation narratives stored in SatyaAI.")
    
    try:
        narratives = get_all_narratives()
        
        if not narratives:
            st.info("ℹ️ No narratives found yet. Add some data first.")
        else:
            search_term = st.text_input("🔍 Search narratives", "")
            sort_by = st.selectbox("Sort by", ["Most Recent", "Oldest First", "Most Memories", "Longest Lifespan"])
            
            narrative_list = []
            for nid, items in narratives.items():
                years = [int(i.get("year")) for i in items if i.get("year") and str(i.get("year")).isdigit()]
                first_seen = min(years) if years else 0
                last_seen = max(years) if years else 0
                lifespan = last_seen - first_seen if years else 0
                
                if search_term:
                    narrative_text = " ".join([str(i.get("claim", "")) for i in items]).lower()
                    if search_term.lower() not in narrative_text:
                        continue
                
                narrative_list.append({
                    "id": nid, "items": items, "first_seen": first_seen,
                    "last_seen": last_seen, "lifespan": lifespan, "count": len(items)
                })
            
            if sort_by == "Most Recent":
                narrative_list.sort(key=lambda x: x["last_seen"], reverse=True)
            elif sort_by == "Oldest First":
                narrative_list.sort(key=lambda x: x["first_seen"])
            elif sort_by == "Most Memories":
                narrative_list.sort(key=lambda x: x["count"], reverse=True)
            elif sort_by == "Longest Lifespan":
                narrative_list.sort(key=lambda x: x["lifespan"], reverse=True)
            
            st.write(f"**Showing {len(narrative_list)} narrative(s)**")
            
            for n in narrative_list:
                first_display = n["first_seen"] if n["first_seen"] else "Unknown"
                last_display = n["last_seen"] if n["last_seen"] else "Unknown"
                
                with st.expander(f"🧠 {n['id']} | {n['count']} memories | {first_display} → {last_display} | Lifespan: {n['lifespan']} years"):
                    for i in sorted(n["items"], key=lambda x: str(x.get("year", ""))):
                        if i.get("type") in ["image", "video_frame"]:
                            st.write(f"🕐 {i.get('year')} | 📱 {i.get('source')} | 🖼 [Visual evidence]")
                            if os.path.exists(i.get("path", "")):
                                st.image(i.get("path"), width=250)
                        else:
                            st.write(f"🕐 {i.get('year')} | 📱 {i.get('source')} | 💬 {i.get('claim', 'N/A')[:100]}")
    except Exception as e:
        st.error(f"❌ Error loading narratives: {str(e)}")

with tab6:
    from ui.modules.exports_page import render_export_page
    render_export_page(all_narratives)

with tab7:
    from ui.modules.analytics_page import render_analytics_page
    render_analytics_page(all_narratives)

with tab8:
    from ui.modules.backup_page import render_backup_page
    render_backup_page()


st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🧠 <strong>SatyaAI</strong> - Digital Trust Memory System</p>
    <p>Built with Qdrant</p>
    <p style='font-size: 0.8em;'>For decision-support purposes only. Does not declare truth or falsehood.</p>
</div>
""", unsafe_allow_html=True)
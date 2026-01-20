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

# SIDEBAR - Reorganized layout
st.sidebar.title(f"{APP_ICON} SatyaAI")
st.sidebar.markdown("**Digital Trust Memory System**")

# System Status at top
st.sidebar.markdown("### ⚙️ System Status")
try:
    all_narratives_check = get_all_narratives(limit=1)
    st.sidebar.success("✅ Qdrant Memory: Online")
    st.sidebar.success("✅ Embedding Models: Loaded")
    st.sidebar.info("🔄 Multimodal Engine: Active")
except Exception as e:
    st.sidebar.error("❌ System Error")
    st.sidebar.error(f"Details: {str(e)}")

st.sidebar.markdown("---")

# About SatyaAI
st.sidebar.markdown("### 🎯 About SatyaAI")
st.sidebar.markdown("""
SatyaAI is not a fact-checker.  
It is a **long-term misinformation memory engine**.

**Key Capabilities:**
- 🧠 Remembers misinformation
- 🔄 Tracks recurring narratives
- 📜 Reconstructs claim history
- 🔍 Detects resurfacing patterns

Built using **Qdrant** vector memory.
""")

st.sidebar.markdown("---")

# Notification badge
try:
    from ui.modules.notifications_page import show_notification_badge
    show_notification_badge()
except:
    pass

st.sidebar.markdown("---")

# Why SatyaAI
st.sidebar.markdown("### 💡 Why SatyaAI?")
st.sidebar.info("""
Misinformation doesn't disappear.  
**It comes back.**

SatyaAI remembers:  
• What was said  
• What was shown  
• How narratives evolve
""")

st.sidebar.markdown("---")

# Ethics note at bottom
st.sidebar.warning("""
⚖️ **Ethics Note**  
SatyaAI does not declare truth.  
It provides memory, history,  
and patterns to support  
human decision-making.
""")

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
    year = st.text_input("Year (e.g. 2024)", value="2024")
    source = st.text_input("Source (twitter, news, whatsapp, etc.)", value="twitter")
    
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
                    narrative_id = process_new_image(str(path), {"source": "user_upload"})
                    st.success(f"✅ Image linked to narrative: **{narrative_id}**")
                    results = search_images(str(path), limit=5)
                    
                    if results:
                        st.markdown("### 🔍 Similar Past Visuals Found")
                        st.write(f"Found {len(results)} similar images:")
                        for idx, r in enumerate(results, 1):
                            p = r.payload
                            with st.expander(f"Match {idx}: Similarity {r.score:.3f} | {p.get('source', 'Unknown')} ({p.get('year', 'N/A')})"):
                                if os.path.exists(p.get("path", "")):
                                    st.image(p.get("path"), width=300)
                                st.json(p)
                    else:
                        st.info("No similar images found in memory.")
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
                    frames = extract_frames(str(video_path))
                    st.info(f"📸 Extracted {len(frames)} frames")
                    narrative_hits = {}
                    progress_bar = st.progress(0)
                    
                    for idx, frame_path in enumerate(frames[:5]):
                        results = search_video_frames(frame_path, limit=3)
                        for r in results:
                            nid = r.payload.get("narrative_id")
                            if nid:
                                narrative_hits[nid] = narrative_hits.get(nid, 0) + 1
                        progress_bar.progress((idx + 1) / min(5, len(frames)))
                    
                    if narrative_hits:
                        st.success(f"✅ Found matches in {len(narrative_hits)} narratives!")
                        st.markdown("### 🎯 Related Narratives")
                        for nid, count in sorted(narrative_hits.items(), key=lambda x: x[1], reverse=True):
                            st.write(f"🧠 **{nid}** matched {count} frame(s)")
                    else:
                        st.warning("⚠️ No similar past video content found.")
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
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
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



st.set_page_config(page_title="SatyaAI – Digital Trust Memory", layout="centered")


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



st.sidebar.title("🧠 SatyaAI")

st.sidebar.markdown("""
### Digital Trust Memory System

SatyaAI is not a fact-checker.  
It is a **long-term misinformation memory engine.**

It:
• Remembers misinformation  
• Tracks recurring narratives  
• Reconstructs claim history  
• Detects resurfacing patterns  

Built using **Qdrant vector memory**.
""")

st.sidebar.markdown("---")

st.sidebar.markdown("### 🎯 Why SatyaAI?")
st.sidebar.info("""
Misinformation doesn’t disappear.  
It comes back.

SatyaAI was built to remember:
what was said,
what was shown,
and how narratives evolve.
""")

st.sidebar.markdown("---")

st.sidebar.markdown("### ⚙ System Status")
st.sidebar.success("Qdrant Memory: Online")
st.sidebar.success("Embedding Models: Loaded")
st.sidebar.info("Multimodal Engine: Active")

st.sidebar.markdown("---")

st.sidebar.warning("""
Ethics Note:
SatyaAI does not declare truth.
It provides memory, history,
and patterns to support
human decision-making.
""")



all_narratives = get_all_narratives()
total_narratives = len(all_narratives)
total_memories = sum(len(v) for v in all_narratives.values())

st.title("🧠 SatyaAI – Digital Trust Memory System")
st.write("An AI system that remembers misinformation narratives over time.")

c1, c2 = st.columns(2)
c1.metric("🧠 Total Narratives", total_narratives)
c2.metric("📚 Total Memory Points", total_memories)

st.markdown("---")

if all_narratives:
    st.subheader("📈 Narrative Memory Distribution")

    sizes = [len(v) for v in all_narratives.values()]
    fig, ax = plt.subplots()
    ax.bar(range(len(sizes)), sizes)
    ax.set_ylabel("Memory Points")
    ax.set_xlabel("Narratives")
    ax.set_title("Memories per Narrative")

    st.pyplot(fig)

st.markdown("---")




tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "➕ Add New Claim",
    "🔍 Analyze Claim",
    "🖼 Analyze Image",
    "🎥 Analyze Video",
    "🧬 Explore Narratives"
])



with tab1:
    st.subheader("➕ Add new data into memory")

    claim = st.text_area("Enter claim or news text")
    year = st.text_input("Year (e.g. 2022)")
    source = st.text_input("Source (twitter, news, whatsapp, etc.)")

    if st.button("Store Text Claim"):
        if claim.strip():
            nid = process_new_claim(claim, {"year": year, "source": source})
            st.success(f"Stored under Narrative ID: {nid}")
        else:
            st.warning("Please enter a claim.")


    st.markdown("### 🖼 Upload Image")
    image = st.file_uploader("Upload image", type=["png", "jpg", "jpeg", "jfif", "webp"])

    if image:
        os.makedirs("data/uploads", exist_ok=True)
        path = os.path.join("data/uploads", image.name)

        with open(path, "wb") as f:
            f.write(image.read())

        st.image(path, width=250)

        if st.button("Store Image"):
            nid = process_new_image(path, {"year": year, "source": "upload"})
            st.success(f"Image stored under narrative {nid}")


    st.markdown("### 🎥 Upload Video")
    video = st.file_uploader("Upload video", type=["mp4", "mov", "avi"])

    if video:
        os.makedirs("data/uploads", exist_ok=True)
        vpath = os.path.join("data/uploads", video.name)

        with open(vpath, "wb") as f:
            f.write(video.read())

        st.video(vpath)

        if st.button("Store Video"):
            store_video(vpath, {"source": "upload"})
            st.success("Video stored as multimodal memory.")


with tab2:
    st.subheader("🔍 Analyze a claim using system memory")

    demo = st.selectbox("Quick demo examples:", [
        "",
        "Fake flood image in Delhi",
        "Old vaccine rumor resurfaces",
        "Government hid flood data"
    ])

    query = demo if demo else st.text_area("Enter claim to analyze")

    if st.button("Generate Trust Report"):
        if query.strip():
            report = generate_trust_report(query)

            if report["status"] == "no_history":
                st.info("No similar history found.")
            else:
                risk = calculate_risk(report)

                st.markdown(f"## 🧠 Narrative ID: `{report['narrative_id']}`")

                c1, c2 = st.columns(2)
                c1.metric("🔁 Occurrences", report["occurrence_count"])
                c2.metric("⚠ Risk Level", risk["risk_level"], risk["risk_score"])

                # Resurfacing badge
                if report["occurrence_count"] >= 3:
                    st.error("🚨 Resurfacing Narrative Detected")
                elif report["occurrence_count"] == 2:
                    st.warning("⚠ Repeated Claim Detected")
                else:
                    st.success("🆕 New or Rare Claim")

                st.write("**First seen:**", report["first_seen"])
                st.write("**Last seen:**", report["last_seen"])
                st.write("**Platforms:**", report["sources_seen"])

                st.info(report["insight"])
                st.markdown("### 🧠 Intelligence Summary")
                if report["occurrence_count"] >= 3:
                   st.error("This narrative shows long-term resurfacing behavior and is likely part of a recurring misinformation cycle.")
                elif report["occurrence_count"] == 2:
                   st.warning("This narrative has reappeared before and should be monitored.")
                else:
                   st.success("This appears to be a new or low-spread narrative.")

                st.markdown("### 🕒 Narrative Timeline")
                for t in report["timeline"]:
                    st.write(f"• {t['year']} | {t['source']} | {t['claim']} (score {t['score']})")

                st.download_button(
                    "📄 Download Trust Report",
                    data=json.dumps(report, indent=2),
                    file_name="satyaai_trust_report.json"
                )
                
                if st.button("🚩 Flag this narrative as harmful"):
                   st.success("This narrative has been marked as high-risk for review.")


        else:
            st.warning("Please enter a claim.")


with tab3:
    st.subheader("🖼 Analyze an Image")

    uploaded = st.file_uploader("Upload an image to analyze", type=["jpg", "jpeg", "png", "jfif", "webp"])

    if uploaded:
        os.makedirs("data/uploads", exist_ok=True)
        path = os.path.join("data/uploads", uploaded.name)

        with open(path, "wb") as f:
            f.write(uploaded.read())

        st.image(path, caption="Uploaded image", width=300)

        if st.button("Analyze Image Memory"):
            narrative_id = process_new_image(path, {"source": "user_upload"})
            st.success(f"Image linked to narrative: {narrative_id}")

            results = search_images(path, limit=5)

            st.markdown("### 🔁 Similar past visuals found:")
            for r in results:
                p = r.payload
                if os.path.exists(p.get("path", "")):
                    st.image(p.get("path"), width=200)
                st.write(p, " | score:", round(r.score, 3))


with tab4:
    st.subheader("🎥 Analyze a Video")

    uploaded_video = st.file_uploader("Upload a video to analyze", type=["mp4", "mov", "avi"])

    if uploaded_video:
        os.makedirs("data/uploads", exist_ok=True)
        video_path = os.path.join("data/uploads", uploaded_video.name)

        with open(video_path, "wb") as f:
            f.write(uploaded_video.read())

        st.video(video_path)

        if st.button("Analyze Video Memory"):
            st.info("Extracting frames and searching visual memory...")

            frames = extract_frames(video_path)

            narrative_hits = {}

            for frame_path in frames[:5]:  # limit for speed
                results = search_video_frames(frame_path, limit=3)

                for r in results:
                    nid = r.payload.get("narrative_id")
                    if nid:
                        narrative_hits[nid] = narrative_hits.get(nid, 0) + 1

            if narrative_hits:
                st.success("Related narratives found:")

                for nid, count in narrative_hits.items():
                    st.write(f"🧠 {nid} matched {count} times")

            else:
                st.warning("No similar past video content found.")



with tab5:
    st.subheader("🧬 Narrative Memory Explorer")
    st.write("Explore all long-term misinformation narratives stored in SatyaAI.")

    narratives = get_all_narratives()

    if not narratives:
        st.info("No narratives found yet. Add some data first.")
    else:
        for nid, items in narratives.items():
            years = [int(i.get("year")) for i in items if i.get("year") and str(i.get("year")).isdigit()]
            first_seen = min(years) if years else "Unknown"
            last_seen = max(years) if years else "Unknown"

            with st.expander(f"🧠 {nid} | {len(items)} memories | {first_seen} → {last_seen}"):
                for i in sorted(items, key=lambda x: str(x.get("year", ""))):
                    if i.get("type") in ["image", "video_frame"]:
                        st.write(f"🕒 {i.get('year')} | {i.get('source')} | [Visual evidence]")
                        if os.path.exists(i.get("path", "")):
                            st.image(i.get("path"), width=250)
                    else:
                        st.write(f"🕒 {i.get('year')} | {i.get('source')} | {i.get('claim')}")



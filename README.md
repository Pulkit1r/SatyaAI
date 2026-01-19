# 🧠 SatyaAI — Digital Trust Memory System  
A Multimodal Long-Term Misinformation Memory Engine built on Qdrant

---

## 📌 Overview

SatyaAI is a multimodal digital trust memory system designed to combat long-term and resurfacing misinformation.

Unlike traditional fact-checkers or chatbots that analyze content in isolation, SatyaAI is built as a persistent narrative intelligence engine. It stores and retrieves historical claims, images, and videos to detect how misinformation narratives evolve, resurface, and spread across time and platforms.

**SatyaAI does not declare content "true" or "false."**  
Instead, it provides evidence-based historical memory so that journalists, researchers, and institutions can make informed decisions.

---

## 🎯 Problem Statement

Misinformation does not disappear after being debunked.  
It resurfaces during elections, disasters, pandemics, and social crises — often with minor wording changes or reused visuals.

**Examples:**
- Old flood images reshared as new disasters  
- Debunked vaccine rumors resurfacing every few years  
- The same political narratives recycled across platforms  

Current AI systems lack long-term memory. They repeatedly rediscover the same misinformation because they cannot remember what has already happened.

**SatyaAI reframes misinformation as a memory and narrative intelligence problem.**

---

## 💡 What SatyaAI Solves

SatyaAI enables:

- **Long-term storage** of misinformation narratives  
- **Multimodal retrieval** across text, images, and video  
- **Detection of resurfacing** and recurring narratives  
- **Historical reconstruction** of how claims evolve  
- **Evidence-grounded trust reports**  
- **Advanced analytics** including:
  - Viral narrative detection
  - Platform risk scoring
  - Coordinated campaign identification
  - Temporal pattern analysis
- **Professional PDF reports** for sharing and archival
- **Flexible export options** (JSON, CSV, PDF)

This transforms misinformation handling from reactionary fact-checking into **proactive narrative intelligence**.

---

## 🏗️ System Architecture

SatyaAI follows a layered multimodal memory architecture:

### Core Layers

**1. User Interface Layer** (Streamlit Dashboard)
- Tab-based navigation for different workflows
- Real-time analytics visualization with matplotlib
- Interactive trust report generation
- Export and data management interfaces
- System status monitoring

**2. Multimodal Ingestion Layer**
- Text claims processing with validation
- Image upload and analysis
- Video frame extraction and storage
- Metadata enrichment

**3. Embedding Layer**
- **Text:** Sentence Transformers (all-MiniLM-L6-v2, 384-dim)
- **Images:** CLIP embeddings (512-dim)
- **Video:** Frame-by-frame CLIP processing

**4. Vector Memory Core** (Qdrant)
- Three separate collections: `text_memory`, `image_memory`, `video_memory`
- Semantic similarity search with cosine distance
- Persistent storage with rich metadata filtering
- Narrative-level grouping via `narrative_id`

**5. Narrative Intelligence Layer**
- Temporal pattern detection
- Resurfacing analysis
- Threat level assessment (LOW, MEDIUM, HIGH, CRITICAL)
- Memory strength calculation
- State tracking (NEW, ACTIVE, DORMANT, RESURFACED)
- Mutation and drift scoring

**6. Analytics & Reporting Layer**
- Viral narrative detection with velocity metrics
- Platform risk scoring
- Coordinated campaign identification
- Professional PDF report generation with ReportLab
- Bulk JSON/CSV exports

**All system intelligence is retrieval-driven and grounded in stored evidence.**

---

## 🧠 Why Qdrant is Central

Qdrant serves as the primary long-term vector memory system.

**It enables:**
- High-dimensional semantic similarity search  
- Multimodal vector storage in separate collections
- Structured payload filtering and metadata queries
- Narrative-level grouping across modalities
- Scalable persistent memory with disk storage

**SatyaAI does not use Qdrant as simple storage — it is the core cognitive substrate of the system.**

### Collection Structure
```
qdrant_data/
├── text_memory/       # 384-dim vectors (MiniLM)
│   └── Payload: {narrative_id, year, source, type, claim}
├── image_memory/      # 512-dim vectors (CLIP)
│   └── Payload: {narrative_id, year, source, type, path}
└── video_memory/      # 512-dim vectors (CLIP frames)
    └── Payload: {narrative_id, year, source, type, path, video_source}
```

**Each memory stores:**
- `narrative_id`: Links related memories across modalities
- `year`: Temporal tracking for trend analysis
- `source`: Platform attribution (twitter, facebook, etc.)
- `type`: Content modality (text, image, video_frame)
- `claim`: Text content (for text memories)
- `path`: File location (for images/video frames)

---

## 📁 Project Structure
```
SatyaAI/
├── core/                           # Core system logic
│   ├── analytics/                  # Analytics engines
│   │   ├── __init__.py
│   │   └── trend_detector.py       # Viral detection, clustering, campaigns
│   ├── embeddings/                 # Embedding generators
│   │   ├── image_embedder.py       # CLIP for images
│   │   ├── text_embedder.py        # Sentence transformers
│   │   └── video_processor.py      # Frame extraction
│   ├── exports/                    # Export functionality
│   │   ├── __init__.py
│   │   ├── csv_exporter.py         # CSV generation
│   │   ├── json_exporter.py        # JSON exports
│   │   └── pdf_exporter.py         # Professional PDF reports
│   ├── memory/                     # Memory operations
│   │   ├── image_search.py         # Visual similarity search
│   │   ├── image_store.py          # Image storage
│   │   ├── text_search.py          # Semantic text search
│   │   ├── text_store.py           # Text storage
│   │   ├── video_search.py         # Video frame search
│   │   └── video_store.py          # Video processing & storage
│   ├── narratives/                 # Narrative intelligence
│   │   ├── decay_engine.py         # Memory strength calculation
│   │   ├── narrative_evolution.py  # Drift detection
│   │   ├── narrative_explorer.py   # Data retrieval
│   │   ├── narrative_graph.py      # NetworkX graph representation
│   │   ├── narrative_intelligence.py  # Stats & threat scoring
│   │   ├── narrative_manager.py    # Claim/image processing
│   │   ├── state_engine.py         # State classification
│   │   └── temporal_engine.py      # Temporal pattern detection
│   ├── qdrant/                     # Vector database
│   │   ├── client.py               # Qdrant connection & collections
│   │   └── schema.py               # Collection setup
│   ├── reports/                    # Report generation
│   │   ├── evidence_engine.py      # Evidence scoring
│   │   ├── resurgence_engine.py    # Resurgence calculation
│   │   ├── responsibility.py       # Attribution logic
│   │   ├── risk_engine.py          # Risk assessment
│   │   └── trust_report.py         # Trust report generation
│   ├── utils/                      # Utilities
│   │   └── validators.py           # Input validation
│   └── config.py                   # System configuration
├── ui/                             # User interface
│   ├── modules/                    # UI modules (not Streamlit pages)
│   │   ├── __init__.py
│   │   ├── analytics_page.py       # Analytics dashboard renderer
│   │   └── exports_page.py         # Export interface renderer
│   └── app.py                      # Main Streamlit application
├── data/                           # Data storage
│   └── uploads/                    # Uploaded files (images, videos)
├── exports/                        # Generated exports
│   ├── *.json                      # JSON exports
│   ├── *.csv                       # CSV exports
│   └── *.pdf                       # PDF reports
├── qdrant_data/                    # Qdrant persistent storage
│   ├── collection/
│   ├── meta.json
│   └── storage.sqlite
├── tests/                          # Test suite
│   ├── unit/                       # Unit tests
│   └── integration/                # Integration tests
├── demo/                           # Demo materials
│   └── screenshots/                # Application screenshots
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Python dependencies
├── quick_setup.py                  # Quick setup with demo data
├── quick_test.py                   # Manual testing script
├── diagnostic_check.py             # System diagnostic tool
├── test_pages.py                   # UI page testing
├── run_tests.py                    # Test runner
├── README.md                       # This file
└── TESTING.md                      # Testing documentation
```

---

## 🔀 Multimodal Strategy

SatyaAI supports three primary modalities:

### Text
- Semantic embedding of claims using Sentence Transformers
- Detects paraphrased and mutated narratives
- Links similar claims across time and platforms
- Threshold: 0.75 similarity for linking

### Images
- Visual similarity search using CLIP embeddings
- Detects reused or slightly modified images
- Works across different image formats and sizes
- Threshold: 0.80 similarity for linking

### Video
- Videos decomposed into frames (1 frame per second)
- Each frame embedded as visual memory
- Enables resurfacing detection even when full videos change
- Frame-level matching with 0.80 threshold

**Each memory item stores metadata:**
- `narrative_id` for cross-modal linking
- `year` for temporal analysis
- `source` for platform tracking
- `type` for modality identification

---

## 🧩 Memory Beyond a Single Prompt

SatyaAI implements true long-term memory:

**Narratives are persistent objects that evolve over time.**  
New inputs either:
1. **Reinforce an existing narrative** (if similarity > threshold)
2. **Create a new narrative** (if no match found)

The system separates:
- **Knowledge memory:** Stored narratives in Qdrant
- **Interaction context:** User queries and sessions
- **System intelligence:** Risk scoring and resurfacing logic

**Key insight:** Memory persists across sessions, enabling longitudinal analysis of misinformation evolution.

---

## 🔍 Retrieval, Memory & Recommendation Logic

### Processing Pipeline

1. **New content is embedded** using appropriate model (text/image)
2. **Qdrant similarity search** retrieves nearest memories
3. **Similarity threshold check:**
   - High similarity (>0.75 text, >0.80 image) → Link to existing narrative
   - Low similarity → Create new narrative with unique ID
4. **Metadata enrichment** with year, source, type
5. **Storage in appropriate collection**

### Trust Report Generation

**Outputs include:**
- Occurrence counts across time
- First/last seen dates
- Platform diffusion patterns
- Resurfacing alerts (gap > 2 years)
- Historical timelines with similarity scores
- Threat level assessment (LOW/MEDIUM/HIGH/CRITICAL)
- Memory strength score (1-100)
- Narrative state (NEW/ACTIVE/DORMANT/RESURFACED)

**All outputs are traceable to retrieved records.**

---

## 📊 Advanced Analytics

### Viral Narrative Detection
Identifies narratives spreading rapidly across platforms:
- **Velocity metric:** Recent mentions / Total mentions
- **Platform diversity score:** Number of unique sources
- **Risk scoring:** Combination of velocity, diversity, and recency
- **Threshold:** 3+ recent mentions with 30%+ velocity

### Platform Risk Assessment
Evaluates platform-level threat patterns:
- **Unique narratives per platform**
- **High-risk narrative counts**
- **Total mention volume**
- **Risk levels:** CRITICAL (100+), HIGH (60+), MEDIUM (30+), LOW (<30)

### Coordinated Campaign Detection
Identifies potential coordination patterns:
- **Same-year, same-platform clustering**
- **Multiple narratives (3+) threshold**
- **Coordination score based on narrative count**
- **Temporal grouping analysis**

### Narrative Clustering
Ecosystem-wide statistics:
- Total narratives and memories
- Average narrative size
- Modality distribution
- Yearly activity patterns
- Peak activity identification

---

## ⚖️ Ethics, Responsibility & Limitations

### Principles

**SatyaAI is a decision-support system, not an authority.**

- ✅ **No automated truth labeling**
- ✅ **Evidence-first outputs**
- ✅ **Human-in-the-loop analysis**
- ✅ **Transparency of retrieved data**
- ✅ **Privacy-aware payload design**
- ✅ **Attribution to sources**

### Limitations

**Current limitations:**
- **Embedding bias:** Inherits biases from pre-trained models
- **Partial visual matches:** May miss heavily edited content
- **Incomplete datasets:** Only knows what has been stored
- **Language support:** Optimized for English text
- **Threshold sensitivity:** Fixed similarity thresholds may need tuning

### Future Improvements

**Planned enhancements:**
- 🎤 Audio ingestion and analysis
- 📉 Narrative decay modeling
- 🌍 Multilingual memory support
- 🕸️ Influence network analysis
- 🤖 Active learning for threshold optimization
- 🔗 Cross-platform entity resolution

---

## 🖥️ User Interface

The SatyaAI dashboard provides **7 main tabs:**

### 1. ➕ Add New Claim
- Text claim entry with validation
- Image upload and processing
- Video upload with frame extraction
- Real-time narrative linking feedback

### 2. 🔍 Analyze Claim
- Text-based trust report generation
- Similarity search results
- Temporal activity visualization
- Complete narrative timeline
- Threat assessment display
- Risk scoring and insights

### 3. 🖼️ Analyze Image
- Image upload and analysis
- Visual similarity results
- Historical image matches
- Source and year attribution

### 4. 🎥 Analyze Video
- Video upload and processing
- Frame extraction progress
- Narrative match detection
- Cross-frame analysis

### 5. 🧬 Explore Narratives
- Complete narrative browser
- Search and filtering
- Sorting options (recent, oldest, most memories, longest lifespan)
- Detailed memory inspection
- Visual content preview

### 6. 📤 Export & Reports
- **Bulk exports:** All narratives to JSON/CSV
- **Individual exports:** Selected narrative to JSON/CSV/PDF
- **Professional PDF reports** with ReportLab styling
- Download functionality
- Export preview samples

### 7. 📊 Analytics
- **System overview metrics**
- **Viral narrative detection** with risk visualization
- **Platform risk assessment** with color-coded levels
- **Coordinated campaign detection**
- **Temporal activity charts**
- **Content distribution analysis**

**Additional Features:**
- **Sidebar:** System status, ethics reminder, project info
- **Mode selection:** Journalist, Government Analyst, Social Media Monitor, Researcher
- **Real-time updates:** Metrics refresh on data changes

---

## 📈 Demo & Examples

### Example 1: Claim Resurfacing

**Input:**
```
"Old vaccine infertility rumor resurfaces"
```

**Output:**
- Narrative ID: `NAR_a1b2c3d4`
- Occurrences: 5
- Risk Level: HIGH
- Threat Level: MEDIUM
- First seen: 2021
- Last seen: 2024
- Platform history: telegram → twitter → facebook → whatsapp
- Timeline with 5 similar claims
- Resurfacing alert (3-year lifespan)

---

### Example 2: Image Reuse

**Input:**
- Uploaded flood image

**Output:**
- Linked narrative: `NAR_e5f6g7h8`
- Similar historical visuals: 3 matches found
- Visual reuse detected across:
  - 2020: facebook
  - 2022: twitter
  - 2024: whatsapp
- Similarity scores: 0.92, 0.88, 0.85

---

### Example 3: Narrative Exploration

**Action:**
- Open "Explore Narratives" tab
- Search for "flood"
- Sort by "Most Recent"

**Output:**
- 4 flood-related narratives
- Timeline reconstruction
- Multimodal memory display
- Source attribution
- Visual evidence gallery

---

### Example 4: Analytics Dashboard

**Action:**
- Open "Analytics" tab

**Output:**
- Total narratives: 18
- Total memories: 30
- Viral narratives detected: 2
  - NAR_flood_2024 (Velocity: 65%, Risk: 78)
  - NAR_vaccine_2024 (Velocity: 45%, Risk: 62)
- Platform risks:
  - Twitter: HIGH (Risk: 85)
  - Facebook: MEDIUM (Risk: 52)
  - WhatsApp: MEDIUM (Risk: 48)
- Coordinated campaigns: 1 detected
  - 2024 twitter campaign (3 narratives)

---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.8+
- 4GB RAM minimum (8GB recommended)
- 2GB disk space for Qdrant storage

### Installation

**1. Clone repository**
```bash
git clone <repo-link>
cd SatyaAI
```

**2. Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Initialize Qdrant collections**
```bash
python -m core.qdrant.schema
```

**5. Load demo data (optional)**
```bash
python quick_setup.py
```

**6. Run diagnostic check**
```bash
python diagnostic_check.py
```

**7. Launch application**
```bash
streamlit run ui/app.py
```

The application will open at `http://localhost:8501`

---

## 🔧 Configuration

Edit `core/config.py` to customize:
```python
# Paths
UPLOAD_DIR = Path("data/uploads")
EXPORT_DIR = Path("exports")

# Similarity thresholds
TEXT_SIMILARITY_THRESHOLD = 0.75
IMAGE_SIMILARITY_THRESHOLD = 0.80

# Threat scoring thresholds
CRITICAL_THREAT_SCORE = 80
HIGH_THREAT_SCORE = 60
MEDIUM_THREAT_SCORE = 30

# Collection names
TEXT_COLLECTION = "text_memory"
IMAGE_COLLECTION = "image_memory"
VIDEO_COLLECTION = "video_memory"
```

---

## 🧪 Testing

### Run All Tests
```bash
python run_tests.py
```

### Run Specific Tests
```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# Specific test file
pytest tests/unit/test_validators.py -v
```

### Test Coverage
```bash
pytest tests/ --cov=core --cov-report=html
open htmlcov/index.html
```

### Manual Testing
```bash
# Quick functionality test
python quick_test.py

# UI page testing
streamlit run test_pages.py

# System diagnostic
python diagnostic_check.py
```

See `TESTING.md` for detailed testing documentation.

---

## 📦 Tech Stack

### Core Technologies

- **Python 3.8+** - Primary language
- **Streamlit 1.28+** - Web interface
- **Qdrant 1.7+** - Vector database
- **Sentence Transformers 2.2+** - Text embeddings
- **PyTorch 2.1+** - Deep learning backend
- **CLIP** - Image/video embeddings

### Key Libraries

- **Data Processing**
  - NumPy - Numerical operations
  - Pandas - Data manipulation
  
- **Visualization**
  - Matplotlib - Charts and graphs
  - NetworkX - Graph visualization

- **Export & Reporting**
  - ReportLab - Professional PDF generation
  - JSON/CSV - Standard data formats

- **Testing**
  - Pytest - Test framework
  - Pytest-cov - Coverage reporting

### System Requirements

- **OS:** Windows 10+, Linux, macOS
- **RAM:** 4GB minimum, 8GB recommended
- **Storage:** 2GB for Qdrant + data
- **Network:** Required for initial model downloads

---

## 🚀 Deployment Considerations

### Local Deployment

- Single-user setup with Streamlit
- Persistent Qdrant storage on disk
- Suitable for research and testing

### Production Deployment

**Recommended stack:**
- **Frontend:** Streamlit Cloud or custom server
- **Vector DB:** Qdrant Cloud or self-hosted cluster
- **Storage:** Cloud storage for uploads (S3, GCS)
- **Monitoring:** Application logs and metrics

**Scaling considerations:**
- Qdrant supports distributed deployment
- Horizontal scaling for ingestion workers
- CDN for static assets
- Database backup strategies

---

## 📖 Usage Examples

### Adding a Text Claim
```python
from core.narratives.narrative_manager import process_new_claim

narrative_id = process_new_claim(
    "Fake flood image viral on social media",
    {"year": 2024, "source": "twitter"}
)
print(f"Stored under: {narrative_id}")
```

### Searching for Similar Claims
```python
from core.memory.text_search import search_claims

results = search_claims("flood image misinformation", limit=5)
for result in results:
    print(f"Score: {result.score:.3f}")
    print(f"Claim: {result.payload['claim']}")
```

### Generating Trust Report
```python
from core.reports.trust_report import generate_trust_report

report = generate_trust_report("vaccine causes infertility")

print(f"Narrative: {report['narrative_id']}")
print(f"Occurrences: {report['occurrence_count']}")
print(f"Risk: {report['risk_level']}")
print(f"Insight: {report['insight']}")
```

### Exporting Data
```python
from core.exports.json_exporter import export_all_narratives_json
from core.narratives.narrative_explorer import get_all_narratives

narratives = get_all_narratives()
filepath = export_all_narratives_json(narratives)
print(f"Exported to: {filepath}")
```

---

## 🤝 Contributing

We welcome contributions! Areas of interest:

- **New modalities:** Audio, document analysis
- **ML improvements:** Better embeddings, threshold tuning
- **UI enhancements:** Visualizations, dashboards
- **Analytics:** New detection algorithms
- **Testing:** Test coverage expansion
- **Documentation:** Tutorials, examples

**Contribution guidelines:**
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit pull request with description

---

## 📄 License

This project is developed for research and educational purposes.

**Usage restrictions:**
- Not for commercial misinformation tracking without disclosure
- Must maintain ethical guidelines
- Attribute original work

---

## 🙏 Acknowledgments

**Technologies:**
- Qdrant team for the excellent vector database
- Hugging Face for Sentence Transformers
- OpenAI for CLIP embeddings
- Streamlit for the intuitive framework

**Inspiration:**
- Research on information ecosystems
- Fact-checking organizations
- Misinformation research community

---

## 📧 Contact & Support

**For questions, issues, or collaboration:**
- Open an issue on GitHub
- Check existing documentation
- Review TESTING.md for test guidance

**Reporting bugs:**
1. Check if issue already exists
2. Run `python diagnostic_check.py`
3. Include error logs and system info
4. Describe steps to reproduce

---

## 🔮 Future Roadmap

### Short-term (3-6 months)
- [ ] Audio ingestion support
- [ ] Multilingual embeddings
- [ ] Real-time API endpoints
- [ ] Advanced visualization dashboards
- [ ] User authentication

### Medium-term (6-12 months)
- [ ] Cross-platform entity resolution
- [ ] Influence network analysis
- [ ] Machine learning for threshold optimization
- [ ] Collaborative annotation tools
- [ ] Mobile application

### Long-term (12+ months)
- [ ] Distributed deployment architecture
- [ ] Real-time narrative tracking
- [ ] Integration with fact-checking APIs
- [ ] Browser extension
- [ ] Public narrative database (with privacy controls)

---

## 📚 Additional Resources

**Documentation:**
- `TESTING.md` - Comprehensive testing guide
- `core/config.py` - Configuration options
- `requirements.txt` - Dependency versions

**Scripts:**
- `quick_setup.py` - Initialize with demo data
- `quick_test.py` - Manual functionality test
- `diagnostic_check.py` - System health check
- `run_tests.py` - Automated test suite

**Examples:**
- Demo data in `quick_setup.py`
- Test cases in `tests/` directory
- UI examples in `test_pages.py`

---

## 🎯 Conclusion

SatyaAI demonstrates how multimodal vector memory can serve as long-term societal infrastructure rather than short-lived assistants.

By integrating:
- **Qdrant-powered retrieval** for persistent memory
- **Narrative intelligence** for pattern detection
- **Evidence-based outputs** for transparency
- **Advanced analytics** for insights

**SatyaAI enables historically grounded digital trust systems.**

The system transforms misinformation handling from reactive fact-checking into **proactive narrative intelligence**, providing decision-makers with the historical context needed to understand and respond to evolving information threats.

---

**Built with 🧠 by the SatyaAI Team**  
*Powered by Qdrant
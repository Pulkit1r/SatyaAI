# 🧠 SatyaAI — Digital Trust Memory System

A multimodal misinformation memory engine that remembers what gets repeated.

---

## What's the Problem?

Misinformation doesn't die after being debunked. It comes back during elections, disasters, and crises—often with small tweaks or reused images.

Examples:
- Old flood photos reshared as "breaking news"
- Debunked vaccine claims resurfacing every year
- Same political narratives recycled across platforms

Traditional fact-checkers treat each instance as new. **They have no memory.**

---

## What SatyaAI Does

SatyaAI is a long-term memory system for misinformation. It:

- **Remembers** claims, images, and videos over time
- **Detects** when narratives resurface (even years later)
- **Tracks** how misinformation evolves across platforms
- **Provides** evidence-based trust reports (not fact-checks)

Think of it as a searchable archive that connects the dots between related misinformation over months and years.

---

## How It Works

### Architecture

```
User Input (Text/Image/Video)
    ↓
Embedding Layer (Sentence Transformers + CLIP)
    ↓
Qdrant Vector Database (3 collections)
    ↓
Narrative Intelligence Engine
    ↓
Trust Reports + Analytics
```

### Multimodal Memory

**Text:** Semantic search using sentence embeddings (384-dim)  
**Images:** Visual similarity via CLIP embeddings (512-dim)  
**Video:** Frame-by-frame analysis and matching

Each memory stores:
- `narrative_id` - links related content across time/platforms
- `year` - when it appeared
- `source` - where it came from (twitter, facebook, etc.)
- `type` - text, image, or video_frame

### Smart Linking

When you add new content:
1. System searches for similar past content
2. If match found (>75% similarity) → links to existing narrative
3. If no match → creates new narrative ID
4. Stores with metadata for future retrieval

---

## Key Features

### 📊 Trust Reports
- Shows how many times a narrative appeared
- First seen vs. last seen dates
- Platform distribution
- Threat level (LOW/MEDIUM/HIGH/CRITICAL)
- Full timeline with similarity scores

### 🔍 Visual Search
- Upload an image, find past uses
- Detects reused/edited visuals
- Works even if cropped or resized

### 🎥 Video Analysis
- Extracts frames automatically
- Matches against historical video content
- Finds reused footage across different videos

### 📈 Analytics Dashboard
- Viral narrative detection
- Platform risk scoring
- Coordinated campaign identification
- Temporal patterns and trends

### 📤 Export Options
- JSON/CSV bulk exports
- Professional PDF reports
- Individual narrative downloads

### 💾 Backup System
- One-click database backup
- Restore with rollback protection
- Auto-cleanup (keeps last 10)

---

## Tech Stack

**Core:**
- Python 3.11
- Qdrant (vector database)
- Sentence Transformers (text embeddings)
- CLIP (image/video embeddings)
- Streamlit (web UI)

**Why Qdrant?**
- Handles high-dimensional vector search efficiently
- Persistent storage across sessions
- Rich metadata filtering
- Scales well with growing data

---

## Setup for Windows and Linux
```bash
# Clone the repository
git clone https://github.com/Pulkit1r/SatyaAI.git
cd SatyaAI

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate          # Linux
venv\Scripts\activate             # Windows PowerShell

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run ui/app.py
```

Opens at `http://localhost:8501`

## Setup for MAC(M1-M4)
```bash
# Clone the repository
git clone https://github.com/Pulkit1r/SatyaAI.git
cd SatyaAI

# Install Python 3.10 (required)
brew install python@3.10

# Create virtual environment using Python 3.10
/opt/homebrew/bin/python3.10 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade build tools
pip install --upgrade pip setuptools wheel

# Install core ML dependencies (explicitly pinned for stability)
pip install qdrant-client==1.7.0
pip install sentence-transformers==2.2.2
pip install transformers==4.30.2
pip install huggingface_hub==0.16.4

# Install remaining dependencies
pip install -r requirements.txt

# (Optional) Run diagnostics
python diagnostic_check.py

# Run the application
streamlit run ui/app.py
```

Opens at `http://localhost:8501`

---
---

## Quick Example

**Scenario:** Someone shares a "new" flood image on Twitter.

**What SatyaAI does:**
1. You upload the image
2. Searches visual memory
3. Finds 3 matches:
   - 2020: facebook (score: 0.92)
   - 2022: twitter (score: 0.88)
   - 2024: whatsapp (score: 0.85)
4. Shows this is a resurfacing narrative, not breaking news
5. Displays full timeline and threat assessment

**Output:**
- Narrative ID: NAR_flood_2024
- Status: RESURFACING (4-year lifespan)
- Risk Level: HIGH
- Platforms: 3 different sources

---

## Use Cases

**For Journalists:**
- Verify if a viral claim has history
- Trace narrative origins
- Get context before reporting

**For Researchers:**
- Study misinformation evolution
- Analyze platform dynamics
- Track long-term patterns

**For Government/NGOs:**
- Monitor recurring threats
- Identify coordinated campaigns
- Track public risk narratives

---

## What Makes This Different

**Traditional approach:**  
"Is this true or false?" → Answer disappears after the check.

**SatyaAI approach:**  
"Have we seen this before? When? Where? How did it change?" → Builds permanent memory.

**Key insight:** The problem isn't just individual false claims. It's recurring narratives that adapt and spread. You need memory to fight memory.

---

## Current Limitations

- English-optimized (multilingual support planned)
- Fixed similarity thresholds (active learning coming)
- Requires manual upload (API/automation planned)
- Limited to stored content (can't search the whole internet)

---

## Ethics & Responsibility

⚠️ **Important:**

SatyaAI does NOT:
- Declare content "true" or "false"
- Make automated decisions
- Label people or sources

It DOES:
- Show historical evidence
- Provide context and patterns
- Support human decision-making
- Maintain transparency on sources

**Human judgment is always required.**

---

## Configuration

Edit `core/config.py`:

```python
# Similarity thresholds
TEXT_SIMILARITY_THRESHOLD = 0.7
IMAGE_SIMILARITY_THRESHOLD = 0.75

# Threat scoring
CRITICAL_THREAT_SCORE = 75
HIGH_THREAT_SCORE = 50
MEDIUM_THREAT_SCORE = 25

# Paths
UPLOAD_DIR = Path("data/uploads")
```

---

## Project Structure

```
SatyaAI/
├── core/
│   ├── embeddings/      # Text/image/video embedding
    ├── backup/          3 Backup data
│   ├── memory/          # Storage and retrieval
│   ├── narratives/      # Intelligence engine
│   ├── reports/         # Trust report generation
│   ├── qdrant/          # Vector DB setup
    ├── utils            # Validation and error handling
    ├── analytics        # Advanced analytics engine
    ├── exports          # JSON/CSV/PDF exporters
    ├── graphs           # Network visualization
│   └── config.py        # Configuration
├── ui/
│   ├── app.py          # Main Streamlit app
│   └── modules/        # Export, analytics, backup
├── data/
│   ├── uploads/        # User uploads
│   └── backups/        # Database backups
├── qdrant_data/        # Vector database
└── requirements.txt
```

---

## Roadmap

**Next up:**
- [ ] Audio support (podcasts, voice messages)
- [ ] Real-time monitoring APIs
- [ ] Multilingual embeddings
- [ ] Browser extension
- [ ] Cross-platform entity resolution


## The Big Picture

Misinformation is a memory problem. It persists, evolves, and resurfaces.

SatyaAI gives society a memory system—so we stop treating every resurfacing narrative as something new.

Built for the long game, not just today's viral tweet.

---

**Built with 🧠 by the SatyaAI Team**  
*Powered by Qdrant vector search*

GitHub: [Pulkit1r/SatyaAI](https://github.com/Pulkit1r/SatyaAI)

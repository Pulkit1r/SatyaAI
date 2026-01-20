"""
Configuration file for SatyaAI
Complete configuration with all required constants
"""
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Application settings
APP_TITLE = "SatyaAI – Digital Trust Memory System"
APP_ICON = "🧠"

# ====== SIMILARITY THRESHOLDS ======
TEXT_SIMILARITY_THRESHOLD = 0.7  # Minimum cosine similarity for text matches
IMAGE_SIMILARITY_THRESHOLD = 0.75  # Minimum cosine similarity for image matches
VIDEO_SIMILARITY_THRESHOLD = 0.75  # Minimum cosine similarity for video frame matches

# ====== THREAT SCORING THRESHOLDS ======
CRITICAL_THREAT_SCORE = 75  # Score >= 75 is CRITICAL
HIGH_THREAT_SCORE = 50      # Score >= 50 is HIGH
MEDIUM_THREAT_SCORE = 25    # Score >= 25 is MEDIUM
# Below 25 is LOW

# File upload restrictions
ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.jfif', '.webp'}
ALLOWED_VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi'}
MAX_UPLOAD_SIZE_MB = 100  # Maximum file size in megabytes

# Embedding model settings
TEXT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"
IMAGE_EMBEDDING_MODEL = "clip-ViT-B-32"
TEXT_EMBEDDING_DIM = 384
IMAGE_EMBEDDING_DIM = 512

# Qdrant settings
QDRANT_PATH = "qdrant_data"
TEXT_COLLECTION = "text_memory"
IMAGE_COLLECTION = "image_memory"
VIDEO_COLLECTION = "video_memory"

# Video processing
DEFAULT_FRAME_EXTRACTION_RATE = 60  # Extract 1 frame every N frames

# Search settings
DEFAULT_SEARCH_LIMIT = 10
MAX_SEARCH_LIMIT = 50

# Narrative clustering
NARRATIVE_CLUSTER_THRESHOLD = 0.65  # Threshold for grouping into same narrative

# Risk calculation weights
RISK_WEIGHTS = {
    "occurrence_count": 0.3,
    "lifespan": 0.2,
    "recency": 0.2,
    "platform_diversity": 0.15,
    "multimodal": 0.15
}

# Narrative state thresholds
DORMANT_THRESHOLD_YEARS = 2  # Years of inactivity before marking as dormant
ACTIVE_MEMORY_THRESHOLD = 5  # Minimum memories to be considered actively spreading
RESURFACING_MIN_GAP = 1      # Minimum gap (years) to count as resurfacing

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(exist_ok=True)
"""
Central configuration for SatyaAI
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
EXPORT_DIR = BASE_DIR / "exports"
QDRANT_PATH = BASE_DIR / "qdrant_data"

# Create directories if they don't exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

# Embedding models
TEXT_MODEL = "all-MiniLM-L6-v2"
IMAGE_MODEL = "clip-ViT-B-32"

# Similarity thresholds
TEXT_SIMILARITY_THRESHOLD = 0.75
IMAGE_SIMILARITY_THRESHOLD = 0.80
VIDEO_SIMILARITY_THRESHOLD = 0.75

# Risk thresholds
HIGH_RISK_THRESHOLD = 8
MEDIUM_RISK_THRESHOLD = 4

# Threat level thresholds
CRITICAL_THREAT_SCORE = 70
HIGH_THREAT_SCORE = 50
MEDIUM_THREAT_SCORE = 30

# Collection names
TEXT_COLLECTION = "text_memory"
IMAGE_COLLECTION = "image_memory"
VIDEO_COLLECTION = "video_memory"

# Vector dimensions
TEXT_DIM = 384
IMAGE_DIM = 512
VIDEO_DIM = 512

# Video processing
VIDEO_FRAME_INTERVAL = 60  # Extract every 60th frame
MAX_VIDEO_FRAMES = 100     # Maximum frames to extract

# Upload limits
MAX_UPLOAD_SIZE_MB = 100
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.jfif'}
ALLOWED_VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi'}

# Search limits
DEFAULT_SEARCH_LIMIT = 5
MAX_SEARCH_LIMIT = 20

# UI Configuration
APP_TITLE = "SatyaAI — Digital Trust Memory System"
APP_ICON = "🧠"
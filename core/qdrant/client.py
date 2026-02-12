import os
from qdrant_client import QdrantClient

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

# Collection names
TEXT_COLLECTION = "text_memory"
IMAGE_COLLECTION = "image_memory"
VIDEO_COLLECTION = "video_memory"

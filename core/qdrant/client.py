from qdrant_client import QdrantClient

# Single persistent Qdrant engine
client = QdrantClient(path="qdrant_data")

# Collection names (logical memory partitions)
TEXT_COLLECTION = "text_memory"
IMAGE_COLLECTION = "image_memory"
VIDEO_COLLECTION = "video_memory"

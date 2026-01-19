from core.embeddings.video_processor import extract_frames
from core.memory.image_store import store_image


def store_video(video_path, metadata):
    frames = extract_frames(video_path)

    for f in frames:
        store_image(f, {
            "video_source": video_path,
            "type": "video_frame",
            **metadata
        })

    print("✅ Video stored as multimodal visual memory")

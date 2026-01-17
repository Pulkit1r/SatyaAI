from core.memory.image_store import store_image
from core.memory.image_search import search_images

store_image("data/images/image.png", {"year": 2022, "source": "twitter"})

results = search_images("data/images/image.png")

for r in results:
    print(r.payload, r.score)

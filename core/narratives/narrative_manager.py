import uuid
from core.memory.text_search import search_claims
from core.memory.text_store import store_claim
from core.memory.image_store import store_image
from core.memory.image_search import search_images


SIMILARITY_THRESHOLD = 0.75
IMAGE_SIMILARITY_THRESHOLD = 0.8

def process_new_claim(claim_text, metadata):

    results = search_claims(claim_text, limit=3)

    if results and results[0].score >= SIMILARITY_THRESHOLD:
        narrative_id = results[0].payload.get("narrative_id")

        if not narrative_id:
            narrative_id = "NAR_" + str(uuid.uuid4())[:8]

        print("🔁 Linked to existing narrative:", narrative_id)

    else:
        narrative_id = "NAR_" + str(uuid.uuid4())[:8]
        print("🆕 New narrative created:", narrative_id)

    metadata["narrative_id"] = narrative_id
    store_claim(claim_text, metadata)

    return narrative_id



def process_new_image(image_path, metadata):

    results = search_images(image_path, limit=3)

    if results and results[0].score >= 0.8:
        narrative_id = results[0].payload.get("narrative_id")
        print("🔁 Image linked to narrative:", narrative_id)
    else:
        import uuid
        narrative_id = "NAR_" + str(uuid.uuid4())[:8]
        print("🆕 New visual narrative created:", narrative_id)

    metadata["narrative_id"] = narrative_id
    store_image(image_path, metadata)

    return narrative_id

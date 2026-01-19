"""
Narrative management - linking claims to narratives
"""
import uuid
from core.memory.text_search import search_claims
from core.memory.text_store import store_claim
from core.memory.image_store import store_image
from core.memory.image_search import search_images
from core.config import TEXT_SIMILARITY_THRESHOLD, IMAGE_SIMILARITY_THRESHOLD


def _new_narrative_id():
    """Generate a new narrative ID"""
    return "NAR_" + str(uuid.uuid4())[:8]


def process_new_claim(claim_text, metadata):
    """
    Process a new text claim.
    Links to existing narrative or creates new one.
    
    Args:
        claim_text (str): The claim text
        metadata (dict): Metadata including year, source, etc.
        
    Returns:
        str: Narrative ID
    """
    # Search for similar claims
    results = search_claims(claim_text, limit=3)

    if results and results[0].score >= TEXT_SIMILARITY_THRESHOLD:
        # Link to existing narrative
        narrative_id = results[0].payload.get("narrative_id", _new_narrative_id())
        metadata["reinforced"] = True
        print(f"🔁 Reinforced narrative: {narrative_id}")
    else:
        # Create new narrative
        narrative_id = _new_narrative_id()
        metadata["reinforced"] = False
        metadata["created_at"] = str(uuid.uuid1())
        print(f"🆕 New narrative created: {narrative_id}")

    # Store the claim
    metadata["narrative_id"] = narrative_id
    metadata["type"] = "text"
    store_claim(claim_text, metadata)

    return narrative_id


def process_new_image(image_path, metadata):
    """
    Process a new image.
    Links to existing narrative or creates new one.
    
    Args:
        image_path (str): Path to the image file
        metadata (dict): Metadata including year, source, etc.
        
    Returns:
        str: Narrative ID
    """
    # Search for similar images
    results = search_images(image_path, limit=3)

    if results and results[0].score >= IMAGE_SIMILARITY_THRESHOLD:
        # Link to existing narrative
        narrative_id = results[0].payload.get("narrative_id", _new_narrative_id())
        metadata["reinforced"] = True
        print(f"🔁 Visual narrative reinforced: {narrative_id}")
    else:
        # Create new narrative
        narrative_id = _new_narrative_id()
        metadata["reinforced"] = False
        print(f"🆕 New visual narrative created: {narrative_id}")

    # Store the image
    metadata["narrative_id"] = narrative_id
    metadata["type"] = "image"
    store_image(image_path, metadata)

    return narrative_id
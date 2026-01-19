from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_drift(origin_text, new_text, last_text=None):
    emb1 = model.encode(origin_text, convert_to_tensor=True)
    emb2 = model.encode(new_text, convert_to_tensor=True)

    drift_from_origin = 1 - util.cos_sim(emb1, emb2).item()

    drift_from_last = None
    if last_text:
        emb3 = model.encode(last_text, convert_to_tensor=True)
        drift_from_last = 1 - util.cos_sim(emb3, emb2).item()

    return round(drift_from_origin, 3), round(drift_from_last, 3) if drift_from_last else None

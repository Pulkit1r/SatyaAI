from core.embeddings.text_embedder import embed_text

v1 = embed_text("This is fake news about floods")
v2 = embed_text("Flood related misinformation")

print(len(v1))
print(v1[:10])

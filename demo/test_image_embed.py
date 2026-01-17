from core.embeddings.image_embedder import embed_image

vec = embed_image("data/images/test.jpg")
print(len(vec))
print(vec[:10])
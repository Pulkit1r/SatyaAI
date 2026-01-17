from sentence_transformers import SentenceTransformer
from PIL import Image
import streamlit as st

@st.cache_resource
def load_model():
    return SentenceTransformer("clip-ViT-B-32")

model = load_model()

def embed_image(image_path):
    image = Image.open(image_path).convert("RGB")
    vector = model.encode(image)
    return vector.tolist()

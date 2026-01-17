from sentence_transformers import SentenceTransformer
import streamlit as st

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

def embed_text(text):
    return model.encode(text).tolist()

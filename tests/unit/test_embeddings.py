"""
Test embedding generation
"""
import pytest
import numpy as np
from core.embeddings.text_embedder import embed_text
from core.embeddings.image_embedder import embed_image
from core.config import TEXT_DIM, IMAGE_DIM


class TestTextEmbeddings:
    """Test text embedding generation"""
    
    def test_embed_text_returns_list(self):
        """Test that embedding returns a list"""
        result = embed_text("Test claim")
        assert isinstance(result, list)
    
    def test_embed_text_correct_dimension(self):
        """Test embedding has correct dimension"""
        result = embed_text("Test claim")
        assert len(result) == TEXT_DIM
    
    def test_embed_text_returns_floats(self):
        """Test embedding contains float values"""
        result = embed_text("Test claim")
        assert all(isinstance(x, (float, np.float32, np.float64)) for x in result)
    
    def test_similar_texts_similar_embeddings(self):
        """Test similar texts produce similar embeddings"""
        emb1 = np.array(embed_text("Fake news about floods"))
        emb2 = np.array(embed_text("False information about flooding"))
        emb3 = np.array(embed_text("Recipe for chocolate cake"))
        
        # Cosine similarity
        sim_12 = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        sim_13 = np.dot(emb1, emb3) / (np.linalg.norm(emb1) * np.linalg.norm(emb3))
        
        # Similar texts should be more similar than dissimilar texts
        assert sim_12 > sim_13
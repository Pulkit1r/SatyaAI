"""
Pytest configuration and fixtures
"""
import pytest
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

@pytest.fixture
def sample_claim():
    """Sample claim for testing"""
    return {
        "claim": "This is a test misinformation claim about floods",
        "year": 2024,
        "source": "test_platform"
    }


@pytest.fixture
def sample_memories():
    """Sample memories for narrative testing"""
    return [
        {"year": 2020, "source": "twitter", "type": "text", "claim": "Test claim 1"},
        {"year": 2022, "source": "facebook", "type": "text", "claim": "Test claim 2"},
        {"year": 2024, "source": "whatsapp", "type": "text", "claim": "Test claim 3"},
    ]


@pytest.fixture
def sample_narrative_stats():
    """Sample narrative statistics"""
    return {
        "first_seen": 2020,
        "last_seen": 2024,
        "lifespan": 4,
        "sources": ["twitter", "facebook", "whatsapp"],
        "modalities": ["text"],
        "mutation_score": 3,
        "resurfacing": True,
        "memory_strength": 85,
        "state": "ACTIVE",
        "threat_level": "MEDIUM",
        "strength": 75
    }
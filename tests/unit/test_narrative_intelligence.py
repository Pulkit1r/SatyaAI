"""
Test narrative intelligence computations
"""
import pytest
from core.narratives.narrative_intelligence import compute_narrative_stats


class TestNarrativeStats:
    """Test narrative statistics computation"""
    
    def test_basic_stats(self, sample_memories):
        """Test basic statistics computation"""
        stats = compute_narrative_stats(sample_memories)
        
        assert stats["first_seen"] == 2020
        assert stats["last_seen"] == 2024
        assert stats["lifespan"] == 4
    
    def test_resurfacing_detection(self, sample_memories):
        """Test resurfacing detection"""
        stats = compute_narrative_stats(sample_memories)
        # 3+ memories with 1+ year lifespan = resurfacing
        assert stats["resurfacing"] == True
    
    def test_source_counting(self, sample_memories):
        """Test source counting"""
        stats = compute_narrative_stats(sample_memories)
        assert len(stats["sources"]) == 3
        assert "twitter" in stats["sources"]
        assert "facebook" in stats["sources"]
        assert "whatsapp" in stats["sources"]
    
    def test_modality_tracking(self, sample_memories):
        """Test modality tracking"""
        stats = compute_narrative_stats(sample_memories)
        assert "text" in stats["modalities"]
    
    def test_threat_level_computation(self, sample_memories):
        """Test threat level is computed"""
        stats = compute_narrative_stats(sample_memories)
        assert "threat_level" in stats
        assert stats["threat_level"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    
    def test_strength_computation(self, sample_memories):
        """Test narrative strength is computed"""
        stats = compute_narrative_stats(sample_memories)
        assert "strength" in stats
        assert isinstance(stats["strength"], (int, float))
        assert 0 <= stats["strength"] <= 100
    
    def test_memory_strength_computation(self, sample_memories):
        """Test memory strength is computed"""
        stats = compute_narrative_stats(sample_memories)
        assert "memory_strength" in stats
        assert isinstance(stats["memory_strength"], (int, float))
        assert stats["memory_strength"] >= 1
    
    def test_state_computation(self, sample_memories):
        """Test narrative state is computed"""
        stats = compute_narrative_stats(sample_memories)
        assert "state" in stats
        assert stats["state"] in ["NEW", "ACTIVE", "DORMANT", "RESURFACED"]
    
    def test_temporal_patterns(self, sample_memories):
        """Test temporal patterns are computed"""
        stats = compute_narrative_stats(sample_memories)
        assert "temporal_patterns" in stats
        assert "activity_years" in stats["temporal_patterns"]
        assert "resurfacing_gaps" in stats["temporal_patterns"]
    
    def test_empty_memories(self):
        """Test with empty memories list"""
        stats = compute_narrative_stats([])
        assert stats["first_seen"] is None
        assert stats["last_seen"] is None
        assert stats["lifespan"] == 0
        assert stats["resurfacing"] == False
    
    def test_single_memory(self):
        """Test with single memory"""
        single_memory = [
            {"year": 2024, "source": "twitter", "type": "text", "claim": "Test claim"}
        ]
        stats = compute_narrative_stats(single_memory)
        
        assert stats["first_seen"] == 2024
        assert stats["last_seen"] == 2024
        assert stats["lifespan"] == 0
        assert stats["resurfacing"] == False
        assert len(stats["sources"]) == 1
    
    def test_mutation_score(self, sample_memories):
        """Test mutation score calculation"""
        stats = compute_narrative_stats(sample_memories)
        # Mutation score = unique claims
        assert stats["mutation_score"] >= 0
    
    def test_high_threat_narrative(self):
        """Test high threat narrative detection"""
        high_threat_memories = [
            {"year": 2020, "source": "twitter", "type": "text", "claim": "Claim 1"},
            {"year": 2021, "source": "facebook", "type": "text", "claim": "Claim 2"},
            {"year": 2022, "source": "whatsapp", "type": "text", "claim": "Claim 3"},
            {"year": 2023, "source": "instagram", "type": "text", "claim": "Claim 4"},
            {"year": 2024, "source": "telegram", "type": "text", "claim": "Claim 5"},
        ]
        stats = compute_narrative_stats(high_threat_memories)
        
        # Should have high threat due to multiple sources, long lifespan, resurfacing
        assert stats["threat_level"] in ["HIGH", "CRITICAL"]
    
    def test_low_threat_narrative(self):
        """Test low threat narrative detection"""
        low_threat_memories = [
            {"year": 2024, "source": "twitter", "type": "text", "claim": "Single claim"}
        ]
        stats = compute_narrative_stats(low_threat_memories)
        
        # Single occurrence should be low threat
        assert stats["threat_level"] == "LOW"
    
    def test_missing_year_handling(self):
        """Test handling of memories without year"""
        memories_no_year = [
            {"source": "twitter", "type": "text", "claim": "Claim without year"}
        ]
        stats = compute_narrative_stats(memories_no_year)
        
        assert stats["first_seen"] is None
        assert stats["last_seen"] is None
        assert stats["lifespan"] == 0
    
    def test_missing_source_handling(self):
        """Test handling of memories without source"""
        memories_no_source = [
            {"year": 2024, "type": "text", "claim": "Claim without source"}
        ]
        stats = compute_narrative_stats(memories_no_source)
        
        assert len(stats["sources"]) == 0
    
    def test_mixed_modalities(self):
        """Test with mixed content types"""
        mixed_memories = [
            {"year": 2020, "source": "twitter", "type": "text", "claim": "Text claim"},
            {"year": 2021, "source": "facebook", "type": "image", "path": "/path/image.jpg"},
            {"year": 2022, "source": "youtube", "type": "video_frame", "path": "/path/frame.jpg"},
        ]
        stats = compute_narrative_stats(mixed_memories)
        
        assert len(stats["modalities"]) == 3
        assert "text" in stats["modalities"]
        assert "image" in stats["modalities"]
        assert "video_frame" in stats["modalities"]


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_very_old_narrative(self):
        """Test narrative from very old year"""
        old_memories = [
            {"year": 1950, "source": "archive", "type": "text", "claim": "Old claim"}
        ]
        stats = compute_narrative_stats(old_memories)
        
        assert stats["first_seen"] == 1950
        assert stats["lifespan"] == 0
    
    def test_future_year(self):
        """Test narrative with future year (edge case)"""
        future_memories = [
            {"year": 2030, "source": "test", "type": "text", "claim": "Future claim"}
        ]
        stats = compute_narrative_stats(future_memories)
        
        assert stats["first_seen"] == 2030
    
    def test_duplicate_sources(self):
        """Test multiple entries from same source"""
        duplicate_source_memories = [
            {"year": 2020, "source": "twitter", "type": "text", "claim": "Claim 1"},
            {"year": 2021, "source": "twitter", "type": "text", "claim": "Claim 2"},
            {"year": 2022, "source": "twitter", "type": "text", "claim": "Claim 3"},
        ]
        stats = compute_narrative_stats(duplicate_source_memories)
        
        # Should still count as one unique source
        assert len(stats["sources"]) == 1
        assert "twitter" in stats["sources"]
    
    def test_large_narrative(self):
        """Test narrative with many memories"""
        large_memories = [
            {"year": 2020 + i, "source": f"source_{i}", "type": "text", "claim": f"Claim {i}"}
            for i in range(20)
        ]
        stats = compute_narrative_stats(large_memories)
        
        assert len(stats["sources"]) == 20
        assert stats["lifespan"] == 19
        assert stats["resurfacing"] == True


class TestThreatLevelLogic:
    """Test threat level calculation logic"""
    
    def test_critical_threat_criteria(self):
        """Test criteria for CRITICAL threat level"""
        # Many sources, long lifespan, many mutations, resurfacing
        critical_memories = [
            {"year": 2020, "source": f"source_{i}", "type": "text", "claim": f"Claim {i}"}
            for i in range(5)
        ]
        stats = compute_narrative_stats(critical_memories)
        
        # With 5 sources, resurfacing, mutations, should get high threat score
        assert stats["threat_score"] >= 50
    
    def test_threat_score_components(self):
        """Test individual components of threat score"""
        memories = [
            {"year": 2020, "source": "twitter", "type": "text", "claim": "Claim 1"},
            {"year": 2021, "source": "facebook", "type": "text", "claim": "Claim 2"},
            {"year": 2024, "source": "whatsapp", "type": "text", "claim": "Claim 3"},
        ]
        stats = compute_narrative_stats(memories)
        
        # Has: resurfacing (30), 3 sources (20), mutations (15), lifespan 4 (25)
        # Total should be around 90
        assert stats["threat_score"] > 0
        assert "threat_level" in stats


class TestStrengthCalculation:
    """Test narrative strength calculation"""
    
    def test_strength_increases_with_frequency(self):
        """Test strength increases with more occurrences"""
        few_memories = [
            {"year": 2024, "source": "twitter", "type": "text", "claim": "Claim"}
        ]
        many_memories = [
            {"year": 2024, "source": "twitter", "type": "text", "claim": f"Claim {i}"}
            for i in range(5)
        ]
        
        stats_few = compute_narrative_stats(few_memories)
        stats_many = compute_narrative_stats(many_memories)
        
        assert stats_many["strength"] > stats_few["strength"]
    
    def test_strength_bounded_by_100(self):
        """Test strength never exceeds 100"""
        massive_memories = [
            {"year": 2024, "source": f"source_{i}", "type": "text", "claim": f"Claim {i}"}
            for i in range(50)
        ]
        stats = compute_narrative_stats(massive_memories)
        
        assert stats["strength"] <= 100
"""
Test temporal pattern detection
"""
import pytest
from core.narratives.temporal_engine import compute_temporal_patterns


class TestTemporalPatterns:
    """Test temporal pattern computation"""
    
    def test_basic_temporal_pattern(self):
        """Test basic temporal pattern detection"""
        memories = [
            {"year": 2020},
            {"year": 2022},
            {"year": 2024}
        ]
        patterns = compute_temporal_patterns(memories)
        
        assert patterns["activity_years"] == [2020, 2022, 2024]
        assert len(patterns["resurfacing_gaps"]) == 2
        assert patterns["seasonal"] == True
    
    def test_single_year(self):
        """Test with single year"""
        memories = [{"year": 2024}]
        patterns = compute_temporal_patterns(memories)
        
        assert patterns["activity_years"] == [2024]
        assert patterns["resurfacing_gaps"] == []
        assert patterns["seasonal"] == False
    
    def test_consecutive_years(self):
        """Test consecutive years detection"""
        memories = [
            {"year": 2020},
            {"year": 2021},
            {"year": 2022}
        ]
        patterns = compute_temporal_patterns(memories)
        
        assert patterns["seasonal"] == True
        assert all(gap >= 1 for gap in patterns["resurfacing_gaps"])
"""
Test risk calculation engine
"""
import pytest
from core.reports.risk_engine import calculate_risk


class TestRiskCalculation:
    """Test risk score calculation"""
    
    def test_high_risk(self):
        """Test high risk detection"""
        report = {
            "occurrence_count": 5,
            "sources_seen": ["twitter", "facebook", "whatsapp"]
        }
        risk = calculate_risk(report)
        assert risk["risk_level"] == "HIGH"
        assert risk["risk_score"] >= 8
    
    def test_medium_risk(self):
        """Test medium risk detection"""
        report = {
            "occurrence_count": 2,
            "sources_seen": ["twitter", "facebook"]
        }
        risk = calculate_risk(report)
        assert risk["risk_level"] == "MEDIUM"
        assert risk["risk_score"] >= 4
    
    def test_low_risk(self):
        """Test low risk detection"""
        report = {
            "occurrence_count": 1,
            "sources_seen": ["twitter"]
        }
        risk = calculate_risk(report)
        assert risk["risk_level"] == "LOW"
        assert risk["risk_score"] < 4
    
    def test_no_sources(self):
        """Test with no sources"""
        report = {
            "occurrence_count": 3,
            "sources_seen": []
        }
        risk = calculate_risk(report)
        assert risk["risk_score"] == 0
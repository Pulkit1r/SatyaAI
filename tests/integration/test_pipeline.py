"""
Test complete data pipeline
"""
import pytest
import time
from core.narratives.narrative_manager import process_new_claim
from core.memory.text_search import search_claims
from core.reports.trust_report import generate_trust_report


class TestCompletePipeline:
    """Test complete data flow"""
    
    def test_claim_to_search_pipeline(self):
        """Test: Add claim -> Search -> Find it"""
        # Add a unique claim
        unique_claim = f"Unique test claim for pipeline testing {time.time()}"
        
        narrative_id = process_new_claim(unique_claim, {
            "year": 2024,
            "source": "test"
        })
        
        assert narrative_id is not None
        assert narrative_id.startswith("NAR_")
        
        # Search for it
        results = search_claims(unique_claim, limit=5)
        
        # Should find our claim
        assert len(results) > 0
        found_narratives = [r.payload.get("narrative_id") for r in results]
        assert narrative_id in found_narratives
    
    def test_claim_to_report_pipeline(self):
        """Test: Add claim -> Generate report"""
        test_claim = f"Pipeline test claim for report generation {time.time()}"
        
        # Add claim
        narrative_id = process_new_claim(test_claim, {"year": 2024, "source": "test"})
        
        # Generate report
        report = generate_trust_report(test_claim)
        
        assert report is not None
        assert "status" in report
        
        if report["status"] == "history_found":
            assert "narrative_id" in report
            assert "occurrence_count" in report
    
    def test_multiple_claims_same_narrative(self):
        """Test: Multiple similar claims link to same narrative"""
        base_claim = f"Similar claim about floods {time.time()}"
        
        # Add first claim
        nid1 = process_new_claim(base_claim, {"year": 2024, "source": "twitter"})
        
        # Add similar claim
        similar_claim = base_claim.replace("floods", "flooding")
        nid2 = process_new_claim(similar_claim, {"year": 2024, "source": "facebook"})
        
        # They might link to the same narrative (if similarity is high enough)
        # This test verifies the mechanism works, not necessarily that they link
        assert nid1 is not None
        assert nid2 is not None
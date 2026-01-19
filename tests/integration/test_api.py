"""
Test API endpoints (requires API server running)
"""
import pytest
import requests
import time

BASE_URL = "http://localhost:8000"


@pytest.fixture
def api_available():
    """Check if API is available"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        pytest.skip("API server not running. Start it with: python api/run.py")


class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_root_endpoint(self, api_available):
        """Test root endpoint"""
        response = requests.get(BASE_URL)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "endpoints" in data
    
    def test_health_check(self, api_available):
        """Test health check endpoint"""
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_add_claim(self, api_available):
        """Test adding a claim"""
        payload = {
            "claim": f"Test claim for API integration test {time.time()}",
            "year": 2024,
            "source": "test_api"
        }
        response = requests.post(f"{BASE_URL}/claims", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "narrative_id" in data
        assert "reinforced" in data
    
    def test_invalid_claim_too_short(self, api_available):
        """Test adding invalid claim (too short)"""
        payload = {
            "claim": "Short",
            "year": 2024,
            "source": "test"
        }
        response = requests.post(f"{BASE_URL}/claims", json=payload)
        assert response.status_code in [400, 422]  # Bad request or validation error
    
    def test_search_claims(self, api_available):
        """Test searching claims"""
        payload = {
            "query": "test claim",
            "limit": 5
        }
        response = requests.post(f"{BASE_URL}/search/claims", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "results_count" in data
        assert isinstance(data["results"], list)
    
    def test_get_stats(self, api_available):
        """Test getting system stats"""
        response = requests.get(f"{BASE_URL}/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_narratives" in data
        assert "total_memories" in data
    
    def test_get_narratives(self, api_available):
        """Test getting all narratives"""
        response = requests.get(f"{BASE_URL}/narratives")
        assert response.status_code == 200
        data = response.json()
        assert "total_narratives" in data
        assert "narratives" in data
    
    def test_trust_report(self, api_available):
        """Test generating trust report"""
        payload = {
            "query": "test claim",
            "limit": 10
        }
        response = requests.post(f"{BASE_URL}/reports/trust", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
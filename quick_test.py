"""
Quick test script for manual testing
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.narratives.narrative_manager import process_new_claim
from core.memory.text_search import search_claims
from core.reports.trust_report import generate_trust_report


def test_basic_flow():
    """Test basic flow manually"""
    print("🧪 Testing Basic SatyaAI Flow")
    print("=" * 60)
    
    # Test 1: Add a claim
    print("\n1️⃣ Adding a test claim...")
    claim = "Test claim about fake news for manual testing"
    narrative_id = process_new_claim(claim, {"year": 2024, "source": "test"})
    print(f"   ✅ Claim added. Narrative ID: {narrative_id}")
    
    # Test 2: Search for the claim
    print("\n2️⃣ Searching for similar claims...")
    results = search_claims(claim, limit=3)
    print(f"   ✅ Found {len(results)} similar claims")
    for i, r in enumerate(results, 1):
        print(f"   {i}. Score: {r.score:.3f} | {r.payload.get('claim', 'N/A')[:50]}")
    
    # Test 3: Generate trust report
    print("\n3️⃣ Generating trust report...")
    report = generate_trust_report(claim)
    print(f"   ✅ Report status: {report.get('status')}")
    if report.get('status') == 'history_found':
        print(f"   📊 Occurrences: {report.get('occurrence_count')}")
        print(f"   ⚠️  Risk level: {report.get('risk_level', 'N/A')}")
    
    print("\n" + "=" * 60)
    print("✅ All manual tests completed successfully!")


if __name__ == "__main__":
    try:
        test_basic_flow()
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
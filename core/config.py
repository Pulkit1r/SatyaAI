"""
Test configuration on different platforms
"""
import platform
from core.config import *

def test_config():
    """Test that config works correctly"""
    
    print(f"\n{'='*60}")
    print(f"Testing SatyaAI Config on {PLATFORM}")
    print(f"{'='*60}\n")
    
    # Test 1: Directories exist
    print("✓ Testing directory creation...")
    for dir_path in [DATA_DIR, UPLOAD_DIR, BACKUP_DIR, QDRANT_DIR]:
        assert dir_path.exists(), f"Directory not created: {dir_path}"
        print(f"  ✅ {dir_path.name}")
    
    # Test 2: Paths are platform-agnostic
    print("\n✓ Testing path handling...")
    test_file = get_upload_path("test.jpg")
    assert isinstance(test_file, Path), "Should return Path object"
    print(f"  ✅ Upload path: {test_file}")
    
    # Test 3: Platform detection
    print("\n✓ Testing platform detection...")
    print(f"  Platform: {PLATFORM}")
    print(f"  Is Windows: {IS_WINDOWS}")
    print(f"  Is Mac: {IS_MAC}")
    print(f"  Is Linux: {IS_LINUX}")
    
    # Test 4: Environment variables
    print("\n✓ Testing environment variables...")
    print(f"  Qdrant Host: {QDRANT_HOST}")
    print(f"  Qdrant Port: {QDRANT_PORT}")
    
    # Test 5: Model cache
    print("\n✓ Testing model cache...")
    assert MODEL_CACHE_DIR.exists(), "Model cache not created"
    print(f"  ✅ Cache: {MODEL_CACHE_DIR}")
    
    print(f"\n{'='*60}")
    print(f"✅ All tests passed on {PLATFORM}!")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    test_config()
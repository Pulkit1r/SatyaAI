"""
Run all tests
"""
import pytest
import sys

def main():
    """Run pytest with coverage"""
    print("=" * 60)
    print("🧪 Running SatyaAI Test Suite")
    print("=" * 60)
    print()
    
    # Run tests with various options
    args = [
        "tests/",
        "-v",                    # Verbose output
        "--tb=short",           # Short traceback format
        "--color=yes",          # Colored output
        "-s",                   # Don't capture output (shows print statements)
    ]
    
    # Add coverage if pytest-cov is installed
    try:
        import pytest_cov
        args.extend([
            "--cov=core",           # Coverage for core module
            "--cov-report=term",    # Terminal coverage report
            "--cov-report=html",    # HTML coverage report
        ])
        print("📊 Coverage reporting enabled")
        print()
    except ImportError:
        print("ℹ️  Install pytest-cov for coverage reports: pip install pytest-cov")
        print()
    
    # Run tests
    exit_code = pytest.main(args)
    
    print()
    print("=" * 60)
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed")
    print("=" * 60)
    
    if 'pytest_cov' in sys.modules:
        print()
        print("📊 HTML coverage report generated at: htmlcov/index.html")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
"""
Launch the SatyaAI API server
"""
import uvicorn
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    """Launch the FastAPI server"""
    print("=" * 60)
    print("🚀 Starting SatyaAI API Server")
    print("=" * 60)
    print(f"\n📍 API Server: http://localhost:8000")
    print(f"📚 Documentation (Swagger): http://localhost:8000/docs")
    print(f"📖 Documentation (ReDoc): http://localhost:8000/redoc")
    print(f"❤️  Health Check: http://localhost:8000/health")
    print(f"📊 Statistics: http://localhost:8000/stats")
    print("\n⌨️  Press Ctrl+C to stop the server\n")
    print("=" * 60)
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes during development
        log_level="info"
    )


if __name__ == "__main__":
    main()
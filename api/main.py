"""
Main FastAPI application for SatyaAI
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import routers
from api.routes import claims, images, search, reports, narratives, stats
from api.models.schemas import HealthResponse, ErrorResponse

# Create FastAPI app
app = FastAPI(
    title="SatyaAI API",
    description="Digital Trust Memory System - REST API for narrative intelligence and misinformation tracking",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware - Allow all origins (restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: ["https://yourdomain.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all uncaught exceptions"""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_type": type(exc).__name__,
            "timestamp": datetime.now().isoformat()
        }
    )


# Include routers
app.include_router(claims.router)
app.include_router(images.router)
app.include_router(search.router)
app.include_router(reports.router)
app.include_router(narratives.router)
app.include_router(stats.router)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """API root endpoint with available endpoints information"""
    return {
        "message": "🧠 SatyaAI Digital Trust Memory API",
        "version": "1.0.0",
        "status": "active",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc"
        },
        "endpoints": {
            "health": "GET /health",
            "stats": "GET /stats",
            "claims": {
                "add": "POST /claims"
            },
            "images": {
                "upload": "POST /images"
            },
            "search": {
                "claims": "POST /search/claims"
            },
            "reports": {
                "trust_report": "POST /reports/trust"
            },
            "narratives": {
                "list": "GET /narratives",
                "detail": "GET /narratives/{narrative_id}"
            }
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify system status.
    
    Returns:
    - Status of the system
    - Qdrant connection status
    - Number of narratives
    """
    try:
        from core.narratives.narrative_explorer import get_all_narratives
        
        narratives = get_all_narratives(limit=1)
        
        return {
            "status": "healthy",
            "qdrant": "connected",
            "narratives_count": len(narratives),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "qdrant": "disconnected",
                "narratives_count": 0,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
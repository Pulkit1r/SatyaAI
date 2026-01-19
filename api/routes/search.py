"""
Search-related API endpoints
"""
from fastapi import APIRouter, HTTPException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from api.models.schemas import SearchQuery, SearchResponse, SearchResult
from core.memory.text_search import search_claims

router = APIRouter(prefix="/search", tags=["Search"])


@router.post("/claims", response_model=SearchResponse)
async def search_claims_endpoint(query: SearchQuery):
    """
    Search for similar claims in the memory system.
    
    - **query**: Search query text
    - **limit**: Maximum number of results (1-50, default: 5)
    
    Returns matching claims with similarity scores
    """
    try:
        results = search_claims(query.query, limit=query.limit)
        
        search_results = [
            SearchResult(
                score=round(r.score, 3),
                narrative_id=r.payload.get("narrative_id"),
                claim=r.payload.get("claim"),
                year=r.payload.get("year"),
                source=r.payload.get("source"),
                type=r.payload.get("type")
            )
            for r in results
        ]
        
        return SearchResponse(
            query=query.query,
            results_count=len(search_results),
            results=search_results
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
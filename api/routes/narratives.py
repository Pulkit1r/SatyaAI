"""
Narrative-related API endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.narratives.narrative_explorer import get_all_narratives

router = APIRouter(prefix="/narratives", tags=["Narratives"])


@router.get("")
async def get_all_narratives_endpoint(limit: int = 1000) -> Dict[str, Any]:
    """
    Get all narratives in the system.
    
    - **limit**: Maximum number of records per collection (default: 1000)
    
    Returns summary of all narratives
    """
    try:
        narratives = get_all_narratives(limit=limit)
        
        summary = {}
        for nid, memories in narratives.items():
            years = [m.get('year') for m in memories if m.get('year')]
            sources = set(m.get('source') for m in memories if m.get('source'))
            
            summary[nid] = {
                "memory_count": len(memories),
                "first_seen": min(years) if years else None,
                "last_seen": max(years) if years else None,
                "sources": list(sources),
                "modalities": list(set(m.get('type') for m in memories if m.get('type')))
            }
        
        return {
            "total_narratives": len(narratives),
            "narratives": summary
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{narrative_id}")
async def get_narrative_detail(narrative_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific narrative.
    
    - **narrative_id**: The narrative ID to retrieve
    
    Returns all memories associated with this narrative
    """
    try:
        all_narratives = get_all_narratives()
        
        if narrative_id not in all_narratives:
            raise HTTPException(status_code=404, detail="Narrative not found")
        
        memories = all_narratives[narrative_id]
        
        return {
            "narrative_id": narrative_id,
            "total_memories": len(memories),
            "memories": memories
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
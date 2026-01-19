"""
Statistics and analytics API endpoints
"""
from fastapi import APIRouter, HTTPException
from collections import Counter
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.narratives.narrative_explorer import get_all_narratives

router = APIRouter(prefix="/stats", tags=["Statistics"])


@router.get("")
async def get_system_stats():
    """
    Get overall system statistics.
    
    Returns:
    - Total narratives and memories
    - Distribution by source, modality, year
    - Average memories per narrative
    """
    try:
        narratives = get_all_narratives()
        
        if not narratives:
            return {
                "total_narratives": 0,
                "total_memories": 0,
                "message": "No data in system yet"
            }
        
        total_memories = sum(len(v) for v in narratives.values())
        
        all_sources = []
        all_modalities = []
        all_years = []
        
        for memories in narratives.values():
            for m in memories:
                if m.get('source'):
                    all_sources.append(m['source'])
                if m.get('type'):
                    all_modalities.append(m['type'])
                if m.get('year'):
                    all_years.append(m['year'])
        
        return {
            "total_narratives": len(narratives),
            "total_memories": total_memories,
            "average_memories_per_narrative": round(total_memories / len(narratives), 2),
            "source_distribution": dict(Counter(all_sources).most_common()),
            "modality_distribution": dict(Counter(all_modalities)),
            "year_distribution": dict(sorted(Counter(all_years).items()))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
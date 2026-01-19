"""
Report generation API endpoints
"""
from fastapi import APIRouter, HTTPException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from api.models.schemas import SearchQuery
from core.reports.trust_report import generate_trust_report

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("/trust")
async def generate_trust_report_endpoint(query: SearchQuery):
    """
    Generate a comprehensive trust report for a claim.
    
    - **query**: Claim or query to analyze
    - **limit**: Search depth (default: 10)
    
    Returns:
    - Complete narrative history
    - Risk assessment
    - Timeline of occurrences
    - Platform distribution
    - Intelligence metrics
    """
    try:
        report = generate_trust_report(query.query)
        return report
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
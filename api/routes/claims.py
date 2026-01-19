"""
Claims-related API endpoints
"""
from fastapi import APIRouter, HTTPException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from api.models.schemas import ClaimInput, NarrativeResponse
from core.narratives.narrative_manager import process_new_claim
from core.utils.validators import validate_claim_text, validate_year, validate_source

router = APIRouter(prefix="/claims", tags=["Claims"])


@router.post("", response_model=NarrativeResponse)
async def add_claim(claim_input: ClaimInput):
    """
    Add a new claim to the system.
    
    - **claim**: The claim text (10-5000 characters)
    - **year**: Year of the claim (1900-2100)
    - **source**: Source platform (e.g., twitter, facebook)
    
    Returns:
    - **narrative_id**: ID of the linked or newly created narrative
    - **reinforced**: Whether this reinforced an existing narrative
    - **message**: Success message
    """
    try:
        # Validate inputs
        validated_claim = validate_claim_text(claim_input.claim)
        validated_year = validate_year(claim_input.year)
        validated_source = validate_source(claim_input.source)
        
        # Process claim
        metadata = {
            "year": validated_year,
            "source": validated_source
        }
        
        narrative_id = process_new_claim(validated_claim, metadata)
        
        return {
            "narrative_id": narrative_id,
            "reinforced": metadata.get("reinforced", False),
            "message": "Claim processed and stored successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
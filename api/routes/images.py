"""
Image-related API endpoints
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import shutil
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from api.models.schemas import NarrativeResponse
from core.narratives.narrative_manager import process_new_image
from core.utils.validators import validate_year, validate_source, sanitize_filename
from core.config import UPLOAD_DIR

router = APIRouter(prefix="/images", tags=["Images"])


@router.post("", response_model=NarrativeResponse)
async def add_image(
    file: UploadFile = File(...),
    year: int = Form(...),
    source: str = Form(...)
):
    """
    Upload and process an image.
    
    - **file**: Image file (jpg, png, jpeg, webp)
    - **year**: Year the image was created/shared
    - **source**: Source platform
    
    Returns narrative information
    """
    try:
        # Validate inputs
        validated_year = validate_year(year)
        validated_source = validate_source(source)
        
        # Validate file type
        allowed_types = {'image/jpeg', 'image/png', 'image/jpg', 'image/webp'}
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed: {allowed_types}"
            )
        
        # Save uploaded file
        filename = sanitize_filename(file.filename)
        filepath = UPLOAD_DIR / filename
        
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process image
        metadata = {
            "year": validated_year,
            "source": validated_source
        }
        
        narrative_id = process_new_image(str(filepath), metadata)
        
        return {
            "narrative_id": narrative_id,
            "reinforced": metadata.get("reinforced", False),
            "message": "Image processed and stored successfully",
            "metadata": {"filename": filename, "path": str(filepath)}
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        file.file.close()
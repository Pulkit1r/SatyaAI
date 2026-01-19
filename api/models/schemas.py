"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime


class ClaimInput(BaseModel):
    """Schema for adding a new claim"""
    claim: str = Field(..., min_length=10, max_length=5000)
    year: int = Field(..., ge=1900, le=2100)
    source: str = Field(..., min_length=1, max_length=100)
    
    @validator('claim')
    def claim_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Claim cannot be empty or whitespace')
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "claim": "Fake flood image viral on social media",
                "year": 2024,
                "source": "twitter"
            }
        }


class ImageMetadata(BaseModel):
    """Schema for image upload metadata"""
    year: int = Field(..., ge=1900, le=2100)
    source: str = Field(..., min_length=1, max_length=100)


class SearchQuery(BaseModel):
    """Schema for search queries"""
    query: str = Field(..., min_length=3, max_length=1000)
    limit: Optional[int] = Field(5, ge=1, le=50)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "fake flood image",
                "limit": 5
            }
        }


class NarrativeResponse(BaseModel):
    """Schema for narrative operation responses"""
    narrative_id: str
    reinforced: bool
    message: str
    metadata: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    """Schema for health check response"""
    status: str
    qdrant: str
    narratives_count: int
    timestamp: str


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    detail: str
    error_type: Optional[str] = None
    timestamp: str


class SearchResult(BaseModel):
    """Schema for individual search result"""
    score: float
    narrative_id: Optional[str]
    claim: Optional[str]
    year: Optional[int]
    source: Optional[str]
    type: Optional[str]


class SearchResponse(BaseModel):
    """Schema for search response"""
    query: str
    results_count: int
    results: List[SearchResult]
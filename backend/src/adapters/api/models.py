"""
Infrastructure Web Layer - API Models
"""

from typing import Optional
from pydantic import BaseModel


class AnalysisRequest(BaseModel):
    """Request model for resume analysis"""
    resume_text: str
    job_description: Optional[str] = None
    mode: str  # 'ats' or 'job_match'


class AnalysisResponse(BaseModel):
    """Response model for resume analysis results"""
    id: str
    mode: str
    score: int
    score_level: str
    feedback: str
    recommendations: list
    strengths: list
    weaknesses: list
    missing_keywords: list
    matched_keywords: list
    timestamp: str


class UploadResponse(BaseModel):
    """Response model for resume upload"""
    success: bool
    message: str
    resume_id: str
    extracted_text: str 
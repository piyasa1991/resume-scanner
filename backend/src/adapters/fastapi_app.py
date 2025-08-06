"""
Infrastructure Web Layer - FastAPI Application
"""

import os
import uuid
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# In production, these would be proper imports:
# from ...application.services.resume_analysis_service import ResumeAnalysisService
# from ...infrastructure.adapters.file_parser_adapter import FileParserAdapter
# from ...infrastructure.adapters.ai_analysis_adapter import AIAnalysisAdapter
# from ...infrastructure.repositories.analysis_repository import InMemoryAnalysisRepository
# from ...domain.entities.resume import JobDescription

# Mock classes for WebContainer environment
class MockResumeAnalysisService:
    def __init__(self, file_parser, ai_analyzer, analysis_repository):
        self.file_parser = file_parser
        self.ai_analyzer = ai_analyzer
        self.analysis_repository = analysis_repository
    
    def process_resume_file(self, file_bytes: bytes, file_name: str):
        from ...domain.entities.resume import Resume, ContactInfo, ResumeSection
        return Resume(
            id=str(uuid.uuid4()),
            raw_text="Sample resume text",
            contact_info=ContactInfo(email="john@example.com"),
            sections=[ResumeSection(name="experience", content="", is_present=True)],
            keywords=["Python", "FastAPI", "React"],
            created_at=datetime.now(),
            file_name=file_name,
            file_size=len(file_bytes)
        )
    
    def analyze_ats_compatibility(self, resume):
        from ...domain.entities.resume import AnalysisResult, AnalysisMode
        return AnalysisResult(
            id=str(uuid.uuid4()),
            resume_id=resume.id,
            mode=AnalysisMode.ATS,
            score=8,
            score_level=None,
            feedback="<div>Mock ATS analysis feedback</div>",
            recommendations=["Add more keywords", "Improve formatting"],
            strengths=["Good structure", "Clear contact info"],
            weaknesses=["Missing certifications"],
            missing_keywords=[],
            matched_keywords=resume.keywords,
            created_at=datetime.now()
        )
    
    def analyze_job_match(self, resume, job_description):
        from ...domain.entities.resume import AnalysisResult, AnalysisMode
        return AnalysisResult(
            id=str(uuid.uuid4()),
            resume_id=resume.id,
            mode=AnalysisMode.JOB_MATCH,
            score=7,
            score_level=None,
            feedback="<div>Mock job match analysis feedback</div>",
            recommendations=["Add GraphQL experience", "Highlight leadership"],
            strengths=["Technical skills match", "Relevant experience"],
            weaknesses=["Missing some keywords"],
            missing_keywords=["GraphQL", "Microservices"],
            matched_keywords=["Python", "React"],
            created_at=datetime.now(),
            job_description_id=job_description.id
        )


# Pydantic models for API
class AnalysisRequest(BaseModel):
    resume_text: str
    job_description: Optional[str] = None
    mode: str  # 'ats' or 'job_match'


class AnalysisResponse(BaseModel):
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
    success: bool
    message: str
    resume_id: str
    extracted_text: str


def create_fastapi_app() -> FastAPI:
    """Factory function to create FastAPI application"""
    
    app = FastAPI(
        title="Resume Scanner API",
        description="AI-powered resume analysis for ATS compatibility and job matching",
        version="1.0.0"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify actual origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Initialize dependencies (mock for WebContainer)
    from .file_parser_adapter import FileParserAdapter
    from .ai_analysis_adapter import AIAnalysisAdapter
    from .analysis_repository import InMemoryAnalysisRepository
    
    file_parser = FileParserAdapter()
    ai_analyzer = AIAnalysisAdapter(api_key=os.getenv("OPENAI_API_KEY"))
    analysis_repo = InMemoryAnalysisRepository()
    
    # Use mock service for WebContainer
    resume_service = MockResumeAnalysisService(file_parser, ai_analyzer, analysis_repo)
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "service": "Resume Scanner API",
            "version": "1.0.0"
        }
    
    @app.post("/api/upload", response_model=UploadResponse)
    async def upload_resume(file: UploadFile = File(...)):
        """Upload and process resume file"""
        try:
            # Validate file type
            if not file.filename.lower().endswith(('.pdf', '.docx')):
                raise HTTPException(
                    status_code=400, 
                    detail="Only PDF and DOCX files are supported"
                )
            
            # Read file content
            file_content = await file.read()
            
            # Validate file size (5MB limit)
            if len(file_content) > 5 * 1024 * 1024:
                raise HTTPException(
                    status_code=400,
                    detail="File size exceeds 5MB limit"
                )
            
            # Process resume
            resume = resume_service.process_resume_file(file_content, file.filename)
            
            return UploadResponse(
                success=True,
                message="Resume uploaded and processed successfully",
                resume_id=resume.id,
                extracted_text=resume.raw_text[:500] + "..." if len(resume.raw_text) > 500 else resume.raw_text
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
    @app.post("/api/analyze", response_model=AnalysisResponse)
    async def analyze_resume(request: AnalysisRequest):
        """Analyze resume for ATS compatibility or job matching"""
        try:
            # Create mock resume object
            from ..domain.resume import Resume, ContactInfo, ResumeSection, JobDescription
            
            resume = Resume(
                id=str(uuid.uuid4()),
                raw_text=request.resume_text,
                contact_info=ContactInfo(),
                sections=[],
                keywords=["Python", "FastAPI", "React"],
                created_at=datetime.now()
            )
            
            if request.mode == "ats":
                result = resume_service.analyze_ats_compatibility(resume)
            elif request.mode == "job_match":
                if not request.job_description:
                    raise HTTPException(
                        status_code=400,
                        detail="Job description is required for job matching analysis"
                    )
                
                job_desc = JobDescription(
                    id=str(uuid.uuid4()),
                    raw_text=request.job_description,
                    required_skills=[],
                    preferred_skills=[],
                    keywords=["GraphQL", "Microservices", "Python", "React"]
                )
                
                result = resume_service.analyze_job_match(resume, job_desc)
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid analysis mode. Use 'ats' or 'job_match'"
                )
            
            return AnalysisResponse(
                id=result.id,
                mode=result.mode.value,
                score=result.score,
                score_level=result.score_level.value,
                feedback=result.feedback,
                recommendations=result.recommendations,
                strengths=result.strengths,
                weaknesses=result.weaknesses,
                missing_keywords=result.missing_keywords,
                matched_keywords=result.matched_keywords,
                timestamp=result.created_at.isoformat()
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    @app.get("/api/analysis/{analysis_id}")
    async def get_analysis(analysis_id: str):
        """Get analysis result by ID"""
        analysis = analysis_repo.get_analysis(analysis_id)
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        return AnalysisResponse(
            id=analysis.id,
            mode=analysis.mode.value,
            score=analysis.score,
            score_level=analysis.score_level.value,
            feedback=analysis.feedback,
            recommendations=analysis.recommendations,
            strengths=analysis.strengths,
            weaknesses=analysis.weaknesses,
            missing_keywords=analysis.missing_keywords,
            matched_keywords=analysis.matched_keywords,
            timestamp=analysis.created_at.isoformat()
        )
    
    return app


# For running with uvicorn
app = create_fastapi_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
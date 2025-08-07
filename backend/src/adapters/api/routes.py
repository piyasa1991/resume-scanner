"""
Infrastructure Web Layer - API Routes
"""

import uuid
from datetime import datetime
from fastapi import APIRouter, File, UploadFile, HTTPException
from src.adapters.api.models import AnalysisRequest, AnalysisResponse, UploadResponse
from src.adapters.mock_resume_analysis_service import MockResumeAnalysisService
from src.domain.resume import Resume, ContactInfo, ResumeSection, JobDescription


def create_routes(resume_service: MockResumeAnalysisService, analysis_repo) -> APIRouter:
    """Create API routes"""
    
    router = APIRouter()
    
    @router.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "service": "Resume Scanner API",
            "version": "1.0.0"
        }
    
    @router.post("/api/upload", response_model=UploadResponse)
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
    
    @router.post("/api/analyze", response_model=AnalysisResponse)
    async def analyze_resume(request: AnalysisRequest):
        """Analyze resume for ATS compatibility or job matching"""
        try:
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
    
    @router.get("/api/analysis/{analysis_id}")
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
    
    return router 
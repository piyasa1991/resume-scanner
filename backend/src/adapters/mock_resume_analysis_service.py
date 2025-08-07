"""
Infrastructure Web Layer - Mock Resume Analysis Service
"""

import uuid
from datetime import datetime
from src.domain.resume import AnalysisResult, AnalysisMode
from src.domain.resume import Resume, ContactInfo, ResumeSection


class MockResumeAnalysisService:
    """Mock service for resume analysis operations in WebContainer environment"""
    
    def __init__(self, file_parser, ai_analyzer, analysis_repository):
        self.file_parser = file_parser
        self.ai_analyzer = ai_analyzer
        self.analysis_repository = analysis_repository
    
    def process_resume_file(self, file_bytes: bytes, file_name: str):
        """Process uploaded resume file and create Resume entity"""
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
        """Analyze resume for ATS compatibility"""
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
        """Analyze resume against job description"""

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
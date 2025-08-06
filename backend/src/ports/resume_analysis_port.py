"""
Application Ports - Interfaces for Resume Analysis
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..domain.resume import Resume, JobDescription, AnalysisResult, AnalysisMode


class ResumeAnalysisPort(ABC):
    """Port for resume analysis operations"""
    
    @abstractmethod
    def analyze_ats_compatibility(self, resume: Resume) -> AnalysisResult:
        """Analyze resume for ATS compatibility"""
        pass
    
    @abstractmethod
    def analyze_job_match(self, resume: Resume, job_description: JobDescription) -> AnalysisResult:
        """Analyze resume against job description"""
        pass


class FileParserPort(ABC):
    """Port for file parsing operations"""
    
    @abstractmethod
    def extract_text_from_pdf(self, file_bytes: bytes) -> str:
        """Extract text from PDF file"""
        pass
    
    @abstractmethod
    def extract_text_from_docx(self, file_bytes: bytes) -> str:
        """Extract text from DOCX file"""
        pass


class AIAnalysisPort(ABC):
    """Port for AI-powered analysis"""
    
    @abstractmethod
    def analyze_resume_content(self, resume_text: str, analysis_mode: AnalysisMode, 
                             job_description: Optional[str] = None) -> dict:
        """Analyze resume content using AI"""
        pass
    
    @abstractmethod
    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        pass


class AnalysisRepositoryPort(ABC):
    """Port for analysis result persistence"""
    
    @abstractmethod
    def save_analysis(self, analysis: AnalysisResult) -> str:
        """Save analysis result and return ID"""
        pass
    
    @abstractmethod
    def get_analysis(self, analysis_id: str) -> Optional[AnalysisResult]:
        """Get analysis result by ID"""
        pass
    
    @abstractmethod
    def get_analyses_by_resume(self, resume_id: str) -> List[AnalysisResult]:
        """Get all analyses for a resume"""
        pass
"""
Domain Entities - Core Business Objects
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum


class AnalysisMode(Enum):
    ATS = "ats"
    JOB_MATCH = "job_match"


class ScoreLevel(Enum):
    EXCELLENT = "excellent"  # 9-10
    GOOD = "good"           # 7-8
    FAIR = "fair"           # 5-6
    POOR = "poor"           # 1-4


@dataclass
class ContactInfo:
    """Contact information extracted from resume"""
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    location: Optional[str] = None


@dataclass
class ResumeSection:
    """A section of the resume (e.g., Experience, Education)"""
    name: str
    content: str
    is_present: bool = True
    quality_score: int = 0  # 1-10


@dataclass
class Resume:
    """Core resume entity"""
    id: str
    raw_text: str
    contact_info: ContactInfo
    sections: List[ResumeSection]
    keywords: List[str]
    created_at: datetime
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    
    def get_section(self, section_name: str) -> Optional[ResumeSection]:
        """Get a specific section by name"""
        for section in self.sections:
            if section.name.lower() == section_name.lower():
                return section
        return None
    
    def has_section(self, section_name: str) -> bool:
        """Check if resume has a specific section"""
        return self.get_section(section_name) is not None


@dataclass
class JobDescription:
    """Job description entity"""
    id: str
    raw_text: str
    required_skills: List[str]
    preferred_skills: List[str]
    keywords: List[str]
    experience_level: Optional[str] = None
    industry: Optional[str] = None


@dataclass
class AnalysisResult:
    """Result of resume analysis"""
    id: str
    resume_id: str
    mode: AnalysisMode
    score: int  # 1-10
    score_level: ScoreLevel
    feedback: str
    recommendations: List[str]
    strengths: List[str]
    weaknesses: List[str]
    missing_keywords: List[str]
    matched_keywords: List[str]
    created_at: datetime
    job_description_id: Optional[str] = None
    
    def __post_init__(self):
        """Set score level based on score"""
        if self.score >= 9:
            self.score_level = ScoreLevel.EXCELLENT
        elif self.score >= 7:
            self.score_level = ScoreLevel.GOOD
        elif self.score >= 5:
            self.score_level = ScoreLevel.FAIR
        else:
            self.score_level = ScoreLevel.POOR


@dataclass
class AnalysisMetrics:
    """Detailed metrics for analysis"""
    keyword_match_percentage: float
    section_completeness_score: int
    formatting_score: int
    content_quality_score: int
    ats_compatibility_score: int
    readability_score: int
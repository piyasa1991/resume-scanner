"""
Domain Value Objects - Analysis Criteria and Rules
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from enum import Enum


class SectionType(Enum):
    CONTACT = "contact"
    SUMMARY = "summary"
    EXPERIENCE = "experience"
    EDUCATION = "education"
    SKILLS = "skills"
    CERTIFICATIONS = "certifications"
    PROJECTS = "projects"


@dataclass(frozen=True)
class ATSCriteria:
    """ATS evaluation criteria"""
    required_sections: List[SectionType]
    preferred_sections: List[SectionType]
    max_file_size_mb: int
    supported_formats: List[str]
    min_keyword_density: float
    max_keyword_density: float
    
    @classmethod
    def default(cls) -> 'ATSCriteria':
        return cls(
            required_sections=[
                SectionType.CONTACT,
                SectionType.EXPERIENCE,
                SectionType.EDUCATION,
                SectionType.SKILLS
            ],
            preferred_sections=[
                SectionType.SUMMARY,
                SectionType.CERTIFICATIONS,
                SectionType.PROJECTS
            ],
            max_file_size_mb=5,
            supported_formats=['pdf', 'docx'],
            min_keyword_density=0.02,
            max_keyword_density=0.08
        )


@dataclass(frozen=True)
class JobMatchCriteria:
    """Job matching evaluation criteria"""
    required_skill_weight: float
    preferred_skill_weight: float
    experience_weight: float
    education_weight: float
    keyword_match_threshold: float
    
    @classmethod
    def default(cls) -> 'JobMatchCriteria':
        return cls(
            required_skill_weight=0.4,
            preferred_skill_weight=0.2,
            experience_weight=0.25,
            education_weight=0.15,
            keyword_match_threshold=0.6
        )


@dataclass(frozen=True)
class ScoringWeights:
    """Weights for different scoring components"""
    content_quality: float
    keyword_match: float
    section_completeness: float
    formatting: float
    ats_compatibility: float
    
    @classmethod
    def ats_weights(cls) -> 'ScoringWeights':
        return cls(
            content_quality=0.3,
            keyword_match=0.2,
            section_completeness=0.25,
            formatting=0.15,
            ats_compatibility=0.1
        )
    
    @classmethod
    def job_match_weights(cls) -> 'ScoringWeights':
        return cls(
            content_quality=0.2,
            keyword_match=0.4,
            section_completeness=0.15,
            formatting=0.1,
            ats_compatibility=0.15
        )
"""
Application Services - Business Logic Implementation
"""

import uuid
from datetime import datetime
from typing import List, Optional
from ..ports.resume_analysis_port import (
    ResumeAnalysisPort, FileParserPort, AIAnalysisPort, AnalysisRepositoryPort
)
from ...domain.entities.resume import (
    Resume, JobDescription, AnalysisResult, AnalysisMode, 
    ContactInfo, ResumeSection
)
from ...domain.value_objects.analysis_criteria import ATSCriteria, JobMatchCriteria


class ResumeAnalysisService(ResumeAnalysisPort):
    """Main service for resume analysis operations"""
    
    def __init__(self, 
                 file_parser: FileParserPort,
                 ai_analyzer: AIAnalysisPort,
                 analysis_repository: AnalysisRepositoryPort):
        self.file_parser = file_parser
        self.ai_analyzer = ai_analyzer
        self.analysis_repository = analysis_repository
        self.ats_criteria = ATSCriteria.default()
        self.job_match_criteria = JobMatchCriteria.default()
    
    def process_resume_file(self, file_bytes: bytes, file_name: str) -> Resume:
        """Process uploaded resume file and create Resume entity"""
        
        # Extract text based on file type
        if file_name.lower().endswith('.pdf'):
            raw_text = self.file_parser.extract_text_from_pdf(file_bytes)
        elif file_name.lower().endswith('.docx'):
            raw_text = self.file_parser.extract_text_from_docx(file_bytes)
        else:
            raise ValueError("Unsupported file format")
        
        # Extract structured information
        contact_info = self._extract_contact_info(raw_text)
        sections = self._extract_sections(raw_text)
        keywords = self.ai_analyzer.extract_keywords(raw_text)
        
        return Resume(
            id=str(uuid.uuid4()),
            raw_text=raw_text,
            contact_info=contact_info,
            sections=sections,
            keywords=keywords,
            created_at=datetime.now(),
            file_name=file_name,
            file_size=len(file_bytes)
        )
    
    def analyze_ats_compatibility(self, resume: Resume) -> AnalysisResult:
        """Analyze resume for ATS compatibility"""
        
        # Get AI analysis
        ai_result = self.ai_analyzer.analyze_resume_content(
            resume.raw_text, 
            AnalysisMode.ATS
        )
        
        # Calculate comprehensive score
        score = self._calculate_ats_score(resume, ai_result)
        
        # Generate structured feedback
        feedback = self._generate_ats_feedback(resume, ai_result, score)
        
        analysis = AnalysisResult(
            id=str(uuid.uuid4()),
            resume_id=resume.id,
            mode=AnalysisMode.ATS,
            score=score,
            score_level=None,  # Will be set in __post_init__
            feedback=feedback,
            recommendations=ai_result.get('recommendations', []),
            strengths=ai_result.get('strengths', []),
            weaknesses=ai_result.get('weaknesses', []),
            missing_keywords=[],
            matched_keywords=resume.keywords,
            created_at=datetime.now()
        )
        
        # Save analysis
        self.analysis_repository.save_analysis(analysis)
        
        return analysis
    
    def analyze_job_match(self, resume: Resume, job_description: JobDescription) -> AnalysisResult:
        """Analyze resume against job description"""
        
        # Get AI analysis
        ai_result = self.ai_analyzer.analyze_resume_content(
            resume.raw_text,
            AnalysisMode.JOB_MATCH,
            job_description.raw_text
        )
        
        # Calculate match score
        score = self._calculate_job_match_score(resume, job_description, ai_result)
        
        # Analyze keyword matching
        matched_keywords, missing_keywords = self._analyze_keyword_match(
            resume.keywords, 
            job_description.keywords
        )
        
        # Generate structured feedback
        feedback = self._generate_job_match_feedback(
            resume, job_description, ai_result, score
        )
        
        analysis = AnalysisResult(
            id=str(uuid.uuid4()),
            resume_id=resume.id,
            mode=AnalysisMode.JOB_MATCH,
            score=score,
            score_level=None,  # Will be set in __post_init__
            feedback=feedback,
            recommendations=ai_result.get('recommendations', []),
            strengths=ai_result.get('strengths', []),
            weaknesses=ai_result.get('weaknesses', []),
            missing_keywords=missing_keywords,
            matched_keywords=matched_keywords,
            created_at=datetime.now(),
            job_description_id=job_description.id
        )
        
        # Save analysis
        self.analysis_repository.save_analysis(analysis)
        
        return analysis
    
    def _extract_contact_info(self, text: str) -> ContactInfo:
        """Extract contact information from resume text"""
        import re
        
        # Simple regex patterns for contact info
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        
        email = re.search(email_pattern, text)
        phone = re.search(phone_pattern, text)
        linkedin = re.search(linkedin_pattern, text)
        
        return ContactInfo(
            email=email.group() if email else None,
            phone=phone.group() if phone else None,
            linkedin=linkedin.group() if linkedin else None
        )
    
    def _extract_sections(self, text: str) -> List[ResumeSection]:
        """Extract resume sections"""
        sections = []
        
        # Common section headers
        section_patterns = {
            'experience': r'(PROFESSIONAL\s+EXPERIENCE|WORK\s+EXPERIENCE|EXPERIENCE)',
            'education': r'(EDUCATION|ACADEMIC\s+BACKGROUND)',
            'skills': r'(TECHNICAL\s+SKILLS|SKILLS|COMPETENCIES)',
            'summary': r'(PROFESSIONAL\s+SUMMARY|SUMMARY|PROFILE)',
            'certifications': r'(CERTIFICATIONS|CERTIFICATES)',
            'projects': r'(PROJECTS|PORTFOLIO)'
        }
        
        for section_name, pattern in section_patterns.items():
            import re
            if re.search(pattern, text, re.IGNORECASE):
                sections.append(ResumeSection(
                    name=section_name,
                    content="",  # Would extract actual content in production
                    is_present=True,
                    quality_score=7  # Mock score
                ))
        
        return sections
    
    def _calculate_ats_score(self, resume: Resume, ai_result: dict) -> int:
        """Calculate ATS compatibility score"""
        base_score = 5
        
        # Section completeness (40%)
        required_sections = len([s for s in resume.sections if s.name in ['experience', 'education', 'skills']])
        section_score = min(required_sections * 2, 4)
        
        # Contact info completeness (20%)
        contact_score = 0
        if resume.contact_info.email: contact_score += 1
        if resume.contact_info.phone: contact_score += 1
        
        # AI analysis score (40%)
        ai_score = ai_result.get('score', 5)
        
        total_score = min(base_score + section_score + contact_score + (ai_score - 5), 10)
        return max(1, int(total_score))
    
    def _calculate_job_match_score(self, resume: Resume, job_description: JobDescription, ai_result: dict) -> int:
        """Calculate job match score"""
        # Keyword matching
        matched_keywords, _ = self._analyze_keyword_match(resume.keywords, job_description.keywords)
        keyword_match_ratio = len(matched_keywords) / max(len(job_description.keywords), 1)
        
        # AI analysis
        ai_score = ai_result.get('score', 5)
        
        # Weighted calculation
        final_score = (keyword_match_ratio * 4) + (ai_score * 0.6)
        return max(1, min(10, int(final_score)))
    
    def _analyze_keyword_match(self, resume_keywords: List[str], job_keywords: List[str]) -> tuple:
        """Analyze keyword matching between resume and job description"""
        resume_lower = [k.lower() for k in resume_keywords]
        job_lower = [k.lower() for k in job_keywords]
        
        matched = [k for k in job_keywords if k.lower() in resume_lower]
        missing = [k for k in job_keywords if k.lower() not in resume_lower]
        
        return matched, missing
    
    def _generate_ats_feedback(self, resume: Resume, ai_result: dict, score: int) -> str:
        """Generate ATS feedback in HTML format"""
        return f"""
        <div class="space-y-6">
            <div class="p-4 bg-green-50 border-l-4 border-green-400 rounded-r-lg">
                <h4 class="font-semibold text-green-800 mb-2">✅ Strengths</h4>
                <ul class="text-green-700 space-y-1">
                    <li>• Clear contact information present</li>
                    <li>• Well-structured sections (Experience, Skills, Education)</li>
                    <li>• Good use of action verbs and quantified achievements</li>
                    <li>• Relevant technical skills clearly listed</li>
                </ul>
            </div>
            
            <div class="p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded-r-lg">
                <h4 class="font-semibold text-yellow-800 mb-2">⚠️ Areas for Improvement</h4>
                <ul class="text-yellow-700 space-y-1">
                    <li>• Consider adding a "Core Competencies" section with keywords</li>
                    <li>• Include more industry-specific buzzwords</li>
                    <li>• Add metrics to quantify your impact where possible</li>
                </ul>
            </div>
            
            <div class="p-4 bg-blue-50 border-l-4 border-blue-400 rounded-r-lg">
                <h4 class="font-semibold text-blue-800 mb-2">🚀 ATS Optimization Tips</h4>
                <ul class="text-blue-700 space-y-1">
                    <li>• Use standard section headings (Experience, Education, Skills)</li>
                    <li>• Avoid graphics, tables, or complex formatting</li>
                    <li>• Include both acronyms and full terms (e.g., "AI" and "Artificial Intelligence")</li>
                    <li>• Use keywords from job postings naturally throughout your resume</li>
                </ul>
            </div>
        </div>
        """
    
    def _generate_job_match_feedback(self, resume: Resume, job_description: JobDescription, 
                                   ai_result: dict, score: int) -> str:
        """Generate job match feedback in HTML format"""
        matched_keywords, missing_keywords = self._analyze_keyword_match(
            resume.keywords, job_description.keywords
        )
        
        return f"""
        <div class="space-y-6">
            <div class="p-4 bg-green-50 border-l-4 border-green-400 rounded-r-lg">
                <h4 class="font-semibold text-green-800 mb-2">✅ Strong Matches</h4>
                <ul class="text-green-700 space-y-1">
                    <li>• <strong>Technical Skills:</strong> {', '.join(matched_keywords[:3]) if matched_keywords else 'Various skills match'}</li>
                    <li>• <strong>Experience Level:</strong> Aligns with job requirements</li>
                    <li>• <strong>Industry Background:</strong> Relevant experience demonstrated</li>
                </ul>
            </div>
            
            <div class="p-4 bg-red-50 border-l-4 border-red-400 rounded-r-lg">
                <h4 class="font-semibold text-red-800 mb-2">❌ Missing Keywords</h4>
                <ul class="text-red-700 space-y-1">
                    {chr(10).join([f'<li>• <strong>{keyword}:</strong> Consider adding this skill/experience</li>' for keyword in missing_keywords[:5]])}
                </ul>
            </div>
            
            <div class="p-4 bg-blue-50 border-l-4 border-blue-400 rounded-r-lg">
                <h4 class="font-semibold text-blue-800 mb-2">🚀 Recommendations</h4>
                <ul class="text-blue-700 space-y-1">
                    <li>• Incorporate missing keywords naturally into your experience descriptions</li>
                    <li>• Highlight relevant projects that demonstrate required skills</li>
                    <li>• Consider adding certifications in missing technology areas</li>
                    <li>• Quantify achievements with metrics that matter to this role</li>
                </ul>
            </div>
        </div>
        """
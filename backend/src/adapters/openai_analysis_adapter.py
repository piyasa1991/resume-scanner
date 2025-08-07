"""
Infrastructure Adapters - AI Analysis Implementation
"""

import json
import re
from typing import List, Optional, Dict, Any
from src.ports.resume_analysis_port import AIAnalysisPort
from src.domain.resume import AnalysisMode
import openai


class OpenAIAnalysisAdapter(AIAnalysisPort):
    """Adapter for AI-powered analysis using OpenAI"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
    
    def analyze_resume_content(self, resume_text: str, analysis_mode: AnalysisMode, 
                             job_description: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze resume content using AI
        """
        
        if analysis_mode == AnalysisMode.ATS:
            prompt = self._get_ats_analysis_prompt(resume_text)
        else:
            prompt = self._get_job_match_prompt(resume_text, job_description)
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert resume analyzer..."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        return json.loads(response.choices[0].message.content)
        
        """
        # Mock implementation for demonstration
        if analysis_mode == AnalysisMode.ATS:
            return self._mock_ats_analysis(resume_text)
        else:
            return self._mock_job_match_analysis(resume_text, job_description or "")
        """
    
    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract keywords from text
        
        In production, this could use:
        - OpenAI for intelligent keyword extraction
        - NLTK/spaCy for NLP-based extraction
        - Custom domain-specific keyword lists
        """
        
        # Simple keyword extraction for demonstration
        technical_keywords = [
            'React', 'TypeScript', 'JavaScript', 'Node.js', 'Python', 'FastAPI',
            'PostgreSQL', 'MongoDB', 'AWS', 'Docker', 'Kubernetes', 'Git',
            'HTML5', 'CSS3', 'Tailwind CSS', 'Express.js', 'Redis', 'Webpack',
            'Jest', 'CI/CD', 'Vue.js', 'microservices', 'full-stack', 'Agile',
            'Scrum', 'GraphQL', 'REST API', 'DevOps', 'cloud computing'
        ]
        
        found_keywords = []
        text_lower = text.lower()
        
        for keyword in technical_keywords:
            if keyword.lower() in text_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def _mock_ats_analysis(self, resume_text: str) -> Dict[str, Any]:
        """Mock ATS analysis for demonstration"""
        return {
            "score": 8,
            "strengths": [
                "Clear contact information and professional summary",
                "Well-structured sections with standard headings",
                "Good use of action verbs and quantified achievements",
                "Relevant technical skills clearly listed"
            ],
            "weaknesses": [
                "Could benefit from more industry-specific keywords",
                "Missing some quantified metrics in experience section",
                "Could add more certifications or professional development"
            ],
            "recommendations": [
                "Add a 'Core Competencies' section with key technical skills",
                "Include more specific metrics and KPIs in experience descriptions",
                "Consider adding relevant industry certifications",
                "Use more action verbs to start bullet points",
                "Include keywords from target job descriptions"
            ],
            "ats_compatibility": {
                "format_score": 9,
                "keyword_density": 7,
                "section_structure": 8,
                "readability": 8
            }
        }
    
    def _mock_job_match_analysis(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Mock job match analysis for demonstration"""
        return {
            "score": 7,
            "strengths": [
                "Strong technical skills match with React and TypeScript",
                "Relevant full-stack development experience",
                "Leadership experience aligns with senior role requirements",
                "Cloud technology experience matches infrastructure needs"
            ],
            "weaknesses": [
                "Missing specific mention of GraphQL experience",
                "Could highlight more testing framework experience",
                "Agile/Scrum methodology not explicitly mentioned",
                "Mobile development experience not evident"
            ],
            "recommendations": [
                "Add GraphQL to technical skills if you have experience",
                "Highlight testing frameworks usage (Jest, Cypress, etc.)",
                "Mention Agile/Scrum experience in project descriptions",
                "Consider adding any mobile development projects",
                "Quantify team leadership and mentoring achievements"
            ],
            "keyword_analysis": {
                "matched_keywords": ["React", "TypeScript", "Node.js", "AWS", "PostgreSQL"],
                "missing_keywords": ["GraphQL", "Microservices", "Agile", "Testing"],
                "match_percentage": 75
            }
        }
    
    def _get_ats_analysis_prompt(self, resume_text: str) -> str:
        """Get prompt for ATS analysis"""
        return f"""
        Analyze this resume for ATS (Applicant Tracking System) compatibility and provide a comprehensive evaluation.

        Resume Text:
        {resume_text}

        Please provide analysis in the following JSON format:
        {{
            "score": <1-10 integer>,
            "strengths": [<list of strengths>],
            "weaknesses": [<list of areas for improvement>],
            "recommendations": [<list of specific recommendations>],
            "ats_compatibility": {{
                "format_score": <1-10>,
                "keyword_density": <1-10>,
                "section_structure": <1-10>,
                "readability": <1-10>
            }}
        }}

        Focus on:
        1. Resume structure and formatting
        2. Section organization and completeness
        3. Keyword usage and density
        4. ATS-friendly formatting practices
        5. Contact information completeness
        6. Professional summary effectiveness
        """
    
    def _get_job_match_prompt(self, resume_text: str, job_description: str) -> str:
        """Get prompt for job match analysis"""
        return f"""
        Analyze how well this resume matches the given job description and provide detailed feedback.

        Resume Text:
        {resume_text}

        Job Description:
        {job_description}

        Please provide analysis in the following JSON format:
        {{
            "score": <1-10 integer>,
            "strengths": [<list of matching strengths>],
            "weaknesses": [<list of gaps or missing elements>],
            "recommendations": [<list of specific improvements>],
            "keyword_analysis": {{
                "matched_keywords": [<list of matched keywords>],
                "missing_keywords": [<list of missing important keywords>],
                "match_percentage": <percentage as integer>
            }}
        }}

        Focus on:
        1. Technical skills alignment
        2. Experience level match
        3. Industry-specific requirements
        4. Keyword matching
        5. Qualifications and certifications
        6. Soft skills and cultural fit indicators
        """
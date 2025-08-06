"""
Infrastructure Adapters - File Parsing Implementation
"""

import re
from typing import List
from ...application.ports.resume_analysis_port import FileParserPort


class FileParserAdapter(FileParserPort):
    """Adapter for file parsing operations"""
    
    def extract_text_from_pdf(self, file_bytes: bytes) -> str:
        """
        Extract text from PDF file
        In production, this would use pdfplumber or PyMuPDF:
        
        import pdfplumber
        from io import BytesIO
        
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text.strip()
        """
        
        # Mock implementation for WebContainer environment
        return self._get_sample_resume_text()
    
    def extract_text_from_docx(self, file_bytes: bytes) -> str:
        """
        Extract text from DOCX file
        In production, this would use python-docx:
        
        from docx import Document
        from io import BytesIO
        
        doc = Document(BytesIO(file_bytes))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
        """
        
        # Mock implementation for WebContainer environment
        return self._get_sample_resume_text()
    
    def _get_sample_resume_text(self) -> str:
        """Return sample resume text for demonstration"""
        return """
JOHN DOE
Software Engineer
📧 john.doe@email.com | 📱 (555) 123-4567 | 🔗 linkedin.com/in/johndoe

PROFESSIONAL SUMMARY
Results-driven Software Engineer with 5+ years of experience in full-stack development, 
specializing in React, Node.js, and cloud technologies. Proven track record of delivering 
scalable web applications and leading cross-functional teams.

TECHNICAL SKILLS
• Frontend: React, TypeScript, JavaScript, HTML5, CSS3, Tailwind CSS
• Backend: Node.js, Python, Express.js, FastAPI
• Databases: PostgreSQL, MongoDB, Redis
• Cloud: AWS, Docker, Kubernetes
• Tools: Git, Webpack, Jest, CI/CD

PROFESSIONAL EXPERIENCE

Senior Software Engineer | TechCorp Inc. | 2021 - Present
• Led development of customer-facing web application serving 100k+ users
• Implemented microservices architecture reducing system downtime by 40%
• Mentored junior developers and established coding best practices
• Technologies: React, Node.js, AWS, PostgreSQL

Software Developer | StartupXYZ | 2019 - 2021
• Developed responsive web applications using modern JavaScript frameworks
• Collaborated with design team to implement pixel-perfect user interfaces
• Optimized database queries improving application performance by 60%
• Technologies: Vue.js, Python, MongoDB

EDUCATION
Bachelor of Science in Computer Science
University of Technology | 2015 - 2019

CERTIFICATIONS
• AWS Certified Solutions Architect
• Google Cloud Professional Developer

PROJECTS
• Open-source contributor to React ecosystem (2000+ GitHub stars)
• Built personal finance app with 10k+ active users
"""
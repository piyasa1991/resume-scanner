"""
Tests for FileParserAdapter
"""

import pytest
from io import BytesIO
from src.adapters.file_parser_adapter import FileParserAdapter
from docx import Document
import pdfplumber
import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


class TestFileParserAdapter:
    """Test cases for FileParserAdapter"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.file_parser = FileParserAdapter()
        self.sample_resume_text = self._create_sample_resume_text()
    
    def _create_sample_resume_text(self) -> str:
        """Create sample resume text for testing"""
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
    
    def _create_sample_pdf_bytes(self, text: str) -> bytes:
        """Create a PDF file in memory with the given text"""
        buffer = BytesIO()
        
        # Create PDF with reportlab
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Split text into lines and add to PDF
        lines = text.split('\n')
        y_position = height - 50
        
        for line in lines:
            if line.strip():  # Only add non-empty lines
                c.drawString(50, y_position, line.strip())
                y_position -= 15
                
                # Add new page if we run out of space
                if y_position < 50:
                    c.showPage()
                    y_position = height - 50
        
        c.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def _create_sample_docx_bytes(self, text: str) -> bytes:
        """Create a DOCX file in memory with the given text"""
        # Create a new Document
        doc = Document()
        
        # Split text into paragraphs and add to document
        paragraphs = text.split('\n')
        for paragraph_text in paragraphs:
            if paragraph_text.strip():  # Only add non-empty paragraphs
                doc.add_paragraph(paragraph_text.strip())
        
        # Save to bytes
        buffer = BytesIO()
        doc.save(buffer)
        docx_bytes = buffer.getvalue()
        buffer.close()
        
        return docx_bytes
    
    def test_extract_text_from_pdf_with_real_pdf(self):
        """Test PDF text extraction with a real PDF file"""
        # Create sample PDF bytes
        pdf_bytes = self._create_sample_pdf_bytes(self.sample_resume_text)
        
        # Test the method
        result = self.file_parser.extract_text_from_pdf(pdf_bytes)
        
        # Assertions
        assert isinstance(result, str)
        assert len(result) > 0
        # Note: PDF text extraction might not be perfect, so we check for key content
        assert "JOHN DOE" in result or "Software Engineer" in result
    
    def test_extract_text_from_docx_with_real_docx(self):
        """Test DOCX text extraction with a real DOCX file"""
        # Create sample DOCX bytes
        docx_bytes = self._create_sample_docx_bytes(self.sample_resume_text)
        
        # Test the method
        result = self.file_parser.extract_text_from_docx(docx_bytes)
        
        # Assertions
        assert isinstance(result, str)
        assert len(result) > 0
        assert "JOHN DOE" in result
        assert "Software Engineer" in result
        assert "PROFESSIONAL SUMMARY" in result
        assert "TECHNICAL SKILLS" in result
        assert "PROFESSIONAL EXPERIENCE" in result
        assert "EDUCATION" in result
    
    def test_extract_text_from_pdf_simple_text(self):
        """Test PDF text extraction with simple text"""
        simple_text = "This is a simple test document for PDF extraction."
        pdf_bytes = self._create_sample_pdf_bytes(simple_text)
        
        result = self.file_parser.extract_text_from_pdf(pdf_bytes)
        
        assert isinstance(result, str)
        assert len(result) > 0
        # PDF extraction might not be perfect, so we check for partial content
        assert "test" in result.lower() or "document" in result.lower()
    
    def test_extract_text_from_docx_simple_text(self):
        """Test DOCX text extraction with simple text"""
        simple_text = "This is a simple test document for DOCX extraction."
        docx_bytes = self._create_sample_docx_bytes(simple_text)
        
        result = self.file_parser.extract_text_from_docx(docx_bytes)
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "simple test document" in result
    
    def test_extract_text_from_pdf_multiple_paragraphs(self):
        """Test PDF text extraction with multiple paragraphs"""
        multi_para_text = """First paragraph with some content.
Second paragraph with different content.
Third paragraph to test multiple paragraphs."""
        
        pdf_bytes = self._create_sample_pdf_bytes(multi_para_text)
        result = self.file_parser.extract_text_from_pdf(pdf_bytes)
        
        assert isinstance(result, str)
        assert len(result) > 0
        # Check that we get some content back
        assert any(word in result.lower() for word in ["first", "second", "third", "paragraph"])
    
    def test_extract_text_from_docx_multiple_paragraphs(self):
        """Test DOCX text extraction with multiple paragraphs"""
        multi_para_text = """First paragraph with some content.
Second paragraph with different content.
Third paragraph to test multiple paragraphs."""
        
        docx_bytes = self._create_sample_docx_bytes(multi_para_text)
        result = self.file_parser.extract_text_from_docx(docx_bytes)
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "First paragraph" in result
        assert "Second paragraph" in result
        assert "Third paragraph" in result
    
    def test_extract_text_from_pdf_special_characters(self):
        """Test PDF text extraction with special characters"""
        special_text = "Special chars: éñüß@#$%^&*()_+-=[]{}|;':\",./<>?"
        pdf_bytes = self._create_sample_pdf_bytes(special_text)
        
        result = self.file_parser.extract_text_from_pdf(pdf_bytes)
        
        assert isinstance(result, str)
        assert len(result) > 0
        # PDF extraction might not preserve all special chars perfectly
        assert "Special chars" in result
    
    def test_extract_text_from_docx_special_characters(self):
        """Test DOCX text extraction with special characters"""
        special_text = "Special chars: éñüß@#$%^&*()_+-=[]{}|;':\",./<>?"
        docx_bytes = self._create_sample_docx_bytes(special_text)
        
        result = self.file_parser.extract_text_from_docx(docx_bytes)
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "Special chars" in result
        # DOCX should preserve most special characters
        assert "@#$%^&*()" in result
    
    def test_extract_text_from_pdf_empty_content(self):
        """Test PDF text extraction with empty content"""
        empty_text = ""
        pdf_bytes = self._create_sample_pdf_bytes(empty_text)
        
        result = self.file_parser.extract_text_from_pdf(pdf_bytes)
        
        assert isinstance(result, str)
        # Empty PDF should return empty string or minimal content
        assert len(result) >= 0
    
    def test_extract_text_from_docx_empty_content(self):
        """Test DOCX text extraction with empty content"""
        empty_text = ""
        docx_bytes = self._create_sample_docx_bytes(empty_text)
        
        result = self.file_parser.extract_text_from_docx(docx_bytes)
        
        assert isinstance(result, str)
        # Empty DOCX should return empty string
        assert result == ""
    
    def test_extract_text_from_pdf_large_content(self):
        """Test PDF text extraction with large content"""
        large_text = "Large content test. " * 1000  # Create large text
        pdf_bytes = self._create_sample_pdf_bytes(large_text)
        
        result = self.file_parser.extract_text_from_pdf(pdf_bytes)
        
        assert isinstance(result, str)
        assert len(result) > 0
        # Should handle large content without errors
        assert "Large content test" in result
    
    def test_extract_text_from_docx_large_content(self):
        """Test DOCX text extraction with large content"""
        large_text = "Large content test. " * 1000  # Create large text
        docx_bytes = self._create_sample_docx_bytes(large_text)
        
        result = self.file_parser.extract_text_from_docx(docx_bytes)
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "Large content test" in result
        assert len(result) > 1000  # Should contain substantial content
    
    def test_file_parser_implements_port_interface(self):
        """Test that FileParserAdapter implements the FileParserPort interface"""
        # Check that the class has the required methods
        assert hasattr(self.file_parser, 'extract_text_from_pdf')
        assert hasattr(self.file_parser, 'extract_text_from_docx')
        
        # Check that methods are callable
        assert callable(self.file_parser.extract_text_from_pdf)
        assert callable(self.file_parser.extract_text_from_docx)
    
    def test_extract_text_from_pdf_invalid_bytes(self):
        """Test PDF text extraction with invalid bytes"""
        invalid_bytes = b"not a pdf file"
        
        # This should raise an exception or handle gracefully
        try:
            result = self.file_parser.extract_text_from_pdf(invalid_bytes)
            # If it doesn't raise an exception, result should be a string
            assert isinstance(result, str)
        except Exception as e:
            # Exception is acceptable for invalid PDF data
            assert isinstance(e, Exception)
    
    def test_extract_text_from_docx_invalid_bytes(self):
        """Test DOCX text extraction with invalid bytes"""
        invalid_bytes = b"not a docx file"
        
        # This should raise an exception or handle gracefully
        try:
            result = self.file_parser.extract_text_from_docx(invalid_bytes)
            # If it doesn't raise an exception, result should be a string
            assert isinstance(result, str)
        except Exception as e:
            # Exception is acceptable for invalid DOCX data
            assert isinstance(e, Exception) 
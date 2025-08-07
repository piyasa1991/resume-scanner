"""
Infrastructure Adapters - File Parsing Implementation
"""

import re
from typing import List
from src.ports.resume_analysis_port import FileParserPort
import pdfplumber
from io import BytesIO
from docx import Document


class FileParserAdapter(FileParserPort):
    """Adapter for file parsing operations"""
    
    def extract_text_from_pdf(self, file_bytes: bytes) -> str:
        """
        Extract text from PDF file
        """
        
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text.strip()
    
    def extract_text_from_docx(self, file_bytes: bytes) -> str:
        """
        Extract text from DOCX file

        """
        
        doc = Document(BytesIO(file_bytes))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    
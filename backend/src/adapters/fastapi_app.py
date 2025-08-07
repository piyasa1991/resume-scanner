"""
Infrastructure Web Layer - FastAPI Application
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.adapters.api.routes import create_routes
from src.domain.resume_analysis_service import ResumeAnalysisService
from src.adapters.mock_resume_analysis_service import MockResumeAnalysisService
from src.adapters.file_parser_adapter import FileParserAdapter
from src.adapters.openai_analysis_adapter import OpenAIAnalysisAdapter
from src.adapters.analysis_repository import InMemoryAnalysisRepository


def create_fastapi_app() -> FastAPI:
    """Factory function to create FastAPI application"""
    
    app = FastAPI(
        title="Resume Scanner API",
        description="AI-powered resume analysis for ATS compatibility and job matching",
        version="1.0.0"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify actual origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    
    file_parser = FileParserAdapter()
    ai_analyzer = OpenAIAnalysisAdapter(api_key=os.getenv("OPENAI_API_KEY", "my-api-key"))
    analysis_repo = InMemoryAnalysisRepository()
    
    resume_service = MockResumeAnalysisService(file_parser, ai_analyzer, analysis_repo)
    # resume_service = ResumeAnalysisService(file_parser, ai_analyzer, analysis_repo)
    
    # Create and include routes
    routes = create_routes(resume_service, analysis_repo)
    app.include_router(routes)
    
    return app


# For running with uvicorn
app = create_fastapi_app()
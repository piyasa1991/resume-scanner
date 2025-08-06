"""
Infrastructure Repositories - Data Persistence Implementation
"""

from typing import Dict, List, Optional
from ..ports.resume_analysis_port import AnalysisRepositoryPort
from ..domain.resume import AnalysisResult


class InMemoryAnalysisRepository(AnalysisRepositoryPort):
    """In-memory implementation of analysis repository for development"""
    
    def __init__(self):
        self._analyses: Dict[str, AnalysisResult] = {}
        self._resume_analyses: Dict[str, List[str]] = {}  # resume_id -> analysis_ids
    
    def save_analysis(self, analysis: AnalysisResult) -> str:
        """Save analysis result and return ID"""
        self._analyses[analysis.id] = analysis
        
        # Track analyses by resume
        if analysis.resume_id not in self._resume_analyses:
            self._resume_analyses[analysis.resume_id] = []
        self._resume_analyses[analysis.resume_id].append(analysis.id)
        
        return analysis.id
    
    def get_analysis(self, analysis_id: str) -> Optional[AnalysisResult]:
        """Get analysis result by ID"""
        return self._analyses.get(analysis_id)
    
    def get_analyses_by_resume(self, resume_id: str) -> List[AnalysisResult]:
        """Get all analyses for a resume"""
        analysis_ids = self._resume_analyses.get(resume_id, [])
        return [self._analyses[aid] for aid in analysis_ids if aid in self._analyses]


class DatabaseAnalysisRepository(AnalysisRepositoryPort):
    """Database implementation of analysis repository for production"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        # In production, initialize database connection:
        # import sqlalchemy
        # self.engine = sqlalchemy.create_engine(database_url)
        # self.Session = sqlalchemy.orm.sessionmaker(bind=self.engine)
    
    def save_analysis(self, analysis: AnalysisResult) -> str:
        """Save analysis result to database"""
        # In production, implement database save:
        # session = self.Session()
        # try:
        #     db_analysis = AnalysisModel(
        #         id=analysis.id,
        #         resume_id=analysis.resume_id,
        #         mode=analysis.mode.value,
        #         score=analysis.score,
        #         feedback=analysis.feedback,
        #         # ... other fields
        #     )
        #     session.add(db_analysis)
        #     session.commit()
        #     return analysis.id
        # finally:
        #     session.close()
        
        # Mock implementation
        return analysis.id
    
    def get_analysis(self, analysis_id: str) -> Optional[AnalysisResult]:
        """Get analysis result from database"""
        # In production, implement database query
        return None
    
    def get_analyses_by_resume(self, resume_id: str) -> List[AnalysisResult]:
        """Get all analyses for a resume from database"""
        # In production, implement database query
        return []
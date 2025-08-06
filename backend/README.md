# Resume Scanner Backend

A Python backend service for analyzing resumes using AI, built with hexagonal architecture principles.

## Architecture

This backend follows **Hexagonal Architecture** (Ports and Adapters) for clean separation of concerns:

```
backend/
├── src/
│   ├── domain/                 # Core business logic
│   │   ├── entities/          # Business entities
│   │   └── value_objects/     # Domain value objects
│   ├── application/           # Application services
│   │   ├── ports/            # Interfaces/contracts
│   │   └── services/         # Business logic implementation
│   └── infrastructure/       # External concerns
│       ├── adapters/         # External service adapters
│       ├── repositories/     # Data persistence
│       └── web/             # Web framework (FastAPI)
├── main.py                   # Application entry point
└── requirements.txt         # Python dependencies
```

## Features

- **PDF/DOCX Resume Processing**: Extract text from uploaded resume files
- **ATS Compatibility Analysis**: Evaluate resume structure, formatting, and keyword usage
- **Job Matching Analysis**: Compare resume against job descriptions
- **AI-Powered Insights**: Use OpenAI GPT-4 for intelligent analysis
- **RESTful API**: Clean HTTP endpoints for frontend integration
- **Extensible Architecture**: Easy to add new analysis types or integrations

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
# Create .env file
echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
```

### 3. Run the Server

```bash
# Development server
python main.py

# Or with uvicorn directly
uvicorn src.infrastructure.web.fastapi_app:app --reload --host 0.0.0.0 --port 8000
```

### 4. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Upload resume
curl -X POST "http://localhost:8000/api/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_resume.pdf"

# Analyze resume
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Your resume text here...",
    "mode": "ats"
  }'
```

## API Endpoints

### Core Endpoints

- `GET /health` - Health check
- `POST /api/upload` - Upload and process resume file
- `POST /api/analyze` - Analyze resume (ATS or job matching)
- `GET /api/analysis/{id}` - Get analysis result by ID

### Request/Response Examples

#### Upload Resume
```json
POST /api/upload
Content-Type: multipart/form-data

Response:
{
  "success": true,
  "message": "Resume uploaded and processed successfully",
  "resume_id": "uuid-here",
  "extracted_text": "Resume text preview..."
}
```

#### Analyze Resume
```json
POST /api/analyze
{
  "resume_text": "Full resume text...",
  "job_description": "Job description text...", // optional
  "mode": "ats" // or "job_match"
}

Response:
{
  "id": "analysis-uuid",
  "mode": "ats",
  "score": 8,
  "score_level": "good",
  "feedback": "<div>HTML formatted feedback</div>",
  "recommendations": ["Add more keywords", "Improve formatting"],
  "strengths": ["Good structure", "Clear contact info"],
  "weaknesses": ["Missing certifications"],
  "missing_keywords": [],
  "matched_keywords": ["Python", "React"],
  "timestamp": "2024-01-01T12:00:00"
}
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY` - OpenAI API key for AI analysis
- `DATABASE_URL` - Database connection string (optional)
- `MAX_FILE_SIZE_MB` - Maximum upload file size (default: 5)
- `CORS_ORIGINS` - Allowed CORS origins (default: *)

### AI Prompts

The AI analysis prompts are defined in the `AIAnalysisAdapter` class and can be customized for different analysis types:

- **ATS Analysis**: Focuses on resume structure, formatting, and ATS compatibility
- **Job Matching**: Compares resume content against job requirements

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Code Quality

```bash
# Format code
black src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

### Adding New Analysis Types

1. Create new analysis mode in `domain/entities/resume.py`
2. Add analysis logic in `application/services/resume_analysis_service.py`
3. Update AI prompts in `infrastructure/adapters/ai_analysis_adapter.py`
4. Add API endpoint in `infrastructure/web/fastapi_app.py`

## Deployment

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "src.infrastructure.web.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Cloud Deployment Options

- **Railway**: `railway up` (with railway.json config)
- **Heroku**: Standard Python buildpack
- **AWS Lambda**: Use Mangum adapter for serverless
- **Google Cloud Run**: Container-based deployment
- **DigitalOcean App Platform**: Direct GitHub integration

### Production Considerations

1. **Database**: Replace in-memory repository with PostgreSQL/MongoDB
2. **File Storage**: Use cloud storage (S3, GCS) for uploaded files
3. **Rate Limiting**: Add rate limiting for API endpoints
4. **Monitoring**: Add logging, metrics, and health checks
5. **Security**: Implement authentication and input validation
6. **Caching**: Cache analysis results for performance

## Integration with Frontend

The backend is designed to work seamlessly with the React frontend. Update the frontend's `AnalysisService.ts` to call the real API endpoints:

```typescript
// Replace mock implementation with real API calls
const response = await fetch('http://localhost:8000/api/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ resume_text, job_description, mode })
});
```

## Contributing

1. Follow hexagonal architecture principles
2. Write tests for new features
3. Update documentation
4. Follow Python code style guidelines
5. Add type hints for all functions

## License

MIT License - see LICENSE file for details
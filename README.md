# Resume Scanner

A full-stack application for analyzing resumes using AI, built with React (Frontend) and FastAPI (Backend).

## 🏗️ Project Structure

```
resume-scanner/
├── frontend/                 # React + Vite application
│   ├── src/                 # React source code
│   ├── package.json         # Frontend dependencies
│   ├── vite.config.ts       # Vite configuration
│   ├── tailwind.config.js   # Tailwind CSS configuration
│   └── index.html           # Entry HTML file
├── backend/                 # FastAPI application
│   ├── src/                 # Python source code (Hexagonal Architecture)
│   ├── pyproject.toml       # Poetry dependencies
│   ├── main.py              # Application entry point
│   └── requirements.txt     # Legacy pip dependencies
├── Makefile                 # Build and development commands
├── start-services.sh        # Service starter script
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v18 or higher)
- **Python** (3.12 or higher)
- **Poetry** (for backend dependency management)

### Installation & Setup

```bash
# Clone the repository
git clone <repository-url>
cd resume-scanner

# Complete setup (frontend + backend)
make setup

# Start both services
make dev
```

### Service URLs

Once running, access the services at:

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🛠️ Development Commands

### Using Make (Recommended)

```bash
# See all available commands
make help

# Development
make dev                    # Start both frontend and backend
make dev-frontend          # Start only frontend
make dev-backend           # Start only backend
make dev-backend-bg        # Start backend in background

# Installation
make install               # Install all dependencies
make install-frontend      # Install frontend dependencies
make install-backend       # Install backend dependencies

# Building
make build                 # Build both applications
make build-frontend        # Build frontend for production
make build-backend         # Build backend

# Code Quality
make lint                  # Lint both frontend and backend
make test                  # Run tests for both applications

# Service Management
make stop                  # Stop all running services
make check-ports           # Check port availability
make health                # Check service health
```

### Poetry Commands (Backend)

```bash
# From project root
make poetry-install        # Install Poetry dependencies
make poetry-add package=requests     # Add new dependency
make poetry-add-dev package=pytest   # Add development dependency
make poetry-update         # Update all dependencies
make poetry-lock           # Generate lock file
```

## 🏛️ Architecture

### Frontend (React + Vite)
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **State Management**: React Hooks
- **HTTP Client**: Fetch API

### Backend (FastAPI)
- **Framework**: FastAPI with Python 3.12
- **Architecture**: Hexagonal Architecture (Ports & Adapters)
- **Dependency Management**: Poetry
- **File Processing**: PDF/DOCX parsing
- **AI Integration**: OpenAI GPT-4
- **Database**: In-memory (configurable for production)

## 📁 Directory Structure

### Frontend (`/frontend`)
```
frontend/
├── src/
│   ├── components/        # React components
│   ├── services/          # API services
│   ├── types/            # TypeScript type definitions
│   ├── utils/            # Utility functions
│   └── App.tsx           # Main application component
├── package.json          # Dependencies and scripts
├── vite.config.ts        # Vite configuration
├── tailwind.config.js    # Tailwind CSS configuration
└── index.html            # Entry point
```

### Backend (`/backend`)
```
backend/
├── src/
│   ├── domain/           # Core business logic
│   │   ├── entities/     # Business entities
│   │   └── value_objects/ # Domain value objects
│   ├── application/      # Application services
│   │   ├── ports/        # Interfaces/contracts
│   │   └── services/     # Business logic implementation
│   └── infrastructure/   # External concerns
│       ├── adapters/     # External service adapters
│       ├── repositories/ # Data persistence
│       └── web/          # Web framework (FastAPI)
├── main.py               # Application entry point
├── pyproject.toml        # Poetry dependencies
└── requirements.txt      # Legacy pip dependencies
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# Backend (.env)
OPENAI_API_KEY=your-openai-api-key-here
DATABASE_URL=postgresql://user:pass@localhost/dbname  # Optional
MAX_FILE_SIZE_MB=5
CORS_ORIGINS=http://localhost:5173
```

### Frontend Configuration

The frontend is configured through:
- `frontend/vite.config.ts` - Build and development settings
- `frontend/tailwind.config.js` - Styling configuration
- `frontend/tsconfig.json` - TypeScript configuration

## 🧪 Testing

```bash
# Run all tests
make test

# Frontend tests
make test-frontend

# Backend tests
make test-backend
```

## 🚀 Deployment

### Frontend Deployment
```bash
# Build for production
make build-frontend

# Deploy to static hosting (Netlify, Vercel, etc.)
# The built files will be in frontend/dist/
```

### Backend Deployment
```bash
# Using Docker
docker build -t resume-scanner-backend ./backend
docker run -p 8000:8000 resume-scanner-backend

# Using Poetry
cd backend
poetry install --only=main
poetry run uvicorn src.infrastructure.web.fastapi_app:app --host 0.0.0.0 --port 8000
```

## 🤝 Contributing

1. Follow the existing code structure and patterns
2. Write tests for new features
3. Update documentation
4. Use the provided Make commands for development
5. Follow the established coding standards

## 📚 Additional Documentation

- [Backend README](./backend/README.md) - Detailed backend documentation
- [Poetry Setup Guide](./backend/POETRY_README.md) - Poetry configuration and usage
- [Frontend Documentation](./frontend/README.md) - Frontend-specific documentation

## 📄 License

MIT License - see LICENSE file for details

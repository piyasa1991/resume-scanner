# Resume Scanner - Makefile
# Bootstrap frontend and backend servers

.PHONY: help install install-frontend install-backend dev dev-frontend dev-backend build build-frontend build-backend clean clean-frontend clean-backend lint lint-frontend lint-backend test test-frontend test-backend setup setup-frontend setup-backend

# Default target
help:
	@echo "🚀 Resume Scanner - Available Commands:"
	@echo ""
	@echo "📦 Installation:"
	@echo "  install          - Install dependencies for both frontend and backend"
	@echo "  install-frontend - Install frontend dependencies (npm install)"
	@echo "  install-backend  - Install backend dependencies (pip install)"
	@echo ""
	@echo "🔄 Development:"
	@echo "  dev              - Start both frontend and backend in development mode"
	@echo "  dev-frontend     - Start frontend development server (npm run dev)"
	@echo "  dev-backend      - Start backend development server (python main.py)"
	@echo "  dev-backend-bg   - Start backend in background"
	@echo "  stop             - Stop all running services"
	@echo "  check-ports      - Check if required ports are available"
	@echo ""
	@echo "🏗️  Build:"
	@echo "  build            - Build both frontend and backend"
	@echo "  build-frontend   - Build frontend for production (npm run build)"
	@echo "  build-backend    - Build backend (no build step needed)"
	@echo ""
	@echo "🧹 Clean:"
	@echo "  clean            - Clean both frontend and backend"
	@echo "  clean-frontend   - Clean frontend build artifacts"
	@echo "  clean-backend    - Clean backend cache and artifacts"
	@echo ""
	@echo "🔍 Linting:"
	@echo "  lint             - Lint both frontend and backend"
	@echo "  lint-frontend    - Lint frontend code (npm run lint)"
	@echo "  lint-backend     - Lint backend code (black, flake8)"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  test             - Run tests for both frontend and backend"
	@echo "  test-frontend    - Run frontend tests"
	@echo "  test-backend     - Run backend tests (pytest)"
	@echo ""
	@echo "⚙️  Setup:"
	@echo "  setup            - Complete setup (install + setup env)"
	@echo "  setup-frontend   - Setup frontend environment"
	@echo "  setup-backend    - Setup backend environment"
	@echo ""
	@echo "📦 Poetry (Backend):"
	@echo "  poetry-install   - Install Poetry dependencies"
	@echo "  poetry-add       - Add new dependency (make poetry-add package=requests)"
	@echo "  poetry-add-dev   - Add dev dependency (make poetry-add-dev package=pytest)"
	@echo "  poetry-update    - Update all dependencies"
	@echo "  poetry-lock      - Generate lock file"

# Installation targets
install: install-frontend install-backend

install-frontend:
	@echo "📦 Installing frontend dependencies..."
	@cd frontend && npm install
	@echo "✅ Frontend dependencies installed"

install-backend:
	@echo "📦 Installing backend dependencies with Poetry..."
	@cd backend && poetry install
	@echo "✅ Backend dependencies installed"

# Development targets
dev: dev-backend-bg dev-frontend

dev-frontend:
	@echo "🚀 Starting frontend development server..."
	@echo "📱 Frontend will be available at: http://localhost:5173"
	@cd frontend && npm run dev

dev-backend:
	@echo "🚀 Starting backend development server..."
	@echo "🔗 Backend will be available at: http://localhost:8000"
	@echo "📚 API Documentation: http://localhost:8000/docs"
	@cd backend && poetry run python main.py

dev-backend-bg:
	@echo "🚀 Starting backend development server in background..."
	@echo "🔗 Backend will be available at: http://localhost:8000"
	@echo "📚 API Documentation: http://localhost:8000/docs"
	@cd backend && poetry run python main.py &
	@sleep 3
	@echo "✅ Backend started in background"

# Build targets
build: build-frontend build-backend

build-frontend:
	@echo "🏗️  Building frontend for production..."
	@cd frontend && npm run build
	@echo "✅ Frontend built successfully"

build-backend:
	@echo "🏗️  Backend build step (no build required for Python)"
	@echo "✅ Backend ready for deployment"

# Clean targets
clean: clean-frontend clean-backend

clean-frontend:
	@echo "🧹 Cleaning frontend build artifacts..."
	@rm -rf frontend/dist
	@rm -rf frontend/node_modules/.vite
	@echo "✅ Frontend cleaned"

clean-backend:
	@echo "🧹 Cleaning backend cache and artifacts..."
	@cd backend && find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@cd backend && find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@cd backend && find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "✅ Backend cleaned"

# Linting targets
lint: lint-frontend lint-backend

lint-frontend:
	@echo "🔍 Linting frontend code..."
	@cd frontend && npm run lint
	@echo "✅ Frontend linting complete"

lint-backend:
	@echo "🔍 Linting backend code..."
	@cd backend && poetry run black src/ --check
	@cd backend && poetry run flake8 src/ --max-line-length=88 --extend-ignore=E203,W503
	@echo "✅ Backend linting complete"

# Testing targets
test: test-frontend test-backend

test-frontend:
	@echo "🧪 Running frontend tests..."
	@echo "⚠️  No frontend tests configured yet"
	@echo "✅ Frontend testing complete"

test-backend:
	@echo "🧪 Running backend tests..."
	@cd backend && poetry run pytest tests/ -v
	@echo "✅ Backend testing complete"

# Setup targets
setup: setup-frontend setup-backend

setup-frontend:
	@echo "⚙️  Setting up frontend environment..."
	@cd frontend && npm install
	@echo "✅ Frontend setup complete"

setup-backend:
	@echo "⚙️  Setting up backend environment..."
	@cd backend && poetry install
	@echo "✅ Backend setup complete"

# Additional utility targets
logs:
	@echo "📋 Showing recent logs..."
	@echo "Frontend logs:"
	@echo "Backend logs:"

restart: clean install dev

# Docker targets (if needed in the future)
docker-build:
	@echo "🐳 Building Docker images..."
	@echo "⚠️  Docker configuration not set up yet"

docker-run:
	@echo "🐳 Running with Docker..."
	@echo "⚠️  Docker configuration not set up yet"

# Production targets
prod-build: build
	@echo "🚀 Production build complete"

prod-run:
	@echo "🚀 Starting production servers..."
	@echo "⚠️  Production configuration not set up yet"

# Poetry-specific targets
poetry-install:
	@echo "📦 Installing Poetry dependencies..."
	@cd backend && poetry install
	@echo "✅ Poetry dependencies installed"

poetry-add:
	@echo "📦 Adding new dependency..."
	@cd backend && poetry add $(package)
	@echo "✅ Dependency added"

poetry-add-dev:
	@echo "📦 Adding new development dependency..."
	@cd backend && poetry add --group dev $(package)
	@echo "✅ Development dependency added"

poetry-update:
	@echo "🔄 Updating Poetry dependencies..."
	@cd backend && poetry update
	@echo "✅ Dependencies updated"

poetry-lock:
	@echo "🔒 Generating Poetry lock file..."
	@cd backend && poetry lock
	@echo "✅ Lock file generated"

# Service management
stop:
	@echo "🛑 Stopping all services..."
	@pkill -f "python main.py" || true
	@pkill -f "vite" || true
	@echo "✅ Services stopped"

check-ports:
	@echo "🔍 Checking port availability..."
	@echo "Port 8000 (Backend):"
	@lsof -ti:8000 > /dev/null 2>&1 && echo "❌ Port 8000 is in use" || echo "✅ Port 8000 is available"
	@echo "Port 5173 (Frontend):"
	@lsof -ti:5173 > /dev/null 2>&1 && echo "❌ Port 5173 is in use" || echo "✅ Port 5173 is available"

# Health check
health:
	@echo "🏥 Checking service health..."
	@echo "Frontend: http://localhost:5173"
	@echo "Backend: http://localhost:8000/health"
	@curl -s http://localhost:8000/health || echo "Backend not running" 
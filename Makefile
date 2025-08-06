# Resume Scanner - Makefile
# Simple and clean development commands

.PHONY: help install dev build lint test clean

# Default target
help:
	@echo "🚀 Resume Scanner - Available Commands:"
	@echo ""
	@echo "📦 Installation:"
	@echo "  install          - Install dependencies for both frontend and backend"
	@echo ""
	@echo "🔄 Development:"
	@echo "  dev              - Start both frontend and backend in development mode"
	@echo ""
	@echo "🏗️  Build:"
	@echo "  build            - Build both frontend and backend for production"
	@echo ""
	@echo "🔍 Code Quality:"
	@echo "  lint             - Lint both frontend and backend code"
	@echo "  test             - Run tests for both frontend and backend"
	@echo ""
	@echo "🧹 Clean:"
	@echo "  clean            - Clean build artifacts and cache"

# Installation
install:
	@echo "📦 Installing dependencies..."
	@cd frontend && npm install
	@cd backend && poetry config virtualenvs.in-project true
	@cd backend && poetry install
	@echo "✅ Dependencies installed"

# Development
dev:
	@echo "🚀 Starting development servers..."
	@echo "📱 Frontend: http://localhost:5173"
	@echo "🔗 Backend: http://localhost:8000"
	@echo "📚 API Docs: http://localhost:8000/docs"
	@cd backend && poetry run python main.py &
	@sleep 3
	@cd frontend && npm run dev

# Build
build:
	@echo "🏗️  Building applications..."
	@cd frontend && npm run build
	@echo "✅ Applications built"

# Lint
lint:
	@echo "🔍 Linting code..."
	@cd frontend && npm run lint
	@cd backend && poetry run black src/ --check
	@cd backend && poetry run flake8 src/ --max-line-length=88 --extend-ignore=E203,W503
	@echo "✅ Linting complete"

# Test
test:
	@echo "🧪 Running tests..."
	@cd backend && poetry run pytest tests/ -v
	@echo "✅ Tests complete"

# Clean
clean:
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf frontend/dist
	@rm -rf frontend/node_modules/.vite
	@rm -rf backend/.venv
	@cd backend && find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@cd backend && find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Clean complete" 
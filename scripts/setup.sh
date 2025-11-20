#!/bin/bash
# EvoForge setup script

set -e

echo "======================================"
echo "  EvoForge Setup Script"
echo "======================================"
echo ""

# Check prerequisites
echo "Checking prerequisites..."

# Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi
echo "✅ Docker found"

# Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose first."
    exit 1
fi
echo "✅ Docker Compose found"

# Python (for local development)
if ! command -v python3 &> /dev/null; then
    echo "⚠️  Python3 not found. Skipping local development setup."
    SKIP_PYTHON=true
else
    echo "✅ Python3 found"
fi

# Node (for frontend development)
if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js not found. Skipping frontend development setup."
    SKIP_NODE=true
else
    echo "✅ Node.js found"
fi

echo ""
echo "Setting up EvoForge..."
echo ""

# Create .env file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "Creating backend/.env from template..."
    cp backend/.env.example backend/.env
    echo "⚠️  Please edit backend/.env and add your API keys!"
else
    echo "✅ backend/.env already exists"
fi

# Pull required Docker images
echo ""
echo "Pulling Docker images (this may take a while)..."
docker-compose pull

# Build custom images
echo ""
echo "Building EvoForge images..."
docker-compose build

# Optional: Set up Python virtual environment
if [ -z "$SKIP_PYTHON" ]; then
    echo ""
    read -p "Set up Python virtual environment for backend development? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd backend
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        echo "✅ Python virtual environment created and dependencies installed"
        cd ..
    fi
fi

# Optional: Install frontend dependencies
if [ -z "$SKIP_NODE" ]; then
    echo ""
    read -p "Install frontend dependencies? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd frontend
        npm install
        echo "✅ Frontend dependencies installed"
        cd ..
    fi
fi

echo ""
echo "======================================"
echo "  Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "  1. Edit backend/.env and add your API keys"
echo "  2. Run 'docker-compose up' to start EvoForge"
echo "  3. Access the platform:"
echo "     - Frontend: http://localhost:3000"
echo "     - Backend API: http://localhost:8000"
echo "     - Ray Dashboard: http://localhost:8265"
echo "     - API Docs: http://localhost:8000/docs"
echo ""
echo "For development:"
echo "  Backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "  Frontend: cd frontend && npm run dev"
echo ""
echo "Happy evolving! 🧬"

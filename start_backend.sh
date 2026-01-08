#!/bin/bash

# RAG Pipeline Optimizer - Backend Startup Script

echo "🚀 Starting RAG Pipeline Optimizer Backend..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check for .env file
if [ -f ".env" ]; then
    echo "📄 Loading environment variables from .env"
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️  No .env file found - running in MOCK MODE"
    echo "   To use real LLM execution:"
    echo "   1. Copy .env.example to .env"
    echo "   2. Add your OPENAI_API_KEY"
    export MOCK_MODE=true
fi

echo ""
echo "🌐 Starting FastAPI server at http://127.0.0.1:8000"
echo "📚 API docs available at http://127.0.0.1:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn backend.main:app --reload

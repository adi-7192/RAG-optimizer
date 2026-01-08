#!/bin/bash

# RAG Pipeline Optimizer - Frontend Startup Script

echo "🎨 Starting RAG Pipeline Optimizer Frontend..."
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

# Check if backend is running
if ! curl -s http://127.0.0.1:8000 > /dev/null 2>&1; then
    echo "⚠️  Backend not detected at http://127.0.0.1:8000"
    echo "   Please start the backend first:"
    echo "   ./start_backend.sh"
    echo ""
    echo "   Continuing anyway - you can start backend later"
    echo ""
fi

echo "🌐 Starting Streamlit dashboard..."
echo "   The app will open in your browser automatically"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run frontend/app.py

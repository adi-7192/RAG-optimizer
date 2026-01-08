# RAG Pipeline Optimizer - Walkthrough

This guide will help you run the prototype RAG Pipeline Optimizer.

## Prerequisites
- Python 3.8+
- OpenAI API Key (Optional, for real execution. If not provided, the system runs in Mock Mode).

## 1. Setup

First, ensure you are in the project directory:
```bash
cd "/Users/adi7192/Documents/RAG optimizer"
```

Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## 2. Running the Backend

Start the FastAPI server in a new terminal window:
```bash
# If you have an OpenAI Key, export it first:
# export OPENAI_API_KEY="sk-..."
uvicorn backend.main:app --reload
```
*The backend will start at `http://127.0.0.1:8000`.*

## 3. Running the Frontend

Start the Streamlit dashboard in another terminal window:
```bash
streamlit run frontend/app.py
```
*The dashboard will open in your browser (usually `http://localhost:8501`).*

## 4. Usage Guide

1.  **Upload Documents**:
    - Go to the sidebar.
    - Click "Browse files" and select a PDF or Text file.
    - Click "Ingest Documents".
    
2.  **Select Pipelines**:
    - In the sidebar, select which pipelines you want to compare (e.g., "Fast & Cheap" vs "High Accuracy").

3.  **Run Experiment**:
    - Enter a question in the main text box.
    - Click "Run Experiment".

4.  **View Results**:
    - The "Pipeline Results" section shows the answer, context, latency, and cost for each pipeline.
    - The "Evaluation Leaderboard" shows the AI-graded scores for Accuracy and Relevance.
    - Charts visualize the comparison.

## 5. Mock Mode
If you do not provide an `OPENAI_API_KEY`, the system automatically runs in **Mock Mode**.
- It will return simulated answers.
- It will return simulated evaluation scores.
- This is useful for demonstrating the UI without incurring costs.

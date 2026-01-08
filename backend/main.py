from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
import os
import shutil
from .models import RunPipelineRequest, PipelineResult, EvaluationRequest, EvaluationResult
from .pipeline_runner import PipelineRunner
from .evaluator import Evaluator
from .config import load_pipeline_configs

app = FastAPI(title="RAG Pipeline Optimizer API")

# Global state for prototype (in production, use a database/cache)
runner = PipelineRunner()
evaluator = Evaluator()
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "RAG Pipeline Optimizer API is running"}

@app.get("/pipelines")
def list_pipelines():
    configs = load_pipeline_configs()
    return {"pipelines": [c.dict() for c in configs.values()]}

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    saved_paths = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_paths.append(file_path)
    
    # Ingest immediately for prototype simplicity
    runner.ingest_documents(saved_paths)
    
    return {"message": f"Uploaded {len(files)} files", "files": [f.filename for f in files]}

@app.post("/run", response_model=List[PipelineResult])
def run_pipelines(request: RunPipelineRequest):
    results = []
    for pipeline_name in request.selected_pipelines:
        try:
            result = runner.run_pipeline(pipeline_name, request.question)
            results.append(result)
        except Exception as e:
            # Return error as a result so UI doesn't crash
            results.append(PipelineResult(
                pipeline_name=pipeline_name,
                answer=f"Error: {str(e)}",
                context=[],
                metrics={},
                cost_estimate=0.0,
                latency=0.0
            ))
    return results

@app.post("/evaluate", response_model=List[EvaluationResult])
def evaluate_results(request: EvaluationRequest):
    return evaluator.evaluate(request.question, request.pipeline_results)

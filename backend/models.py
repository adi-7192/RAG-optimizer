from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class PipelineConfig(BaseModel):
    name: str
    chunk_size: int
    chunk_overlap: int
    embedding_model: str
    llm_model: str
    top_k: int = 3

class PipelineResult(BaseModel):
    pipeline_name: str
    answer: str
    context: List[str]
    metrics: Optional[Dict[str, float]] = None
    cost_estimate: float = 0.0
    latency: float = 0.0

class EvaluationRequest(BaseModel):
    question: str
    pipeline_results: List[PipelineResult]

class EvaluationResult(BaseModel):
    pipeline_name: str
    accuracy_score: float
    relevance_score: float
    cost_score: float
    overall_score: float
    reasoning: str

class RunPipelineRequest(BaseModel):
    question: str
    selected_pipelines: List[str]  # List of pipeline names to run

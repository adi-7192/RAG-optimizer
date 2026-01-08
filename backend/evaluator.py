import os
from typing import List
from .models import PipelineResult, EvaluationResult

class Evaluator:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.mock_mode = os.getenv("MOCK_MODE", "false").lower() == "true" or not self.api_key

    def evaluate(self, question: str, results: List[PipelineResult]) -> List[EvaluationResult]:
        evaluations = []
        
        for res in results:
            if self.mock_mode:
                # Mock evaluation
                evaluations.append(EvaluationResult(
                    pipeline_name=res.pipeline_name,
                    accuracy_score=0.8 + (len(res.answer) % 10) / 100, # Random-ish
                    relevance_score=0.9,
                    cost_score=1.0 if res.cost_estimate < 0.01 else 0.5,
                    overall_score=0.85,
                    reasoning="[Mock] Good answer, relevant context."
                ))
                continue

            # Real Evaluation using LLM
            # We ask the LLM to grade the answer 0-10
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            
            prompt = f"""
            Question: {question}
            Context Used: {res.context}
            Answer: {res.answer}
            
            Evaluate this RAG response on:
            1. Accuracy (0-10): Is it factually correct based on context?
            2. Relevance (0-10): Does it answer the user's question?
            
            Return format:
            Accuracy: <score>
            Relevance: <score>
            Reasoning: <text>
            """
            
            try:
                response = client.chat.completions.create(
                    model="gpt-4", # Use a strong model for evaluation
                    messages=[{"role": "system", "content": "You are an expert RAG evaluator."},
                              {"role": "user", "content": prompt}]
                )
                content = response.choices[0].message.content
                
                # Naive parsing for prototype
                accuracy = 0.0
                relevance = 0.0
                reasoning = content
                
                lines = content.split('\n')
                for line in lines:
                    if "Accuracy:" in line:
                        try:
                            accuracy = float(line.split(":")[1].strip()) / 10.0
                        except: pass
                    if "Relevance:" in line:
                        try:
                            relevance = float(line.split(":")[1].strip()) / 10.0
                        except: pass
                
                evaluations.append(EvaluationResult(
                    pipeline_name=res.pipeline_name,
                    accuracy_score=accuracy,
                    relevance_score=relevance,
                    cost_score=1.0, # Placeholder
                    overall_score=(accuracy + relevance) / 2,
                    reasoning=reasoning
                ))
            except Exception as e:
                print(f"Evaluation failed: {e}")
                evaluations.append(EvaluationResult(
                    pipeline_name=res.pipeline_name,
                    accuracy_score=0, relevance_score=0, cost_score=0, overall_score=0,
                    reasoning=f"Error: {str(e)}"
                ))

        return evaluations

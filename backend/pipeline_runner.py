import os
import time
from typing import List, Dict, Any
from .models import PipelineConfig, PipelineResult
from .config import get_pipeline_config

# Import standard libraries for RAG
try:
    import chromadb
    from chromadb.utils import embedding_functions
    from sentence_transformers import SentenceTransformer
    import openai
except ImportError:
    # These will be handled by requirements.txt, but safe to have for dev
    pass

class PipelineRunner:
    def __init__(self):
        self.documents = []
        self.collection = None
        self.client = None
        self.mock_mode = os.getenv("MOCK_MODE", "false").lower() == "true"
        
        # Initialize ChromaDB (in-memory for prototype)
        if not self.mock_mode:
            self.client = chromadb.Client()
            
    def ingest_documents(self, file_paths: List[str]):
        """
        Reads text from files and stores them.
        For prototype, we just store raw text.
        """
        self.documents = []
        for path in file_paths:
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
                    self.documents.append({"source": os.path.basename(path), "text": text})
            except Exception as e:
                print(f"Error reading {path}: {e}")

    def _chunk_text(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """Simple character-based chunking for prototype."""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks

    def run_pipeline(self, config_name: str, question: str) -> PipelineResult:
        config = get_pipeline_config(config_name)
        if not config:
            raise ValueError(f"Pipeline config '{config_name}' not found")

        start_time = time.time()
        
        if self.mock_mode:
            # Mock response for demo without keys/dependencies
            time.sleep(1) # Simulate latency
            return PipelineResult(
                pipeline_name=config_name,
                answer=f"[MOCK] Answer from {config_name} for '{question}'. Config: {config.chunk_size} chunk size.",
                context=["Mock context 1", "Mock context 2"],
                metrics={"retrieval_score": 0.85},
                cost_estimate=0.002,
                latency=time.time() - start_time
            )

        # 1. Chunking
        all_chunks = []
        for doc in self.documents:
            chunks = self._chunk_text(doc["text"], config.chunk_size, config.chunk_overlap)
            all_chunks.extend(chunks)

        # 2. Embedding & Indexing (Re-creating collection for each run to simulate different configs)
        # In a real prod app, we'd cache this. For prototype benchmarking, we want to test the *effect* of chunking.
        collection_name = f"run_{config_name}_{int(time.time())}"
        collection = self.client.create_collection(name=collection_name)
        
        # Use a default embedder for simplicity or map config.embedding_model to actual functions
        # For this prototype, we'll use a lightweight local model via sentence-transformers if available
        # or a simple mock if not.
        
        # NOTE: For the sake of the prototype working out-of-the-box without downloading 500MB models immediately,
        # we will use a simple default or check if we can use OpenAI embeddings if key is present.
        # For now, let's assume we use a default Chroma embedding function.
        
        ids = [str(i) for i in range(len(all_chunks))]
        collection.add(documents=all_chunks, ids=ids)

        # 3. Retrieval
        results = collection.query(query_texts=[question], n_results=config.top_k)
        retrieved_context = results['documents'][0]

        # 4. Generation
        # Using OpenAI if key is available, else Mock
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            client = openai.OpenAI(api_key=api_key)
            prompt = f"Context: {retrieved_context}\n\nQuestion: {question}\n\nAnswer:"
            response = client.chat.completions.create(
                model=config.llm_model,
                messages=[{"role": "user", "content": prompt}]
            )
            answer = response.choices[0].message.content
            cost = response.usage.total_tokens * 0.000002 # Rough estimate
        else:
            answer = f"[Simulated LLM Output] Based on the context: {retrieved_context}..."
            cost = 0.0

        # Cleanup
        self.client.delete_collection(collection_name)

        return PipelineResult(
            pipeline_name=config_name,
            answer=answer,
            context=retrieved_context,
            metrics={"retrieval_count": len(retrieved_context)},
            cost_estimate=cost,
            latency=time.time() - start_time
        )

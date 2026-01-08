# 🚀 RAG Pipeline Optimizer

> **Benchmark and optimize your RAG pipelines with data-driven insights**

A powerful tool to test, compare, and optimize different RAG (Retrieval-Augmented Generation) configurations side-by-side. Make informed decisions about chunk sizes, embedding models, and LLMs based on real performance metrics.

![RAG Pipeline Optimizer](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🎯 The Problem This Solves

### The RAG Configuration Dilemma

When building RAG applications, developers face critical questions:

- **"Should I use 512 or 1024 token chunks?"** 🤔
- **"Which embedding model gives the best results for my use case?"** 🔍
- **"Is GPT-4 worth the extra cost, or will GPT-3.5-turbo suffice?"** 💰
- **"How do different configurations affect accuracy vs. cost?"** ⚖️

### The Current Approach is Broken

Most developers either:
1. **Guess based on blog posts** - What works for others may not work for your data
2. **Stick with defaults** - Missing potential 2-3x improvements in quality or cost
3. **Test manually** - Time-consuming, inconsistent, hard to compare
4. **Build custom benchmarking tools** - Reinventing the wheel for each project

### Our Solution

**RAG Pipeline Optimizer** lets you:
- ✅ **Test multiple RAG configurations in parallel** with a single click
- ✅ **Compare results side-by-side** with objective metrics
- ✅ **Get AI-powered evaluation** of accuracy and relevance
- ✅ **Track costs and latency** for each configuration
- ✅ **Make data-driven decisions** instead of guessing

**Result**: Find the optimal RAG configuration for your specific use case in minutes, not days.

---

## ✨ Features

### 🔄 Parallel Pipeline Testing
Run multiple RAG configurations simultaneously:
- Different chunk sizes (512, 768, 1024 tokens)
- Various embedding models (MiniLM, MPNet, etc.)
- Multiple LLMs (GPT-3.5, GPT-4, GPT-4-turbo)
- Configurable retrieval parameters (top-k, overlap)

### 📊 Comprehensive Metrics
Track what matters:
- **Accuracy Score** - How factually correct is the answer?
- **Relevance Score** - Does it answer the question?
- **Cost Estimate** - API costs per query
- **Latency** - Response time in seconds
- **Overall Score** - Weighted combination

### 🤖 AI-Powered Evaluation
LLM-based evaluation agent that:
- Judges answer quality objectively
- Provides detailed reasoning
- Compares against retrieved context
- Ranks pipelines by performance

### 📈 Visual Analytics
- Side-by-side answer comparison
- Performance leaderboards
- Interactive charts
- Cost vs. quality trade-offs

### 🎮 Easy-to-Use Interface
- Drag-and-drop document upload
- One-click pipeline selection
- Real-time results
- No coding required for testing

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                    │
│              (Interactive Dashboard & UI)                │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP/REST
┌─────────────────────▼───────────────────────────────────┐
│                    FastAPI Backend                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Pipeline   │  │  Evaluator   │  │   Config     │  │
│  │   Runner     │  │   Agent      │  │   Manager    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────┬───────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
┌───────▼──────┐ ┌───▼────┐ ┌─────▼─────┐
│   ChromaDB   │ │ OpenAI │ │ Sentence  │
│  (Vectors)   │ │  API   │ │Transformers│
└──────────────┘ └────────┘ └───────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- OpenAI API key (optional - works in mock mode without it)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/rag-pipeline-optimizer.git
   cd rag-pipeline-optimizer
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment** (Optional)
   
   For **Mock Mode** (no API key needed):
   ```bash
   export MOCK_MODE=true
   ```
   
   For **Real LLM Execution**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

### Running the Application

**Option 1: Using startup scripts (Recommended)**

Terminal 1 - Backend:
```bash
./start_backend.sh
```

Terminal 2 - Frontend:
```bash
./start_frontend.sh
```

**Option 2: Manual commands**

Terminal 1 - Backend:
```bash
source venv/bin/activate
uvicorn backend.main:app --reload
```

Terminal 2 - Frontend:
```bash
source venv/bin/activate
streamlit run frontend/app.py
```

### Access the Application
- **Frontend**: http://localhost:8501
- **API Docs**: http://127.0.0.1:8000/docs

---

## 📖 Usage Guide

### 1. Upload Documents
- Click "Browse files" in the sidebar
- Upload PDF or TXT files
- Click "Ingest Documents"

### 2. Select Pipelines
Choose which configurations to compare:
- **Fast & Cheap** - Optimized for speed and cost
- **High Accuracy** - Maximum quality, higher cost
- **Balanced** - Best of both worlds

### 3. Run Experiment
- Enter your test question
- Click "Run Experiment"
- Wait for results (typically 10-30 seconds)

### 4. Analyze Results
- Compare answers side-by-side
- Review evaluation scores
- Check cost and latency metrics
- View visual comparisons

### 5. Make Decisions
Based on the data:
- Choose the best configuration for your use case
- Optimize for cost, speed, or accuracy
- Fine-tune parameters in `configs/pipelines.yaml`

---

## 🎨 Screenshots

### Main Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### Pipeline Comparison
![Comparison](docs/screenshots/comparison.png)

### Evaluation Leaderboard
![Leaderboard](docs/screenshots/leaderboard.png)

---

## ⚙️ Configuration

### Adding Custom Pipelines

Edit `configs/pipelines.yaml`:

```yaml
pipelines:
  - name: "My Custom Pipeline"
    chunk_size: 800
    chunk_overlap: 80
    embedding_model: "all-MiniLM-L6-v2"
    llm_model: "gpt-4-turbo"
    top_k: 4
```

### Supported Embedding Models
- `all-MiniLM-L6-v2` (Fast, lightweight)
- `all-mpnet-base-v2` (Balanced)
- Custom sentence-transformers models

### Supported LLMs
- `gpt-3.5-turbo` (Fast, cheap)
- `gpt-4` (High quality)
- `gpt-4-turbo` (Balanced)
- Any OpenAI-compatible model

---

## 🧪 Mock Mode vs. Production Mode

### Mock Mode (Default without API key)
- ✅ No API costs
- ✅ Instant results
- ✅ Perfect for UI testing
- ✅ Demo-ready
- ⚠️ Simulated answers

### Production Mode (With OpenAI API key)
- ✅ Real RAG execution
- ✅ Actual LLM evaluation
- ✅ Accurate metrics
- ⚠️ API costs apply
- ⚠️ Slower (real API calls)

---

## 📊 Example Use Cases

### 1. Document Q&A Optimization
**Scenario**: Building a customer support chatbot  
**Goal**: Find the cheapest configuration that maintains 90%+ accuracy  
**Result**: Discovered GPT-3.5-turbo with 768 chunks saves 70% vs GPT-4 with minimal quality loss

### 2. Research Paper Analysis
**Scenario**: Academic research assistant  
**Goal**: Maximize accuracy for complex queries  
**Result**: GPT-4 with 1024 chunks and top-k=5 provides best results

### 3. Cost Optimization
**Scenario**: High-volume production application  
**Goal**: Reduce API costs while maintaining quality  
**Result**: Identified optimal chunk size that reduced costs by 40%

---

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.9+
- **Frontend**: Streamlit
- **Vector DB**: ChromaDB
- **Embeddings**: Sentence Transformers
- **LLMs**: OpenAI API
- **Data Processing**: Pandas, NumPy

---

## 📝 Project Structure

```
rag-pipeline-optimizer/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI app & endpoints
│   ├── models.py            # Pydantic models
│   ├── config.py            # Configuration loader
│   ├── pipeline_runner.py   # RAG pipeline execution
│   └── evaluator.py         # LLM-based evaluation
├── frontend/
│   └── app.py               # Streamlit dashboard
├── configs/
│   └── pipelines.yaml       # Pipeline configurations
├── data/                    # Uploaded documents
├── .env.example             # Environment template
├── .gitignore
├── requirements.txt
├── start_backend.sh         # Backend startup script
├── start_frontend.sh        # Frontend startup script
└── README.md
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- UI powered by [Streamlit](https://streamlit.io/)
- Vector search by [ChromaDB](https://www.trychroma.com/)
- Embeddings from [Sentence Transformers](https://www.sbert.net/)

---

## 📧 Contact

Have questions or suggestions? Open an issue or reach out!

---

## ⭐ Star History

If this project helped you optimize your RAG pipeline, please consider giving it a star! ⭐

---

**Made with ❤️ for the RAG community**

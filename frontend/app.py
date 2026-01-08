import streamlit as st
import requests
import pandas as pd
import json

# Configuration
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="RAG Pipeline Optimizer", layout="wide")

st.title("RAG Pipeline Optimizer 🚀")
st.markdown("Upload documents, configure pipelines, and benchmark results side-by-side.")

# Sidebar: Setup & Upload
with st.sidebar:
    st.header("1. Upload Data")
    uploaded_files = st.file_uploader("Upload Documents (PDF, TXT)", accept_multiple_files=True)
    
    if st.button("Ingest Documents"):
        if uploaded_files:
            files = [("files", (f.name, f, f.type)) for f in uploaded_files]
            try:
                response = requests.post(f"{API_URL}/upload", files=files)
                if response.status_code == 200:
                    st.success(f"Ingested {len(uploaded_files)} files!")
                else:
                    st.error(f"Error: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Backend not reachable. Is uvicorn running?")
        else:
            st.warning("Please select files first.")

    st.header("2. Select Pipelines")
    try:
        resp = requests.get(f"{API_URL}/pipelines")
        if resp.status_code == 200:
            available_pipelines = resp.json()["pipelines"]
            pipeline_names = [p["name"] for p in available_pipelines]
            selected_pipelines = st.multiselect("Choose pipelines to compare:", pipeline_names, default=pipeline_names[:2])
        else:
            st.error("Failed to fetch pipelines.")
            selected_pipelines = []
    except:
        st.error("Backend not reachable.")
        selected_pipelines = []

# Main Area: Execution
st.header("3. Run & Benchmark")
question = st.text_input("Enter your test question:", "What are the key safety protocols mentioned?")

if st.button("Run Experiment"):
    if not question or not selected_pipelines:
        st.warning("Please enter a question and select at least one pipeline.")
    else:
        with st.spinner("Running RAG pipelines..."):
            try:
                # Run Pipelines
                payload = {"question": question, "selected_pipelines": selected_pipelines}
                run_resp = requests.post(f"{API_URL}/run", json=payload)
                
                if run_resp.status_code == 200:
                    results = run_resp.json()
                    
                    # Display Raw Results
                    st.subheader("Pipeline Results")
                    cols = st.columns(len(results))
                    for i, res in enumerate(results):
                        with cols[i]:
                            st.info(f"**{res['pipeline_name']}**")
                            st.write(f"**Answer:** {res['answer']}")
                            with st.expander("View Context"):
                                st.write(res['context'])
                            st.write(f"Latency: {res['latency']:.2f}s")
                            st.write(f"Cost: ${res['cost_estimate']:.6f}")

                    # Run Evaluation
                    with st.spinner("Running AI Evaluator..."):
                        eval_payload = {"question": question, "pipeline_results": results}
                        eval_resp = requests.post(f"{API_URL}/evaluate", json=eval_payload)
                        
                        if eval_resp.status_code == 200:
                            evals = eval_resp.json()
                            
                            st.subheader("🏆 Evaluation Leaderboard")
                            
                            # Prepare Data for Table
                            data = []
                            for e in evals:
                                data.append({
                                    "Pipeline": e["pipeline_name"],
                                    "Overall Score": e["overall_score"],
                                    "Accuracy": e["accuracy_score"],
                                    "Relevance": e["relevance_score"],
                                    "Reasoning": e["reasoning"]
                                })
                            
                            df = pd.DataFrame(data)
                            st.dataframe(df.style.highlight_max(axis=0, subset=["Overall Score", "Accuracy", "Relevance"]), use_container_width=True)
                            
                            # Charts
                            st.subheader("Visual Comparison")
                            chart_data = df.set_index("Pipeline")[["Accuracy", "Relevance"]]
                            st.bar_chart(chart_data)
                            
                        else:
                            st.error("Evaluation failed.")
                else:
                    st.error(f"Pipeline run failed: {run_resp.text}")
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.caption("Prototype RAG Optimizer | Backend: FastAPI | Frontend: Streamlit")

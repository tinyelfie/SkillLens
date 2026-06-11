# SkillLens 🎯

SkillLens is an **LLM-powered, RAG-augmented Applicant Tracking System (ATS)**. 

It moves beyond simple keyword matching to evaluate true semantic competency alignment between a candidate's résumé and a job description. It extracts structured data via LLMs, maps skills into a 384-dimensional dense vector space, infers missing skills using a Directed Acyclic Graph (DAG) ontology, and rewrites résumés using context strictly grounded in Pinecone vector retrieval to eliminate hallucinations.

## Features
- **Zero-Shot Semantic Extraction:** Uses Gemini 2.0 Flash Lite to structure raw PDF/DOCX text into clean JSON.
- **Dual Vector Database:** Utilizes local ChromaDB for fast offline processing and cloud-based Pinecone for real-time Retrieval-Augmented Generation (RAG).
- **Skill Knowledge Graph:** Employs symbolic AI graph traversal to infer implicit skills (e.g., if you know PyTorch, you know Deep Learning).
- **LLM-as-a-Judge Guardrails:** Factual and semantic overlap checking ensures the AI does not hallucinate new experiences.
- **FastAPI Backend & UI Dashboard:** Lightning-fast backend serving a clean, minimalist web frontend.

## Quick Start

1. **Clone the repository**
2. **Set up virtual environment:**
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Set API Keys in `.env`:**
   ```
   GEMINI_API_KEY="your-gemini-key"
   PINECONE_API_KEY="your-pinecone-key"
   ```
4. **Run the server:**
   ```powershell
   python -m uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
   ```
5. **Access the Application:** Navigate to `http://127.0.0.1:8000` in your browser.


## Repository Structure
- `backend/`: FastAPI application and routing.
- `frontend/`: Web dashboard UI.
- `pipeline/`: Pure orchestration linking LLM, RAG, and extraction.
- `embeddings/`: Sentence-Transformers integration and ChromaDB.
- `retrieval/`: Pinecone integration and RAG logic.
- `ontology/`: Skill graph and symbolic inference logic.
- `llm/`: Google GenAI interface and configurations.
- `evaluation/`: LLM-as-a-judge and hallucination metrics.

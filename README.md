# 🧠 EngineIQ — Engineering Knowledge RAG System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.3+-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6B35?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-LLM-F55036?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

**Turn your engineering documentation into an intelligent, queryable knowledge base.**

</div>

---

## 📌 What is EngineIQ?

EngineIQ is a **Retrieval-Augmented Generation (RAG)** system built for engineering teams.  
It ingests your internal documentation — ADRs, runbooks, API specs, incident reports, policies — and lets you query it in natural language using a powerful LLM, grounded strictly in your own knowledge base.

> **No hallucinations. No guessing. Only answers backed by your own docs.**

---

## ✨ Features

| Feature | Details |
|---------|---------|
| 📄 **Multi-format Ingestion** | Supports `.md`, `.pdf`, and `.txt` documents |
| 🧹 **Smart Cleaning Pipeline** | OCR error fixing, boilerplate removal, deduplication — 10-step pipeline |
| ✂️ **Structure-Aware Chunking** | Respects Markdown headings and document hierarchy |
| 🔍 **3 Retrieval Strategies** | Similarity · MMR · Hybrid (BM25 + Semantic) |
| 🤖 **Groq LLM** | Fast inference with Llama, Qwen, or custom Groq-supported models |
| 🔗 **LangSmith Tracing** | Full observability for every query |
| 🎛️ **Streamlit UI** | Simple, clean chat interface with source attribution & sample questions |

---

## 🏗️ Architecture

```
Documents (PDF / MD / TXT)
        │
        ▼
  ┌─────────────┐
  │   loader    │  DirectoryLoader — multi-format support
  └──────┬──────┘
         │
         ▼
  ┌─────────────────────┐
  │  cleaning pipeline  │  10-step: noise removal → OCR fix → normalization
  └──────────┬──────────┘
             │
             ▼
  ┌───────────────────────┐
  │  structure-aware      │  Respects Markdown section hierarchy
  │  chunker              │  + metadata: title, section, parent
  └──────────┬────────────┘
             │
             ▼
  ┌──────────────────────┐
  │  HuggingFace         │  all-MiniLM-L6-v2 embeddings
  │  embeddings          │
  └──────────┬───────────┘
             │
             ▼
  ┌──────────────────────┐
  │  ChromaDB            │  Persistent local vector store
  └──────────┬───────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
 User Query      Retriever (Similarity / MMR / Hybrid)
    │                 │
    └────────┬────────┘
             │
             ▼
  ┌──────────────────────┐
  │   Groq LLM           │  Grounded answer generation
  │   + Prompt           │
  └──────────┬───────────┘
             │
             ▼
     Answer + Sources
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/ahmedyasser1588/RAG-System-Project-.git
cd RAG-System-Project-
```

### 2. Create a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
llm_api_key=your_groq_api_key
llm_model_name=openai/gpt-oss-20b
```

### 5. Build the vector database

```bash
python ingest.py
```

### 6. Launch the application

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
RAG-System-Project-/
├── app.py                      ← Streamlit entry point & UI
├── ingest.py                   ← Ingestion CLI script
├── requirements.txt
├── README.md
├── .env                        ← Local secrets (not committed)
├── .gitignore
├── .streamlit/
│   ├── config.toml             ← UI theme configuration
│   └── secrets.toml.example
│
├── src/                        ← Core package (PEP 8 compliant)
│   ├── __init__.py
│   ├── application/            ← Application service layer
│   │   ├── __init__.py
│   │   └── rag_service.py
│   ├── config/                 ← Settings & configuration
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── generation/             ← LLM & prompt engineering
│   │   ├── __init__.py
│   │   ├── llm.py
│   │   └── prompt.py
│   ├── ingestion/              ← Document loading & chunking
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   ├── chunker.py
│   │   ├── cleaning/           ← 10-step cleaning pipeline
│   │   │   ├── __init__.py
│   │   │   ├── cleaner.py
│   │   │   ├── normalizer.py
│   │   │   ├── rules.py
│   │   │   ├── document_cleaner.py
│   │   │   └── pipeline.py
│   │   └── chunking/           ← Structure-aware chunking
│   │       ├── __init__.py
│   │       ├── structure.py
│   │       └── structure_aware.py
│   └── retriever/              ← Embedding & vector storage
│       ├── __init__.py
│       ├── embedding.py
│       ├── vector_store.py
│       └── retriever.py
│
├── Data/
│   ├── Documents/              ← Source documents (.md, .pdf, .txt)
│   ├── Evaluation/             ← 30 evaluation questions
│   ├── MetaData/               ← Documents metadata registry
│   └── Vector_DB/              ← ChromaDB vector store
│
├── NoteBooks/                  ← Exploratory notebooks
│   ├── a.ipynb
│   ├── Anything.ipynb
│   └── Dummy.ipynb
│
└── tests/                      ← Unit tests
    └── test_cleaner.py
```

---

## 📄 License

This project is licensed under the MIT License.
